# Импорт библиотек и классов
from aiogram import types, filters, F, Router
from aiogram.fsm.context import FSMContext
import logging
import random as rd
import markups as mk
from create_bot import database, States
from functions import *


# Инициализация
router = Router()


### Хэндлеры запросов

@router.my_chat_member(filters.ChatMemberUpdatedFilter(filters.MEMBER >> filters.KICKED))
async def user_blocked_bot(event: types.ChatMemberUpdated):
    """
    A function that sets information about users who blocked the bot into the database.

    Args:
        event (types.ChatMemberUpdated): Event type.
    """
    user_id = event.from_user.id
    logging.info(f'Пользователь с id: {user_id} заблокировал бота')
    await database.set_dead(user_id)

@router.my_chat_member(filters.ChatMemberUpdatedFilter(filters.KICKED >> filters.MEMBER))
async def user_unblocked_bot(event: types.ChatMemberUpdated):
    """
    A function that sets information about users who blocked the bot into the database.

    Args:
        event (types.ChatMemberUpdated): Event type.
    """
    user_id = event.from_user.id
    logging.info(f'Пользователь с id: {user_id} разблокировал бота')
    await database.set_alive(user_id)


@router.callback_query(States.waiting_answer)
async def wait_for_answer_call_handler(call: types.CallbackQuery):
    """
    A function that warns the user to wait until the end of generation.

    Args:
        call (types.CallbackQuery): Event type.
    """
    try:
        await call.answer('Подождите конца генерации')
    except:
        pass


@router.callback_query(F.data == 'menu')
async def start_call_handler(call: types.CallbackQuery):
    """
    A function that allows user to go to main menu.

    Args:
        call (types.CallbackQuery): Event type.
    """
    await send_menu_message(call.message)

    try:
        await call.answer()
    except:
        pass


@router.callback_query(F.data == 'start')
async def edit_assistent_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to change his assistant.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    if not (await database.user_exists(call.from_user.id)):
        await database.add_user(call.from_user.id)

    await state.set_state(States.setting_assistent)
    await edit_assistent_choice_message(call.message)
    
    try:
        await call.answer()
    except:
        pass


@router.callback_query(F.data =='back')
async def backstage_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to go back 1 step via changing his state.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    match await state.get_state():
        case 'States:setting_assistent':
            await state.clear()
            await edit_menu_message(call.message)
        case 'States:setting_gender':
            await state.set_state(States.setting_assistent)
            await edit_assistent_choice_message(call.message)
        case 'States:setting_age':
            await state.set_state(States.setting_gender)
            await edit_gender_choice_message(call.message)
        case 'States:setting_budget':
            await state.set_state(States.setting_age)
            await edit_age_choice_message(call)
        case 'States:waiting_message':
            await state.set_state(States.setting_budget)
            await edit_budget_choice_message(call)
        
    try:
        await call.answer()
    except:
        pass
        

@router.callback_query(States.setting_assistent, F.data.in_(['multipurpose','designer','stylist','cosmetologist','nutritionist']))
async def set_assistent_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to choose his assistant.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    user_id = call.from_user.id
    await database.set_assistent(user_id, call.data)

    await state.set_state(States.setting_gender)
    await edit_gender_choice_message(call.message)

    try:
        await call.answer()
    except:
        pass


@router.callback_query(States.setting_gender, F.data.in_(['male','female']))
async def set_gender_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to set his gender.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    user_id = call.from_user.id
    await database.set_gender(user_id, call.data)

    await state.set_state(States.setting_age)
    await edit_age_choice_message(call)

    try:
        await call.answer()
    except:
        pass


@router.callback_query(States.setting_age, F.data.in_(['< 18','18-25','26-45','> 45']))
async def set_age_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to set his age.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    user_id = call.from_user.id
    await database.set_age(user_id, call.data)

    await state.set_state(States.setting_budget)
    await edit_budget_choice_message(call)

    try:
        await call.answer()
    except:
        pass


@router.callback_query(States.setting_budget, F.data.in_(['0','1','2','3','4','5','6','7','8','9','del_all','budget_ready']))
async def set_budget_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to set his shopping cart budget.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    user_id = call.from_user.id

    match call.data:
        case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
            budget_now = await database.get_budget(user_id)
            if budget_now == '_____':
                if call.data != '0':
                    await database.set_budget(user_id, call.data)
            else:
                await database.set_budget(user_id, budget_now + call.data)
            await edit_budget_choice_message(call)
        case 'del_all':
            await database.set_budget(user_id, '_____')
            await edit_budget_choice_message(call)
        case 'budget_ready':
            await state.set_state(States.waiting_message)
            await edit_waiting_message(call.message)

    try:
        await call.answer()
    except:
        pass


@router.callback_query(F.data=='rephrase')
async def set_budget_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to rephrase his request.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    await state.set_state(States.waiting_message)
    await send_waiting_message(call.message)

    try:
        await call.answer()
    except:
        pass


@router.callback_query(F.data=='add_one')
async def add_one_call_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that adds one item to the cart.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    user_id = call.from_user.id
    id_list = (await database.get_goods(user_id)).split('||')
    message_list = (await database.get_messages(user_id)).split('||')

    temp_dict = {}

    for i in range(len(id_list)):
        temp_dict[str(i+1)] = {'id': id_list[i], 'message': message_list[i]}

    await state.set_state(States.waiting_answer)
    await send_generated_added(call, state, json.dumps(temp_dict, indent = 4, ensure_ascii=False))

    try:
        await call.answer()
    except:
        pass


@router.callback_query(F.data.in_(['regenerate', 'ask_multipurpose']))
async def give_another_answer_handler(call: types.CallbackQuery, state: FSMContext):
    """
    A function that allows user to generate his shopping cart again, or,
    if the request is invalid for NOT multipurpose assistant, choose the multipurpose assistant.

    Args:
        call (types.CallbackQuery): Event type.
        state (FSMContext): Current state.
    """
    await state.set_state(States.waiting_answer)

    if call.data == 'ask_multipurpose':
        await database.set_assistent(call.from_user.id, 'multipurpose')

    await send_generated(call, state)
    
    try:
        await call.answer()
    except:
        pass


@router.callback_query(F.data[:6] == 'delete')
async def give_another_answer_handler(call: types.CallbackQuery):
    """
    A function that allows user to delete a product from the shopping cart via removing it from the database.

    Args:
        call (types.CallbackQuery): Event type.
    """
    user_id = call.from_user.id
    id_list = (await database.get_goods(user_id)).split('||')
    message_list = (await database.get_messages(user_id)).split('||')

    try:
        del id_list[int(call.data[6:])-1]
        del message_list[int(call.data[6:])-1]
        await database.set_goods(user_id, '||'.join(id_list))
        await database.set_messages(user_id, '||'.join(message_list))
        await send_result(call.message, await create_caption(id_list, message_list, 'goods/all_goods.csv'), id_list)
    
    except Exception as e:
        logging.exception('Не удалось удалить товар, ошибка: ' + str(e))
        await call.message.answer(
            text=f'{rd.choice(['🥺','🤧','😔','🤕','😟','😭'])} Не удалось удалить товар'
        )

    try:
        await call.answer()
    except:
        pass


### Хэндлеры сообщений

@router.message(filters.StateFilter('States:setting_gender', 'States:setting_age', 'States:setting_budget', 'States:setting_assistent'))
async def warning(message: types.Message, state: FSMContext):
    """
    A function that warns user to choose all needed parameters and changes his state. 

    Args:
        message (types.Message): Event type.
        state (FSMContext): Current state.
    """
    match await state.get_state():
        case 'States:setting_assistent':
            await message.answer(
                f'{rd.choice(['🤨','🤔','🧐'])} Для начала выберите подходящего Вам ассистента',
                reply_markup=mk.assistent_inline_markup
            )
        case 'States:setting_gender':
            await message.answer(
                f'{rd.choice(['🤨','🤔','🧐'])} Укажите Ваш пол',
                reply_markup=mk.gender_inline_markup
            )
        case 'States:setting_age':
            await message.answer(
                text='✏️ Укажите Ваш возраст',
                reply_markup=mk.age_inline_markup
            )
        case 'States:setting_budget':
            await message.answer(
                text=f'{rd.choice(['💸', '🤑', '💲', '💳', '💰', '💵'])} Введите бюджет корзины: {await database.get_budget()}',
                reply_markup=mk.budget_inline_markup
            )


# Старт
@router.message(filters.Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    """
    A function that handles /start command and adds him to the database.

    Args:
        message (types.Message): Event type.
        state (FSMContext): Current state.
    """
    if not (await database.user_exists(message.from_user.id)):
        await database.add_user(message.from_user.id)
    await state.clear()
    await send_start_message(message)
    

@router.message(States.waiting_answer)
async def wait_answer_handler(message: types.Message):
    """
    A function that warns user to wait until the end of generation.

    Args:
        message (types.Message): Event type.
        state (FSMContext): Current state.
    """
    await message.answer(f'{rd.choice(['⛔️','🚫','😠','🙅','🥴'])} Подождите конца генерации')


@router.message(States.waiting_message)
async def give_answer_handler(message: types.Message, state: FSMContext):
    """
    A function that sends the generated shopping cart.

    Args:
        message (types.Message): Event type.
        state (FSMContext): Current state.
    """
    user_id = message.from_user.id
    await state.set_state(States.waiting_answer)
    await database.set_info(user_id, message.text)
    await send_generated(message, state)


# Сообщения без фильтров
@router.message()
async def message_handler(message: types.Message):
    """
    A function that adds user to the database if he is not there.

    Args:
        message (types.Message): _description_
        state (FSMContext): _description_
    """

    if not (await database.user_exists(message.from_user.id)):
        await database.add_user(message.from_user.id)

    else:
        match message.text:
            case _:
                await send_menu_message(message)
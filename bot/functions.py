# Импорт библиотек и классов
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
import logging
import markups as mk
from create_bot import database
from generating import *
import random as rd
import csv
from aiogram.utils.media_group import MediaGroupBuilder


message_effect_id_success = [
    "5104841245755180586", # 🔥
    "5107584321108051014", # 👍
    "5046509860389126442", # ❤️
    "5159385139981059251"  # 🎉
]

message_effect_id_fail = [
    "5104858069142078462", # 👎
    "5046589136895476101"  # 💩
]


async def split_text_by_words(text: str):
    """
    A function that splits the message by words. If the message is longer than 1024 symbols, splits it in several parts.

    Args:
        text (str): Text of the message.

    Returns:
        list: Returns all parts of the message.
    """
    words = text.split(sep=' ')
    result = []
    current_group = []
    current_chars = 0

    for word in words:
        if current_chars + len(word) + len(current_group) <= 1024:
            current_group.append(word)
            current_chars += len(word)
        else:
            result.append(" ".join(current_group))
            current_group = [word]
            current_chars = len(word)

    if current_group:
        result.append(" ".join(current_group))

    return result


async def csv_extract_all_needed(filename: str, id: str):
    """
    A function that extracts data (name, price, link) from chosen .csv file
    Args:
        filename (str): Name of .csv file with goods.
        id (str): ID of the required product

    Returns:
        list[str]: Returns extracted data from .csv file.
    """
    with open(filename, 'r', encoding='utf8') as file:
        reader = list(csv.reader(file, delimiter=';'))
        for i in reader:
            if i[0] == id:
                return [i[1], i[2], i[3]]


async def send_start_message(message: types.Message):
    """
    Function that sends a greeting message.

    Args:
        message (types.Message): Event type.
    """
    await message.answer_photo(
        photo=types.FSInputFile('pictures/copilot_tbank.jpg'),
        caption=f'{rd.choice(['😁','👋','🤖'])} Привет! Я - ИИ-ассистент, я помогу тебе собрать корзину по твоим предпочтениям!',
        parse_mode='Markdown'
    )
    await send_menu_message(message)


async def send_menu_message(message: types.Message):
    """
    A function that allows user to go to main menu via inline buttons.

    Args:
        message (types.Message): Event type.
    """
    await message.answer(
        text=f'{rd.choice(['🤨','🤔','🧐'])} Приступим к составлению корзины',
        reply_markup=mk.menu_inline_markup,
        parse_mode='Markdown'
    )

async def edit_menu_message(message: types.Message):
    """
    A function that allows user to go to main menu via inline buttons with editing last message.

    Args:
        message (types.Message): Event type.
    """
    try:
        await message.edit_text(
            text=f'{rd.choice(['🤨','🤔','🧐'])} Приступим к составлению корзины',
            reply_markup=mk.menu_inline_markup,
            parse_mode='Markdown'
        )
    except:
        pass


async def edit_assistent_choice_message(message: types.Message):
    """
    A function that allows user to choose his assistant via inline buttons with editing last message.

    Args:
        message (types.Message): Event type.
    """
    try:
        await message.edit_text(
            text=f'{rd.choice(['🤨','🤔','🧐'])} Для начала выберите подходящего ассистента:\n\n🛠️ Универсальный - соберет корзину на любой вкус\n🪴 Дизайнер - подберет декор от мебели до мелких деталей\n🥻 Стилист - подберет образ полностью или к элементу одежды\n🪞 Косметолог - подбирет уход под тип кожи и образ жизни\n🥕 Нутрициолог - подбирет продуктовую корзину под КБЖУ',
            reply_markup=mk.assistent_inline_markup,
            parse_mode='Markdown'
        )
    except:
        pass

    
async def edit_gender_choice_message(message: types.Message):
    """
    A function that allows user to choose his gender via inline buttons with editing last message.

    Args:
        message (types.Message): Event type.
    """
    try:
        await message.edit_text(
            text=f'{rd.choice(['🤨','🤔','🧐'])} Укажите Ваш пол',
            reply_markup=mk.gender_inline_markup,
            parse_mode='Markdown'
        )
    except:
        pass

async def edit_age_choice_message(event: types.CallbackQuery | types.Message):
    """
    A function that allows user to choose his age via inline buttons with editing last message.

    Args:
        event (types.CallbackQuery | types.Message): Event type.

    Raises:
        TypeError: Raises TypeError when event type is neither Message or CallbackQuery.
    """
    user_id = event.from_user.id
    
    if type(event) == types.Message:
        message = event
    elif type(event) == types.CallbackQuery:
        message = event.message
    else:
        raise TypeError
    
    try:
        await message.edit_text(
            text='✏️ Укажите Ваш возраст',
            reply_markup=mk.age_inline_markup
        )
        await database.set_budget(user_id, '_____')
    except:
        pass


async def edit_budget_choice_message(event: types.CallbackQuery | types.Message):
    """
    A function that allows user to enter the budget of a shopping cart via inline buttons with editing last message.

    Args:
        event (types.CallbackQuery | types.Message): Event type.

    Raises:
        TypeError: Raises TypeError when event type is neither Message or CallbackQuery.
    """
    user_id = event.from_user.id

    if type(event) == types.Message:
        message = event
    elif type(event) == types.CallbackQuery:
        message = event.message
    else:
        raise TypeError
    
    try:
        await message.edit_text(
            text=f'{rd.choice(['💸', '🤑', '💲', '💳', '💰', '💵'])} Введите бюджет корзины: {await database.get_budget(user_id)}',
            reply_markup=mk.budget_inline_markup
        )
    except:
        pass


async def edit_waiting_message(message: types.Message):
    """
    Edits a message that allows the user to describe his cart requirements.

    Args:
        message (types.Message): Event type.
    """
    try:
        await message.edit_text(
            text='✏️ Расскажите для чего вам необходимо собрать корзину',
            reply_markup=mk.back_inline_markup
        )
    except:
        pass

async def send_waiting_message(message: types.Message):
    """
    Sends a message that allows the user to describe his cart requirements.

    Args:
        message (types.Message): Event type.
    """
    await message.answer(
        text='✏️ Расскажите для чего вам необходимо собрать корзину',
        reply_markup=mk.back_inline_markup
    )


async def create_caption(id_list: list, message_list: list, filename: str):
    """
    Makes the full text description of the generated shopping cart.

    Args:
        id_list (list): IDs of goods currently in the cart.
        message_list (list): Descriptions of all products.
        filename (str): Name of .csv file with goods.

    Returns:
        str: Returns the full text description of the generated shopping cart.
    """
    
    caption = ''
    for i in range(len(id_list)):
        name, price, link = await csv_extract_all_needed(filename, id_list[i])
        caption += f'✨ Позиция {i+1} ✨\n🛍 {name}: {price}\n{message_list[i]}\nСсылка: {link}\n\n'
    return caption


async def send_result(message: types.Message, caption: str, id_list: list):
    """
    A function that sends the final shopping cart with all changes included (splits the message into two if the message is too long).

    Args:
        message (types.Message): Event type.
        caption (str): Shopping cart description.
        id_list (list): IDs of goods currently in the cart.
    """
    if len(caption) <= 1024:
        basket_of_goods = MediaGroupBuilder(caption=caption)
        for i in id_list:
            basket_of_goods.add(type='photo', media=FSInputFile(f'pictures/goods/{i}.jpg'))
        await message.answer_media_group(media=basket_of_goods.build(), message_effect_id=rd.choice(message_effect_id_success))
    else:
        caption_list = await split_text_by_words(caption)

        basket_of_goods = MediaGroupBuilder(caption=caption_list[0])
        for i in id_list:
            basket_of_goods.add(type='photo', media=FSInputFile(f'pictures/goods/{i}.jpg'))
        await message.answer_media_group(media=basket_of_goods.build(), message_effect_id=rd.choice(message_effect_id_success))

        for i in range(1, len(caption_list)):
            await message.answer(caption_list[i], parse_mode='Markdown')

    inline_list = [[InlineKeyboardButton(text='♻️ Повторить подбор', callback_data='regenerate')]]
    for i in range(len(id_list)):
        if i % 2 > 0:
            inline_list[-1].append(InlineKeyboardButton(text=f'🗑 Удалить товар {i+1}', callback_data=f'delete{i+1}'))
        else:
            inline_list.append([InlineKeyboardButton(text=f'🗑 Удалить товар {i+1}', callback_data=f'delete{i+1}')])
    inline_list.append([InlineKeyboardButton(text='✙𝟏 Добавить товар', callback_data='add_one')])
    inline_list.append([InlineKeyboardButton(text='❌ Начать заново', callback_data='menu')])
    result_inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_list)

    await message.answer(
        text=f'Подбор завершен! Как вам такие товары?',
        reply_markup=result_inline_markup,
        parse_mode='Markdown'
    )


async def send_generated(event: types.CallbackQuery | types.Message, state: FSMContext):
    """
    Sends the generated shopping cart, handling the event type, as well as the selected assistant, invalid requests and generation errors.

    Args:
        event (types.CallbackQuery | types.Message): Event type.
        state (FSMContext): Current state.

    Raises:
        TypeError: Raises TypeError when event type is neither Message or CallbackQuery.
    """
    user_id = event.from_user.id

    if type(event) == types.Message:
        message = event
    elif type(event) == types.CallbackQuery:
        message = event.message
    else:
        raise TypeError

    temp_message = await message.answer(f'Идет подбор {rd.choice(['💃','😉','⏳'])}')

    assistent = await database.get_assistent(user_id)
    gender = await database.get_gender(user_id)
    age = await database.get_age(user_id)
    budget = await database.get_budget(user_id)

    match gender:
        case 'female': gender = 'женский'
        case 'male': gender = 'мужской'

    try:
        message_text = await database.get_info(user_id)

        match assistent:
            case 'multipurpose':
                result_dict = await generate_universal_mode(gender, age, budget, message_text)
                filename = 'goods/all_goods.csv'
            case 'designer':
                result_dict = await generate_decoration_mode(gender, age, budget, message_text)
                filename = 'goods/decoration_goods.csv'
            case 'stylist':
                result_dict = await generate_cloths_mode(gender, age, budget, message_text)
                filename = 'goods/cloths_goods.csv'
            case 'cosmetologist':
                result_dict = await generate_cosmetic_mode(gender, age, budget, message_text)
                filename = 'goods/cosmetic_goods.csv'
            case 'nutritionist':
                result_dict = await generate_food_mode(gender, age, budget, message_text)
                filename = 'goods/food_goods.csv'

        for i in result_dict:
            if i == 'message':
                await state.clear()
                match result_dict['message']:
                    case 'bad criteria':
                        await message.answer(f"{rd.choice(['🗿', '🤯', '🤓', '😵', '😵‍💫', '🤦'])} Вы ввели некорректные критерии", reply_markup=mk.to_menu_or_rephrase_inline_markup)
                    case 'not enough money':
                        await message.answer(f"{rd.choice(['📉🫢', '❌💲', '😭🔻', '🚬😮‍💨'])} Не удалось собрать корзину из-за слишком маленького бюджета", reply_markup=mk.to_menu_inline_markup)
                    case 'not my specialty':
                        await message.answer(f"{rd.choice(['🗿', '🤯', '🤓', '😵', '😵‍💫', '🤦'])} Ваши критерии не соответствует области работы ассистента. Выберите другого ассистента или переформулируйте запрос.", reply_markup=mk.wrong_request_inline_markup)      
                return

        await database.set_goods(user_id, '||'.join([result_dict[j]['id'] for j in result_dict]))
        await database.set_messages(user_id, '||'.join([result_dict[j]['message'] for j in result_dict]))

        await send_result(message, await create_caption([result_dict[i]['id'] for i in result_dict], [result_dict[i]['message'] for i in result_dict], filename), [result_dict[i]['id'] for i in result_dict])

    except Exception as e:
        logging.exception(e)
        await message.answer(
            text=f'{rd.choice(['🥺','🤧','😔','🤕','😟','😭'])} Возникла ошибка. Попробуйте еще раз.',
            reply_markup=mk.generate_again_inline_markup,
            parse_mode='Markdown',
            message_effect_id=rd.choice(message_effect_id_fail)
        )

    try:
        await temp_message.delete()
    except:
        pass

    await state.clear()



async def send_generated_added(event: types.CallbackQuery | types.Message, state: FSMContext, json_str_market_cart):
    """
    A function that sends the final generated shopping cart with one item added.

    Args:
        event (types.CallbackQuery | types.Message): Event type.
        state (FSMContext): Current state.
        json_str_market_cart (_type_): String of the JSON shopping cart.

    Raises:
        TypeError: Raises TypeError when event type is neither Message or CallbackQuery.
    """
    user_id = event.from_user.id

    if type(event) == types.Message:
        message = event
    elif type(event) == types.CallbackQuery:
        message = event.message
    else:
        raise TypeError

    temp_message = await message.answer(f'Идет подбор {rd.choice(['💃','😉','⏳'])}')

    assistent = await database.get_assistent(user_id)
    gender = await database.get_gender(user_id)
    age = await database.get_age(user_id)
    budget = await database.get_budget(user_id)

    match gender:
        case 'female': gender = 'женский'
        case 'male': gender = 'мужской'

    try:
        message_text = await database.get_info(user_id)

        match assistent:
            case 'multipurpose':
                result_dict = await generate_add_universal_mode(gender, age, budget, message_text, json_str_market_cart)
                filename = 'goods/all_goods.csv'
            case 'designer':
                result_dict = await generate_add_decoration_mode(gender, age, budget, message_text, json_str_market_cart)
                filename = 'goods/decoration_goods.csv'
            case 'stylist':
                result_dict = await generate_add_cloths_mode(gender, age, budget, message_text, json_str_market_cart)
                filename = 'goods/cloths_goods.csv'
            case 'cosmetologist':
                result_dict = await generate_add_cosmetic_mode(gender, age, budget, message_text, json_str_market_cart)
                filename = 'goods/cosmetic_goods.csv'
            case 'nutritionist':
                result_dict = await generate_add_food_mode(gender, age, budget, message_text, json_str_market_cart)
                filename = 'goods/food_goods.csv'

        for i in result_dict:
            if i == 'message':
                await state.clear()
                match result_dict['message']:
                    case 'bad criteria':
                        await message.answer(f"{rd.choice(['🗿', '🤯', '🤓', '😵', '😵‍💫', '🤦'])} Вы ввели некорректные критерии", reply_markup=mk.to_menu_or_rephrase_inline_markup)
                    case 'too many items':
                        await message.answer(f"{rd.choice(['🗿', '🤯', '🤓', '😵', '😵‍💫', '🤦'])} Кажется, что у вас в корзине слишком много товаров", reply_markup=mk.generate_again_inline_markup)
                    case 'not enough money':
                        await message.answer(f"{rd.choice(['📉🫢', '❌💲', '😭🔻', '🚬😮‍💨'])} Не удалось собрать корзину из-за слишком маленького бюджета", reply_markup=mk.to_menu_inline_markup)
                    case 'not my specialty':
                        await message.answer(f"{rd.choice(['🗿', '🤯', '🤓', '😵', '😵‍💫', '🤦'])} Ваши критерии не соответствует области работы ассистента. Выберите другого ассистента или переформулируйте запрос.", reply_markup=mk.wrong_request_inline_markup)      
                return

        await database.set_goods(user_id, '||'.join([result_dict[j]['id'] for j in result_dict]))
        await database.set_messages(user_id, '||'.join([result_dict[j]['message'] for j in result_dict]))

        await send_result(message, await create_caption([result_dict[i]['id'] for i in result_dict], [result_dict[i]['message'] for i in result_dict], filename), [result_dict[i]['id'] for i in result_dict])

    except Exception as e:
        logging.exception(e)
        await message.answer(
            text=f'{rd.choice(['🥺','🤧','😔','🤕','😟','😭'])} Возникла ошибка. Попробуйте еще раз.',
            reply_markup=mk.generate_again_inline_markup,
            parse_mode='Markdown',
            message_effect_id=rd.choice(message_effect_id_fail)
        )

    try:
        await temp_message.delete()
    except:
        pass

    await state.clear()
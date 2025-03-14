# Импорт библиотек и классов
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random as rd


### Inline marks

menu_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать ✅', callback_data='start')]
])

assistent_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛠️ Универсальный', callback_data='multipurpose')],
    [InlineKeyboardButton(text='🪴 Дизайнер', callback_data='designer'), InlineKeyboardButton(text='🥻 Стилист', callback_data='stylist')],
    [InlineKeyboardButton(text='🪞 Косметолог', callback_data='cosmetologist'), InlineKeyboardButton(text='🥕 Нутрициолог', callback_data='nutritionist')],
    [InlineKeyboardButton(text=f'{rd.choice(['⛔️','🚫','❌'])} Отмена', callback_data='back')]
])

wrong_request_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛠️ Спросить универсального ассистента', callback_data='ask_multipurpose')],
    [InlineKeyboardButton(text='♻️ Переформулировать запрос', callback_data='rephrase')],
    [InlineKeyboardButton(text='❌ Начать заново', callback_data='menu')]
])

gender_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='♂️ Мужской', callback_data='male'), InlineKeyboardButton(text='♀️ Женский', callback_data='female')],
    [InlineKeyboardButton(text='⛔️ Назад', callback_data='back')]
])  


age_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👶 < 18', callback_data='< 18'), InlineKeyboardButton(text='🧑 18-25', callback_data='18-25')],
    [InlineKeyboardButton(text='👨 26-45', callback_data='26-45'), InlineKeyboardButton(text='👵 > 45', callback_data='> 45')],
    [InlineKeyboardButton(text='⛔️ Назад', callback_data='back')]
])

budget_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='1'), InlineKeyboardButton(text='2', callback_data='2'), InlineKeyboardButton(text='3', callback_data='3')],
    [InlineKeyboardButton(text='4', callback_data='4'), InlineKeyboardButton(text='5', callback_data='5'), InlineKeyboardButton(text='6', callback_data='6')],
    [InlineKeyboardButton(text='7', callback_data='7'), InlineKeyboardButton(text='8', callback_data='8'), InlineKeyboardButton(text='9', callback_data='9')],
    [InlineKeyboardButton(text='❌', callback_data='del_all'), InlineKeyboardButton(text='0', callback_data='0'), InlineKeyboardButton(text='✅', callback_data='budget_ready')],
    [InlineKeyboardButton(text='⛔️ Назад', callback_data='back')]
])

back_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⛔️ Назад', callback_data='back')]
])

generate_again_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='♻️ Повторить подбор', callback_data='regenerate')],
    [InlineKeyboardButton(text='❌ Начать заново', callback_data='menu')]
])

to_menu_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Начать заново', callback_data='menu')]
])

to_menu_or_rephrase_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='♻️ Переформулировать запрос', callback_data='rephrase')],
    [InlineKeyboardButton(text='❌ Начать заново', callback_data='menu')]
])
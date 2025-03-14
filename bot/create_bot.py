# Импорт библиотек и классов
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import db
import config
from aiogram.fsm.state import StatesGroup, State

# Инициализация бота и диспетчера для работы с ним
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
database = db.DataBase('data/database_file.db')

class States(StatesGroup):
    setting_assistent = State()
    setting_gender = State()
    setting_age = State()
    setting_budget = State()
    waiting_message = State()
    waiting_answer = State()
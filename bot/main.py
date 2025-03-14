# Импорт библиотек и классов
import asyncio
import logging
from time import sleep
from aiogram.types import BotCommand, BotCommandScopeDefault
from handlers import router
from create_bot import bot, dp

# Командное меню
async def set_commands():
    """
    Add bot commands to the command menu
    """    
    commands = [
        BotCommand(command='start', description='Старт')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

# Функция, которая будет вызвана при запуске бота
async def on_startup():
    """
    Execute functions on startup
    """    
    await set_commands()

# Запуск бота
async def start_bot():
    """
    Function to start the bot
    """    
    dp.startup.register(on_startup)
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=False)

    while True:
        try:
            await dp.start_polling(bot, skip_updates=True)
        except Exception as e:
            logging.exception(e)
            await asyncio.sleep(0.1)
            continue


# Главная функция
async def main():
    await start_bot()


# Асинхронный пуск
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b %H:%M:%S', level=logging.INFO, filename="data/bot_log.log", filemode="a", encoding='utf8')
    while True:
        try:
            logging.info("Запуск")
            asyncio.run(main())
        except Exception as e:
            logging.exception(e)
            sleep(0.1)
            continue
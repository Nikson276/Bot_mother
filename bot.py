from aiogram import executor
from dispatcher import dp
import keyboards as kb
import handlers

# Подключаем БД

from db import BotDB
BotDB = BotDB('sleepcounter.db')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
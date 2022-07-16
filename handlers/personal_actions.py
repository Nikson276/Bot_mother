from aiogram import types
from dispatcher import dp
import keyboards as kb
import config
import re
from bot import BotDB

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!\nЯ буду помогать тебе с малышом", reply_markup=kb.markup3)

    
@dp.message_handler(commands = "help")
async def info(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Пока ты можешь использовать текстовые команды\n/rise - проснулся\n/fall - уснул\n/h - история\n\nИли используй кнопки. Удачи")
    

@dp.message_handler(commands = ("rise", "fall", "r", "f"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = (('/rise', '/r', '!rise', '!r'), ('/fall', '/f', '!fall', '!f'))
    act_type = 'rise' if message.text.startswith(cmd_variants[0]) else 'fall'


    # Вызываем метод добавления записи в БД
    BotDB.add_record(message.from_user.id, act_type) 

    if(act_type == 'rise'):
        await message.reply("📖 Запись о 😀<u><b>Пробуждении</b></u> успешно внесена!")
    else:
        await message.reply("📖 Запись о 💤<u><b>Засыпании</b></u> успешно внесена!")


@dp.message_handler(commands = ("history", "h"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        "year": ('year', 'год'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()

    within = 'day' # default
    # выберем с помощью словаря (по ключу) значение периода
    if(len(cmd)):
        for k in within_als:
            for als in within_als[k]:
                if(als == cmd):
                    within = k

    # получаем записи
    records = BotDB.get_records(message.from_user.id, within)
    #Список кортежей со строками таблицы
    #[(10, 2, 'rise', '2022-04-24 20:53:54', None),
    # (11, 2, 'fall', '2022-04-24 21:07:23', '0:12:57'), 
    # (12, 2, 'rise', '2022-04-24 21:11:30', '0:04:07'), 
    # (13, 2, 'fall', '2022-04-24 21:17:15', '0:05:45')]

    if(len(records)): #Если длинна не пуста.
        answer = f"📖 История операций за {within_als[within][-1]}🕘\n\n"

        for r in records: #цикл по каждой строке r - row в records
            answer += "<b>" + ("➖ Уснул" if not r[2] == 'rise' else "➕ Проснулся") + "</b>"
            answer += f" - {r[3]}\n"
            answer += "<b>" + ("😀 Бодроствовал" if not r[2] == 'rise' else "💤 Спал") + "</b>"
            answer += f" <i>({r[4]})</i>\n\n"

        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#button_hi = KeyboardButton('Привет! 👋')

# greet_kb = ReplyKeyboardMarkup()
# greet_kb.add(button_hi)

#одна кнопка
#(атрибут one_time_keyboard=True используется для скрытия после нажатия)
#greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

button1 = KeyboardButton('/rise')
button2 = KeyboardButton('/fall')
button3 = KeyboardButton('/history')

markup3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    button1, button2).row(button3
)
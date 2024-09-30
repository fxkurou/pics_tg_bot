from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Gallery'),
            KeyboardButton(text='Search'),
            KeyboardButton(text='Upload pic')
        ]
    ],
    resize_keyboard=True
)
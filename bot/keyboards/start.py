from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Gallery'),
            KeyboardButton(text='Search'),
        ],
        [
            KeyboardButton(text='Upload picture'),
            KeyboardButton(text='Help')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)
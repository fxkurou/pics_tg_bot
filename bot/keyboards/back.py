from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Back'),
        ]
    ],
    resize_keyboard=True
)
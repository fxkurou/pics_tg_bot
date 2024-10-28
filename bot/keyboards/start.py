from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Gallery', callback_data='gallery'),
            InlineKeyboardButton(text='By Creators', callback_data='creators'),
        ],
        [
            InlineKeyboardButton(text='Upload picture', callback_data='upload'),
            InlineKeyboardButton(text='Help', callback_data='help'),
        ],
        [
            InlineKeyboardButton(text='Donate', callback_data='donate'),
        ]
    ],
)
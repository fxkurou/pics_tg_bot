from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Gallery', callback_data='gallery'),
            InlineKeyboardButton(text='Search', callback_data='search'),
        ],
        [
            InlineKeyboardButton(text='Upload picture', callback_data='upload'),
            InlineKeyboardButton(text='Help', callback_data='help'),
        ]
    ],
)
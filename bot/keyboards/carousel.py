from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


class PaginationCallback(CallbackData, prefix='pic_pagination'):
    action: str
    page: int


def pics_paginator(page: int, items: list):
    kb = InlineKeyboardBuilder()

    if len(items) > 1:
        if page > 0:
            kb.add(
                InlineKeyboardButton(text='⬅Previous', callback_data=PaginationCallback(action='prev', page=page - 1).pack())
            )

        if page < len(items) - 1:
            kb.add(
                InlineKeyboardButton(text='➡Next', callback_data=PaginationCallback(action='next', page=page + 1).pack())
            )
        kb.adjust(2)

    kb.row(InlineKeyboardButton(text='⬅Back', callback_data=PaginationCallback(action='back', page=page).pack()))

    return kb.as_markup()
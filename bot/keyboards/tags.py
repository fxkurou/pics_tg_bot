from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

class TagsCallbackFactory(CallbackData, prefix='tag'):
    name: str


async def get_tags_kb(tags):
    kb = InlineKeyboardBuilder()
    for tag in tags:
        callback_data = TagsCallbackFactory(name=tag.name).pack()
        kb.add(InlineKeyboardButton(text=tag.name, callback_data=callback_data))
    return kb.as_markup()
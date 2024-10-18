from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

class TagsCallbackFactory(CallbackData, prefix='tag'):
    name: str


async def get_tags_kb(tags):
    sorted_tags = sorted(tags, key=lambda tag: tag.name)

    kb = InlineKeyboardBuilder()
    for tag in sorted_tags:
        callback_data = TagsCallbackFactory(name=tag.name).pack()
        kb.add(InlineKeyboardButton(text=tag.name, callback_data=callback_data))
    kb.adjust(3)
    kb.row(InlineKeyboardButton(text='Back', callback_data='back'))
    return kb.as_markup()
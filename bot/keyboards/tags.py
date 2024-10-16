from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

async def get_tags_kb(tags):
    kb = InlineKeyboardBuilder()
    for tag in tags:
        kb.add(InlineKeyboardButton(text=tag.name, callback_data=f'{tag.name}'))
    return kb.as_markup()
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

class TagsCallbackFactory(CallbackData, prefix='tag'):
    name: str

class TagsPaginationCallbackFactory(CallbackData, prefix='tag_pagination'):
    page: int

TAGS_PER_PAGE = 9

async def get_tags_kb(tags, page=0):
    sorted_tags = sorted(tags, key=lambda tag: tag.name)

    # Calculate pagination range
    start = page * TAGS_PER_PAGE
    end = start + TAGS_PER_PAGE
    paginated_tags = sorted_tags[start:end]

    kb = InlineKeyboardBuilder()
    for tag in paginated_tags:
        callback_data = TagsCallbackFactory(name=tag.name).pack()
        kb.add(InlineKeyboardButton(text=tag.name, callback_data=callback_data))
    kb.adjust(3)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            text='⬅Previous',
            callback_data=TagsPaginationCallbackFactory(page=page - 1).pack()
        ))
    if end < len(sorted_tags):
        nav_buttons.append(InlineKeyboardButton(
            text='Next➡',
            callback_data=TagsPaginationCallbackFactory(page=page + 1).pack()
        ))
    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text='⬅Back', callback_data='back'))
    return kb.as_markup()
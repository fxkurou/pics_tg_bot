from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class DonateCallbackFactory(CallbackData, prefix="donate"):
    amount: int


async def get_donate_kb():
    kb = InlineKeyboardBuilder()
    for amount in [1, 5, 15, 25, 50, 100]:
        callback_data = DonateCallbackFactory(amount=amount).pack()
        kb.add(InlineKeyboardButton(text=f"{amount} ⭐", callback_data=callback_data))
    kb.adjust(3)
    kb.row(InlineKeyboardButton(text="⬅Back", callback_data="back"))
    return kb.as_markup()


async def invoice_kb(amount: int):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=f"Pay {amount} XTR", pay=True))
    kb.row(InlineKeyboardButton(text="⬅Back", callback_data="back"))
    kb.adjust(1)
    return kb.as_markup()
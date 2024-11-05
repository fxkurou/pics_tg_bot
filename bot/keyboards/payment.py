from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


class PaymentCallbackFactory(CallbackData, prefix="payment"):
    amount: int
    action: str
    page: int

def get_payment_kb(amount: int, page: int, items: list):
    kb = InlineKeyboardBuilder()

    if len(items) > 1:
        if page > 0:
            kb.add(
                InlineKeyboardButton(text='⬅Previous', callback_data=PaymentCallbackFactory(action='prev', page=page - 1, amount=amount).pack())
            )

        if page < len(items) - 1:
            kb.add(
                InlineKeyboardButton(text='➡Next', callback_data=PaymentCallbackFactory(action='next', page=page + 1, amount=amount).pack())
            )
        kb.adjust(2)

    kb.row(InlineKeyboardButton(text=f'Pay {amount}$', callback_data=PaymentCallbackFactory(action='pay', page=page, amount=amount).pack(), pay=True))

    kb.row(InlineKeyboardButton(text='⬅Back', callback_data=PaymentCallbackFactory(action='back', page=page, amount=amount).pack()))

    return kb.as_markup()


def get_invoice_kb(amount: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text=f'Pay {amount}$', pay=True))
    kb.row(InlineKeyboardButton(text='⬅Back', callback_data='back'))

    return kb.as_markup()
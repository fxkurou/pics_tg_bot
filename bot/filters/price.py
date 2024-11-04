from aiogram.filters import BaseFilter

from bot.keyboards.payment import PaymentCallbackFactory


class PaymentAmountValidator(BaseFilter):
    async def __call__(self, callback_data: PaymentCallbackFactory) -> bool:
        return 1 <= int(callback_data.amount) <= 1000
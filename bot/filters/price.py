from aiogram.types import Message
from aiogram.filters import BaseFilter


class PaymentAmountValidator(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and 1 <= int(message.text) <= 1000
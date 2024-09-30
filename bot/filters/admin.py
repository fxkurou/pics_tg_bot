from aiogram.filters import BaseFilter
from aiogram.types import Message
import os


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == os.getenv('ADMIN_ID')
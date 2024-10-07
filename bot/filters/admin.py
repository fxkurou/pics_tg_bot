from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
import os


class IsAdmin(BaseFilter):

    def __init__(self, admin_ids: List[int]|int) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.admin_ids, int):
            return message.from_user.id == self.admin_ids
        return message.from_user.id in self.admin_ids
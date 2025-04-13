from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.core.config import settings


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.user_ids = settings.ADMINS

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.user_ids, int):
            return message.from_user.id == self.user_ids
        return message.from_user.id in self.user_ids

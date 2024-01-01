from aiogram.types import Chat

from ..models import Profile


class ProfileMapper:
    def __init__(self, chat: Chat):
        self.chat = chat

    def map(self) -> Profile:
        return Profile(
            external_id=self.chat.id,
            username=self.chat.username,
            first_name=self.chat.first_name,
            last_name=self.chat.last_name,
        )

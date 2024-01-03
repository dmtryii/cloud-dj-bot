from aiogram.types import Chat


class ProfileDTO:
    def __init__(self, external_id: int, username: str, first_name: str, last_name: str):
        self.external_id = external_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class ProfileMapper:
    def __init__(self, chat: Chat):
        self.chat = chat

    def map(self) -> ProfileDTO:
        return ProfileDTO(
            external_id=self.chat.id,
            username=self.chat.username,
            first_name=self.chat.first_name,
            last_name=self.chat.last_name,
        )

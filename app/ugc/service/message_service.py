from aiogram import types

from .profile_service import ProfileService
from ..models import Message


class MessageService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    async def save(self, message: types.Message) -> None:
        profile = await self._profile_service.get()
        await Message(
            external_id=message.message_id,
            content_type=message.content_type,
            profile=profile,
            text=message.text,
        ).asave()

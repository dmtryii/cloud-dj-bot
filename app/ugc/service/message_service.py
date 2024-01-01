from aiogram import types

from .profile_service import ProfileService
from ..models import Message, Profile


class MessageService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    async def save(self, profile: Profile, message: types.Message) -> None:
        profile = await self._profile_service.get_or_create(profile)
        await Message(
            external_id=message.message_id,
            content_type=message.content_type,
            profile=profile,
            text=message.text,
        ).asave()

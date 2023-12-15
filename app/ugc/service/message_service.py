from aiogram import types

from .profile_service import add_profile
from ..models import Message, Profile


async def save_message(profile: Profile, message: types.Message) -> None:
    profile = await add_profile(profile)
    await Message(
        external_id=message.message_id,
        content_type=message.content_type,
        profile=profile,
        text=message.text,
    ).asave()

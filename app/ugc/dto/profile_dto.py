from aiogram.types import Chat

from ..models import Profile


async def map_profile(chat: Chat) -> Profile:
    return Profile(
        external_id=chat.id,
        username=chat.username,
        first_name=chat.first_name,
        last_name=chat.last_name,
    )

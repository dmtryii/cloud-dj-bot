from aiogram.types import Chat

from ..models import Profile


async def add_profile(profile: Profile) -> Profile:
    profile, created = await Profile.objects.aget_or_create(
        external_id=profile.external_id,
        defaults={
            'username': profile.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
        },
    )
    return profile


async def map_profile(chat: Chat) -> Profile:
    return Profile(
        external_id=chat.id,
        username=chat.username,
        first_name=chat.first_name,
        last_name=chat.last_name,
    )

from .profile_service import get_or_create_profile
from ..models import Profile, CurrentAction


async def set_current_action(profile: Profile, message_id: int) -> CurrentAction:
    profile = await get_or_create_profile(profile)

    current_action, created = await CurrentAction.objects.aget_or_create(
        profile=profile,
        defaults={
            "message_id": message_id
        }
    )

    if not created:
        current_action.message_id = message_id
        await current_action.asave()

    return current_action


async def get_current_action(profile: Profile) -> CurrentAction | None:
    profile = await get_or_create_profile(profile)

    current_action = await CurrentAction.objects.filter(profile=profile).afirst()

    if not current_action:
        return None

    return current_action

from .profile_service import ProfileService
from ..models import Profile, CurrentAction


class CurrentActionService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    async def set_current_action(self, profile: Profile, message_id: int) -> CurrentAction:
        profile = await self._profile_service.get_or_create(profile)

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

    async def get_current_action(self, profile: Profile) -> CurrentAction | None:
        profile = await self._profile_service.get_or_create(profile)

        current_action = await CurrentAction.objects.filter(profile=profile).afirst()

        if not current_action:
            return None

        return current_action

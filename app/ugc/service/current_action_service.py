from typing import Optional

from .profile_service import ProfileService
from ..management.commands.bot import delete_message
from ..models import CurrentAction


class CurrentActionService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    async def swap_current_action(self, message_id: int) -> None:
        current_action_service = CurrentActionService(self._profile_service)
        current_action = await current_action_service.get_current_action()
        if current_action:
            profile = await self._profile_service.get()
            await current_action_service.set_current_action(message_id)
            await delete_message(chat_id=profile.external_id, message_id=current_action.message_id)
        else:
            await current_action_service.set_current_action(message_id)

    async def set_current_action(self, message_id: int) -> CurrentAction:
        profile = await self._profile_service.get()
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

    async def get_current_action(self) -> Optional[CurrentAction]:
        profile = await self._profile_service.get()
        return await CurrentAction.objects.filter(profile=profile).afirst()

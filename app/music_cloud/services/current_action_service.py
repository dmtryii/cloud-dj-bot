from typing import Optional

from .profile_service import ProfileService
from ..models import CurrentAction


class CurrentActionService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    def create(self, message_id: int, profile_id: str) -> CurrentAction:
        profile = self._profile_service.get(profile_id)
        current_action, created = CurrentAction.objects.get_or_create(
            profile=profile,
            defaults={
                "message_id": message_id
            }
        )

        if not created:
            current_action.message_id = message_id
            current_action.save()

        return current_action

    def get(self, profile_id: str) -> Optional[CurrentAction]:
        profile = self._profile_service.get(profile_id)
        return CurrentAction.objects.filter(profile=profile).first()

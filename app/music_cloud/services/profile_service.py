from typing import Optional

from ..exceptions.profile_exception import ProfileNotFound, ProfileRoleNotFound
from ..models import Profile, Role


class ProfileService:
    def create(self, profile_id: str, username: str, first_name: str, last_name: str) -> Profile:
        default_role = self._get_default_role()
        profile, _ = Profile.objects.get_or_create(
            profile_id=profile_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'role': default_role,
            },
        )
        return profile

    def get(self, profile_id: str) -> Optional[Profile]:
        profile = Profile.objects.filter(profile_id=profile_id).first()

        if not profile:
            raise ProfileNotFound('Profile not found for external ID: {}'.format(profile_id))

        return profile

    def get_role(self, profile_id: str) -> Optional[Role]:
        profile = self.get(profile_id)
        role = Role.objects.filter(profile=profile).first()

        if not role:
            raise ProfileRoleNotFound('Role not found for profile: {}'.format(profile))

        return role

    @staticmethod
    def _get_default_role() -> Role:
        role, _ = Role.objects.get_or_create(
            name='DefaultRole',
            defaults={
                'delay_between_downloads': 60,
                'allowed_media_length': 600,
            }
        )
        return role

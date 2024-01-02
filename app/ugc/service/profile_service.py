from typing import Optional

from ..exceptions.profile_exception import ProfileNotFound, ProfileRoleNotFound
from ..mappers.profile_mapper import ProfileDTO
from ..models import Profile, Role


class ProfileService:
    def __init__(self, profile: ProfileDTO):
        self._profile = profile

    async def get(self) -> Profile:
        return await self._get_or_create()

    @classmethod
    async def get_by_external_id(cls, external_id: int) -> Optional[Profile]:
        profile = await Profile.objects.filter(external_id=external_id).afirst()

        if not profile:
            raise ProfileNotFound('Profile not found for external ID: {}'.format(external_id))

        return await cls(profile).get()

    async def get_role(self) -> Optional[Role]:
        profile = await self.get()
        role = await Role.objects.filter(profile=profile).afirst()

        if not role:
            raise ProfileRoleNotFound('Role not found for profile: {}'.format(self._profile))

        return role

    async def _get_or_create(self) -> Profile:
        default_role = await self._get_default_role()
        profile, _ = await Profile.objects.aget_or_create(
            external_id=self._profile.external_id,
            defaults={
                'username': self._profile.username,
                'first_name': self._profile.first_name,
                'last_name': self._profile.last_name,
                'role': default_role,
            },
        )
        return profile

    @staticmethod
    async def _get_default_role() -> Role:
        role, _ = await Role.objects.aget_or_create(
            name='DefaultRole',
            defaults={
                'delay_between_downloads': 60,
                'allowed_media_length': 600,
            }
        )
        return role

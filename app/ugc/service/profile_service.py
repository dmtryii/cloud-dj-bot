from ..models import Profile, Role


class ProfileService:
    async def get_or_create(self, profile: Profile) -> Profile:
        profile, _ = await Profile.objects.aget_or_create(
            external_id=profile.external_id,
            defaults={
                'username': profile.username,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'role': await self.get_default_role(),
            },
        )
        return profile

    @staticmethod
    async def get_by_external_id(external_id: int) -> Profile:
        return await Profile.objects.filter(external_id=external_id).afirst()

    @staticmethod
    async def get_default_role() -> Role:
        role, _ = await Role.objects.aget_or_create(
            name='DefaultRole',
            defaults={
                'delay_between_downloads': 60,
                'allowed_media_length': 600,
            }
        )
        return role

    @staticmethod
    async def get_role(profile: Profile) -> Role:
        return await Role.objects.filter(profile=profile).afirst()

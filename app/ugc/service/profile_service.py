from ..models import Profile, Role


async def get_or_create_profile(profile: Profile) -> Profile:
    profile, _ = await Profile.objects.aget_or_create(
        external_id=profile.external_id,
        defaults={
            'username': profile.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'role': await get_default_role(),
        },
    )
    return profile


async def get_profile_by_external_id(external_id: int) -> Profile:
    return await Profile.objects.filter(external_id=external_id).afirst()


async def get_default_role() -> Role:
    role, _ = await Role.objects.aget_or_create(
        name='DefaultRole',
        defaults={
            'allowed_downloads_per_day': 5,
            'allowed_media_length': 600,
        }
    )
    return role


async def get_role_by_profile(profile: Profile) -> Role:
    return await Role.objects.filter(profile=profile).afirst()

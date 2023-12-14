from .media_service import create_or_get_media
from ..models import Profile, CurrentAction, Media


def create_or_get_profile(profile: Profile) -> Profile:
    profile, created = Profile.objects.get_or_create(
        external_id=profile.external_id,
        defaults={
            'username': profile.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
        },
    )
    return profile


def create_or_update_current_action(profile: Profile, url: str) -> Media:
    media = create_or_get_media(profile, url)
    profile = create_or_get_profile(profile)
    current_action = CurrentAction.objects.filter(profile=profile).first()

    if current_action:
        current_action.media = media
        current_action.save()
    else:
        CurrentAction.objects.create(
            profile=profile,
            media=media,
        )

    return media


def get_current_action(profile: Profile) -> CurrentAction:
    profile = create_or_get_profile(profile)
    return CurrentAction.objects.filter(profile=profile).first()

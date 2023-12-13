from .media_service import create_or_get_media
from ..models import Profile, Contacts, CurrentAction
from django.db import transaction


def create_or_get_profile(chat):
    with transaction.atomic():
        profile, created = Profile.objects.get_or_create(
            external_id=chat.id,
            defaults={
                'username': chat.username,
            },
        )

        if created:
            Contacts.objects.create(
                profile=profile,
                first_name=chat.first_name,
                last_name=chat.last_name,
            )

    return profile


def create_or_update_current_action(chat, url):
    media = create_or_get_media(url, chat)
    profile = create_or_get_profile(chat)
    current_action = CurrentAction.objects.filter(profile=profile).first()

    if current_action:
        current_action.media = media
        current_action.save()
    else:
        CurrentAction.objects.create(
            profile=profile,
            media=media,
        )

    return profile, media


def get_current_action(chat):
    profile = create_or_get_profile(chat)
    return CurrentAction.objects.filter(profile=profile).first()

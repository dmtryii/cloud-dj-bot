from .media_service import get_media_by_profile
from .profile_service import get_current_action, create_or_get_profile
from ..models import Hashtag, MediaProfileHashtag


def create_tag(name):
    existing_hashtag, created = Hashtag.objects.get_or_create(title=name)
    return existing_hashtag


def get_all_tags_from_text(text):
    return [tag for tag in text.split(' ') if tag.startswith('#')]


def create_all_tags_from_text(text):
    for tag in get_all_tags_from_text(text):
        create_tag(tag)


def add_tags_to_media(text, chat):
    media = get_current_action(chat).media
    profile = create_or_get_profile(chat)
    media_profile = get_media_by_profile(profile, media)

    create_all_tags_from_text(text)

    for hashtag_text in get_all_tags_from_text(text):
        hashtag_instance = create_tag(hashtag_text)

        if hashtag_instance:
            MediaProfileHashtag.objects.get_or_create(
                media_profile=media_profile,
                hashtag=hashtag_instance
            )

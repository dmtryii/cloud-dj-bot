from .media_service import get_media_by_profile
from .profile_service import get_current_action, add_profile
from ..models import Hashtag, MediaProfileHashtag, Profile


def create_tag(title: str) -> Hashtag:
    hashtag, created = Hashtag.objects.get_or_create(title=title)
    return hashtag


def get_all_tags_from_text(text: str) -> list[str]:
    return [tag for tag in text.split(' ') if tag.startswith('#')]


def create_all_tags_from_text(text: str) -> None:
    for tag in get_all_tags_from_text(text):
        create_tag(tag)


def add_all_tags_to_media(text: str, profile: Profile) -> None:
    media = get_current_action(profile).media
    profile = add_profile(profile)
    media_profile = get_media_by_profile(profile, media)

    create_all_tags_from_text(text)

    for hashtag_text in get_all_tags_from_text(text):
        hashtag_instance = create_tag(hashtag_text)

        if hashtag_instance:
            MediaProfileHashtag.objects.get_or_create(
                media_profile=media_profile,
                hashtag=hashtag_instance
            )

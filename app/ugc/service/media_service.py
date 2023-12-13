from pytube import YouTube

from ..models import Media, MediaProfile


def create_or_get_media(url, chat):
    from .profile_service import create_or_get_profile

    youtube = YouTube(url)
    media, created = Media.objects.get_or_create(
        external_id=youtube.video_id,
        defaults={
            'title': youtube.title,
            'url': url,
            'duration': youtube.length,
            'channel': youtube.author,
        }
    )

    if created:
        profile = create_or_get_profile(chat)
        add_media_to_profile(profile, media)

    return media


def get_media_by_profile(profile, media):
    return MediaProfile.objects.filter(
        profile=profile,
        media=media).first()


def add_media_to_profile(profile, media):
    return MediaProfile.objects.create(
        profile=profile,
        media=media,
    )

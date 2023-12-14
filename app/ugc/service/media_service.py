from pytube import YouTube

from ..models import Media, MediaProfile, Profile


def create_or_get_media(profile: Profile, url: str) -> Media:
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
        profile = create_or_get_profile(profile)
        add_media_to_profile(profile, media)

    return media


def get_media_by_profile(profile: Profile, media: Media) -> MediaProfile:
    return MediaProfile.objects.filter(
        profile=profile,
        media=media).first()


def add_media_to_profile(profile: Profile, media: Media) -> MediaProfile:
    return MediaProfile.objects.create(
        profile=profile,
        media=media,
    )

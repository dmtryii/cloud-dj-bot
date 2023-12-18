from pytube import YouTube

from .profile_service import add_profile
from ..models import Media, MediaProfile, Profile


async def add_media(url: str) -> Media:
    youtube = YouTube(url)
    media, created = await Media.objects.aget_or_create(
        external_id=youtube.video_id,
        defaults={
            'title': youtube.title,
            'url': url,
            'duration': youtube.length,
            'channel': youtube.author,
        }
    )
    return media


async def get_all_media_by_profile__reverse(profile: Profile):
    profile = await add_profile(profile)
    return [media async for media in Media.objects.filter(mediaprofile__profile=profile)][::-1]


async def get_media_by_profile(profile: Profile, media: Media) -> MediaProfile:
    return await MediaProfile.objects.filter(
        profile=profile,
        media=media).afirst()


async def add_media_to_profile(profile: Profile, media: Media) -> MediaProfile:
    profile = await add_profile(profile)
    media = await add_media(media.url)
    media_profile, created = await MediaProfile.objects.aget_or_create(
        profile=profile,
        media=media,
    )
    return media_profile

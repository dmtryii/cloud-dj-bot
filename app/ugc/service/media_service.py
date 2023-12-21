from .profile_service import get_or_create_profile
from ..models import Media, MediaProfile, Profile


async def get_or_create_media(media: Media) -> Media:
    media, created = await Media.objects.aget_or_create(
        external_id=media.external_id,
        defaults={
            'telegram_video_file_id': media.telegram_video_file_id,
            'telegram_audio_file_id': media.telegram_audio_file_id,
            'title': media.title,
            'url': media.url,
            'duration': media.duration,
            'channel': media.channel,
        }
    )
    return media


async def get_media_by_id(media_id: int) -> Media:
    return await Media.objects.aget(id=media_id)


async def get_all_media_by_profile__reverse(profile: Profile):
    profile = await get_or_create_profile(profile)
    return [media async for media in Media.objects.filter(mediaprofile__profile=profile)][::-1]


async def get_all_favorite_media_by_profile__reverse(profile: Profile):
    profile = await get_or_create_profile(profile)
    return [media async for media in Media.objects.filter(mediaprofile__profile=profile,
                                                          mediaprofile__is_favorite=True)][::-1]


async def get_media_by_profile(profile: Profile, media: Media) -> MediaProfile:
    return await MediaProfile.objects.filter(
        profile=profile,
        media=media).afirst()


async def add_media_to_profile(profile: Profile, media: Media) -> MediaProfile:
    profile = await get_or_create_profile(profile)
    media = await get_or_create_media(media)
    media_profile, created = await MediaProfile.objects.aget_or_create(
        profile=profile,
        media=media,
    )
    return media_profile

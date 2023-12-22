import datetime

from .profile_service import get_role_by_profile
from ..models import Profile, Media, MediaDownload


async def add_download_media(profile: Profile, media: Media):
    return await MediaDownload.objects.acreate(
        profile=profile,
        media=media,
    )


async def last_download_media(profile: Profile) -> MediaDownload:
    return await MediaDownload.objects.filter(profile=profile).alast()


async def can_download_media(profile: Profile) -> bool:
    role = await get_role_by_profile(profile)
    delay_between_downloads = role.delay_between_downloads

    last_download = await last_download_media(profile)

    if last_download is None:
        return True

    last_download_time = last_download.download_date

    current_time = datetime.datetime.now(datetime.timezone.utc)
    time_since_last_download = current_time - last_download_time

    if time_since_last_download.total_seconds() >= delay_between_downloads:
        return True

    return False

import datetime

from .profile_service import get_role_by_profile
from ..models import Profile, Media, MediaDownload


async def add_download_media(profile: Profile, media: Media):
    return await MediaDownload.objects.acreate(
        profile=profile,
        media=media,
    )


async def count_download_in_period__by_profile(profile: Profile, start_time: datetime, end_time: datetime) -> int:
    return len([md async for md in MediaDownload.objects.filter(profile=profile,
                                                                download_date__gte=start_time,
                                                                download_date__lte=end_time)])


async def can_download_media(profile: Profile) -> bool:
    role = await get_role_by_profile(profile)
    allowed_downloads_per_day = role.allowed_downloads_per_day
    today = datetime.datetime.today()
    count_downloads = await count_download_in_period__by_profile(profile,
                                                                 start_time=today - datetime.timedelta(days=1),
                                                                 end_time=today)
    if count_downloads > allowed_downloads_per_day:
        return False

    return True

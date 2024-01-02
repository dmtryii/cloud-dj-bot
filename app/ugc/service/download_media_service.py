import datetime

from .profile_service import ProfileService
from ..models import Profile, Media, MediaDownload


class DownloadMediaService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    async def can_download(self, profile: Profile) -> bool:
        role = await self._profile_service.get_role(profile)
        delay_between_downloads = role.delay_between_downloads

        last_download = await self.last_download(profile)

        if last_download is None:
            return True

        last_download_time = last_download.download_date

        current_time = datetime.datetime.now(datetime.timezone.utc)
        time_since_last_download = current_time - last_download_time

        if time_since_last_download.total_seconds() >= delay_between_downloads:
            return True

        return False

    @staticmethod
    async def add_download(profile: Profile, media: Media):
        return await MediaDownload.objects.acreate(
            profile=profile,
            media=media,
        )

    @staticmethod
    async def last_download(profile: Profile) -> MediaDownload:
        return await MediaDownload.objects.filter(profile=profile).alast()

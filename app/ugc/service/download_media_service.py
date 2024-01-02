import datetime
from typing import Optional

from .profile_service import ProfileService
from ..models import Media, MediaDownload


class DownloadMediaService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    async def can_download(self) -> bool:
        role = await self._profile_service.get_role()
        delay_between_downloads = role.delay_between_downloads

        last_download = await self.last_download()

        if last_download is None:
            return True

        last_download_time = last_download.download_date

        current_time = datetime.datetime.now(datetime.timezone.utc)
        time_since_last_download = current_time - last_download_time

        if time_since_last_download.total_seconds() >= delay_between_downloads:
            return True

        return False

    async def add_download(self, media: Media) -> None:
        profile = await self._profile_service.get()
        return await MediaDownload.objects.acreate(
            profile=profile,
            media=media,
        )

    async def last_download(self) -> Optional[MediaDownload]:
        profile = await self._profile_service.get()
        return await MediaDownload.objects.filter(profile=profile).alast()

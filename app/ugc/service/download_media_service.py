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

    async def get_message_id(self, media: Media) -> Optional[int]:
        profile = await self._profile_service.get()
        media_download = await MediaDownload.objects.filter(profile=profile, media=media).afirst()

        if media_download:
            return media_download.message_id

    async def add_download(self, message_id: int, media: Media) -> None:
        profile = await self._profile_service.get()
        media_download, created = await MediaDownload.objects.aget_or_create(
            profile=profile,
            media=media,
            defaults={
                "message_id": message_id
            }
        )

        if not created:
            media_download.message_id = message_id
            await media_download.asave()

        return media_download

    async def last_download(self) -> Optional[MediaDownload]:
        profile = await self._profile_service.get()
        return await MediaDownload.objects.filter(profile=profile).alast()

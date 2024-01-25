import datetime
import os
from typing import Optional

from .media_service import MediaService
from .profile_service import ProfileService
from ..exceptions.media_exception import MediaDownloadNotFound
from ..exceptions.role_exception import RoleDelayBetweenDownloadsExceeded
from ..models import MediaDownload
from ..utils.downloaders.media_downloader import MediaDownloader


class DownloadMediaService:

    def __init__(self, profile_service: ProfileService, media_service: MediaService):
        self._profile_service = profile_service
        self._media_service = media_service

    def download_video(self, profile_id: str, media_id: str,
                       media_downloader: MediaDownloader) -> str:
        return self._download_media(profile_id, media_id, media_downloader.download_video)

    def download_audio(self, profile_id: str, media_id: str,
                       media_downloader: MediaDownloader) -> str:
        return self._download_media(profile_id, media_id, media_downloader.download_audio)

    def _download_media(self, profile_id: str, media_id: str,
                        download_func) -> str:
        if not self.can_download(profile_id):
            role = self._profile_service.get_role(profile_id)
            delay_between_downloads = role.delay_between_downloads
            raise RoleDelayBetweenDownloadsExceeded('Delay between downloads - {}'.format(delay_between_downloads))

        output = None

        try:
            media = self._media_service.get(media_id)
            output = download_func(media.url)
            return output
        except Exception as e:
            self.cleanup_file(output)
            print(f'Error downloading media {e}')

    def can_download(self, profile_id: str) -> bool:
        role = self._profile_service.get_role(profile_id)
        delay_between_downloads = role.delay_between_downloads

        last_download = self._last_download(profile_id)

        if not last_download:
            return True

        last_download_time = last_download.download_date

        current_time = datetime.datetime.now(datetime.timezone.utc)
        time_since_last_download = current_time - last_download_time

        if time_since_last_download.total_seconds() >= delay_between_downloads:
            return True

        return False

    def get(self, profile_id: str, media_id: str) -> Optional[MediaDownload]:
        profile = self._profile_service.get(profile_id)
        media = self._media_service.get(media_id)
        media_download = MediaDownload.objects.filter(profile=profile, media=media).first()

        if not media_download:
            raise MediaDownloadNotFound('MediaDownload not found for profile: {} and media: {}'
                                        .format(profile, media))
        return media_download

    def add_download(self, message_id: str, profile_id: str, media_id: str) -> MediaDownload:
        profile = self._profile_service.get(profile_id)
        media = self._media_service.get(media_id)
        media_download, created = MediaDownload.objects.get_or_create(
            profile=profile,
            media=media,
            defaults={
                "message_id": message_id
            }
        )

        if not created:
            media_download.message_id = message_id
            media_download.save()

        return media_download

    def _last_download(self, profile_id: str) -> Optional[MediaDownload]:
        profile = self._profile_service.get(profile_id)
        return MediaDownload.objects.filter(profile=profile).last()

    @staticmethod
    def cleanup_file(path: str) -> None:
        try:
            if path:
                os.remove(path)
        except Exception as e:
            print(f"Error removing file: {e}")

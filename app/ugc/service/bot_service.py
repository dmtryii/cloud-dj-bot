import asyncio
import os

from aiogram.types import FSInputFile, CallbackQuery

from .download_media_service import DownloadMediaService
from .profile_service import ProfileService
from ..models import Media
from ..utils.downloaders.media_downloader import MediaDownloader


class BotMediaService:
    VIDEO = 'video'
    AUDIO = 'audio'

    def __init__(self, query: CallbackQuery, profile_service: ProfileService,
                 download_media_service: DownloadMediaService, downloader: MediaDownloader):
        self._query = query
        self._profile_service = profile_service
        self._download_media_service = download_media_service
        self._downloader = downloader

    async def send_video(self, media: Media, caption: str = '', warning: str = '') -> None:
        telegram_file_id = media.telegram_video_file_id

        if telegram_file_id:
            await self._query.message.answer_video(video=telegram_file_id, caption=caption)
        else:
            await self._handle_new_media_file(media, self.VIDEO, warning=warning)

    async def send_audio(self, media: Media, caption: str = '', warning: str = '') -> None:
        telegram_file_id = media.telegram_audio_file_id

        if telegram_file_id:
            await self._query.message.answer_audio(audio=telegram_file_id, caption=caption)
        else:
            await self._handle_new_media_file(media, self.AUDIO, warning=warning)

    async def _handle_new_media_file(self, media: Media, media_type: str, warning: str = '') -> None:
        if not await self._download_media_service.can_download():
            await self._query.answer(warning)
            return

        await self._download_media_service.add_download(media)
        await self._query.answer('Downloading, please wait...')

        path = None
        try:
            path = await self._download_media(self._downloader, media_type)
            await self._send_media_message(media, path, media_type)
        except Exception as e:
            print(f"Error sending media: {e}")
        finally:
            await self._cleanup_file(path)

    async def _download_media(self, downloader: MediaDownloader, media_type: str) -> str:
        if media_type == self.VIDEO:
            return await downloader.download_video()
        elif media_type == self.AUDIO:
            return await downloader.download_audio()

    async def _send_media_message(self, media: Media, path: str, media_type: str, caption: str = '') -> None:
        if media_type == self.VIDEO:
            msg = await self._query.message.answer_video(video=FSInputFile(path), caption=caption)
            media.telegram_video_file_id = msg.video.file_id
        elif media_type == self.AUDIO:
            msg = await self._query.message.answer_audio(audio=FSInputFile(path), caption=caption)
            media.telegram_audio_file_id = msg.audio.file_id
        await media.asave()

    @staticmethod
    async def _cleanup_file(path: str) -> None:
        await asyncio.sleep(1)
        try:
            if path:
                os.remove(path)
        except Exception as e:
            print(f"Error removing file: {e}")

import asyncio
import os

from aiogram.types import FSInputFile, CallbackQuery

from .download_media_service import DownloadMediaService
from .media_service import MediaService
from .profile_service import ProfileService
from ..models import Media
from ..utils.downloaders.media_downloader import YouTubeDownloader, MediaDownloader, InstagramDownloader


class BotMediaService:
    VIDEO = 'video'
    AUDIO = 'audio'

    def __init__(self, query: CallbackQuery, profile_service: ProfileService,
                 download_media_service: DownloadMediaService, media: Media, caption: str = '', warning: str = ''):
        self._query = query
        self._profile_service = profile_service
        self._download_media_service = download_media_service
        self._media = media
        self._caption = caption
        self._warning = warning

    async def send_video(self) -> None:
        telegram_file_id = self._media.telegram_video_file_id

        if telegram_file_id:
            await self._query.message.answer_video(video=telegram_file_id, caption=self._caption)
        else:
            await self._handle_external_media(self.VIDEO)

    async def send_audio(self) -> None:
        telegram_file_id = self._media.telegram_audio_file_id

        if telegram_file_id:
            await self._query.message.answer_audio(audio=telegram_file_id, caption=self._caption)
        else:
            await self._handle_external_media(self.AUDIO)

    async def _handle_external_media(self, media_type: str) -> None:
        social_network = self._media.external_id.split('_')[0]

        if social_network == 'yt':
            downloader = YouTubeDownloader(self._media)
        elif social_network == 'inst':
            downloader = InstagramDownloader(self._media, MediaService(self._profile_service))
        else:
            return

        await self._handle_new_media_file(downloader, media_type)

    async def _handle_new_media_file(self, downloader: MediaDownloader, media_type: str) -> None:
        chat_id = self._query.message.chat.id
        profile = await self._profile_service.get_by_external_id(external_id=chat_id)

        if not await self._download_media_service.can_download(profile):
            await self._query.answer(self._warning)
            return

        await self._download_media_service.add_download(profile, self._media)
        await self._query.answer('Downloading, please wait...')

        path = None
        try:
            path = await self._download_media(downloader, media_type)
            await self._send_media_message(path, media_type)
            await self._media.asave()
        except Exception as e:
            print(f"Error sending media: {e}")
        finally:
            await self._cleanup_file(path)

    async def _download_media(self, downloader: MediaDownloader, media_type: str) -> str:
        if media_type == self.VIDEO:
            return await downloader.download_video()
        elif media_type == self.AUDIO:
            return await downloader.download_audio()

    async def _send_media_message(self, path: str, media_type: str) -> None:
        if media_type == self.VIDEO:
            msg = await self._query.message.answer_video(video=FSInputFile(path), caption=self._caption)
            self._media.telegram_video_file_id = msg.video.file_id
        elif media_type == self.AUDIO:
            msg = await self._query.message.answer_audio(audio=FSInputFile(path), caption=self._caption)
            self._media.telegram_audio_file_id = msg.audio.file_id

    @staticmethod
    async def _cleanup_file(path: str) -> None:
        await asyncio.sleep(1)
        try:
            if path:
                os.remove(path)
        except Exception as e:
            print(f"Error removing file: {e}")

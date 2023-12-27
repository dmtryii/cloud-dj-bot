import asyncio
from abc import ABC
from typing import Optional

from django.conf import settings
from pytube import YouTube

from ...models import Media


class MediaDownloader(ABC):
    def __init__(self, media: Media):
        self.media = media
        self.output_path = settings.MEDIA_FILES

    async def download_video(self) -> str:
        pass

    async def download_audio(self) -> str:
        pass


class YouTubeDownloader(MediaDownloader):
    def __init__(self, media: Media):
        super().__init__(media)

    async def download_video(self) -> Optional[str]:
        try:
            video = YouTube(self.media.url)
            stream = video.streams.filter(file_extension="mp4").first()
            return await asyncio.to_thread(stream.download,
                                           output_path=self.output_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def download_audio(self) -> Optional[str]:
        try:
            video = YouTube(self.media.url)
            stream = video.streams.filter(only_audio=True).first()
            return await asyncio.to_thread(stream.download,
                                           output_path=self.output_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

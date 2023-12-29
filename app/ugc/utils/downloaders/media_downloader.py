import asyncio
import os
from abc import ABC
from typing import Optional

from django.conf import settings
from instaloader import Post
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube

from ..media_utils import InstagramLoader
from ...models import Media
from ...service.media_service import get_media_id_without_prefix


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


class InstagramDownloader(MediaDownloader):
    def __init__(self, media: Media):
        super().__init__(media)

    async def download_video(self) -> Optional[str]:
        inst_loader_singleton = InstagramLoader()
        inst_loader = inst_loader_singleton.inst_loader

        inst_loader.dirname_pattern = self.output_path

        shortcode = await get_media_id_without_prefix(self.media)
        post = Post.from_shortcode(context=inst_loader.context, shortcode=shortcode)
        filename = os.path.join(self.output_path, f"{post.owner_username}_{shortcode}")
        inst_loader.filename_pattern = filename

        inst_loader.download_pictures = False
        inst_loader.download_videos = True
        inst_loader.download_post(post, filename)

        for file in os.listdir(self.output_path):
            file_path = os.path.join(self.output_path, file)
            try:
                if not file.endswith(".mp4"):
                    os.remove(file_path)
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        return filename + '.mp4'

    async def download_audio(self) -> Optional[str]:
        video_path = await self.download_video()

        if video_path:
            audio_path = self.convert_video_to_audio(video_path)
            os.remove(video_path)
            return audio_path

        return None

    def convert_video_to_audio(self, video_path: str) -> str:
        audio_path = video_path.replace(".mp4", ".mp3")

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        audio_clip.write_audiofile(audio_path)
        video_clip.close()

        return audio_path

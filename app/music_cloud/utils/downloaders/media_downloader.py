import os
import re
from abc import ABC
from typing import Optional

from django.conf import settings
from instaloader import Post
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube

from .. import regular_expressions
from ..media_utils import InstagramLoader


class MediaDownloader(ABC):

    OUTPUT_PATH = settings.MEDIA_FILES

    def download_video(self, url: str) -> str:
        pass

    def download_audio(self, url: str) -> str:
        pass


class YouTubeDownloader(MediaDownloader):
    def download_video(self, url: str) -> Optional[str]:
        try:
            video = YouTube(url)
            stream = video.streams.filter(file_extension="mp4", res="360p").first()
            return stream.download(output_path=self.OUTPUT_PATH)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def download_audio(self, url: str) -> Optional[str]:
        try:
            video = YouTube(url)
            stream = video.streams.filter(only_audio=True).first()
            return stream.download(output_path=self.OUTPUT_PATH)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


class InstagramDownloader(MediaDownloader):
    def download_video(self, url: str) -> Optional[str]:
        inst_loader_singleton = InstagramLoader()
        inst_loader = inst_loader_singleton.inst_loader

        inst_loader.dirname_pattern = self.OUTPUT_PATH

        shortcode = self._extract_shortcode(url)
        post = Post.from_shortcode(context=inst_loader.context, shortcode=shortcode)
        filename = os.path.join(self.OUTPUT_PATH, f"{post.owner_username}_{shortcode}")
        inst_loader.filename_pattern = filename

        inst_loader.download_pictures = False
        inst_loader.download_videos = True
        inst_loader.download_post(post, filename)

        for file in os.listdir(self.OUTPUT_PATH):
            file_path = os.path.join(self.OUTPUT_PATH, file)
            try:
                if not file.endswith(".mp4"):
                    os.remove(file_path)
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        return filename + '.mp4'

    def download_audio(self, url: str) -> Optional[str]:
        video_path = self.download_video(url)

        if video_path:
            audio_path = self._convert_video_to_audio(video_path)
            os.remove(video_path)
            return audio_path

        return None

    @staticmethod
    def _convert_video_to_audio(video_path: str) -> str:
        audio_path = video_path.replace(".mp4", ".mp3")

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        audio_clip.write_audiofile(audio_path)
        video_clip.close()

        return audio_path

    @staticmethod
    def _extract_shortcode(url: str) -> Optional[str]:
        pattern = re.compile(regular_expressions.INSTAGRAM_EXTRACT_SHORTCODE)
        match = pattern.match(url)

        if match:
            shortcode = match.group(1)
            return shortcode

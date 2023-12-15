import asyncio
import os

from django.conf import settings
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube


async def download_video(url: str) -> str | None:
    try:
        video = YouTube(url)
        stream = video.streams.filter(file_extension="mp4").first()
        output_path = settings.MEDIA_FILES
        file_path = await asyncio.to_thread(stream.download, output_path=output_path)
        return file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


async def convert_video_to_audio(url: str) -> str | None:
    try:
        video_path = await download_video(url)
        if video_path is None:
            return None

        audio_path = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path, codec='mp3')

        video_clip.close()
        audio_clip.close()
        os.remove(video_path)

        return audio_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

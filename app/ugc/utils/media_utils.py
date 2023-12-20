import asyncio

from django.conf import settings
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


async def download_audio(url: str) -> str | None:
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        output_path = settings.MEDIA_FILES
        file_path = await asyncio.to_thread(stream.download, output_path=output_path)
        return file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

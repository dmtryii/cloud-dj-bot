import asyncio

from django.conf import settings
from pytube import YouTube

from ..models import Media


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


async def get_media_info_cart(media: Media) -> str:
    duration = divmod(media.duration, 60)
    return (f'{media.title}\n\n' +
            f'Channel: {media.channel}\n' +
            f'Duration: {duration[0]}:{duration[1]}\n')

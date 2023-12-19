from pytube import YouTube

from ..models import Media


async def map_youtube_media(url: str) -> Media:
    youtube = YouTube(url)
    return Media(
        external_id=f'ty_{youtube.video_id}',
        title=youtube.title,
        url=url,
        duration=youtube.length,
        channel=youtube.author
    )

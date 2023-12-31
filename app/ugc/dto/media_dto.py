import re
from typing import Optional

from instaloader import Post
from pytube import YouTube

from ..models import Media
from ..utils.media_utils import InstagramLoader


async def map_youtube_media(url: str) -> Media:
    youtube = YouTube(url)
    return Media(
        external_id=f'yt_{youtube.video_id}',
        title=youtube.title,
        url=url,
        duration=youtube.length,
        channel=youtube.author
    )


async def map_instagram_media(url: str) -> Media:

    inst_loader_singleton = InstagramLoader()
    inst_loader = inst_loader_singleton.inst_loader

    post = Post.from_shortcode(context=inst_loader.context, shortcode=extract_shortcode(url))

    if post.is_video:
        return Media(
            external_id=f'inst_{post.shortcode}',
            title=remove_hashtags(post.caption if post.caption else 'no_name').strip(),
            url=url,
            duration=round(post.video_duration),
            channel=post.owner_username
        )


def extract_shortcode(url: str) -> Optional[str]:
    pattern = re.compile(r'https?://(?:www\.)?instagram\.com/(?:reel|reels|p)/([^/]+)/?')
    match = pattern.match(url)

    if match:
        shortcode = match.group(1)
        return shortcode


def remove_hashtags(text):
    hashtag_pattern = re.compile(r'#\w+')
    return re.sub(hashtag_pattern, '', text)

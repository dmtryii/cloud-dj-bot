import re
from abc import ABC
from typing import Optional

from instaloader import Post
from pytube import YouTube

from ..models import Media
from ..utils.media_utils import InstagramLoader


class MediaMapper(ABC):
    def map(self, url: str) -> Media:
        pass

    @staticmethod
    def _remove_hashtags(text: str):
        hashtag_pattern = re.compile(r'#\w+')
        return re.sub(hashtag_pattern, '', text)


class YouTubeMapper(MediaMapper):
    def map(self, url: str) -> Media:
        youtube = YouTube(url)
        return Media(
            media_id=f'yt_{youtube.video_id}',
            title=self._remove_hashtags(youtube.title),
            url=url,
            duration=youtube.length,
            channel=youtube.author
        )


class InstagramMapper(MediaMapper):
    def map(self, url: str) -> Media:
        inst_loader_singleton = InstagramLoader()
        inst_loader = inst_loader_singleton.inst_loader

        post = Post.from_shortcode(context=inst_loader.context, shortcode=self._extract_shortcode(url))

        if post.is_video:
            return Media(
                media_id=f'inst_{post.shortcode}',
                title=self._remove_hashtags(post.caption if post.caption else 'no_name').strip(),
                url=url,
                duration=round(post.video_duration),
                channel=post.owner_username
            )

    @staticmethod
    def _extract_shortcode(url: str) -> Optional[str]:
        pattern = re.compile(r'https?://(?:www\.)?instagram\.com/(?:reel|reels|p)/([^/]+)/?')
        match = pattern.match(url)

        if match:
            shortcode = match.group(1)
            return shortcode

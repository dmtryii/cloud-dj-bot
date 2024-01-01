import re
from abc import ABC
from typing import Optional

from instaloader import Post
from pytube import YouTube

from ..models import Media
from ..utils import regular_expressions
from ..utils.media_utils import InstagramLoader


class MediaMapper(ABC):
    def __init__(self, url: str):
        self.url = url

    async def map(self) -> Media:
        pass

    @staticmethod
    def _remove_hashtags(text: str):
        hashtag_pattern = re.compile(r'#\w+')
        return re.sub(hashtag_pattern, '', text)


class YouTubeMapper(MediaMapper):
    def __init__(self, url: str):
        super().__init__(url)

    def map(self) -> Media:
        youtube = YouTube(self.url)
        return Media(
            external_id=f'yt_{youtube.video_id}',
            title=self._remove_hashtags(youtube.title),
            url=self.url,
            duration=youtube.length,
            channel=youtube.author
        )


class InstagramMapper(MediaMapper):
    def __init__(self, url: str):
        super().__init__(url)

    def map(self) -> Media:
        inst_loader_singleton = InstagramLoader()
        inst_loader = inst_loader_singleton.inst_loader

        post = Post.from_shortcode(context=inst_loader.context, shortcode=self._extract_shortcode(self.url))

        if post.is_video:
            return Media(
                external_id=f'inst_{post.shortcode}',
                title=self._remove_hashtags(post.caption if post.caption else 'no_name').strip(),
                url=self.url,
                duration=round(post.video_duration),
                channel=post.owner_username
            )

    @staticmethod
    def _extract_shortcode(url: str) -> Optional[str]:
        pattern = re.compile(regular_expressions.INSTAGRAM_EXTRACT_SHORTCODE)
        match = pattern.match(url)

        if match:
            shortcode = match.group(1)
            return shortcode

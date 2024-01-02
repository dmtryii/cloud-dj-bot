import re
from abc import ABC
from typing import Optional

from instaloader import Post
from pytube import YouTube

from ..utils import regular_expressions
from ..utils.media_utils import InstagramLoader


class MediaDTO:
    def __init__(self, external_id: str, title: str, url: str, duration: int, channel: str):
        self.external_id = external_id
        self.title = title
        self.url = url
        self.duration = duration
        self.channel = channel


class MediaMapper(ABC):
    def __init__(self, url: str):
        self.url = url

    async def map(self) -> MediaDTO:
        pass

    @staticmethod
    def _remove_hashtags(text: str):
        hashtag_pattern = re.compile(r'#\w+')
        return re.sub(hashtag_pattern, '', text)


class YouTubeMapper(MediaMapper):
    def __init__(self, url: str):
        super().__init__(url)

    def map(self) -> MediaDTO:
        youtube = YouTube(self.url)
        return MediaDTO(
            external_id=f'yt_{youtube.video_id}',
            title=self._remove_hashtags(youtube.title),
            url=self.url,
            duration=youtube.length,
            channel=youtube.author
        )


class InstagramMapper(MediaMapper):
    def __init__(self, url: str):
        super().__init__(url)

    def map(self) -> MediaDTO:
        inst_loader_singleton = InstagramLoader()
        inst_loader = inst_loader_singleton.inst_loader

        post = Post.from_shortcode(context=inst_loader.context, shortcode=self._extract_shortcode(self.url))

        if post.is_video:
            return MediaDTO(
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

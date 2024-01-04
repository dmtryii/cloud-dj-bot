from typing import Optional, List

from .profile_service import ProfileService
from ..exceptions.media_exception import MediaNotFound, MediaProfileNotFound
from ..mappers.media_mapper import MediaDTO
from ..models import Media, MediaProfile


class MediaService:
    def __init__(self, media: MediaDTO, profile_service: ProfileService):
        self._media = media
        self._profile_service = profile_service

    async def get(self) -> Media:
        return await self._get_or_create()

    @classmethod
    async def get_instance_by_id(cls, media_id: int, profile_service: ProfileService):
        media = await Media.objects.aget(id=media_id)

        if not media:
            raise MediaNotFound('Media not found for ID: {}'.format(media_id))

        return cls(media, profile_service)

    @classmethod
    async def get_by_id(cls, media_id: int, profile_service: ProfileService) -> Optional[Media]:
        media = await Media.objects.aget(id=media_id)

        if not media:
            raise MediaNotFound('Media not found for ID: {}'.format(media_id))

        return await cls(media, profile_service).get()

    async def get_social_network(self) -> str:
        return self._media.external_id.split('_')[0]

    async def get_id_without_prefix(self) -> str:
        media = await self.get()
        prefix = media.external_id.split('_')[0]
        return media.external_id[len(prefix)+1:]

    async def get_by_profile(self) -> Optional[MediaProfile]:
        profile = await self._profile_service.get()
        media = await self.get()
        media_profile = await MediaProfile.objects.filter(
            profile=profile,
            media=media).afirst()

        if not media_profile:
            raise MediaProfileNotFound('MediaProfile not found for profile: {} and media: {}'
                                       .format(media_profile.profile, media_profile.media))
        return media_profile

    async def add_to_profile(self) -> MediaProfile:
        profile = await self._profile_service.get()
        media = await self.get()
        return await MediaProfile.objects.aget_or_create(
            profile=profile,
            media=media,
        )

    async def get_all_by_profile__reverse(self) -> List[Media]:
        profile = await self._profile_service.get()
        return [media async for media in Media.objects.filter(mediaprofile__profile=profile)][::-1]

    async def get_all_favorite_by_profile__reverse(self) -> List[Media]:
        profile = await self._profile_service.get()
        return [media async for media in Media.objects.filter(mediaprofile__profile=profile,
                                                              mediaprofile__is_favorite=True)][::-1]

    async def _get_or_create(self) -> Media:
        media, _ = await Media.objects.aget_or_create(
            external_id=self._media.external_id,
            defaults={
                'telegram_video_file_id': '',
                'telegram_audio_file_id': '',
                'title': self._media.title,
                'url': self._media.url,
                'duration': self._media.duration,
                'channel': self._media.channel,
            }
        )
        return media

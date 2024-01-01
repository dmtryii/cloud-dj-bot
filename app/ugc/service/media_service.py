from .profile_service import ProfileService
from ..models import Media, MediaProfile, Profile


class MediaService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    @staticmethod
    async def get_or_create(media: Media) -> Media:
        media, created = await Media.objects.aget_or_create(
            external_id=media.external_id,
            defaults={
                'telegram_video_file_id': media.telegram_video_file_id,
                'telegram_audio_file_id': media.telegram_audio_file_id,
                'title': media.title,
                'url': media.url,
                'duration': media.duration,
                'channel': media.channel,
            }
        )
        return media

    @staticmethod
    async def get_by_id(media_id: int) -> Media:
        return await Media.objects.aget(id=media_id)

    @staticmethod
    async def get_id_without_prefix(media: Media) -> str:
        prefix = media.external_id.split('_')[0]
        return media.external_id[len(prefix)+1:]

    @staticmethod
    async def get_by_profile(profile: Profile, media: Media) -> MediaProfile:
        return await MediaProfile.objects.filter(
            profile=profile,
            media=media).afirst()

    async def get_all_by_profile__reverse(self, profile: Profile):
        profile = await self._profile_service.get_or_create(profile)
        return [media async for media in Media.objects.filter(mediaprofile__profile=profile)][::-1]

    async def get_all_favorite_by_profile__reverse(self, profile: Profile):
        profile = await self._profile_service.get_or_create(profile)
        return [media async for media in Media.objects.filter(mediaprofile__profile=profile,
                                                              mediaprofile__is_favorite=True)][::-1]

    async def add_to_profile(self, profile: Profile, media: Media) -> MediaProfile:
        profile = await self._profile_service.get_or_create(profile)
        media = await self.get_or_create(media)
        media_profile, created = await MediaProfile.objects.aget_or_create(
            profile=profile,
            media=media,
        )
        return media_profile

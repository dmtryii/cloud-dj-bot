from typing import Optional, List

from .profile_service import ProfileService
from ..exceptions.media_exception import MediaNotFound, MediaProfileNotFound
from ..exceptions.role_exception import RoleMediaLengthExceeded
from ..mappers.media_mapper import MediaMapper
from ..models import Media, MediaProfile


class MediaService:
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    def create(self, url: str, mapper: MediaMapper) -> Media:
        media_map = mapper.map(url)
        media, _ = Media.objects.get_or_create(
            media_id=media_map.media_id,
            defaults={
                'telegram_video_file_id': '',
                'telegram_audio_file_id': '',
                'title': media_map.title,
                'url': media_map.url,
                'duration': media_map.duration,
                'channel': media_map.channel,
            }
        )
        return media

    def set_telegram_video_id(self, media_id: str, telegram_video_file_id: str) -> Media:
        media = self.get(media_id)
        media.telegram_video_file_id = telegram_video_file_id
        media.save()
        return media

    def set_telegram_audio_id(self, media_id: str, telegram_audio_file_id: str) -> Media:
        media = self.get(media_id)
        media.telegram_audio_file_id = telegram_audio_file_id
        media.save()
        return media

    def add_to_profile(self, media_id: str, profile_id: str) -> MediaProfile:
        media = self.get(media_id)
        profile = self._profile_service.get(profile_id)

        if not self.can_add_media(profile_id, media_id):
            max_length = profile.role.allowed_media_length
            raise RoleMediaLengthExceeded(f"The maximum allowed video length is {max_length}")

        media_profile, _ = MediaProfile.objects.get_or_create(
            profile=profile,
            media=media,
        )
        return media_profile

    def add_to_favorites(self, media_id: str, profile_id: str) -> MediaProfile:
        media_profile = self.get_by_profile(media_id, profile_id)
        media_profile.is_favorite = not media_profile.is_favorite
        media_profile.save()
        return media_profile

    def get(self, media_id: str) -> Optional[Media]:
        media = Media.objects.get(media_id=media_id)

        if not media:
            raise MediaNotFound('Media not found for ID: {}'.format(media_id))

        return media

    def get_by_profile(self, media_id: str, profile_id: str) -> Optional[MediaProfile]:
        profile = self._profile_service.get(profile_id)
        media = self.get(media_id)
        media_profile = MediaProfile.objects.filter(
            profile=profile,
            media=media).first()

        if not media_profile:
            raise MediaProfileNotFound('MediaProfile not found for profile: {} and media: {}'
                                       .format(media_profile.profile, media_profile.media))
        return media_profile

    def get_all_by_profile(self, profile_id: str) -> List[Media]:
        profile = self._profile_service.get(profile_id)
        return Media.objects.filter(mediaprofile__profile=profile)

    def get_all_favorite_by_profile(self, profile_id: str) -> List[Media]:
        profile = self._profile_service.get(profile_id)
        return Media.objects.filter(mediaprofile__profile=profile,
                                    mediaprofile__is_favorite=True)

    def get_count(self, profile_id: str) -> int:
        profile = self._profile_service.get(profile_id)
        return Media.objects.filter(mediaprofile__profile=profile).count()

    def get_favorite_count(self, profile_id: str) -> int:
        profile = self._profile_service.get(profile_id)
        return Media.objects.filter(mediaprofile__profile=profile,
                                    mediaprofile__is_favorite=True).count()

    def get_for_profile_on_counter(self, profile_id: str, media_counter: int) -> Media:
        if media_counter > self.get_count(profile_id):
            raise MediaNotFound('Media not found for count: {}'.format(media_counter))

        profile = self._profile_service.get(profile_id)
        media_profile = MediaProfile.objects.filter(profile=profile).order_by('date_added')
        return media_profile[media_counter].media

    def get_favorite_for_profile_on_counter(self, profile_id: str, media_counter: int) -> Media:
        if media_counter > self.get_favorite_count(profile_id):
            raise MediaNotFound('Media not found for count: {}'.format(media_counter))

        profile = self._profile_service.get(profile_id)
        media_profile = MediaProfile.objects.filter(profile=profile,
                                                    is_favorite=True).order_by('date_added')
        return media_profile[media_counter].media

    def can_add_media(self, profile_id: str, media_id: str) -> bool:
        profile = self._profile_service.get(profile_id)
        role = profile.role
        media = self.get(media_id)

        return media.duration <= role.allowed_media_length

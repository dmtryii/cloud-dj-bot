from rest_framework import status
from rest_framework.views import APIView, Response

from .mappers.media_mapper import YouTubeMapper, InstagramMapper
from .serializers import ProfileCreateSerializer, RoleSerializer, MediaUrlSerializer, MediaAddToProfileSerializer, \
    MediaSerializer, MediaProfileSerializer, ProfileSerializer, MediaDownloadSerializer, \
    CurrentActionSetMessageSerializer, CurrentActionSerializer, \
    DownloaderSerializer, DownloadedMediaFileSerializer, MediaSetTelegramVideoIdSerializer, \
    MediaSetTelegramAudioIdSerializer, MediaDownloadUpdateSerializer
from .services.current_action_service import CurrentActionService
from .services.download_media_service import DownloadMediaService
from .services.media_service import MediaService
from .services.profile_service import ProfileService
from .utils.downloaders.media_downloader import YouTubeDownloader, MediaDownloader, InstagramDownloader


class BaseView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_service = ProfileService()
        self.media_service = MediaService(self.profile_service)
        self.current_action_service = CurrentActionService(self.profile_service)
        self.download_media_service = DownloadMediaService(self.profile_service, self.media_service)


class BaseMediaCreateView(BaseView):
    def create_media(self, request, media_mapper):
        serializer = MediaUrlSerializer(data=request.data)

        if serializer.is_valid():
            media_response = self.media_service.create(serializer.data.get('url'), media_mapper)
            return Response(
                MediaSerializer(media_response).data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MediaYoutubeCreateView(BaseMediaCreateView):
    def post(self, request):
        return self.create_media(request, YouTubeMapper())


class MediaInstagramCreateView(BaseMediaCreateView):
    def post(self, request):
        return self.create_media(request, InstagramMapper())


class BaseDownloaderView(BaseView):
    def download(self, request, media_downloader: MediaDownloader):
        serializer = DownloaderSerializer(data=request.data)

        if serializer.is_valid():

            profile_id = serializer.data.get('profile_id')
            media_id = serializer.data.get('media_id')
            media_type = serializer.data.get('media_type')

            if media_type == 'video':
                output = self.download_media_service.download_video(
                    profile_id, media_id, media_downloader
                )
            elif media_type == 'audio':
                output = self.download_media_service.download_audio(
                    profile_id, media_id, media_downloader
                )
            else:
                return Response({'error': 'Invalid media_type'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'output': output}, status=status.HTTP_200_OK)


class DownloaderYoutubeView(BaseDownloaderView):
    def post(self, request):
        return self.download(request, YouTubeDownloader())


class DownloaderInstagramView(BaseDownloaderView):
    def post(self, request):
        return self.download(request, InstagramDownloader())


class DownloaderDeleteFile(BaseView):
    def post(self, request):
        serializer = DownloadedMediaFileSerializer(data=request.data)

        if serializer.is_valid():
            output = serializer.data.get('output')
            self.download_media_service.cleanup_file(output)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileGetCurrentActionView(BaseView):
    def get(self, request, profile_id):
        current_action = self.current_action_service.get(
            profile_id
        )
        return Response(
            CurrentActionSerializer(current_action).data,
            status=status.HTTP_200_OK
        )


class ProfileSetCurrentActionView(BaseView):
    def post(self, request):
        serializer = CurrentActionSetMessageSerializer(data=request.data)

        if serializer.is_valid():
            current_action = self.current_action_service.create(serializer.validated_data['message_id'],
                                                                serializer.validated_data['profile_id'])
            return Response(
                CurrentActionSerializer(current_action).data,
                status=status.HTTP_200_OK
            )


class MediaSetTelegramVideoIdView(BaseView):
    def patch(self, request):
        serializer = MediaSetTelegramVideoIdSerializer(data=request.data)

        if serializer.is_valid():
            media_id = serializer.validated_data['media_id']
            telegram_video_file_id = serializer.validated_data['telegram_video_file_id']
            media = self.media_service.set_telegram_video_id(media_id, telegram_video_file_id)

            return Response(
                MediaSerializer(media).data,
                status=status.HTTP_200_OK
            )


class MediaSetTelegramAudioIdView(BaseView):
    def patch(self, request):
        serializer = MediaSetTelegramAudioIdSerializer(data=request.data)

        if serializer.is_valid():
            media_id = serializer.validated_data['media_id']
            telegram_video_file_id = serializer.validated_data['telegram_audio_file_id']
            media = self.media_service.set_telegram_audio_id(media_id, telegram_video_file_id)

            return Response(
                MediaSerializer(media).data,
                status=status.HTTP_200_OK
            )


class MediaDownloadGetView(BaseView):
    def get(self, request, profile_id, media_id, *args, **kwargs):
        download_media = self.download_media_service.get(profile_id, media_id)
        return Response(
            MediaDownloadSerializer(download_media).data,
            status=status.HTTP_200_OK
        )


class MediaDownloadUpdateView(BaseView):
    def patch(self, request, *args, **kwargs):
        serializer = MediaDownloadUpdateSerializer(data=request.data)

        if serializer.is_valid():
            message_id = serializer.validated_data['message_id']
            profile_id = serializer.validated_data['profile_id']
            media_id = serializer.validated_data['media_id']

            media_download = self.download_media_service.add_download(message_id, profile_id, media_id)

            return Response(
                MediaDownloadSerializer(media_download).data,
                status=status.HTTP_200_OK
            )


class MediaAddToFavoriteView(BaseView):
    def patch(self, request):
        serializer = MediaAddToProfileSerializer(data=request.data)

        if serializer.is_valid():
            media_id = serializer.validated_data['media_id']
            profile_id = serializer.validated_data['profile_id']

            media_profile = self.media_service.add_to_favorites(media_id, profile_id)

            return Response(
                MediaProfileSerializer(media_profile).data,
                status=status.HTTP_200_OK
            )


class MediaForProfileOnCounterView(BaseView):
    def get(self, request, profile_id):
        counter = request.query_params.get('counter')
        media = self.media_service.get_for_profile_on_counter(profile_id, int(counter))

        return Response(
            MediaSerializer(media).data,
            status=status.HTTP_200_OK
        )


class MediaFavoriteForProfileOnCounterView(BaseView):
    def get(self, request, profile_id):
        counter = request.query_params.get('counter')
        media = self.media_service.get_favorite_for_profile_on_counter(profile_id, int(counter))

        return Response(
            MediaSerializer(media).data,
            status=status.HTTP_200_OK
        )


class MediaGetByIdView(BaseView):
    def get(self, request, media_id):
        media_response = self.media_service.get(media_id)
        return Response(
            MediaSerializer(media_response).data,
            status=status.HTTP_200_OK
        )


class MediaCountView(BaseView):
    def get(self, request, profile_id):
        media_count = self.media_service.get_count(profile_id)
        return Response(
            {'count': media_count}, status=status.HTTP_200_OK
        )


class MediaFavoriteCountView(BaseView):
    def get(self, request, profile_id):
        media_count = self.media_service.get_favorite_count(profile_id)
        return Response(
            {'count': media_count}, status=status.HTTP_200_OK
        )


class MediaProfileView(BaseView):
    def get(self, request, profile_id, media_id):
        media_profile = self.media_service.get_by_profile(media_id, profile_id)
        return Response(
            MediaProfileSerializer(media_profile).data,
            status=status.HTTP_200_OK
        )


class MediaProfileAddView(BaseView):
    def post(self, request):
        serializer = MediaAddToProfileSerializer(data=request.data)

        if serializer.is_valid():
            media_id = serializer.validated_data['media_id']
            profile_id = serializer.validated_data['profile_id']
            media_profile = self.media_service.add_to_profile(media_id, profile_id)

            return Response(
                MediaProfileSerializer(media_profile).data,
                status=status.HTTP_201_CREATED
            )


class ProfileCreateView(BaseView):
    def post(self, request):
        serializer = ProfileCreateSerializer(data=request.data)

        if serializer.is_valid():
            profile = self.profile_service.create(
                profile_id=serializer.data.get('profile_id'),
                username=serializer.data.get('username'),
                first_name=serializer.data.get('first_name'),
                last_name=serializer.data.get('last_name')
            )
            return Response(
                ProfileSerializer(profile).data,
                status=status.HTTP_201_CREATED
            )


class ProfileView(BaseView):
    def get(self, request, profile_id):
        profile = self.profile_service.get(profile_id)
        return Response(
            ProfileSerializer(profile).data,
            status=status.HTTP_200_OK
        )


class ProfileGetRoleView(BaseView):
    def get(self, request, profile_id):
        role = self.profile_service.get_role(profile_id)
        return Response(
            RoleSerializer(role).data,
            status=status.HTTP_200_OK
        )

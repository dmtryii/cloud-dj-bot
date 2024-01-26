from rest_framework import serializers

from .models import Role, Profile, Media, MediaProfile, MediaDownload, CurrentAction


class MediaDownloadUpdateSerializer(serializers.Serializer):
    message_id = serializers.CharField()
    profile_id = serializers.CharField()
    media_id = serializers.CharField()


class MediaSetTelegramVideoIdSerializer(serializers.Serializer):
    media_id = serializers.CharField()
    telegram_video_file_id = serializers.CharField()


class MediaSetTelegramAudioIdSerializer(serializers.Serializer):
    media_id = serializers.CharField()
    telegram_audio_file_id = serializers.CharField()


class DownloadedMediaFileSerializer(serializers.Serializer):
    output = serializers.CharField()


class DownloaderSerializer(serializers.Serializer):
    profile_id = serializers.CharField()
    media_id = serializers.CharField()
    media_type = serializers.CharField()


class CurrentActionSetMessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    profile_id = serializers.CharField()


class MediaAddToProfileSerializer(serializers.Serializer):
    media_id = serializers.CharField()
    profile_id = serializers.CharField()


class ProfileCreateSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)


class MediaUrlSerializer(serializers.Serializer):
    url = serializers.CharField()


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class MediaProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaProfile
        fields = '__all__'


class MediaDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaDownload
        fields = '__all__'


class CurrentActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAction
        fields = '__all__'

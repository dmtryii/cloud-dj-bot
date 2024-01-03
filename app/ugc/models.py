from django.db import models


class Media(models.Model):
    external_id = models.CharField(
        verbose_name='Media ID',
        unique=True,
        max_length=255,
    )
    telegram_video_file_id = models.CharField(
        verbose_name='Telegram Video File ID',
        max_length=255,
    )
    telegram_audio_file_id = models.CharField(
        verbose_name='Telegram Audio File ID',
        max_length=255,
    )
    title = models.TextField(
        verbose_name='Title',
        null=False,
    )
    url = models.TextField(
        verbose_name='Url',
        null=False,
    )
    channel = models.TextField(
        verbose_name='Channel',
        null=False
    )
    duration = models.IntegerField(
        verbose_name='Duration',
        null=False,
    )
    date_of_addition = models.DateTimeField(
        verbose_name='Date of addition',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title} (#{self.external_id})'

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Medias'


class Role(models.Model):
    name = models.CharField(
        verbose_name='Role name',
        max_length=255,
        unique=True,
    )
    delay_between_downloads = models.PositiveIntegerField(
        verbose_name='Delay between downloads',
        null=False,
    )
    allowed_media_length = models.PositiveIntegerField(
        verbose_name='Allowed Media Length',
        null=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class Profile(models.Model):
    external_id = models.BigIntegerField(
        verbose_name='Profile ID',
        unique=True,
    )
    username = models.TextField(
        verbose_name='Username',
        null=True,
    )
    first_name = models.TextField(
        verbose_name='First Name',
        null=True,
    )
    last_name = models.TextField(
        verbose_name='Last Name',
        null=True,
    )
    first_login_date = models.DateTimeField(
        verbose_name='First login date',
        auto_now_add=True,
    )
    role = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Role',
    )

    def __str__(self):
        return f'#{self.external_id} {self.username}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class MediaProfile(models.Model):
    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
        verbose_name='Media',
    )
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        verbose_name='Profile',
    )
    is_favorite = models.BooleanField(
        verbose_name='Is Favorite',
        default=False,
    )
    date_added = models.DateTimeField(
        verbose_name='Date Added',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Media Profile'
        verbose_name_plural = 'Media Profiles'
        unique_together = ('media', 'profile')


class MediaDownload(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
    )
    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
    )
    download_date = models.DateTimeField(
        verbose_name='Date Downloaded',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Media Download'
        verbose_name_plural = 'Media Downloads'


class Message(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Message ID',
    )
    content_type = models.TextField(
        verbose_name='Content Type',
    )
    profile = models.ForeignKey(
        'Profile',
        verbose_name='Profile',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Text',
    )
    created_at = models.DateTimeField(
        verbose_name='Time of receiving',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Message {self.text} from {self.profile}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class CurrentAction(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
    )
    message_id = models.PositiveIntegerField(
        verbose_name='Message ID',
    )

    class Meta:
        verbose_name = 'CurrentAction'
        verbose_name_plural = 'CurrentActions'

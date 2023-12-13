from django.db import models


class Media(models.Model):
    external_id = models.CharField(
        verbose_name='Media ID',
        unique=True,
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


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Profile ID',
        unique=True,
    )
    username = models.TextField(
        verbose_name='Username',
    )
    first_login_date = models.DateTimeField(
        verbose_name='First login date',
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        verbose_name='Is Active',
        default=False,
    )

    PROFILE_STATE_CHOICES = {
        ('BASIC', 'Basic State'),
        ('WAIT_FOR_EMAIL', 'Wait for Email'),
    }
    state = models.CharField(
        choices=PROFILE_STATE_CHOICES,
        default='BASIC',
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
    date_added = models.DateTimeField(
        verbose_name='Date Added',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Media Profile'
        verbose_name_plural = 'Media Profiles'
        unique_together = ('media', 'profile')


class Hashtag(models.Model):
    title = models.CharField(
        verbose_name='Title',
        max_length=255,
    )
    create_at = models.DateTimeField(
        verbose_name='Create At',
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'


class MediaProfileHashtag(models.Model):
    media_profile = models.ForeignKey(
        'MediaProfile',
        on_delete=models.CASCADE,
        verbose_name='MediaProfile',
    )
    hashtag = models.ForeignKey(
        'Hashtag',
        on_delete=models.CASCADE,
        verbose_name='Hashtag',
    )

    class Meta:
        verbose_name = 'Media Profile Hashtag'
        verbose_name_plural = 'Media Profiles Hashtags'
        unique_together = ('media_profile', 'hashtag')


class Contacts(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    first_name = models.TextField(
        verbose_name='First Name'
    )
    last_name = models.TextField(
        verbose_name='Last Name'
    )
    email = models.EmailField(
        verbose_name='Email',
    )

    def __str__(self):
        return f'Email: {self.email}'

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class CurrentAction(models.Model):
    profile = models.ForeignKey(
        'Profile',
        verbose_name='Profile',
        on_delete=models.CASCADE
    )
    media = models.ForeignKey(
        'Media',
        verbose_name='Media',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Current Action'
        verbose_name_plural = 'Current Actions'


class Message(models.Model):
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

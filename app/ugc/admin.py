from django.contrib import admin

from .models import Profile, Media, MediaProfile, Hashtag


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'first_login_date', 'is_active', 'state')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'title', 'url', 'channel', 'duration', 'date_of_addition')


@admin.register(MediaProfile)
class MediaProfileAdmin(admin.ModelAdmin):
    list_display = ('media', 'profile', 'date_added')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at')

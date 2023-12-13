from django.contrib import admin

from .models import Profile, Contacts, Media, MediaProfile, Hashtag, CurrentAction


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_login_date', 'is_active', 'state')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'first_name', 'last_name', 'email')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'title', 'url', 'channel', 'duration', 'date_of_addition')


@admin.register(CurrentAction)
class CurrentActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'media')


@admin.register(MediaProfile)
class MediaProfileAdmin(admin.ModelAdmin):
    list_display = ('media', 'profile', 'date_added')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at')

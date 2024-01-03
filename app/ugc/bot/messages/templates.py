from ...models import Profile, Role, Media

from django.conf import settings


def default_message() -> str:
    return 'I do not understand you'


def start_message(profile: Profile) -> str:
    return f'''
Hello <b>{profile.first_name}</b>!
I am a <b>BOT</b> for downloading and arranging media resources from social networks.

You can:
- download media (video or audio)
- view history
- add media to favorites

Just send me a link to the <b>media resource</b> and follow the instructions.

<b>Available social networks - YouTube and Instagram.</b>
    '''


def video_len_limit_message(role: Role) -> str:
    return f'''
Sorry, you are <b>not</b> allowed to download videos longer 
than <b>{convert_seconds(role.allowed_media_length)}</b> minutes.

You can contact the administrator for help - {settings.BOT_ADMIN_NAME}.
        '''


def video_download_limit_message(second: int) -> str:
    return f'''
You are allowed to download media with a delay 
of {convert_seconds(second)}
        '''


def video_caption(media: Media) -> str:
    return f'{media.title}\nAuthor: {media.channel}\n{settings.BOT_NAME}'


def audio_caption(media: Media) -> str:
    return f'Author: {media.channel}\n{settings.BOT_NAME}'


def get_media_info_cart(media: Media, title: str = '') -> str:
    return (f'<b>{title}</b>\n' +
            f'<a href="{media.url}">{media.title}</a>\n' +
            f'Author: {media.channel}\n' +
            f'Duration: {convert_seconds(media.duration)}')


def convert_seconds(seconds) -> str:
    minutes, seconds = divmod(seconds, 60)
    return format_time_tuple((int(minutes), int(seconds)))


def format_time_tuple(time_tuple: tuple) -> str:
    return f"{time_tuple[0]:02d}:{time_tuple[1]:02d}"


from django.conf import settings


def default_message() -> str:
    return 'I do not understand you.'


def start_message(first_name: str) -> str:
    return f'''
Hello <b>{first_name}</b>!
I am a <b>BOT</b> for downloading and arranging media resources from social networks.

You can:
- download media (video or audio)
- view history
- add media to favorites

Just send me a link to the <b>media resource</b> and follow the instructions.

<b>Available social networks - YouTube and Instagram.</b>
    '''


def help_message() -> str:
    return f'''
Click on the menu and choose the desired action.

You can:
- download media (video or audio)
- view history
- add media to favorites

Just send me a link to the <b>media resource</b> and follow the instructions.

<b>Available social networks - YouTube and Instagram.</b>

You can contact the administrator for help - {settings.BOT_ADMIN_NAME}.
    '''


def get_media_info_cart(media_title: str, url: str, author: str, duration: int, title: str = '') -> str:
    return (f'<b>{title}</b>\n' +
            f'<a href="{url}">{media_title}</a>\n' +
            f'Author: {author}\n' +
            f'Duration: {convert_seconds(duration)}')


def media_caption(title: str, channel: str) -> str:
    return f'{title}\nAuthor: {channel}\n{settings.BOT_NAME}'


def role_restriction(allowed_media_length: int, delay_between_downloads: int) -> str:
    return f'''
There are restrictions on your account:
- You are <b>not</b> allowed to download videos longer than <b>{convert_seconds(allowed_media_length)}</b> minutes.
- The delay between downloads should exceed <b>{convert_seconds(delay_between_downloads)}</b> minutes.

You can contact the administrator for help - {settings.BOT_ADMIN_NAME}.
    '''


def convert_seconds(seconds) -> str:
    minutes, seconds = divmod(seconds, 60)
    return format_time_tuple((int(minutes), int(seconds)))


def format_time_tuple(time_tuple: tuple) -> str:
    return f"{time_tuple[0]:02d}:{time_tuple[1]:02d}"

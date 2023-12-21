from ...models import Profile, Media, Role


async def default_message() -> str:
    return 'I do not understand you'


def start_message(profile: Profile) -> str:
    return f'''
Hello <b>{profile.first_name}</b>!
I am a <b>BOT</b> for downloading and arranging media resources from social networks.

You can:
- download media (video or audio)
- view history
- add media to favorites
- create playlists (adding tags)

Just send me a link to the <b>media resource</b> and follow the instructions.
    '''


def video_len_limit_message(role: Role) -> str:
    return f'''
Sorry, you are <b>not</b> allowed to download videos longer 
than <b>{convert_seconds(role.allowed_media_length)}</b> minutes.

You can contact the administrator for help.
        '''


def video_download_limit_message() -> str:
    return f'''
You have exceeded the number of download attempts allowed. 
Try again later.
        '''


def video_caption(media: Media) -> str:
    return f'{media.title}\n\nChannel: {media.channel}\n'


def audio_caption(media: Media) -> str:
    return f'Channel: {media.channel}'


def get_media_info_cart(media: Media, title: str = '') -> str:
    return (f'<b>{title}</b>\n' +
            f'<a href="{media.url}">{media.title}</a>\n' +
            f'Channel: {media.channel}\n' +
            f'Duration: {convert_seconds(media.duration)}')


def convert_seconds(seconds) -> str:
    minutes, seconds = divmod(seconds, 60)
    return format_time_tuple((int(minutes), int(seconds)))


def format_time_tuple(time_tuple: tuple) -> str:
    return f"{time_tuple[0]:02d}:{time_tuple[1]:02d}"

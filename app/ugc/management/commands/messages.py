from ...models import Profile, Media


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

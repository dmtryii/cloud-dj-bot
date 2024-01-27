from aiogram.client.session import aiohttp
from django.conf import settings


async def get_start(profile: dict) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=profile) as response:
            return await response.json()


async def get_role(profile_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/roles'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def get_current_action(profile_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/current-actions'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def set_current_action(profile_id: str, message_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/current-actions'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={'message_id': message_id, 'profile_id': profile_id}) as response:
            return await response.json()


async def get_media(media_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/media/{media_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def set_telegram_video_id(media_id: str, telegram_video_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/telegram-video-id'
    async with aiohttp.ClientSession() as session:
        async with session.patch(api_url, json={'media_id': media_id,
                                                'telegram_video_file_id': telegram_video_id}) as response:
            return await response.json()


async def set_telegram_audio_id(media_id: str, telegram_audio_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/telegram-audio-id'
    async with aiohttp.ClientSession() as session:
        async with session.patch(api_url, json={'media_id': media_id,
                                                'telegram_audio_file_id': telegram_audio_id}) as response:
            return await response.json()


async def get_profile_history_count(profile_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/medias/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def get_profile_favorite_count(profile_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/medias/favorite/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def swap_media_favorites(profile_id: str, media_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profile/media/favorite'
    async with aiohttp.ClientSession() as session:
        async with session.patch(api_url, json={'profile_id': profile_id, 'media_id': media_id}) as response:
            return await response.json()


async def get_media_for_profile_on_counter(profile_id: str, media_counter: int) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/media?counter={media_counter}'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def get_media_favorite_for_profile_on_counter(profile_id: str, media_counter: int) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/media/favorite?counter={media_counter}'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def add_media_to_profile(profile_id: str, media_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/medias'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={'profile_id': profile_id, 'media_id': media_id}) as response:
            return await response.json()


async def create_media_youtube(url: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/youtube/'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={'url': url}) as response:
            return await response.json()


async def create_media_instagram(url: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/instagram/'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={'url': url}) as response:
            return await response.json()


async def download_youtube_media(profile_id: str, media_id: str, media_type: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/youtube/download'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url,
                                json={
                                    'profile_id': profile_id,
                                    'media_id': media_id,
                                    'media_type': media_type
                                }) as response:
            return await response.json()


async def download_instagram_media(profile_id: str, media_id: str, media_type: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/instagram/download'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url,
                                json={
                                    'profile_id': profile_id,
                                    'media_id': media_id,
                                    'media_type': media_type
                                }) as response:
            return await response.json()


async def add_download_media(message_id: str, profile_id: str, media_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/medias/downloads'
    async with aiohttp.ClientSession() as session:
        async with session.patch(api_url,
                                 json={
                                     'message_id': message_id,
                                     'profile_id': profile_id,
                                     'media_id': media_id
                                 }) as response:
            return await response.json()


async def get_download_media(profile_id: str, media_id: str) -> dict:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/profiles/{profile_id}/medias/{media_id}/downloads'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()


async def delete_download(output: str) -> None:
    api_url = f'{settings.MUSIC_CLOUD_API_URL}/medias/download/delete'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={'output': output}):
            pass

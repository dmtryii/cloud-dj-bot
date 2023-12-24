import asyncio
import os

from aiogram.types import FSInputFile, CallbackQuery

from .download_media_service import can_download_media, add_download_media
from .profile_service import get_profile_by_external_id
from ..models import Media
from ..utils.media_utils import download_video, download_audio


async def send_media(query: CallbackQuery, media: Media, send_media_func,
                     caption: str = '', warning: str = '') -> None:
    file_id_attr = f"telegram_{send_media_func.__name__.replace('send_', '')}_file_id"
    file_id = getattr(media, file_id_attr, None)
    chat_id = query.message.chat.id

    if file_id:
        await send_media_func(chat_id=chat_id,
                              caption=caption, **{file_id_attr.split('_')[1]: file_id})
    else:
        await handle_missing_file_id(query, media, send_media_func,
                                     caption, warning, file_id_attr)


async def handle_missing_file_id(query: CallbackQuery, media: Media,
                                 send_media_func, caption, warning, file_id_attr):
    chat_id = query.message.chat.id
    profile = await get_profile_by_external_id(external_id=chat_id)

    if not await can_download_media(profile):
        await query.answer(warning)
        return

    await add_download_media(profile, media)

    path = None
    try:
        download_func = download_video if send_media_func.__name__ == 'send_video' else download_audio

        path = await download_func(media.url)
        await send_with_file_id(chat_id, caption, file_id_attr, media, path, send_media_func)
    except Exception as e:
        print(f"Error sending media: {e}")
    finally:
        await cleanup_file(path)


async def send_with_file_id(chat_id, caption, file_id_attr, media, path, send_media_func):
    msg = await send_media_func(chat_id=chat_id,
                                caption=caption,
                                **{file_id_attr.split('_')[1]: FSInputFile(path)})
    setattr(media, file_id_attr, getattr(msg, file_id_attr.split('_')[1]).file_id)
    await media.asave()


async def cleanup_file(path):
    await asyncio.sleep(1)
    try:
        if path:
            os.remove(path)
    except Exception as e:
        print(f"Error removing file: {e}")

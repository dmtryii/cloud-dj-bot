import asyncio
import os

from aiogram.types import FSInputFile

from .download_media_service import can_download_media, add_download_media
from .profile_service import get_profile_by_external_id
from ..models import Media
from ..utils.media_utils import download_video, download_audio


async def send_media(chat_id: int, media: Media, send_media_func, send_warning_func,
                     caption: str = '', warning: str = '') -> None:
    file_id_attr = f"telegram_{send_media_func.__name__.replace('send_', '')}_file_id"
    file_id = getattr(media, file_id_attr, None)

    if file_id:
        await send_media_func(chat_id=chat_id,
                              caption=caption,
                              **{file_id_attr.split('_')[1]: file_id})
    else:
        profile = await get_profile_by_external_id(external_id=chat_id)

        if not await can_download_media(profile):
            await send_warning_func(chat_id, warning)
            return

        await add_download_media(profile, media)

        path = None
        try:
            download_func = download_video if send_media_func.__name__ == 'send_video' else download_audio

            path = await download_func(media.url)
            msg = await send_media_func(chat_id=chat_id,
                                        caption=caption,
                                        **{file_id_attr.split('_')[1]: FSInputFile(path)})
            setattr(media, file_id_attr, getattr(msg, file_id_attr.split('_')[1]).file_id)
            await media.asave()
        except Exception as e:
            print(f"Error sending media: {e}")
        finally:
            await asyncio.sleep(1)
            try:
                if path:
                    os.remove(path)
            except Exception as e:
                print(f"Error removing file: {e}")

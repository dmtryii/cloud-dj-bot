import asyncio
import os

from aiogram.types import FSInputFile

from ..models import Media


async def send_media(chat_id: int, media: Media, send_func, download_func, caption: str = '') -> None:
    telegram_file_id_attr = f'telegram_{send_func.__name__.replace("send_", "")}_file_id'
    file_type = send_func.__name__.replace("send_", "")

    telegram_file_id = getattr(media, telegram_file_id_attr, None)

    if telegram_file_id:
        await send_func(chat_id=chat_id, caption=caption, **{file_type: telegram_file_id})
    else:
        path = await download_func(media.url)
        try:
            msg = await send_func(chat_id=chat_id, caption=caption, **{file_type: FSInputFile(path)})
            setattr(media, telegram_file_id_attr, getattr(msg, file_type).file_id)
            await media.asave()
        except Exception as e:
            print(f"Error sending media: {e}")
        finally:
            await asyncio.sleep(1)
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error removing file: {e}")
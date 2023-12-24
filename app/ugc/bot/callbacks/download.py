from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.inline import SelectDownloadType, Action
from ...management.commands.bot import send_video, send_audio
from ...service.media_service import get_media_by_id


router = Router()


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         send_function) -> None:
    media = await get_media_by_id(callback_data.media_id)
    await send_function(query=query, media=media)


@router.callback_query(SelectDownloadType.filter(F.action == Action.VIDEO_DOWNLOAD))
async def handle_video_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, send_video)


@router.callback_query(SelectDownloadType.filter(F.action == Action.AUDIO_DOWNLOAD))
async def handle_audio_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, send_audio)

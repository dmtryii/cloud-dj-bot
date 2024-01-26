from aiogram import F, Router
from aiogram.types import CallbackQuery

from .. import data_fetcher
from ..keyboards.inline import SelectDownloadType, Action
from ..services.bot_media_service import BotMediaService

router = Router()


async def _handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         media_type: str) -> None:

    media_prefix = callback_data.media_id.split('_', 1)[0]

    if media_prefix == 'yt':
        bot_media_service = BotMediaService(query, media_type, data_fetcher.download_youtube_media)
    elif media_prefix == 'inst':
        bot_media_service = BotMediaService(query, media_type, data_fetcher.download_instagram_media)
    else:
        return

    if media_type == BotMediaService.VIDEO:
        await bot_media_service.send_video(callback_data.media_id)
    elif media_type == BotMediaService.AUDIO:
        await bot_media_service.send_audio(callback_data.media_id)


@router.callback_query(SelectDownloadType.filter(F.action == Action.VIDEO_DOWNLOAD))
async def handle_video_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await _handle_media_download_callback(query, callback_data, BotMediaService.VIDEO)


@router.callback_query(SelectDownloadType.filter(F.action == Action.AUDIO_DOWNLOAD))
async def handle_audio_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await _handle_media_download_callback(query, callback_data, BotMediaService.AUDIO)

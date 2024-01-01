from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.inline import SelectDownloadType, Action
from ..messages import templates
from ...service.bot_service import BotMediaService
from ...service.media_service import get_media_by_id
from ...service.profile_service import get_profile_by_external_id, get_role_by_profile

router = Router()


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         media_type: str) -> None:
    media = await get_media_by_id(callback_data.media_id)
    profile = await get_profile_by_external_id(query.message.chat.id)
    role = await get_role_by_profile(profile)
    caption = templates.video_caption(media)
    warning = templates.video_download_limit_message(role.delay_between_downloads)
    bot_media_service = BotMediaService(query=query, media=media, caption=caption, warning=warning)

    if media_type == BotMediaService.VIDEO:
        await bot_media_service.send_video()
    elif media_type == BotMediaService.AUDIO:
        await bot_media_service.send_audio()


@router.callback_query(SelectDownloadType.filter(F.action == Action.VIDEO_DOWNLOAD))
async def handle_video_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, BotMediaService.VIDEO)


@router.callback_query(SelectDownloadType.filter(F.action == Action.AUDIO_DOWNLOAD))
async def handle_audio_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, BotMediaService.AUDIO)

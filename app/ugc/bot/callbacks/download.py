from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.inline import SelectDownloadType, Action
from ..messages import templates
from ...service.bot_service import BotMediaService
from ...service.download_media_service import DownloadMediaService
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService

router = Router()


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         media_type: str) -> None:
    profile_service = ProfileService()
    download_media_service = DownloadMediaService(profile_service)

    media = await MediaService.get_by_id(callback_data.media_id)
    profile = await profile_service.get_by_external_id(query.message.chat.id)
    role = await profile_service.get_role(profile)
    caption = templates.video_caption(media)
    warning = templates.video_download_limit_message(role.delay_between_downloads)

    bot_media_service = BotMediaService(query=query, profile_service=profile_service,
                                        download_media_service=download_media_service,
                                        media=media, caption=caption, warning=warning)

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

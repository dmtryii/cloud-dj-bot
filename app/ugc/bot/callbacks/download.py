from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.inline import SelectDownloadType, Action
from ..messages import templates
from ...mappers.profile_mapper import ProfileMapper
from ...service.bot_service import BotMediaService
from ...service.download_media_service import DownloadMediaService
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService
from ...utils.downloaders.media_downloader import YouTubeDownloader, InstagramDownloader

router = Router()


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         media_type: str) -> None:
    profile_dto = ProfileMapper(query.message.chat).map()
    profile_service = ProfileService(profile_dto)
    media = await MediaService.get_by_id(callback_data.media_id, profile_service)
    media_service = await MediaService.get_instance_by_id(media.id, profile_service)
    download_media_service = DownloadMediaService(profile_service)

    role = await profile_service.get_role()
    caption = templates.video_caption(media)
    warning = templates.video_download_limit_message(role.delay_between_downloads)

    social_network = await media_service.get_social_network()

    if social_network == 'yt':
        downloader = YouTubeDownloader(media)
    elif social_network == 'inst':
        downloader = InstagramDownloader(media, media_service)
    else:
        return

    bot_media_service = BotMediaService(query=query, profile_service=profile_service,
                                        download_media_service=download_media_service,
                                        downloader=downloader)

    if media_type == BotMediaService.VIDEO:
        await bot_media_service.send_video(media, caption=caption, warning=warning)
    elif media_type == BotMediaService.AUDIO:
        await bot_media_service.send_audio(media, caption=caption, warning=warning)


@router.callback_query(SelectDownloadType.filter(F.action == Action.VIDEO_DOWNLOAD))
async def handle_video_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, BotMediaService.VIDEO)


@router.callback_query(SelectDownloadType.filter(F.action == Action.AUDIO_DOWNLOAD))
async def handle_audio_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, BotMediaService.AUDIO)

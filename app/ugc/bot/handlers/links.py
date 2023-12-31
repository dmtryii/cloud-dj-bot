from aiogram import Router, F, types

from ..keyboards.inline import select_download_type
from ..messages import templates
from ..messages.templates import get_media_info_cart
from ...mappers.media_mapper import YouTubeMapper, InstagramMapper, MediaDTO
from ...mappers.profile_mapper import ProfileMapper
from ...service.current_action_service import CurrentActionService
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService
from ...utils import regular_expressions

router = Router()


async def handle_media_url(message: types.Message, media_dto: MediaDTO) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    current_action_service = CurrentActionService(profile_service)

    media_service = MediaService(media_dto, profile_service)

    role = await profile_service.get_role()

    if media_dto.duration > role.allowed_media_length:
        msg = await message.answer(
            text=templates.video_len_limit_message(role),
            parse_mode='HTML'
        )
        await current_action_service.swap_current_action(msg.message_id)
        return

    media = await media_service.get()
    await media_service.add_to_profile()

    msg = await message.answer(
        text=get_media_info_cart(media),
        reply_markup=select_download_type(media_id=media.id),
        parse_mode='HTML'
    )
    await current_action_service.swap_current_action(msg.message_id)


@router.message(F.text.regexp(regular_expressions.YOUTUBE))
async def youtube_url_handler(message: types.Message) -> None:
    await handle_media_url(message=message,
                           media_dto=YouTubeMapper(message.text).map())


@router.message(F.text.regexp(regular_expressions.INSTAGRAM))
async def instagram_url_handler(message: types.Message) -> None:
    await handle_media_url(message=message,
                           media_dto=InstagramMapper(message.text).map())

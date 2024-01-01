from aiogram import Router, F, types

from ..keyboards.inline import select_download_type
from ..messages import templates
from ..messages.templates import get_media_info_cart
from ...mappers.media_mapper import YouTubeMapper, InstagramMapper
from ...mappers.profile_mapper import ProfileMapper
from ...management.commands.bot import swap_current_action
from ...models import Media
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService
from ...utils import regular_expressions

router = Router()


async def handle_media_url(message: types.Message, media_dto: Media) -> None:
    await message.delete()

    profile_service = ProfileService()
    media_service = MediaService(profile_service)

    profile_dto = ProfileMapper(message.chat).map()
    profile = await profile_service.get_or_create(profile_dto)
    role = await profile_service.get_role(profile)

    if media_dto.duration > role.allowed_media_length:
        await message.answer(
            text=templates.video_len_limit_message(role),
            parse_mode='HTML'
        )
        return

    media = await media_service.get_or_create(media_dto)
    await media_service.add_to_profile(media=media, profile=profile)

    msg = await message.answer(
        text=get_media_info_cart(media),
        reply_markup=select_download_type(media_id=media.id),
        parse_mode='HTML'
    )
    await swap_current_action(profile, msg)


@router.message(F.text.regexp(regular_expressions.YOUTUBE))
async def youtube_url_handler(message: types.Message) -> None:
    await handle_media_url(message=message,
                           media_dto=YouTubeMapper(message.text).map())


@router.message(F.text.regexp(regular_expressions.INSTAGRAM))
async def instagram_url_handler(message: types.Message) -> None:
    await handle_media_url(message=message,
                           media_dto=InstagramMapper(message.text).map())

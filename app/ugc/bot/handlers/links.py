from aiogram import Router, F, types

from ..keyboards.inline import select_download_type
from ..messages import templates
from ..messages.templates import get_media_info_cart
from ...dto.media_dto import map_youtube_media
from ...dto.profile_dto import map_profile
from ...management.commands.bot import swap_current_action
from ...service.media_service import get_or_create_media, add_media_to_profile
from ...service.profile_service import get_or_create_profile, get_role_by_profile

router = Router()


@router.message(F.text.regexp(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$'))
async def youtube_url_handler(message: types.Message) -> None:
    await message.delete()
    youtube_url = message.text

    profile_dto = await map_profile(message.chat)
    media_dto = await map_youtube_media(youtube_url)
    profile = await get_or_create_profile(profile_dto)
    media = await get_or_create_media(media_dto)

    role = await get_role_by_profile(profile)

    if media.duration > role.allowed_media_length:
        await message.answer(
            text=templates.video_len_limit_message(role),
            parse_mode='HTML'
        )
        return

    await add_media_to_profile(media=media, profile=profile)
    msg = await message.answer(
        text=get_media_info_cart(media),
        reply_markup=select_download_type(media.id),
        parse_mode='HTML'
    )
    await swap_current_action(profile, msg)

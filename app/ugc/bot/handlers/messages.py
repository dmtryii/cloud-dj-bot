from aiogram import Router, F, types

from ..keyboards.inline import media_pagination
from ..messages import templates
from ..messages.templates import get_media_info_cart
from ...mappers.profile_mapper import ProfileMapper
from ...management.commands.bot import swap_current_action
from ...service.media_service import MediaService
from ...service.message_service import MessageService
from ...service.profile_service import ProfileService

router = Router()


@router.message(F.text.lower().in_(['history', 'favorite']))
async def show_media(message: types.Message) -> None:
    await message.delete()

    profile_service = ProfileService()
    media_service = MediaService(profile_service)
    profile = ProfileMapper(message.chat).map()

    types_mapping = {
        'history': media_service.get_all_by_profile__reverse,
        'favorite': media_service.get_all_favorite_by_profile__reverse
    }

    media_type = message.text.lower()
    medias = await types_mapping[media_type](profile)

    if len(medias) == 0:
        await message.answer(text=f"You don't have {media_type} media yet")
        return

    answer_text = get_media_info_cart(medias[0], title=media_type.upper())

    msg = await message.answer(
        text=answer_text,
        reply_markup=media_pagination(medias[0].id,
                                      media_type,
                                      total_pages=len(medias)),
        parse_mode='HTML'
    )
    await swap_current_action(profile, msg)


@router.message()
async def default_handler(message: types.Message) -> None:
    profile_service = ProfileService()
    message_service = MessageService(profile_service)
    profile = ProfileMapper(message.chat).map()
    answer = await templates.default_message()
    await message.reply(answer)
    await message_service.save(profile, message)

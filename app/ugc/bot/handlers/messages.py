from aiogram import Router, F, types

from ..keyboards.inline import media_pagination
from ..messages import templates
from ..messages.templates import get_media_info_cart
from ...dto.profile_dto import map_profile
from ...management.commands.bot import swap_current_action
from ...service.media_service import get_all_media_by_profile__reverse, get_all_favorite_media_by_profile__reverse
from ...service.message_service import save_message

router = Router()


@router.message(F.text.lower().in_(['history', 'favorite']))
async def show_media(message: types.Message) -> None:
    await message.delete()
    profile = await map_profile(message.chat)

    types_mapping = {'history': get_all_media_by_profile__reverse,
                     'favorite': get_all_favorite_media_by_profile__reverse}

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
    profile = await map_profile(message.chat)
    answer = await templates.default_message()
    await message.reply(answer)
    await save_message(profile, message)

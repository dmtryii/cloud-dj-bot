from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart, Command

from ..keyboards.inline import media_pagination
from ..messages import templates
from ..messages.templates import get_media_info_cart
from ...mappers.profile_mapper import ProfileMapper
from ...service.current_action_service import CurrentActionService
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService

router = Router()


@router.message(Command(commands=['history', 'favorite']))
async def show_media_command_handler(message: types.Message) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    current_action_service = CurrentActionService(profile_service)

    media_service = MediaService(media=None, profile_service=profile_service)

    media_type = message.text.lower()[1:]

    if media_type == 'history':
        medias = await media_service.get_all_by_profile__reverse()
    elif media_type == 'favorite':
        medias = await media_service.get_all_favorite_by_profile__reverse()
    else:
        return

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
    await current_action_service.swap_current_action(msg.message_id)


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    current_action_service = CurrentActionService(profile_service)
    profile = await profile_service.get()

    answer = templates.start_message(profile)
    msg = await message.answer(
        text=answer,
        parse_mode='HTML')
    await current_action_service.swap_current_action(msg.message_id)


@router.message(Command(commands=['help']))
async def help_command_handler(message: types.Message) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    current_action_service = CurrentActionService(profile_service)

    answer = templates.help_message()
    msg = await message.answer(
        text=answer,
        parse_mode='HTML'
    )
    await current_action_service.swap_current_action(msg.message_id)

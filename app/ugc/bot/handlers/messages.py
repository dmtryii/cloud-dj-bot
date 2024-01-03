from aiogram import Router, types

from ..messages import templates
from ...management.commands.bot import swap_current_action
from ...mappers.profile_mapper import ProfileMapper
from ...service.message_service import MessageService
from ...service.profile_service import ProfileService

router = Router()


@router.message()
async def default_handler(message: types.Message) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    message_service = MessageService(profile_service)

    answer = templates.default_message()
    msg = await message.answer(answer)
    await swap_current_action(profile_dto, msg)

    await message_service.save(message)

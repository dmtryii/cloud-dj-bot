from aiogram import Router, types

from ..messages import templates
from ...mappers.profile_mapper import ProfileMapper
from ...service.current_action_service import CurrentActionService
from ...service.message_service import MessageService
from ...service.profile_service import ProfileService

router = Router()


@router.message()
async def default_handler(message: types.Message) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    current_action_service = CurrentActionService(profile_service)
    message_service = MessageService(profile_service)

    answer = templates.default_message()
    msg = await message.answer(answer)
    await current_action_service.swap_current_action(msg.message_id)

    await message_service.save(message)

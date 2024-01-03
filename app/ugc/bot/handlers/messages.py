from aiogram import Router, types

from ..messages import templates
from ...mappers.profile_mapper import ProfileMapper
from ...service.message_service import MessageService
from ...service.profile_service import ProfileService

router = Router()


@router.message()
async def default_handler(message: types.Message) -> None:
    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    message_service = MessageService(profile_service)
    answer = await templates.default_message()
    await message.reply(answer)
    await message_service.save(message)

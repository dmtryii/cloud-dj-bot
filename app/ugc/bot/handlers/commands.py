from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart

from ..keyboards.reply import main_menu
from ..messages import templates
from ...mappers.profile_mapper import ProfileMapper
from ...service.profile_service import ProfileService

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.delete()

    profile_dto = ProfileMapper(message.chat).map()
    profile_service = ProfileService(profile_dto)
    profile = await profile_service.get()

    answer = templates.start_message(profile)
    await message.answer(
        text=answer,
        reply_markup=main_menu,
        parse_mode='HTML')

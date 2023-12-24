from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart

from ..keyboards.reply import main_menu
from ..messages import templates
from ...dto.profile_dto import map_profile
from ...management.commands.bot import swap_current_action
from ...service.profile_service import get_or_create_profile

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.delete()
    profile_dto = await map_profile(message.chat)
    profile = await get_or_create_profile(profile_dto)
    answer = templates.start_message(profile)
    await message.answer(
        text=answer,
        reply_markup=main_menu,
        parse_mode='HTML')

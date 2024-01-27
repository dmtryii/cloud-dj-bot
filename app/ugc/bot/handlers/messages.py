from aiogram import Router, types

from ..services.bot_management_content_service import BotManagementService
from ...bot.messages import templates

router = Router()


@router.message()
async def default_handler(message: types.Message) -> None:
    await message.delete()

    chat_id = str(message.chat.id)

    answer = templates.default_message()
    msg = await message.answer(answer)
    await BotManagementService.swap_action(chat_id, str(msg.message_id))

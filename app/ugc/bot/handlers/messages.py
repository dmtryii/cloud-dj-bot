from aiogram import Router, types

from ...bot import main_bot
from ...bot.messages import templates

router = Router()


@router.message()
async def default_handler(message: types.Message) -> None:
    await message.delete()

    chat_id = str(message.chat.id)

    answer = templates.default_message()
    msg = await message.answer(answer)
    await main_bot.swap_action(chat_id, str(msg.message_id))

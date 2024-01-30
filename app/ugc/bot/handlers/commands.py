from typing import Callable

from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart, Command

from .. import data_fetcher
from ..keyboards.inline import media_pagination
from ..messages import templates
from ..services.bot_management_content_service import BotManagementService

router = Router()


async def _show_media(message: types.Message, command_type: str) -> None:
    await message.delete()

    chat_id = str(message.chat.id)

    media_count, media_fetcher = await _get_media_details(chat_id, command_type)

    if media_count == 0:
        msg = await message.answer(text=f"You don't have {command_type} media yet.")
        await BotManagementService.swap_action(chat_id, str(msg.message_id))
        return

    media = await media_fetcher(chat_id, 0)
    answer_text = templates.get_media_info_cart(
        media['title'],
        media['url'],
        media['channel'],
        media['duration'],
        title=command_type.upper()
    )

    msg = await message.answer(
        text=answer_text,
        reply_markup=media_pagination(media_id=media['media_id'],
                                      types=command_type,
                                      total_pages=media_count)
    )
    await BotManagementService.swap_action(chat_id, str(msg.message_id))


async def _get_media_details(chat_id: str, command_type: str) -> tuple[int, Callable]:
    if command_type == 'history':
        response_count = await data_fetcher.get_profile_history_count(chat_id)
        media_count = response_count['count']
        media_fetcher = data_fetcher.get_media_for_profile_on_counter
    else:  # command_type == 'favorite'
        response_count = await data_fetcher.get_profile_favorite_count(chat_id)
        media_count = response_count['count']
        media_fetcher = data_fetcher.get_media_favorite_for_profile_on_counter

    return media_count, media_fetcher


@router.message(Command(commands=['history', 'favorite']))
async def show_media_command_handler(message: types.Message) -> None:
    command_type = message.text.lower()[1:]
    await _show_media(message, command_type)


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.delete()
    chat = message.chat

    profile = await data_fetcher.get_start(
        {
            'profile_id': chat.id,
            'username': chat.username if chat.username else '',
            'first_name': chat.first_name if chat.username else '',
            'last_name': chat.last_name if chat.username else ''
        }
    )
    msg = await message.answer(
        text=templates.start_message(profile['first_name'])
    )
    await BotManagementService.swap_action(str(chat.id), str(msg.message_id))


@router.message(Command(commands=['help']))
async def help_command_handler(message: types.Message) -> None:
    await message.delete()
    chat_id = str(message.chat.id)

    msg = await message.answer(
        text=templates.help_message()
    )
    await BotManagementService.swap_action(chat_id, str(msg.message_id))

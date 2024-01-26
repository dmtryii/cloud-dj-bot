from aiogram import Router, F, types

from .. import main_bot
from ..exceptions import bot_exception_handler
from ..keyboards.inline import select_download_type
from ..messages import templates
from ...bot import data_fetcher
from ...utils import regular_expressions

router = Router()


async def _handle_media_message(message: types.Message, create_media_func) -> None:
    await message.delete()

    chat_id = str(message.chat.id)
    url = message.text
    media = await create_media_func(url)

    media_profile = await data_fetcher.add_media_to_profile(chat_id, media['media_id'])

    if 'error_message' in media_profile:
        msg_text = await bot_exception_handler.role_restriction(chat_id)
        msg = await main_bot.bot.send_message(chat_id=chat_id, text=msg_text, parse_mode='HTML')
        await main_bot.swap_action(chat_id, msg.message_id)
        return

    msg = await message.answer(
        text=templates.get_media_info_cart(
            media_title=media['title'],
            url=media['url'],
            author=media['channel'],
            duration=media['duration']
        ),
        reply_markup=select_download_type(media_id=media['media_id']),
        parse_mode='HTML'
    )
    await main_bot.swap_action(chat_id, str(msg.message_id))


@router.message(F.text.regexp(regular_expressions.YOUTUBE))
async def youtube_url_handler(message: types.Message) -> None:
    await _handle_media_message(message, data_fetcher.create_media_youtube)


@router.message(F.text.regexp(regular_expressions.INSTAGRAM))
async def instagram_url_handler(message: types.Message) -> None:
    await _handle_media_message(message, data_fetcher.create_media_instagram)

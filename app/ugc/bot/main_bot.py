import logging

from aiogram import Bot, Dispatcher

from django.conf import settings

from .callbacks import download, pagination, favorite
from .handlers import media_urls, messages, commands
from ..bot import data_fetcher

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


async def swap_action(chat_id: str, message_id: str) -> None:
    current_action = await data_fetcher.get_current_action(chat_id)

    if current_action:
        await delete_message(chat_id, current_action['message_id'])

    await data_fetcher.set_current_action(chat_id, message_id)


async def delete_message(chat_id: str, message_id: str) -> None:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=int(message_id))
    except Exception as e:
        logging.error(f"Error deleting message: {e}")


async def main():
    logging.basicConfig(level=logging.DEBUG)
    dp.include_routers(
        commands.router,
        media_urls.router,
        messages.router,
        download.router,
        favorite.router,
        pagination.router
    )
    await dp.start_polling(bot)

import asyncio
import logging

from aiogram import Bot, Dispatcher

from django.conf import settings
from django.core.management import BaseCommand


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


async def delete_message(chat_id: int, message_id: int) -> None:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.error(f"Error deleting message: {e}")


async def main():
    from ...bot.callbacks import download, favorite, pagination
    from ...bot.handlers import commands, links, messages
    logging.basicConfig(level=logging.DEBUG)
    dp.include_routers(
        commands.router,
        links.router,
        messages.router,
        download.router,
        favorite.router,
        pagination.router
    )
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        asyncio.run(main())

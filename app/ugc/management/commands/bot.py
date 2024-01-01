import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from django.conf import settings
from django.core.management import BaseCommand

from ...models import Profile
from ...service.current_message_service import get_current_action, set_current_action

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def swap_current_action(profile: Profile, message: types.Message) -> None:
    current_action = await get_current_action(profile)
    if current_action:
        await set_current_action(profile, message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=current_action.message_id)
    else:
        await set_current_action(profile, message.message_id)


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

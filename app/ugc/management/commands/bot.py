import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from django.conf import settings
from django.core.management import BaseCommand

from ...mappers.profile_mapper import ProfileDTO
from ...service.current_action_service import CurrentActionService
from ...service.profile_service import ProfileService

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def swap_current_action(profile_dto: ProfileDTO, message: types.Message) -> None:
    profile_service = ProfileService(profile_dto)
    current_action_service = CurrentActionService(profile_service)
    current_action = await current_action_service.get_current_action()
    if current_action:
        await current_action_service.set_current_action(message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=current_action.message_id)
    else:
        await current_action_service.set_current_action(message.message_id)


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

import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery

from django.conf import settings
from django.core.management import BaseCommand

from ...bot.messages import templates
from ...models import Media, Profile
from ...service.bot_service import send_media
from ...service.current_message_service import get_current_action, set_current_action
from ...service.profile_service import get_role_by_profile, get_profile_by_external_id

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def send_video(query: CallbackQuery, media: Media) -> None:
    chat_id = query.message.chat.id
    profile = await get_profile_by_external_id(chat_id)
    role = await get_role_by_profile(profile)
    caption = templates.video_caption(media)
    warning = templates.video_download_limit_message(role.delay_between_downloads)
    await send_media(query, media, bot.send_video,
                     caption=caption,
                     warning=warning)


async def send_audio(query: CallbackQuery, media: Media) -> None:
    chat_id = query.message.chat.id
    profile = await get_profile_by_external_id(chat_id)
    role = await get_role_by_profile(profile)
    caption = templates.audio_caption(media)
    warning = templates.video_download_limit_message(role.delay_between_downloads)
    await send_media(query, media, bot.send_audio,
                     caption=caption,
                     warning=warning)


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

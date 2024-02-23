import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from django.conf import settings

from .callbacks import download, pagination, favorite
from .handlers import media_urls, messages, commands


bot = Bot(token=settings.BOT_TOKEN,
          parse_mode='HTML')
dp = Dispatcher()


async def on_startup() -> None:
    await bot.set_webhook(f"{settings.BOT_WEBHOOK_URL}{settings.BOT_WEBHOOK_PATH}")


def main():
    logging.basicConfig(level=logging.DEBUG)
    dp.include_routers(
        commands.router,
        media_urls.router,
        messages.router,
        download.router,
        favorite.router,
        pagination.router
    )

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    webhook_requests_handler.register(app, path=settings.BOT_WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, port=int(settings.BOT_PORT))

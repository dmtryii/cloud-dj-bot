import asyncio
import logging
import os
from contextlib import suppress

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, CallbackQuery

from django.conf import settings
from django.core.management import BaseCommand
from pytube import YouTube

from .keyboards import SelectDownloadType, Action, select_download_type, pagination, Navigation, Pagination
from ...models import Media
from ...service.media_service import add_media, add_media_to_profile, get_all_media_by_profile
from ...service.message_service import save_message
from ...service.profile_service import map_profile
from ...utils.media_utils import download_video, get_media_info_cart

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def send_media(chat_id: int, media: Media, send_func, caption: str = '') -> None:
    path = await download_video(media.url)
    try:
        if send_func == bot.send_video:
            await send_func(chat_id=chat_id, caption=caption,
                            video=FSInputFile(path))
        elif send_func == bot.send_audio:
            await send_func(chat_id=chat_id, caption=caption,
                            audio=FSInputFile(path))
    except Exception as e:
        print(f"Error sending media: {e}")
    finally:
        os.remove(path)


async def send_video(chat_id: int, media: Media) -> None:
    await send_media(chat_id, media, bot.send_video,
                     caption=f'{media.title}\n\nChannel: {media.channel}\n')


async def send_audio(chat_id: int, media: Media) -> None:
    await send_media(chat_id, media, bot.send_audio,
                     caption=f'Channel: {media.channel}')


@dp.message(F.text.regexp(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$'))
async def youtube_url_handler(message: types.Message) -> None:
    profile = await map_profile(message.chat)
    youtube_url = message.text

    try:
        youtube_video_id = YouTube(youtube_url).video_id
    except Exception as e:
        print(f"Error fetching video ID: {e}")
        await message.reply("Invalid YouTube URL or unable to fetch video ID.")
        return

    media = await add_media(url=youtube_url)
    await add_media_to_profile(media=media, profile=profile)

    await message.reply(
        text=(await get_media_info_cart(media)),
        reply_markup=select_download_type(youtube_video_id)
    )


@dp.message(Command('playlist'))
async def show_playlist(message: types.Message) -> None:
    profile = await map_profile(message.chat)
    medias = await get_all_media_by_profile(profile)

    await message.answer(
        text=(await get_media_info_cart(medias[0])),
        reply_markup=pagination(medias[0].external_id)
    )


@dp.callback_query(Pagination.filter(F.navigation.in_([Navigation.PREV_STEP, Navigation.NEXT_STEP])))
async def pagination_playlist(query: CallbackQuery, callback_data: Pagination) -> None:
    profile = await map_profile(query.message.chat)
    medias = await get_all_media_by_profile(profile)

    page_num = int(callback_data.page)
    total_pages = len(medias)

    page = max(0, min(page_num - 1, total_pages - 1))

    if callback_data.navigation == Navigation.NEXT_STEP:
        page = min(page_num + 1, total_pages - 1)

    with suppress(TelegramBadRequest):
        await query.message.edit_text(
            await get_media_info_cart(medias[page]),
            reply_markup=pagination(medias[page].external_id, page)
        )
    await query.answer()


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         send_function) -> None:
    video_url = f"https://www.youtube.com/watch?v={callback_data.youtube_video_id}"
    media = await add_media(url=video_url)
    await send_function(chat_id=query.message.chat.id, media=media)


@dp.callback_query(SelectDownloadType.filter(F.action == Action.VIDEO_DOWNLOAD))
async def handle_video_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, send_video)


@dp.callback_query(SelectDownloadType.filter(F.action == Action.AUDIO_DOWNLOAD))
async def handle_audio_download_callback(query: CallbackQuery, callback_data: SelectDownloadType) -> None:
    await handle_media_download_callback(query, callback_data, send_audio)


@dp.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.delete()
    profile = await map_profile(message.chat)
    await message.answer(f'''
    Hello {profile.first_name}! Nice to meet you, follow the instructions (/help) for working with me.
    ''')
    await save_message(profile, message)


@dp.message()
async def default_handler(message: types.Message) -> None:
    profile = await map_profile(message.chat)
    await message.reply('I do not understand you')
    await save_message(profile, message)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        asyncio.run(main())

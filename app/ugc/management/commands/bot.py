import asyncio
import logging
import os
from enum import Enum

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Chat, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from django.conf import settings
from django.core.management import BaseCommand
from pytube import YouTube

from ...models import Profile, Media
from ...service.media_service import add_media, add_media_to_profile
from ...service.message_service import save_message
from ...utils.media_utils import download_video

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def send_video(chat_id: int, media: Media) -> None:
    path = await download_video(media.url)
    try:
        caption = f'{media.title}\n\nChannel: {media.channel}\n'
        await bot.send_video(chat_id=chat_id,
                             caption=caption,
                             video=FSInputFile(path))
    except Exception as e:
        print(f"Error sending video: {e}")
    finally:
        os.remove(path)


async def send_audio(chat_id: int, media: Media) -> None:
    path = await download_video(media.url)
    try:
        await bot.send_audio(chat_id=chat_id,
                             caption=f'Channel: {media.channel}',
                             audio=FSInputFile(path))
    except Exception as e:
        print(f"Error sending video: {e}")
    finally:
        os.remove(path)


async def get_media_info_cart(media: Media) -> str:
    duration = divmod(media.duration, 60)
    return (f'{media.title}\n\n' +
            f'Channel: {media.channel}\n' +
            f'Duration: {duration[0]}:{duration[1]}\n')


async def map_profile(chat: Chat) -> Profile:
    return Profile(
        external_id=chat.id,
        username=chat.username,
        first_name=chat.first_name,
        last_name=chat.last_name,
    )


@dp.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    profile = await map_profile(message.chat)
    await message.answer(f'''
    Hello {profile.first_name}! Nice to meet you, follow the instructions (/help) for working with me.
    ''')
    await save_message(profile, message)


class Action(str, Enum):
    VIDEO_DOWNLOAD = 'video'
    AUDIO_DOWNLOAD = 'audio'


class SelectTypeCallback(CallbackData, prefix="my"):
    action: Action
    youtube_video_id: str


@dp.message(F.text.regexp(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$'))
async def youtube_url_handler(message: types.Message) -> None:
    profile = await map_profile(message.chat)
    youtube_url = message.text

    youtube_video_id = YouTube(youtube_url).video_id

    builder = InlineKeyboardBuilder()
    builder.button(
        text='Video',
        callback_data=SelectTypeCallback(action=Action.VIDEO_DOWNLOAD, youtube_video_id=youtube_video_id)
    )
    builder.button(
        text='Audio',
        callback_data=SelectTypeCallback(action=Action.AUDIO_DOWNLOAD, youtube_video_id=youtube_video_id)
    )

    media = await add_media(url=youtube_url)
    await add_media_to_profile(media=media, profile=profile)

    await bot.send_message(
        chat_id=message.chat.id,
        text=(await get_media_info_cart(media)),
        reply_markup=builder.as_markup()
    )


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectTypeCallback,
                                         send_function) -> None:
    video_url = f"https://www.youtube.com/watch?v={callback_data.youtube_video_id}"
    media = await add_media(url=video_url)
    await send_function(chat_id=query.message.chat.id, media=media)


@dp.callback_query(SelectTypeCallback.filter(F.action == Action.VIDEO_DOWNLOAD))
async def handle_video_download_callback(query: CallbackQuery, callback_data: SelectTypeCallback) -> None:
    await handle_media_download_callback(query, callback_data, send_video)


@dp.callback_query(SelectTypeCallback.filter(F.action == Action.AUDIO_DOWNLOAD))
async def handle_audio_download_callback(query: CallbackQuery, callback_data: SelectTypeCallback) -> None:
    await handle_media_download_callback(query, callback_data, send_audio)


@dp.message(F.text.regexp(r'(#+[a-zA-Z0-9(_)]{1,})'))
async def add_tags_handler(message):
    profile = await map_profile(message.chat)
    if message.reply_to_message:
        pass


@dp.message()
async def default_handler(message: types.Message) -> None:
    await message.reply('I do not understand you')


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        asyncio.run(main())

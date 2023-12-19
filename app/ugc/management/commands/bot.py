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

from .keyboards import SelectDownloadType, Action, select_download_type, pagination, Navigation, Pagination
from ...dto.media_dto import map_youtube_media
from ...dto.profile_dto import map_profile
from ...models import Media
from ...service.media_service import add_media, add_media_to_profile, get_all_media_by_profile__reverse, get_media_by_id
from ...service.message_service import save_message
from ...utils.media_utils import download_video, get_media_info_cart, download_audio

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def send_media(chat_id: int, media: Media, send_func, download_func, caption: str = '') -> None:
    telegram_file_id_attr = f'telegram_{send_func.__name__.replace("send_", "")}_file_id'
    file_type = send_func.__name__.replace("send_", "")

    telegram_file_id = getattr(media, telegram_file_id_attr, None)

    if telegram_file_id:
        await send_func(chat_id=chat_id, caption=caption, **{file_type: telegram_file_id})
    else:
        path = await download_func(media.url)
        try:
            msg = await send_func(chat_id=chat_id, caption=caption, **{file_type: FSInputFile(path)})
            setattr(media, telegram_file_id_attr, getattr(msg, file_type).file_id)
            await media.asave()
        except Exception as e:
            print(f"Error sending media: {e}")
        finally:
            await asyncio.sleep(1)
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error removing file: {e}")


async def send_video(chat_id: int, media: Media) -> None:
    await send_media(chat_id, media, bot.send_video, download_video,
                     caption=f'{media.title}\n\nChannel: {media.channel}\n')


async def send_audio(chat_id: int, media: Media) -> None:
    await send_media(chat_id, media, bot.send_audio, download_audio,
                     caption=f'Channel: {media.channel}')


@dp.message(F.text.regexp(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$'))
async def youtube_url_handler(message: types.Message) -> None:
    profile = await map_profile(message.chat)
    youtube_url = message.text

    media_dto = await map_youtube_media(youtube_url)
    media = await add_media(media_dto)
    await add_media_to_profile(media=media, profile=profile)

    await message.reply(
        text=(await get_media_info_cart(media)),
        reply_markup=select_download_type(media.id)
    )


@dp.message(Command('history'))
async def show_history(message: types.Message) -> None:
    await message.delete()
    profile = await map_profile(message.chat)
    medias = await get_all_media_by_profile__reverse(profile)

    if len(medias) == 0:
        await message.answer(text="You don't have a media history yet")
        return

    await message.answer(
        text=(await get_media_info_cart(medias[0])),
        reply_markup=pagination(medias[0].id)
    )


@dp.callback_query(Pagination.filter(F.navigation.in_([Navigation.PREV_STEP, Navigation.NEXT_STEP])))
async def pagination_history(query: CallbackQuery, callback_data: Pagination) -> None:
    profile = await map_profile(query.message.chat)
    medias = await get_all_media_by_profile__reverse(profile)

    page_num = int(callback_data.page)
    total_pages = len(medias)

    page = max(0, min(page_num - 1, total_pages - 1))

    if callback_data.navigation == Navigation.NEXT_STEP:
        page = min(page_num, total_pages - 1)

    with suppress(TelegramBadRequest):
        current_media = medias[page]
        await query.message.edit_text(
            await get_media_info_cart(current_media),
            reply_markup=pagination(current_media.id, page)
        )
    await query.answer()


async def handle_media_download_callback(query: CallbackQuery, callback_data: SelectDownloadType,
                                         send_function) -> None:
    media = await get_media_by_id(callback_data.media_id)
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

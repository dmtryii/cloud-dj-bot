import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from django.conf import settings
from django.core.management import BaseCommand

from .keyboards import (SelectDownloadType, Action, select_download_type, media_pagination, Navigation, Pagination,
                        Favorite, main_menu)
from ...dto.media_dto import map_youtube_media
from ...dto.profile_dto import map_profile
from ...models import Media
from ...service.bot_service import send_media
from ...service.media_service import add_media, add_media_to_profile, get_all_media_by_profile__reverse, \
    get_media_by_id, get_media_by_profile, get_all_favorite_media_by_profile__reverse
from ...service.message_service import save_message
from ...service.profile_service import add_profile
from ...utils.media_utils import download_video, get_media_info_cart, download_audio

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


async def send_video(chat_id: int, media: Media) -> None:
    await send_media(chat_id, media, bot.send_video, download_video,
                     caption=f'{media.title}\n\nChannel: {media.channel}\n')


async def send_audio(chat_id: int, media: Media) -> None:
    await send_media(chat_id, media, bot.send_audio, download_audio,
                     caption=f'Channel: {media.channel}')


@dp.message(F.text.regexp(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$'))
async def youtube_url_handler(message: types.Message) -> None:
    await message.delete()
    profile = await map_profile(message.chat)
    youtube_url = message.text

    media_dto = await map_youtube_media(youtube_url)
    media = await add_media(media_dto)
    await add_media_to_profile(media=media, profile=profile)

    await message.answer(
        text=(await get_media_info_cart(media)),
        reply_markup=select_download_type(media.id),
        parse_mode='HTML'
    )


@dp.message(F.text.lower().in_(['history', 'favorite']))
async def show_media(message: types.Message) -> None:
    await message.delete()
    profile = await map_profile(message.chat)

    types_mapping = {'history': get_all_media_by_profile__reverse,
                     'favorite': get_all_favorite_media_by_profile__reverse}

    media_type = message.text.lower()
    medias = await types_mapping[media_type](profile)

    if len(medias) == 0:
        await message.answer(text=f"You don't have {media_type} media yet")
        return

    answer_text = await get_media_info_cart(medias[0])

    await message.answer(
        text=answer_text,
        reply_markup=media_pagination(medias[0].id,
                                      media_type,
                                      total_pages=len(medias)),
        parse_mode='HTML'
    )


@dp.callback_query(Pagination.filter(F.navigation.in_([Navigation.PREV_STEP, Navigation.NEXT_STEP])))
async def pagination_media_callback(query: CallbackQuery, callback_data: Pagination) -> None:
    profile = await map_profile(query.message.chat)
    media_type = callback_data.types

    types_mapping = {'history': get_all_media_by_profile__reverse,
                     'favorite': get_all_favorite_media_by_profile__reverse}

    medias = await types_mapping[media_type](profile)

    page_num = int(callback_data.page)
    total_pages = len(medias)
    page = max(0, min(page_num - 1, total_pages - 1))

    if callback_data.navigation == Navigation.NEXT_STEP:
        page = min(page_num, total_pages - 1)

    with suppress(TelegramBadRequest):
        current_media = medias[page]
        await query.message.edit_text(
            text=await get_media_info_cart(current_media),
            reply_markup=media_pagination(current_media.id,
                                          media_type, page,
                                          total_pages=len(medias)),
            parse_mode='HTML'
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


@dp.callback_query(Favorite.filter(F.action == Action.MEDIA_TO_FAVORITES))
async def handle_media_favorite_callback(query: CallbackQuery, callback_data: Favorite) -> None:
    profile = await map_profile(query.message.chat)
    profile = await add_profile(profile)
    media = await get_media_by_id(callback_data.media_id)

    media_profile = await get_media_by_profile(profile, media)
    if media_profile.is_favorite:
        media_profile.is_favorite = False
        await query.answer("Removed from favorites")
    else:
        media_profile.is_favorite = True
        await query.answer("Added to favorites")
    await media_profile.asave()


@dp.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.delete()
    profile = await map_profile(message.chat)
    await message.answer(f'''
    Hello {profile.first_name}! Nice to meet you, follow the instructions (/help) for working with me.
    ''', reply_markup=main_menu)


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

from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from .. import data_fetcher
from ..keyboards.inline import Pagination, Navigation, media_pagination
from ..messages import templates

router = Router()


async def _get_media_count(chat_id: str, media_type: str) -> int:
    if media_type == 'history':
        response_count = await data_fetcher.get_profile_history_count(chat_id)
    elif media_type == 'favorite':
        response_count = await data_fetcher.get_profile_favorite_count(chat_id)
    else:
        return 0

    return response_count['count']


async def _get_media(chat_id: str, media_type: str, page: int) -> dict:
    if media_type == 'history':
        return await data_fetcher.get_media_for_profile_on_counter(chat_id, page)
    elif media_type == 'favorite':
        return await data_fetcher.get_media_favorite_for_profile_on_counter(chat_id, page)
    return {}


@router.callback_query(Pagination.filter(F.navigation.in_([Navigation.PREV_STEP, Navigation.NEXT_STEP,
                                                           Navigation.START, Navigation.END])))
async def pagination_media_callback(query: CallbackQuery, callback_data: Pagination) -> None:
    chat_id = str(query.message.chat.id)
    media_type = callback_data.types

    total_pages = await _get_media_count(chat_id, media_type)

    if total_pages == 0:
        await query.answer(f'You don\'t have any {media_type}s yet')
        return

    page_num = int(callback_data.page)

    page = max(0, min(page_num, total_pages - 1))

    navigation_mapping = {
        Navigation.NEXT_STEP: min(page_num, total_pages - 1),
        Navigation.START: 0,
        Navigation.END: total_pages - 1
    }

    page = navigation_mapping.get(callback_data.navigation, page)

    with suppress(TelegramBadRequest):
        current_media = await _get_media(chat_id, media_type, page)

        answer_text = templates.get_media_info_cart(
            current_media['title'],
            current_media['url'],
            current_media['channel'],
            current_media['duration'],
            title=media_type.upper()
        )

        await query.message.edit_text(
            text=answer_text,
            reply_markup=media_pagination(current_media['media_id'],
                                          media_type,
                                          page=page,
                                          total_pages=total_pages)
        )
    await query.answer()

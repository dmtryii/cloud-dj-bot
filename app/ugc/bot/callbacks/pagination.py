from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from ..keyboards.inline import Pagination, Navigation, media_pagination
from ..messages.templates import get_media_info_cart
from ...dto.profile_dto import map_profile
from ...service.media_service import get_all_media_by_profile__reverse, get_all_favorite_media_by_profile__reverse

router = Router()


@router.callback_query(Pagination.filter(F.navigation.in_([Navigation.PREV_STEP, Navigation.NEXT_STEP])))
async def pagination_media_callback(query: CallbackQuery, callback_data: Pagination) -> None:
    profile = await map_profile(query.message.chat)
    media_type = callback_data.types

    types_mapping = {'history': get_all_media_by_profile__reverse,
                     'favorite': get_all_favorite_media_by_profile__reverse}

    medias = await types_mapping[media_type](profile)

    page_num = int(callback_data.page)
    total_pages = len(medias)
    page = max(0, min(page_num, total_pages - 1))

    if callback_data.navigation == Navigation.NEXT_STEP:
        page = min(page_num, total_pages - 1)

    with suppress(TelegramBadRequest):
        current_media = medias[page]
        await query.message.edit_text(
            text=get_media_info_cart(current_media, media_type.upper()),
            reply_markup=media_pagination(current_media.id,
                                          media_type,
                                          page=page,
                                          total_pages=len(medias)),
            parse_mode='HTML'
        )
    await query.answer()

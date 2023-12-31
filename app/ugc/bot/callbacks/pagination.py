from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from ..keyboards.inline import Pagination, Navigation, media_pagination
from ..messages.templates import get_media_info_cart
from ...mappers.profile_mapper import ProfileMapper
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService

router = Router()


@router.callback_query(Pagination.filter(F.navigation.in_([Navigation.PREV_STEP, Navigation.NEXT_STEP])))
async def pagination_media_callback(query: CallbackQuery, callback_data: Pagination) -> None:
    profile_dto = ProfileMapper(query.message.chat).map()
    profile_service = ProfileService(profile_dto)

    media_service = MediaService(media=None, profile_service=profile_service)

    media_type = callback_data.types

    if media_type == 'history':
        medias = await media_service.get_all_by_profile__reverse()
    elif media_type == 'favorite':
        medias = await media_service.get_all_favorite_by_profile__reverse()
    else:
        return

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

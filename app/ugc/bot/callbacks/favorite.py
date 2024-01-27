from aiogram import Router, F
from aiogram.types import CallbackQuery

from .. import data_fetcher
from ..keyboards.inline import Favorite, Action

router = Router()


@router.callback_query(Favorite.filter(F.action == Action.MEDIA_TO_FAVORITES))
async def handle_media_favorite_callback(query: CallbackQuery, callback_data: Favorite) -> None:

    chat_id = str(query.message.chat.id)
    media_id = callback_data.media_id

    media_profile = await data_fetcher.swap_media_favorites(chat_id, media_id)

    if media_profile['is_favorite']:
        await query.answer("Added to favorites")
    else:
        await query.answer("Removed from favorites")

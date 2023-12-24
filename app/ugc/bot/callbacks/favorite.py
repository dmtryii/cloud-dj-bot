from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.inline import Favorite, Action
from ...dto.profile_dto import map_profile
from ...service.media_service import get_media_by_id, get_media_by_profile
from ...service.profile_service import get_or_create_profile

router = Router()


@router.callback_query(Favorite.filter(F.action == Action.MEDIA_TO_FAVORITES))
async def handle_media_favorite_callback(query: CallbackQuery, callback_data: Favorite) -> None:
    profile = await map_profile(query.message.chat)
    profile = await get_or_create_profile(profile)
    media = await get_media_by_id(callback_data.media_id)

    media_profile = await get_media_by_profile(profile, media)
    if media_profile.is_favorite:
        media_profile.is_favorite = False
        await query.answer("Removed from favorites")
    else:
        media_profile.is_favorite = True
        await query.answer("Added to favorites")
    await media_profile.asave()

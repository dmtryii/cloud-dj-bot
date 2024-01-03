from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.inline import Favorite, Action
from ...mappers.profile_mapper import ProfileMapper
from ...service.media_service import MediaService
from ...service.profile_service import ProfileService

router = Router()


@router.callback_query(Favorite.filter(F.action == Action.MEDIA_TO_FAVORITES))
async def handle_media_favorite_callback(query: CallbackQuery, callback_data: Favorite) -> None:
    profile_dto = ProfileMapper(query.message.chat).map()
    profile_service = ProfileService(profile_dto)

    media = await MediaService.get_by_id(callback_data.media_id, profile_service)
    media_service = await MediaService.get_instance_by_id(media.id, profile_service)

    media_profile = await media_service.get_by_profile()

    if media_profile.is_favorite:
        media_profile.is_favorite = False
        await query.answer("Removed from favorites")
    else:
        media_profile.is_favorite = True
        await query.answer("Added to favorites")
    await media_profile.asave()

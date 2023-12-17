from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Action(str, Enum):
    VIDEO_DOWNLOAD = 'video'
    AUDIO_DOWNLOAD = 'audio'


class SelectDownloadTypeCallback(CallbackData, prefix="my"):
    action: Action
    youtube_video_id: str


async def build_select_download_keyboard(youtube_video_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Video',
        callback_data=SelectDownloadTypeCallback(action=Action.VIDEO_DOWNLOAD, youtube_video_id=youtube_video_id)
    )
    builder.button(
        text='Audio',
        callback_data=SelectDownloadTypeCallback(action=Action.AUDIO_DOWNLOAD, youtube_video_id=youtube_video_id)
    )
    return builder.as_markup()

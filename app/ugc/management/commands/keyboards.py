from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Action(str, Enum):
    VIDEO_DOWNLOAD = 'video'
    AUDIO_DOWNLOAD = 'audio'


class Navigation(str, Enum):
    PREV_STEP = 'video'
    NEXT_STEP = 'audio'


class SelectDownloadType(CallbackData, prefix="dow"):
    action: Action
    youtube_video_id: str


class Pagination(CallbackData, prefix="pag"):
    navigation: Navigation
    page: int


def select_download_type(youtube_video_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Video',
                             callback_data=SelectDownloadType(action=Action.VIDEO_DOWNLOAD,
                                                              youtube_video_id=youtube_video_id).pack()),
        InlineKeyboardButton(text='Audio',
                             callback_data=SelectDownloadType(action=Action.AUDIO_DOWNLOAD,
                                                              youtube_video_id=youtube_video_id).pack())
    )
    return builder.as_markup()


def pagination(youtube_video_id: str, page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='<',
                             callback_data=Pagination(navigation=Navigation.PREV_STEP, page=page - 1).pack()),
        InlineKeyboardButton(text='>',
                             callback_data=Pagination(navigation=Navigation.NEXT_STEP, page=page + 1).pack())
    )
    builder.row(
        InlineKeyboardButton(text='Video',
                             callback_data=SelectDownloadType(action=Action.VIDEO_DOWNLOAD,
                                                              youtube_video_id=youtube_video_id).pack()),
        InlineKeyboardButton(text='Audio',
                             callback_data=SelectDownloadType(action=Action.AUDIO_DOWNLOAD,
                                                              youtube_video_id=youtube_video_id).pack())
    )
    return builder.as_markup()

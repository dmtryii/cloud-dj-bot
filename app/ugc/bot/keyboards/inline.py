from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Action(str, Enum):
    VIDEO_DOWNLOAD = 'video'
    AUDIO_DOWNLOAD = 'audio'
    MEDIA_TO_FAVORITES = 'favorite'


class Navigation(str, Enum):
    START = 'start'
    PREV_STEP = 'prev'
    NEXT_STEP = 'next'
    END = 'end'


class SelectDownloadType(CallbackData, prefix="dow"):
    action: Action
    media_id: str


class Pagination(CallbackData, prefix="pag"):
    navigation: Navigation
    page: int
    types: str


class Favorite(CallbackData, prefix="fav"):
    action: Action
    media_id: str


def select_download_type(media_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Video',
                             callback_data=SelectDownloadType(action=Action.VIDEO_DOWNLOAD,
                                                              media_id=media_id).pack()),
        InlineKeyboardButton(text='Audio',
                             callback_data=SelectDownloadType(action=Action.AUDIO_DOWNLOAD,
                                                              media_id=media_id).pack())
    )
    return builder.as_markup()


def media_pagination(media_id: str, types: str,
                     page: int = 0, total_pages: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='<<',
                             callback_data=Pagination(navigation=Navigation.START,
                                                      types=types,
                                                      page=page).pack()),
        InlineKeyboardButton(text='<',
                             callback_data=Pagination(navigation=Navigation.PREV_STEP,
                                                      types=types,
                                                      page=page - 1).pack()),

        InlineKeyboardButton(text=f'{page + 1}/{total_pages}',
                             callback_data=f'{page + 1}/{total_pages}'),

        InlineKeyboardButton(text='>',
                             callback_data=Pagination(navigation=Navigation.NEXT_STEP,
                                                      types=types,
                                                      page=page + 1).pack()),
        InlineKeyboardButton(text='>>',
                             callback_data=Pagination(navigation=Navigation.END,
                                                      types=types,
                                                      page=page).pack())
    )
    builder.row(
        InlineKeyboardButton(text='Video',
                             callback_data=SelectDownloadType(action=Action.VIDEO_DOWNLOAD,
                                                              media_id=media_id).pack()),
        InlineKeyboardButton(text='Audio',
                             callback_data=SelectDownloadType(action=Action.AUDIO_DOWNLOAD,
                                                              media_id=media_id).pack())
    )
    builder.row(
        InlineKeyboardButton(text='Favorite',
                             callback_data=Favorite(action=Action.MEDIA_TO_FAVORITES,
                                                    media_id=media_id).pack())
    )
    return builder.as_markup()

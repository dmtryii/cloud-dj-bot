from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="History")
        ],
[
            KeyboardButton(text="Favorite")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Choose an action from the menu'
)


class Action(str, Enum):
    VIDEO_DOWNLOAD = 'video'
    AUDIO_DOWNLOAD = 'audio'
    MEDIA_TO_FAVORITES = 'favorite'


class Navigation(str, Enum):
    PREV_STEP = 'video'
    NEXT_STEP = 'audio'


class SelectDownloadType(CallbackData, prefix="dow"):
    action: Action
    media_id: int


class Pagination(CallbackData, prefix="pag"):
    navigation: Navigation
    page: int
    types: str


class Favorite(CallbackData, prefix="fav"):
    action: Action
    media_id: int


def select_download_type(media_id: int) -> InlineKeyboardMarkup:
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


def media_pagination(media_id: int, types: str, page: int = 0, total_pages: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='<',
                             callback_data=Pagination(navigation=Navigation.PREV_STEP,
                                                      types=types,
                                                      page=page - 1).pack()),
        InlineKeyboardButton(text=f'{page + 1}/{total_pages}',
                             callback_data=f'{page + 1}/{total_pages}'),

        InlineKeyboardButton(text='>',
                             callback_data=Pagination(navigation=Navigation.NEXT_STEP,
                                                      types=types,
                                                      page=page + 1).pack())
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

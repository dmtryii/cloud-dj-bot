import os

import telebot
from django.conf import settings
from django.core.management import BaseCommand
from telebot import types
from telebot.types import Chat

from ...models import Profile, Media
from ...service.hashtag_service import add_all_tags_to_media
from ...service.message_service import save_message
from ...service.profile_service import create_or_update_current_action, get_current_action
from ...utils.media_utils import download_video, convert_video_to_audio

bot = telebot.TeleBot(settings.TOKEN)

VIDEO_CALLBACK = 'video'
AUDIO_CALLBACK = 'audio'


def send_video(chat_id: int, path: str) -> None:
    with open(path, 'rb') as video_file:
        bot.send_video(chat_id=chat_id, video=video_file, supports_streaming=True)
    os.remove(path)


def send_audio(chat_id: int, path: str) -> None:
    with open(path, 'rb') as audio_file:
        bot.send_audio(chat_id=chat_id, audio=audio_file)
    os.remove(path)
    os.remove(path.replace('.mp3', '.mp4'))


def get_media_info(media: Media) -> str:
    duration = divmod(media.duration, 60)
    return (f'Title: {media.title}\n' +
            f'Channel: {media.channel}\n' +
            f'Duration: {duration[0]}:{duration[1]}\n')


def map_profile(chat: Chat) -> Profile:
    return Profile(
        external_id=chat.id,
        username=chat.username,
        first_name=chat.first_name,
        last_name=chat.last_name,
    )


@bot.message_handler(regexp=r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$')
def youtube_url_handler(message):
    profile = map_profile(message.chat)
    youtube_url = message.text

    inline_keyboard = types.InlineKeyboardMarkup()

    item1 = types.InlineKeyboardButton('Video', callback_data=VIDEO_CALLBACK)
    item2 = types.InlineKeyboardButton('Audio', callback_data=AUDIO_CALLBACK)

    inline_keyboard.row(item1, item2)

    media = create_or_update_current_action(profile, youtube_url)

    bot.send_message(
        message.chat.id,
        get_media_info(media),
        reply_markup=inline_keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_media_callback(call):
    chat = call.message.chat
    profile = map_profile(chat)

    current_action = get_current_action(profile)
    url = current_action.media.url

    if call.data == VIDEO_CALLBACK:
        path = download_video(url)
        send_video(chat.id, path)
    elif call.data == AUDIO_CALLBACK:
        path = convert_video_to_audio(url)
        send_audio(chat.id, path)


@bot.message_handler(regexp=r'(#+[a-zA-Z0-9(_)]{1,})')
def playlist_tags_handler(message):
    profile = map_profile(message.chat)
    if message.reply_to_message:
        text = message.text
        add_all_tags_to_media(text, profile)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    profile = map_profile(message.chat)
    bot.reply_to(message, f'''
            Hello {profile.first_name}! Nice to meet you, follow the instructions for working with me.
            ''')
    save_message(profile, message.text)


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        bot.infinity_polling()

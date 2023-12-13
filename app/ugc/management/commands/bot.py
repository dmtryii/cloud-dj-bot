import os

import telebot
from django.conf import settings
from django.core.management import BaseCommand
from telebot import types

from ...service.hashtag_service import add_tags_to_media
from ...service.message_service import save_message
from ...service.profile_service import create_or_update_current_action, get_current_action
from ...utils.media_utils import download_video, convert_video_to_audio

bot = telebot.TeleBot(settings.TOKEN)

VIDEO_CALLBACK = 'video'
AUDIO_CALLBACK = 'audio'


def send_video(chat_id, path):
    with open(path, 'rb') as video_file:
        bot.send_video(chat_id=chat_id, video=video_file, supports_streaming=True)
    os.remove(path)


def send_audio(chat_id, path):
    with open(path, 'rb') as audio_file:
        bot.send_audio(chat_id=chat_id, audio=audio_file)
    os.remove(path)
    os.remove(path.replace('.mp3', '.mp4'))


def get_media_info(media):
    return (f'Title: {media.title}\n' +
            f'Channel: {media.channel}\n' +
            f'Duration: {divmod(media.duration, 60)}\n')


@bot.message_handler(regexp=r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$')
def youtube_url_handler(message):
    url = message.text
    youtube_url = url.split(' ')[0]

    inline_keyboard = types.InlineKeyboardMarkup()

    item1 = types.InlineKeyboardButton('Video', callback_data=VIDEO_CALLBACK)
    item2 = types.InlineKeyboardButton('Audio', callback_data=AUDIO_CALLBACK)

    inline_keyboard.row(item1, item2)

    profile, media = create_or_update_current_action(message.chat, youtube_url)

    bot.send_message(
        message.chat.id,
        get_media_info(media),
        reply_markup=inline_keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_media_callback(call):

    chat = call.message.chat

    current_action = get_current_action(chat)

    if call.data == VIDEO_CALLBACK:
        url = current_action.media.url
        path = download_video(url, chat)
        send_video(chat.id, path)
    elif call.data == AUDIO_CALLBACK:
        url = current_action.media.url
        path = download_video(url, chat)
        audio_path = convert_video_to_audio(path)
        send_audio(chat.id, audio_path)


@bot.message_handler(regexp=r'(#+[a-zA-Z0-9(_)]{1,})')
def playlist_tags_handler(message):
    if message.reply_to_message:
        text = message.text
        add_tags_to_media(text, message.chat)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    chat = message.chat
    bot.reply_to(message, f'''
            Hello {chat.first_name}! Nice to meet you, follow the instructions for working with me.
            ''')
    save_message(message)


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        bot.infinity_polling()

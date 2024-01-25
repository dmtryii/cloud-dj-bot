from aiogram.types import CallbackQuery, FSInputFile

from .. import main_bot
from ..exceptions import bot_exception_handler
from ..messages import templates
from ...bot import data_fetcher


class BotMediaService:
    VIDEO = 'video'
    AUDIO = 'audio'

    def __init__(self, query: CallbackQuery, media_type: str, download_social_network):
        self._query = query
        self._media_type = media_type
        self._download_social_network = download_social_network

    async def send_video(self, media_id: str) -> None:
        media = await data_fetcher.get_media(media_id)
        caption = templates.media_caption(media['title'], media['channel'])

        telegram_file_id = media['telegram_video_file_id']

        if telegram_file_id:
            msg = await self._query.message.answer_video(video=telegram_file_id, caption=caption)
            await self._swap_media_in_chat(msg.message_id, media_id)
        else:
            await self._handle_new_media_file(media_id, caption)

    async def send_audio(self, media_id: str) -> None:
        media = await data_fetcher.get_media(media_id)
        caption = templates.media_caption(media['title'], media['channel'])
        telegram_file_id = media['telegram_audio_file_id']

        if telegram_file_id:
            msg = await self._query.message.answer_audio(audio=telegram_file_id, caption=caption)
            await self._swap_media_in_chat(msg.message_id, media_id)
        else:
            await self._handle_new_media_file(media_id, caption)

    async def _handle_new_media_file(self, media_id: str, caption: str = '') -> None:

        chat_id = str(self._query.message.chat.id)
        downloading_alert = await self._query.message.answer('Downloading, please wait...')
        await main_bot.swap_action(chat_id, str(downloading_alert.message_id))

        download = await self._download_social_network(chat_id, media_id, self._media_type)

        if 'error_message' in download:
            msg_text = await bot_exception_handler.role_restriction(chat_id)
            msg = await main_bot.bot.send_message(chat_id=chat_id, text=msg_text, parse_mode='HTML')
            await main_bot.swap_action(chat_id, msg.message_id)
            return

        output = download['output']
        await self._send_media_message(media_id, output, caption)
        await data_fetcher.delete_download(output)

    async def _send_media_message(self, media_id: str, path: str, caption: str = '') -> None:
        if self._media_type == self.VIDEO:
            msg = await self._query.message.answer_video(video=FSInputFile(path), caption=caption)
            await data_fetcher.set_telegram_video_id(media_id, msg.video.file_id)
        else:
            msg = await self._query.message.answer_audio(audio=FSInputFile(path), caption=caption)
            await data_fetcher.set_telegram_audio_id(media_id, msg.audio.file_id)

        await self._swap_media_in_chat(msg.message_id, media_id)

    async def _swap_media_in_chat(self, message_id, media_id: str) -> None:
        chat_id = str(self._query.message.chat.id)
        media_download = await data_fetcher.get_download_media(chat_id, media_id)

        if 'message_id' in media_download:
            await main_bot.delete_message(chat_id, media_download['message_id'])

        await data_fetcher.add_download_media(message_id, chat_id, media_id)

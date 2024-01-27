from ...bot import data_fetcher


class BotManagementService:
    @staticmethod
    async def swap_action(chat_id: str, message_id: str) -> None:
        current_action = await data_fetcher.get_current_action(chat_id)

        if current_action:
            await BotManagementService.delete_message(chat_id, current_action['message_id'])

        await data_fetcher.set_current_action(chat_id, message_id)

    @staticmethod
    async def delete_message(chat_id: str, message_id: str) -> None:
        from ..main_bot import bot
        try:
            await bot.delete_message(chat_id=chat_id, message_id=int(message_id))
        except Exception as e:
            print(f"Error deleting message: {e}")

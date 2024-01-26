from ...bot import data_fetcher
from ...bot.messages import templates


async def role_restriction(profile_id: str) -> str:
    role = await data_fetcher.get_role(profile_id)
    return templates.role_restriction(role['allowed_media_length'], role['delay_between_downloads'])

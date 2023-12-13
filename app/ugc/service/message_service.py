from .profile_service import create_or_get_profile
from ..models import Message


def save_message(message) -> None:
    chat = message.chat
    profile = create_or_get_profile(chat)
    Message(profile=profile, text=message.text).save()

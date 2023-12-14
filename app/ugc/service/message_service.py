from .profile_service import create_or_get_profile
from ..models import Message, Profile


def save_message(profile: Profile, text_message: str) -> None:
    profile = create_or_get_profile(profile)
    Message(profile=profile, text=text_message).save()

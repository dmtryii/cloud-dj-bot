from instaloader import instaloader

from django.conf import settings


class InstagramLoader:
    _inst_loader = None

    def __new__(cls, *args, **kwargs):
        if not cls._inst_loader:
            cls._inst_loader = super().__new__(cls)
            cls._inst_loader.inst_loader = instaloader.Instaloader()
            cls._inst_loader.inst_loader.login(user=settings.INST_USERNAME, passwd=settings.INST_PASSWORD)
        return cls._inst_loader

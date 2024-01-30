from django.core.management import BaseCommand

from ...bot.main_bot import main


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        main()

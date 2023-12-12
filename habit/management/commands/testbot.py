from django.conf import settings
from django.core.management import BaseCommand

from habit.services import MyBot


class Command(BaseCommand):
    """
    Команда для проверки работы бота
    """

    def handle(self, *args, **options):
        my_bot = MyBot()
        my_bot.send_message('Hi, Egor!', settings.CHAT_ID_TG_TEST)

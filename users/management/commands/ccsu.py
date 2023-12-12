from django.conf import settings
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    # Создание суперюзера из-за того, что мы переопределили создание юзера. Мы не можно создать его командой createsuperuser

    def handle(self, *args, **options):
        User.objects.create_superuser(
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD,
            chat_id_tg=settings.CHAT_ID_TG_TEST
        )
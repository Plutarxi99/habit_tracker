from django.core.management import BaseCommand

# from education.models import *
from django.db import connection


class Command(BaseCommand):
    help = 'Удаление всех пользователей и обнуление автоинкремента. Только с пустой базой или без форейна кейна'

    def handle(self, *args, **options):
        list_table = [
            'public.users_user',
        ]
        # Подключается к базе данных и обнуляет автоинкремент и удаляет наполнение таблиц
        with connection.cursor() as cursor:
            for list_table_item in list_table:
                cursor.execute(f'DELETE FROM {list_table_item};')
                cursor.execute(f'TRUNCATE TABLE {list_table_item} RESTART IDENTITY CASCADE;')

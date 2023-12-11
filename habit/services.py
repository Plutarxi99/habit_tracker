import requests
from django.conf import settings
import datetime
import time
#
# from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
#
# from users.models import User


def get_second(t: datetime.time) -> int:
    """
    Переводит формат из datetime.time в int. Выраженных в секундах
    @rtype: datetime.time
    """
    str_time = t.strftime('%H:%M:%S')
    x = time.strptime(str_time.split(',')[0], '%H:%M:%S')
    sec = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return int(sec)


class MixinListSerializer:
    """
    Миксин для комфортного отображения данных для пользователя
    """
    def to_representation(self, instance):
        representation = super(MixinListSerializer, self).to_representation(instance)
        representation['time_to_do'] = instance.time_to_do.strftime('%d.%m.%Y %H:%M:%S')
        representation['time_run'] = get_second(instance.time_run)
        return representation


class MyBot:
    """
    Класс для создания сообщения и отправки сообщений
    """
    URL = 'https://api.telegram.org/bot'
    TOKEN = settings.TELEGRAM_TOKEN

    def __init__(self, text, chat_id):
        self.text = text
        self.chat_id = chat_id

    def send_message(self):
        """
        Отправка сообщений пользователю
        """
        requests.post(
            url=f'{self.URL}{self.TOKEN}/sendMessage',
            data={
                'chat_id': self.chat_id,
                'text': self.text
            }
        )

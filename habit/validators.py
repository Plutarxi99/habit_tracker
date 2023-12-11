# import re
import datetime

from rest_framework.exceptions import ValidationError

from habit.models import Habit


class TimeRunValidator:
    """
    Валидатор для проверки поля time_run, что его значение было не больше 120 секунд
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """
        Метод класс для его вызова
        Валидирует, чтобы ссылка вела только на внешний ресурс с доменом youtube.com
        """
        limit_time = datetime.time(minute=2)
        time_run: datetime.time | None = dict(value).get(self.field)  # получение заполняемой строки
        compare_time: bool | None = limit_time > time_run
        if not compare_time:
            raise ValidationError(
                'Значение выполняемой задачи, должно быть меньше 120 секунд или 2 минут'
            )


class IsPrettyValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки related и award
    """

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        """
        OrderedDict([('is_pretty', False), ('award', 'скушать яблоко'), ('is_public', False), ('location', 'спортзал'),
        ('action_to_do', 'ходить на беговой дорожки'), ('time_to_do', datetime.datetime(2023, 11, 16, 21, 36, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
        ('time_run', datetime.time(0, 11)), ('period', 'day'), ('user', <User: admin@plut.arx>)])
        """
        is_pretty = dict(obj).get('is_pretty')
        award = dict(obj).get('award')
        related = dict(obj).get('related')
        if is_pretty:
            if award or related:
                raise ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки'
                )


class RelatedAwardValidator:
    """
    Валидатор для исключений одновременного выбора полей related и is_pretty
    """

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        """
        """
        related = dict(obj).get('related')
        is_pretty = dict(obj).get('is_pretty')
        if is_pretty and related:
            raise ValidationError(
                'Исключите одновременный выбор связанной привычки и указания вознаграждения.'
            )


class RelatedValidator:
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        """
        """
        related = dict(obj).get('related')
        if related:
            rel_check = Habit.objects.get(pk=related.pk).is_pretty
            if not rel_check:
                raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки.'
                )

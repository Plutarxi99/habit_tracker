# import re
import datetime

from rest_framework.exceptions import ValidationError

from habit.models import Habit


class TimeRunValidator:
    """
    Валидатор для проверки поля time_run, что его значение было не больше 120 секунд
    """

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        """
        Метод класс для его вызова
        Валидирует, чтобы ссылка вела только на внешний ресурс с доменом youtube.com
        """
        limit_time = datetime.time(minute=2)
        time_run: datetime.time | None = dict(obj).get('time_run')  # получение заполняемой строки
        if time_run is not None:
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
        is_pretty: bool | None = dict(obj).get('is_pretty')
        award: str | None = dict(obj).get('award')
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
        is_pretty: bool | None = dict(obj).get('is_pretty')
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


class EveryRunValidator:
    """Ограничение на выполнение привычки, если привычка выполняется реже 1 раза в неделю"""

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        every_run: int | None = dict(obj).get('every_run')
        period: str | None = dict(obj).get('period')
        if every_run or period:
            if Habit.MINUTES == period and 10080 < every_run:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
                )
            elif Habit.HOURS == period and 168 < every_run:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
                )
            elif Habit.DAYS == period and 7 < every_run:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
                )


class EveryRunValidatorUpdate:
    """Ограничение на выполнение привычки, если привычка выполняется реже 1 раза в неделю"""

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        every_run: int | None = dict(obj).get('every_run')
        period: str | None = dict(obj).get('period')
        if every_run and period:
            if Habit.MINUTES == period and 10080 < every_run:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
                )
            elif Habit.HOURS == period and 168 < every_run:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
                )
            elif Habit.DAYS == period and 7 < every_run:
                raise ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
                )
        elif every_run is None:
            if period:
                raise ValidationError(
                    'Для обновления рассылки укажите оба поля: every_run и period'
                )
        elif period is None:
            if every_run:
                raise ValidationError(
                    'Для обновления рассылки укажите оба поля: every_run и period'
                )

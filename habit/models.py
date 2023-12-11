from django.conf import settings
from django.db import models


class Habit(models.Model):
    HOURS = 'hours'
    DAYS = 'days'
    PERIOD = [
        ('hours', 'hours'),
        ('days', 'days'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user',
                             verbose_name='пользователь')
    related = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='связанная привычка',
                                **settings.NULLABLE)
    is_pretty = models.BooleanField(verbose_name='приятная привычка')
    award = models.CharField(max_length=300, verbose_name='вознаграждение', **settings.NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    location = models.CharField(max_length=300, verbose_name='место выполнения привычки')
    action_to_do = models.CharField(max_length=300, verbose_name='действия выполнения привычки')
    time_to_do = models.DateTimeField(verbose_name='время, когда необходимо выполнять привычку')
    time_run = models.TimeField(default=0, verbose_name='время на выполнение')
    period = models.CharField(choices=PERIOD, default=DAYS, verbose_name='периодичность')

    class Meta:
        verbose_name = 'условия привычки'
        verbose_name_plural = 'условия привычек'

    def __str__(self):
        return self.location

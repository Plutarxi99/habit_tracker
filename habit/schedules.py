import json
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule


def set_time_notif_tg(pk_habit, start_time, period, text, chat_id_tg, every_run, is_active_notif):
    """
    Вспомагательная функция для установки переодической задач для отправки уведомлений
    @param is_active_notif: присылать ли уведомление по привычке
    @param every_run: запуск каждый указанный промежуток
    @param pk_habit: номер привычки
    @param start_time: начало времени выполнения привычки
    @param period: как часто будет отправка уведомлений
    @param text: какой текст будет в сообщении
    @param chat_id_tg: подтягивается от пользователя, который при регистрировании указывал его
    @return:
    """
    #  Если есть уже эта задача, то не выполнеяется
    if not PeriodicTask.objects.filter(name=f'Привычка № {pk_habit}').exists():
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=every_run,
            period=period,
        )
        task = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name=f'Привычка № {pk_habit}',
            task="habit.tasks.run_send_notif_telegram",
            start_time=start_time,
            kwargs=json.dumps(
                {
                    'text': text,
                    'chat_id_tg': chat_id_tg,
                }
            ),
            enabled=is_active_notif
        )
        return task
    # Для обновления задачи при изменении входных данных
    else:
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=every_run,
            period=period,
        )
        task = PeriodicTask.objects.filter(
            name=f'Привычка № {pk_habit}'
        )
        task.update(
            interval=schedule,
            start_time=start_time,
            kwargs=json.dumps(
                {
                    'text': text,
                    'chat_id_tg': chat_id_tg,
                }
            ),
            enabled=is_active_notif
        )
        return task

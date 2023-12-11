from celery import shared_task

from habit.models import Habit
from habit.schedules import set_time_notif_tg
from habit.services import MyBot
from users.models import User


@shared_task
def set_send_notif_telegram(pk_habit):
    """
    Принимает индефикатор созданного или обновленной привычки и
    отдаёт в создание переодической задачи
    @param pk_habit: индефикатор привычки
    @return:
    """
    habit = tuple(Habit.objects.filter(pk=pk_habit).values())[0]
    user_pk = habit['user_id']
    chat_id_tg = User.objects.get(pk=user_pk).chat_id_tg
    start_time = habit['time_to_do']
    time_run = habit['time_run']
    action_to_do = habit['action_to_do']
    location = habit['location']
    period = habit['period']
    # award = habit['award']
    # is_pretty = habit['is_pretty']
    text = f"Я буду {action_to_do} в {time_run} в {location}"
    set_time_notif_tg(chat_id_tg=chat_id_tg, start_time=start_time, text=text, period=period, pk_habit=habit['id'])


@shared_task(bind=True)
def run_send_notif_telegram(self, text, chat_id_tg):
    """
    Отправка сообщений в указанный чат и привычкой, которая указана
    @param self: ???
    @param text: Текст сообщения
    @param chat_id_tg: куда отправится сообщение
    @return:
    """
    bot = MyBot(text=text, chat_id=chat_id_tg)
    bot.send_message()

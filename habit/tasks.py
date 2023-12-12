from celery import shared_task

from habit.models import Habit
from habit.schedules import set_time_notif_tg
from habit.services import MyBot, get_second
from users.models import User


@shared_task
def set_send_notif_telegram(pk_habit: int) -> None:
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
    t_r = habit['time_run']
    time_run = get_second(t_r)
    action_to_do = habit['action_to_do']
    location = habit['location']
    period = habit['period']
    every_run = habit['every_run']
    award = habit['award']
    is_active_notif = habit['is_active_notif']
    # is_pretty = habit['is_pretty']
    text = f"Я буду {action_to_do}{award} в {start_time.strftime('%d.%m.%Y %H:%M:%S')} в течении {time_run} в {location}"
    set_time_notif_tg(chat_id_tg=chat_id_tg, start_time=start_time, text=text, period=period, pk_habit=habit['id'],
                      every_run=every_run, is_active_notif=is_active_notif)


@shared_task(bind=True)
def run_send_notif_telegram(self, text: str, chat_id_tg: str) -> None:
    """
    Отправка сообщений в указанный чат и привычкой, которая указана
    @param self: ???
    @param text: Текст сообщения
    @param chat_id_tg: куда отправится сообщение
    @return:
    """
    bot = MyBot(text=text, chat_id=chat_id_tg)
    bot.send_message()

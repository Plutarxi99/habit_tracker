from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.permissions import IsUserCreator, IsPublicHabit
from habit.piganators import HabitPaginator
from habit.serializers import HabitSerializer, HabitCreateSerializer, PublicHabitListSerializer, MyHabitListSerializer, \
    HabitUpdateSerializer

from habit.tasks import set_send_notif_telegram


class HabitCreateAPIView(CreateAPIView):
    """
    Создание привычки
    """
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        set_send_notif_telegram.delay(
            pk_habit=serializer.data['id']
        )  # Занесение переодичской задачи на отправку уведомлений


class MyHabitListAPIView(ListAPIView):
    """
    Отображение списка привычек пользователя созданых им, который авторизован в приложении
    """
    queryset = Habit.objects.all()
    serializer_class = MyHabitListSerializer
    pagination_class = HabitPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_public', 'is_pretty']
    ordering_fields = ['time_to_do']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Привычки пользователя созданных им
        """
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user.pk)


class PublicHabitListAPIView(ListAPIView):
    """
    Отображение списка опубликованных привычек в приложении
    """
    queryset = Habit.objects.all()
    serializer_class = PublicHabitListSerializer
    pagination_class = HabitPaginator
    # permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user', 'is_pretty']
    ordering_fields = ['time_to_do']

    def get_queryset(self):
        """
        Привычки пользователя
        """
        queryset = super().get_queryset()
        return queryset.filter(is_public=True)


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Отображение одной привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsPublicHabit]


class HabitUpdateAPIView(UpdateAPIView):
    """
    Обновление привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitUpdateSerializer
    permission_classes = [IsAuthenticated, IsUserCreator]

    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = self.get_object()
        # Занесение переодичской задачи на отправку уведомлений
        set_send_notif_telegram.delay(pk_habit=instance.pk)


class HabitDestroyAPIView(DestroyAPIView):
    """
    Удаление привычки
    """
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsUserCreator]

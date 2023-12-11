from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.permissions import IsUserCreator, IsPublicHabit
from habit.piganators import HabitPaginator
from habit.serializers import HabitSerializer, HabitCreateSerializer, PublicHabitListSerializer, MyHabitListSerializer
from rest_framework.response import Response
from rest_framework import status

from habit.tasks import set_send_notif_telegram


class HabitCreateAPIView(CreateAPIView):
    """
    Создание привычки
    """
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Для создания привычки"""
        dict_req = self.request.data
        dict_req['user'] = self.request.user.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        set_send_notif_telegram.delay(
            pk_habit=serializer.data['id']
        )  # Занесение переодичской задачи на отправку уведомлений
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsUserCreator]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        set_send_notif_telegram.delay(pk_habit=instance.pk)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class HabitDestroyAPIView(DestroyAPIView):
    """
    Удаление привычки
    """
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsUserCreator]

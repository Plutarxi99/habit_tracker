from django.urls import path

from habit.apps import HabitConfig
from habit.views import MyHabitListAPIView, PublicHabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitConfig.name

urlpatterns = [
    path('my/', MyHabitListAPIView.as_view(), name='my_habit_list'),
    path('public/', PublicHabitListAPIView.as_view(), name='public_habit_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
]

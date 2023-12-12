from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from habit.models import Habit
from habit.services import MixinListSerializer
from habit.validators import TimeRunValidator, RelatedAwardValidator, IsPrettyValidator, RelatedValidator, \
    EveryRunValidator, EveryRunValidatorUpdate
from users.models import User


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(ModelSerializer):
    # сохранение пользователя как создателя
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeRunValidator(obj='self'),
            RelatedValidator(obj='self'),
            RelatedAwardValidator(obj='self'),
            IsPrettyValidator(obj='self'),
            EveryRunValidator(obj='self')
        ]


class HabitUpdateSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeRunValidator(obj='self'),
            RelatedValidator(obj='self'),
            RelatedAwardValidator(obj='self'),
            IsPrettyValidator(obj='self'),
            EveryRunValidatorUpdate(obj='self')
        ]


class MyHabitListSerializer(MixinListSerializer, ModelSerializer):
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Habit
        fields = '__all__'


class PublicHabitListSerializer(MixinListSerializer, ModelSerializer):
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Habit
        fields = '__all__'

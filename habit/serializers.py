from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from habit.models import Habit
from habit.services import MixinListSerializer
from habit.validators import TimeRunValidator, RelatedAwardValidator, IsPrettyValidator, RelatedValidator
from users.models import User


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(ModelSerializer):

    # def is_valid(self, *, raise_exception=False):
    #     # dict(self)['user'] = self.context.items()
    #     print(self.context.get('user'))
    #     super().is_valid()

    # def save(self, **kwargs):
    #     self.validated_data['user'] = self.r
    #     super().save(**kwargs)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeRunValidator(field='time_run'),
            RelatedValidator(obj='self'),
            RelatedAwardValidator(obj='self'),
            IsPrettyValidator(obj='self')
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

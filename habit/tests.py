from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from habit.services import MixinTestCaseCreateUser
from users.models import User


class HabitTestCase(MixinTestCaseCreateUser, APITestCase):
    password = 'testpassword'
    email = 'test@test.test'
    email_1 = 'test_1@test.test'
    email_2 = 'test_2@test.test'
    email_3 = 'test_3@test.test'

    def setUp(self):
        user_data_setup = self.create_user_test(
            email=self.email,
            password=self.password,
        )
        self.user = user_data_setup['user']
        self.token = user_data_setup['token']

        self.habit = Habit.objects.create(
            is_pretty=False,
            award="тест ОК",
            is_public=False,
            location="двор тест",
            action_to_do="тест действия",
            time_to_do="2028-11-18T21:36:00Z",
            time_run="00:01:40",
            period="days",
            user=self.user,
            every_run=1
            # related=''
        )
        self.habit_pretty = Habit.objects.create(
            is_pretty=True,
            award=None,
            is_public=True,
            location="двор тест приятная",
            action_to_do="тест действия приятная",
            time_to_do="2028-11-18T21:36:00Z",
            time_run="00:01:40",
            period="days",
            user=self.user,
            every_run=1
            # related=''
        )
        self.habit_related = Habit.objects.create(
            is_pretty=False,
            award="тест ОК связанная",
            is_public=True,
            location="двор тест связанная",
            action_to_do="тест действия связанная",
            time_to_do="2028-11-18T21:36:00Z",
            time_run="00:01:40",
            period="days",
            user=self.user,
            related=self.habit_pretty,
            every_run=1
        )

    def test_habit_create(self):
        """Создание новой привычки"""
        user_data = self.create_user_test(email=self.email_1, password=self.password)
        data = {
            "is_pretty": False,
            "award": "яблоко",
            "is_public": True,
            "location": "двор тест",
            "action_to_do": "чистка проверка снега",
            "time_to_do": "2028-11-18T21:36:00Z",
            "time_run": "00:01:40",
            "period": "days",
            "every_run": 1
            # "user": user_data['user']
            # "related": self.habit
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            # '/habit/create/',
            data=data,
            headers={'Authorization': 'Bearer {}'.format(user_data['token'])}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_habit_public_list(self):
        """ Тестирование списка опубликованных привычек"""

        response = self.client.get(
            reverse('habit:public_habit_list'),
            headers={'Authorization': 'Bearer {}'.format(self.token)}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json()['count'],
            2
        )

    def test_habit_my_list(self):
        """ Тестирование списка моих привычек """
        user_data_my = self.create_user_test(email=self.email_2, password=self.password)
        self.habit = Habit.objects.create(
            is_pretty=False,
            award="тест ОК",
            is_public=False,
            location="двор тест",
            action_to_do="тест действия",
            time_to_do="2028-11-18T21:36:00Z",
            time_run="00:01:40",
            period="days",
            user=user_data_my['user'],
            every_run=1
            # related=''
        )

        response = self.client.get(
            reverse('habit:my_habit_list'),
            headers={'Authorization': 'Bearer {}'.format(user_data_my['token'])}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json()['count'],
            1
        )

    def test_my_habit_destroy(self):
        """ Тестирование удаление привычки"""

        user_data_des = self.create_user_test(email=self.email_1, password=self.password)

        habit_pk_4 = Habit.objects.create(
            is_pretty=False,
            award="тест ОК",
            is_public=False,
            location="двор тест",
            action_to_do="тест действия",
            time_to_do="2028-11-18T21:36:00Z",
            time_run="00:01:40",
            period="days",
            user=user_data_des['user'],
            every_run=1
            # related=''
        )
        pk = habit_pk_4.id
        response = self.client.delete(
            f'/habit/delete/{pk}/',
            headers={'Authorization': 'Bearer {}'.format(user_data_des['token'])}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_alien_habit_destroy(self):
        """ Удаление чужой привычки """
        user_data_des = self.create_user_test(email=self.email_1, password=self.password)

        pk = 1
        response = self.client.delete(
            f'/habit/delete/{pk}/',
            headers={'Authorization': 'Bearer {}'.format(user_data_des['token'])}
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_my_habit_update(self):
        """Тестирование обновление моей привычки"""
        user_data_upd = self.create_user_test(email=self.email_3, password=self.password)
        habit_update = Habit.objects.create(
            is_pretty=False,
            award="тест ОК",
            is_public=False,
            location="двор тест",
            action_to_do="тест действия",
            time_to_do="2028-11-18T21:36:00Z",
            time_run="00:01:40",
            period="days",
            user=user_data_upd['user'],
            every_run=1
            # related=''
        )

        data = {
            "action_to_do": "обновление"
        }
        response = self.client.patch(
            reverse('habit:habit_update', kwargs={"pk": habit_update.pk}),
            data=data,
            headers={'Authorization': 'Bearer {}'.format(user_data_upd['token'])},
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_alien_habit_update(self):
        """Тестирование обновление чужой привычки"""
        user_data_upd = self.create_user_test(email=self.email_3, password=self.password)
        data = {
            "action_to_do": "обновление"
        }
        response = self.client.patch(
            reverse('habit:habit_update', kwargs={"pk": self.habit.pk}),
            data=data,
            headers={'Authorization': 'Bearer {}'.format(user_data_upd['token'])},
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

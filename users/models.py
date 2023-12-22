from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from config.settings import NULLABLE
# from users.services import MyUserManager
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, chat_id_tg):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            chat_id_tg=chat_id_tg,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, chat_id_tg, password):
        """
        Создание суперпользователя, если уже пользователь существует,
        то ошибки не будет
        """
        user = self.get(
            email=email
        )
        if not user:
            user = self.create_user(
                email=email,
                password=password,
                chat_id_tg=chat_id_tg,
            )
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    chat_id_tg = models.CharField(max_length=30, verbose_name='для отправки ботом уведомлений')
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["chat_id_tg"]

    objects = MyUserManager()

    def has_one_of_groups(self, *groups: str) -> bool:
        groups_filter = Q()
        for group_name in groups:
            groups_filter |= Q(name=group_name)
        return self.groups.filter(groups_filter).exists()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

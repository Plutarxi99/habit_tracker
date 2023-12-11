from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from config.settings import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    chat_id_tg = models.CharField(max_length=30, verbose_name='для отправки ботом уведомлений', **NULLABLE)
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
    REQUIRED_FIELDS = []

    def has_one_of_groups(self, *groups: str) -> bool:
        groups_filter = Q()
        for group_name in groups:
            groups_filter |= Q(name=group_name)
        return self.groups.filter(groups_filter).exists()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

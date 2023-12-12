from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


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
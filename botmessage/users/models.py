from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import username_validator

ADMIN = 'admin'
USER = 'user'
ROLES = (
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь'),
)


class User(AbstractUser):
    """Создание кастомного класса User, описание базовых функций"""

    username = models.CharField(
        max_length=settings.FIELD_MAX_LENGTH,
        unique=True,
        db_index=True,
        validators=[username_validator],
        verbose_name='Никнейм'
    )

    email = models.EmailField(
        max_length=settings.FIELD_EMAIL_LENGTH,
        unique=True,
        verbose_name='Почта'
    )

    role = models.CharField(
        max_length=max([len(role) for role, name in ROLES]),
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

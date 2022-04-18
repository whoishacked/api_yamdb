from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
)


class User(AbstractUser):
    """User model customization class."""
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField('Роль пользователя',
                            max_length=16,
                            choices=ROLES,
                            default='user')
    password = models.CharField('Пароль',
                                max_length=128,
                                blank=True,
                                null=True,
                                default='')
    email = models.EmailField('Адрес электронной почты', unique=True)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

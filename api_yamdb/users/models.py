from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
)


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField('Роль пользователя',
                            max_length=16,
                            choices=ROLES,
                            default='user')
    password = models.CharField('password',
                                max_length=128,
                                blank=True,
                                null=True)
    email = models.EmailField('Адрес электронной почты')

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
)


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(max_length=16, choices=ROLES)

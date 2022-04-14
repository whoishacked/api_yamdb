import datetime
import random
import hashlib

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


def get_confirmation_code():
    random_num = str(random.random())
    data_time = str(datetime.datetime.now())
    hash_object = random_num + data_time
    hash_data = hashlib.md5(bytes(hash_object, encoding='utf8'))
    return str(hash_data.hexdigest())


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
    email = models.EmailField('Адрес электронной почты', unique=True)
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        default=get_confirmation_code()
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

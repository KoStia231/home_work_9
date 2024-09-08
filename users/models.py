from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    first_name = models.CharField(verbose_name='имя', max_length=30, unique=True)
    email = models.EmailField(verbose_name='почта', unique=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', **NULLABLE)
    phone_number = models.IntegerField(verbose_name='Телефон', **NULLABLE)
    country = models.CharField(verbose_name='Страна', max_length=100, **NULLABLE)
    token = models.CharField(max_length=255, **NULLABLE, verbose_name='Токен')
    new_password = models.CharField(verbose_name='Новый пароль', max_length=100, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.

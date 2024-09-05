from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', **NULLABLE)
    phone_number = models.IntegerField(verbose_name='Телефон', max_length=11)
    country = models.CharField(verbose_name='Страна', max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.

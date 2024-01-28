from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name='Фотография')
    date_of_bird = models.DateTimeField(blank=True, null=True, verbose_name='День рождения')

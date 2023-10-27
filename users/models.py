from django.contrib.auth.models import AbstractUser
from django.db import models

NULL = {'null': True, 'blank': True}

# Create your models here.

class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULL)
    city = models.CharField(max_length=75, verbose_name='город', **NULL)
    avatar = models.ImageField(upload_to='users_pics/', verbose_name='аватар', **NULL)

    email = models.EmailField(verbose_name='почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

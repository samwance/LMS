from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _

NULL = {'null': True, 'blank': True}


class UserRole(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULL)
    city = models.CharField(max_length=75, verbose_name='город', **NULL)
    avatar = models.ImageField(upload_to='users_pics/', verbose_name='аватар', **NULL)
    role = models.CharField(max_length=9, choices=UserRole.choices, default=UserRole.MEMBER)

    email = models.EmailField(verbose_name='почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

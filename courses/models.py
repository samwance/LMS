from django.db import models
from django.db.models import Q

from config import settings
from users.models import NULL, User


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='courses_pics/', verbose_name='превью курса', **NULL)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULL)
    price = models.IntegerField(verbose_name='цена', default=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='lessons_pics/', verbose_name='превью урока', **NULL)
    description = models.TextField(verbose_name='описание')
    url = models.URLField(verbose_name='ссылка на видео', **NULL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULL)
    price = models.IntegerField(verbose_name='цена', default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    date = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULL, related_name='payment')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULL, related_name='payment')
    amount = models.FloatField(verbose_name='сумма оплаты')
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('bank_transfer', 'Перевод на счет'),
    ]
    method = models.CharField(
        max_length=20,
        choices=payment_method_choices,
        default='cash'
    )

    def __str__(self):
        return f'{self.pk} {self.date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        constraints = [
            models.CheckConstraint(
                check=Q(course__isnull=False, lesson__isnull=True) | Q(course__isnull=True, lesson__isnull=False),
                name='course_and_lesson_not_both_null_or_both_filled'
            )
        ]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")

    def __str__(self):
        return f'{self.user.email} подписан на {self.course.title}'

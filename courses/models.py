from django.db import models

from users.models import NULL


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='courses_pics/', verbose_name='превью курса', **NULL)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='lessons_pics/', verbose_name='превью урока', **NULL)
    description = models.TextField(verbose_name='описание')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

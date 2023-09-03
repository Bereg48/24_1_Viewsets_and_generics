from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}
nl = '\n'


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    photo = models.ImageField(upload_to='main/', **NULLABLE, verbose_name='превью (картинка)')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name='урок')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.name} ({self.description}), {self.photo}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    photo = models.ImageField(upload_to='main/', **NULLABLE, verbose_name='превью (картинка)')
    link_video = models.CharField(max_length=150, verbose_name='ссылка на видео')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.name} ({self.description}), {self.photo}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

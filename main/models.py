from django.db import models
from django.db.models import DateTimeField

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


class Pay(models.Model):
    TRANSFER = 'transfer'
    CASH = 'cash'
    METHOD_PAY = [
        (TRANSFER, 'наличные'),
        (CASH, 'перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_time = DateTimeField(auto_now=False, auto_now_add=False, verbose_name='дата оплаты')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс')
    payment_amount = models.SmallIntegerField(max_length=150, verbose_name='сумма оплаты')
    method_pay = models.CharField(max_length=15, choices=METHOD_PAY, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} ({self.date_time}), {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

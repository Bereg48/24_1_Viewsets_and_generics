from django.db import models
from django.db.models import DateTimeField

from users.models import User

NULLABLE = {'blank': True, 'null': True}
nl = '\n'


class Course(models.Model):
    """Модель Course"""
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    photo = models.ImageField(upload_to='main/', **NULLABLE, verbose_name='превью (картинка)')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name='урок', related_name="course_set")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.description}), {self.photo}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель Lesson"""
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE, related_name="lesson_set")
    photo = models.ImageField(upload_to='main/', **NULLABLE, verbose_name='превью (картинка)')
    link_video = models.CharField(max_length=150, verbose_name='ссылка на видео')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.name} ({self.description}), {self.photo}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Pay(models.Model):
    """Модель Pay"""
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
    payment_amount = models.SmallIntegerField(verbose_name='сумма оплаты', null=True)
    method_pay = models.CharField(max_length=15, choices=METHOD_PAY, verbose_name='способ оплаты')
    is_paid = models.BooleanField(default=False, verbose_name="статус оплаты")
    session = models.CharField(max_length=250, verbose_name='сессия оплаты', **NULLABLE)

    def __str__(self):
        return f'{self.user} ({self.date_time}), {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    """Модель Subscription"""
    INSTALL = 'install'
    DELETE = 'delete'

    SUBSCRIPT = [
        (INSTALL, 'у пользователя есть подписка на курс'),
        (DELETE, 'у пользователя отсутствует подписка на курс'),
    ]

    UPDATES_USER = 'update_user'
    NOT_UPDAT_USER = 'not_updat_user'

    UPDATES = [
        (UPDATES_USER, 'пользователь подписан на обновления'),
        (NOT_UPDAT_USER, 'пользователь  не подписан на обновления'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    updates = models.CharField(max_length=15, choices=UPDATES, verbose_name='признак обновление')
    subscription = models.CharField(max_length=15, choices=SUBSCRIPT, verbose_name='признак подписки')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')


    def __str__(self):
        return f'{self.user} ({self.subscription})'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

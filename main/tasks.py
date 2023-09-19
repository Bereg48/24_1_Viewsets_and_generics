from celery import shared_task
from django.core.mail import send_mail
import logging
from config import settings
from config.celery import app
from .models import Course, Subscription

from datetime import timedelta
from main.tasks import send_course_update_email
from main.models import Subscription

unique_courses = set(sub.course for sub in Subscription.objects.all())
beat_schedule = {}

for index, course in enumerate(unique_courses):
    task_id = f"send_course_update_email_task_{index}"
    beat_schedule[task_id] = {
        "task": "main.tasks.send_course_update_email",
        "schedule": timedelta(seconds=60),  # Запускать каждые 60 секунд
        "args": (course.pk,),  # course_id здесь передается в качестве аргумента
    }

app.conf.beat_schedule = beat_schedule

logger = logging.getLogger(__name__)


### Рабочая версия 1 ###
@shared_task(name='send_message_subscriptions')
def send_course_update_email(course_id):
    logger.info(f"Starting send_course_update_email task with course_id: {course_id}")
    # Список подписчиков на обновления курса
    subscriptions = Subscription.objects.filter(course=course_id)

    # Объект курса
    course = Course.objects.get(pk=course_id)
    # Отправка письма подписчику
    for subscription in subscriptions:
        send_mail(
            subject=f"Курс {course.name} обновлен",
            message=f"Здравствуйте, {subscription.user.username}.\nКурс {course.name} был обновлен. Переходите на "
                    f"сайт, чтобы"
                    f"прочитать новый материал.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {subscription.user.email}")

    logger.info("Finished send_course_update_email task")


def notify_course_subscribers(course_id):
    logger.info(f"Starting notify_course_subscribers with course_id: {course_id}")
    send_course_update_email.delay(course_id)

### Рабочая версия 1 ###

### Рабочая версия 2 ###

# from celery import shared_task
# from django.core.mail import send_mail
# from .models import Subscription
#
#
# @shared_task
# def send_async_email(subject, message, from_email, recipient_list):
#     send_mail(subject, message, from_email, recipient_list)
#
#
# def send_emails_to_users(course_id):
#     subscriptions = Subscription.objects.filter(course_id=course_id, subscription=Subscription.INSTALL,
#                                                 updates=Subscription.UPDATES_USER)
#
#     subject = 'Обновление материалов курса'
#     message = 'Дорогой пользователь, материалы курса были обновлены. Посетите сайт, чтобы ознакомиться с новыми ' \
#               'материалами.'
#     from_email = settings.EMAIL_HOST_USER
#
#     for subscription in subscriptions:
#         recipient_list = [subscription.user.email]
#         print(recipient_list)
#         send_async_email.delay(subject, message, from_email, recipient_list)
#
#
# def notify_course_subscribers(course_id):
#     send_emails_to_users(course_id)
### Рабочая версия 2 ###

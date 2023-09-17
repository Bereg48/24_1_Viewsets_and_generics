from rest_framework import serializers

from main.models import Course, Lesson, Pay, Subscription
from main.services import retrieve_session
from main.validators import DescriptionLessonValidator
from users.models import User
from users.serializers import UserSerializers


class LessonSerializers(serializers.ModelSerializer):
    """Класс LessonSerializers сериализует данные полученные в соответствии с установленной моделью класса Lesson,
    данные сериализуются, в рамках функциональности CRUD"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    validators = [DescriptionLessonValidator(field='link_video')]

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    """Класс CourseSerializers сериализует данные полученные в соответствии с установленной моделью класса Course,
        данные сериализуются, в рамках функциональности CRUD"""
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializers(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        # validators = [DescriptionCourseValidator(field='description')]

    def get_lesson_count(self, lesson):
        return lesson.lesson_set.count()


class PaySerializers(serializers.ModelSerializer):
    """Класс PaySerializers сериализует данные полученные в соответствии с установленной моделью класса Pay,
            данные сериализуются, в рамках функциональности CRUD"""

    class Meta:
        model = Pay
        fields = '__all__'


class PayRetrieveSerializers(serializers.ModelSerializer):
    """Класс PayRetrieveSerializers сериализует данные полученные в соответствии с установленной моделью класса Pay,
            данные сериализуются, в рамках функциональности CRUD"""
    user = UserSerializers(read_only=True)
    lesson = LessonSerializers(read_only=True)
    course = CourseSerializers(read_only=True)
    url_for_pay = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pay
        fields = '__all__'

    def get_url_for_pay(self, instance):
        """Метод возвращает ссылку на оплату"""

        if instance.is_paid:
            return None

        session = retrieve_session(instance.session)
        if session.payment_status == 'unpaid' and session.status == 'open':
            return session.url
        elif session.payment_status == 'paid' and session.status == 'complete':
            return None
        status = {
            'session': "Сессия завершена, создайте платеж заново"
        }
        return status


class PayCreateSerializers(serializers.ModelSerializer):
    lesson = serializers.SlugRelatedField(slug_field='id', queryset=Lesson.objects.all(),
                                          allow_null=True, required=False)
    course = serializers.SlugRelatedField(slug_field='id', queryset=Course.objects.all(),
                                          allow_null=True, required=False)
    user = serializers.SlugRelatedField(slug_field='phone', queryset=User.objects.all())

    class Meta:
        model = Pay
        fields = '__all__'


class SubscriptionSerializers(serializers.ModelSerializer):
    """Класс SubscriptionSerializers сериализует данные полученные в соответствии с установленной моделью класса Subscription,
                данные сериализуются, в рамках функциональности CRUD"""

    class Meta:
        model = Subscription
        fields = '__all__'

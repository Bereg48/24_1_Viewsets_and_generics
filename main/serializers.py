from rest_framework import serializers

from main.models import Course, Lesson, Pay, Subscription
from main.validators import DescriptionLessonValidator


class LessonSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    validators = [DescriptionLessonValidator(field='link_video')]

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializers(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        # validators = [DescriptionCourseValidator(field='description')]

    def get_lesson_count(self, lesson):
        return lesson.lesson_set.count()


class PaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'


class SubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

from rest_framework import serializers

from main.models import Course, Lesson, Pay


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializers(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()


class PaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from main.models import Course, Lesson, Pay
from main.serializers import CourseSerializers, LessonSerializers, PaySerializers


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class PayCreateAPIView(generics.CreateAPIView):
    serializer_class = PaySerializers


class PayListAPIView(generics.ListAPIView):
    serializer_class = PaySerializers
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method_pay']
    ordering_fields = ('date_time',)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from main.models import Course, Lesson, Pay, Subscription
from main.paginator import MainPaginator
from main.permissions import IsModerator, IsOwner, IsOwnerUpdate, IsOwnerOrReadOnly
from main.serializers import CourseSerializers, LessonSerializers, PaySerializers, SubscriptionSerializers


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = IsAuthenticated
    pagination_class = MainPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MainPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class PayCreateAPIView(generics.CreateAPIView):
    serializer_class = PaySerializers
    permission_classes = IsAdminUser


class PayListAPIView(generics.ListAPIView):
    serializer_class = PaySerializers
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method_pay']
    ordering_fields = ('date_time',)
    permission_classes = IsAuthenticated
    pagination_class = MainPaginator


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MainPaginator


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializers
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]

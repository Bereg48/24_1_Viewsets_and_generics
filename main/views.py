from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from main.models import Course, Lesson, Pay, Subscription
from main.paginator import MainPaginator
from main.permissions import IsModerator, IsOwner, IsOwnerUpdate, IsOwnerOrReadOnly
from main.serializers import CourseSerializers, LessonSerializers, PaySerializers, SubscriptionSerializers, \
    PayCreateSerializers, PayRetrieveSerializers
from main.services import get_session, retrieve_session


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet класса Course"""
    serializer_class = CourseSerializers
    queryset = Course.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    pagination_class = MainPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    """Класс LessonCreateAPIView отвечате за функциональность добавления урока при применении
    класса LessonSerializers, который функционирует в соответсвии с определенной моделью класса Lesson"""
    serializer_class = LessonSerializers
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Класс LessonListAPIView отвечает за функциональность просмотра урока при применении
    класса LessonSerializers, который функционирует в соответствии с определенной моделью класса Lesson"""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    pagination_class = MainPaginator
    ordering_fields = ["name", "description"]
    ordering = ["name"]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс LessonRetrieveAPIView отвечает за функциональность просмотра конкретного урока при применении
        класса LessonSerializers, который функционирует в соответствии с определенной моделью класса Lesson"""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс LessonUpdateAPIView отвечает за функциональность обновление конкретного урока при применении
        класса LessonSerializers, который функционирует в соответствии с определенной моделью класса Lesson"""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс LessonDestroyAPIView отвечает за функциональность удаления конкретного урока при применении
            класса LessonSerializers, который функционирует в соответствии с определенной моделью класса Lesson"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class PayRetrieveAPIView(generics.RetrieveAPIView):
    """Класс PayRetrieveAPIView отвечает за функциональность извлечения информации об оплате при применении
                класса PaySerializers, который функционирует в соответствии с определенной моделью класса Pay"""
    serializer_class = PayRetrieveSerializers
    queryset = Pay.objects.all()

    def get_object(self):
        """Метод get_object получает объект по pk от пользователя. Если такого нет, то возвращается ошибка"""
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        session = retrieve_session(obj.session)
        if session.payment_status == 'paid' and session.status == 'complete':
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj


class PayCreateAPIView(generics.CreateAPIView):
    """Класс PayCreateAPIView отвечает за функциональность добавления информации об оплате при применении
                класса PayCreateSerializers, который функционирует в соответствии с определенной моделью класса Pay"""
    serializer_class = PayCreateSerializers
    queryset = Pay.objects.all()

    def perform_create(self, serializer):
        lesson = serializer.validated_data.get('lesson')
        course = serializer.validated_data.get('course')
        if not lesson and not course:
            raise serializers.ValidationError({
                'not_empty_fields': "Заполните lesson или course"
            })
        new_nat = serializer.save()
        new_nat.user = self.request.user
        new_nat.session = get_session(new_nat).id
        new_nat.save()


class PayListAPIView(generics.ListAPIView):
    """Класс PayListAPIView отвечает за функциональность просмотра листа информации об оплате при применении
                класса PaySerializers, который функционирует в соответствии с определенной моделью класса Pay"""
    serializer_class = PaySerializers
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method_pay']
    ordering_fields = ('date_time',)
    permission_classes = IsAuthenticated
    pagination_class = MainPaginator


class SubscriptionListAPIView(generics.ListAPIView):
    """Класс SubscriptionListAPIView отвечает за функциональность просмотра листа информации о подписках пользователней
    при применении класса SubscriptionSerializers, который функционирует в соответствии с определенной моделью класса Subscription"""
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MainPaginator


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Класс SubscriptionCreateAPIView отвечает за функциональность добавления информации о подписках пользователней
        при применении класса SubscriptionSerializers, который функционирует в соответствии с определенной моделью класса Subscription"""
    serializer_class = SubscriptionSerializers
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Класс SubscriptionCreateAPIView отвечает за функциональность удаление информации о подписках отдельного пользователя
        при применении класса SubscriptionSerializers, который функционирует в соответствии с определенной моделью класса Subscription"""
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """Класс SubscriptionCreateAPIView отвечает за функциональность обновление информации о подписках отдельного пользователя
        при применении класса SubscriptionSerializers, который функционирует в соответствии с определенной моделью класса Subscription"""
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """Класс SubscriptionCreateAPIView отвечает за функциональность просмотр информации о подписках отдельного пользователя
        при применении класса SubscriptionSerializers, который функционирует в соответствии с определенной моделью класса Subscription"""
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]

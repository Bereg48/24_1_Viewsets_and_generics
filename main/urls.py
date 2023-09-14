from django.urls import path

from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from main.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PayCreateAPIView, PayListAPIView, SubscriptionListAPIView, \
    SubscriptionCreateAPIView, SubscriptionDestroyAPIView, SubscriptionUpdateAPIView, SubscriptionRetrieveAPIView

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [

                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
                  path('pay/', PayListAPIView.as_view(), name='pay-list'),
                  path('pay/create/', PayCreateAPIView.as_view(), name='pay-create'),
                  path('subscription/', SubscriptionListAPIView.as_view(), name='subscription-list'),
                  path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
                  path('subscription/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription-retrieve'),
                  path('subscription/update/<int:pk>/', SubscriptionUpdateAPIView.as_view(), name='subscription-update'),
                  path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),

              ] + router.urls

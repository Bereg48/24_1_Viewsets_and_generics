from django.urls import path

from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from main.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'main', CourseViewSet, basename='main')

urlpatterns = [
                  path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

              ] + router.urls

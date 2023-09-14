from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Course, Lesson, Subscription
from users.models import User
from rest_framework import status
from django.urls import reverse


class CourseAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='ivan', password='454125')
        self.lesson = Lesson.objects.create(
            name='test',
            link_video='vdvdsvsd',
            user=self.user
        )

    def test_get_course(self):
        """Тестирование просмотра курсов"""

        response = self.client.get('/course/')

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='oleg', password='454125')
        self.client.login(username='oleg', password='454125')

    def test_create_subscription(self):
        """Тестирование создание подписки"""
        self.client.force_authenticate(user=self.user)

        # Отправка POST-запроса для создания объекта
        response = self.client.post('/subscription/create/', {
            'user': self.user.id,
            'updates': 'not_updat_user',
            'subscription': 'install',
        })

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка создания объекта в базе данных
        self.assertTrue(
            Subscription.objects.filter(id=1, updates='not_updat_user', subscription='install',
                                        user=self.user.id).exists())

    def test_read_subscription(self):
        """Тестирование просмотра подписок"""
        subscription = Subscription.objects.create(
            user=self.user,
            updates='not_updat_user',
            subscription='install',
        )
        response = self.client.get(f'/subscription/{subscription.id}/')
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_subscription(self):
        self.client.force_authenticate(user=self.user)
        """Тестирование просмотра подписки"""

        response = self.client.get('/subscription/')

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscription(self):
        """Тестирование удаления подписок"""
        self.client.force_authenticate(user=self.user)
        subscription = Subscription.objects.create(
            user=self.user,
            updates='not_updat_user',
            subscription='install',
        )
        response = self.client.delete(f'/subscription/delete/{subscription.id}/')
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Subscription.DoesNotExist):
            Subscription.objects.get(id=subscription.id)


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_lesson(self):
        """Тестирование создания уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lesson/create/', {
            'user': self.user,
            'name': 'New Lesson',
            'link_video': 'Lesson content goes here',
        })

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_lesson(self):
        """Тестирование просмотра уроков"""
        lesson = Lesson.objects.create(
            user=self.user,
            name='Test Lesson',
            link_video='Lesson content goes here',
        )
        response = self.client.get(f'/lesson/{lesson.id}/')
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Тестирование обновления уроков"""
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(
            user=self.user,
            name='Old Lesson',
            link_video='Old lesson content',
        )
        response = self.client.put(f'/lesson/update/{lesson.id}/', {
            'name': 'Updated Lesson',
            'link_video': 'Updated lesson content',
        })
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_lesson = Lesson.objects.get(id=lesson.id)
        self.assertEqual(updated_lesson.name, 'Updated Lesson')
        self.assertEqual(updated_lesson.link_video, 'Updated lesson content')

    def test_delete_lesson(self):
        """Тестирование удаления уроков"""
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(
            user=self.user,
            name='To be deleted',
            link_video='This lesson will be deleted',
        )
        response = self.client.delete(f'/lesson/delete/{lesson.id}/')
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=lesson.id)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Lesson, Subscription
from users.models import User


# class CourseTestCase(APITestCase):
#
#     def setUp(self):
#         self.course = Course.objects.create(
#             name='test_course',
#             description='test_c'
#         )
#
#     def test_get_list(self):
#         self


class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='test_lesson',
            description='test_l',
            course=self.course,
            url='http://www.youtube.com/test_l',
            owner=self.user
        )

    def test_list(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(
            reverse('courses:lessons_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'id': self.lesson.pk,
                  'name': self.lesson.name,
                  'preview': None,
                  'description': self.lesson.description,
                  'course': self.course.pk,
                  'owner': self.user.pk,
                  'url': self.lesson.url
                  }
             ]
             }
        )

    def test_retrieve(self):
        """Тестирование вывода одного урока"""
        response = self.client.get(
            reverse('courses:lesson', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk,
             'name': self.lesson.name,
             'preview': None,
             'description': self.lesson.description,
             'course': self.course.pk,
             'owner': self.user.pk,
             'url': self.lesson.url
             }
        )

    def test_create(self):
        """Тестирование создания урока"""
        data = {
            'name': 'test_lesson',
            'description': 'test_l',
            'course': self.course.pk,
            'url': 'http://www.youtube.com/test_l'
        }

        response = self.client.post(
            reverse('courses:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2,
             'name': 'test_lesson',
             'preview': None,
             'description': 'test_l',
             'course': self.course.pk,
             'owner': self.user.pk,
             'url': 'http://www.youtube.com/test_l'
             }

        )

    def test_update(self):
        """Тестирование обновления урока"""
        data = {
            'name': 'test_lesson_upd'
        }

        response = self.client.patch(
            reverse('courses:lesson_update', kwargs={'pk': self.lesson.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk,
             'name': 'test_lesson_upd',
             'preview': None,
             'description': self.lesson.description,
             'course': self.course.pk,
             'owner': self.user.pk,
             'url': self.lesson.url
             }
        )

    def test_delete(self):
        """Тестирование удаления урока"""
        response = self.client.delete(
            reverse('courses:lesson_delete', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user
        )

    def test_create(self):
        """Тестирование создания подписки"""
        subscription = {
            "user": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.post(
            reverse('courses:sub_create', kwargs={'pk': self.course.pk}),
            data=subscription
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete(self):
        """Тестирование удаления подписки"""

        course = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.delete(
            reverse('courses:sub_delete', kwargs={'pk': course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

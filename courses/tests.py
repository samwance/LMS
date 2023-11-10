from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='test_course',
            description='test_c'
        )

    def test_get_list(self):
        self


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

    def test_get_list(self):
        response = self.client.get(
            reverse('courses:lessons_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        print(response.json())

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                {'id': 1,
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

    def test_create(self):
        data = {
            'name': 'test_lesson',
            'description': 'test_l',
            'course': self.course,
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



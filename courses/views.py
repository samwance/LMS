from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

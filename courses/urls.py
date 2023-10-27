from django.urls import path

from courses.apps import CoursesConfig
from courses.views import LessonListAPIView, LessonCreateAPIView, CourseViewSet, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonRetrieveAPIView
from rest_framework.routers import DefaultRouter

app_name = CoursesConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls
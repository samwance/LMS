from django.urls import path

from courses.apps import CoursesConfig
from courses.views import LessonListAPIView, LessonCreateAPIView, CourseViewSet, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonRetrieveAPIView, PaymentListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, LessonPaymentAPIView, CoursePaymentAPIView
from rest_framework.routers import DefaultRouter

app_name = CoursesConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('courses/<int:pk>/pay/', CoursePaymentAPIView.as_view(), name='course_pay'),
    path('lessons/<int:pk>/pay/', LessonPaymentAPIView.as_view(), name='lesson_pay'),
    path('courses/<int:pk>/create_sub/', SubscriptionCreateAPIView.as_view(), name='sub_create'),
    path('courses/<int:pk>/delete_sub/', SubscriptionDestroyAPIView.as_view(), name='sub_delete'),
] + router.urls
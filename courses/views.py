from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson, Payment, Subscription
from courses.paginators import CoursePaginator, LessonPaginator
from courses.permissons import IsOwner, IsModerator, IsSubscriber
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from courses.tasks import send_course_update_email


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer


    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()



class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]
    pagination_class = LessonPaginator


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]

    def perform_update(self, serializer):
        serializer.save()
        pk = self.kwargs.get('pk')
        course = Lesson.objects.get(pk=pk).course
        subscriptions = Subscription.objects.filter(course=course)

        if subscriptions:
            for subscription in subscriptions:
                send_course_update_email.delay(subscription.pk)


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [~IsModerator, IsOwner]
        else:
            permission_classes = [IsModerator | IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        serializer.save()
        pk = self.kwargs.get('pk')
        course = Course.objects.get(pk=pk)
        subscriptions = Subscription.objects.filter(course=course)

        if subscriptions:
            for subscription in subscriptions:
                send_course_update_email.delay(subscription.pk)


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('date',)

class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        pk = self.kwargs.get('pk')
        new_subscription.course = Course.objects.get(pk=pk)
        new_subscription.save()

class SubscriptionDestroyAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSubscriber]


class LessonPaymentAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        payment_link = serializer.data['payment_link']
        return Response({'payment_link': payment_link})


class CoursePaymentAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        payment_link = serializer.data['payment_link']
        return Response({'payment_link': payment_link})

from datetime import date

from rest_framework import serializers
from courses.models import Course, Lesson, Payment, Subscription
from courses.services import get_link_to_pay
from courses.validators import validator_links


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[validator_links])
    payment_link = serializers.SerializerMethodField(read_only=True)

    def get_payment_link(self, lesson):
        user = self.context['request'].user
        current_date = date.today()
        Payment.objects.create(
            user=user,
            date=current_date,
            lesson=lesson,
            amount=lesson.price,
            method='bank_transfer'
        )

        return get_link_to_pay(lesson)
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'preview', 'description', 'course', 'owner', 'url', 'payment_link')


class CourseSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    payment_link = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    def get_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def get_payment_link(self, course):
        user = self.context['request'].user
        current_date = date.today()
        Payment.objects.create(
            user=user,
            date=current_date,
            course=course,
            amount=course.price,
            method='bank_transfer'
        )

        return get_link_to_pay(course)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'preview', 'lessons_count', 'lessons', 'owner', 'subscribed',
                  'payment_link')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

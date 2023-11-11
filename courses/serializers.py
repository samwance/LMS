from rest_framework import serializers
from courses.models import Course, Lesson, Payment, Subscription
from courses.validators import validator_links


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[validator_links])

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'preview', 'description', 'course', 'owner', 'url')


class CourseSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    def get_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'preview', 'lessons_count', 'lessons', 'owner', 'subscribed')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

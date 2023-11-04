from rest_framework import serializers
from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'preview', 'description', 'course', 'owner')


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lesson_set.count()
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'preview', 'lessons_count', 'lessons', 'owner')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

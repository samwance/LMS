from rest_framework import serializers
from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'preview', 'description', 'course')


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return course.lessons_set.all()
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'preview', 'lesson_count', 'lesson')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

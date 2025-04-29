from rest_framework.serializers import ModelSerializer
from .models import *


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CoursePostSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'instructor', 'created_at')

        extra_kwargs = {
            'instructor': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }
        }


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('created_at',)


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

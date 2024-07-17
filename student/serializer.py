from rest_framework import serializers
from .models import ReviewModel,CourseEnrolModel

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'

class CourseEnrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrolModel
        fields='__all__'
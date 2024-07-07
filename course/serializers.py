from .models import CourseModel
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields='__all__'
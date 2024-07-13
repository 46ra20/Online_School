from .models import CourseModel,CourseCategory
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields='__all__'
        
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
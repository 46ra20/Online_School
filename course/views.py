from django.shortcuts import render
from .models import CourseModel
from .serializers import CourseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import Http404
# Create your views here.

class CourseView(APIView):
    def get(self,request,id):
        courses = CourseModel.objects.filter(pk=id)
        serializer = CourseSerializer(courses,many=True)
        return Response(serializer.data)

class AllCourseView(APIView):
    def get(self,request,home):
        if home=='home':
            courses = CourseModel.objects.all()[0:4]
        else:
            courses = CourseModel.objects.all()
        serializer = CourseSerializer(courses,many=True)
        return Response(serializer.data)


class CourseViewForTeacher(APIView):
    # permission_classes=[IsAdminUser]
    def get(self,request,teacher_id):
        try:
            teacher = User.objects.get(pk=teacher_id)
        except(User.DoesNotExist):
            teacher=None
        print(teacher)
        if teacher is not None and teacher.is_staff:
            courses = CourseModel.objects.filter(user = teacher)
            serializer = CourseSerializer(courses,many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,teacher_id):
        try:
            teacher = User.objects.get(pk=teacher_id)
        except(User.DoesNotExist):
            teacher=None
        print(teacher,request.user)
        if teacher is not None and teacher.is_staff:
            
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_501_NOT_IMPLEMENTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class CourseEditOrDeleteViewForTeacher(APIView):
    # permission_classes=[IsAdminUser]
    def get_object(self,pk):
        try:
            course = CourseModel.objects.get(pk=pk)
        except(CourseModel.DoesNotExist):
            raise Http404
        return course
    
    def get_teacher(self,teacher_id):
        try:
            teacher = User.objects.get(pk=teacher_id)
        except(User.DoesNotExist):
            raise Http404
        
        if teacher is not None and teacher.is_staff:
            return teacher
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,teacher_id,id):
        course = self.get_object(pk=id)
        teacher = self.get_teacher(teacher_id=teacher_id)

        if course is not None and teacher is not None and course.user.id == teacher.id:
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,teacher_id,id):
        course = self.get_object(pk=id)
        teacher = self.get_teacher(teacher_id=teacher_id)

        serializer = CourseSerializer(course, data = request.data,partial=True)

        # print(serializer)
        # if serializer.is_valid():
        #     serializer.save()
        if course.user.id == teacher.id:
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                print(serializer.errors)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,teacher_id,id):
        course = self.get_object(pk=id)
        if course is not None:
            course.delete()
            return Response(status=status.HTTP_301_MOVED_PERMANENTLY)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        

    

from django.shortcuts import render
from .serializer import ReviewSerializers,CourseEnrlSerializer
from .models import ReviewModel,CourseEnrolModel
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from course.models import CourseModel
from course.serializers import CourseSerializer
from django.contrib.auth.models import User
from account.models import UserRegistrarionModel
# Create your views here.

class AllReviewView(viewsets.ViewSet):
    def list(self,request):
        data = []
        reviews = ReviewModel.objects.all()
        serializer = ReviewSerializers(reviews,many=True)
        for sr in serializer.data:
            get_data = {}
            try:
                user = User.objects.get(pk=sr['reviewer'])
                image = UserRegistrarionModel.objects.get(user=user)
                get_data['name'] = f'{user.first_name} {user.last_name}'
                get_data['image'] = str(image.image)
                get_data['review']=sr['review']
                get_data['rating']=sr['rating']
                get_data['date']=sr['date']

                # print(get_data)
                data.append(get_data)
            except(User.DoesNotExist):
                return Response({'error':"bad request"})
        return Response({'data':data})

class ReviewView(viewsets.ViewSet):
    # permission_classes=[IsAuthenticated]
    def list(self,request,course_id):
        data = []
        reviews = ReviewModel.objects.filter(course=course_id)
        serializer = ReviewSerializers(reviews,many=True)
        for sr in serializer.data:
            get_data = {}
            try:
                user = User.objects.get(pk=sr['reviewer'])
                image = UserRegistrarionModel.objects.get(user=user)
                get_data['name'] = f'{user.first_name} {user.last_name}'
                get_data['image'] = str(image.image)
                get_data['review']=sr['review']
                get_data['rating']=sr['rating']
                get_data['date']=sr['date']

                # print(get_data)
                data.append(get_data)
            except(User.DoesNotExist):
                return Response({'error':"bad request"})
        return Response({'data':data})
    

    def create(self,request):
        serializer = ReviewSerializers(data = request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"comment push successfully"})
        print(serializer.errors)
        return Response({"error":"someting wrong plase try agin"})
        

class CourseEnrolView(viewsets.ViewSet):
    # permission_classes=[IsAuthenticated]
    def list(self,request,enrol_by):
        courses=CourseEnrolModel.objects.filter(enrol_by=enrol_by)
        # data = {enroled_courses.enrol_course.title,enroled_courses.enrol_course.price,enroled_courses.date}
        serializer =CourseEnrlSerializer(courses,many=True)
        course_details = []
        for cr in serializer.data:
            print(cr['enrol_course'])
            try:
                course = CourseModel.objects.get(pk=cr['enrol_course'])
                sr = CourseSerializer(course)
                data = {}
                data
                data['title']=sr.data['title']
                data['price']=sr.data['price']
                data['course_duration']=sr.data['course_duration']
                course_details.append(data)
            except(CourseModel.DoesNotExist):
                course = None
        return Response({"data":serializer.data,"course_details":course_details})

    def create(self,request):
        # enroled_courses=CourseEnrolModel
        print(request.data['enrol_course'],request.data['enrol_by'])
        try:
            is_enroled = CourseEnrolModel.objects.filter(enrol_course=request.data['enrol_course'],enrol_by=request.data['enrol_by'])
        except(CourseEnrolModel.DoesNotExist):
            is_enroled=False
        # print(is_enroled)
        if len(is_enroled) == 0:
            serializer =CourseEnrlSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({"msg":"Already enroled this course"})
    def destroy(self,request,id):
        try:
            course = CourseEnrolModel.objects.get(pk=id)
            course.delete()
            return Response({'success':'Course Unenroled successfully'})
        except(CourseEnrolModel.DoesNotExist):
            course=None
            return Response({'error':'Operation Faild'})

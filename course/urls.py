from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CourseView,CourseViewForTeacher,AllCourseView,CourseEditOrDeleteViewForTeacher,CategoryView,GetCourseByDep


router = DefaultRouter()
# router.register('authentic',CourseView)

urlpatterns = [
    path('public/<id>/',CourseView.as_view()),
    path('public/all/<home>/',AllCourseView.as_view()),

    path('authentic/<teacher_id>/',CourseViewForTeacher.as_view()),
    path('details/<teacher_id>/<id>/',CourseEditOrDeleteViewForTeacher.as_view()),
    path('get_by_dep/<dep_id>/',GetCourseByDep.as_view()),
    # category all
    path('category/',CategoryView.as_view({'get':'list'}))
]

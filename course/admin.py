from django.contrib import admin
from .models import CourseCategory,CourseModel
# Register your models here.

class AdminTable(admin.ModelAdmin):
    list_display=['teacher_name','title','price','course_duration','date']

    def teacher_name(self,obj):
       return obj.user.first_name+' '+obj.user.last_name

admin.site.register(CourseCategory)
admin.site.register(CourseModel,AdminTable)

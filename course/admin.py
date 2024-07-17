from django.contrib import admin
from .models import CourseCategory,CourseModel
# Register your models here.

class AdminTable(admin.ModelAdmin):
    list_display=['teacher_name','title','price','course_duration','date']

    def teacher_name(self,obj):
       return obj.user
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["category"]}

admin.site.register(CourseCategory,CategoryAdmin)
admin.site.register(CourseModel,AdminTable)

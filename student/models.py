from django.db import models
from django.contrib.auth.models import User
from course.models import CourseModel

# Create your models here.

USER_TRATING = [
    ('1','★'),
    ('2','★★'),
    ('3','★★★'),
    ('4','★★★★'),
]

class ReviewModel(models.Model):
    rating = models.CharField(max_length=4,choices=USER_TRATING)
    review = models.TextField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(CourseModel,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.reviewer.first_name} {self.reviewer.last_name} review to {self.course.title}'



class CourseEnrolModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    enrol_by = models.ForeignKey(User,on_delete=models.CASCADE)
    enrol_course = models.ForeignKey(CourseModel,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.enrol_by.first_name} enrolled {self.enrol_course.title}'
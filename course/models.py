from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CourseCategory(models.Model):
    category = models.CharField(max_length=30)
    slug = models.SlugField(default="",null=False)

    def __str__(self) -> str:
        return self.category
    
class CourseModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assessment_methods=models.TextField(blank=True)
    learing_outcomes = models.TextField()
    course_duration =models.CharField(max_length=100)
    prerequisites=models.TextField(blank=True)
    image = models.ImageField(upload_to='course/image',blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)

    department = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title}'


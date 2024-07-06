from django.db import models
from django.contrib.auth.models import User
# Create your models here.
ACCOUNT_TYPE = [
    ('STUDENT','Student'),
    ('TEACHER','Teacher'),
]

class UserRegistrarionModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='account/image')
    account_type = models.CharField(choices=ACCOUNT_TYPE,max_length=10)

    def __str__(self) -> str:
        return self.user.first_name+' '+self.user.last_name

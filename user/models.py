from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    designation=[
        ("TEACHER","Teacher"),
        ("STUDENT","Student"),
    ]
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)
    designation=models.CharField(max_length=50,choices=designation,default="STUDENT")


    def __str__(self):
        return "{} profile".format(self.user.username)
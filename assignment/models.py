from django.db import models
from django.contrib.auth.models import User
from group.models import Classroom
from django.utils import timezone

# Create your models here.

class Assignment(models.Model):
    name=models.CharField(max_length=255)
    message=models.CharField(max_length=500)
    uploader=models.ForeignKey(User,on_delete=models.CASCADE)
    classroom=models.ForeignKey(Classroom,on_delete=models.CASCADE)
    file=models.FileField(upload_to='assignment',blank=False)
    date_uploaded=models.DateTimeField(default=timezone.now)
    date_submission=models.DateField()

    def __str__(self):
        return self.name

class Submission(models.Model):
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='submission',blank=False)
    submission_date=models.DateTimeField(default=timezone.now)
    remark=models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.student.username

   
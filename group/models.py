from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Classroom(models.Model):
    code=models.CharField(max_length=10, unique=True)
    name=models.CharField(max_length=255)
    sub_code=models.CharField(max_length=255)
    admin=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin')
    members=models.ManyToManyField(User,through='ClassMember')


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group:classroom_details', kwargs={'pk': self.pk})

    class Meta:
        ordering=['name']


class ClassMember(models.Model):
    classroom=models.ForeignKey(Classroom,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together=('classroom','user')
from django.shortcuts import render
from user.forms import UserRegistrationForm,UserProfileForm
from ams.decorators import unauthenticated_user

@unauthenticated_user
def index(request):
    u_form=UserRegistrationForm()
    p_form=UserProfileForm()
    context={'u_form':u_form,'p_form':p_form}
    return render(request,'ams/index.html',context)

def welcome(request):
    return render(request,'ams/welcome.html')
    
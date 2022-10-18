from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from user.forms import UserRegistrationForm,UserProfileForm,UserUpdateForm,UserProfileUpdateForm
from user.models import Profile
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login
from ams.decorators import unauthenticated_user
# Create your views here.

@unauthenticated_user
def register(request):
    if request.method=='POST':
        u_form=UserRegistrationForm(request.POST)
        p_form=UserProfileForm(request.POST,request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            check=User.objects.filter(email=u_form.cleaned_data.get('email')).exists()
            if check is False:
                user=u_form.save()
                user.save()
                designation=p_form.cleaned_data.get('designation')
                
                if designation=='TEACHER':
                    group=Group.objects.get(name='TEACHERS')
                    user.groups.add(group)
                else:
                    group=Group.objects.get(name='STUDENTS')
                    user.groups.add(group)
                profile=p_form.save(commit=False)
                profile.user=user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic=request.FILES['profile_pic']
                profile.save()
                messages.success(request,"Your account has been created. Click Log In to Sign In")
                return redirect('index')
            else:
                messages.warning(request,'Email already exists')
                return redirect('index')
    
    return render(request,'ams/index.html')

@unauthenticated_user
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                if user.profile.designation=="TEACHER":
                    login(request,user)
                    return HttpResponseRedirect(reverse('group:teacher_dashboard'))
                else:
                    login(request,user)
                    return HttpResponseRedirect(reverse('group:student_dashboard'))
            else:
                return HttpResponse('Account is not active')
        else:
            return HttpResponse('User does not exists')
    return render(request,'ams/index.html')

def profile_update(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=UserProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Your profile has been successfully updated")
            return redirect('welcome')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=UserProfileUpdateForm(instance=request.user.profile)
        context={'u_form':u_form,'p_form':p_form}
    return render(request,'ams/update.html',context)

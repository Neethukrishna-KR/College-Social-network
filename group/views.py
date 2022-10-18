from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect
from group.models import ClassMember,Classroom 
from assignment.models import Assignment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from group.forms import JoinClassForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from ams.decorators import allowed_users


# Create your views here.
@login_required
@allowed_users(allowed_roles=['TEACHERS'])
def teacher_dashboard(request):
    return render(request,'group/teacher_dashboard.html')

@login_required
@allowed_users(allowed_roles=['STUDENTS'])
def student_dashboard(request):
    return render(request,'group/student_dashboard.html')

@method_decorator(allowed_users(allowed_roles=['TEACHERS']), name='dispatch')
class CreateClassroom(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    model=Classroom
    fields=('code','name','sub_code')
    success_message="Created Successfully"

    def form_valid(self,form):
        form.instance.admin=self.request.user
        return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['TEACHERS']), name='dispatch')
class UpdateClassroom(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,generic.UpdateView):
    model=Classroom
    fields=('name','sub_code')
    success_message="Updated Successfully"

    def form_valid(self,form):
        form.instance.admin=self.request.user
        return super().form_valid(form)

    def test_func(self):
        classroom=self.get_object()
        if self.request.user ==classroom.admin:
            return True
        return False

@method_decorator(allowed_users(allowed_roles=['TEACHERS']), name='dispatch')
class DeleteClassroom(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    model=Classroom
    success_url=reverse_lazy('group:teacher_dashboard')
    

    def test_func(self):
        classroom=self.get_object()
        if self.request.user ==classroom.admin:
            return True
        return False


@login_required
def classroom_details(request,pk):
    classroom=Classroom.objects.get(id=pk)
    print(classroom)
    assignments=Assignment.objects.filter(classroom=pk).order_by('-date_uploaded')
    context={'classroom':classroom,'assignments':assignments}
    return render(request,'group/classroom_detail.html',context)

@login_required
def ClassroomList(request):
    class1=Classroom.objects.filter(admin=request.user)
    class2=ClassMember.objects.filter(user=request.user)
    context={'class1':class1,'class2':class2}
    return render(request,'group/classroom_list.html',context)

@login_required
def join_class(request):
    if request.method == 'POST':
        j_form=JoinClassForm(request.POST)
        if j_form.is_valid():
            code=j_form.cleaned_data.get('code')
            class3=Classroom.objects.filter(code=code).exists()
            if class3 is True:
                    room=Classroom.objects.filter(code=code).first()
                    check=ClassMember.objects.filter(classroom=room,user=request.user).first()
                    
                    if check is None:
                        ClassMember.objects.create(classroom=room,user=request.user)
                        messages.success(request,'Successfully added')
                        if request.user.profile.designation == 'TEACHER':
                            return redirect('group:teacher_dashboard')
                        else:
                            return redirect('group:student_dashboard')
                    else:                
                        messages.warning(request,'Already a member')
                        if request.user.profile.designation == 'TEACHER':
                            return redirect('group:teacher_dashboard')
                        else:
                            return redirect('group:student_dashboard')
            else:
                messages.warning(request,'Classroom not present')
                if request.user.profile.designation == 'TEACHER':
                    return redirect('group:teacher_dashboard')
                else:
                    return redirect('group:student_dashboard')
    else:
        j_form=JoinClassForm()
        context={'j_form':j_form}
    return render(request,'group/join_class.html',context)

@login_required
def leave_classroom(request,pk):
    obj=get_object_or_404(ClassMember,classroom=pk,user=request.user)
    obj.delete()
    messages.success(request,"Your membership has been successfully deleted")
    if request.user.profile.designation == 'TEACHER':
        return redirect('group:teacher_dashboard')
    else:
        return redirect('group:student_dashboard')
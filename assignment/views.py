from django.shortcuts import render,redirect
from assignment.forms import AssignmentForm,AssignmentUpdateForm,SubmissionForm
from group.models import Classroom
from assignment.models import Assignment,Submission
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic  
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ams.decorators import allowed_users
# Create your views here.

@login_required
@allowed_users(allowed_roles=['TEACHERS'])
def upload(request,pk):
    if request.method=='POST':
        a_form=AssignmentForm(request.POST,request.FILES)
        cl=Classroom.objects.get(id=pk)
        a_form.instance.classroom=cl
        a_form.instance.uploader=request.user
        if a_form.is_valid():
            a_form2=a_form.save(commit=False)
            if 'file' in request.FILES:
                a_form2.file=request.FILES['file']
            a_form2.save()
            messages.success(request,"Uploaded successfully")
            return HttpResponseRedirect(reverse('group:classroom_details', kwargs={'pk':pk}))
        else:
            messages.warning(request,"Not Uploaded")
            return redirect('group:teacher_dashboard')
    else:
        a_form=AssignmentForm()
        context={'a_form':a_form}
    return render(request,'assignment/assignment_upload.html',context)

@login_required
def assignment_details(request,pk):
    assignment=Assignment.objects.get(id=pk)
    submit_1=Submission.objects.filter(assignment=assignment)
    submit_2=Submission.objects.filter(assignment=assignment,student=request.user).first()
    context={'assignment':assignment,'submit_1':submit_1,'submit_2':submit_2}
    return render(request,'assignment/assignment_detail.html',context)

@login_required
@allowed_users(allowed_roles=['TEACHERS'])
def assignment_edit(request,pk):
    if request.method=='POST':
        assign=Assignment.objects.get(id=pk)
        a_form=AssignmentUpdateForm(request.POST,request.FILES,instance=assign)
        if a_form.is_valid():
            a_form.save()
            messages.success(request,'Successfully updated')
            return redirect('group:teacher_dashboard')
    else:
        assign=Assignment.objects.get(id=pk)
        a_form=AssignmentUpdateForm(instance=assign)
        context={'a_form':a_form}
    return render(request,'assignment/assignment_update.html',context)

@method_decorator(allowed_users(allowed_roles=['TEACHERS']), name='dispatch')
class DeleteAssignment(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,generic.DeleteView):
    model=Assignment
    success_url=reverse_lazy('group:teacher_dashboard')
    success_message="Deleted Successfully"

    def test_func(self):
        assignment=self.get_object()
        if self.request.user == assignment.uploader:
            return True
        return False

@login_required
def submission_upload(request,pk):
    if request.method=='POST':
        s_form=SubmissionForm(request.POST,request.FILES)
        assign=Assignment.objects.get(id=pk)
        s_form.instance.assignment=assign
        s_form.instance.student=request.user
        if s_form.is_valid():
            s_form2=s_form.save(commit=False)
            if 'file' in request.FILES:
                s_form2.file=request.FILES['file']
            s_form2.save()
            messages.success(request,"Uploaded successfully")
            if request.user.profile.designation == 'TEACHER':
                return redirect('group:teacher_dashboard')
            else:
                return redirect('group:student_dashboard')
        else:
            messages.warning(request,"Not Uploaded")
            if request.user.profile.designation == 'TEACHER':
                return redirect('group:teacher_dashboard')
            else:
                return redirect('group:student_dashboard')
    else:
        s_form=SubmissionForm()
        context={'form':s_form}
    return render(request,'assignment/submission_form.html',context)

@method_decorator(allowed_users(allowed_roles=['TEACHERS']), name='dispatch')
class TeacherRemark(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):
    model=Submission
    fields=('remark',)
    success_url=reverse_lazy('group:classroom_list')
    success_message="Updated Successfully"

@method_decorator(allowed_users(allowed_roles=['STUDENTS']), name='dispatch')
class StudentEdit(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):
    model=Submission
    fields=('file',)
    success_url=reverse_lazy('group:classroom_list')
    success_message="Updated Successfully"

@method_decorator(allowed_users(allowed_roles=['STUDENTS']), name='dispatch')
class DeleteSubmission(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,generic.DeleteView):
    model=Submission
    success_url=reverse_lazy('group:classroom_list')
    success_message="Updated Successfully"

    def test_func(self):
        submission=self.get_object()
        if self.request.user == submission.student:
            return True
        return False


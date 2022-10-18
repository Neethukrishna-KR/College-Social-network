from django import forms
from assignment.models import Assignment,Submission

class DateInput(forms.DateInput):
     input_type = 'date'

class AssignmentForm(forms.ModelForm):
    name=forms.CharField()
    message=forms.CharField()
    file=forms.FileField()
    date_submission=forms.DateField(widget=DateInput)
    class Meta:
        model=Assignment
        fields=('name','message','file','date_submission')
        widgets = {'date_submission':DateInput()}

class AssignmentUpdateForm(forms.ModelForm):
    name=forms.CharField()
    message=forms.CharField()
    file=forms.FileField()
    date_submission=forms.DateField(widget=DateInput)
    class Meta:
        model=Assignment
        fields=('name','message','file','date_submission')
        widgets = {'date_submission':DateInput()}

class SubmissionForm(forms.ModelForm):
    file=forms.FileField()
    class Meta:
        model=Submission
        fields=('file',)
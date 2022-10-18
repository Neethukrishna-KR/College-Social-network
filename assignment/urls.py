from django.urls import path
from assignment import views
app_name='assignment'

urlpatterns = [
    path('upload/<int:pk>/',views.upload,name='upload'),
    path('assignment_details/<int:pk>/',views.assignment_details,name='assignment_details'),
    path('assignment_edit/<int:pk>/',views.assignment_edit,name='assignment_edit'),
    path('assignment_delete/<int:pk>/',views.DeleteAssignment.as_view(),name='assignment_delete'),
    path('add_remark/<int:pk>/',views.TeacherRemark.as_view(),name='teacher_remark'),
    path('edit_file/<int:pk>/',views.StudentEdit.as_view(),name='edit_file'),
    path('upload_submission/<int:pk>/',views.submission_upload,name='upload_submission'),
    path('delete_file/<int:pk>/',views.DeleteSubmission.as_view(),name='delete_file'),
]
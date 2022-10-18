from django.urls import path
from . import views
app_name='group'

urlpatterns = [
    path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('classroom_create/',views.CreateClassroom.as_view(),name='create_classroom'),
    path('classroom_list/',views.ClassroomList,name='classroom_list'),
    path('classroom_details/<int:pk>/',views.classroom_details,name='classroom_details'),
    path('classroom_update/<int:pk>/',views.UpdateClassroom.as_view(),name='update_classroom'),
    path('classroom_delete/<int:pk>/',views.DeleteClassroom.as_view(),name='delete_classroom'),
    path('join_class/',views.join_class,name='join_classroom'),
    path('leave_classroom/<int:pk>/',views.leave_classroom,name='leave_classroom'),

]
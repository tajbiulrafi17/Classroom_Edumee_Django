from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('login/teacher/', views.TeacherLogin.as_view(), name='teacher_login'),
    path('login/student/', views.StudentLogin.as_view(), name='student_login'),

    path('register/teacher/', views.TeacherRegister.as_view(), name='teacher_register'),
    path('register/student/', views.StudentRegister.as_view(), name='student_register'),
    
    path('teacher/', views.TeacherDashboard.as_view(), name='t_dash'),
    path('student/', views.StudentDashboard.as_view(), name='s_dash'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

]
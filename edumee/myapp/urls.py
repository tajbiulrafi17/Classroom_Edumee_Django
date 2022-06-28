from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #path('', views.index, name="index"),
    path('', views.indexV2, name="index"),
    
    path('login/teacher/', views.TeacherLogin.as_view(), name='teacher_login'),
    path('login/student/', views.StudentLogin.as_view(), name='student_login'),

    path('register/teacher/', views.TeacherRegister.as_view(), name='teacher_register'),
    path('register/student/', views.StudentRegister.as_view(), name='student_register'),
    
    path('teacher/', views.TeacherDashboard.as_view(), name='t_dash'),
    path('student/', views.StudentDashboard.as_view(), name='s_dash'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('activate_user/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', 
            views.activate_user, name='activate'),

    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()),
            name='validate-email')

]
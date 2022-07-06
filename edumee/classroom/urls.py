
from django.urls import path
from . import views

urlpatterns =[
    path('class/<int:id>/', views.ClassDashboard.as_view(), name='class_dash'),
    path('create_class/', views.CreateClass.as_view(), name='create_class'),
    path('join_class/', views.JoinClass.as_view(), name='join_class'),
]
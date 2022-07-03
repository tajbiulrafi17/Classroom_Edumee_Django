
from django.urls import path
from . import views

urlpatterns =[
    path('class/<int:id>/', views.ClassDashboard.as_view(), name='class_dash')
]
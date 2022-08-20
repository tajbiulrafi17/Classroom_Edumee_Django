

from django.urls import path
from . import views

urlpatterns =[
    path('class/<int:id>/', views.ClassDashboard.as_view(), name='class_dash'),
    path('create_class/', views.CreateClass.as_view(), name='create_class'),
    path('join_class/', views.JoinClass.as_view(), name='join_class'),
    path('leave_class/<int:id>', views.LeaveClass.as_view(), name='leave_class'),
    path('delete_class/<int:id>/', views.DeleteClass.as_view(), name="delete_class"),
    path('invite_class/<int:id>', views.InviteClass.as_view(), name="invite_class"),
    path('<int:id>/people/', views.RoomPeople.as_view(), name='people'),
    
    path('add_material/<int:id>/', views.AddMaterial.as_view(), name='add_material'),
    path('<int:id>/material/', views.view_materials, name='material'),

    path('<int:id>/assignment/', views.view_assignments, name='assignment'),
    path('add_assignment/<int:id>/', views.AddAssignment.as_view(), name='add_assignment'),

    path('<int:id>/assignment_submissions/', views.view_assignmentSubmissions, name='assignment_submissions'),
    path('<int:id>/submission_assignment/', views.AssignmentSubmission.as_view(), name='submit_assignment'),

    path('addmark_assignment/<int:id>/', views.AddMarkAssignment.as_view(), name='addmark_assignment'),
    path('<int:id>/assignment_marks/', views.view_assignmentMarks, name='assignment_marks'),

    path('<int:id>/announcement/', views.view_announcements, name='announcement'),
    path('add_announcement/<int:id>/', views.AddAnnouncement.as_view(), name='add_announcement'),

    path('discussions/<int:id>/', views.discussions, name='discussions'),

    path('<int:id>/pdf/', views.show_pdf, name='pdfview'),




]
from django.contrib import admin
from .models import Classroom, Membership, Notification, Announcement, StudyMaterials,Message, DiscussionRoom, Assignment, SubmissionAssignment, Notification

# Register your models here.

admin.site.register(Classroom)
admin.site.register(Membership)
admin.site.register(StudyMaterials)
admin.site.register(Assignment)
admin.site.register(SubmissionAssignment)
admin.site.register(Notification)
admin.site.register(DiscussionRoom)
admin.site.register(Message)
admin.site.register(Announcement)
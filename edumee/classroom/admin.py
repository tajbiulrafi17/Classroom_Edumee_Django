from django.contrib import admin
from .models import Classroom, Membership, Notification, StudyMaterials, Assignment, SubmissionAssignment, Notification

# Register your models here.

admin.site.register(Classroom)
admin.site.register(Membership)
admin.site.register(StudyMaterials)
admin.site.register(Assignment)
admin.site.register(SubmissionAssignment)
admin.site.register(Notification)

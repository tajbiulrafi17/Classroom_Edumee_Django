import datetime
from django.db import models
from myapp.models import Teacher, Student, User
from .utils import unique_code_generate
from django.db.models.signals import pre_save

# Create your models here.

class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class Classroom(Time):
    name = models.CharField(max_length=50, blank=False, null=True, unique=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    details = models.TextField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='t_room')
    student = models.ManyToManyField(Student, through='Membership', related_name='s_room')

    def __str__(self):
        return self.name

def make_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = unique_code_generate(instance)

pre_save.connect(make_code, sender=Classroom)    


class Membership(models.Model):
    room = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    is_join = models.BooleanField(default=False)

    def __str__(self):
        return f"{ self.room } | { self.student }"


class StudyMaterials(models.Model):
    title = models.CharField(max_length=100)
    file_resource = models.FileField(upload_to='files/', null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='class_material')
    time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    name = models.CharField(max_length=1000)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files/', null=True)
    total_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    post_time = models.DateTimeField(auto_now_add = True)
    due_time = models.DateTimeField()

class SubmissionAssignment(models.Model):
    file = models.FileField(upload_to='files/', null=True)
    get_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    time = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{ self.assignment.course } |{ self.assignment.name } | { self.user }"


class Announcement(models.Model):
    title = models.CharField(max_length=150)
    details = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    

class Notification(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    material = models.ForeignKey(StudyMaterials, on_delete=models.CASCADE, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True)


class DiscussionRoom(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)

class Message(models.Model):
    room = models.ForeignKey(DiscussionRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('time',)






from django.db import models
from myapp.models import Teacher, Student
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
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='room')
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


def make_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = unique_code_generate(instance)

pre_save.connect(make_code, sender=Classroom)    
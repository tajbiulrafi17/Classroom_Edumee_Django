from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_("An email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __self__(self):
        return self.email



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='teachers')
    name = models.CharField(max_length=100, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to = 'user/', default ='profile-icon.png')
    
    def __str__(self):
        # return f"{self.user}"
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='students')
    name = models.CharField(max_length=100, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to = 'user/', default = 'profile-icon.png')
    
    def __str__(self):
        #return f"{self.user}"
        return self.name
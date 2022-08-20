from unicodedata import name
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.contrib.auth.base_user import BaseUserManager

from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


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
    name = models.CharField(max_length=100, null=True, default="default")
    photo = models.ImageField(null=True, blank=True, upload_to = 'images/user/', default ='images/profile-icon.png')

    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)

    def __self__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='teachers')
    name = models.CharField(max_length=100, null=True, default="default")
    photo = models.ImageField(null=True, blank=True, upload_to = 'images/user/', default ='images/profile-icon.png')
    
    
    def __str__(self):
        # return f"{self.user}"
        return self.user.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='students')
    name = models.CharField(max_length=100, null=True, default="default")
    photo = models.ImageField(null=True, blank=True, upload_to = 'images/user/', default ='images/profile-icon.png')
    
    def __str__(self):
        #return f"{self.user}"
        return self.user.name

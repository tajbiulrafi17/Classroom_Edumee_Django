
from rest_framework import serializers
from myapp.models import Student, Teacher, User




# class TeacherSignupSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model=Teacher
#         fields=['name']
#         user=Teacher
         
      

# class UserSerializer(serializers.ModelSerializer):
    
#     Teacher=TeacherSignupSerializer()
#     password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
#     class Meta:
#         model=User
#         fields=['email','password', 'password2', 'Teacher']
#         extra_kwargs={
#             'password':{'write_only':True}
#         }
    
#     def create(self, validated_data):
#         t_data=validated_data.pop('Teacher')
#         user=User(
#             email=self.validated_data['email']
#         )
        
#         password=self.validated_data['password']
#         password2=self.validated_data['password2']
#         if password != password2:
#             raise serializers.ValidationError({"error":"Password did not match"})
#         user.set_password(password)
#         user.is_teacher=True
#         user.save()
#         for name in t_data:
#             Teacher.objects.create(user=user, name=name)
#         return user

    




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email', 'name', 'is_teacher', 'is_student']
    

class TeacherSignupSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['email', 'name', 'password', 'confirm_password']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            email=self.validated_data['email'],
            name=self.validated_data['name']
        )
        
        password=self.validated_data['password']
        password2=self.validated_data['confirm_password']
        if password != password2:
            raise serializers.ValidationError({"error":"Password did not match"})
        user.set_password(password)
        user.is_email_verified=True
        user.is_teacher=True
        user.save()
        Teacher.objects.create(user=user)
        return user

class StudentSignupSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['email', 'name', 'password', 'confirm_password']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            email=self.validated_data['email'],
            name=self.validated_data['name']
        )
        password=self.validated_data['password']
        password2=self.validated_data['confirm_password']
        if password != password2:
            raise serializers.ValidationError({"error":"Password did not match"})
        user.set_password(password)
        user.is_email_verified=True
        user.is_student=True
        user.save()
        Student.objects.create(user=user)
        return user
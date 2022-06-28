from audioop import reverse
from curses.ascii import US
import threading
from django import views
from django.shortcuts import render, redirect
from django.views import View
from .models import Student, Teacher, User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings 
import json
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'myapp/index.html')

def indexV2(request):
    return render(request, 'myapp/index_v2.html')


# Email verification functions and Email Thread
class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send( )
        
        

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('myapp/activate_email.html',{
        'user':user,
        'domain':request.get_host(),
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, 
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email]
                    )
    EmailThread(email).start()



def activate_user(request, uidb64, token):

    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except Exception as e:
        user = None
    
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 
                            'Email verified, you can login now.')
        return redirect('index')

    messages.add_message(request, messages.SUCCESS, 
                            'Link Expired!')
    return render(request, 'myapp/activate_failed.html', {"user":user})

      
#
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        # if not str(email).isalnum():
        #     return JsonResponse({'email_error':'USername should only contain alphaneumeric character'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email already used! Try another one or Login.'}, status=400)
        return JsonResponse({'email_valid': True})



#Register View
class TeacherRegister(View):
    def get(self,reqeust,*args,**kwargs):
        # is_teacher = Teacher.objects.filter(is_teacher= True)
        # if reqeust.user.is_authenticated and is_teacher:
        #     return redirect('t_dash')
        context ={

        }
        return render(reqeust,'myapp/t_register_ajax.html',context)
    
    def post(self,request,*args,**kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mail_check = User.objects.filter(email = email)
        if mail_check:
            messages.warning(request,'Already have an account. Please login!')
            return redirect('teacher_register')
        elif password1 != password2:
            messages.warning(request,'Sorry! Password didnot match.')
            return redirect('teacher_register')
        elif len(password1) < 5:
            messages.warning(request,'Password too short! Atleast 5 character nedeed.')
            return redirect('teacher_register')
        else:
            auth_info ={
                'email':email,
                'password':make_password(password1)
            }
            
            user = User(**auth_info)
            
            user.is_teacher = True
            user.save()
        user_obj = Teacher(user=user, name=name)
        user_obj.save()
        send_activation_email(user, request)
        messages.success(request, 'Thanks for Signup ! Activate your account from your gmail.')
        return redirect ('index')




class StudentRegister(View):
    def get(self,request,*args,**kwargs):
        # is_student = Student.objects.filter(is_student=True)
        # if request.user.is_authenticated and is_student:
        #     return redirect('s_dash')
        context ={
            
        }
        return render(request,'myapp/s_register_ajax.html',context)

    def post(self,request,*args,**kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        photo = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mail_check = User.objects.filter(email=email)
        if mail_check:
            messages.warning(request,'Already have an account. Please login!')
            return redirect('teacher_register')
        elif password1 != password2:
            messages.warning(request,'Sorry! Password didnot match.')
            return redirect('teacher_register')
        elif len(password1) < 5:
            messages.warning(request,'Password too short! Atleast 5 character nedeed.')
            return redirect('teacher_register')
        else:
            auth_info ={
                'email':email,
                'password':make_password(password1)
            }
            
            user = User(**auth_info)
            
            user.is_student = True
            user.save()
            user_obj = Student(user=user, name=name, photo=photo)
            user_obj.save()
        send_activation_email(user, request)
        messages.success(request,'Thanks for Signup! Activate your account from your gmail.')
        return redirect ('index')
    

#Login View
class TeacherLogin(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return redirect('')
        return render(request, 'myapp/t_login.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username = email, password=password)

        email_check = User.objects.filter(email = email)

        if not email_check :
                messages.warning(request, 'User Not found. Please Signup!!')
                return redirect('teacher_register')

        elif user is not None :
            check_teacher = User.objects.get(email = user)

            if check_teacher.is_email_verified == False:
                messages.warning(request, 'Email not verified. Please check email inbox')
                return redirect('index')

            if check_teacher.is_teacher == True:
                login(request, user)
                return redirect('t_dash')

            elif check_teacher.is_student == False:
                messages.warning(request, 'You are an Admin. Login from Admin Panel!')
                return redirect('index')
            else:
                messages.warning(request, 'You are not a Teacher. Please Login as a Student!')
                return redirect('index')
        else:
            messages.warning(request, 'Wrong Password!!')
            return redirect('index')


class StudentLogin(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return redirect('')
        return render(request, 'myapp/s_login.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        email_check = User.objects.filter(email = email)
        
        if not email_check:
                messages.warning(request, 'User Not found. Please Signup!!')
                return redirect('student_register')
       
        elif user is not None:           
            check_student = User.objects.get(email = user)

            if check_student.is_email_verified == False:
                messages.warning(request, 'Email not verified. Please check email inbox')
                return redirect('index')

            if check_student.is_student == True:
                login(request, user)
                return redirect('s_dash')
            elif check_student.is_teacher == False:
                messages.warning(request, 'You are an Admin. Login from Admin Panel!')
                return redirect('index')
            else:
                messages.warning(request, 'You are not a Student. Please Login as a Teacher!')
                return redirect('index')
        else:
            messages.warning(request, 'Wrong Password!!')
            return redirect('index')

#Logout View 
class LogoutView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('/')


#Dashboard View

class TeacherDashboard(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        user = request.user.teachers
        return render(request,'myapp/t_dashboard.html')

class StudentDashboard(View):
    @method_decorator(login_required(login_url='student_login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        user = request.user.students
        return render(request,'myapp/s_dashboard.html')   
    

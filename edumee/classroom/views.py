import imp
from json import load
from operator import methodcaller
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Classroom, Membership
from django.contrib import messages
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

class ClassDashboard(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request, id):
        room = get_object_or_404(Classroom, id=id)
        context = {
            'room':room,
        }
        return render(request, 'classroom/class_dashboard.html', context)

class CreateClass(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        name = request.POST.get('name')
        details = request.POST.get('details')
        name_check = Classroom.objects.filter(name = name)
        if name_check:
            messages.warning(request, 'Sorry! Class with this name exists. Try another name.')
            return redirect('create_class')
        user = request.user.teachers
        room = Classroom(teacher=user, name=name, details=details)
        room.save()
        messages.success(request, 'Classroom has been Created !!')
        return redirect('class_dash', id=room.id)

class JoinClass(View):
    @method_decorator(login_required(login_url='student_join'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        code = request.POST.get('code')
        try:
            check_code = Classroom.objects.get(code= code)
            user = request.user.students
            classroom = Classroom(id = check_code.id)
            check = Membership.objects.filter(room=classroom, student=user)
            if check:
                messages.success(request,'You are Already a member')
                return redirect('s_dash') 
            else:
                member = Membership(room=classroom, student = user)
                member.is_join = True
                member.save()
                messages.success(request,'Welcome to The Class!')
                return redirect('class_dash', id=check_code.id)



        except:
            messages.warning(request, "No class found! Check Class code and try again.")
            return redirect('s_dash')


class LeaveClass(View):
    @method_decorator(login_required(login_url='student_login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        password = request.POST.get('password')
        email = request.user.email
        check = authenticate(request, username=email, password=password)

        if check:
            user = request.user.students
            room = get_object_or_404(Classroom, id=id)
            membership = Membership.objects.filter(student=user, room=room)
            membership.delete()
            messages.warning(request, 'You left the Classroom')
            return redirect('s_dash')
        else:
            messages.warning(request, 'Verification failed! Could not leave.')
            return redirect('view_class', id=id)


class DeleteClass(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        password = request.POST.get('password')
        email = request.user.email
        check = authenticate(request, username=email, password=password)
        if check:
            room = get_object_or_404(Classroom, id=id)
            room.delete()
            messages.warning(request, 'You deleted the Classroom')
            return redirect('t_dash')
        else:
            messages.warning(request, 'Verification failed! Could not delete.')
            return redirect('view_class', id=id)


class InviteClass(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        try: 
            room = get_object_or_404(Classroom, id=id)
            send_to = request.POST.get('email')
            subject = 'Edumee Classroom Invitation'
            message = f'Hi Student, Greetings!!\nPlease join into class {room.name}, using class code: {room.code}.\nYour Teacher: {room.teacher}\n\nThank you,\nEdumee.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [send_to]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'Invitation successful!')
            return redirect('class_dash', id=id)
        except:
            messages.warning(request, 'Something wrong! Invitation failed!')
            return redirect('class_dash', id=id)
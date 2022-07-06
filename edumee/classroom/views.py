import imp
from operator import methodcaller
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Classroom
from django.contrib import messages

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
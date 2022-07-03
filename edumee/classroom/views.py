from django.shortcuts import get_object_or_404, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Classroom

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

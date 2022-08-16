
from datetime import datetime
from json import load
from operator import methodcaller
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Assignment, Classroom, Membership, Notification, StudyMaterials, SubmissionAssignment
from django.contrib import messages
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail
import re
from django.http import FileResponse
import os
 



# Create your views here.

class ClassDashboard(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request, id):
        room = get_object_or_404(Classroom, id=id)
        notification = Notification.objects.filter(course=room)
        now = datetime.now()
        context = {
            'room':room,
            'notification':notification,
            'now':now
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
            recipient_list = re.split(" , | ,|, |,| ", send_to)
            subject = 'Edumee Classroom Invitation'
            message = f'Hi Student, Greetings!!\nPlease join into class {room.name}, using class code: {room.code}.\nYour Teacher: {room.teacher}\n\nThank you,\nEdumee.'
            email_from = settings.EMAIL_HOST_USER
            
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'Invitation successful!')
            return redirect('class_dash', id=id)
        except:
            messages.warning(request, 'Something wrong! Invitation failed!')
            return redirect('class_dash', id=id)


class RoomPeople(View):
    @method_decorator(login_required(login_url='student_login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        room = get_object_or_404(Classroom, id=id)
        students = room.student.all().order_by('name')
        teacher = room.teacher
        context = {
            't':teacher,
            'room': room,
            's': students
        }
        return render(request, 'classroom/class_people.html', context)

class AddMaterial(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, id):
        title = request.POST.get('title')
        file = request.FILES.get('file')
        room = get_object_or_404(Classroom, id=id)
        material = StudyMaterials(title=title, file_resource=file, classroom=room)
        material.save()
        noti = Notification()
        noti.title = " - New Material Uploaded - "
        noti.material = material
        noti.course = room
        noti.save()
        messages.success(request, 'Study Material added !!')
        return redirect('material', id=room.id)




@login_required
def view_materials(request, id):
    classroom = Classroom.objects.get(id=id)
    materials = StudyMaterials.objects.filter(classroom=classroom)
    context = {
        'room' : classroom,
        'materials' : materials,
    }
    return render(request,'classroom/class_material.html',context)


class AddAssignment(View):
    @method_decorator(login_required(login_url='teacher_login'))
    def dispatch(self,request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, id):
        title = request.POST.get('title')
        file = request.FILES.get('file')
        due = request.POST.get('due')
        mark = request.POST.get('mark')
        room = get_object_or_404(Classroom, id=id)
        assignment = Assignment(name=title, file=file, course=room, due_time=due, total_mark=mark)
        assignment.save()
        noti = Notification()
        noti.title = " - New Assignment Uploaded - "
        noti.assignment = assignment
        noti.course = room
        noti.save()
        messages.success(request, 'Assignment added !!')
        return redirect('assignment', id=room.id)



@login_required
def view_assignments(request, id):
    classroom = Classroom.objects.get(id=id)
    assignments = Assignment.objects.filter(course=classroom)
    now = datetime.now()
    context = {
        'room' : classroom,
        'assignments' : assignments,
        'now':now
    }
    return render(request,'classroom/class_assignment.html',context)


# for modal
# class AssignmentSubmission(View):
#     @method_decorator(login_required(login_url='teacher_login'))
#     def dispatch(self,request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self,request, id):
#         file = request.FILES.get('file')
#         assignment = Assignment.objects.get(id=id)
#         course_id = assignment.course.id
#         room = Classroom.objects.get(id=course_id)
#         user = request.user.students
#         room = assignment.course
#         submission = SubmissionAssignment( file=file, user=user , assignment=assignment)
#         submission.save()
#         messages.success(request, 'Submit Successful !!')
        
#         return redirect('assignment', id=room.id)

class AssignmentSubmission(View):
    
    def get(self, request, id):
        assignment = Assignment.objects.get(id=id)
        course_id = assignment.course.id
        room = Classroom.objects.get(id=course_id)
        context={
            'assignment':assignment,
            'room':room
        }
        return render(request, 'classroom/upload_submission.html', context)

    def post(self,request, id):
        file = request.FILES.get('file')
        assignment = Assignment.objects.get(id=id)
        course_id = assignment.course.id
        room = Classroom.objects.get(id=course_id)
        user = request.user.students
        room = assignment.course
        submission = SubmissionAssignment( file=file, user=user , assignment=assignment)
        submission.save()
        messages.success(request, 'Submit Successful !!')
        
        return redirect('assignment', id=room.id)

@login_required
def view_assignmentSubmissions(request, id):
    assignment = Assignment.objects.get(id=id)
    submissions = SubmissionAssignment.objects.filter(assignment=assignment)
    course_id = assignment.course.id
    room = Classroom.objects.get(id=course_id)
    context = {
        'assignment' : assignment,
        'submissions' : submissions,
        'room': room
    }
    return render(request,'classroom/view_submissions.html',context)

# for modal
# class AddMarkAssignment(View):
#     @method_decorator(login_required(login_url='teacher_login'))
#     def dispatch(self,request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self,request, id):
#         mark = request.POST.get('mark')
#         submission = get_object_or_404(SubmissionAssignment, id=id)
#         submission.get_mark = mark
#         submission.save()
#         assignment_id = submission.assignment.id
#         assignment = Assignment.objects.filter(id=assignment_id)
#         messages.success(request, 'Mark Assigned !!')
#         return redirect('assignment_submissions', id=assignment_id)

class AddMarkAssignment(View):

    def get(self, request, id):
        submission = SubmissionAssignment.objects.get(id=id)
        assignment= submission.assignment
        user = submission.user
        course_id = assignment.course.id
        room = Classroom.objects.get(id=course_id)
        context={
            'submission':submission,
            'assignment':assignment,
            'user':user,
            'room':room
        }
        return render(request, 'classroom/assign_mark.html', context)

    def post(self,request, id):
        mark = request.POST.get('mark')
        submission = get_object_or_404(SubmissionAssignment, id=id)
        submission.get_mark = mark
        submission.save()
        assignment_id = submission.assignment.id
        messages.success(request, 'Mark Assigned !!')
        return redirect('assignment_submissions', id=assignment_id)


@login_required
def view_assignmentMarks(request, id):
    assignment = Assignment.objects.get(id=id)
    submissions = SubmissionAssignment.objects.filter(assignment=assignment)
    course_id = assignment.course.id
    room = Classroom.objects.get(id=course_id)
    context = {
        'assignment' : assignment,
        'submissions' : submissions,
        'room': room
    }
    return render(request,'classroom/view_assignment_marks.html',context)
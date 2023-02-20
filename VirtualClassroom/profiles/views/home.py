from django.shortcuts import redirect, render
from  django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login , logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# model import 
from VirtualClassroom.profiles.models import Student, Teacher, User
from VirtualClassroom.classroom.models import ClassRoom

# Class Index
class Index(View):
    def get(self, request,*args,**kwargs):
        # if request user is student
        if request.user.is_authenticated:
            if request.user.is_teacher:
                return redirect('teacher')
            else:
                return redirect('student')

        return render(request,'index2.html')
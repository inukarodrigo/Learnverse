from django.shortcuts import redirect, render
from  django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login , logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# model import
from profiles.models import Student, Teacher, User
from classroom.models import ClassRoom


class fileView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    def get(self,reqeust):
        user = reqeust.user.teachers
        context = {
            'room':user.room.all().order_by('-id'),
            'post':user.post.all()
        }
        return render(reqeust,'class/detail.html',context)
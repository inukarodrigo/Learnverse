import fnmatch
import os
import threading

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from vidstream import StreamingServer

from classroom.forms import PodcastForm
from classroom.models import ClassRoom, MemberShip, CoursePack
from profiles.models import Teacher, Student
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class start_session(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        room = get_object_or_404(ClassRoom, id=id)

        context = {
            'room': room
        }
        return render(request, 'class/share_screen.html', context)

    def display_video(request, vid=None):



        # getting full url -
        video_url = 'screen.mp4'

        return render(request, "class/share_screen.html", {"url": video_url})

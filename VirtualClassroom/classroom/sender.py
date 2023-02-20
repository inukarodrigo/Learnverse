import threading


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
import cv2
import numpy as np
from win32api import GetSystemMetrics
from PIL import ImageGrab

from VirtualClassroom.classroom.models import ClassRoom


class Set_screen(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        room = get_object_or_404(ClassRoom, id=id)
        context = {
            'room': room,
            'user': request.user,

        }

        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        file_name = f'screen.mp4'
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        captured_video = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))


        while True:
            img = ImageGrab.grab(bbox=(0, 0, width, height))
            img_np = np.array(img)
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            cv2.imshow('Secret Capture', img_final)
            captured_video.write(img_final)

            if cv2.waitKey(10) == ord('q'):
                break

        return render(request, 'class/share_screen.html', context)




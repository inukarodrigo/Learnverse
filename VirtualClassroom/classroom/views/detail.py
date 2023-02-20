from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages

from classroom.forms import PodcastForm
from classroom.models import ClassRoom, MemberShip, CoursePack, ClassFiles
from profiles.models import Teacher, Student
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg', 'mp4', 'pdf']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


# People under Class
class get_detail(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        all_data = ClassFiles.objects.all()
        room = get_object_or_404(ClassRoom, id=id)
        context = {
            'room': room,
            'user': request.user,
            'data': all_data

        }
        return render(request, 'class/detail.html', context)


"""def create_podcast(request, course_id):
    form = PodcastForm(request.POST or None, request.FILES or None)
    course = get_object_or_404(CoursePack, pk=course_id)
    if form.is_valid():
        courses_podcasts = course.podcast_set.all()
        for p in courses_podcasts:
            if p.material_title == form.cleaned_data.get("material_title"):
                context = {
                    'course': course,
                    'form': form,
                    'error_message': 'You already added that podcast',
                }
                return render(request, 'class/create_podcast.html', context)
        podcast = form.save(commit=False)
        podcast.course = course
        podcast.material_file = request.FILES['material_file']
        file_type = podcast.material_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'course': course,
                'form': form,
                'error_message': 'Podcast file must be MP4, MP3, or OGG',
            }
            return render(request, 'class/create_podcast.html', context)

        podcast.save()
        return render(request, 'class/detail.html', {'course': course})
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'class/create_podcast.html', context)
"""
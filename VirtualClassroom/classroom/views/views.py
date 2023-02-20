from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from ..forms import MyfileUploadForm
from ..models import file_upload
from ..functions import handle_uploaded_file
from ..forms import StudentForm
from ..models import RoomStream, ClassRoom, ClassFiles


"""def addNew(request):
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)


        print(form.as_p)

        if form.is_valid():
            name = request.POST.get('file_name')
            the_files = request.POST.get('files_data')
            teacher = request.user.teachers
            room = get_object_or_404(ClassRoom, id=id)

            ClassFiles(file_name=name, class_files=the_files,room=room,teacher=teacher).save()

            return HttpResponse("file upload")
        else:
            return HttpResponse('error')

    else:

        context = {
            'form':MyfileUploadForm()
        }

        return render(request, 'class/addnewfile.html', context)"""
"""def show_file(request):
    # this for testing
    all_data = ClassFiles.objects.all()

    context = {
        'data':all_data
        }

    return render(request, 'class/detail.html', context)"""

class CreateFile(View):
    method_decorator(login_required(login_url='login'))

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, id):
        room = get_object_or_404(ClassRoom, id=id)
        teacher=request.user.teachers
        name = request.POST.get('file_name')
        the_files = request.POST.get('files_data')
        class_files = ClassFiles(room=room,teacher=teacher,file_name=name, class_files=the_files)
        class_files.save()
        messages.success(request, 'The file has Been Added')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


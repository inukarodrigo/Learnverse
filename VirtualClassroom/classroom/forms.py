from django import forms
from django.contrib.auth.models import User

from .models import CoursePack, Podcast, Video


class CoursePackForm(forms.ModelForm):
    class Meta:
        model = CoursePack
        fields = ['instructor', 'course_title', 'course_code', 'thumbnail']


class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['material_title', 'material_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EvaluationForm(forms.Form):
    post = forms.CharField()


class StudentForm(forms.Form):
    firstname = forms.CharField(label="Enter first name", max_length=50)
    lastname = forms.CharField(label="Enter last name", max_length=10)
    email = forms.EmailField(label="Enter Email")
    file = forms.FileField()  # for creating file input


class MyfileUploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
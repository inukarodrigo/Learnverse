import random
import uuid
from django.db import models
from django.db.models.fields import TextField
from VirtualClassroom.profiles.models import Teacher, Student, User
from .utils import unique_code_generate
from django.db.models.signals import pre_save


class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

#ile upload
class file_upload(Time):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    file_name = models.CharField(max_length=255)
    class_files = models.FileField(upload_to='upload')

    def __str__(self):
        return self.file_name

# classroom model
class ClassRoom(Time):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=True)
    cover = models.ImageField(upload_to='others/cover/', default='others/class.jpg', null=True)
    unit = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=8, blank=True, null=True)  # random
    details = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='room')
    student = models.ManyToManyField(Student, through='MemberShip', related_name='s_room')
    #post = models.FileField(on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


def make_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = unique_code_generate(instance)


pre_save.connect(make_code, sender=ClassRoom)


# Group member
class MemberShip(models.Model):
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, related_name='classroom')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='members')
    is_join = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room} | {self.student}"


# class Files
class ClassFiles(Time):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)
    class_files = models.FileField( upload_to='upload/')
    file_name= models.CharField(max_length=255, null=True)


    def __str__(self):
        return f"{self.teacher} | {self.room} | {self.class_files}"

    class Meta:
        verbose_name_plural = 'Class Files'
        verbose_name = 'Class File'


# forum
class RoomStream(Time):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.TextField()
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room}|{self.user}|{self.post}|{self.is_featured}"


# Comment model of Stream
class Comment(Time):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stream = models.ForeignKey(RoomStream, on_delete=models.DO_NOTHING, null=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} commented on {self.stream}"


class CoursePack(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=250)
    course_title = models.CharField(max_length=500)
    course_code = models.CharField(max_length=100)
    thumbnail = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.course_title + ' - ' + self.instructor


class Podcast(models.Model):
    course = models.ForeignKey(CoursePack, on_delete=models.CASCADE)
    material_title = models.CharField(max_length=300)
    material_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.material_title


class Video(models.Model):
    course = models.ForeignKey(CoursePack, on_delete=models.CASCADE)
    video_title = models.CharField(max_length=300)
    video_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.video_title

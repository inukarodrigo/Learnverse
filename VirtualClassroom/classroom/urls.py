from django import views
from django.urls import path

import sender
from .views import detail
from .views.addFile import addNew
from .views.detail import get_detail
from .views import views
from .views.room import ViewClassRoom,SingleClass,CreateClassRoom,JoinRoom, LeaveClass, SendMail
from .views.people import PeopleUnderRoom
from .views.session import start_session
from .views.stream import CreateStream, CreateComment
from .views.views import CreateFile

urlpatterns =[
    path('',ViewClassRoom.as_view(),name='all_class'),
    path('view/<str:id>/',SingleClass.as_view(), name='single'),
    path('create/',CreateClassRoom.as_view(),name='create_class'),
    path('join/class/',JoinRoom.as_view(),name='join'),

    #path('<str:id>/detail/',get_detail.as_view(), name='detail'),
    path('<str:id>/detail/', get_detail.as_view(), name='detail'),
    path('<str:id>/addFile/', addNew.as_view(), name='addNew'),
    path('<str:id>/people/', PeopleUnderRoom.as_view(),name='people'),
    path('<str:id>/leave/', LeaveClass.as_view(), name='leave'),
    path('<str:id>/create/views',CreateFile.as_view(),name='file_create'),
    path('<str:id>/create/stream',CreateStream.as_view(),name='stream_create'),
    #path('stream/<str:id>/view/',SingleStream.as_view(),name='single_stream'),
    path('<str:id>/session/', start_session.as_view(),name='session'),
    path('<str:id>/sender/', sender.Set_screen.as_view(),name='send_screen'),
    #path('', views.addNew, name="home"),
    #path('view', views.show_file, name="view"),

    path('<str:id>/create/comment', CreateComment.as_view(),name='comment_create'),

    #send email route
    path('send/code/via/mail',SendMail.as_view(),name='send'),
]
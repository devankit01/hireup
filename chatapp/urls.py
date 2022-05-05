from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('chathome/',homechat,name="homechat"),
    path('index/user/<str:user>/',Chatroom,name="Chatroom"),
    path('chats/mychats',mychats,name="mychats"),
    path('chat/user/<str:user>',Userchats, name="Userchats")
]

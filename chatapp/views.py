from django.shortcuts import render
from concurrent.futures import thread
import imp
from django.http import HttpRequest
from django.shortcuts import render
from . models import *
from django.contrib.auth.models import User
import uuid
from django.db.models import Count
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
from django.core.mail import send_mail
from HireApp.models import RecruiterProfile
# Create your views here.


def homechat(request):
    recuiter=None
    if request.session.get('username', None):
        
        user = get_object_or_404(User, username=request.user)
        if RecruiterProfile.objects.filter(username=user).exists():
            recuiter=RecruiterProfile.objects.filter(username=user).first()
            print(recuiter.username.username)
    return render(request, 'chatapp/index.html',{'recuiter':recuiter})

def Chatroom(request,user):
    print(request.session)
    if request.session.get('username', None):
            
            user_main = get_object_or_404(User, username=request.user)
        # if RecruiterProfile.objects.filter(username=user_main).exists():
        #     recuiter=RecruiterProfile.objects.filter(username=user_main).first()
            user1=user_main
            print(user1)
            user2=User.objects.get(username=user)
            print("hua")
            threads=SplitThread(user1,user2)
            if threads:
                thread=Thread.objects.filter(name=threads.name).first()
                chats=Message.objects.filter(thread=thread)
                return render(request,"chatapp/index.html",{'chatuser':user,'chats':chats})
            else:
                us1=user1.id
                us2=user2.id
                UID = uuid.uuid4()
                id=str(us1)+str(UID)+str(us2)
                thread=Thread.objects.create(thread_type='personal',name=id)
                thread.users.add(user1.id)
                thread.users.add(user2.id)
                # return thread
                return render(request,"chatapp/index.html",{'chatuser':user})

def SplitThread(user1,user2):
    # try:
        threads=Thread.objects.filter(thread_type ='personal')
        print(user1.id,user2.id)
        threads=threads.filter(users__in=[user1.id,user2.id]).distinct()
        threads=threads.annotate(u_count=Count('users')).filter(u_count=2)
        user11en=len(str(user1.id))
        user2len=len(str(user2.id))
        for i in threads:
            print(i.name[:user11en],user1.id,"---------", i.name[-user2len:],user2.id)
            if (int(i.name[:user11en])==user1.id and int(i.name[-user2len:])==user2.id) or (int(i.name[:user11en])==user2.id and int(i.name[-user2len:])==user1.id):
                return i
    # except:
    #     return None
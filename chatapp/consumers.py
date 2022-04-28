import asyncio
import imp
from re import A
from chatapp.models import Message
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
from asgiref.sync import async_to_sync,sync_to_async
import json
from .models import *
from channels.db import database_sync_to_async
from . views import SplitThread
from django.contrib.auth.models import User

class MyChatConsumer(SyncConsumer):
    def websocket_connect(self,event):
        me=self.scope['user'].username
        self.other_username=self.scope['url_route']['kwargs']['username']
        print(me)
        me=User.objects.filter(username=me).first()
        print(me)
        other_user=User.objects.get(username=self.other_username)
        print(other_user)
        self.thread_obj=SplitThread(me,other_user)
        print(self.thread_obj.name,self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.thread_obj.name,self.channel_name)
        print("websocket is connected...")
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print("websocket is recieved a msg from client")
        print(self.other_username)
        self.store_msg(event['text'])
        async_to_sync(self.channel_layer.group_send)(self.thread_obj.name,{
                'type':'chat_message',
                'text':event['text']
            })
        print(event)
    def chat_message(self,event):
        print("event ...",event)
        self.send({
            'type':'websocket.send',
            'text':event['text']
        })
        
    def websocket_disconnect(self,event):
        print(event)
        print("websocket is disconnect")
        raise StopConsumer()

    def store_msg(self,event):
        print("event aaya")
        data=json.loads(event)
        me=self.scope['user'].username
        me=User.objects.get(username=me)
        print(data['msg'])
        Message.objects.create(
            thread=self.thread_obj,
            sender=me,
            text=data['msg']
        )
        
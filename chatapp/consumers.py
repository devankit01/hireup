import asyncio
from concurrent.futures import thread
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
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class MyChatConsumer(AsyncConsumer):
    @database_sync_to_async
    def thread_object(self,me,other_username):
        me=User.objects.filter(username=me).first()
        print(me)
        other_user=User.objects.get(username=other_username)
        print(other_user)
        thread_obj=SplitThread(me,other_user)
        print("group thread")
        print(thread_obj)
        return thread_obj.name
        
    
    async def websocket_connect(self,event):
        me=self.scope['user'].username
        self.other_username=self.scope['url_route']['kwargs']['username']
        
        self.thread_obj=await self.thread_object(me,self.other_username)
        print(self.thread_obj)
        await self.channel_layer.group_add(self.thread_obj,self.channel_name)
        print("websocket is connected...")
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print("websocket is recieved a msg from client")
        print(self.other_username)
        await self.store_msg(event['text'])
        await self.channel_layer.group_send(self.thread_obj,{
                'type':'chat_message',
                'text':event['text']
            })
        print(event)
    async def chat_message(self,event):
        print("event ...",event)
        await self.send({
            'type':'websocket.send',
            'text':event['text']
        })
        
    async def websocket_disconnect(self,event):
        print(event)
        print("websocket is disconnect")
        raise StopConsumer()
    # to create msg using sync to async function
    @database_sync_to_async
    def createMessage(self,thread_obj,me,data):
        me=User.objects.get(username=me)
        thread_objs=Thread.objects.filter(name=thread_obj).first()
        print(data['msg'])
        msg=Message.objects.create(
            thread=thread_objs,
            sender=me,
            text=data['msg']
        )
        return msg
    async def store_msg(self,event):
        print("event aaya")
        data=json.loads(event)
        me=self.scope['user'].username
        message=await self.createMessage(self.thread_obj,me,data)
        
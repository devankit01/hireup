from django.urls import path
from . import consumers


websocket_urlpatterns=[
    # path('ws/sc/<str:groupname>/',consumers.MySyncConsumer.as_asgi()),
    # path('ws/asc/',consumers.MyChatConsumer.as_asgi()),
    path('ws/user/sc/<str:username>/',consumers.MyChatConsumer.as_asgi()),
]
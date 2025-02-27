from django.urls import path
from .consumers import ChatConsumer 

websocket_urlpatterns = [
    #re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
    path('ws/chat/<str:room_number>/', ChatConsumer.as_asgi()),
]

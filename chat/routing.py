# chat/routing.py
from django.urls import path
from .consumers import ChatConsumer 
from .staff_dashboard_consumer import StaffDashboardConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_number>/', ChatConsumer.as_asgi()),
    path('ws/staff_dashboard/', StaffDashboardConsumer.as_asgi()),
]
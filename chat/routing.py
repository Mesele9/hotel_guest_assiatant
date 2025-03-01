from django.urls import path
from .consumers import ChatConsumer
from .staff_dashboard_consumer import StaffDashboardConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:session_id>/', ChatConsumer.as_asgi()),
    path('ws/staff_dashboard/', StaffDashboardConsumer.as_asgi()),
]
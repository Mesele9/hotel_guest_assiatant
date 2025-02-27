# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_number>/', views.chat_room, name='chat_room'),
    path('staff/chat/', views.staff_chat_dashboard, name='staff_chat_dashboard'),
    path('staff/chat/<str:room_number>/', views.staff_chat_room, name='staff_chat_room'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_number>/', views.chat_room, name='chat_room'),
    path('staff/chat/', views.staff_chat_dashboard, name='staff_chat_dashboard'),
    path('history/<int:session_id>/', views.chat_history, name='chat_history'),
    path('upload/', views.upload_file, name='upload_file'),
]
# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from common_user.decorators import public_view, role_required

@public_view
def chat_room(request, room_number):
    messages = ChatMessage.objects.filter(room_number=room_number).order_by('timestamp')
    return render(request, 'chat/chat_room.html', {'room_number': room_number, 'messages': messages})

@login_required
def staff_chat_dashboard(request):
    rooms_with_messages = ChatMessage.objects.values('room_number').distinct()
    rooms = [r['room_number'] for r in rooms_with_messages]
    return render(request, 'chat/staff_chat_dashboard.html', {'rooms': rooms})

@login_required
def staff_chat_room(request, room_number):
    messages = ChatMessage.objects.filter(room_number=room_number).order_by('timestamp')
    return render(request, 'chat/staff_chat_room.html', {'room_number': room_number, 'messages': messages})
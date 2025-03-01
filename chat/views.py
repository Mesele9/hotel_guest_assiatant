# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from common_user.decorators import public_view, role_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

@public_view
def chat_room(request, room_number):
    messages = ChatMessage.objects.filter(room_number=room_number).order_by('timestamp')
    return render(request, 'chat/chat_room.html', {'room_number': room_number, 'messages': messages})

@login_required
def staff_chat_dashboard(request):
    # Get distinct rooms active in last 30 minutes
    cutoff = timezone.now() - timedelta(minutes=30)
    active_rooms = ChatMessage.objects.filter(
        timestamp__gte=cutoff
    ).order_by('room_number').values_list('room_number', flat=True).distinct()
    return render(request, 'chat/staff_chat_dashboard.html', {'rooms': active_rooms})

@login_required
def chat_history(request, room_number):
    messages = ChatMessage.objects.filter(room_number=room_number).order_by('timestamp')
    data = [{'sender': msg.sender, 'message': msg.message} for msg in messages]
    return JsonResponse({'messages': data})
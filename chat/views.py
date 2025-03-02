from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.views.decorators.csrf import csrf_exempt

def get_active_session(room_number):
    active_sessions = ChatSession.objects.filter(
        room_number=room_number,
        status__in=['new', 'in_progress']
    ).order_by('-created_at')
    if active_sessions.exists():
        return active_sessions.first()
    return ChatSession.objects.create(room_number=room_number, status='new')

def chat_room(request, room_number):
    session = get_active_session(room_number)
    messages = session.messages.order_by('timestamp')
    return render(request, 'chat/chat_room.html', {
        'room_number': room_number,
        'session_id': session.id,
        'messages': messages
    })

@login_required
def staff_chat_dashboard(request):
    sessions = ChatSession.objects.filter(status__in=['new', 'in_progress']).order_by('-last_activity')
    return render(request, 'chat/staff_chat_dashboard.html', {'sessions': sessions})

@login_required
def chat_history(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    messages = session.messages.order_by('timestamp')
    data = [
        {'sender': msg.sender, 'message': msg.message, 'file_url': msg.file_url}
        for msg in messages
    ]
    return JsonResponse({'messages': data})

@csrf_exempt  # Exempted for simplicity; use CSRF tokens in production
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        if file.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)
        if file.size > 15 * 1024 * 1024:  # 15MB limit
            return JsonResponse({'error': 'File too large'}, status=400)
        file_name = default_storage.save(os.path.join('chat_files', file.name), ContentFile(file.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({'file_url': file_url})
    return JsonResponse({'error': 'No file uploaded'}, status=400)
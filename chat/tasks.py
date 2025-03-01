# chat/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import ChatSession

@shared_task
def close_inactive_sessions():
    timeout = timezone.now() - timedelta(minutes=10)
    inactive_sessions = ChatSession.objects.filter(
        status__in=['new', 'in_progress'],
        last_activity__lt=timeout
    )
    for session in inactive_sessions:
        session.status = 'closed'
        session.save()
        # Notify connected clients
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        channel_layer.group_send(
            f'session_{session.id}',
            {
                'type': 'session_closed',
                'session_id': session.id,
                'room_number': session.room_number
            }
        )
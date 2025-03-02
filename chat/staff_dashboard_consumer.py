from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import ChatSession, ChatMessage
from django.utils import timezone

class StaffDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('staff_dashboard', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('staff_dashboard', self.channel_name)
        if hasattr(self, 'session_group_name'):
            await self.channel_layer.group_discard(self.session_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'join_session':
            session_id = data['session_id']
            self.session_group_name = f'session_{session_id}'
            await self.channel_layer.group_add(self.session_group_name, self.channel_name)
            session = await database_sync_to_async(ChatSession.objects.get)(id=session_id)
            session.unread_count = 0
            await database_sync_to_async(session.save)()

        elif message_type == 'send_message':
            session_id = data['session_id']
            message = data['message']
            sender = data['sender']
            session = await database_sync_to_async(ChatSession.objects.get)(id=session_id)
            await database_sync_to_async(ChatMessage.objects.create)(
                session=session,
                message=message,
                sender=sender
            )
            session.last_activity = timezone.now()
            if session.status == 'new':
                session.status = 'in_progress'
            await database_sync_to_async(session.save)()
            await self.channel_layer.group_send(
                f'session_{session_id}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                    'session_id': str(session_id),
                    'room_number': session.room_number
                }
            )

        elif message_type == 'close_session':
            session_id = data['session_id']
            session = await database_sync_to_async(ChatSession.objects.get)(id=session_id)
            session.status = 'closed'
            await database_sync_to_async(session.save)()
            await self.channel_layer.group_send(
                f'session_{session_id}',
                {
                    'type': 'session_closed',
                    'session_id': str(session_id),
                    'room_number': session.room_number
                }
            )
            # Leave the session group to prevent further messages
            await self.channel_layer.group_discard(f'session_{session_id}', self.channel_name)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'session_id': event['session_id'],
            'room_number': event['room_number'],
            'message': event['message'],
            'file_url': event['file_url'],
            'sender': event['sender']
        }))

    async def session_closed(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_session(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_session',
            'session_id': event['session_id'],
            'room_number': event['room_number']
        }))

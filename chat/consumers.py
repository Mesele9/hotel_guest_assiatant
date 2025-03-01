from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import ChatSession, ChatMessage
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.session = await database_sync_to_async(ChatSession.objects.get)(id=self.session_id)
        self.session_group_name = f'session_{self.session_id}'
        await self.channel_layer.group_add(self.session_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.session_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        file_url = data.get('file_url', '')
        sender = data['sender']

        # Save message and update session
        msg = await database_sync_to_async(ChatMessage.objects.create)(
            session=self.session,
            message=message,
            file_url=file_url if file_url else None,
            sender=sender
        )
        self.session.last_activity = timezone.now()
        if sender == 'guest' and self.session.status == 'new':
            self.session.status = 'new'  # Remains 'new' until staff responds
            self.session.unread_count += 1
        await database_sync_to_async(self.session.save)()

        # Broadcast to session group (guest and staff viewing this session)
        await self.channel_layer.group_send(
            self.session_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'file_url': file_url,
                'sender': sender,
                'session_id': self.session_id,
                'room_number': self.session.room_number
            }
        )

        # Notify staff dashboard if message is from guest
        if sender == 'guest':
            await self.channel_layer.group_send(
                'staff_dashboard',
                {
                    'type': 'new_message',
                    'session_id': self.session_id,
                    'room_number': self.session.room_number,
                    'message': message,
                    'file_url': file_url,
                    'sender': sender
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
# chat/staff_dashboard_consumer.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
import json
from django.utils import timezone
from datetime import timedelta

class StaffDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('staff_dashboard', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('staff_dashboard', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        room = data['room']
        message = data['message']
        sender = data['sender']

        await self.save_message(room, message, sender)

        await self.channel_layer.group_send(
            f'chat_{room}',
            {
                'type': 'chat_message',
                'room': room,
                'message': message,
                'sender': sender
            }
        )

        await self.channel_layer.group_send(
            'staff_dashboard',
            {
                'type': 'chat_message',
                'room': room,
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        # Handle both messages and new room notifications
        if event.get('new_room'):
            await self.send(text_data=json.dumps({
                'type': 'new_room',
                'room': event['room']
            }))
        else:
            await self.send(text_data=json.dumps(event))

    async def new_active_room(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_room',
            'room': event['room']
        }))

    @database_sync_to_async
    def save_message(self, room, message, sender):
        # Similar cleanup logic as ChatConsumer
        last_msg = ChatMessage.objects.filter(
            room_number=room
        ).order_by('-timestamp').first()
        
        if last_msg:
            inactive_period = timezone.now() - last_msg.timestamp
            if inactive_period > timedelta(hours=2):
                ChatMessage.objects.filter(room_number=room).delete()
        
        return ChatMessage.objects.create(
            room_number=room,
            message=message,
            sender=sender
        )
# chat/staff_dashboard_consumer.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
import json

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

        # Save the message to the database
        await database_sync_to_async(ChatMessage.objects.create)(
            room_number=room,
            message=message,
            sender=sender
        )

        # Broadcast the message to the room's group
        await self.channel_layer.group_send(
            f'chat_{room}',
            {
                'type': 'chat_message',
                'room': room,
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'room': event['room'],
            'message': event['message'],
            'sender': event['sender']
        }))
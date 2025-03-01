# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import ChatMessage
from django.utils import timezone
from datetime import timedelta

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_number = self.scope['url_route']['kwargs']['room_number']
        self.room_group_name = f'chat_{self.room_number}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.notify_room_presence()

    async def notify_room_presence(self):
        """Notify staff dashboard about room activity"""
        if await self.is_new_active_room():
            await self.channel_layer.group_send(
                'staff_dashboard',
                {'type': 'new_active_room', 'room': self.room_number}
            )

    @database_sync_to_async
    def is_new_active_room(self):
        """Check if room was inactive for more than 30 minutes"""
        last_msg = ChatMessage.objects.filter(
            room_number=self.room_number
        ).order_by('-timestamp').first()
        
        if not last_msg:
            return True  # New room
        return (timezone.now() - last_msg.timestamp) > timedelta(minutes=30)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']

        # Save message and check room activity
        is_new = await self.save_message(message, sender)

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message, 'sender': sender}
        )

        # Notify staff dashboard
        await self.channel_layer.group_send(
            'staff_dashboard',
            {
                'type': 'chat_message',
                'room': self.room_number,
                'message': message,
                'sender': sender,
                'new_room': is_new
            }
        )

    @database_sync_to_async
    def save_message(self, message, sender):
        # Clean messages if room was inactive >2 hours
        last_msg = ChatMessage.objects.filter(
            room_number=self.room_number
        ).order_by('-timestamp').first()
        
        is_new = False
        if last_msg:
            inactive_period = timezone.now() - last_msg.timestamp
            if inactive_period > timedelta(hours=2):
                ChatMessage.objects.filter(room_number=self.room_number).delete()
                is_new = True
        else:
            is_new = True
            
        ChatMessage.objects.create(
            room_number=self.room_number,
            message=message,
            sender=sender
        )
        return is_new

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
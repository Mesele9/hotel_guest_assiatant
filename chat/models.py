# chat/models.py
from django.db import models

class ChatMessage(models.Model):
    room_number = models.CharField(max_length=10)
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('staff', 'Staff')])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender} from room {self.room_number}: {self.message}"
from django.db import models

class ChatSession(models.Model):
    room_number = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=[('new', 'New'), ('in_progress', 'In Progress'), ('closed', 'Closed')],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    unread_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Session for room {self.room_number} - {self.status}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField(blank=True)
    file_url = models.URLField(blank=True, null=True)
    sender = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('staff', 'Staff')])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} in session {self.session.id}: {self.message or 'File'}"
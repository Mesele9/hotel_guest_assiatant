# common_user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
        ROLE_CHOICES = [
                ('hr_staff', 'HR Staff'),
                ('store_staff', 'Store Staff'),
                ('reception', 'Reception Staff'),
                ('fb', 'F&B Staff'),
                ('admin', 'Admin'),
                ]
        role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class AccessLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=255)
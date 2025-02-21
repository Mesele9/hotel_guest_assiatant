from django.db import models
import os
from datetime import date

def upload_to(instance, filename):
    today = date.today()
    folder = f"{today.year}-{today.month:02d}-{today.day:02d}"
    return os.path.join('uploads', folder, filename)

class File(models.Model):
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class UploadedFile(models.Model):
    files = models.ManyToManyField(File)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uploaded files at {self.uploaded_at}"
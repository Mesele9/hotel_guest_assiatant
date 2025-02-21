from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import GuestFeedback

@receiver(post_save, sender=GuestFeedback)
def send_feedback_thankyou(sender, instance, created, **kwargs):
    if created:
        subject = 'Thank you for your feedback!'
        message = f'''Dear {instance.name},
        
        Thank you for taking the time to provide feedback. 
        We appreciate your input and will use it to improve our services.
        
        Best regards,
        Hotel Management Team'''
        
        send_mail(
            subject,
            message,
            'noreply@hotel.com',
            [instance.email],
            fail_silently=False,
        )
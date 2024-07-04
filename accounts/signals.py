"""
This module conyains signals for the account app.
"""
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import UserAccount


@receiver(post_save, sender=UserAccount)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    The function to send a welcome email when an account is created.
    """
    if created and instance.email:
        subject = 'Welcome to DELIVEET'
        body = render_to_string(
            'accounts/welcome_email.html',
            {
                'user': instance,
            }
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(
            subject,
            body,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

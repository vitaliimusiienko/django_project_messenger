from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in,user_logged_out
from .models import MessageLog, Messages, UserStatus

@receiver(post_save, sender=Messages)
def log_message(sender, instance,created,**kwargs):
    if created:
        MessageLog.objects.create(message=instance,message_log=
                f'Message sent from {instance.user.username} to {instance.receiver.username}')
        
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': True})
    
@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': False})


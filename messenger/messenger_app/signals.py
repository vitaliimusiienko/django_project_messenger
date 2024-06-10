from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import MessageLog, Messages

@receiver(post_save, sender=Messages)
def log_message(sender, instance,created,**kwargs):
    if created:
        MessageLog.objects.create(message=instance,message_log=
                f'Message sent from {instance.user.username} to {instance.receiver.username}')


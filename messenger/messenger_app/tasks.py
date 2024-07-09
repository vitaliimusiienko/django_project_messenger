from messenger.celery import shared_task
from .models import Messages
import logging

@shared_task
def log_last_10_messages():
    last_10_messages = Messages.objects.order_by('-created_at')[:10]
    logger = logging.getLogger('django')
    for message in last_10_messages:
        logger.info(f'{message.created_at}:{message.text}')
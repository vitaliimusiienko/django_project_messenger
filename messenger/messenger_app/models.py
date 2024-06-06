from django.db import models
from django.contrib.auth.models import User
from datetime import timezone, datetime, timedelta

class Chats(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
class ChatsMembership(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Messages(TimeStampMixin,models.Model):
    chat = models.ForeignKey(Chats, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    
    
    def can_edit_message(self, user):
        if user.is_superuser:
            return True
        
        if self.user == user and (timezone.now() - self.created_at) < timedelta(days=1):
            return True
        
        return False
    
    def can_delete_message(self, user):
        if user.is_superuser:
            return True
        
        if self.user == user:
            return True
        
        return False
    
    
    class Meta:
        permissions = [('can_edit_message', 'user can edit message'),
                      ('can_delete_message', 'user can delete message'),]


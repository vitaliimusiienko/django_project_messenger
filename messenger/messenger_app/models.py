from django.db import models
from django.contrib.auth.models import User
from datetime import timezone, timedelta

class Chats(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
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
    user = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receiver', on_delete=models.DO_NOTHING)
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
 
class MessageLog(models.Model):
    message = models.OneToOneField(Messages,related_name='log',on_delete=models.CASCADE)
    message_log = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"
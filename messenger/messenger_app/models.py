from django.db import models
from django.contrib.auth.models import User

class Chats(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
class ChatsMembership(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Message(models.Model):
    chat = models.ForeignKey(Chats, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    
    
    def can_edit_message(self, user):
        if user.is_superuser:
            return True
        
        if self.user:
            return self.user == user
        
        return True
    
    def can_delete_message(self, user):
        return user == self.user or user.is_superuser
    
    
    class Meta:
        ordering = ('date_published',)
        permissions = [('can_edit_message', 'user can edit message'),
                      ('can_delete_message', 'user can delete message'),]


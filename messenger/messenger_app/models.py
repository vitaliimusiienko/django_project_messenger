from django.db import models
from django.contrib.auth.models import User

class Chats(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    
class Message(models.Model):
    chat = models.ForeignKey(Chats, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('date_published',)


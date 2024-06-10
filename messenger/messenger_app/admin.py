from django.contrib import admin
from .models import Chats,Messages,MessageLog

admin.site.register(Chats)
admin.site.register(Messages)
admin.site.register(MessageLog)

# Register your models here.

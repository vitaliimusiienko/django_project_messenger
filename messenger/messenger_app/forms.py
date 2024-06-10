from django.forms import ModelForm
from .models import Messages

class NewMessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = [
            'text',
            'user',
            'receiver',
            'chat',
        ]
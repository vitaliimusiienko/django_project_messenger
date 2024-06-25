from rest_framework import serializers
from messenger_app.models import Chats, Messages
        
class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = '__all__'
        
class MessageSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Messages
        fields = '__all__'
        
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
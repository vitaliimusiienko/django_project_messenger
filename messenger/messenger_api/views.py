from rest_framework import generics,permissions
from messenger_app.models import Chats, Messages
from .serializers import ChatsSerializer, MessageSerializer, MessageCreateSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class UserChatView(generics.ListAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Chats.objects.all()
        else:
            return Chats.objects.filter(chatsmembership__user=self.request.user)
    
class ChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chats, id=chat_id)
        if self.request.user.is_superuser:
            return Messages.objects.filter(chat=chat)
        else:
            return Messages.objects.filter(chat=chat, user=self.request.user)
    
class MessageDetailView(generics.RetrieveAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Messages.objects.all()
    
class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
class MessageUpdateView(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Messages.objects.all()
    
    def perform_update(self,serializer):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer.save()
            
class MessageDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Messages.objects.all()
    
    def perform_destroy(self,instance):
        if instance.user == self.request.user:
            instance.delete()



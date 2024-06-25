from django.urls import path
from . import views

urlpatterns = [
    path('chats-api/', views.UserChatView.as_view(), name='user-chats'),
    path('chats-api/<int:chat_id>/messages/', views.ChatMessagesView.as_view(), name='chat-messages'),
    path('messages-api/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('messages-api/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('messages-api/update/<int:pk>/', views.MessageUpdateView.as_view(), name='message-update'),
    path('messages-api/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message-delete')
]
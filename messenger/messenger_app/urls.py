from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.ChatsView.as_view(), name='chats'),
    path('<slug:slug>/', views.ChatView.as_view(), name='chat'),
    path('<slug:slug>/new_message', views.CreateMessageView.as_view(), name='new_message'),
    path('<slug:slug>/edit_message/<int:message_id>', views.EditMessageView.as_view(), name='edit_message'),
    path('<slug:slug>/delete_message/<int:message_id>', views.DeleteMessageView.as_view(), name='delete_message'),
    path('add_to_chat/<int:chat_id>/', views.AddToChatView.as_view(), name='add_to_chat')
    
]
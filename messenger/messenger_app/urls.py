from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chats, name='chats'),
    path('<slug:slug>/', views.chat, name='chat'),
    path('<slug:slug>/new_message', views.new_message, name='new_message'),
    path('<slug:slug>/edit_message/<int:message_id>', views.edit_message, name='edit_message'),
    path('<slug:slug>/delete_message/<int:message_id>', views.delete_message, name='delete_message'),
    path('add_to_chat/<int:chat_id>/', views.add_to_chat, name='add_to_chat')
    
]
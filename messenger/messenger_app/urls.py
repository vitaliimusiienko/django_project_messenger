from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chats, name='chats'),
    path('<slug:slug>/', views.chat, name='chat'),
    path('<slug:slug>/new_message', views.new_message, name='new_message')
    
]
from django.shortcuts import render,redirect,reverse
from .models import Chats,Message,ChatsMembership
from .forms import NewMessageForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from datetime import datetime

@staff_member_required
@login_required
def add_to_chat(request, chat_id):
    if request.method == 'POST':
       chat = Chats.objects.get(pk=chat_id)
       username = request.POST.get('username')
       try:
           user = User.objects.get(username=username)
           ChatsMembership.objects.create(user=user, chat=chat)
       except User.DoesNotExist:
           pass
    return redirect('chats')


@login_required
def chats(request):
    if request.user.is_superuser:
        chats = Chats.objects.all()
    else:
        chats = Chats.objects.filter(chatsmembership__user=request.user)
    
    return render(request, 'messenger_app/chats.html', {'chats': chats})

@login_required
def chat(request, slug):
    chat = Chats.objects.get(slug=slug)
    messages = Message.objects.filter(chat=chat)[0:25]

    return render(request, 'messenger_app/chat.html', {'chat':chat, 'messages':messages})

@login_required
def new_message(request, slug):
    chat = Chats.objects.get(slug=slug)
    error = ''
    
    
    if request.method == 'POST':
        message_data = {}
        message_data['text'] = request.POST.get('content')
        message_data['chat'] = chat
        message_data['user'] = request.user
        message = NewMessageForm(message_data)
        if message.is_valid:
            message.save()
        else:
            error = 'try again'
            
    messages = NewMessageForm()
    context = {
        'chat':chat,
        'messages':messages,
        'error':error
    }
    return redirect(reverse('chat', kwargs={'slug':slug}))

@permission_required('messenger_app.can_edit_message', raise_exception=True)
def edit_message(request,message_id,slug):
    edit_datetime = datetime.now()
    if request.method == 'POST':
        edited_text = request.POST.get('edited_message')
        message = Message.objects.get(pk=message_id)
        if edited_text and message:
            message.text = edited_text
            message.date_published = edit_datetime
            message.save()
    
    
    return redirect(reverse('chat', kwargs={'slug':slug}))

@login_required
def delete_message(request,message_id,slug):
    message = Message.objects.get(pk=message_id)
    if message.can_delete_message(request.user):
        message.delete()
        return redirect(reverse('chat', kwargs={'slug':slug}))
    
    else:
        return redirect('homepage')
    
    
            

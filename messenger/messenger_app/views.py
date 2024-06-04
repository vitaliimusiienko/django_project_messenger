from django.shortcuts import render,redirect,reverse
from .models import Chats,Message
from .forms import NewMessageForm


def chats(request):
    chats = Chats.objects.all()
    
    return render(request, 'messenger_app/chats.html', {'chats': chats})

def chat(request, slug):
    chat = Chats.objects.get(slug=slug)
    messages = Message.objects.filter(chat=chat)[0:25]

    return render(request, 'messenger_app/chat.html', {'chat':chat, 'messages':messages})

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
    

# Create your views here.

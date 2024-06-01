from django.shortcuts import render,redirect
from .models import Chats,Message
from .forms import NewMessageForm


def chats(request):
    chats = Chats.objects.all()
    
    return render(request, 'messenger_app/chats.html', {'chats': chats})

def chat(request, slug):
    chat = Chats.objects.get(slug=slug)
    messages = Message.objects.filter(chat=chat)[0:25]

    return render(request, 'messenger_app/chat.html', {'chat':chat, 'messages':messages})

def new_message(request,slug):
    chat = Chats.objects.get(slug=slug)

    error = ''
    
    if request.method == 'POST':
        message = NewMessageForm(request.POST)
        if message.is_valid:
            message.save(commit=False)
            return request(message)
        else:
            error = 'Try again'
            
    messages = NewMessageForm()
    context = {
        'chat':chat,
        'messages':messages,
        'error':error
    }
    return redirect('chats')
    

# Create your views here.

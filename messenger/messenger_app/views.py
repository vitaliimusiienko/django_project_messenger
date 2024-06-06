from django.shortcuts import render,redirect,reverse
from .models import Chats,Messages,ChatsMembership
from .forms import NewMessageForm
from django.contrib.auth.models import User
from datetime import datetime
from .mixins import StaffMemberRequiredMixin,LoginRequiredMixin,CanEditMessageMixin,CanDeleteMessageMixin
from django.views.generic import View
    
class AddToChatView(StaffMemberRequiredMixin,LoginRequiredMixin,View):
    def post(self, request, chat_id):
        chat = Chats.objects.get(pk=chat_id)
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            ChatsMembership.objects.create(chat=chat,user=user)
        except User.DoesNotExist:
            pass
        return redirect('chats')
            
class ChatsView(LoginRequiredMixin,View):
    template_name = 'messenger_app/chats.html'
    def get(self,request):
        if request.user.is_superuser:
            chats = Chats.objects.all()
        else:
            chats = Chats.objects.filter(chatsmembership__user=request.user)
            
        return render(request, self.template_name, {'chats':chats})

class ChatView(LoginRequiredMixin,View):
    template_name = 'messenger_app/chat.html'
    
    def get(self,request,slug):
        chat = Chats.objects.get(slug=slug)
        messages = Messages.objects.filter(chat=chat)[0:25]
        
        context = {
            'chat':chat,
            'messages':messages
        }
        return render(request,self.template_name, context=context)
    
class CreateMessageView(LoginRequiredMixin,View):
    def post(self,request,slug):
        chat = Chats.objects.get(slug=slug)
        if request.method =='POST':
            message_data = {'chat':chat,
                        'user':request.user,
                        'text':request.POST.get('content')}
            message = NewMessageForm(message_data)
            if message.is_valid:
                message.save()
        
        message = NewMessageForm()
            
        return redirect(reverse('chat',kwargs={'slug':slug}))
    
class EditMessageView(CanEditMessageMixin,View):
    def post(self,request,message_id,slug):
        edited_datetime = datetime.now()
        edited_text = request.POST.get('edited_text')
        message = Messages.objects.get(pk=message_id)
        
        if edited_text and message:
            message.text = edited_text
            message.updated_at = edited_datetime
            message.save()
        
        return redirect(reverse('chat',kwargs={'slug':slug}))

class DeleteMessageView(CanDeleteMessageMixin,View):
    def post(self,request,message_id,slug):
        message =  Messages.objects.get(pk=message_id)
        if message.can_delete_message(request.user):
            message.delete()
        return redirect(reverse('chat',kwargs={'slug':slug}))
            
from django.shortcuts import render,redirect,reverse
from .models import Chats,Messages,ChatsMembership, UserStatus
from django.http import JsonResponse
from .forms import NewMessageForm
from django.contrib.auth.models import User
from datetime import datetime
from .mixins import StaffMemberRequiredMixin,LoginRequiredMixin,CanEditMessageMixin,CanDeleteMessageMixin
from django.views.generic import View
from django.contrib import messages as django_messages
    
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
        django_messages_for_template = django_messages.get_messages(request)
        
        
        context = {
            'chat':chat,
            'messages':messages,
            'django_messages':django_messages_for_template
        }
        return render(request,self.template_name, context=context)
    
class CreateMessageView(LoginRequiredMixin,View):
    def post(self,request,slug):
        chat = Chats.objects.get(slug=slug)
        if request.method =='POST':
            receiver_username = request.POST.get('receiver')
            receiver = User.objects.get(username=receiver_username)
            message_data = {'chat':chat,
                        'user':request.user,
                        'receiver':receiver,
                        'text':request.POST.get('content')}
            message_form = NewMessageForm(message_data)
            if message_form.is_valid:
                message_form.save()
                if receiver.is_superuser:
                    django_messages.success(request, 'You succesfully sent the message to the superuser')
        message_form = NewMessageForm()
            
        return redirect(reverse('chat', kwargs={'slug':slug}))
    
            
    
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
    
def user_status(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error':'UserDoesNotExist'}, status=404)
    
    try:
        status = UserStatus.objects.get(user=user)
        is_online = status.is_online
    except UserStatus.DoesNotExist:
        is_online = False
    return JsonResponse({'username':user.username, 'is_online':is_online})

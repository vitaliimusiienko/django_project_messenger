from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Messages
from django.utils import timezone
from datetime import timedelta

class StaffMemberRequiredMixin(View):
    @classmethod
    
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        
        return staff_member_required(view)
    
class LoginRequiredMixin(View):
    @classmethod
    
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        
        return login_required(view)
    

class CanEditMessageMixin(PermissionRequiredMixin):
    permission_required = 'messenger_app.can_edit_message'
    
    def has_permission(self):
        message_id = self.kwargs.get('message_id')
        if message_id:
            message = Messages.objects.get(pk=message_id)
            user = self.request.user
            
            if user.is_superuser:
                return True
            
            if message.user == user and (timezone.now() - message.created_at) < timedelta(days=1):
                return True
            
            return False
        
    def handle_no_permission(self):
        self.raise_exception = True
        return super().handle_no_permission()
    
class CanDeleteMessageMixin(PermissionRequiredMixin):
    permission_required = 'messenger_app.can_delete_message'
    
    def has_permission(self):
        message_id = self.kwargs.get('message_id')
        if message_id:
            message = Messages.objects.get(pk=message_id)
            user = self.request.user
            
            if user.is_superuser or message.user == user:
                return True
            
            return False
        
    def handle_no_permission(self):
        self.raise_exception = True
        return super().handle_no_permission()
    

        
    
        
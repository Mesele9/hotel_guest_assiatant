# common_user/mixins.py
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin:
    allowed_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if not (request.user.role in self.allowed_roles or request.user.is_superuser):
            raise PermissionDenied
            
        return super().dispatch(request, *args, **kwargs)
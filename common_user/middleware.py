# common_user/middleware.py
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_views = [
            'login_view',
            'logout',
            'menu_view',
            'menu_item_detail',
            'upload_file',
            'qr_code_page',
            'feedback_view',
            'feedback_success_view',
            'welcome',
            'policies',
            'services',
            'attractions',
            'room_info'
            # Add other public view names here
        ]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = view_func.__name__
        
        # Allow public views
        if view_name in self.public_views or getattr(view_func, 'is_public', False):
            return None
            
        # Redirect unauthenticated users
        if not request.user.is_authenticated:
            return redirect('login')
            
        # Admin bypass
        if request.user.is_superuser or request.user.role == 'admin':
            return None
            
        # Role-based access control
        allowed_roles = getattr(view_func, 'allowed_roles', None)
        if allowed_roles and request.user.role not in allowed_roles:
            return HttpResponseForbidden("You don't have permission to access this page")
            
        return None
# common_user/decorators.py
from django.http import HttpResponseForbidden
from functools import wraps

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            if request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Insufficient permissions")
        return _wrapped_view
    return decorator

def public_view(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view
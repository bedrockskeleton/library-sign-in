from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return redirect('users:admin_only')
    return _wrapped_view

def workstudy_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_workstudy:
            return view_func(request, *args, **kwargs)
        return redirect('sign_in:home')
    return _wrapped_view
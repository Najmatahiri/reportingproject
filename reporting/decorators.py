from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def access_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.give_access:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You don't have access to this page.")
            return redirect("index")

    return wrapper


def role_required(*required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, "role"):
                if request.user.role in required_roles:
                    return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have access to this page.")
                return redirect("index")

            return redirect("access_denied")

        return _wrapped_view

    return decorator

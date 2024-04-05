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
            return redirect('index')

    return wrapper

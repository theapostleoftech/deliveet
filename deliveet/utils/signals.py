from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from accounts.models import UserAccount


def customer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.account_type == UserAccount.UserAccountType.CUSTOMER:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You must be a customer to access this page.")
                return redirect('pages:app_home')
        else:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('accounts:signin')

    return _wrapped_view


def courier_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.account_type == UserAccount.UserAccountType.COURIER:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You must be a courier to access this page.")
                return redirect('pages:app_home')
        else:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('accounts:signin')

    return _wrapped_view

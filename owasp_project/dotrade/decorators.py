from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

from functools import wraps
from django.http import HttpResponseForbidden, HttpResponse

from .models import APIKey


def group_required(*group_names):
    """
    Decorator that checks if the user belongs to the required group(s).
    """
    def check_group(user):
        if user.is_authenticated:
            groups = user.groups.all()
            if not any(group.name in group_names for group in groups):
                raise PermissionDenied()
            return True
        raise PermissionDenied()

    return user_passes_test(check_group, login_url='dashboard')

def api_key_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        api_key = request.META.get('HTTP_APIKEY')

        if not api_key:
            return HttpResponseForbidden('API key missing')

        try:
            api_key_obj = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            return HttpResponseForbidden('Invalid API Key')

        request.user = api_key_obj.user

        return view_func(request, *args, **kwargs)

    return wrapped_view



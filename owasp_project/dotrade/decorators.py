from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group


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

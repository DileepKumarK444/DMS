from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from utils import helper


def permission_decorator(permission=''):
    def decorator(view_func):
        def wrap(request, *args, **kwarges):
            if (request.user.is_superuser):
                return view_func(request, *args, **kwarges)
            else:
                allowed_permissions = helper.get_all_user_permissions(
                    request.user.id)
                if permission in allowed_permissions:
                    return view_func(request, *args, **kwarges)
                else:
                    raise PermissionDenied
        return wrap
    return decorator

from datetime import datetime
from serviceapp.settings import BASE_URL, APP_NAME
from utils import helper
# from django.http import HttpResponse


def add_variable_to_context(request):

    allowed_permissions = request.session.get('permissions')
    # HttpResponse.set_cookie()
    # (key, value, max_age=max_age, expires=expires,
    # domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

    return {
        'date': datetime.now(),
        'app_name': APP_NAME,
        # 'left_menu_lists': list(left_menu_lists),
        'allowed_permissions': allowed_permissions,
        # 'BASE_URL': BASE_URL
    }

from django import template
from utils import helper
from userpermissions.models import UserRoleModel

register = template.Library()


@register.simple_tag(takes_context=True)
def get_roles(context, usid):
    current_roles = list(UserRoleModel.objects.filter(
        user_id=usid).values_list('role_id', flat=True))
    return len(current_roles) and current_roles[0] or ""

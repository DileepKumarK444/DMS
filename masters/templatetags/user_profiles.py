from django import template
from utils import helper
from masters.models import Profile

register = template.Library()


@register.simple_tag(takes_context=True)
def get_profiles(context, usid):
    current_roles = list(Profile.objects.filter(
        user_id=usid).values_list('time_zone', flat=True))
    return len(current_roles) and current_roles[0] or ""

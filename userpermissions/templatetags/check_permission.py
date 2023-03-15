from django import template
from utils import helper
import os
import sys

register = template.Library()


@register.simple_tag(takes_context=True)
def has_permission(context, slug):
    request = context['request']
    if (request.user.is_superuser):
        return 1
    else:
        allowed_permissions = helper.get_all_user_permissions(
            request.user.id)
        if(slug in allowed_permissions):
            return 1
        else:
            return 0


@register.simple_tag(takes_context=True)
def log_has_permission(context, user):
    request = context['request']
    if (user.id == request.user.id or request.user.is_superuser):
        return 1
    else:
        return 0


@register.simple_tag(takes_context=True)
def comment_has_permission(context, user):
    request = context['request']
    if (user.id == request.user or request.user.is_superuser):
        return 1
    else:
        return 0

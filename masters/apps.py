"""
Master App
"""
# pylint: disable=E0401
from django.apps import AppConfig

class MastersConfig(AppConfig):# pylint: disable=too-few-public-methods
    """Masters Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'masters'

# pylint: disable=no-member
"""
POST Customer APIs Testing
"""
from importlib.metadata import files
import pytest
import requests
import json
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

@pytest.mark.django_db
def test_post_add_pilot(api_client,get_user,authorization_token,pilot_details):
    """ Test check list for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('add_pilot')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url)
    
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_post_add_pilot(api_client,get_user,authorization_token,pilot_details):
#     """ Test check list for currently running plan """
#     api_client.login(username=get_user['username'], password=get_user['password'])
#     url = reverse('add_pilot')
#     api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
#     response = api_client.post(url,data=pilot_details,format='json')
#     response_data = response.json()
#     print(response_data)
#     assert response.status_code == 200
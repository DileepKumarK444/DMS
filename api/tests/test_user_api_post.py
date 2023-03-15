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
def test_post_login_check_valid_user(api_client,get_user,authorization_token,login_check):
    """ Test login_check """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('login_check')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=login_check,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_login_check1_invalid_user(api_client,get_user,authorization_token):
    """ Test login_check """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('login_check')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'username':'dileep', 'password':'password11'},format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_login_check1_valid_user_invalid_password(api_client,get_user,authorization_token):
    """ Test login_check """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('login_check')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'username':'dileep@gmail.com', 'password':'password11'},format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_login_check_valid_user_and_valid_password(api_client,get_user,authorization_token,):
    """ Test login_check """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('login_check')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_user,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
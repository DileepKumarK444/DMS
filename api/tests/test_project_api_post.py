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
def test_post_add_project(api_client,get_user,authorization_token,project_details):
    """ Test add_project """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('add_project')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={project_details},format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_delete_project(api_client,get_user,authorization_token,project_details,get_cust_id):
    """ Test delete_project """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('delete_project')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_cust_id,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_get_selelected_project(api_client,get_user,authorization_token,project_details,get_cust_id):
    """ Test get_selected_project """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_sel_project')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_cust_id,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_update_project(api_client,get_user,authorization_token,project_details,get_cust_id):
    """ Test update_project """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('update_project')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_cust_id,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
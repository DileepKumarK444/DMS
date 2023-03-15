# pylint: disable=no-member
"""
POST APIs Testing
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
def test_save_log_data1234(api_client,get_user,get_file):
    """ Test check list for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('save_log_data')
    api_client.credentials(HTTP_AUTHTOKEN=str(get_file[2]))
    response = api_client.post(url, data = get_file[1], format='multipart')
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_drone_list(api_client,get_user,authorization_token):
    """ Test check list for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_checklist')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'id':authorization_token[1]},format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_drone_log(api_client,get_user,authorization_token):
    """ Test drone log for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_drone_log')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'drone_id':authorization_token[1]},format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_filtered_reports(api_client,get_user,authorization_token):
    """ Test filterd report for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_filtered_reports')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url+'?page=1&offset=10',data={'drone_id':authorization_token[1],'filter_from_dt':'','filter_to_dt':'','filter_project':0,'filter_plan':0,'filter_limit':10,'filter_rpt':'','time_from':'','time_to':''},format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_checklist(api_client,get_user,authorization_token):
    """ Test check list for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_checklist')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'id':authorization_token[1]},format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_save_checklist(api_client,get_user,authorization_token):
    """ Test save check list for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('save_checklist')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'plan_id':authorization_token[2].id,'rule_data':[{}],'maintenance_data':[{}],'approval_data':[{}]},format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_get_drone_image(api_client,get_user,authorization_token):
    """ Test get_drone_image log for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_drone_image')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'id':authorization_token[1]},format='json')
    assert response.status_code == 200 

@pytest.mark.django_db
def test_post_get_profile_schema(api_client,get_user,authorization_token):
    """ Test get_profile_schema  for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_profile_schema')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'id':authorization_token[1]},format='json')
    assert response.status_code == 200 

@pytest.mark.django_db    
def test_post_get_plan(api_client,get_user,authorization_token):
    """ Test get_plan  for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_plan')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data={'project_id':0,'drone':1},format='json')
    assert response.status_code == 200 


@pytest.mark.django_db
def test_post_consumption_log(api_client,get_user,token_tring,data_cpu):

    """ Test consumption_log for currently running plan """
    print(token_tring)
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('consumption_log')
    api_client.credentials(HTTP_AUTHTOKEN=str(token_tring[0]))

    response = api_client.post(url,data=data_cpu,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200 


@pytest.mark.django_db
def test_post_forgot_password_invalid(api_client,get_user,authorization_token):
    """ Test forgot password log for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('forgot_password')
    # api_client.credentials(HTTP_AUTHTOKEN=str(authorization_token[2]))
    response = api_client.post(url, data = {'email':'dileep1@gmail.com'}, format='json')
    response_data = response.json()
    print(response_data['msg'])

    assert response_data['msg'] == 'Email does not exist!'


@pytest.mark.django_db
def test_post_forgot_password_valid(api_client,get_user,authorization_token):
    """ Test forgot password log for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('forgot_password')
    # api_client.credentials(HTTP_AUTHTOKEN=str(authorization_token[2]))
    response = api_client.post(url, data = {'email':'dileep@gmail.com'}, format='json')
    response_data = response.json()
    print(response_data['msg'])

    assert response.status_code==200

@pytest.mark.django_db
def test_post_file_upload(api_client,get_user,authorization_token,get_file1):
    """ Test file_upload for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('file_upload')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_file1,format='multipart')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200 


@pytest.mark.django_db
def test_post_download_licence(api_client,get_user,authorization_token):
    """ Test download_licence log for currently running plan """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('download_licence')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    print('authorization_token[2]',authorization_token[2])
    response = api_client.post(url,data={'id':authorization_token[3]},format="json")
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
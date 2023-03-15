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
def test_post_save_customer(api_client,get_user,authorization_token,customer_details2,get_cust_id):
    """ Test save_customer """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('save_customer')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=
    customer_details2,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_GetUserList(api_client,get_user,authorization_token,customer_details1):
    """ Test get user list """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_user_list')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=authorization_token[1],format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_save_user_details(api_client,get_user,authorization_token,customer_details1):
    """ Test get CustomerSave """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('save-user-details')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=customer_details1,format='multipart')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_delete_user(api_client,get_user,authorization_token,customer_details1,get_cust_id):
    """ Test delete_user correct input """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('delete_user')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_cust_id,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_delete_user_wrong_input_id(api_client,get_user,authorization_token,customer_details1,get_cust_id):
    """ Test delete_userwith wrond input id """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('delete_user')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=customer_details1,format='multipart')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_api_log_view(api_client,get_user,authorization_token,customer_details):
    """ Tes api_log_view  """
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('list')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url+'?page=1&offset=10',data={'drone_id':authorization_token[1],'plan':0,'project':0,'date_from':'','date_to':'','time_from':'','time_to':'','filter':''},format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_UserCustomerUpdate_incorrect_info(api_client,get_user,authorization_token,customer_details_for_update):
    """ Test update_customer user incorrect info"""
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('update_user')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=customer_details_for_update,format='multipart')
    response_data = response.json()
    
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_UserCustomerUpdate_correct_info(api_client,get_user,authorization_token,customer_details1):
    """ Test update_user correct info"""
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('update_user')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=customer_details1,format='multipart')
    response_data = response.json()
    
    print(response_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_get_sel_user(api_client,get_user,authorization_token,customer_details1,get_cust_id):
    """ Test get_selected_user"""
    api_client.login(username=get_user['username'], password=get_user['password'])
    url = reverse('get_sel_user')
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    response = api_client.post(url,data=get_cust_id,format='json')
    response_data = response.json()
    
    print(response_data)
    assert response.status_code == 200
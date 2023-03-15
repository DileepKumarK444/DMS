# pylint: disable=no-member
"""
POST APIs Testing
"""
from importlib.metadata import files
from urllib import response
import pytest
import requests
import json
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
import io


# # @pytest.mark.django_db
# # def test_handshake_validation(api_client,get_user,get_file):
# #     """ Test check list for currently running plan """
# #     api_client.login(username=get_user['username'], password=get_user['password'])
# #     url = reverse('handshake_validation')
# #     api_client.credentials(HTTP_AUTHTOKEN=str(get_file[2]))
# #     response = api_client.post(url, data = get_file[1], format='multipart')
# #     assert response.status_code == 200


# # @pytest.mark.django_db
# # def test_post_download_log(api_client,get_user,authorization_token):
# #     """ Test save data log for currently running plan """
# #     api_client.login(username=get_user['username'], password=get_user['password'])
# #     url = reverse('download_log')
# #     api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
# #     response = api_client.post(url,data={'id':authorization_token[1]},format='json')
# #     assert response.status_code == 200




    



# @pytest.mark.django_db
# def test_post_download_licence(api_client,get_user,authorization_token,get_cust_id):
#     """ Test download_licence log for currently running plan """
#     api_client.login(username=get_user['username'], password=get_user['password'])
#     url = reverse('download_licence')
#     api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
#     response = api_client.post(url,_data=get_cust_id,format='json')
#     response_data = response.json()
#     print(response_data)
#     assert response.status_code == 200 



# @pytest.mark.django_db
# def test_post_change_password_with_valid_oldpassword(api_client,get_user,authorization_token,get_cust_id):
#     """ Test change_password log for currently running plan """
#     api_client.login(username=get_user['username'], password=get_user['password'])
#     url = reverse('change_password')
#     api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
#     response = api_client.post(url,data=get_cust_id,format='json')
#     # response = api_client.post(url,data={'id':authorization_token[1],'new_password':'asdf','password':'password'},format='json')
#     response_data = response.json()
#     print(response_data)
#     assert response.status_code == 200 

# @pytest.mark.django_db
# def test_post_change_password_with_invalid_old_password(api_client,get_user,authorization_token,get_cust_id2):
#     """ Test change_password log for currently running plan """
#     api_client.login(username=get_user['username'], password=get_user['password'])
#     url = reverse('change_password')
#     api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
#     response = api_client.post(url,data=get_cust_id2,format='json')
#     # response = api_client.post(url,data={'id':authorization_token[1],'new_password':'asdf','password':'password'},format='json')
#     response_data = response.json()
#     print(response_data)
#     assert response.status_code == 200 

    
# @pytest.mark.django_db
# def test_post_get_login_token(api_client,get_user,get_file,authorization_token):
#     """ Test get_login_token  for currently running plan """
#     api_client.login(username=get_user['username'], password=get_user['password'])
#     url = reverse('get_login_token')
#     # api_client.credentials(HTTP_AUTHTOKEN=str(get_file[2]))
#     response = api_client.post(url,data={'token':authorization_token[1]},format='json')
#     assert response.status_code == 200


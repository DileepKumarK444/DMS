# pylint: disable=no-member
"""
GET APIs Testing
"""
import pytest
import requests
from django.urls import reverse
import json

# def test_login_valid(api_client,get_headers,get_user):
#     """ Test login valid """
#     # url = supply_url + "/login/"
#     data = {'username':get_user['username'],'password':get_user['password']}
#     url = reverse('save_log_data')
#     # api_client.
#     resp = api_client.post(url, json=data,headers=get_headers)
#     assert resp.status_code == 200

@pytest.mark.django_db
def test_get_drone_one(api_client,get_user,authorization_token):
    """ Test get drone list """
    api_client.login(username=get_user['username'], password=get_user['password'])
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    url = reverse('get_drone')
    resp = api_client.post(url,data=json.dumps(authorization_token[1]),format='json')
    resp_data = resp.json()
    assert resp.status_code == 200

def test_get_drone_list123(api_client,get_user,authorization_token):
    """ Test get drone list """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('get_drone_list')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))

def test_get_projectlist(api_client,get_user,authorization_token):
    """ Test get project list """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('get_project_list')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))

def test_get_drone_details(api_client,get_user,authorization_token):
    """ Test get drone details  """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('save_drone_list')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))

def test_release_plan_details(api_client,get_user,authorization_token):
    """ Test release plan """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('get_release_plan')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))

def test_get_pilot_list(api_client,get_user,authorization_token):
    """ Test get pilot list """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('get_pilot_list')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))

def test_get_updated_fileds(api_client,get_user,authorization_token):
    """ Test get updated fields """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('update_fields')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))

def test_get_read_data(api_client,get_user,authorization_token):
    """ Test read data fields """
    try:
        api_client.login(username=get_user['username'], password=get_user['password'])
        api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
        url = reverse('read_data')
        resp = api_client.get(url)
        resp_data = resp.json()
        print(resp_data)
        assert resp.status_code == 200
    except Exception as e:
        print(str(e))
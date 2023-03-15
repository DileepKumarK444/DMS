# pylint: disable=no-member
"""
GET APIs Testing
"""
import pytest
import requests
from django.urls import reverse
import json



def test_get_customer_details(api_client,get_user,authorization_token):
    """ Test get get-customer-details """
    api_client.login(username=get_user['username'], password=get_user['password'])
    api_client.credentials(HTTP_AUTHORIZATION='Token '+str(authorization_token[0]))
    url = reverse('get-customer-details')
    resp = api_client.get(url)
    resp_data = resp.json()
    print(resp_data)
    assert resp.status_code == 200
    
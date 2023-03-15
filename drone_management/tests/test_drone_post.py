import pytest
from django.urls import reverse
from masters.models import Company,Country, State, ProductType,Product
# Country List with out authendication access
# def test_onload_get_Drone_Details(
#     client,login_check,authorization_token
#     ):
#     """Test on load get Drone Details"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('get Drone Details')
#     response = client.post(url,data={'id':authorization_token[1]},format='json')
#     assert response.status_code == 200

# def test_Activate_Drone(
#     client,login_check,authorization_token
#     ):
#     """Test Activate Drone Details"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Activate Drone')
#     response = client.post(url,data={'id':authorization_token[1]},format='json')
#     assert response.status_code == 200

# def test_Test_Connection(
#     client,login_check,authorization_token
#     ):
#     """Test Test Connection"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Test Connection')
#     response = client.post(url,data={'id':authorization_token[1]},format='json')
#     print(response)
#     assert response.status_code == 200

# def test_Save_Config(
#     client,login_check,authorization_token
#     ):
#     """Test Save Config"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Save Config')
#     response = client.post(url,data={'id':authorization_token[1]},format='json')
#     print(response)
#     assert response.status_code == 200

# def test_post_Drone_Details_Add(
#     client,login_check,authorization_token
#     ):
#     """Test post Drone Details Add"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Drone Details Add')
#     response = client.post(url,data={'id':authorization_token[1]},format='json')
#     print(response)
#     assert response.status_code == 200

# def test_post_Drone_Details_Update(
#     client,login_check,authorization_token
#     ):
#     """Test post Drone Details Update"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Drone Details Update')
#     response = client.post(url,data={'id':authorization_token[1]},format='json')
#     print(response)
#     assert response.status_code == 200

def test_post_Get_Drone_Type(
    client,login_check,authorization_token,drone_type):
    """Test post Get Drone Type"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Get Drone Type')
    response = client.post(url,data=drone_type,format='json')
    print(response)
    assert response.status_code == 200

# def test_sav_log_Drone_Details_Update(
#     client,login_check,authorization_token,drone_type_data_for_save
#     ):
#     """Test save log  Drone Details Update"""
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Drone Details Update')
#     response = client.save_log(url,data={'id':True},format='json')
#     print(response)
#     assert response.status_code == 200
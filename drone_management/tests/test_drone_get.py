import pytest
from django.urls import reverse
from masters.models import Company,Country, State, ProductType,Product

def test_get_Schema_Details(
    client,login_check
    ):
    """Test get Schema Details"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('get Schema Details')
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_drone_not_logged_in_admin(client):
    """Access Drone  without logged in """
    url = reverse('get Schema Details')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/drone/drone-details/getSchema/'

def test_get_Drone_Details_List(
    client,login_check
    ):
    """Test Drone Details List"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Drone Details List')
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_Drone_Details_List_without_login(client):
    """Access Drone Details List without logged in """
    url = reverse('Drone Details List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/drone/drone-details/'


def test_get_Drone_Details_Edit(
    client,login_check,authorization_token,token_tring
    ):
    """Test get Drone Details Edit"""
    client.login(username=login_check['username'], password=login_check['password'])
    # url = reverse('Drone Details Edit')
    url = reverse('Drone Details Edit', kwargs={'cid':authorization_token[1]})
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_drone_Drone_Details_Edit_not_logged_in_admin(client,token_tring):
    """Access Drone Details Edit  without logged in """
    url = reverse('Drone Details Edit', kwargs={'cid':token_tring[2]})
    response = client.get(url)
    print(response)
    assert response.url == '/auth/login/?next=/drone/drone-details/edit/6/'  

def test_Get_Config(
    client,login_check,token_tring
    ):
    """Test Get Configs"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Get Config', kwargs={'cid':token_tring[2]})
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_Get_Config_not_logged_in_admin(client,token_tring):
    """Access Get Config  without logged in """
    url = reverse('Get Config', kwargs={'cid':token_tring[2]})
    response = client.get(url)
    print(response)
    assert response.url == '/auth/login/?next=/drone/drone-details/config/10'


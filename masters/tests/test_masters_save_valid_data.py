# pylint: disable=no-member
"""
Country Master
"""
import pytest
from django.urls import reverse
from masters.models import Company,Country, State, ProductType,Product
# Country List with out authendication access
def test_country_save_if_logged_in_with_correct_data(
    client,login_check,country_data_for_save
    ):
    """Test country save logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('SaveCountry')
    response = client.post(url,data=country_data_for_save)
    assert response.status_code == 200

# -------------------------------------------------------------------------------------------------
# State List authendication access
def test_state_save_logged_in_uses_correct_template_admin(client,login_check,state_data_for_save):
    """Test state save logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('SaveState')
    response = client.post(url,data=state_data_for_save)
    assert response.status_code == 200


# -----------------------------------------------------
# Drone Type List authendication access
def test_drone_type_save_logged_in_uses_correct_template_admin(client,login_check,drone_type_data_for_save):
    """Test drone type list logged in uses correct template admin"""
    # login = client.login(username=login_check['username'], password=login_check['password'])
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type Add')
    response = client.post(url,data=drone_type_data_for_save)
    assert response.status_code == 200

# -------------------------------------------------------
# # Customers List authendication access
def test_customers_save_logged_in_uses_correct_template_admin(client,login_check,customer_save_data):
    login = client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Manage customers Add')
    response = client.post(url,data=customer_save_data)
    msg = response.json()
    # print('response',msg['msg'])
    assert response.status_code == 200

    # # Product List authendication access

def test_product_type_save_logged_in_uses_correct_template_admin(client,login_check,save_data_product_type):
    """Test product type list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type Add')
    response = client.post(url,data=save_data_product_type)
    assert response.status_code == 200

def test_purpose_save_logged_in_uses_correct_template_admin(client,login_check,save_data_purpose_type):
    """Test purpose list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Save Purpose')
    response = client.post(url,data=save_data_purpose_type  )
    assert response.status_code == 200 

def test_settings_save_logged_in_uses_correct_template_admin(client,login_check,save_data_settings):
    """Test settings  logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Settings Add')
    response = client.post(url,data=save_data_settings )
    assert response.status_code == 200 

def test_product_save_logged_in_uses_correct_template_admin(client,login_check,save_product_data):
    """Test product list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Page Add')
    response = client.post(url,data=save_product_data)
    assert response.status_code == 200 

def test_log_field_logged_in_uses_correct_template_admin(client,login_check,save_log_field_data):
    """Test log_fields logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Save Fields')
    response = client.post(url,data=save_log_field_data)
    assert response.status_code == 200 

def test_category_logged_in_uses_correct_template_admin(client,login_check,save_category_data):
    """Test category logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('category Add')
    response = client.post(url,data=save_category_data)
    assert response.status_code == 200 

def test_reason_logged_in_uses_correct_template_admin(client,login_check,save_reason_data):
    """Test reason logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('reason Add')
    response = client.post(url,data=save_reason_data)
    assert response.status_code == 200 
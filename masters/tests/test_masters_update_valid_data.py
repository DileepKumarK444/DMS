# pylint: disable=no-member
"""
Country Master
"""
import pytest
from django.urls import reverse
from masters.models import Company,Country, State, ProductType
# Country List with out authendication access
def test_country_save_if_logged_in_with_correct_data(
    client,login_check,country_data_for_update,country_data_for_save
    ):
    """Test country save logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('UpdateCountry')
    # print('country_data_for_update',country_data_for_update,country_data_for_save)
    # response = client.post(url,data=country_data_for_save)
    response = client.post(url,data=country_data_for_update)
    # print(Country.objects.all())
    assert response.status_code == 200

# -------------------------------------------------------------------------------------------------
# State List authendication access
def test_state_update_logged_in_uses_correct_template_admin(client,login_check,state_data_for_update):
    """Test state save logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    # dd = State.objects.all()
    # print('Before DDDD',dd)
    url = reverse('UpdateState')
    response = client.post(url,data=state_data_for_update)
    # dd = State.objects.get(name='Sample State1')
    # print('After DDDD',dd)
    # print('response',response.json())
    assert response.status_code == 200
# # -----------------------------------------------------
# # Drone Type List authendication access
# def test_drone_type_save_logged_in_uses_correct_template_admin(client,login_check,drone_type_data_for_save):
#     """Test drone type list logged in uses correct template admin"""
#     # login = client.login(username=login_check['username'], password=login_check['password'])
#     client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('product Type Add')
#     response = client.post(url,data=drone_type_data_for_save)
#     assert response.status_code == 200

# # -------------------------------------------------------
# # # Customers List authendication access
# def test_customers_save_logged_in_uses_correct_template_admin(client,login_check,customer_save_data):
#     login = client.login(username=login_check['username'], password=login_check['password'])
#     url = reverse('Manage customers Add')
#     response = client.post(url,data=customer_save_data)
#     msg = response.json()
#     # print('response',msg['msg'])
#     assert response.status_code == 200
def test_drone_type_updated_if_logged_in_with_correct_data(
    client,login_check,drone_type_for_updated):
    """Test drone_type updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type Update')
    response = client.post(url,data=drone_type_for_updated)
    assert response.status_code == 200

def test_product_type_updated_if_logged_in_with_correct_data(
    client,login_check,product_type_for_update):
    """Test Product_type updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type Update')
    response = client.post(url,data=product_type_for_update)
    assert response.status_code == 200

def test_products_updated_if_logged_in_with_correct_data(
    client,login_check,products_for_update):
    """Test Product updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Product Update')
    response = client.post(url,data=products_for_update)
    assert response.status_code == 200

def test_settings_updated_if_logged_in_with_correct_data(
    client,login_check,settings_for_update):
    """Test settings updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Product Update')
    response = client.post(url,data=settings_for_update)
    assert response.status_code == 200

def test_purpose_updated_if_logged_in_with_correct_data(
    client,login_check,purpose_for_update):
    """Test purpose updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Product Update')
    response = client.post(url,data=purpose_for_update)
    assert response.status_code == 200


def test_reason_updated_if_logged_in_with_correct_data(
    client,login_check,reason_for_update):
    """Test reason updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('reason Update')
    response = client.post(url,data=reason_for_update)
    assert response.status_code == 200

def test_category_updated_if_logged_in_with_correct_data(
    client,login_check,category_for_update):
    """Test category updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('category Update')
    response = client.post(url,data=category_for_update)
    assert response.status_code == 200

def test_log_field_updated_if_logged_in_with_correct_data(
    client,login_check,log_field_for_update):
    """Test log_field updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Field Update data')
    response = client.post(url,data=log_field_for_update)
    assert response.status_code == 200

def test_customer_updated_if_logged_in_with_correct_data(
    client,login_check,customer_for_update):
    """Test log_field updated logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Manage customers User Save')
    response = client.post(url,data=customer_for_update)
    assert response.status_code == 200
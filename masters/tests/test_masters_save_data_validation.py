# pylint: disable=no-member
"""
Country Master
"""
import pytest
from django.urls import reverse
from masters.models import Company,Country, State, ProductType
# Country List with out authendication access
def test_country_save_if_logged_in_template_validation(
    client,login_check
    ):
    """Test country save logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('SaveCountry')
    response = client.post(url)
    msg = response.json()
    # print('Response POST 123',msg['errors']['txt_name'][0]=='This field is required.')
    assert msg['errors']['txt_name'][0]=='This field is required.'

    # assert 'country/list.html' in (t.name for t in response.templates)
    # assert str(response.context['user']) == 'testuser1'
# -------------------------------------------------------------------------------------------------
# State List authendication access
def test_state_save_logged_in_uses_correct_template_admin(client,login_check):
    """Test state save logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('SaveState')
    response = client.post(url)
    msg = response.json()
    # print('msg',msg)
    assert msg['errors']['txt_name'][0]=='This field is required.'
    # state_obj = State.objects.get(name = 'Sample State')
    # url = reverse('Statelist')
    # response = client.delete(url+'?id='+str(state_obj.id))
    # state_obj_new = State.objects.filter(name = 'Sample State')
    # assert response.status_code == 200


# -----------------------------------------------------
# Drone Type List authendication access
def test_drone_type_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test drone type list logged in uses correct template admin"""
    # login = client.login(username=login_check['username'], password=login_check['password'])
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type Add')
    response = client.post(url)
    msg = response.json()
    assert msg['errors']['txt_name'][0]=='This field is required.'
    # assert 'drone_type/list.html' in (t.name for t in response.templates)
    # assert str(response.context['user']) == 'testuser1'

# -------------------------------------------------------
# # Customers List authendication access

def test_customers_save_logged_in_uses_correct_template_validation(client,login_check):
    login = client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Manage customers Add')
    response = client.post(url)
    msg = response.json()
    assert msg['errors']['first_name'][0]=='This field is required.'
    
def test_product_type_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test product type list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type Add')
    response = client.post(url)
    msg = response.json()
    assert msg['errors']['txt_name'][0]=='This field is required.'

def test_purpose_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test purpose list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Save Purpose')
    response = client.post(url)
    msg = response.json()
    assert msg['errors']['txt_name'][0]=='This field is required.'

def test_settings_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test settings list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Settings Add')
    response = client.post(url)
    msg = response.json()   
    assert msg['errors']['conf_value'][0]=='This field is required.'   
    assert msg['errors']['conf_key'][0]=='This field is required.' 

def test_product_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test product list logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Page Add')
    response = client.post(url)
    msg = response.json()   
    assert msg['errors']['dt_purchase'][0]=='This field is required.'   
    assert msg['errors']['cb_product_type'][0]=='This field is required.'

def test_log_fields_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test log_fields logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Save Fields')
    response = client.post(url)
    msg = response.json()
    print(type(msg))
    # assert msg['errors']['txt_template_name'][0]=='This field is required.'   
    assert msg['errors']['log_fields'][0]=='This field is required.'

def test_category_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test category logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('category Add')
    response = client.post(url)
    msg = response.json()
    assert msg['errors']['txt_model'][0]=='This field is required.'   
    

def test_reason_save_logged_in_uses_correct_template_validation(client,login_check):
    """Test reason logged in uses correct template admin"""
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('reason Add')
    response = client.post(url)
    msg = response.json()
    assert msg['errors']['txt_reason'][0]=='This field is required.'   
    assert msg['errors']['cb_module'][0]=='This field is required.'
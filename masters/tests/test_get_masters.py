# pylint: disable=no-member
"""
GET Methods Testing
"""
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_country_list_if_not_logged_in_admin(client):
    """Access Country list without logged in """
    url = reverse('Countrylist')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/country/'

@pytest.mark.django_db
def test_country_list_logged_in_uses_correct_template_admin(client,login_check):
    """Access Country list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Countrylist')
    response = client.get(url)
    assert response.status_code == 200
    assert 'country/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_state_list_if_not_logged_in_admin(client):
    """Access State list without logged in """
    url = reverse('Statelist')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/state/'

@pytest.mark.django_db
def test_state_list_logged_in_uses_correct_template_admin(client,login_check):
    """Access State list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Statelist')
    response = client.get(url)
    assert response.status_code == 200
    assert 'state/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_drone_type_list_if_not_logged_in_admin(client):
    """Access Drone Type list without logged in """
    url = reverse('Drone Type list')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/drone_type/'

@pytest.mark.django_db
def test_drone_type_list_logged_in_uses_correct_template_admin(client,login_check):
    """Access Drone Type list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Drone Type list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'drone_type/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_customers_list_if_not_logged_in_admin(client):
    """Access Customer list without logged in """
    url = reverse('Manage customers')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/customers/'

@pytest.mark.django_db
def test_customers_list_logged_in_uses_correct_template_admin(client,login_check):
    """Access Customer list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Manage customers')
    response = client.get(url)
    assert response.status_code == 200
    assert 'customers/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_product_type_list_if_not_logged_in_admin(client):
    """Access Product Type list without logged in """
    url = reverse('product Type List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/product_type/'

@pytest.mark.django_db
def test_product_type_list_logged_in_uses_correct_template_admin(client,login_check):
    """Access Product Type list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Type List')
    response = client.get(url)
    assert response.status_code == 200
    assert 'product_type/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_category_list_if_not_logged_in_admin(client):
    """Access Category list without logged in """
    url = reverse('category List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/category/'

@pytest.mark.django_db
def test_category_list_logged_in_uses_correct_template_admin(client,login_check):
    """Access Category list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('category List')
    response = client.get(url)
    assert response.status_code == 200
    assert 'category/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_purpose_if_not_logged_in_admin(client):
    """Access Purpose list without logged in """
    url = reverse('Purpose list')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/purpose/'

@pytest.mark.django_db  
def test_purpose_logged_in_uses_correct_template_admin(client,login_check):
    """Access Purpose list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Purpose list')
    response = client.get(url)
    assert response.status_code == 200 
    assert 'purpose/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_settings_if_not_logged_in_admin(client):
    """Access settings list without logged in """
    url = reverse('Settings List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/settings/'

@pytest.mark.django_db  
def test_settings_logged_in_uses_correct_template_admin(client,login_check):
    """Access settings list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Settings List')
    response = client.get(url)
    assert response.status_code == 200 
    assert 'settings/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_products_if_not_logged_in_admin(client):
    """Access Products list without logged in """
    url = reverse('product Page List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/products/'

@pytest.mark.django_db  
def test_products_logged_in_uses_correct_template_admin(client,login_check):
    """Access Products list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('product Page List')
    response = client.get(url)
    assert response.status_code == 200 
    assert 'products/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_reason_if_not_logged_in_admin(client):
    """Access reason list without logged in """
    url = reverse('reason List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/reason/'

@pytest.mark.django_db  
def test_reason_logged_in_uses_correct_template_admin(client,login_check,get_reason_save_data):
    """Access reason list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('reason List')
    response = client.get(url)
    assert response.status_code == 200 
    assert 'reason/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'

@pytest.mark.django_db
def test_log_fields_if_not_logged_in_admin(client):
    """Access log_fields list without logged in """
    url = reverse('Template List')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/log_field_template/list/'
   
@pytest.mark.django_db  
def test_log_fields_logged_in_uses_correct_template_admin(client,login_check,get_reason_save_data):
    """Access log_fields list with logged in """
    client.login(username=login_check['username'], password=login_check['password'])
    url = reverse('Template List')
    response = client.get(url)
    assert response.status_code == 200 
    assert 'log_fields_template/list.html' in (t.name for t in response.templates)
    assert str(response.context['user']) == 'testuser1'
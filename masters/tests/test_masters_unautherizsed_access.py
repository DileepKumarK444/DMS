# pylint: disable=no-member
"""
Country Master
"""
import pytest
from django.urls import reverse
from masters.models import Company,Country, State, ProductType
# Country List with out authendication access
@pytest.mark.django_db
def test_country_save_if_not_logged_in(client):
    """Test country save if not logged in admin"""
    url = reverse('SaveCountry')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/country/add/'
# -------------------------------------------------------------------------------------------------
# State List direct URL access
@pytest.mark.django_db
def test_state_save_if_not_logged_in_admin(client):
    """Test state save if not logged in admin"""
    # print('Country Data',Country.objects.all())
    url = reverse('SaveState')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/state/add/'
# -----------------------------------------------------
# Drone Type List direct URL access
@pytest.mark.django_db
def test_drone_type_save_if_not_logged_in_admin(client):
    """Test drone type list if not logged in admin"""
    url = reverse('product Type Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/product_type/add/'

# -------------------------------------------------------
# Customers List direct URL access
@pytest.mark.django_db
def test_customers_save_if_not_logged_in_admin(client):
    url = reverse('Manage customers Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/customers/add/'

@pytest.mark.django_db
def test_product_type_save_if_not_logged_in_admin(client):
    url = reverse('product Type Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/product_type/add/'

@pytest.mark.django_db
def test_purpose_save_if_not_logged_in_admin(client):
    url = reverse('Save Purpose')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/purpose/add/'

@pytest.mark.django_db
def test_settings_save_if_not_logged_in_admin(client):
    url = reverse('Settings Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/settings/add/'

@pytest.mark.django_db
def test_products_save_if_not_logged_in_admin(client):
    url = reverse('product Page Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/products/add/'

@pytest.mark.django_db
def test_log_fields_save_if_not_logged_in_admin(client):
    url = reverse('Save Fields')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/log_field_template/save_fields/'

@pytest.mark.django_db
def test_category_save_if_not_logged_in_admin(client):
    url = reverse('category Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/category/add/'

@pytest.mark.django_db
def test_reason_save_if_not_logged_in_admin(client):
    url = reverse('reason Add')
    response = client.get(url)
    assert response.url == '/auth/login/?next=/masters/reason/add/'
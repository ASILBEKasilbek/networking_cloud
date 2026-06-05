import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCustomerAPI:
    """Test Customer API endpoints."""
    
    def test_list_customers(self, authenticated_client):
        """Test listing customers."""
        client, user = authenticated_client
        url = reverse('customer-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_customer(self, authenticated_client):
        """Test creating a customer."""
        client, user = authenticated_client
        url = reverse('customer-list')
        data = {
            'code': 'CUST002',
            'name': 'New Customer',
            'customer_type': 'B2B',
            'email': 'new@example.com',
            'phone': '+1234567890',
            'street_address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'postal_code': '54321',
            'country': 'USA',
            'payment_terms': 'NET30'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_retrieve_customer(self, authenticated_client, sample_customer):
        """Test retrieving a customer."""
        client, user = authenticated_client
        url = reverse('customer-detail', kwargs={'pk': sample_customer.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == sample_customer.name
    
    def test_customer_statistics(self, authenticated_client, sample_customer):
        """Test customer statistics endpoint."""
        client, user = authenticated_client
        url = reverse('customer-statistics', kwargs={'pk': sample_customer.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'total_orders' in response.data


@pytest.mark.django_db
class TestProductAPI:
    """Test Product API endpoints."""
    
    def test_list_products(self, authenticated_client):
        """Test listing products."""
        client, user = authenticated_client
        url = reverse('product-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_product(self, authenticated_client):
        """Test creating a product."""
        client, user = authenticated_client
        url = reverse('product-list')
        data = {
            'sku': 'NEW-SKU-002',
            'name': 'New Product',
            'description': 'A new product',
            'cost_price': 15.00,
            'list_price': 30.00,
            'sale_price': 25.00,
            'unit': 'PCS'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_low_stock_products(self, authenticated_client):
        """Test low stock products endpoint."""
        client, user = authenticated_client
        url = reverse('product-low_stock')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestOrderAPI:
    """Test Order API endpoints."""
    
    def test_list_orders(self, authenticated_client):
        """Test listing orders."""
        client, user = authenticated_client
        url = reverse('order-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAuthenticationAPI:
    """Test Authentication endpoints."""
    
    def test_obtain_token(self, api_client, db):
        """Test obtaining JWT token."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data


@pytest.mark.django_db
class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, api_client):
        """Test health check endpoint."""
        url = reverse('health-check')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'ok'

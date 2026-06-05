import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    """Provide an API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(db):
    """Provide an authenticated API client."""
    client = APIClient()
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        role='manager'
    )
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, user


@pytest.fixture
def admin_client(db):
    """Provide an admin API client."""
    client = APIClient()
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    refresh = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, admin


@pytest.fixture
def sample_customer(db):
    """Create a sample customer."""
    from apps.models import Customer
    return Customer.objects.create(
        code='TEST001',
        name='Test Customer',
        customer_type='B2B',
        email='customer@test.com',
        phone='+1234567890',
        street_address='123 Test St',
        city='Test City',
        state='TC',
        postal_code='12345',
        country='USA'
    )


@pytest.fixture
def sample_product(db):
    """Create a sample product."""
    from apps.models import Product
    return Product.objects.create(
        sku='TEST-SKU-001',
        name='Test Product',
        description='A test product',
        cost_price=10.00,
        list_price=20.00,
        sale_price=15.00,
        unit='PCS'
    )

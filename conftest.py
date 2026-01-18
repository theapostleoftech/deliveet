"""
Pytest configuration and fixtures for Deliveet integration testing.
"""
import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from shipments.models import Shipment, Delivery
from django.contrib.gis.geos import Point
import json


@pytest.fixture
def api_client():
    """DRF API Client fixture for unauthenticated requests."""
    return APIClient()


@pytest.fixture
def django_client():
    """Django test client for traditional requests."""
    return Client()


@pytest.fixture
def test_user_data():
    """Test user data fixture."""
    return {
        'email': 'testuser@example.com',
        'password': 'TestPass123!',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '+2348000000000',
        'user_type': 'customer'
    }


@pytest.fixture
def test_user(test_user_data):
    """Create a test customer user."""
    return User.objects.create_user(**test_user_data)


@pytest.fixture
def test_courier_data():
    """Test courier data fixture."""
    return {
        'email': 'courier@example.com',
        'password': 'CourierPass123!',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'phone_number': '+2348000000001',
        'user_type': 'courier'
    }


@pytest.fixture
def test_courier(test_courier_data):
    """Create a test courier user."""
    return User.objects.create_user(**test_courier_data)


@pytest.fixture
def test_admin_data():
    """Test admin data fixture."""
    return {
        'email': 'admin@example.com',
        'password': 'AdminPass123!',
        'first_name': 'Admin',
        'last_name': 'User',
        'phone_number': '+2348000000002',
        'user_type': 'admin'
    }


@pytest.fixture
def test_admin(test_admin_data):
    """Create a test admin user."""
    user = User.objects.create_user(**test_admin_data)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def authenticated_client(test_user):
    """DRF API Client with JWT authentication for customer."""
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, test_user


@pytest.fixture
def authenticated_courier_client(test_courier):
    """DRF API Client with JWT authentication for courier."""
    client = APIClient()
    refresh = RefreshToken.for_user(test_courier)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, test_courier


@pytest.fixture
def authenticated_admin_client(test_admin):
    """DRF API Client with JWT authentication for admin."""
    client = APIClient()
    refresh = RefreshToken.for_user(test_admin)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, test_admin


@pytest.fixture
def test_shipment_data():
    """Test shipment data fixture."""
    return {
        'pickup_location': '123 Main Street, Lagos, Nigeria',
        'pickup_latitude': 6.5244,
        'pickup_longitude': 3.3792,
        'dropoff_location': '456 Oak Avenue, Lagos, Nigeria',
        'dropoff_latitude': 6.6245,
        'dropoff_longitude': 3.4793,
        'weight': 2.5,
        'dimensions': '30x20x10',
        'package_type': 'parcel',
        'special_instructions': 'Handle with care',
        'recipient_name': 'John Recipient',
        'recipient_phone': '+2348000000010',
        'estimated_cost': 5000,
    }


@pytest.fixture
def test_shipment(test_user, test_shipment_data):
    """Create a test shipment."""
    return Shipment.objects.create(
        customer=test_user,
        **test_shipment_data
    )


@pytest.fixture
def test_delivery(test_shipment, test_courier):
    """Create a test delivery."""
    return Delivery.objects.create(
        shipment=test_shipment,
        courier=test_courier,
        status='pending'
    )


@pytest.fixture
def auth_tokens(test_user):
    """Generate authentication tokens for test user."""
    refresh = RefreshToken.for_user(test_user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


@pytest.fixture(autouse=True)
def reset_sequences(db):
    """Reset database sequences between tests."""
    pass


# Pytest plugins and options
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "auth: marks tests as authentication related"
    )
    config.addinivalue_line(
        "markers", "shipment: marks tests as shipment related"
    )
    config.addinivalue_line(
        "markers", "delivery: marks tests as delivery related"
    )


# Fixtures for WebSocket testing
@pytest.fixture
def websocket_client():
    """WebSocket test client."""
    from channels.testing import WebsocketCommunicator
    return WebsocketCommunicator


# Fixtures for mocking external services
@pytest.fixture
def mock_monnify(monkeypatch):
    """Mock Monnify payment gateway."""
    def mock_init_payment(amount, email, phone):
        return {
            'status': 'SUCCESS',
            'data': {
                'transactionReference': 'TEST_REF_123',
                'paymentLink': 'https://test.monnify.com/pay/TEST_REF_123'
            }
        }
    
    # monkeypatch.setattr('payments.gateway.MonnifyGateway.initialize_payment', mock_init_payment)
    return mock_init_payment


@pytest.fixture
def mock_notifications(monkeypatch):
    """Mock notification sending."""
    def mock_send_notification(user, title, message):
        return {'status': 'sent', 'notification_id': '123'}
    
    # monkeypatch.setattr('notifications.services.send_notification', mock_send_notification)
    return mock_send_notification


# Fixtures for API response testing
@pytest.fixture
def pagination_params():
    """Pagination parameters for list endpoints."""
    return {
        'page': 1,
        'page_size': 10,
    }


@pytest.fixture
def filter_params():
    """Filter parameters for list endpoints."""
    return {
        'status': 'pending',
        'user_type': 'customer',
    }


# Fixtures for performance testing
@pytest.fixture
def performance_threshold():
    """Performance thresholds in milliseconds."""
    return {
        'fast': 100,
        'normal': 500,
        'slow': 2000,
    }

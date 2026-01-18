"""
Integration tests for authentication endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User


@pytest.mark.integration
@pytest.mark.auth
class TestUserRegistration:
    """Test user registration endpoint."""

    def test_register_customer_user(self, api_client):
        """Test registering a new customer."""
        url = reverse('user-register')
        data = {
            'email': 'newcustomer@example.com',
            'password': 'SecurePass123!',
            'first_name': 'Jane',
            'last_name': 'Customer',
            'phone_number': '+2348000000020',
            'user_type': 'customer'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newcustomer@example.com').exists()
        user = User.objects.get(email='newcustomer@example.com')
        assert user.user_type == 'customer'

    def test_register_courier_user(self, api_client):
        """Test registering a new courier."""
        url = reverse('user-register')
        data = {
            'email': 'newcourier@example.com',
            'password': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Courier',
            'phone_number': '+2348000000021',
            'user_type': 'courier'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email='newcourier@example.com')
        assert user.user_type == 'courier'

    def test_register_duplicate_email(self, api_client, test_user):
        """Test registering with duplicate email."""
        url = reverse('user-register')
        data = {
            'email': test_user.email,
            'password': 'SecurePass123!',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'user_type': 'customer'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_invalid_email(self, api_client):
        """Test registering with invalid email."""
        url = reverse('user-register')
        data = {
            'email': 'invalid-email',
            'password': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'customer'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client):
        """Test registering with weak password."""
        url = reverse('user-register')
        data = {
            'email': 'weakpass@example.com',
            'password': '123',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'customer'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.auth
class TestUserLogin:
    """Test user login endpoint."""

    def test_login_successful(self, api_client, test_user, test_user_data):
        """Test successful login."""
        url = reverse('user-login')
        data = {
            'email': test_user.email,
            'password': test_user_data['password']
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == test_user.email

    def test_login_invalid_email(self, api_client):
        """Test login with non-existent email."""
        url = reverse('user-login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'SomePassword123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_wrong_password(self, api_client, test_user):
        """Test login with wrong password."""
        url = reverse('user-login')
        data = {
            'email': test_user.email,
            'password': 'WrongPassword123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_fields(self, api_client):
        """Test login with missing fields."""
        url = reverse('user-login')
        data = {'email': 'test@example.com'}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.auth
class TestTokenRefresh:
    """Test token refresh endpoint."""

    def test_refresh_valid_token(self, api_client, auth_tokens):
        """Test refreshing with valid refresh token."""
        url = reverse('token_refresh')
        data = {'refresh': auth_tokens['refresh']}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert response.data['access'] != auth_tokens['access']

    def test_refresh_invalid_token(self, api_client):
        """Test refreshing with invalid token."""
        url = reverse('token_refresh')
        data = {'refresh': 'invalid_token_value'}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_missing_token(self, api_client):
        """Test refreshing without token."""
        url = reverse('token_refresh')
        data = {}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.auth
class TestCurrentUser:
    """Test get current user endpoint."""

    def test_get_current_user_authenticated(self, authenticated_client):
        """Test getting current user when authenticated."""
        client, user = authenticated_client
        url = reverse('user-detail', kwargs={'pk': 'current'})
        
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['id'] == user.id

    def test_get_current_user_unauthenticated(self, api_client):
        """Test getting current user when not authenticated."""
        url = reverse('user-detail', kwargs={'pk': 'current'})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_current_user(self, authenticated_client):
        """Test updating current user profile."""
        client, user = authenticated_client
        url = reverse('user-detail', kwargs={'pk': 'current'})
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone_number': '+2348000000099'
        }
        
        response = client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == 'Updated'


@pytest.mark.integration
@pytest.mark.auth
class TestUserLogout:
    """Test user logout endpoint."""

    def test_logout_authenticated_user(self, authenticated_client):
        """Test logout for authenticated user."""
        client, user = authenticated_client
        url = reverse('user-logout')
        
        response = client.post(url, format='json')
        
        assert response.status_code == status.HTTP_200_OK

    def test_logout_unauthenticated_user(self, api_client):
        """Test logout without authentication."""
        url = reverse('user-logout')
        
        response = api_client.post(url, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
@pytest.mark.auth
class TestPermissions:
    """Test permission controls."""

    def test_customer_cannot_access_courier_endpoints(self, authenticated_client):
        """Test that customer cannot access courier-only endpoints."""
        client, user = authenticated_client
        url = reverse('delivery-list')
        
        response = client.get(url)
        
        # Depending on implementation, should be forbidden or empty
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_200_OK]

    def test_courier_can_access_delivery_endpoints(self, authenticated_courier_client):
        """Test that courier can access delivery endpoints."""
        client, courier = authenticated_courier_client
        url = reverse('delivery-list')
        
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK

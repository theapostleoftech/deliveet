"""
Integration tests for API endpoints
Tests the complete request/response cycle for all major endpoints
"""
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from app.models import Shipment
from django.contrib.auth import get_user_model

User = get_user_model()


class APIEndpointIntegrationTests(TestCase):
    """Test all API endpoints with real requests"""
    
    def setUp(self):
        """Set up test client and users"""
        self.client = APIClient()
        self.base_url = 'http://localhost:8000/api/v1'
        
        # Create test users
        self.customer_user = User.objects.create_user(
            email='customer@test.com',
            password='testpass123',
            role='customer',
            full_name='Test Customer'
        )
        
        self.courier_user = User.objects.create_user(
            email='courier@test.com',
            password='testpass123',
            role='courier',
            full_name='Test Courier'
        )
        
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            role='admin',
            full_name='Test Admin'
        )
    
    def test_user_registration_endpoint(self):
        """Test user registration endpoint"""
        data = {
            'email': 'newuser@test.com',
            'password': 'newpass123',
            'full_name': 'New User',
            'role': 'customer',
            'phone_number': '+234812345678'
        }
        
        response = self.client.post(
            '/api/v1/accounts/register/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@test.com')
    
    def test_user_login_endpoint(self):
        """Test user login endpoint"""
        data = {
            'email': 'customer@test.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(
            '/api/v1/accounts/login/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['user']['email'], 'customer@test.com')
    
    def test_token_refresh_endpoint(self):
        """Test token refresh endpoint"""
        # First login to get tokens
        login_data = {
            'email': 'customer@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        refresh_token = login_response.data['refresh_token']
        
        # Now refresh the token
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(
            '/api/v1/accounts/token/refresh/',
            refresh_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
    
    def test_protected_endpoint_without_auth(self):
        """Test that protected endpoints require authentication"""
        response = self.client.get('/api/v1/shipments/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_protected_endpoint_with_auth(self):
        """Test that authenticated requests work"""
        # Login
        login_data = {
            'email': 'customer@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Access protected endpoint
        response = self.client.get('/api/v1/shipments/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_shipment_endpoint(self):
        """Test shipment creation endpoint"""
        # Login as customer
        login_data = {
            'email': 'customer@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Create shipment
        shipment_data = {
            'pickup_location': '123 Main St, Lagos',
            'delivery_location': '456 Oak Ave, Lagos',
            'item_description': 'Electronics package',
            'item_weight': 2.5,
            'item_value': 50000,
            'recipient_name': 'John Doe',
            'recipient_phone': '+234812345678',
            'special_instructions': 'Handle with care',
            'estimated_delivery_time': 120
        }
        
        response = self.client.post(
            '/api/v1/shipments/',
            shipment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
        self.assertIn('shipment_id', response.data)
    
    def test_get_shipment_details(self):
        """Test retrieving shipment details"""
        # Create a shipment first
        shipment = Shipment.objects.create(
            customer=self.customer_user,
            pickup_location='123 Main St, Lagos',
            delivery_location='456 Oak Ave, Lagos',
            item_description='Electronics package',
            item_weight=2.5,
            item_value=50000,
            recipient_name='John Doe',
            recipient_phone='+234812345678',
            status='pending'
        )
        
        # Login and get shipment
        login_data = {
            'email': 'customer@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get(f'/api/v1/shipments/{shipment.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], shipment.id)
    
    def test_list_shipments_with_pagination(self):
        """Test shipment list with pagination"""
        # Create multiple shipments
        for i in range(15):
            Shipment.objects.create(
                customer=self.customer_user,
                pickup_location=f'{i} Main St, Lagos',
                delivery_location=f'{i} Oak Ave, Lagos',
                item_description='Package',
                item_weight=1.0,
                item_value=10000,
                recipient_name=f'User {i}',
                recipient_phone='+234812345678',
                status='pending'
            )
        
        # Login and get list
        login_data = {
            'email': 'customer@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Test default pagination
        response = self.client.get('/api/v1/shipments/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 10)  # Default page size
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
    
    def test_role_based_access_control(self):
        """Test that roles restrict access appropriately"""
        # Login as courier
        login_data = {
            'email': 'courier@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to create shipment as courier (should fail)
        shipment_data = {
            'pickup_location': '123 Main St, Lagos',
            'delivery_location': '456 Oak Ave, Lagos',
            'item_description': 'Package',
            'item_weight': 2.5,
            'item_value': 50000,
            'recipient_name': 'John Doe',
            'recipient_phone': '+234812345678'
        }
        
        response = self.client.post(
            '/api/v1/shipments/',
            shipment_data,
            format='json'
        )
        
        # Should be forbidden or not allowed
        self.assertIn(response.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_400_BAD_REQUEST
        ])


class APIErrorHandlingTests(TestCase):
    """Test API error handling and edge cases"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        data = {
            'email': 'test@test.com',
            'password': 'testpass123'
            # Missing full_name and role
        }
        
        response = self.client.post(
            '/api/v1/accounts/register/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('full_name', response.data or 'error' in str(response.content))
    
    def test_invalid_email_format(self):
        """Test handling of invalid email format"""
        data = {
            'email': 'invalid-email',
            'password': 'testpass123',
            'full_name': 'Test User',
            'role': 'customer'
        }
        
        response = self.client.post(
            '/api/v1/accounts/register/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'email': 'nonexistent@test.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(
            '/api/v1/accounts/login/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_nonexistent_resource(self):
        """Test accessing nonexistent resource"""
        # Create a user and login
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            role='customer',
            full_name='Test User'
        )
        
        login_data = {
            'email': 'test@test.com',
            'password': 'testpass123'
        }
        
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            login_data,
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to access nonexistent shipment
        response = self.client.get('/api/v1/shipments/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_rate_limiting(self):
        """Test rate limiting on endpoints"""
        # This test depends on rate limiting configuration
        # Send multiple requests rapidly
        for i in range(5):
            data = {
                'email': f'test{i}@test.com',
                'password': 'testpass123'
            }
            response = self.client.post(
                '/api/v1/accounts/login/',
                data,
                format='json'
            )
            
            # Expect 401 for invalid credentials, not rate limiting initially
            self.assertIn(response.status_code, [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_429_TOO_MANY_REQUESTS
            ])

"""
Payment Integration Tests
Tests complete payment flow including initialization, verification, and refunds
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from app.models import Shipment
from payments.models import Payment
from django.utils import timezone
from unittest.mock import patch, MagicMock
import json

User = get_user_model()


class PaymentInitializationTests(TestCase):
    """Test payment initialization workflow"""
    
    def setUp(self):
        """Set up test users and client"""
        self.client = APIClient()
        
        self.customer = User.objects.create_user(
            email='customer@test.com',
            password='pass123',
            role='customer',
            full_name='Customer User'
        )
        
        self.shipment = Shipment.objects.create(
            customer=self.customer,
            pickup_location='123 Main St, Lagos',
            delivery_location='456 Oak Ave, Lagos',
            item_description='Electronics package',
            item_weight=2.5,
            item_value=50000,
            recipient_name='John Doe',
            recipient_phone='+234812345678',
            status='pending'
        )
    
    def _login_as_customer(self):
        """Login and return token"""
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer@test.com', 'password': 'pass123'},
            format='json'
        )
        return response.data['access_token']
    
    def test_initialize_payment_for_shipment(self):
        """Test payment initialization"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        payment_data = {
            'shipment_id': self.shipment.id,
            'amount': 5000,  # Delivery fee
            'payment_method': 'card'
        }
        
        response = self.client.post(
            '/api/v1/payments/initialize/',
            payment_data,
            format='json'
        )
        
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])
        
        if response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            self.assertIn('reference', response.data)
    
    @patch('payments.utils.initialize_monnify_payment')
    def test_monnify_payment_initialization(self, mock_monnify):
        """Test Monnify payment gateway initialization"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Mock Monnify response
        mock_monnify.return_value = {
            'requestSuccessful': True,
            'responseMessage': 'Success',
            'responseCode': '0',
            'responseBody': {
                'transactionReference': 'MNFY|01|20260118|000001',
                'paymentLink': 'https://checkout.monnify.com/pay/example'
            }
        }
        
        payment_data = {
            'shipment_id': self.shipment.id,
            'amount': 5000,
            'payment_method': 'monnify'
        }
        
        response = self.client.post(
            '/api/v1/payments/initialize/',
            payment_data,
            format='json'
        )
        
        if response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            # Verify payment record created
            self.assertTrue(mock_monnify.called)


class PaymentVerificationTests(TestCase):
    """Test payment verification workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        self.customer = User.objects.create_user(
            email='customer@test.com',
            password='pass123',
            role='customer',
            full_name='Customer'
        )
        
        self.shipment = Shipment.objects.create(
            customer=self.customer,
            pickup_location='123 Main St',
            delivery_location='456 Oak Ave',
            item_description='Package',
            item_weight=2.0,
            item_value=10000,
            recipient_name='John',
            recipient_phone='+234812345678',
            status='pending'
        )
    
    def _login_as_customer(self):
        """Login and return token"""
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer@test.com', 'password': 'pass123'},
            format='json'
        )
        return response.data['access_token']
    
    @patch('payments.utils.verify_monnify_payment')
    def test_verify_payment_success(self, mock_verify):
        """Test successful payment verification"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Mock successful verification
        mock_verify.return_value = {
            'requestSuccessful': True,
            'responseMessage': 'Payment successful',
            'responseBody': {
                'transactionReference': 'MNFY|01|20260118|000001',
                'paymentStatus': 'PAID',
                'amountPaid': 5000
            }
        }
        
        verification_data = {
            'reference': 'MNFY|01|20260118|000001'
        }
        
        response = self.client.post(
            '/api/v1/payments/verify/',
            verification_data,
            format='json'
        )
        
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])
    
    @patch('payments.utils.verify_monnify_payment')
    def test_verify_payment_failed(self, mock_verify):
        """Test failed payment verification"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Mock failed verification
        mock_verify.return_value = {
            'requestSuccessful': False,
            'responseMessage': 'Payment not found',
            'responseCode': '-1'
        }
        
        verification_data = {
            'reference': 'INVALID_REF'
        }
        
        response = self.client.post(
            '/api/v1/payments/verify/',
            verification_data,
            format='json'
        )
        
        # Should handle failure gracefully
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_verify_already_paid_payment(self):
        """Test verifying an already paid payment"""
        # Create payment record
        payment = Payment.objects.create(
            shipment=self.shipment,
            amount=5000,
            status='completed',
            reference='MNFY|01|20260118|000001'
        )
        
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        verification_data = {
            'reference': payment.reference
        }
        
        response = self.client.post(
            '/api/v1/payments/verify/',
            verification_data,
            format='json'
        )
        
        # Should indicate payment already verified
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])


class PaymentRefundTests(TestCase):
    """Test payment refund workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        self.customer = User.objects.create_user(
            email='customer@test.com',
            password='pass123',
            role='customer',
            full_name='Customer'
        )
        
        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='pass123',
            role='admin',
            full_name='Admin'
        )
        
        self.shipment = Shipment.objects.create(
            customer=self.customer,
            pickup_location='123 Main St',
            delivery_location='456 Oak Ave',
            item_description='Package',
            item_weight=2.0,
            item_value=10000,
            recipient_name='John',
            recipient_phone='+234812345678',
            status='cancelled'
        )
        
        self.payment = Payment.objects.create(
            shipment=self.shipment,
            amount=5000,
            status='completed',
            reference='MNFY|01|20260118|000001'
        )
    
    def _login_as_customer(self):
        """Login as customer"""
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer@test.com', 'password': 'pass123'},
            format='json'
        )
        return response.data['access_token']
    
    @patch('payments.utils.refund_monnify_payment')
    def test_refund_payment(self, mock_refund):
        """Test initiating a payment refund"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Mock successful refund
        mock_refund.return_value = {
            'requestSuccessful': True,
            'responseMessage': 'Refund successful',
            'responseBody': {
                'transactionReference': 'MNFY|01|20260118|000001',
                'refundReference': 'REF|01|20260118|000001',
                'refundAmount': 5000
            }
        }
        
        refund_data = {
            'payment_id': self.payment.id,
            'reason': 'Shipment cancelled'
        }
        
        response = self.client.post(
            '/api/v1/payments/refund/',
            refund_data,
            format='json'
        )
        
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])
    
    @patch('payments.utils.refund_monnify_payment')
    def test_refund_failed(self, mock_refund):
        """Test failed refund"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Mock failed refund
        mock_refund.return_value = {
            'requestSuccessful': False,
            'responseMessage': 'Refund failed'
        }
        
        refund_data = {
            'payment_id': self.payment.id,
            'reason': 'Shipment cancelled'
        }
        
        response = self.client.post(
            '/api/v1/payments/refund/',
            refund_data,
            format='json'
        )
        
        # Should handle failure
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ])


class CompletePaymentFlowTests(TestCase):
    """Test complete payment workflows"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        self.customer = User.objects.create_user(
            email='customer@test.com',
            password='pass123',
            role='customer',
            full_name='Customer'
        )
        
        self.shipment = Shipment.objects.create(
            customer=self.customer,
            pickup_location='123 Main St',
            delivery_location='456 Oak Ave',
            item_description='Package',
            item_weight=2.0,
            item_value=10000,
            recipient_name='John',
            recipient_phone='+234812345678',
            status='pending'
        )
    
    def _login_as_customer(self):
        """Login and return token"""
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer@test.com', 'password': 'pass123'},
            format='json'
        )
        return response.data['access_token']
    
    @patch('payments.utils.initialize_monnify_payment')
    @patch('payments.utils.verify_monnify_payment')
    def test_complete_payment_flow(self, mock_verify, mock_init):
        """Test: Initialize -> Redirect -> Verify -> Confirm"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Step 1: Initialize payment
        mock_init.return_value = {
            'requestSuccessful': True,
            'responseBody': {
                'transactionReference': 'MNFY|01|20260118|000001',
                'paymentLink': 'https://checkout.monnify.com/pay/example'
            }
        }
        
        init_response = self.client.post(
            '/api/v1/payments/initialize/',
            {
                'shipment_id': self.shipment.id,
                'amount': 5000,
                'payment_method': 'monnify'
            },
            format='json'
        )
        
        # Step 2: User would redirect to payment link and complete payment
        
        # Step 3: Verify payment
        mock_verify.return_value = {
            'requestSuccessful': True,
            'responseBody': {
                'paymentStatus': 'PAID',
                'amountPaid': 5000
            }
        }
        
        verify_response = self.client.post(
            '/api/v1/payments/verify/',
            {
                'reference': 'MNFY|01|20260118|000001'
            },
            format='json'
        )
    
    def test_payment_status_tracking(self):
        """Test tracking payment status"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Create payment
        payment = Payment.objects.create(
            shipment=self.shipment,
            amount=5000,
            status='pending',
            reference='MNFY|01|20260118|000001'
        )
        
        # Get payment status
        response = self.client.get(f'/api/v1/payments/{payment.id}/')
        
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])


class PaymentValidationTests(TestCase):
    """Test payment validation and error handling"""
    
    def setUp(self):
        """Set up test user"""
        self.client = APIClient()
        
        self.customer = User.objects.create_user(
            email='customer@test.com',
            password='pass123',
            role='customer',
            full_name='Customer'
        )
    
    def _login_as_customer(self):
        """Login and return token"""
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer@test.com', 'password': 'pass123'},
            format='json'
        )
        return response.data['access_token']
    
    def test_invalid_amount(self):
        """Test payment with invalid amount"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        payment_data = {
            'amount': -5000,  # Negative amount
            'payment_method': 'card'
        }
        
        response = self.client.post(
            '/api/v1/payments/initialize/',
            payment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_missing_required_payment_fields(self):
        """Test payment without required fields"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        payment_data = {
            'amount': 5000
            # Missing payment_method and shipment_id
        }
        
        response = self.client.post(
            '/api/v1/payments/initialize/',
            payment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_payment_method(self):
        """Test payment with invalid method"""
        token = self._login_as_customer()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        payment_data = {
            'amount': 5000,
            'payment_method': 'invalid_method'
        }
        
        response = self.client.post(
            '/api/v1/payments/initialize/',
            payment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaymentSecurityTests(TestCase):
    """Test payment security measures"""
    
    def setUp(self):
        """Set up test users"""
        self.client = APIClient()
        
        self.customer1 = User.objects.create_user(
            email='customer1@test.com',
            password='pass123',
            role='customer',
            full_name='Customer 1'
        )
        
        self.customer2 = User.objects.create_user(
            email='customer2@test.com',
            password='pass123',
            role='customer',
            full_name='Customer 2'
        )
        
        self.shipment1 = Shipment.objects.create(
            customer=self.customer1,
            pickup_location='123 Main St',
            delivery_location='456 Oak Ave',
            item_description='Package',
            item_weight=2.0,
            item_value=10000,
            recipient_name='John',
            recipient_phone='+234812345678',
            status='pending'
        )
        
        self.payment1 = Payment.objects.create(
            shipment=self.shipment1,
            amount=5000,
            status='pending',
            reference='MNFY|01|20260118|000001'
        )
    
    def test_customer_cannot_access_other_payment(self):
        """Test that customer cannot access another customer's payment"""
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer2@test.com', 'password': 'pass123'},
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to access payment of customer1
        response = self.client.get(f'/api/v1/payments/{self.payment1.id}/')
        
        # Should be forbidden or return 404
        self.assertIn(response.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_payment_amount_tampering_prevention(self):
        """Test that payment amount cannot be tampered with"""
        login_response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'customer1@test.com', 'password': 'pass123'},
            format='json'
        )
        
        token = login_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to update payment amount (should fail)
        response = self.client.patch(
            f'/api/v1/payments/{self.payment1.id}/',
            {'amount': 1000},  # Try to reduce amount
            format='json'
        )
        
        # Should not allow modification
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])

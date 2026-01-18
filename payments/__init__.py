"""
Payment Processing Module
Monnify Payment Gateway Integration
"""
from django.conf import settings
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MonnifyPaymentGateway:
    """
    Monnify Payment Gateway Integration
    Handles payment initialization, verification, and settlement
    """
    
    BASE_URL = settings.MONNIFY_BASE_URL
    API_KEY = settings.MONNIFY_API_KEY
    PUBLIC_KEY = settings.MONNIFY_PUBLIC_KEY
    SECRET_KEY = settings.MONNIFY_SECRET_KEY
    CONTRACT_CODE = settings.MONNIFY_CONTRACT_CODE
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        })
    
    def initialize_payment(self, 
                          customer_email: str,
                          customer_name: str,
                          amount: float,
                          transaction_ref: str,
                          payment_description: str = "Deliveet Payment",
                          callback_url: str = None) -> dict:
        """
        Initialize a payment transaction
        
        Args:
            customer_email: Customer email
            customer_name: Customer name
            amount: Amount in NGN
            transaction_ref: Unique transaction reference
            payment_description: Payment description
            callback_url: Webhook callback URL
            
        Returns:
            dict: Payment initialization response
        """
        try:
            payload = {
                "amount": amount,
                "customerEmail": customer_email,
                "customerName": customer_name,
                "paymentReference": transaction_ref,
                "paymentDescription": payment_description,
                "currencyCode": "NGN",
                "contractCode": self.CONTRACT_CODE,
                "redirectUrl": callback_url or f"{settings.NOTIFICATION_URL}/payments/callback",
                "incomeSplitConfig": [
                    {
                        "subAccountCode": "DELIVEET",
                        "splitType": "FLAT",
                        "splitValue": 100,
                        "splitRatio": 100
                    }
                ]
            }
            
            response = self.session.post(
                f"{self.BASE_URL}/api/v1/transactions/init-transaction",
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('requestSuccessful'):
                logger.info(f"Payment initialized: {transaction_ref}")
                return {
                    'status': 'success',
                    'data': result.get('responseBody'),
                    'payment_link': result.get('responseBody', {}).get('checkoutUrl')
                }
            else:
                logger.error(f"Payment initialization failed: {result}")
                return {'status': 'failed', 'message': result.get('responseMessage')}
                
        except Exception as e:
            logger.error(f"Error initializing payment: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def verify_transaction(self, transaction_ref: str) -> dict:
        """
        Verify a transaction status
        
        Args:
            transaction_ref: Transaction reference to verify
            
        Returns:
            dict: Transaction verification response
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/api/v1/transactions/query",
                params={'transactionReference': transaction_ref},
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('requestSuccessful'):
                transaction = result.get('responseBody', {})
                payment_status = transaction.get('paymentStatus')
                
                logger.info(f"Transaction verified: {transaction_ref} - Status: {payment_status}")
                return {
                    'status': 'success',
                    'payment_status': payment_status,
                    'amount': transaction.get('amount'),
                    'transaction_data': transaction
                }
            else:
                logger.error(f"Verification failed: {result}")
                return {'status': 'failed', 'message': result.get('responseMessage')}
                
        except Exception as e:
            logger.error(f"Error verifying transaction: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def get_bank_transfer_details(self) -> dict:
        """
        Get bank transfer details for direct payment
        
        Returns:
            dict: Bank transfer details
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/api/v1/bank-transfer/get-account-details",
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('requestSuccessful'):
                return {
                    'status': 'success',
                    'data': result.get('responseBody')
                }
            else:
                return {'status': 'failed', 'message': result.get('responseMessage')}
                
        except Exception as e:
            logger.error(f"Error getting bank transfer details: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def get_transaction_status(self, transaction_ref: str) -> str:
        """
        Simple method to get transaction status
        
        Args:
            transaction_ref: Transaction reference
            
        Returns:
            str: Payment status (PAID, PENDING, FAILED, etc.)
        """
        response = self.verify_transaction(transaction_ref)
        if response['status'] == 'success':
            return response.get('payment_status', 'UNKNOWN')
        return 'ERROR'


# Convenience functions
def initialize_payment(customer_email, customer_name, amount, transaction_ref, **kwargs):
    """Initialize a payment"""
    gateway = MonnifyPaymentGateway()
    return gateway.initialize_payment(
        customer_email, customer_name, amount, transaction_ref, **kwargs
    )


def verify_payment(transaction_ref):
    """Verify a payment"""
    gateway = MonnifyPaymentGateway()
    return gateway.verify_transaction(transaction_ref)


def get_payment_status(transaction_ref):
    """Get payment status"""
    gateway = MonnifyPaymentGateway()
    return gateway.get_transaction_status(transaction_ref)

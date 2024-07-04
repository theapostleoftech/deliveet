"""
This module provides methods to initiate payments
"""
import requests

from django.conf import settings


class Paystack:
    """
    This class provides methods to initiate payments
    """
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"

    def verify_transaction(self, transaction_reference, *args, **kwargs):
        """
        This initializes the paystack api key
        """
        path = f'transaction/verify/{transaction_reference}'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            "Content-Type": "application/json",
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']

        response_data = response.json()

        return response_data['status'], response_data['message']

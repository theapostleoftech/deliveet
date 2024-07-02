"""
This contains form for the finance app
"""
from django import forms


class TransactionForm(forms.Form):
    """
    This is the form for the transaction model
    """
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

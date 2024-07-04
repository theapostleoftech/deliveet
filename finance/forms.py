"""
This contains form for the finance app
"""
from django import forms

from finance.models import WalletTransaction


class TransactionForm(forms.ModelForm):
    """
    This is the form for the transaction model
    """

    class Meta:
        model = WalletTransaction
        fields = ('amount',)

"""
This contains all the forms for the profile app
"""
from django import forms

from accounts.models import Customer, Courier


class CustomerUpdateForm(forms.ModelForm):
    """
    This is form is used to update customer details
    """

    class Meta:
        model = Customer
        fields = ['gender']


class CourierUpdateForm(forms.ModelForm):
    """
    This form is used to update courier details
    """

    class Meta:
        model = Courier
        fields = ['gender']

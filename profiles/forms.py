"""
This contains all the forms for the profile app
"""
from django import forms

from accounts.models import Customer, Courier


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'gender']


class CourierUpdateForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ['phone', 'gender']

"""
This module provides forms for creating and updating accounts.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction

from accounts.models import UserAccount, Customer, Courier
from app.forms import BaseForm


class SignUpForm(UserCreationForm):
    """
    This form is used to create a new user.
    """

    class Meta(UserCreationForm.Meta):
        model = UserAccount
        fields = ("email", "first_name", "last_name", "account_type",)

    def clean_email(self):
        """
        This validates that the email address is unique.
        :return: a validated email address.
        """
        email = self.cleaned_data.get("email")
        if UserAccount.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists. Try with another email.")
        return email

    def clean_password2(self):
        """
        This validates that the two password are correct.
        :return: a validated password
        """
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two passwords entered are not the same. Try again!")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        """
        This method saves a new user into the database.
        It also creates the corresponding profiles of the user
        :param commit:
        :return: a new user account and corresponding profiles
        """
        user = super().save(commit=False)
        if self.cleaned_data["account_type"] == "courier":
            user.is_courier = True
            courier = Courier.objects.create(user=user)
            courier.save()
        elif self.cleaned_data["account_type"] == "customer":
            user.is_customer = True
            customer = Customer.objects.create(user=user)
            customer.save()
        else:
            user.is_customer = True
            customer = Customer.objects.create(user=user)
            customer.save()
        if commit:
            user.save()
        return user

    pass


class SignInForm(forms.Form):
    """
    This form is used to login a user.
    """
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

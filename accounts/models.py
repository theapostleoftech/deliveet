"""
This contains models for the account app
"""
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse

from accounts.managers import UserAccountManager
from app.models import PhoneField, ProfileBaseModel


# Create your models here.
class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    This class contains fields for the user account
    """

    class UserAccountType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        COURIER = "courier", "Courier"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    account_type = models.CharField(
        choices=UserAccountType.choices,
        max_length=10,
        default=UserAccountType.CUSTOMER,
        help_text='Select the type of account you wish to create'
    )
    first_name = models.CharField(
        max_length=255,
        help_text='Type in your first name',
    )
    last_name = models.CharField(
        max_length=255,
        help_text='Type in your last name',
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        help_text='Type in your email address',
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )
    is_customer = models.BooleanField(
        default=False
    )
    is_courier = models.BooleanField(
        default=False
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        auto_now=True
    )
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name_plural = 'User Accounts'

    def __str__(self) -> str:
        """
        This prints the string
        representation of the user account
        """
        return self.email

    def get_full_name(self) -> str:
        """
        This prints a string representation
        of the full name of the user.
        """
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

    def get_short_name(self) -> str:
        """
        This prints a string representation
        of the user's first name.
        """
        return f'{self.first_name}'

    pass


class Customer(ProfileBaseModel):
    """
    This is the profile model for all customer accounts
    """
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='customer_account',
        limit_choices_to={'account_type': 'customer'},
    )

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self) -> str:
        return self.user.email

    def get_absolute_url(self):
        return reverse('profiles:customer_details', kwargs={'uuid': str(self.user_id)})

    pass


class Courier(ProfileBaseModel):
    """
    This is the profile model for all courier accounts
    """
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='courier_account',
        limit_choices_to={'account_type': 'courier'},
    )

    class Meta:
        verbose_name_plural = 'Couriers'

    def __str__(self) -> str:
        return self.user.email

    def get_absolute_url(self):
        return reverse('profiles:courier_details', args=[str(self.pk)])

    pass

"""
This contains miscellaneous and core models for the deliveet app
"""
import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from deliveet.utils.validators import phone_number_validator


# Create your models here.
class BaseModel(models.Model):
    """
    This is the base model which
    other models will inherit from.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class PhoneField(PhoneNumberField):
    """
    This class defines a custom phone number field
    """
    default_validators = [phone_number_validator]


class ProfileBaseModel(models.Model):
    """
    This is the base model for all user profiles
    """
    phone = PhoneField(
        help_text='Type in your phone number',
        unique=True,
    )

    class GenderChoice(models.TextChoices):
        """
        This is a field choice for genders
        """
        Male = 'Male', 'Male'
        Female = 'Female', 'Female'

    gender = models.CharField(
        choices=GenderChoice.choices,
        max_length=10,
        default=GenderChoice.Male,
        help_text='Select your sex',
    )

    class Meta:
        abstract = True

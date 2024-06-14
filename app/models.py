"""
This contains miscellaneous and core models for the deliveet app
"""
import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from uloahia.utils.validators import phone_number_validator


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

"""
This contains different validators for some model fields
"""
from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number


def phone_number_validator(phone, country=None):
    """
    This function validates phone numbers
    """
    phone_number = to_python(phone, country)
    if (
            phone_number and not is_possible_number(phone_number)
            or not phone_number.is_valid()
    ):
        raise ValidationError(
            'The phone number entered is not valid. Please try again.'
        )
    return phone_number
    pass

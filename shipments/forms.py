"""
This contains all the forms for the shipments app.
"""
from django import forms

from shipments.models import Delivery


class DeliveryItemForm(forms.ModelForm):
    """
    This renders form for the item to be delivered
    """

    class Meta:
        model = Delivery
        fields = ('item_name', 'item_type', 'size', 'quantity', 'photo')


class DeliveryPickupForm(forms.ModelForm):
    """
    This renders form for pickup
    """

    class Meta:
        model = Delivery
        fields = ['pickup_address', 'pickup_latitude', 'pickup_longitude', 'sender_name', 'sender_phone', ]


class DeliveryRecipientForm(forms.ModelForm):
    """
    This renders forms for Delivery Recipient
    """

    class Meta:
        model = Delivery
        fields = ['delivery_address', 'delivery_latitude', 'delivery_longitude', 'recipient_name', 'recipient_phone', ]


class PaymentMethodForm(forms.ModelForm):
    """
    This renders forms for the transaction model
    """

    class Meta:
        model = Delivery
        fields = ['payment_method', ]

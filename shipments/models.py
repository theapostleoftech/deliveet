"""
This contains all models for the shipments app.
"""
import secrets
import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer, Courier
from app.models import BaseModel
from deliveet.utils.finance import Paystack


# Create your models here.
class Delivery(BaseModel):
    """
    This contains fields for requesting delivery of items
    """

    class StatusChoices(models.TextChoices):
        """
        This defines the different statuses of delivery
        """
        CREATING = 'creating', 'Creating'
        PROCESSING = 'processing', 'Processing'
        PICKUP_IN_PROGRESS = 'pickup_in_progress', 'Pickup in progress'
        DELIVERY_IN_PROGRESS = 'in-progress', 'Delivery In Progress'
        COMPLETED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'

    class ItemTypeChoices(models.TextChoices):
        """
        This defines the type of item to be delivered
        """
        CLOTHING = 'clothing', 'Clothing'
        FOOD = 'Food', 'Food'
        DOCUMENTS = 'documents', 'Documents'
        PHARMACEUTICALS = 'pharmaceuticals', 'Pharmaceuticals'
        ELECTRONICS = 'electronics', 'Electronics'
        GOODS = 'goods', 'Goods'

    class SizeChoices(models.TextChoices):
        """
        This defines the items to be delivered
        """
        SMALL = 'small', 'Small'
        MEDIUM = 'medium', 'Medium'
        LARGE = 'large', 'Large'
        EXTRA_LARGE = 'extra_large', 'Extra Large'

    class PaymentMethodChoices(models.TextChoices):
        """"
        This is the various choices for payment
        """
        CARD = 'card', 'Card Payment'
        COD = 'cod', 'Cash on Delivery'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='user_deliveries',
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.CASCADE,
        related_name='courier_deliveries',
        null=True,
        blank=True
    )
    item_name = models.CharField(
        help_text='Name of item to be delivered',
        verbose_name='Item Name',
        max_length=255
    )
    item_type = models.CharField(
        max_length=50,
        choices=ItemTypeChoices.choices,
        default=ItemTypeChoices.GOODS,
        help_text='Select the type of item to be delivered'
    )
    size = models.CharField(
        max_length=20,
        choices=SizeChoices.choices,
        default=SizeChoices.SMALL,
        help_text='Select the size of type to be delivered'
    )
    quantity = models.PositiveIntegerField(
        default=1
    )
    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.CREATING
    )

    pickup_address = models.CharField(
        max_length=255,
        null=True,
    )
    pickup_latitude = models.FloatField(
        default=0
    )
    pickup_longitude = models.FloatField(
        default=0
    )
    sender_name = models.CharField(
        help_text='Name of the sender or the person to be picked up from',
        max_length=255,
        null=True,
    )
    sender_phone = PhoneNumberField(
        help_text='Phone number of the sender or the person to be picked up from',
        max_length=50,
        null=True
    )

    # Step 3
    delivery_address = models.CharField(
        max_length=255,
        null=True
    )
    delivery_latitude = models.FloatField(
        default=0
    )
    delivery_longitude = models.FloatField(
        default=0
    )
    recipient_name = models.CharField(
        help_text='Name of the receiver or the person to be delivered to',
        max_length=255,
        null=True
    )
    recipient_phone = PhoneNumberField(
        help_text='Name of the receiver or the person to be delivered to',
        max_length=50,
        null=True
    )
    duration = models.IntegerField(
        default=0
    )
    distance = models.FloatField(
        default=0
    )
    price = models.FloatField(
        default=0
    )

    pickedup_at = models.DateTimeField(
        null=True,
        blank=True
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )
    tracking_number = models.CharField(
        max_length=255,
        default='',
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CARD
    )

    class Meta:
        """"
        This is the metaclass for the model
        """
        ordering = ['-created_at', ]
        verbose_name_plural = 'Deliveries'
        # indexes = ['tracking_number']

    def __str__(self):
        """
        This returns a string representation of the model
        """
        return self.item_name

    # def __str__(self):
    #     """
    #     This returns a string representation of the model
    #     """
    #     return f"{self.get_payment_method_display()}"

    def save(self, *args, **kwargs):
        """
        This is the save method for the delivery model
        """
        while not self.tracking_number:
            tracking_number = secrets.token_urlsafe(16)
            existing_tracking_number = Delivery.objects.filter(
                tracking_number=tracking_number
            ).first()
            if not existing_tracking_number:
                self.tracking_number = tracking_number
        super().save(*args, **kwargs)


#
# class TransactionMethod(BaseModel):
#     """
#     This defines the payment method
#     """
#     delivery = models.ForeignKey(
#         Delivery,
#         on_delete=models.CASCADE,
#         related_name='transaction_methods',
#         null=True,
#     )
#
#     class MethodChoices(models.TextChoices):
#         """"
#         This is the various choices for payment
#         """
#         CARD = 'card', 'Card'
#         COD = 'cod', 'Cash on Delivery'
#
#     payment_method = models.CharField(
#         max_length=50,
#         choices=MethodChoices.choices,
#         default=MethodChoices.CARD
#     )
#
#     def __str__(self):
#         """
#         This returns a string representation of the model
#         """
#         return f"{self.get_payment_method_display()} for {self.delivery}"


class DeliveryTransaction(BaseModel):
    """
    This contains fields for delivery transactions
    """
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name='delivery_transactions',
    )

    class PaymentStatus(models.TextChoices):
        NOT_PAID = 'not_paid', 'Not Paid'
        PAID = 'paid', 'Paid'

    amount = models.DecimalField(
        max_digits=10,
        default=0,
        decimal_places=2,
    )
    transaction_reference = models.CharField(
        max_length=255,
        default='',
        blank=True
    )
    transaction_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_PAID,
    )
    transaction_verified = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.transaction_reference

    def save(self, *args, **kwargs):
        """
        This is the save method for the wallet transaction
        """
        while not self.transaction_reference:
            transaction_reference = secrets.token_urlsafe(16)
            existing_transaction_reference = DeliveryTransaction.objects.filter(
                transaction_reference=transaction_reference
            ).first()
            if not existing_transaction_reference:
                self.transaction_reference = transaction_reference
        super().save(*args, **kwargs)

    def amount_value(self):
        """
        This changes the amount to naira by multiplying
        the amount by 100
        """
        one_naira = 100
        return int(self.amount) * one_naira

    def verify_transaction(self):
        paystack = Paystack()
        status, result = paystack.verify_transaction(self.transaction_reference, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    pass

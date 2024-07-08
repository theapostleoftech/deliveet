"""
This contains all the models for the finance app.
"""
import secrets

from django.db import models

from accounts.models import UserAccount
from app.models import BaseModel
from deliveet.utils.finance import Paystack


class Wallet(BaseModel):
    """
    This is model contains field for the user wallet
    """
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE
    )
    currency = models.CharField(
        max_length=50,
        default='NGN'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        """
        This is the string representation of the wallet
        :return: The user who has the wallet
        """
        return self.user.__str__()


class WalletTransaction(BaseModel):
    """
    This is model contains field for the user wallet transactions
    """
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
    )
    wallet = models.ForeignKey(
        Wallet,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_wallet_transactions'
    )
    transaction_type = models.CharField(
        max_length=50,
        choices=TRANSACTION_TYPES,
        default='Deposit'
    )
    amount = models.DecimalField(
        max_digits=10,
        null=True,
        decimal_places=2,
    )
    transaction_reference = models.CharField(
        max_length=50,
        default='',
        blank=True
    )
    transaction_verified = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        This is the string representation of the wallet transaction
        :return: The user who performed the transactions
        """
        return self.transaction_reference

    def save(self, *args, **kwargs):
        """
        This is the save method for the wallet transaction
        """
        while not self.transaction_reference:
            transaction_reference = secrets.token_urlsafe(16)
            existing_transaction_reference = WalletTransaction.objects.filter(
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

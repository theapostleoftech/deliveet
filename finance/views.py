"""
This contains all the views related to finance.
"""
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from finance.forms import TransactionForm
from finance.models import WalletTransaction, Wallet
from shipments.models import Delivery

# Paystack Variables
_public_key = settings.PAYSTACK_PUBLIC_KEY


@method_decorator([login_required], name='dispatch')
class WalletView(TemplateView):
    """
    This view displays the wallet info and transactions.
    """
    template_name = 'finance/wallet.html'

    def get_context_data(self, **kwargs):
        """
        This function helps to return the details of the wallet and updates it for couriers
        """
        context = super().get_context_data(**kwargs)

        # Get or create the user's wallet
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)

        # Check if the user is a courier
        if self.request.user.account_type == 'courier':
            self.update_courier_wallet(wallet)

        # Add wallet balance to context
        context['wallet_balance'] = wallet.balance

        # Optionally, add recent transactions
        context['recent_transactions'] = WalletTransaction.objects.filter(wallet=wallet).order_by('-created_at')[:5]

        return context

    @transaction.atomic
    def update_courier_wallet(self, wallet):
        """
        Update the courier's wallet with their earnings
        """
        # Get the timestamp of the last earnings update
        last_update = WalletTransaction.objects.filter(
            wallet=wallet,
        ).order_by('-created_at').first()

        last_update_time = last_update.created_at if last_update else timezone.make_aware(timezone.datetime.min)

        # Calculate courier's earnings
        new_delivery_tasks = Delivery.objects.filter(
            courier=self.request.user.courier_account,
            status=Delivery.StatusChoices.COMPLETED,
            delivered_at__gt=last_update_time,

        )
        total_price = new_delivery_tasks.aggregate(Sum('price'))['price__sum'] or Decimal('0')
        courier_earnings = (total_price * Decimal('0.9')).quantize(Decimal('0.01'))

        if courier_earnings > Decimal('0'):
            # Create a transaction for the earnings
            WalletTransaction.objects.create(
                wallet=wallet,
                amount=courier_earnings,
            )

            # Update wallet balance
            wallet.balance += courier_earnings
            wallet.save()


@login_required
def initiate_transaction(request: HttpRequest) -> HttpResponse:
    """
    This view is used to initiate a transaction.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        # amount = request.POST['amount']
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.email = request.user.email
            transaction.save()

            context = {
                'transaction': transaction,
                'field_values': request.POST,
                'paystack_pub_key': _public_key,
                'amount_value': transaction.amount_value(),
            }

            return render(
                request,
                'finance/initiate_transaction.html',
                context
            )
    else:
        form = TransactionForm(initial={'email': request.user.email})

    return render(request, 'finance/transaction.html', {'form': form})


@login_required
def verify_transaction(request, transaction_reference):
    """
    This view is used to verify a transaction.
    """
    transaction_obj = get_object_or_404(WalletTransaction, transaction_reference=transaction_reference)

    # Check if the transaction has already been verified
    if transaction_obj.transaction_verified:
        messages.info(request, 'This transaction has already been processed.')
        return redirect('finance:wallet')
    else:
        verified = transaction_obj.verify_transaction()

        if verified:
            with transaction.atomic():
                user_wallet = Wallet.objects.select_for_update().get(user=request.user)
                user_wallet.balance += transaction_obj.amount
                user_wallet.save()

                # Mark the transaction as verified
                transaction_obj.transaction_verified = True
                transaction_obj.save()

            messages.success(request, 'Wallet funding successful')
        else:
            messages.error(request, 'Transaction verification failed')

    context = {
        'transaction_reference': transaction_obj.transaction_reference,
        'amount': transaction_obj.amount,
        'transaction_verified': transaction_obj.transaction_verified,
    }

    return render(request, "finance/success.html", context)

"""
This contains all the views related to finance.
"""
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView

from finance.forms import TransactionForm
from finance.models import WalletTransaction, Wallet

# Paystack Variables
_public_key = settings.PAYSTACK_PUBLIC_KEY


class WalletView(TemplateView):
    """
    This view displays the wallet info and transactions.
    """
    template_name = 'finance/wallet.html'


def initiate_transaction(request):
    """
    This view is used to initiate a transaction.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        # amount = request.POST['amount']
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # wallet, created = Wallet.objects.get_or_create(user=request.user)

            transaction = WalletTransaction.objects.create(
                amount=amount,
                # wallet=wallet,
                transaction_type='Deposit',
            )
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
        form = TransactionForm()

    return render(request, 'finance/transaction.html', {'form': form})


def verify_transaction(request, transaction_reference):
    """
    This view is used to verify a transaction.
    """
    transaction = WalletTransaction.objects.get(transaction_reference=transaction_reference)
    verified = transaction.verify_transaction()

    if verified:
        user_wallet = Wallet.objects.get(user=request.user)
        user_wallet.balance += transaction.amount
        user_wallet.save()
        messages.success(request, f'Wallet funding successful')
        # print(request.user.username, " funded wallet successfully")
        return render(request, "finance/success.html")
    return render(request, "finance/success.html")

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from finance.forms import TransactionForm
from shipments.models import Delivery, TransactionMethod, DeliveryTransaction


# Create your views here.


class ShipmentView(LoginRequiredMixin, TemplateView):
    """
    This class shows the shipping dashboard`
    """
    template_name = 'shipments/shipment.html'


class ChooseTransactionMethodView(LoginRequiredMixin, FormView):
    template_name = 'shipments/choose_transaction_method.html'
    form_class = TransactionForm

    def dispatch(self, request, *args, **kwargs):
        self.delivery = Delivery.objects.get(pk=self.kwargs['delivery_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        method = form.cleaned_data['transaction_method']
        transaction_method, _ = TransactionMethod.objects.get_or_create(payment_method=method)

        delivery_transaction = DeliveryTransaction.objects.create(
            delivery=self.delivery,
            transaction_method=transaction_method,
            amount=self.delivery.price
        )

        if method == TransactionMethod.MethodChoices.CARD:
            # Redirect to payment gateway
            return redirect(reverse('payment_gateway', kwargs={'transaction_id': delivery_transaction.id}))
        elif method == TransactionMethod.MethodChoices.COD:
            # Mark as COD and redirect to confirmation page
            delivery_transaction.transaction_status = DeliveryTransaction.PaymentStatus.NOT_PAID
            delivery_transaction.save()
            return redirect(reverse('cod_confirmation', kwargs={'transaction_id': delivery_transaction.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery'] = self.delivery
        return context


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView

from finance.forms import TransactionForm
from shipments.forms import DeliveryItemForm, DeliveryPickupForm, DeliveryRecipientForm
from shipments.models import Delivery, TransactionMethod, DeliveryTransaction


# Create your views here.


# class ShipmentView(LoginRequiredMixin, TemplateView):
#     """
#     This class shows the shipping dashboard`
#     """
#     template_name = 'shipments/shipment.html'


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


class ShipmentView(LoginRequiredMixin, ListView):
    """
    This lists the ongoing delivery of the user
    """
    template_name = 'shipments/shipment.html'
    context_object_name = 'deliveries'
    model = Delivery

    def get_queryset(self):
        return Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status__in=[
                Delivery.StatusChoices.PROCESSING,
                Delivery.StatusChoices.PICKUP_IN_PROGRESS,
                Delivery.StatusChoices.DELIVERY_IN_PROGRESS,
            ]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_deliveries = Delivery.objects.filter(customer=self.request.user.customer_account).count()

        deliveries_completed = Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status=Delivery.StatusChoices.COMPLETED
        ).count()

        deliveries_in_progress = Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status__in=[
                Delivery.StatusChoices.PROCESSING,
                Delivery.StatusChoices.PICKUP_IN_PROGRESS,
                Delivery.StatusChoices.DELIVERY_IN_PROGRESS,
            ]
        ).count()

        context['total_deliveries'] = total_deliveries
        context['deliveries_completed'] = deliveries_completed
        context['deliveries_in_progress'] = deliveries_in_progress

        return context


def create_delivery_view(request):
    """
    This handles view for creation of delivery tasks
    """
    task_owner = request.user.customer_account

    existing_delivery_task = Delivery.objects.filter(
        customer=task_owner,
        status__in=[
            Delivery.StatusChoices.PROCESSING,
            Delivery.StatusChoices.PICKUP_IN_PROGRESS,
            Delivery.StatusChoices.DELIVERY_IN_PROGRESS,
        ]
    ).exists()
    if existing_delivery_task:
        messages.info(request, 'You currently have an ongoing delivery request.')
        return redirect(reverse('shipments:shipment_index'))

    creating_delivery_task = Delivery.objects.filter(
        customer=task_owner,
        status=Delivery.StatusChoices.CREATING

    ).last()
    item_form = DeliveryItemForm(instance=creating_delivery_task)
    pickup_form = DeliveryPickupForm(instance=creating_delivery_task)
    delivery_form = DeliveryRecipientForm(instance=creating_delivery_task)

    if request.method == 'POST':
        if request.POST.get('step') == '1':
            item_form = DeliveryItemForm(request.POST, instance=creating_delivery_task)
            if item_form.is_valid():
                creating_delivery_task = item_form.save(commit=False)
                creating_delivery_task.customer = task_owner
                creating_delivery_task.save()
                return redirect(reverse('shipments:create_delivery'))

    if not creating_delivery_task:
        progress = 1

    return render(request, 'shipments/create_delivery.html',
                  {
                      'delivery_task': creating_delivery_task,
                      'step': progress,
                      'item_form': item_form,
                  })

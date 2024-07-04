import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView

from finance.forms import TransactionForm
from shipments.forms import DeliveryItemForm, DeliveryPickupForm, DeliveryRecipientForm, PaymentMethod
from shipments.models import Delivery, DeliveryTransaction


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
    payment_form = PaymentMethod(instance=creating_delivery_task)

    map_url = ("https://maps.googleapis.com/maps/api/distancematrix/json?origins"
               "={}&destinations={}&mode=transit&key={}").format(
        creating_delivery_task.pickup_address if creating_delivery_task else '',
        creating_delivery_task.delivery_address if creating_delivery_task else '',
        settings.GOOGLE_MAP_API_KEY,
    )
    price_per_km = 100

    if request.method == 'POST':
        if request.POST.get('step') == '1':
            item_form = DeliveryItemForm(request.POST, instance=creating_delivery_task)
            if item_form.is_valid():
                creating_delivery_task = item_form.save(commit=False)
                creating_delivery_task.customer = task_owner
                creating_delivery_task.save()
                return redirect(reverse('shipments:create_delivery'))
        elif request.POST.get('step') == '2':
            pickup_form = DeliveryPickupForm(request.POST, instance=creating_delivery_task)
            if pickup_form.is_valid():
                creating_delivery_task = pickup_form.save()
                return redirect(reverse('shipments:create_delivery'))
        elif request.POST.get('step') == '3':
            delivery_form = DeliveryRecipientForm(request.POST, instance=creating_delivery_task)
            if delivery_form.is_valid():
                creating_delivery_task = delivery_form.save()
                try:
                    response = requests.get(map_url)
                    distance = response.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = response.json()['rows'][0]['elements'][0]['duration']['value']
                    creating_delivery_task.distance = round(distance / 1000, 2)
                    creating_delivery_task.duration = int(duration / 60)
                    creating_delivery_task.price = creating_delivery_task.distance * price_per_km
                    creating_delivery_task.save()
                except Exception as e:
                    messages.error(request, str(e))
                return redirect(reverse('shipments:create_delivery'))
        elif request.POST.get('step') == '4':
            payment_form = PaymentMethod(request.POST, instance=creating_delivery_task)
            if payment_form.is_valid():
                creating_delivery_task = payment_form.save()
                if creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.COD:
                    creating_delivery_task.status = Delivery.StatusChoices.PROCESSING
                    creating_delivery_task.save()
                    messages.success(request, 'Delivery task created successfully.')
                    return redirect(reverse('shipments:shipment_index'))
                elif creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.CARD:
                    # Create a DeliveryTransaction
                    transaction = DeliveryTransaction.objects.create(
                        delivery=creating_delivery_task,
                        amount=creating_delivery_task.price
                    )
                    return redirect(reverse('finance:initiate_transaction',))

    if not creating_delivery_task:
        progress = 1
    elif creating_delivery_task.recipient_name:
        progress = 4
    elif creating_delivery_task.sender_name:
        progress = 3
    else:
        progress = 2

    return render(request, 'shipments/create_delivery.html',
                  {
                      'delivery_task': creating_delivery_task,
                      'step': progress,
                      'item_form': item_form,
                      'pickup_form': pickup_form,
                      'delivery_form': delivery_form,
                      'payment_form': payment_form,
                      'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
                  })


def verify_delivery_payment(request, transaction_reference):
    transaction = get_object_or_404(DeliveryTransaction, id=transaction_reference)

    if transaction.transaction_verified:
        messages.info(request, 'This transaction has already been processed.')
        return redirect('shipments:shipment_index')

    verified = transaction.verify_transaction()

    if verified:
        with transaction.atomic():
            delivery = transaction.delivery
            delivery.status = Delivery.StatusChoices.PROCESSING
            delivery.save()

            transaction.transaction_verified = True
            transaction.save()

        messages.success(request, 'Payment successful. Delivery task created.')
    else:
        messages.error(request, 'Transaction verification failed')

    return redirect('shipments:shipment_index')

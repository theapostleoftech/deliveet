import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView
from firebase_admin import messaging

from accounts.models import Courier
from deliveet.utils.decorators import customer_required
from finance.forms import TransactionForm
from finance.models import Wallet, WalletTransaction
from shipments.forms import DeliveryItemForm, DeliveryPickupForm, DeliveryRecipientForm, PaymentMethodForm
from shipments.models import Delivery, DeliveryTransaction


def check_existing_delivery_tasks(request):
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
        messages.info(request, 'You have an ongoing delivery request.')
        return redirect(reverse('customers:customer_shipments'))

    creating_delivery_task = Delivery.objects.filter(
        customer=task_owner,
        status=Delivery.StatusChoices.CREATING
    ).last()

    if not creating_delivery_task:
        creating_delivery_task = Delivery.objects.create(
            customer=task_owner,
            status=Delivery.StatusChoices.CREATING
        )

    return creating_delivery_task


def create_delivery_task_view(request):
    task_owner = request.user.customer_account
    creating_delivery_task = check_existing_delivery_tasks(request)

    if isinstance(creating_delivery_task, HttpResponseRedirect):
        return creating_delivery_task

    item_form = DeliveryItemForm(instance=creating_delivery_task)
    pickup_form = DeliveryPickupForm(instance=creating_delivery_task)
    delivery_form = DeliveryRecipientForm(instance=creating_delivery_task)
    payment_form = PaymentMethodForm(instance=creating_delivery_task)

    if request.method == 'POST':
        step = int(request.POST.get('step', 1))
        if step == 1:
            item_form = DeliveryItemForm(request.POST, request.FILES, instance=creating_delivery_task)
            if item_form.is_valid():
                creating_delivery_task = item_form.save(commit=False)
                creating_delivery_task.customer = task_owner
                creating_delivery_task.save()
                return redirect(reverse('shipments:create_delivery') + f'?step=2')
            else:
                messages.error(request, item_form.errors)
                item_form = DeliveryItemForm(instance=creating_delivery_task)
        elif step == 2:
            pickup_form = DeliveryPickupForm(request.POST, instance=creating_delivery_task)
            if pickup_form.is_valid():
                creating_delivery_task = pickup_form.save()
                return redirect(reverse('shipments:create_delivery') + f'?step=3')
            else:
                messages.error(pickup_form, pickup_form.errors)
                pickup_form = DeliveryPickupForm(instance=creating_delivery_task)
        elif step == 3:
            delivery_form = DeliveryRecipientForm(request.POST, instance=creating_delivery_task)
            if delivery_form.is_valid():
                creating_delivery_task = delivery_form.save()
                calculate_distance_and_price(request, creating_delivery_task)
                return redirect(reverse('shipments:create_delivery') + f'?step=4')
        elif step == 4:
            payment = handle_payment_form(request, creating_delivery_task)
            if payment:
                return payment

    if not creating_delivery_task.item_name:
        progress = 1
    elif not creating_delivery_task.sender_name:
        progress = 2
    elif not creating_delivery_task.recipient_name:
        progress = 3
    else:
        progress = 4

    step = int(request.GET.get('step', progress))

    context = {
        'delivery_task': creating_delivery_task,
        'step': step,
        'item_form': item_form,
        'pickup_form': pickup_form,
        'delivery_form': delivery_form,
        'payment_form': payment_form,
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY
    }
    return render(request, 'shipments/create_delivery.html', context)

    pass


def calculate_distance_and_price(request, creating_delivery_task):
    origin = creating_delivery_task.pickup_address
    destination = creating_delivery_task.delivery_address
    api_key = settings.GOOGLE_MAP_API_KEY
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            distance = data['rows'][0]['elements'][0]['distance']['value']  # Distance in meters
            duration = data['rows'][0]['elements'][0]['duration']['value']  # Duration in seconds

            creating_delivery_task.distance = round(distance / 1000, 2)  # Convert to km
            creating_delivery_task.duration = int(duration / 60)  # Convert to minutes
            creating_delivery_task.price = creating_delivery_task.distance * 450  # Adjust pricing as needed
            creating_delivery_task.save()
        else:
            messages.error(request, "Unable to calculate distance. Please check the addresses.")

    except Exception as e:
        messages.error(request, str(e))


def handle_payment_form(request, creating_delivery_task):
    payment_form = PaymentMethodForm(request.POST, instance=creating_delivery_task)
    if payment_form.is_valid():
        creating_delivery_task = payment_form.save()
        if creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.COD:
            creating_delivery_task.status = Delivery.StatusChoices.PROCESSING
            creating_delivery_task.save()
            messages.success(request, 'Delivery task created successfully.')
            send_courier_notifications(creating_delivery_task)

            return redirect(reverse('customers:customer_shipments'))

        elif creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.CARD:
            transaction = DeliveryTransaction.objects.create(
                delivery=creating_delivery_task,
                amount=creating_delivery_task.price
            )
            return redirect(reverse('finance:initiate_transaction'))

        elif creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.WALLET:
            wallet = Wallet.objects.get(user=request.user)
            if wallet.balance >= creating_delivery_task.price:
                wallet.balance -= creating_delivery_task.price
                wallet.save()

                WalletTransaction.objects.create(
                    wallet=wallet,
                    transaction_type='Withdraw',
                    amount=creating_delivery_task.price,
                    transaction_verified=True
                )

                DeliveryTransaction.objects.create(
                    delivery=creating_delivery_task,
                    amount=creating_delivery_task.price,
                    status='COMPLETED'
                )

                creating_delivery_task.status = Delivery.StatusChoices.PROCESSING
                creating_delivery_task.save()

                messages.success(request, 'Payment successful. Delivery task created successfully.')
                send_courier_notifications(creating_delivery_task)
                return redirect(reverse('customers:customer_shipments'))
            else:
                messages.error(request, 'Insufficient wallet balance. Please fund your account.')
                return redirect(reverse('finance:initiate_transaction'))
    return None


def send_courier_notifications(creating_delivery_task):
    couriers = Courier.objects.all()
    registration_tokens = [i.fcm_token for i in couriers if i.fcm_token]
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=creating_delivery_task.item_name,
            body=creating_delivery_task.delivery_address,
        ),
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                icon=creating_delivery_task.photo.url,
            ),
            fcm_options=messaging.WebpushFCMOptions(
                link=settings.NOTIFICATION_URL + reverse('couriers:available_delivery_tasks'),
            ),
        ),
        tokens=registration_tokens
    )
    response = messaging.send_multicast(message)
    print('{0} messages were sent successfully'.format(response.success_count))


def verify_delivery_payment(request, transaction_reference):
    transaction = get_object_or_404(DeliveryTransaction, id=transaction_reference)

    if transaction.transaction_verified:
        messages.info(request, 'This transaction has already been processed.')
        return redirect('customers:customer_shipments')

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

    return redirect('customers:customer_shipments')

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
from shipments.forms import DeliveryItemForm, DeliveryPickupForm, DeliveryRecipientForm, PaymentMethod
from shipments.models import Delivery, DeliveryTransaction


# def create_delivery_view(request):
#     task_owner = request.user.customer_account
#
#     existing_delivery_task = Delivery.objects.filter(
#         customer=task_owner,
#         status__in=[
#             Delivery.StatusChoices.PROCESSING,
#             Delivery.StatusChoices.PICKUP_IN_PROGRESS,
#             Delivery.StatusChoices.DELIVERY_IN_PROGRESS,
#         ]
#     ).exists()
#
#     if existing_delivery_task:
#         messages.info(request, 'You currently have an ongoing delivery request.')
#         return redirect(reverse('shipments:shipment_index'))
#
#     creating_delivery_task = Delivery.objects.filter(
#         customer=task_owner,
#         status=Delivery.StatusChoices.CREATING
#     ).last()
#
#     item_form = DeliveryItemForm(instance=creating_delivery_task)
#     pickup_form = DeliveryPickupForm(instance=creating_delivery_task)
#     delivery_form = DeliveryRecipientForm(instance=creating_delivery_task)
#     payment_form = PaymentMethod(instance=creating_delivery_task)
#
#     if request.method == 'POST':
#         if request.POST.get('step') == '1':
#             item_form = DeliveryItemForm(request.POST, instance=creating_delivery_task)
#             if item_form.is_valid():
#                 creating_delivery_task = item_form.save(commit=False)
#                 creating_delivery_task.customer = task_owner
#                 creating_delivery_task.save()
#                 return redirect(reverse('shipments:create_delivery'))
#         elif request.POST.get('step') == '2':
#             pickup_form = DeliveryPickupForm(request.POST, instance=creating_delivery_task)
#             if pickup_form.is_valid():
#                 creating_delivery_task = pickup_form.save()
#                 return redirect(reverse('shipments:create_delivery'))
#         elif request.POST.get('step') == '3':
#             delivery_form = DeliveryRecipientForm(request.POST, instance=creating_delivery_task)
#             if delivery_form.is_valid():
#                 creating_delivery_task = delivery_form.save()
#
#                 origin = creating_delivery_task.pickup_address
#                 destination = creating_delivery_task.delivery_address
#                 api_key = settings.GOOGLE_MAP_API_KEY
#                 url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
#
#                 try:
#                     response = requests.get(url)
#                     data = response.json()
#
#                     if data['status'] == 'OK':
#                         distance = data['rows'][0]['elements'][0]['distance']['value']  # Distance in meters
#                         duration = data['rows'][0]['elements'][0]['duration']['value']  # Duration in seconds
#
#                         creating_delivery_task.distance = round(distance / 1000, 2)  # Convert to km
#                         creating_delivery_task.duration = int(duration / 60)  # Convert to minutes
#                         creating_delivery_task.price = creating_delivery_task.distance * 100  # Adjust pricing as needed
#                         creating_delivery_task.save()
#                     else:
#                         messages.error(request, "Unable to calculate distance. Please check the addresses.")
#
#                 except Exception as e:
#                     messages.error(request, str(e))
#                 return redirect(reverse('shipments:create_delivery'))
#         elif request.POST.get('step') == '4':
#             payment_form = PaymentMethod(request.POST, instance=creating_delivery_task)
#             if payment_form.is_valid():
#                 creating_delivery_task = payment_form.save()
#                 if creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.COD:
#                     creating_delivery_task.status = Delivery.StatusChoices.PROCESSING
#                     creating_delivery_task.save()
#                     messages.success(request, 'Delivery task created successfully.')
#                     return redirect(reverse('shipments:shipment_index'))
#                 elif creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.CARD:
#                     # Create a DeliveryTransaction
#                     transaction = DeliveryTransaction.objects.create(
#                         delivery=creating_delivery_task,
#                         amount=creating_delivery_task.price
#                     )
#                     return redirect(reverse('finance:initiate_transaction', ))
#
#     if not creating_delivery_task:
#         progress = 1
#     elif creating_delivery_task.recipient_name:
#         progress = 4
#     elif creating_delivery_task.sender_name:
#         progress = 3
#     else:
#         progress = 2
#
#     return render(request, 'shipments/create_delivery.html',
#                   {
#                       'delivery_task': creating_delivery_task,
#                       'step': progress,
#                       'item_form': item_form,
#                       'pickup_form': pickup_form,
#                       'delivery_form': delivery_form,
#                       'payment_form': payment_form,
#                       'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
#                   })


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
        messages.info(request, 'You currently have an ongoing delivery request.')
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


def handle_item_form(request, creating_delivery_task, task_owner):
    if request.method == 'POST':
        item_form = DeliveryItemForm(request.POST, request.FILES, instance=creating_delivery_task)
        if item_form.is_valid():
            creating_delivery_task = item_form.save(commit=False)
            creating_delivery_task.customer = task_owner
            creating_delivery_task.save()
            return redirect(reverse('shipments:create_delivery'))
    else:
        item_form = DeliveryItemForm(instance=creating_delivery_task)
    return item_form, creating_delivery_task


def handle_pickup_form(request, creating_delivery_task):
    pickup_form = DeliveryPickupForm(request.POST, instance=creating_delivery_task)
    if pickup_form.is_valid():
        creating_delivery_task = pickup_form.save()
        return redirect(reverse('shipments:create_delivery'))
    return None


def handle_delivery_form(request, creating_delivery_task):
    delivery_form = DeliveryRecipientForm(request.POST, instance=creating_delivery_task)
    if delivery_form.is_valid():
        creating_delivery_task = delivery_form.save()
        calculate_distance_and_price(request, creating_delivery_task)
        return redirect(reverse('shipments:create_delivery'))
    return None


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
            creating_delivery_task.price = creating_delivery_task.distance * 100  # Adjust pricing as needed
            creating_delivery_task.save()
        else:
            messages.error(request, "Unable to calculate distance. Please check the addresses.")

    except Exception as e:
        messages.error(request, str(e))


def handle_payment_form(request, creating_delivery_task):
    payment_form = PaymentMethod(request.POST, instance=creating_delivery_task)
    if payment_form.is_valid():
        creating_delivery_task = payment_form.save()
        if creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.COD:
            creating_delivery_task.status = Delivery.StatusChoices.PROCESSING
            creating_delivery_task.save()
            messages.success(request, 'Delivery task created successfully.')
            return redirect(reverse('customers:customer_shipments'))
        elif creating_delivery_task.payment_method == Delivery.PaymentMethodChoices.CARD:
            transaction = DeliveryTransaction.objects.create(
                delivery=creating_delivery_task,
                amount=creating_delivery_task.price
            )
            return redirect(reverse('finance:initiate_transaction'))
    return None


def get_progress(creating_delivery_task):
    if not creating_delivery_task:
        return 1
    elif creating_delivery_task.recipient_name:
        return 4
    elif creating_delivery_task.sender_name:
        return 3
    else:
        return 2


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


def create_delivery_view(request):
    task_owner = request.user.customer_account
    creating_delivery_task = check_existing_delivery_tasks(request)

    # Check if creating_delivery_task is a redirect
    if isinstance(creating_delivery_task, HttpResponseRedirect):
        return creating_delivery_task

    if request.method == 'POST':
        step = request.POST.get('step')
        if step == '1':
            result = handle_item_form(request, creating_delivery_task, task_owner)
        elif step == '2':
            result = handle_pickup_form(request, creating_delivery_task)
        elif step == '3':
            result = handle_delivery_form(request, creating_delivery_task)
        elif step == '4':
            result = handle_payment_form(request, creating_delivery_task)

        if result:
            return result

    progress = get_progress(creating_delivery_task)

    context = {
        'delivery_task': creating_delivery_task,
        'step': progress,
        'item_form': DeliveryItemForm(instance=creating_delivery_task),
        'pickup_form': DeliveryPickupForm(instance=creating_delivery_task),
        'delivery_form': DeliveryRecipientForm(instance=creating_delivery_task),
        'payment_form': PaymentMethod(instance=creating_delivery_task),
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
    }

    return render(request, 'shipments/create_delivery.html', context)


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
"""
This contains views for courier app.
"""
from decimal import Decimal

from asgiref.sync import async_to_sync
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from deliveet.utils.decorators import courier_required
from shipments.models import Delivery


@method_decorator([courier_required], name='dispatch')
class CourierDashboardView(TemplateView):
    """
    This view handles the courier's dashboard
    """
    template_name = 'courier/courier_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        delivery_tasks = Delivery.objects.filter(
            courier=self.request.user.courier_account,
            status=Delivery.StatusChoices.COMPLETED
        )
        deliveries_in_progress = Delivery.objects.filter(
            courier=self.request.user.courier_account,
            status__in=[
                Delivery.StatusChoices.PROCESSING,
                Delivery.StatusChoices.PICKUP_IN_PROGRESS,
                Delivery.StatusChoices.DELIVERY_IN_PROGRESS,
            ]
        ).count()

        deliveries_canceled = Delivery.objects.filter(
            courier=self.request.user.courier_account,
            status__in=[
                Delivery.StatusChoices.CANCELED,
            ]
        ).count()

        deliveries_completed = Delivery.objects.filter(
            courier=self.request.user.courier_account,
            status__in=[
                Delivery.StatusChoices.COMPLETED,
            ]
        ).count()

        total_price = sum(delivery_task.price for delivery_task in delivery_tasks)
        context['total_earnings'] = (total_price * Decimal('0.9')).quantize(Decimal('0.01'))
        context['total_delivery_tasks'] = len(delivery_tasks)
        context['total_km'] = sum(delivery_task.distance for delivery_task in delivery_tasks)
        context['deliveries_in_progress'] = deliveries_in_progress
        context['deliveries_canceled'] = deliveries_canceled
        context['deliveries_completed'] = deliveries_completed
        return context


@courier_required
def courier_available_delivery_tasks(request):
    """
    Renders the available delivery task page.
    """
    template_name = 'courier/available_delivery_tasks.html'
    GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY
    return render(
        request,
        template_name, {
            'GOOGLE_MAP_API_KEY': GOOGLE_MAP_API_KEY,
        })


@courier_required
def courier_available_delivery_task(request, id):
    """
    Renders details of a specific available delivery task or redirects if not found.
    Allows a courier to accept a delivery task.
    """
    template_name = 'courier/available_delivery_task.html'
    delivery_task = Delivery.objects.filter(
        id=id,
        status=Delivery.StatusChoices.PROCESSING).last()

    if not delivery_task:
        return redirect(reverse('couriers:available_delivery_tasks'))

    if request.method == 'POST':
        delivery_task.courier = request.user.courier_account
        delivery_task.status = Delivery.StatusChoices.PICKUP_IN_PROGRESS
        delivery_task.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("delivery_task_" + str(delivery_task.id), {
                'type': 'delivery_task_update',
                'delivery_task': {
                    'status': delivery_task.get_status_display(),
                }
            })
        except:
            pass

        return redirect(reverse('couriers:delivery_task'))

    return render(
        request,
        template_name, {
            "delivery_task": delivery_task
        })


@courier_required
def courier_delivery_task(request):
    """
    Renders details of the current delivery task being handled by the courier.
    """
    template_name = 'courier/delivery_task.html'
    GOOGLE_MAP_API_KEY = settings.GOOGLE_MAP_API_KEY
    delivery_task = Delivery.objects.filter(
        courier=request.user.courier_account,
        status__in=[
            Delivery.StatusChoices.PICKUP_IN_PROGRESS,
            Delivery.StatusChoices.DELIVERY_IN_PROGRESS
        ]
    ).last()

    return render(request, template_name, {
        "delivery_task": delivery_task,
        "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY
    })


@courier_required
def courier_delivery_task_take_photo(request, id):
    """
    Renders the page for taking a photo of the current delivery in progress.
    """
    template_name = 'courier/delivery_task_take_photo.html'
    delivery_task = Delivery.objects.filter(
        id=id,
        courier=request.user.courier_account,
        status__in=[
            Delivery.StatusChoices.PICKUP_IN_PROGRESS,
            Delivery.StatusChoices.DELIVERY_IN_PROGRESS
        ]
    ).last()

    if not delivery_task:
        return redirect(reverse('courier:delivery_task'))

    return render(request, template_name, {
        "delivery_task": delivery_task
    })


@courier_required
def courier_delivery_task_completed(request):
    """
    Renders the delivery task completion page.
    """
    template_name = 'courier/delivery_task_complete.html'
    return render(request, template_name)


@courier_required
def courier_past_delivery_tasks(request):
    """
    Renders the past delivery_tasks page.
    """
    template_name = 'courier/past_delivery_tasks.html'
    delivery_tasks = Delivery.objects.filter(
        courier=request.user.courier_account,
        status=Delivery.StatusChoices.COMPLETED
    )

    return render(request, template_name, {
        "delivery_tasks": delivery_tasks
    })

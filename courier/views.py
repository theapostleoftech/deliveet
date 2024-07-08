"""
This contains views for courier app.
"""
from asgiref.sync import async_to_sync
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView, View

from deliveet.utils.decorators import courier_required
from shipments.models import Delivery


@method_decorator(courier_required, name='dispatch')
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

        context['total_earnings'] = round(sum(delivery_task.price for delivery_task in delivery_tasks) * 0.9, 2)
        context['total_delivery_tasks'] = len(delivery_tasks)
        context['total_km'] = sum(delivery_task.distance for delivery_task in delivery_tasks)
        return context


@method_decorator(courier_required, name='dispatch')
class CourierShipmentsView(RedirectView):
    """
    This view displays the deliveries available to the courier
    """
    url = reverse_lazy('couriers:shipment_orders')


@method_decorator(courier_required, name='dispatch')
class CourierOrdersView(TemplateView):
    """
    This view displays the deliveries available to the courier
    Allows the courier to accept deliveries
    """
    template_name = 'courier/shipment_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAP_API_KEY'] = settings.GOOGLE_MAP_API_KEY
        return context


@method_decorator(courier_required, name='dispatch')
class CourierOrderDetailView(View):
    template_name = 'courier/shipment_orders.html'

    def get_delivery_task(self, id):
        """
        This function retrieves a delivery order by id
        """
        return Delivery.objects.filter(
            id=id, status=Delivery.StatusChoices.PROCESSING
        ).last()

    def get(self, request, id):
        """
        This function displays the job details
        """
        delivery_task = self.get_delivery_task(id)
        if not delivery_task:
            return redirect(reverse('couriers:shipment_orders'))
        return render(
            request,
            self.template_name,
            {
                "delivery_task": delivery_task
            }
        )

    def post(self, request, id):
        """
        Updates the delivery status, assigns courier and sends messages
        """
        delivery_task = self.get_delivery_task(id)
        if not delivery_task:
            return redirect(reverse('couriers:shipment_orders'))

        delivery_task.courier = request.user.courier_account
        delivery_task.status = Delivery.StatusChoices.PICKUP_IN_PROGRESS
        delivery_task.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("delivery_task_" + str(delivery_task.id),
                                            {
                                                'type': 'delivery_task_update',
                                                'delivery_task': {
                                                    'status': delivery_task.get_status_display(),
                                                }
                                            })
        except:
            pass

        return redirect(reverse('couriers:delivery_tasks'))


@method_decorator(courier_required, name='dispatch')
class CourierOrderView(TemplateView):
    """
    This view displays the current shipment order of a courier.
    """
    template_name = 'courier/shipment_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery_task'] = Delivery.objects.filter(
            courier=self.request.user.courier_account,
            status__in=[
                Delivery.StatusChoices.PICKUP_IN_PROGRESS,
                Delivery.StatusChoices.DELIVERY_IN_PROGRESS
            ]
        ).last()
        context['GOOGLE_MAP_API_KEY'] = settings.GOOGLE_MAP_API_KEY
        return context


@method_decorator(courier_required, name='dispatch')
class CourierOrderCompletedView(TemplateView):
    """
    View for the job completion page.
    """
    template_name = 'courier/delivery_task_complete.html'

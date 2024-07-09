"""
This contains views for customer app.
"""
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

from deliveet.utils.decorators import customer_required
from shipments.models import Delivery


@method_decorator(customer_required, name='dispatch')
class CustomerDashboardView(ListView):
    """
    This is the customers dashboard view
    """
    template_name = 'customers/customers_dashboard.html'
    context_object_name = 'deliveries'
    model = Delivery

    def get_queryset(self):
        return Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status__in=[
                Delivery.StatusChoices.PROCESSING,
                Delivery.StatusChoices.PICKUP_IN_PROGRESS,
                Delivery.StatusChoices.DELIVERY_IN_PROGRESS,
                Delivery.StatusChoices.CANCELED,
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

        deliveries_canceled = Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status__in=[
                Delivery.StatusChoices.CANCELED,
            ]
        ).count()

        context['total_deliveries'] = total_deliveries
        context['deliveries_completed'] = deliveries_completed
        context['deliveries_in_progress'] = deliveries_in_progress
        context['deliveries_canceled'] = deliveries_canceled

        return context


@method_decorator(customer_required, name='dispatch')
class CustomerDeliveryTasksView(ListView):
    """
    This view displays the customers delivery orders.
    """
    template_name = 'customers/customer_shipments.html'
    context_object_name = 'delivery_tasks'

    def get_queryset(self):
        return Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status__in=[
                Delivery.StatusChoices.PROCESSING,
                Delivery.StatusChoices.PICKUP_IN_PROGRESS,
                Delivery.StatusChoices.DELIVERY_IN_PROGRESS
            ]
        )


class CustomerCompletedDeliveryTask(ListView):
    template_name = 'customers/customer_completed_delivery_task.html'
    context_object_name = 'delivery_task'

    def get_queryset(self):
        return Delivery.objects.filter(
            customer=self.request.user.customer_account,
            status__in=[
                Delivery.StatusChoices.COMPLETED,
                Delivery.StatusChoices.CANCELED
            ]
        )


@method_decorator(customer_required, name='dispatch')
class CustomerDeliveryTaskDetailView(DetailView):
    """
    This view displays the customer's current order
    """
    template_name = 'customers/customer_shipment_detail.html'
    model = Delivery
    context_object_name = 'delivery_task'
    pk_url_kwarg = 'delivery_task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAP_API_KEY'] = settings.GOOGLE_MAP_API_KEY
        return context

    def post(self, request, *args, **kwargs):
        delivery_task = self.get_object()
        if delivery_task.status == Delivery.StatusChoices.PROCESSING:
            delivery_task.status = Delivery.StatusChoices.CANCELED
            delivery_task.save()
            return redirect(reverse('customer:archived_jobs'))
        return self.get(request, *args, **kwargs)

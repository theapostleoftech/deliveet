"""
This module provides views for the profiles app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from accounts.models import Customer, Courier
from profiles.forms import CustomerUpdateForm
from shipments.models import Delivery


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """
    This view allows customers to update their profile information.
    """
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('profiles:customer_details')

    def get_object(self, queryset=None):
        return self.request.user.customer_account


class CustomerDetailView(LoginRequiredMixin, DetailView):
    """
    This view displays the customer detail page.
    """
    model = Customer
    context_object_name = 'customer'
    template_name = 'profiles/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        context['user_account'] = customer.user
        return context


class CourierDetailView(LoginRequiredMixin, DetailView):
    """
    This view displays the courier detail page.
    """
    model = Courier
    context_object_name = 'courier'
    template_name = 'profiles/courier_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courier = self.get_object()
        context['user_account'] = courier.user
        return context


def courier_profile_view(request):
    """
    Renders the courier's profile page with statistics.
    """
    template_name = 'profiles/courier_profile.html'
    delivery_tasks = Delivery.objects.filter(
        courier=request.user.courier_account,
        status=Delivery.StatusChoices.COMPLETED
    )

    delivery_in_progress = Delivery.objects.filter(
        courier=request.user.courier_account,
        status__in=[
            Delivery.StatusChoices.DELIVERY_IN_PROGRESS
        ]
    ).count()

    total_earnings: float = round(sum(delivery_task.price for delivery_task in delivery_tasks) * 0.9, 2)
    # balance = round(sum(total_earnings) + wallet_balance)
    total_delivery_tasks = len(delivery_tasks)
    total_km = sum(delivery_task.distance for delivery_task in delivery_tasks)

    return render(request, template_name, {
        "total_earnings": total_earnings,
        "total_delivery_tasks": total_delivery_tasks,
        "total_km": total_km,
        "delivery_in_progress": delivery_in_progress
    })

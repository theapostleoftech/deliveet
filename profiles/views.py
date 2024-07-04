"""
This module provides views for the profiles app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from accounts.models import Customer, Courier
from profiles.forms import CustomerUpdateForm


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

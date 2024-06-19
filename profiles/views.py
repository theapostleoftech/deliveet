"""
This module provides views for the profiles app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from accounts.models import Customer, Courier, UserAccount


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'profiles/customer_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     customer = self.get_object()
    #     context['user_account'] = customer.user
    #     return context


class CourierDetailView(LoginRequiredMixin, DetailView):
    model = Courier
    context_object_name = 'courier'
    template_name = 'profiles/courier_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courier = self.get_object()
        context['user_account'] = courier.user
        return context

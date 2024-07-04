"""
This contains views for customer app.
"""

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from deliveet.utils.decorators import customer_required


@method_decorator(customer_required, name='dispatch')
class CustomerDashboardView(TemplateView):
    """
    This view displays the customers dashboard.
    """
    template_name = 'customers/customers_dashboard.html'

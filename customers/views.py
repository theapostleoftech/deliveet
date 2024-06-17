"""
This contains views for customer app.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class CustomerDashboardView(TemplateView):
    """
    This view displays the customers dashboard.
    """
    template_name = 'customers/customers_dashboard.html'

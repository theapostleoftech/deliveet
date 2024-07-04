"""
This contains views for courier app.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class CourierDashboardView(TemplateView):
    """
    This view displays the courier dashboard.
    """
    template_name = 'courier/courier_dashboard.html'

"""
This contains views for courier app.
"""

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from deliveet.utils.decorators import courier_required


# Create your views here.
@method_decorator(courier_required, name='dispatch')
class CourierDashboardView(TemplateView):
    """
    This view displays the courier dashboard.
    """
    template_name = 'courier/courier_dashboard.html'

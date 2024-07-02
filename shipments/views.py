from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class ShipmentView(LoginRequiredMixin, TemplateView):
    """
    This class shows the shipping dashboard`
    """
    template_name = 'shipments/shipment.html'

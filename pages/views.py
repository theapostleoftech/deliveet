"""
This holds views for different pages in the deliveet app
"""
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    """
    This is the homepage class-based view
    """
    template_name = 'pages/index.html'
    pass


class DashboardView(TemplateView):
    """
    This is the view for customer dashboards
    """


class SampleView(TemplateView):
    """
    This is the homepage class-based view
    """
    template_name = 'finance/sample.html'
    pass

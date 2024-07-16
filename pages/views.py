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


# class LandingPageView(TemplateView):
#     template_name = 'pages/landing_page.html'


class AppView(TemplateView):
    """
    This is view for the app home page
    """
    template_name = 'pages/app.html'

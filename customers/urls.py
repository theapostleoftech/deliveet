"""
This contains url routes for the customers app.
"""
from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),

]

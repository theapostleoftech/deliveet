"""
This contains url routes for the customers app.
"""
from django.urls import path
from . import views

app_name = 'couriers'
urlpatterns = [
    path('dashboard/', views.CourierDashboardView.as_view(), name='customer_dashboard'),

]

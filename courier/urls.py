"""
This contains url routes for the courier app.
"""
from django.urls import path
from . import views

app_name = 'couriers'
urlpatterns = [
    path('dashboard/', views.CourierDashboardView.as_view(), name='courier_dashboard'),

]

"""
This holds url routes for all the profile app
"""
from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('customer/<uuid:pk>/', views.CustomerDetailView.as_view(), name='customer_details'),
    path('courier/<uuid:pk>', views.CourierDetailView.as_view(), name='courier_details'),
]

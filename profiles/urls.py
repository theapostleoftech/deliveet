"""
This holds url routes for all the profile app
"""
from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('customer/<uuid:pk>/', views.CustomerDetailView.as_view(), name='customer_details'),
    path('customer/update/<uuid:pk>/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('courier/<uuid:pk>', views.CourierDetailView.as_view(), name='courier_details'),
]

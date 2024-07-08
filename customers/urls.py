"""
This contains url routes for the customers app.
"""
from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('deliveries/', views.CustomerDeliveriesView.as_view(), name='customer_shipments'),

    path('deliveries/completed', views.CustomerCompletedShipmentsView.as_view(), name='customer_completed_shipments'),

    path('deliveries/<uuid:delivery_task_id>', views.CustomerShipmentDetailView.as_view(),
         name='customer_shipment_detail'),

]

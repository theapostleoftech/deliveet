"""
This contains url routes for the customers app.
"""
from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('deliveries/', views.CustomerDeliveryTasksView.as_view(), name='customer_shipments'),

    path('deliveries/completed', views.CustomerCompletedDeliveryTask.as_view(), name='customer_completed_shipments'),

    path('deliveries/<uuid:delivery_task_id>', views.CustomerDeliveryTaskDetailView.as_view(),
         name='customer_shipment_detail'),

]

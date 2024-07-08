"""
This contains url routes for the courier app.
"""
from django.urls import path
from . import views
from .apis.apis import delivery_tasks_api, delivery_task_status_api, fcm_token_update_api

app_name = 'couriers'
urlpatterns = [
    path('dashboard/', views.CourierDashboardView.as_view(), name='courier_dashboard'),

    path('deliveries/', views.CourierShipmentsView.as_view(), name='courier_shipments'),

    path('deliveries/tasks/', views.CourierOrdersView.as_view(), name='shipment_orders'),

    path('deliveries/task/<id>', views.CourierOrderDetailView.as_view(), name='shipment_order_details'),

    # path('shipments/order/', views.CourierShipmentsView.as_view(), name='shipment_order'),

    path('apis/deliveries/tasks', delivery_tasks_api, name='courier_delivery_tasks'),

    path('apis/deliveries/tasks/<id>/status', delivery_tasks_api, name='courier_delivery_tasks_status'),

    path('apis/deliveries/tasks/fcm', delivery_tasks_api, name='courier_delivery_tasks_fcm'),

]

"""
This contains url routes for the courier app.
"""
from django.urls import path
from . import views
from .apis import delivery_tasks_api

app_name = 'couriers'
urlpatterns = [
    path('dashboard/', views.CourierDashboardView.as_view(), name='courier_dashboard'),

    path('deliveries/', views.CourierShipmentsView.as_view(), name='courier_shipments'),

    path('deliveries/orders/', views.CourierOrdersView.as_view(), name='shipment_orders'),

    path('deliveries/order/<id>', views.CourierOrderDetailView.as_view(), name='shipment_order_details'),

    # path('shipments/order/', views.CourierShipmentsView.as_view(), name='shipment_order'),

    path('apis/deliveries/delivery_tasks', delivery_tasks_api, name='courier_delivery_tasks'),

]

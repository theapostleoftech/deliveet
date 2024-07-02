from django.urls import path

from shipments import views

app_name = 'shipments'
urlpatterns = [
    path('shipments/', views.ShipmentView.as_view(), name='shipment_index'),
]

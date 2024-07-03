from django.urls import path

from shipments import views

app_name = 'shipments'
urlpatterns = [
    path('', views.ShipmentView.as_view(), name='shipment_index'),
    path('create/', views.ShipmentView.as_view(), name='shipment_index'),
]

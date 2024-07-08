from django.urls import path

from shipments import views

app_name = 'shipments'
urlpatterns = [
    # path('', views.ShipmentView.as_view(), name='shipment_index'),
    path('create/', views.create_delivery_view, name='create_delivery'),
]

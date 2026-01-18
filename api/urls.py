"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import (
    AuthenticationViewSet, UserAccountViewSet, CourierViewSet,
    CustomerViewSet, ShipmentViewSet, DeliveryViewSet, WalletViewSet
)

router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')
router.register(r'users', UserAccountViewSet, basename='user')
router.register(r'couriers', CourierViewSet, basename='courier')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'shipments', ShipmentViewSet, basename='shipment')
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'wallets', WalletViewSet, basename='wallet')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    
    # API Schema & Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]

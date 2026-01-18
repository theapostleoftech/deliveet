"""
Custom permissions for API endpoints
"""
from rest_framework import permissions
from courier.models import Courier
from customers.models import Customer


class IsCourier(permissions.BasePermission):
    """
    Allows access only to courier users
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'courier')


class IsCustomer(permissions.BasePermission):
    """
    Allows access only to customer users
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'customer')


class IsOwner(permissions.BasePermission):
    """
    Allows access only if user is the owner of the object
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsShipmentOwner(permissions.BasePermission):
    """
    Allows access only if user is the shipment owner (customer)
    """
    def has_object_permission(self, request, view, obj):
        return obj.customer.user == request.user


class IsDeliveryAssigned(permissions.BasePermission):
    """
    Allows access only if courier is assigned to the delivery
    """
    def has_object_permission(self, request, view, obj):
        return obj.courier.user == request.user


class IsVerifiedCourier(permissions.BasePermission):
    """
    Allows access only to verified couriers
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            courier = Courier.objects.get(user=request.user)
            return courier.is_verified
        except Courier.DoesNotExist:
            return False

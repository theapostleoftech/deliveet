"""
API Views for Deliveet
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import UserAccount
from courier.models import Courier
from customers.models import Customer
from shipments.models import Shipment, Delivery
from finance.models import Wallet

from .serializers import (
    UserAccountSerializer, CourierSerializer, CustomerSerializer,
    ShipmentSerializer, DeliverySerializer, WalletSerializer,
    LoginSerializer, RegistrationSerializer
)
from .permissions import (
    IsCourier, IsCustomer, IsOwner, IsVerifiedCourier,
    IsShipmentOwner, IsDeliveryAssigned
)


class AuthenticationViewSet(viewsets.ViewSet):
    """
    API endpoint for authentication (login, register, logout)
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user"""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserAccountSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login user"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserAccountSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user"""
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for UserAccount
    """
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']

    def get_queryset(self):
        """Return current user's data only"""
        return UserAccount.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect'},
                          status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully'})


class CourierViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Courier
    """
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_available', 'is_verified', 'vehicle_type']
    search_fields = ['user__first_name', 'user__last_name', 'user__phone_number']
    ordering_fields = ['rating', 'total_deliveries']

    def get_queryset(self):
        """Couriers can only view/edit their own profile"""
        if self.request.user.is_staff:
            return Courier.objects.all()
        try:
            return Courier.objects.filter(user=self.request.user)
        except:
            return Courier.objects.none()

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get nearby available couriers (requires location)"""
        latitude = request.query_params.get('lat')
        longitude = request.query_params.get('lng')
        radius = request.query_params.get('radius', 5)  # km

        if not latitude or not longitude:
            return Response({'detail': 'Latitude and longitude required'},
                          status=status.HTTP_400_BAD_REQUEST)

        # TODO: Implement haversine distance calculation
        couriers = Courier.objects.filter(is_available=True, is_verified=True)
        serializer = self.get_serializer(couriers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsCourier])
    def toggle_availability(self, request):
        """Toggle courier availability"""
        try:
            courier = Courier.objects.get(user=request.user)
            courier.is_available = not courier.is_available
            courier.save()
            return Response({
                'is_available': courier.is_available,
                'detail': 'Availability updated'
            })
        except Courier.DoesNotExist:
            return Response({'detail': 'Courier profile not found'},
                          status=status.HTTP_404_NOT_FOUND)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Customers can only view/edit their own profile"""
        if self.request.user.is_staff:
            return Customer.objects.all()
        try:
            return Customer.objects.filter(user=self.request.user)
        except:
            return Customer.objects.none()


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Shipment
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'customer']
    search_fields = ['tracking_number', 'recipient_name']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        """Users can only see their own shipments"""
        user = self.request.user
        if user.is_staff:
            return Shipment.objects.all()
        try:
            customer = Customer.objects.get(user=user)
            return Shipment.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Shipment.objects.none()

    def perform_create(self, serializer):
        """Create shipment for current user"""
        try:
            customer = Customer.objects.get(user=self.request.user)
            serializer.save(customer=customer)
        except Customer.DoesNotExist:
            return Response({'detail': 'Customer profile not found'},
                          status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_courier(self, request, pk=None):
        """Assign a courier to shipment"""
        shipment = self.get_object()
        courier_id = request.data.get('courier_id')

        if not courier_id:
            return Response({'detail': 'Courier ID required'},
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            courier = Courier.objects.get(id=courier_id)
            delivery = Delivery.objects.create(shipment=shipment, courier=courier)
            serializer = DeliverySerializer(delivery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Courier.DoesNotExist:
            return Response({'detail': 'Courier not found'},
                          status=status.HTTP_404_NOT_FOUND)


class DeliveryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Delivery
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'courier']
    ordering_fields = ['created_at', 'estimated_delivery_time']

    def get_queryset(self):
        """Users can only see relevant deliveries"""
        user = self.request.user
        if user.is_staff:
            return Delivery.objects.all()

        # Couriers see their deliveries
        try:
            courier = Courier.objects.get(user=user)
            return Delivery.objects.filter(courier=courier)
        except Courier.DoesNotExist:
            pass

        # Customers see their shipment deliveries
        try:
            customer = Customer.objects.get(user=user)
            return Delivery.objects.filter(shipment__customer=customer)
        except Customer.DoesNotExist:
            pass

        return Delivery.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsCourier])
    def update_status(self, request, pk=None):
        """Update delivery status (by courier)"""
        delivery = self.get_object()
        new_status = request.data.get('status')

        if new_status not in [choice[0] for choice in Delivery._meta.get_field('status').choices]:
            return Response({'detail': 'Invalid status'},
                          status=status.HTTP_400_BAD_REQUEST)

        delivery.status = new_status
        delivery.save()
        serializer = self.get_serializer(delivery)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsCourier])
    def upload_proof(self, request, pk=None):
        """Upload delivery proof (photo)"""
        delivery = self.get_object()
        photo = request.FILES.get('photo')

        if not photo:
            return Response({'detail': 'Photo required'},
                          status=status.HTTP_400_BAD_REQUEST)

        delivery.delivery_photo = photo
        delivery.status = 'delivered'
        delivery.save()
        serializer = self.get_serializer(delivery)
        return Response(serializer.data)


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Wallet
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own wallet"""
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def balance(self, request):
        """Get user wallet balance"""
        try:
            wallet = Wallet.objects.get(user=request.user)
            return Response({'balance': wallet.balance, 'currency': wallet.currency})
        except Wallet.DoesNotExist:
            return Response({'detail': 'Wallet not found'},
                          status=status.HTTP_404_NOT_FOUND)

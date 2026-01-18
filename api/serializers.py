"""
DRF Serializers for all models
"""
from rest_framework import serializers
from accounts.models import UserAccount
from shipments.models import Shipment, Delivery
from courier.models import Courier
from customers.models import Customer
from finance.models import Wallet
from django.contrib.auth import authenticate


class UserAccountSerializer(serializers.ModelSerializer):
    """Serializer for UserAccount model"""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 
                  'avatar', 'is_active', 'date_joined', 'password']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CourierSerializer(serializers.ModelSerializer):
    """Serializer for Courier model"""
    user = UserAccountSerializer(read_only=True)
    
    class Meta:
        model = Courier
        fields = ['id', 'user', 'rating', 'total_deliveries', 'vehicle_type',
                  'license_number', 'insurance_number', 'is_verified', 'is_available']
        read_only_fields = ['id', 'total_deliveries']


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    user = UserAccountSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'address', 'city', 'state', 'postal_code']
        read_only_fields = ['id']


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Wallet/Finance model"""
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'currency', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class ShipmentSerializer(serializers.ModelSerializer):
    """Serializer for Shipment model"""
    
    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeliverySerializer(serializers.ModelSerializer):
    """Serializer for Delivery model"""
    
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        data['user'] = user
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = UserAccount
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Additional serializers for notification and advanced features
from rest_framework import serializers
from .models import Notification, Rating, Transaction, Promotion, Support, Document


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'data',
                  'is_read', 'read_at', 'created_at']
        read_only_fields = ['id', 'created_at', 'read_at']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model"""
    rater_name = serializers.CharField(source='rater.get_full_name', read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'rater', 'rater_name', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'currency', 'description',
                  'status', 'created_at', 'completed_at']
        read_only_fields = ['id', 'created_at', 'completed_at']


class PromotionSerializer(serializers.ModelSerializer):
    """Serializer for Promotion model"""
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Promotion
        fields = ['id', 'code', 'name', 'description', 'promotion_type',
                  'discount_value', 'min_order_amount', 'is_valid']
        read_only_fields = ['id']
    
    def get_is_valid(self, obj):
        return obj.is_valid()


class SupportSerializer(serializers.ModelSerializer):
    """Serializer for Support model"""
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', 
                                            read_only=True, required=False)
    
    class Meta:
        model = Support
        fields = ['id', 'subject', 'description', 'status', 'priority',
                  'assigned_to', 'assigned_to_name', 'created_at', 'resolved_at']
        read_only_fields = ['id', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    
    class Meta:
        model = Document
        fields = ['id', 'document_type', 'original_filename', 'is_verified',
                  'expiry_date', 'is_expired', 'created_at']
        read_only_fields = ['id', 'created_at']

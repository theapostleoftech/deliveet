"""
Database Models Optimization & Additional Features
Enhanced models with indexing, validation, and business logic
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
import uuid


class Notification(models.Model):
    """Real-time notifications model"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('delivery_created', _('Delivery Created')),
        ('delivery_assigned', _('Delivery Assigned')),
        ('delivery_updated', _('Delivery Updated')),
        ('delivery_completed', _('Delivery Completed')),
        ('courier_arrived', _('Courier Arrived')),
        ('payment_received', _('Payment Received')),
        ('rating_received', _('Rating Received')),
        ('message', _('Message')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)  # Additional data (e.g., shipment_id)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'is_read', '-created_at']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class Rating(models.Model):
    """Ratings and reviews"""
    
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rater = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='ratings_received')
    delivery = models.OneToOneField('shipments.Delivery', on_delete=models.CASCADE, related_name='rating', null=True, blank=True)
    
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['rater', 'delivery']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rated_user', '-created_at']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.rater.email} rated {self.rated_user.email} - {self.rating}⭐"


class Transaction(models.Model):
    """Transaction tracking for audit and accounting"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('payment', _('Payment')),
        ('refund', _('Refund')),
        ('earning', _('Earning')),
        ('commission', _('Commission')),
        ('adjustment', _('Adjustment')),
    ]
    
    TRANSACTION_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='NGN')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    
    # Reference IDs
    payment_ref = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_ref = models.ForeignKey('shipments.Delivery', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['transaction_type', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields='-created_at'),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - ₦{self.amount}"


class Promotion(models.Model):
    """Promotions and discounts"""
    
    PROMOTION_TYPE_CHOICES = [
        ('percentage', _('Percentage Discount')),
        ('fixed', _('Fixed Amount')),
        ('free_delivery', _('Free Delivery')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active', '-end_date']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def is_valid(self):
        """Check if promotion is still valid"""
        from django.utils import timezone
        now = timezone.now()
        return (self.is_active and 
                self.start_date <= now <= self.end_date and
                (self.usage_limit is None or self.used_count < self.usage_limit))
    
    def apply_discount(self, amount):
        """Calculate discount amount"""
        if self.promotion_type == 'percentage':
            discount = amount * (self.discount_value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
            return discount
        else:
            return self.discount_value


class Support(models.Model):
    """Customer support tickets"""
    
    SUPPORT_STATUS_CHOICES = [
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=SUPPORT_STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    assigned_to = models.ForeignKey('accounts.UserAccount', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='assigned_tickets')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.subject} - {self.status}"


class Document(models.Model):
    """Document storage for courier verification, delivery proofs, etc."""
    
    DOCUMENT_TYPE_CHOICES = [
        ('license', _('Driver License')),
        ('insurance', _('Insurance')),
        ('vehicle_registration', _('Vehicle Registration')),
        ('proof_of_delivery', _('Proof of Delivery')),
        ('id_card', _('ID Card')),
        ('other', _('Other')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField()  # Size in bytes
    
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey('accounts.UserAccount', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='verified_documents')
    
    expiry_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'document_type']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.document_type}"

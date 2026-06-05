from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class CustomUser(AbstractUser):
    """Extended User model with additional fields."""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    company = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Administrator'),
            ('manager', 'Manager'),
            ('sales', 'Sales'),
            ('warehouse', 'Warehouse'),
            ('finance', 'Finance'),
            ('customer', 'Customer'),
        ],
        default='customer'
    )
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.get_full_name() or self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Audit(BaseModel):
    """Model for tracking changes to entities."""
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(
        max_length=10,
        choices=[
            ('create', 'Created'),
            ('update', 'Updated'),
            ('delete', 'Deleted'),
        ]
    )
    content_type = models.CharField(max_length=100)  # e.g., 'Product', 'Order'
    object_id = models.UUIDField()
    description = models.TextField()
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} - {self.content_type} ({self.created_at})"


class CompanyInfo(BaseModel):
    """Company information and settings."""
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    description = models.TextField(blank=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    
    # Address
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Company Details
    tax_id = models.CharField(max_length=50, unique=True)
    registration_number = models.CharField(max_length=50, unique=True, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.IntegerField(default=1)
    
    # Financial
    currency = models.CharField(
        max_length=3,
        default='USD',
        choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen')]
    )
    fiscal_year_start = models.DateField(null=True, blank=True)
    
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Company Info'
        verbose_name_plural = 'Company Info'

    def __str__(self):
        return self.name

    @classmethod
    def get_default(cls):
        """Get or create default company info."""
        return cls.objects.first()


class NotificationPreference(BaseModel):
    """User notification preferences."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_preference')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    order_updates = models.BooleanField(default=True)
    inventory_alerts = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'

    def __str__(self):
        return f"Preferences for {self.user.username}"

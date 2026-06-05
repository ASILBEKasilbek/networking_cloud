from django.db import models
from apps.core.models import BaseModel, CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


# ==================== CUSTOMERS APP ====================

class Customer(BaseModel):
    """Customer model for B2B and B2C."""
    customer_type = models.CharField(
        max_length=10,
        choices=[('B2B', 'Business'), ('B2C', 'Consumer')],
        default='B2B'
    )
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    
    # Business Info
    tax_id = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # Address
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Business Terms
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_terms = models.CharField(
        max_length=50,
        choices=[('NET30', 'Net 30'), ('NET60', 'Net 60'), ('COD', 'Cash on Delivery'), ('PREPAID', 'Prepaid')],
        default='NET30'
    )
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive'), ('blacklisted', 'Blacklisted')],
        default='active'
    )
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['name']
        indexes = [
            models.Index(fields=['customer_type', 'status']),
            models.Index(fields=['email']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Contact(BaseModel):
    """Contact person for a customer."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, blank=True)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f"{self.name} ({self.customer.name})"


# ==================== PRODUCTS APP ====================

class Category(BaseModel):
    """Product category."""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Product model."""
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    # Pricing
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    list_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    wholesale_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    
    # Details
    unit = models.CharField(max_length=20, default='PCS')
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True)
    
    # Inventory
    reorder_level = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    reorder_quantity = models.IntegerField(default=50, validators=[MinValueValidator(1)])
    
    # Images
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    discontinued = models.BooleanField(default=False)
    
    # Attributes
    attributes = models.JSONField(default=dict, blank=True)  # e.g., color, size, brand
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['sku']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"

    @property
    def profit_margin(self):
        if self.list_price:
            return ((self.list_price - self.cost_price) / self.list_price) * 100
        return 0


# ==================== ORDERS APP ====================

class Order(BaseModel):
    """Sales order model."""
    order_number = models.CharField(max_length=100, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    sales_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Dates
    order_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    shipped_date = models.DateTimeField(null=True, blank=True)
    
    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        db_index=True
    )
    
    # Shipping & Billing
    shipping_address = models.TextField()
    billing_address = models.TextField()
    shipping_method = models.CharField(max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['customer']),
        ]

    def __str__(self):
        return self.order_number

    def update_total(self):
        """Recalculate order total."""
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.total = self.subtotal + self.tax + self.shipping_cost
        self.save(update_fields=['subtotal', 'total'])


class OrderItem(BaseModel):
    """Order line item."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ['order', 'product']

    def __str__(self):
        return f"{self.order.order_number} - {self.product.sku}"

    @property
    def total_price(self):
        return (self.unit_price * self.quantity) * (1 - self.discount / 100) * (1 + self.tax_percent / 100)


# ==================== INVENTORY APP ====================

class StockMovement(BaseModel):
    """Track product stock movements."""
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_movements')
    warehouse = models.CharField(max_length=100)
    movement_type = models.CharField(
        max_length=20,
        choices=[
            ('in', 'Stock In'),
            ('out', 'Stock Out'),
            ('adjustment', 'Adjustment'),
            ('return', 'Return'),
            ('damaged', 'Damaged'),
        ]
    )
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'warehouse']),
        ]

    def __str__(self):
        return f"{self.product.sku} - {self.movement_type} ({self.quantity})"


# ==================== CRM APP ====================

class Lead(BaseModel):
    """Sales lead for potential customers."""
    code = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    source = models.CharField(
        max_length=50,
        choices=[
            ('website', 'Website'),
            ('social_media', 'Social Media'),
            ('referral', 'Referral'),
            ('cold_call', 'Cold Call'),
            ('trade_show', 'Trade Show'),
            ('other', 'Other'),
        ]
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('interested', 'Interested'),
            ('qualified', 'Qualified'),
            ('lost', 'Lost'),
            ('converted', 'Converted'),
        ],
        default='new'
    )
    
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    probability = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.company_name}"


class Interaction(BaseModel):
    """Customer/Lead interaction tracking."""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='interactions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='interactions')
    interaction_type = models.CharField(
        max_length=20,
        choices=[
            ('call', 'Call'),
            ('email', 'Email'),
            ('meeting', 'Meeting'),
            ('note', 'Note'),
            ('task', 'Task'),
        ]
    )
    subject = models.CharField(max_length=255)
    description = models.TextField()
    interaction_date = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
        ordering = ['-interaction_date']

    def __str__(self):
        return f"{self.interaction_type} - {self.subject}"


# ==================== ERP APP ====================

class Supplier(BaseModel):
    """Supplier model."""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    
    # Address
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Business Info
    tax_id = models.CharField(max_length=50, blank=True)
    payment_terms = models.CharField(max_length=50, default='NET30')
    lead_time_days = models.IntegerField(default=7)
    
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive'), ('blacklisted', 'Blacklisted')],
        default='active'
    )
    
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class PurchaseOrder(BaseModel):
    """Purchase order from suppliers."""
    po_number = models.CharField(max_length=100, unique=True, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    
    # Dates
    po_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    received_date = models.DateTimeField(null=True, blank=True)
    
    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Status
    status = models.CharField(
        max_digits=20,
        choices=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('acknowledged', 'Acknowledged'),
            ('partial', 'Partially Received'),
            ('received', 'Received'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        db_index=True
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-po_date']

    def __str__(self):
        return self.po_number


# ==================== WMS APP ====================

class Warehouse(BaseModel):
    """Warehouse/Distribution center."""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    
    # Capacity
    total_capacity = models.DecimalField(max_digits=12, decimal_places=2)  # in cubic meters
    current_utilization = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Staff
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    staff_count = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class PickList(BaseModel):
    """Pick list for order fulfillment."""
    pick_number = models.CharField(max_length=100, unique=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='pick_lists')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    
    picked_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    picked_date = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Pick List'
        verbose_name_plural = 'Pick Lists'
        ordering = ['-created_at']

    def __str__(self):
        return self.pick_number

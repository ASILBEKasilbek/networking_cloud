from django.contrib import admin
from django.utils.html import format_html
from apps.models import (
    Customer, Contact, Category, Product, Order, OrderItem,
    StockMovement, Lead, Interaction, Supplier, PurchaseOrder,
    Warehouse, PickList
)


# ==================== CUSTOMERS ADMIN ====================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'customer_type', 'email', 'city', 'status', 'credit_limit']
    list_filter = ['customer_type', 'status', 'payment_terms', 'created_at']
    search_fields = ['code', 'name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Customer Info', {'fields': ('id', 'code', 'name', 'customer_type', 'email', 'phone', 'website')}),
        ('Business Info', {'fields': ('tax_id', 'industry')}),
        ('Address', {'fields': ('street_address', 'city', 'state', 'postal_code', 'country')}),
        ('Business Terms', {'fields': ('credit_limit', 'payment_terms', 'discount_percentage')}),
        ('Status', {'fields': ('status', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    ordering = ['name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer', 'email', 'phone', 'is_primary']
    list_filter = ['is_primary', 'customer', 'created_at']
    search_fields = ['name', 'email', 'customer__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


# ==================== PRODUCTS ADMIN ====================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'parent', 'is_featured']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['code', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'list_price', 'sale_price', 'is_active']
    list_filter = ['is_active', 'discontinued', 'category', 'created_at']
    search_fields = ['sku', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Product Info', {'fields': ('id', 'sku', 'name', 'description', 'category')}),
        ('Pricing', {'fields': ('cost_price', 'list_price', 'sale_price', 'wholesale_price')}),
        ('Details', {'fields': ('unit', 'weight', 'dimensions')}),
        ('Inventory', {'fields': ('reorder_level', 'reorder_quantity')}),
        ('Images & Attributes', {'fields': ('image', 'attributes')}),
        ('Status', {'fields': ('is_active', 'is_featured', 'discontinued')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


# ==================== ORDERS ADMIN ====================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['id', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'order_date', 'total', 'status']
    list_filter = ['status', 'order_date', 'customer']
    search_fields = ['order_number', 'customer__name']
    readonly_fields = ['id', 'order_date', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {'fields': ('id', 'order_number', 'customer', 'sales_person')}),
        ('Dates', {'fields': ('order_date', 'required_date', 'shipped_date')}),
        ('Amounts', {'fields': ('subtotal', 'tax', 'shipping_cost', 'total')}),
        ('Status & Shipping', {'fields': ('status', 'shipping_method')}),
        ('Addresses', {'fields': ('shipping_address', 'billing_address')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    ordering = ['-order_date']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    list_filter = ['order', 'product']
    search_fields = ['order__order_number', 'product__sku']
    readonly_fields = ['id', 'created_at', 'updated_at']


# ==================== INVENTORY ADMIN ====================

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'movement_type', 'quantity', 'created_by', 'created_at']
    list_filter = ['movement_type', 'warehouse', 'created_at']
    search_fields = ['product__sku', 'reference_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']


# ==================== CRM ADMIN ====================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['code', 'company_name', 'source', 'status', 'priority', 'assigned_to']
    list_filter = ['status', 'source', 'priority', 'created_at']
    search_fields = ['code', 'company_name', 'contact_name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Lead Info', {'fields': ('id', 'code', 'company_name', 'contact_name', 'email', 'phone')}),
        ('Source & Status', {'fields': ('source', 'status', 'priority')}),
        ('Assignment', {'fields': ('assigned_to',)}),
        ('Value', {'fields': ('estimated_value', 'probability')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['interaction_type', 'subject', 'interaction_date', 'created_by']
    list_filter = ['interaction_type', 'interaction_date', 'created_by']
    search_fields = ['subject', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


# ==================== ERP ADMIN ====================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'email', 'status', 'rating']
    list_filter = ['status', 'rating', 'created_at']
    search_fields = ['code', 'name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Supplier Info', {'fields': ('id', 'code', 'name', 'email', 'phone', 'website')}),
        ('Address', {'fields': ('street_address', 'city', 'state', 'postal_code', 'country')}),
        ('Business Info', {'fields': ('tax_id', 'payment_terms', 'lead_time_days')}),
        ('Status & Rating', {'fields': ('status', 'rating')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'po_date', 'total', 'status']
    list_filter = ['status', 'po_date', 'supplier']
    search_fields = ['po_number', 'supplier__name']
    readonly_fields = ['id', 'po_date', 'created_at', 'updated_at']
    fieldsets = (
        ('PO Info', {'fields': ('id', 'po_number', 'supplier')}),
        ('Dates', {'fields': ('po_date', 'required_date', 'received_date')}),
        ('Amounts', {'fields': ('subtotal', 'tax', 'shipping_cost', 'total')}),
        ('Status', {'fields': ('status',)}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


# ==================== WMS ADMIN ====================

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'location', 'current_utilization', 'staff_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'name', 'location']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Warehouse Info', {'fields': ('id', 'code', 'name', 'location')}),
        ('Capacity', {'fields': ('total_capacity', 'current_utilization')}),
        ('Staff', {'fields': ('manager', 'staff_count')}),
        ('Status', {'fields': ('is_active', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PickList)
class PickListAdmin(admin.ModelAdmin):
    list_display = ['pick_number', 'order', 'warehouse', 'status', 'picked_by', 'picked_date']
    list_filter = ['status', 'warehouse', 'created_at']
    search_fields = ['pick_number', 'order__order_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Pick List Info', {'fields': ('id', 'pick_number', 'order', 'warehouse')}),
        ('Status', {'fields': ('status', 'picked_by', 'picked_date')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

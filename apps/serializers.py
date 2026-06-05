from rest_framework import serializers
from apps.models import (
    Customer, Contact, Category, Product, Order, OrderItem,
    StockMovement, Lead, Interaction, Supplier, PurchaseOrder,
    Warehouse, PickList
)


# ==================== CUSTOMERS SERIALIZERS ====================

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'customer', 'name', 'title', 'email', 'phone', 'mobile', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomerSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'customer_type', 'code', 'name', 'email', 'phone', 'website',
            'tax_id', 'industry', 'street_address', 'city', 'state', 'postal_code', 'country',
            'credit_limit', 'payment_terms', 'discount_percentage', 'status', 'notes',
            'contacts', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==================== PRODUCTS SERIALIZERS ====================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'code', 'name', 'description', 'parent', 'image', 'is_featured', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    profit_margin = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'description', 'category', 'category_name',
            'cost_price', 'list_price', 'sale_price', 'wholesale_price',
            'unit', 'weight', 'dimensions', 'reorder_level', 'reorder_quantity',
            'image', 'is_active', 'is_featured', 'discontinued', 'attributes',
            'profit_margin', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_profit_margin(self, obj):
        return obj.profit_margin


# ==================== ORDERS SERIALIZERS ====================

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'product_sku', 'product_name',
            'quantity', 'unit_price', 'discount', 'tax_percent', 'total_price',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_price(self, obj):
        return str(obj.total_price)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    sales_person_name = serializers.CharField(source='sales_person.get_full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'sales_person', 'sales_person_name',
            'order_date', 'required_date', 'shipped_date',
            'subtotal', 'tax', 'shipping_cost', 'total',
            'status', 'shipping_address', 'billing_address', 'shipping_method',
            'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_date', 'created_at', 'updated_at']


# ==================== INVENTORY SERIALIZERS ====================

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_name', 'warehouse', 'movement_type',
            'quantity', 'reference_number', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==================== CRM SERIALIZERS ====================

class LeadSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'code', 'company_name', 'contact_name', 'email', 'phone',
            'source', 'status', 'priority', 'assigned_to', 'assigned_to_name',
            'estimated_value', 'probability', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    lead_code = serializers.CharField(source='lead.code', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Interaction
        fields = [
            'id', 'lead', 'lead_code', 'customer', 'customer_name',
            'interaction_type', 'subject', 'description', 'interaction_date',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==================== ERP SERIALIZERS ====================

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'code', 'name', 'email', 'phone', 'website',
            'street_address', 'city', 'state', 'postal_code', 'country',
            'tax_id', 'payment_terms', 'lead_time_days', 'status', 'rating',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'supplier', 'supplier_name',
            'po_date', 'required_date', 'received_date',
            'subtotal', 'tax', 'shipping_cost', 'total',
            'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'po_date', 'created_at', 'updated_at']


# ==================== WMS SERIALIZERS ====================

class WarehouseSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    utilization_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = Warehouse
        fields = [
            'id', 'code', 'name', 'location', 'total_capacity', 'current_utilization',
            'utilization_percent', 'manager', 'manager_name', 'staff_count',
            'is_active', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_utilization_percent(self, obj):
        if obj.total_capacity:
            return (obj.current_utilization / obj.total_capacity) * 100
        return 0


class PickListSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    picked_by_name = serializers.CharField(source='picked_by.get_full_name', read_only=True)
    
    class Meta:
        model = PickList
        fields = [
            'id', 'pick_number', 'order', 'order_number', 'warehouse', 'warehouse_name',
            'status', 'picked_by', 'picked_by_name', 'picked_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

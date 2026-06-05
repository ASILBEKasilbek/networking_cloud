from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.models import (
    Customer, Contact, Category, Product, Order, OrderItem,
    StockMovement, Lead, Interaction, Supplier, PurchaseOrder,
    Warehouse, PickList
)
from apps.serializers import (
    CustomerSerializer, ContactSerializer, CategorySerializer, ProductSerializer,
    OrderSerializer, OrderItemSerializer, StockMovementSerializer,
    LeadSerializer, InteractionSerializer, SupplierSerializer, PurchaseOrderSerializer,
    WarehouseSerializer, PickListSerializer
)


# ==================== CUSTOMERS VIEWSETS ====================

class CustomerViewSet(viewsets.ModelViewSet):
    """Customer management viewset."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer_type', 'status']
    search_fields = ['name', 'email', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get customer statistics."""
        customer = self.get_object()
        orders = customer.orders.all()
        return Response({
            'total_orders': orders.count(),
            'total_spent': sum(o.total for o in orders),
            'average_order_value': sum(o.total for o in orders) / orders.count() if orders.exists() else 0,
        })


class ContactViewSet(viewsets.ModelViewSet):
    """Contact management viewset."""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['customer', 'is_primary']
    search_fields = ['name', 'email']
    ordering_fields = ['-is_primary', 'name']


# ==================== PRODUCTS VIEWSETS ====================

class CategoryViewSet(viewsets.ModelViewSet):
    """Category management viewset."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """Product management viewset."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active', 'discontinued']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['sku', 'name', 'list_price']
    ordering = ['sku']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock."""
        products = Product.objects.filter(
            stock_movements__movement_type='in',
            reorder_level__gte=0
        ).distinct()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# ==================== ORDERS VIEWSETS ====================

class OrderItemViewSet(viewsets.ModelViewSet):
    """Order item management viewset."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'product']


class OrderViewSet(viewsets.ModelViewSet):
    """Order management viewset."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'status', 'sales_person']
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['order_date', 'total']
    ordering = ['-order_date']

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Get orders assigned to current user."""
        orders = Order.objects.filter(sales_person=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm an order."""
        order = self.get_object()
        if order.status == 'draft':
            order.status = 'confirmed'
            order.save()
            return Response({'status': 'Order confirmed'})
        return Response({'error': 'Order cannot be confirmed'}, status=status.HTTP_400_BAD_REQUEST)


# ==================== INVENTORY VIEWSETS ====================

class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """Stock movement tracking viewset."""
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product', 'warehouse', 'movement_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# ==================== CRM VIEWSETS ====================

class LeadViewSet(viewsets.ModelViewSet):
    """Lead management viewset."""
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source', 'status', 'priority', 'assigned_to']
    search_fields = ['company_name', 'contact_name', 'email']
    ordering_fields = ['created_at', 'estimated_value']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def my_leads(self, request):
        """Get leads assigned to current user."""
        leads = Lead.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        """Convert lead to customer."""
        lead = self.get_object()
        if lead.status != 'converted':
            lead.status = 'converted'
            lead.save()
            return Response({'status': 'Lead converted'})
        return Response({'error': 'Lead already converted'}, status=status.HTTP_400_BAD_REQUEST)


class InteractionViewSet(viewsets.ModelViewSet):
    """Interaction tracking viewset."""
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lead', 'customer', 'interaction_type', 'created_by']
    ordering_fields = ['interaction_date']
    ordering = ['-interaction_date']


# ==================== ERP VIEWSETS ====================

class SupplierViewSet(viewsets.ModelViewSet):
    """Supplier management viewset."""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'code']
    ordering_fields = ['name', 'rating']
    ordering = ['name']


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """Purchase order management viewset."""
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supplier', 'status']
    search_fields = ['po_number', 'supplier__name']
    ordering_fields = ['po_date', 'total']
    ordering = ['-po_date']


# ==================== WMS VIEWSETS ====================

class WarehouseViewSet(viewsets.ModelViewSet):
    """Warehouse management viewset."""
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'location']
    ordering_fields = ['name']
    ordering = ['name']


class PickListViewSet(viewsets.ModelViewSet):
    """Pick list management viewset."""
    queryset = PickList.objects.all()
    serializer_class = PickListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse', 'status', 'picked_by']
    search_fields = ['pick_number', 'order__order_number']
    ordering_fields = ['created_at', 'picked_date']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark pick list as completed."""
        pick_list = self.get_object()
        if pick_list.status == 'pending' or pick_list.status == 'in_progress':
            pick_list.status = 'completed'
            pick_list.picked_by = request.user
            pick_list.picked_date = timezone.now()
            pick_list.save()
            return Response({'status': 'Pick list marked as completed'})
        return Response({'error': 'Pick list cannot be completed'}, status=status.HTTP_400_BAD_REQUEST)

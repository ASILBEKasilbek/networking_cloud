from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Health check view
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Frontend views
from apps.core.views import login_view, dashboard_view, logout_view

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for load balancer."""
    return JsonResponse({
        'status': 'ok',
        'service': 'wholesale_platform',
    })

# Initialize router
router = DefaultRouter()

# Import viewsets from apps
from apps.core.viewsets import HealthViewSet
from apps.viewsets import (
    CustomerViewSet, ContactViewSet, ProductViewSet, CategoryViewSet,
    OrderViewSet, OrderItemViewSet, StockMovementViewSet,
    LeadViewSet, InteractionViewSet, SupplierViewSet, PurchaseOrderViewSet,
    WarehouseViewSet, PickListViewSet
)

# Register viewsets
router.register(r'health', HealthViewSet, basename='health')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movement')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'interactions', InteractionViewSet, basename='interaction')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-order')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'pick-lists', PickListViewSet, basename='pick-list')

urlpatterns = [
    # Frontend pages
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    # Admin
    path('admin/', admin.site.urls),

    # Health check
    path('health/', health_check, name='health-check'),

    # Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API v1
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls')),

    # App-specific URLs
    path('api/v1/customers/', include('apps.customers.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/crm/', include('apps.crm.urls')),
    path('api/v1/erp/', include('apps.erp.urls')),
    path('api/v1/wms/', include('apps.wms.urls')),
]

# Serve media and static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

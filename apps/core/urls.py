from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.viewsets import CustomUserViewSet, AuditViewSet, CompanyInfoViewSet, NotificationPreferenceViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'audit', AuditViewSet, basename='audit')
router.register(r'company', CompanyInfoViewSet, basename='company')
router.register(r'notifications', NotificationPreferenceViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]

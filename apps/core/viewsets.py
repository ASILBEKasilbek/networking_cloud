from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.core.models import CustomUser, Audit, CompanyInfo, NotificationPreference
from apps.core.serializers import CustomUserSerializer, AuditSerializer, CompanyInfoSerializer, NotificationPreferenceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class HealthViewSet(viewsets.ViewSet):
    """Health check endpoint."""
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({'status': 'ok'})


class CustomUserViewSet(viewsets.ModelViewSet):
    """User management viewset."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']

    def get_queryset(self):
        """Users can only see their own profile unless they're admin."""
        if self.request.user.is_staff:
            return super().get_queryset()
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update current user profile."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuditViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit log viewset - read only."""
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['action', 'content_type', 'user']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Only staff can view audit logs."""
        if self.request.user.is_staff:
            return super().get_queryset()
        return Audit.objects.none()


class CompanyInfoViewSet(viewsets.ModelViewSet):
    """Company information viewset."""
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return the first company (single instance)."""
        return super().get_queryset().first() or CompanyInfo.objects.none()

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current company info."""
        company = CompanyInfo.objects.first()
        if company:
            serializer = self.get_serializer(company)
            return Response(serializer.data)
        return Response({'detail': 'No company configured.'}, status=status.HTTP_404_NOT_FOUND)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """Notification preferences viewset."""
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only access their own preferences."""
        if self.request.user.is_staff:
            return super().get_queryset()
        return NotificationPreference.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put'])
    def my_preferences(self, request):
        """Get or update current user's notification preferences."""
        pref, created = NotificationPreference.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(pref)
            return Response(serializer.data)
        
        serializer = self.get_serializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

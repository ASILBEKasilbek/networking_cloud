from rest_framework import serializers
from apps.core.models import CustomUser, Audit, CompanyInfo, NotificationPreference


class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'full_name', 'first_name', 'last_name',
            'phone', 'avatar', 'company', 'department', 'role', 'is_verified',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()


class AuditSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Audit
        fields = [
            'id', 'user', 'user_name', 'action', 'content_type',
            'object_id', 'description', 'changes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = [
            'id', 'name', 'legal_name', 'logo', 'description',
            'email', 'phone', 'website',
            'street_address', 'city', 'state', 'postal_code', 'country',
            'tax_id', 'registration_number', 'industry', 'employee_count',
            'currency', 'fiscal_year_start', 'settings',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'email_notifications', 'sms_notifications',
            'push_notifications', 'newsletter', 'order_updates',
            'inventory_alerts', 'marketing_emails', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

from django.contrib import admin
from django.utils.html import format_html
from apps.core.models import CustomUser, Audit, CompanyInfo, NotificationPreference


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'get_full_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Personal Info', {'fields': ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'avatar')}),
        ('Company Info', {'fields': ('company', 'department', 'role')}),
        ('Verification', {'fields': ('is_verified', 'verification_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    ordering = ['-created_at']


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ['action', 'content_type', 'object_id', 'user', 'created_at']
    list_filter = ['action', 'content_type', 'created_at']
    search_fields = ['user__username', 'content_type', 'description']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_id', 'email', 'country', 'currency']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Company Details', {'fields': ('id', 'name', 'legal_name', 'logo', 'description')}),
        ('Contact Information', {'fields': ('email', 'phone', 'website')}),
        ('Address', {'fields': ('street_address', 'city', 'state', 'postal_code', 'country')}),
        ('Business Information', {'fields': ('tax_id', 'registration_number', 'industry', 'employee_count')}),
        ('Financial Settings', {'fields': ('currency', 'fiscal_year_start')}),
        ('Additional Settings', {'fields': ('settings',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'sms_notifications', 'push_notifications']
    list_filter = ['email_notifications', 'sms_notifications', 'push_notifications', 'newsletter']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']

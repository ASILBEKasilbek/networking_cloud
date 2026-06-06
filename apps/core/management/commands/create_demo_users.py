from django.core.management.base import BaseCommand
from apps.core.models import CustomUser


class Command(BaseCommand):
    help = 'Create demo users for each role'

    def handle(self, *args, **options):
        demo_users = [
            {'username': 'admin_user', 'role': 'admin', 'first_name': 'Admin', 'last_name': 'User', 'email': 'admin@demo.com', 'is_staff': True, 'is_superuser': True},
            {'username': 'manager_user', 'role': 'manager', 'first_name': 'Manager', 'last_name': 'User', 'email': 'manager@demo.com', 'is_staff': True},
            {'username': 'sales_user', 'role': 'sales', 'first_name': 'Sales', 'last_name': 'User', 'email': 'sales@demo.com'},
            {'username': 'warehouse_user', 'role': 'warehouse', 'first_name': 'Warehouse', 'last_name': 'User', 'email': 'warehouse@demo.com'},
            {'username': 'finance_user', 'role': 'finance', 'first_name': 'Finance', 'last_name': 'User', 'email': 'finance@demo.com'},
            {'username': 'customer_user', 'role': 'customer', 'first_name': 'Customer', 'last_name': 'User', 'email': 'customer@demo.com'},
        ]

        for user_data in demo_users:
            username = user_data.pop('username')
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults=user_data
            )
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created: {username} ({user.role})'))
            else:
                self.stdout.write(self.style.WARNING(f'Exists: {username} ({user.role})'))

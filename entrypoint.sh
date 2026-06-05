#!/bin/bash
set -e

echo "================================"
echo "Smart Wholesale Cloud Platform"
echo "================================"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z "$DATABASE_HOST" "${DATABASE_PORT:-5432}"; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
while ! nc -z "$REDIS_HOST" "${REDIS_PORT:-6379}"; do
  sleep 1
done
echo "Redis is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating default superuser..."
python manage.py shell << END
from apps.core.models import CustomUser
if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' created successfully!")
else:
    print("Superuser 'admin' already exists!")
END

echo ""
echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "Admin Panel: http://localhost/admin/"
echo "API Documentation: http://localhost/api/v1/"
echo "Health Check: http://localhost/health/"
echo ""
echo "Default Credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo ""

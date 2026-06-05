#!/bin/bash

# Wholesale Platform - Quick Setup Script
# This script sets up the entire project in one go

set -e

echo "======================================"
echo "Smart Wholesale Cloud Platform Setup"
echo "======================================"
echo ""

PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_DIR"

# Check prerequisites
echo "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed."; exit 1; }
echo "✓ Docker and Docker Compose are installed"
echo ""

# Setup environment
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "  (You may want to edit it with custom values)"
else
    echo "✓ .env file already exists"
fi
echo ""

# Build images
echo "Building Docker images..."
docker-compose build
echo "✓ Docker images built successfully"
echo ""

# Start services
echo "Starting Docker services..."
docker-compose up -d
echo "✓ Docker services started"
echo ""

# Wait for services
echo "Waiting for services to be ready..."
sleep 15
echo "✓ Services are ready"
echo ""

# Run migrations
echo "Running database migrations..."
docker-compose exec -T web python manage.py migrate --noinput
echo "✓ Migrations completed"
echo ""

# Create superuser
echo "Creating default superuser..."
docker-compose exec -T web python manage.py shell << EOF
from apps.core.models import CustomUser
if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✓ Superuser 'admin' created")
else:
    print("✓ Superuser 'admin' already exists")
EOF
echo ""

# Collect static files
echo "Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

# Final message
echo "======================================"
echo "✓ Setup Complete!"
echo "======================================"
echo ""
echo "Access the application:"
echo "  Admin Panel:       http://localhost/admin/"
echo "  API Documentation: http://localhost/api/v1/"
echo "  Health Check:      http://localhost/health/"
echo ""
echo "Default Credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "Next steps:"
echo "  1. View logs:     docker-compose logs -f web"
echo "  2. Run tests:     docker-compose exec web pytest"
echo "  3. Stop services: docker-compose down"
echo ""
echo "For more info, see README.md and PHASE_2_SETUP_GUIDE.md"
echo ""

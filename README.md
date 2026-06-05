# Smart Wholesale Cloud Platform

A production-ready, scalable ERP + CRM + WMS system built with Django 5, PostgreSQL, and Docker.

## 📋 Project Overview

This is a comprehensive wholesale business management platform featuring:
- **ERP**: Enterprise Resource Planning (suppliers, purchase orders, inventory)
- **CRM**: Customer Relationship Management (leads, customers, interactions)
- **WMS**: Warehouse Management System (warehouses, pick lists, stock movements)
- **OMS**: Order Management System (orders, order items, customer management)

## 🏗️ Architecture

```
┌─────────────────┐
│  Docker Compose │
├─────────────────┤
│ • PostgreSQL 16 │ (Database)
│ • Redis 7       │ (Cache & Message Broker)
│ • Django 5      │ (Application)
│ • Celery        │ (Background Tasks)
│ • Nginx         │ (Reverse Proxy)
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development)
- Git

### 1. Clone & Setup
```bash
# Clone repository
git clone <repository-url>
cd networking

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 2. Start with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run migrations (in a new terminal)
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Load sample data
docker-compose exec web python manage.py loaddata initial_data.json
```

### 3. Access the Application
- **API**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

## 📁 Project Structure

```
.
├── config/                   # Django project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── celery.py            # Celery configuration
├── apps/                     # Django applications
│   ├── core/                # Core functionality (users, audit)
│   ├── customers/           # Customer management
│   ├── products/            # Product catalog
│   ├── orders/              # Order management
│   ├── inventory/           # Inventory & stock movements
│   ├── crm/                 # CRM (leads, interactions)
│   ├── erp/                 # ERP (suppliers, purchase orders)
│   └── wms/                 # WMS (warehouses, pick lists)
├── docker-compose.yml       # Docker services definition
├── Dockerfile               # Django application image
├── nginx.conf               # Nginx configuration
├── requirements.txt         # Python dependencies
├── manage.py                # Django management script
└── README.md               # This file
```

## 📦 API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Customers
- `GET /api/v1/customers/` - List customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/{id}/` - Customer detail
- `PUT /api/v1/customers/{id}/` - Update customer
- `DELETE /api/v1/customers/{id}/` - Delete customer
- `GET /api/v1/customers/{id}/statistics/` - Customer statistics

### Products
- `GET /api/v1/categories/` - List categories
- `GET /api/v1/products/` - List products
- `GET /api/v1/products/low_stock/` - Get low stock products

### Orders
- `GET /api/v1/orders/` - List orders
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/{id}/` - Order detail
- `POST /api/v1/orders/{id}/confirm/` - Confirm order

### CRM
- `GET /api/v1/leads/` - List leads
- `GET /api/v1/leads/my_leads/` - My assigned leads
- `POST /api/v1/leads/{id}/convert/` - Convert lead to customer
- `GET /api/v1/interactions/` - List interactions

### Inventory
- `GET /api/v1/stock-movements/` - List stock movements

### ERP
- `GET /api/v1/suppliers/` - List suppliers
- `GET /api/v1/purchase-orders/` - List purchase orders

### WMS
- `GET /api/v1/warehouses/` - List warehouses
- `GET /api/v1/pick-lists/` - List pick lists
- `POST /api/v1/pick-lists/{id}/mark_completed/` - Mark pick list as completed

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Get Access Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Use Token in Requests
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/v1/customers/
```

## 🗄️ Database Models

### Core
- **CustomUser**: Extended user model with roles
- **Audit**: Track all changes
- **CompanyInfo**: Company details
- **NotificationPreference**: User notification settings

### Customers
- **Customer**: B2B/B2C customer
- **Contact**: Customer contact person

### Products
- **Category**: Product categories
- **Product**: Product catalog

### Orders
- **Order**: Sales order
- **OrderItem**: Order line items

### Inventory
- **StockMovement**: Track stock in/out/adjustments

### CRM
- **Lead**: Sales lead
- **Interaction**: Customer/Lead interaction

### ERP
- **Supplier**: Supplier information
- **PurchaseOrder**: Purchase orders

### WMS
- **Warehouse**: Warehouse/distribution center
- **PickList**: Order fulfillment pick lists

## 🛠️ Development

### Local Setup (without Docker)

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Update .env to use localhost for DB/Redis

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# In another terminal, start Celery
celery -A config worker --loglevel=info

# In another terminal, start Celery Beat
celery -A config beat --loglevel=info
```

### Run Tests
```bash
docker-compose exec web pytest

# With coverage
docker-compose exec web pytest --cov=apps --cov-report=html
```

### Code Quality

```bash
# Format code
docker-compose exec web black .

# Lint code
docker-compose exec web flake8

# Sort imports
docker-compose exec web isort .
```

## 📊 Monitoring

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis

# View Django logs
docker-compose exec web tail -f logs/django.log
```

### Health Check
```bash
curl http://localhost/health/
```

### Admin Panel
- URL: http://localhost/admin/
- Default username: `admin`
- Default password: `admin`

## 🔄 Background Tasks

Celery is configured for background task processing:

```python
# Example task
from celery import shared_task

@shared_task
def send_order_confirmation(order_id):
    # Task logic here
    pass
```

### Monitor Tasks
```bash
# View active tasks
docker-compose exec celery celery -A config inspect active

# View stats
docker-compose exec celery celery -A config inspect stats
```

## 📈 Performance Optimization

### Caching (Redis)
- Session storage
- API response caching
- Background task queue

### Database
- Connection pooling
- Query optimization
- Indexed fields

### API Throttling
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour
- Per-endpoint rate limiting

## 🔒 Security

- ✅ HTTPS/TLS encryption
- ✅ JWT authentication
- ✅ CORS protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CSRF protection
- ✅ Rate limiting
- ✅ Secure headers

## 📝 Environment Variables

Key environment variables in `.env`:

```
DEBUG=False                    # Production mode
SECRET_KEY=your-secret-key     # Django secret key
DATABASE_NAME=wholesale_db     # Database name
DATABASE_USER=postgres         # Database user
DATABASE_PASSWORD=password     # Database password
DATABASE_HOST=db               # Database host
DATABASE_PORT=5432            # Database port
REDIS_HOST=redis              # Redis host
REDIS_PORT=6379              # Redis port
ALLOWED_HOSTS=*               # Allowed hosts
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 🚢 Deployment

### AWS Deployment
1. Use AWS RDS for PostgreSQL
2. Use ElastiCache for Redis
3. Deploy Docker images to EC2 or ECS
4. Use Application Load Balancer
5. Configure Route 53 for DNS
6. Use CloudFront for CDN

### Environment-Specific Settings
```python
# Production: DEBUG = False
# Staging: DEBUG = False
# Development: DEBUG = True
```

## 📚 API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
1. Check documentation
2. Review API responses
3. Check logs: `docker-compose logs`
4. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Advanced reporting & analytics
- [ ] Mobile app (React Native)
- [ ] Multi-tenant support
- [ ] Advanced search with Elasticsearch
- [ ] Real-time notifications (WebSocket)
- [ ] Advanced CRM features
- [ ] Accounting integration
- [ ] EDI support

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-01  
**Status**: Production-Ready

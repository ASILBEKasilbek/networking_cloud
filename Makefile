.PHONY: help build up down logs migrate createsuperuser shell test lint format clean

help:
	@echo "Available commands:"
	@echo "  make build              - Build Docker images"
	@echo "  make up                 - Start containers"
	@echo "  make down               - Stop containers"
	@echo "  make logs               - View logs"
	@echo "  make migrate            - Run migrations"
	@echo "  make createsuperuser    - Create admin user"
	@echo "  make shell              - Django shell"
	@echo "  make test               - Run tests"
	@echo "  make lint               - Run linters"
	@echo "  make format             - Format code"
	@echo "  make clean              - Remove generated files"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started. Waiting for database..."
	@sleep 5
	$(MAKE) migrate

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

logs-redis:
	docker-compose logs -f redis

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

shell:
	docker-compose exec web python manage.py shell

shell-db:
	docker-compose exec db psql -U postgres -d wholesale_db

redis-cli:
	docker-compose exec redis redis-cli

test:
	docker-compose exec web pytest

test-verbose:
	docker-compose exec web pytest -v

test-coverage:
	docker-compose exec web pytest --cov=apps --cov-report=html

lint:
	docker-compose exec web flake8 apps config

format:
	docker-compose exec web black apps config
	docker-compose exec web isort apps config

check:
	docker-compose exec web python manage.py check

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

reset-db:
	docker-compose exec web python manage.py flush --no-input
	docker-compose exec web python manage.py migrate

restart:
	docker-compose restart web

restart-all:
	docker-compose restart

ps:
	docker-compose ps

env-example:
	cp .env.example .env
	@echo "Created .env from .env.example"

load-fixtures:
	docker-compose exec web python manage.py loaddata fixtures/*.json

backup-db:
	docker-compose exec db pg_dump -U postgres wholesale_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	@read -p "Enter backup file: " backup; \
	docker-compose exec -T db psql -U postgres wholesale_db < $$backup

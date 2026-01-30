.PHONY: help install dev prod test lint format clean docker-build docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  install       - Install dependencies"
	@echo "  install-dev   - Install development dependencies"
	@echo "  dev           - Run development server"
	@echo "  prod          - Run production server"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linters"
	@echo "  format        - Format code"
	@echo "  clean         - Clean generated files"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-up     - Start Docker containers"
	@echo "  docker-down   - Stop Docker containers"
	@echo "  migrate       - Run database migrations"
	@echo "  init-db       - Initialize database"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

prod:
	gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

test:
	pytest tests/ -v --cov=app --cov-report=html

lint:
	flake8 app tests
	mypy app

format:
	black app tests
	isort app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(message)"

migrate-rollback:
	alembic downgrade -1

init-db:
	python scripts/init_db.py

create-superuser:
	python scripts/create_superuser.py
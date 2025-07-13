# Full-Stack Python Kit - Development Commands

# Default recipe to display available commands
default:
    @just --list

# Setup development environment
setup:
    uv sync --dev
    uv run pre-commit install

# Install dependencies
install:
    uv sync

# Install development dependencies
install-dev:
    uv sync --dev

# Format code with ruff
format:
    uv run ruff format .
    uv run ruff check --fix .

# Lint code with ruff
lint:
    uv run ruff check .

# Type check with mypy
typecheck:
    uv run mypy .

# Run all quality checks
check: lint typecheck

# Run tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=apps --cov=packages --cov-report=html --cov-report=term

# Run CLI app
run-cli *args:
    uv run python -m apps.cli.main {{args}}

# Run GUI app
run-gui:
    uv run python -m apps.gui.main

# Run webapp backend (development)
run-webapp-dev:
    cd apps/webapp/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run webapp frontend (development)
run-webapp-frontend:
    cd apps/webapp/frontend && pnpm dev

# Start all services for development
dev:
    #!/usr/bin/env bash
    echo "Starting Redis..."
    redis-server --daemonize yes --port 6379
    echo "Starting PostgreSQL (assuming local installation)..."
    echo "Starting backend..."
    cd apps/webapp/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    echo "Starting frontend..."
    cd apps/webapp/frontend && pnpm dev &
    echo "All services started. Press Ctrl+C to stop."
    wait

# Database migrations
db-upgrade:
    cd apps/webapp/backend && uv run alembic upgrade head

db-downgrade:
    cd apps/webapp/backend && uv run alembic downgrade -1

db-revision message:
    cd apps/webapp/backend && uv run alembic revision --autogenerate -m "{{message}}"

# Start Celery worker
celery-worker:
    cd apps/webapp/backend && uv run celery -A app.celery worker --loglevel=info

# Start Celery beat (scheduler)
celery-beat:
    cd apps/webapp/backend && uv run celery -A app.celery beat --loglevel=info

# Start Flower (Celery monitoring)
flower:
    cd apps/webapp/backend && uv run celery -A app.celery flower

# Clean up development environment
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    find . -type d -name ".mypy_cache" -exec rm -rf {} +
    find . -type d -name ".coverage" -delete
    find . -type d -name "htmlcov" -exec rm -rf {} +

# Build for production
build:
    uv build

# Install pre-commit hooks
install-hooks:
    uv run pre-commit install

# Run pre-commit on all files
pre-commit:
    uv run pre-commit run --all-files

# Generate documentation
docs:
    echo "Documentation generation not yet implemented"

# Run security checks
security:
    uv run bandit -r apps packages

# Update dependencies
update:
    uv lock --upgrade

# Show project info
info:
    @echo "Full-Stack Python Kit"
    @echo "====================="
    @echo "Python version: $(python --version)"
    @echo "UV version: $(uv --version)"
    @echo "Current directory: $(pwd)"
    @echo ""
    @echo "Available apps:"
    @echo "  CLI: just run-cli --help"
    @echo "  GUI: just run-gui"
    @echo "  Webapp: just run-webapp-dev"
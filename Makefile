.PHONY: help up down logs build migrate status test api-test db dev

help:
	@echo "Available commands:"
	@echo "  make up        - Start all services with docker-compose"
	@echo "  make db        - Start only database (for local development)"
	@echo "  make dev       - Start app locally (requires: make db)"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - Show logs"
	@echo "  make build     - Rebuild containers"
	@echo "  make migrate   - Run migrations"
	@echo "  make status    - Show migration status"
	@echo "  make test      - Run tests"
	@echo "  make api-test  - Test API endpoints"

up:
	docker compose up

db:
	docker compose up db -d

dev:
	@echo "Make sure database is running: make db"
	@echo "Starting application..."
	python main.py

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

migrate:
	docker compose exec app python -m src.infrastructure.database.migration_runner

status:
	docker compose exec app python -m src.infrastructure.database.migration_runner status

test:
	docker compose exec app pytest

api-test:
	./scripts/test_api.sh


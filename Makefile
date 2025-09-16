# Impact Analysis Tool - Makefile

.PHONY: help build up down logs clean demo test lint format

# Default target
help:
	@echo "Impact Analysis Tool - Available Commands:"
	@echo ""
	@echo "  make build     - Build all Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - View logs from all services"
	@echo "  make clean     - Clean up containers and volumes"
	@echo "  make demo      - Run the demo script"
	@echo "  make test      - Run backend tests"
	@echo "  make lint      - Run linting on backend"
	@echo "  make format    - Format backend code"
	@echo ""

# Build all images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up
clean:
	docker-compose down -v
	docker system prune -f

# Run demo
demo:
	python demo/run_demo.py

# Run tests
test:
	cd backend && python -m pytest

# Lint backend
lint:
	cd backend && python -m flake8 src/
	cd backend && python -m mypy src/

# Format backend code
format:
	cd backend && python -m black src/
	cd backend && python -m isort src/

# Initialize demo environment
init:
	./scripts/init_demo.sh

# Generate example diff
diff:
	./scripts/example_diff.sh

# Ingest a repository
ingest:
	@if [ -z "$(REPO)" ]; then \
		echo "Usage: make ingest REPO=<repository_url> [TOKEN=<github_token>]"; \
		echo "Example: make ingest REPO=https://github.com/owner/repo"; \
		exit 1; \
	fi
	./scripts/run_ingest.sh $(REPO) $(TOKEN)

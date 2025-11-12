# ==============================================================================
# Makefile for AI Business Intelligence Agent
# ==============================================================================
# Simplifies common development and deployment tasks
# ==============================================================================

.PHONY: help install dev prod stop clean logs test lint format migrate backup restore

# Default target
.DEFAULT_GOAL := help

# Colors for terminal output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
RESET := \033[0m

# ==============================================================================
# Help
# ==============================================================================

help: ## Show this help message
	@echo "$(CYAN)AI Business Assistant - Makefile Commands$(RESET)"
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ==============================================================================
# Installation & Setup
# ==============================================================================

install: ## Install Python dependencies
	@echo "$(CYAN)Installing Python dependencies...$(RESET)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

setup: ## Initial project setup (dependencies + env + db)
	@echo "$(CYAN)Setting up project...$(RESET)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creating .env from .env.example...$(RESET)"; \
		cp .env.example .env; \
		echo "$(YELLOW)⚠ Please edit .env with your credentials$(RESET)"; \
	fi
	@$(MAKE) install
	@echo "$(GREEN)✓ Setup complete$(RESET)"

# ==============================================================================
# Development
# ==============================================================================

dev: ## Start development environment
	@echo "$(CYAN)Starting development environment...$(RESET)"
	docker-compose up -d
	@echo "$(GREEN)✓ Development environment started$(RESET)"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/api/docs"

dev-build: ## Build and start development environment
	@echo "$(CYAN)Building and starting development environment...$(RESET)"
	docker-compose up -d --build
	@echo "$(GREEN)✓ Development environment started$(RESET)"

# ==============================================================================
# Production
# ==============================================================================

prod: ## Start production environment
	@echo "$(CYAN)Starting production environment...$(RESET)"
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✓ Production environment started$(RESET)"

prod-build: ## Build and start production environment
	@echo "$(CYAN)Building and starting production environment...$(RESET)"
	docker-compose -f docker-compose.prod.yml up -d --build
	@echo "$(GREEN)✓ Production environment started$(RESET)"

# ==============================================================================
# Container Management
# ==============================================================================

stop: ## Stop all containers
	@echo "$(CYAN)Stopping containers...$(RESET)"
	docker-compose down
	docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
	@echo "$(GREEN)✓ Containers stopped$(RESET)"

restart: ## Restart all containers
	@echo "$(CYAN)Restarting containers...$(RESET)"
	@$(MAKE) stop
	@$(MAKE) dev
	@echo "$(GREEN)✓ Containers restarted$(RESET)"

clean: ## Stop containers and remove volumes
	@echo "$(YELLOW)⚠ This will delete all data in volumes$(RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose -f docker-compose.prod.yml down -v 2>/dev/null || true; \
		echo "$(GREEN)✓ Containers and volumes removed$(RESET)"; \
	else \
		echo "$(RED)Cancelled$(RESET)"; \
	fi

# ==============================================================================
# Logs & Monitoring
# ==============================================================================

logs: ## Show logs from all containers
	docker-compose logs -f

logs-api: ## Show API logs
	docker-compose logs -f api

logs-bot: ## Show bot logs
	docker-compose logs -f bot

logs-worker: ## Show worker logs
	docker-compose logs -f worker

logs-db: ## Show database logs
	docker-compose logs -f db

# ==============================================================================
# Database
# ==============================================================================

migrate: ## Run database migrations
	@echo "$(CYAN)Running database migrations...$(RESET)"
	docker-compose exec api alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(RESET)"

migrate-create: ## Create new migration (usage: make migrate-create msg="description")
	@if [ -z "$(msg)" ]; then \
		echo "$(RED)Error: Please provide migration message$(RESET)"; \
		echo "Usage: make migrate-create msg=\"your message\""; \
		exit 1; \
	fi
	@echo "$(CYAN)Creating new migration...$(RESET)"
	docker-compose exec api alembic revision --autogenerate -m "$(msg)"
	@echo "$(GREEN)✓ Migration created$(RESET)"

db-shell: ## Open PostgreSQL shell
	docker-compose exec db psql -U $$DB_USER -d $$DB_NAME

# ==============================================================================
# Backup & Restore
# ==============================================================================

backup: ## Create database backup
	@echo "$(CYAN)Creating database backup...$(RESET)"
	@if [ -f docker-compose.prod.yml ]; then \
		docker-compose -f docker-compose.prod.yml exec db /backup.sh; \
	else \
		docker-compose exec db sh -c "cd /backups && pg_dump -U $$DB_USER $$DB_NAME | gzip > backup_$$(date +%Y%m%d_%H%M%S).sql.gz"; \
	fi
	@echo "$(GREEN)✓ Backup created in ./backups/$(RESET)"

restore: ## Restore database from backup (usage: make restore file=backup.sql.gz)
	@if [ -z "$(file)" ]; then \
		echo "$(RED)Error: Please specify backup file$(RESET)"; \
		echo "Usage: make restore file=backups/backup_20240101_120000.sql.gz"; \
		exit 1; \
	fi
	@echo "$(YELLOW)⚠ This will overwrite the current database$(RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(CYAN)Restoring database...$(RESET)"; \
		docker-compose exec -T db sh -c "gunzip < /backups/$$(basename $(file)) | psql -U $$DB_USER -d $$DB_NAME"; \
		echo "$(GREEN)✓ Database restored$(RESET)"; \
	else \
		echo "$(RED)Cancelled$(RESET)"; \
	fi

# ==============================================================================
# Testing
# ==============================================================================

test: ## Run all tests
	@echo "$(CYAN)Running tests...$(RESET)"
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Tests complete$(RESET)"
	@echo "  Coverage report: htmlcov/index.html"

test-unit: ## Run unit tests only
	@echo "$(CYAN)Running unit tests...$(RESET)"
	pytest tests/unit/ -v
	@echo "$(GREEN)✓ Unit tests complete$(RESET)"

test-integration: ## Run integration tests only
	@echo "$(CYAN)Running integration tests...$(RESET)"
	pytest tests/integration/ -v
	@echo "$(GREEN)✓ Integration tests complete$(RESET)"

# ==============================================================================
# Code Quality
# ==============================================================================

lint: ## Run linters (flake8, mypy)
	@echo "$(CYAN)Running linters...$(RESET)"
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "$(GREEN)✓ Linting complete$(RESET)"

format: ## Format code with black and isort
	@echo "$(CYAN)Formatting code...$(RESET)"
	black .
	isort .
	@echo "$(GREEN)✓ Code formatted$(RESET)"

format-check: ## Check code formatting without modifying
	@echo "$(CYAN)Checking code format...$(RESET)"
	black --check .
	isort --check-only .
	@echo "$(GREEN)✓ Format check complete$(RESET)"

# ==============================================================================
# Security
# ==============================================================================

security: ## Run security checks
	@echo "$(CYAN)Running security checks...$(RESET)"
	safety check
	bandit -r . -ll
	@echo "$(GREEN)✓ Security checks complete$(RESET)"

# ==============================================================================
# Utilities
# ==============================================================================

shell-api: ## Open shell in API container
	docker-compose exec api /bin/bash

shell-bot: ## Open shell in bot container
	docker-compose exec bot /bin/bash

shell-db: ## Open shell in database container
	docker-compose exec db /bin/sh

ps: ## Show running containers
	docker-compose ps

stats: ## Show container resource usage
	docker stats

# ==============================================================================
# Documentation
# ==============================================================================

docs: ## Generate project documentation
	@echo "$(CYAN)Generating documentation...$(RESET)"
	@echo "$(YELLOW)Not implemented yet$(RESET)"

# ==============================================================================
# Environment
# ==============================================================================

env-check: ## Validate .env configuration
	@echo "$(CYAN)Checking environment configuration...$(RESET)"
	python -m config.settings
	@echo "$(GREEN)✓ Environment check complete$(RESET)"

env-generate-jwt: ## Generate new JWT secret key
	@echo "$(CYAN)Generating JWT secret key...$(RESET)"
	@python -c "import secrets; print(secrets.token_hex(32))"

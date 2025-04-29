# =================================================
# Enhanced Makefile for Docker-based Development
# =================================================

# Configuration variables
DOCKER_COMPOSE_FILE = docker-compose.dev.yml
BACKEND_ENV_FILE =  src/.env
DOCKER_COMPOSE_CMD = docker compose -f ${DOCKER_COMPOSE_FILE} --env-file ${BACKEND_ENV_FILE}

# Colors for better readability
CYAN = \033[0;36m
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
RESET = \033[0m

# Define all phony targets (targets that don't produce a file with the target's name)
.PHONY: help setup up build restart down build-up logs rebuild-tools \
        generate-migration migrate-up migrate-up-latest migrate-down migrate-down-previous \
        ruff lint test clean prepare-env-files

# Default target when just 'make' is executed
.DEFAULT_GOAL := help

# =================================================
# HELP SECTION
# =================================================
help:
	@echo "${CYAN}Docker Commands:${RESET}"
	@echo "  ${GREEN}make up${RESET}                    - Start containers in detached mode"
	@echo "  ${GREEN}make build${RESET}                 - Build containers"
	@echo "  ${GREEN}make restart${RESET}               - Restart containers"
	@echo "  ${GREEN}make down${RESET}                  - Stop and remove containers"
	@echo "  ${GREEN}make build-up${RESET}              - Build and start containers"
	@echo "  ${GREEN}make logs${RESET}                  - Show logs from containers"
	@echo "  ${GREEN}make clean${RESET}                 - Clean up Docker resources"
	@echo ""
	@echo "${CYAN}Migration Commands:${RESET}"
	@echo "  ${GREEN}make generate-migration name=...${RESET} - Generate a new migration"
	@echo "  ${GREEN}make migrate-up-latest${RESET}     - Run migrations up to latest"
	@echo "  ${GREEN}make migrate-up n=...${RESET}      - Run n migrations up"
	@echo "  ${GREEN}make migrate-down-previous${RESET} - Revert last migration"
	@echo "  ${GREEN}make migrate-down n=...${RESET}    - Revert n migrations"
	@echo ""
	@echo "${CYAN}Development Commands:${RESET}"
	@echo "  ${GREEN}make ruff${RESET}                  - Run ruff linter"
	@echo "  ${GREEN}make lint${RESET}                  - Run all linters"
	@echo "  ${GREEN}make format${RESET}                - Run code formatting"
	@echo "  ${GREEN}make test${RESET}                  - Run tests"
	@echo "  ${GREEN}make rebuild-tools${RESET}         - Rebuild development tools"
	@echo ""
	@echo "${CYAN}Setup Commands:${RESET}"
	@echo "  ${GREEN}make prepare-env-files${RESET}     - Create environment files"
	@echo "  ${GREEN}make setup${RESET}                 - Complete project setup"

# =================================================
# CONTAINER MANAGEMENT
# =================================================
up:
	@echo "${CYAN}Starting containers in detached mode...${RESET}"
	@${DOCKER_COMPOSE_CMD} up --detach

build:
	@echo "${CYAN}Building containers...${RESET}"
	@${DOCKER_COMPOSE_CMD} build

restart:
	@echo "${CYAN}Restarting containers...${RESET}"
	@${DOCKER_COMPOSE_CMD} restart

down:
	@echo "${CYAN}Stopping and removing containers...${RESET}"
	@${DOCKER_COMPOSE_CMD} down

build-up:
	@echo "${CYAN}Building and starting containers...${RESET}"
	@${DOCKER_COMPOSE_CMD} up --build --detach

logs:
	@echo "${CYAN}Showing container logs (press Ctrl+C to exit)...${RESET}"
	@${DOCKER_COMPOSE_CMD} logs -f

clean:
	@echo "${CYAN}Cleaning up Docker resources...${RESET}"
	@${DOCKER_COMPOSE_CMD} down --volumes --remove-orphans

# =================================================
# MIGRATIONS
# =================================================
generate-migration:
	@if [ -z "$(name)" ]; then \
		echo "${RED}Error: Missing migration name. Usage: make generate-migration name=your_migration_name${RESET}"; \
		exit 1; \
	fi
	@echo "${CYAN}Generating migration: $(name)${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm --user $$(id -u):$$(id -g) migrations \
		sh -c "alembic revision --autogenerate -m '$(name)'"

migrate-up-latest:
	@echo "${CYAN}Running migrations up to latest version...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm migrations sh -c "alembic upgrade head"

migrate-up:
	@if [ -z "$(n)" ]; then \
		echo "${RED}Error: Missing number of migrations. Usage: make migrate-up n=number_of_migrations${RESET}"; \
		exit 1; \
	fi
	@echo "${CYAN}Running $(n) migrations up...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm migrations sh -c "alembic upgrade +$(n)"

migrate-down-previous:
	@echo "${CYAN}Reverting previous migration...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm migrations sh -c "alembic downgrade -1"

migrate-down:
	@if [ -z "$(n)" ]; then \
		echo "${RED}Error: Missing number of migrations. Usage: make migrate-down n=number_of_migrations${RESET}"; \
		exit 1; \
	fi
	@echo "${CYAN}Reverting $(n) migrations...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm migrations sh -c "alembic downgrade -$(n)"

# =================================================
# DEVELOPMENT TOOLS
# =================================================
rebuild-tools:
	@echo "${CYAN}Rebuilding development tools...${RESET}"
	@${DOCKER_COMPOSE_CMD} build migrations
	@${DOCKER_COMPOSE_CMD} build dev-tools

ruff:
	@echo "${CYAN}Running ruff linter...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm dev-tools sh -c "ruff check"

lint: ruff
	@echo "${CYAN}Running additional linters...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm dev-tools sh -c "ruff format --check"

format:
	@echo "${CYAN}Running code formatting...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm dev-tools sh -c "ruff check --fix ."
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm dev-tools sh -c "ruff format ."

test:
	@echo "${CYAN}Running tests...${RESET}"
	@${DOCKER_COMPOSE_CMD} --profile tools run --rm dev-tools sh -c "pytest"

prepare-env-files:
	@echo "${CYAN}Preparing environment files...${RESET}"
	@if [ ! -f src/.env ]; then \
		cp .env.backend.example ${BACKEND_ENV_FILE}; \
		echo "${GREEN}Environment files prepared successfully${RESET}"; \
	else \
		echo "${YELLOW}Environment file already exists, skipping${RESET}"; \
	fi

# Complete project setup in one command
setup: prepare-env-files build-up
	@echo "${GREEN}Setup complete!${RESET}"
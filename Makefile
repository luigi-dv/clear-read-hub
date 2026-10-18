# Shortcuts for the local Docker stack. Only Docker is required.
# Without make, run the `docker compose` command shown for each target.

.DEFAULT_GOAL := help
.PHONY: help up down clean logs ps test lint demo

help: ## Show this help
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  make %-6s %s\n", $$1, $$2}'

up: ## Build and start the stack, wait until it is healthy
	docker compose up -d --build --wait
	@echo "API ready at http://localhost:$${API_PORT:-8000}/docs"

down: ## Stop the stack (data is kept)
	docker compose down

clean: ## Stop the stack and delete all data
	docker compose down -v --remove-orphans

logs: ## Follow the API and worker logs
	docker compose logs -f api worker

ps: ## Show the services and their health
	docker compose ps

test: ## Run all tests, integration included, against the stack services
	docker compose build tests
	docker compose run --rm tests

lint: ## Run ruff and black
	docker compose build tests
	docker compose run --rm tests sh -c "ruff check . && black --check ."

demo: ## Register a user, upload samples/sample.pdf and print its text
	docker compose build demo
	docker compose run --rm demo

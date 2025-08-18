.PHONY: setup-env up down test

up: setup-env
	@echo "Starting up services..."
	@docker compose -f docker-compose.yml up --build -d

down:
	@echo "Stopping services..."
	@docker compose -f docker-compose.yml down

test: up
	@echo "Running tests..."
	@docker compose -f docker-compose.yml run --build --rm tests

setup-env:
	@echo "Searching for .env.example files and creating .env copies..."
	@find . -type f -name ".env.example" -exec sh -c 'cp "$$0" "$$(dirname "$$0")/.env"' {} \;
	@echo "Done."

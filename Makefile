# Makefile for AICPR_MSE

DB_CONTAINER=aipcr_mse-db-1
BACKEND_CONTAINER=aipcr_mse-backend-1

# Run the database shell
dbshell:
	docker exec -it $(DB_CONTAINER) psql -U myuser -d mydb

# Create a new migration (usage: make makemigrations m="add new field")
makemigrations:
	docker compose exec $(BACKEND_CONTAINER) alembic revision --autogenerate -m "$(m)"

# Apply latest migrations
migrate:
	docker compose exec $(BACKEND_CONTAINER) alembic upgrade head

# Rebuild and start containers
up:
	docker compose up --build

# Stop containers
down:
	docker compose down

# Show logs
logs:
	docker compose logs -f

# Open a shell inside backend container
shell:
	docker compose exec $(BACKEND_CONTAINER) /bin/sh

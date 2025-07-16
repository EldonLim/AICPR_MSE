# AICPR_MSE
.env

docker compose up --build

# Makefile (optional)
migrate:
	docker compose exec backend alembic upgrade head

makemigrations:
	docker compose exec backend alembic revision --autogenerate -m "$(m)"

.PHONY: infra-up infra-down infra-logs backend dev lint test

# ==========================================
# Infrastructure
# ==========================================
infra-up:
	docker compose up -d

infra-down:
	docker compose down

infra-logs:
	docker compose logs -f

# ==========================================
# Backend
# ==========================================
backend-install:
	cd backend && pip install -e ".[dev]"

backend-dev:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# ==========================================
# Code Quality
# ==========================================
lint:
	cd backend && ruff check .
	cd backend && mypy .

test:
	cd backend && pytest tests/ -v

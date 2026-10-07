.PHONY: sync up down db run worker test smoke-rag smoke-rbac demo-phap-che

sync:
	uv sync --all-extras

up:
	docker compose up -d postgres redis

down:
	docker compose down

db:
	uv run python -m app.bootstrap_db

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

worker:
	uv run python -m app.workers.ingest_worker

test:
	uv run pytest -q

smoke-rag:
	bash scripts/smoke_rag.sh

smoke-rbac:
	bash scripts/smoke_rbac.sh

demo-phap-che:
	bash scripts/demo_phap_che.sh

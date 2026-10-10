set -e
cat > 'pyproject.toml' <<'FIXTURE_EOF'
[project]
name = "quotes-api"
version = "0.4.0"
description = "HTTP API that serves price quotes for the checkout"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "uvicorn>=0.30", "psycopg[binary]>=3.2"]

[dependency-groups]
dev = ["pytest>=8", "httpx>=0.27"]
FIXTURE_EOF
cat > 'uv.lock' <<'FIXTURE_EOF'
version = 1
FIXTURE_EOF
cat > 'Makefile' <<'FIXTURE_EOF'
run:
	uv run uvicorn quotes.main:app --reload --port 8000

test:
	uv run pytest
FIXTURE_EOF
mkdir -p 'quotes'
cat > 'quotes/__init__.py' <<'FIXTURE_EOF'

FIXTURE_EOF
mkdir -p 'quotes'
cat > 'quotes/main.py' <<'FIXTURE_EOF'
import os
from fastapi import FastAPI
import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/quotes/{sku}")
def quote(sku: str):
    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute("select price_cents from prices where sku = %s", (sku,)).fetchone()
    return {"sku": sku, "price_cents": row[0] if row else None}
FIXTURE_EOF
mkdir -p 'tests'
cat > 'tests/test_health.py' <<'FIXTURE_EOF'
from fastapi.testclient import TestClient

def test_health(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    from quotes.main import app
    assert TestClient(app).get("/health").json() == {"ok": True}
FIXTURE_EOF

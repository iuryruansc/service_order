#!/bin/bash
set -e

echo "Rodando migrations..."
alembic upgrade head

echo "Iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
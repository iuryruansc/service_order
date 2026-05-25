#!/bin/bash
set -e

echo "Aguardando banco de dados..."
python - <<'PY'
import os
import sys
import time
try:
	import psycopg2
except Exception:
	print('psycopg2 não disponível, pulando checagem de conexão', file=sys.stderr)
	sys.exit(0)

url = os.environ.get('DATABASE_URL')
if not url:
	print('DATABASE_URL não definido; as migrations podem falhar', file=sys.stderr)
	sys.exit(0)

max_tries = 30
for i in range(max_tries):
	try:
		conn = psycopg2.connect(url)
		conn.close()
		print('Banco disponível')
		break
	except Exception as e:
		print(f'Tentativa {i+1}/{max_tries} falhou: {e}', file=sys.stderr)
		time.sleep(2)
else:
	print('Não foi possível conectar ao banco após várias tentativas', file=sys.stderr)
	sys.exit(1)
PY

echo "Rodando migrations..."
alembic upgrade head

echo "Iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
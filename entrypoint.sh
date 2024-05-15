#!/bin/sh

echo "Database URL: $DATABASE_URL"

# データベースが起動するのを待機
./wait-for-it.sh fasttodo_database:5432 --timeout=30 --strict -- echo "Database is up"

# コンテナ起動時にmigrateしてデータベースの構成を最新にする
poetry run alembic upgrade head
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_todo.app:app

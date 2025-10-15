#!/bin/sh

# Load environment variables
export $(grep -v '^#' .env | xargs)

echo "Waiting for Postgres to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

echo "Postgres is up - running migrations"
alembic -c app/alembic.ini upgrade head

echo "Starting FastAPI"
exec uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT
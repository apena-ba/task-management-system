#!/bin/sh

echo "\nWaiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT...\n"

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "\nPostgres is up!\n"

echo "\nRunning migrations...\n"
python3 manage.py makemigrations
python3 manage.py migrate

echo "\nCollecting static files...\n"
python3 manage.py collectstatic --noinput

echo "\nStarting: $@\n"
exec "$@"

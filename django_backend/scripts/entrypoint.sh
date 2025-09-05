#!/bin/sh

echo "\nWaiting for Postgres...\n"

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "\nStarting Django...\n"

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000

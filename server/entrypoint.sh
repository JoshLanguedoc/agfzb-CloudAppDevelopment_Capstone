#!/bin/sh

if  [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
  done

  echo "PostgreSQL started"
fi

# MAke migrations and migrate database
echo "Making migrations and migrating database."
python manage.py makemigrations main --noinput
python manage.py migrate --noinput
exec "$@"

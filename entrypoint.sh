#!/bin/sh

echo "Apply database migrations..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn spk.wsgi:application --bind 0.0.0.0:8080 --workers 3
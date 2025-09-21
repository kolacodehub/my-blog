#!/bin/bash

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate

if [[ "$RAILWAY_ENVIRONMENT" == "production" ]]; then
    echo "Starting with Gunicorn..."
    exec poetry run gunicorn djangocourse.wsgi:application --workers 4 --bind 0.0.0.0:$PORT --forwarded-allow-ips="*"
else
    echo "Starting with Django runserver..."
    exec poetry run python manage.py runserver 0.0.0.0:8000
fi

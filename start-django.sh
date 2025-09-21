#!/bin/bash

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate

if [[ "$ENV_STATE" == "production" ]]; then
    echo "Starting with Gunicorn..."
    poetry run gunicorn djangocourse.wsgi --workers 4 --bind 0.0.0.0:8000 --forwarded-allow-ips "*"
else
    echo "Starting with Django runserver..."
    poetry run python manage.py runserver 0.0.0.0:8000
fi

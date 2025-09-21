#!/bin/bash
set -e

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate

if [[ "$ENV_STATE" == "production" ]]; then
    poetry run gunicorn djangocourse.wsgi --workers ${GUNICORN_WORKERS:-4} --bind 0.0.0.0:8000 --forwarded-allow-ips="*"
else
    poetry run python manage.py runserver 0.0.0.0:8000
fi


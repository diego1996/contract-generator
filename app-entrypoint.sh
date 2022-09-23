#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn core.wsgi:application --workers 3 --log-level debug --bind 0.0.0.0:8000

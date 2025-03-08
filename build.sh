#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

if [ "$DJANGO_CREATEUSER" == "1" ]; then 
    python marketplace/manage.py createsuperuser --noinput
fi

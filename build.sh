#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --noinput
python manage.py migrate

if [ "$DJANGO_CREATEUSER" == "1" ]; then 
    python mysite/manage.py createsuperuser --noinput
fi

python marketplace/manage.py runserver 0.0.0.0:$PORT
#!/bin/bash

python marketplace/manage.py collectstatic --noinput
python marketplace/manage.py migrate


if [ "$DJANGO_CREATEUSER" == "1" ]; then 
    python marketplace/manage.py createsuperuser --noinput
fi

python marketplace/manage.py runserver 0.0.0.0:$PORT
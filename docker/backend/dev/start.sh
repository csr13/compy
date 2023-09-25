#!/bin/sh

cd /src;

python manage.py makemigrations 
python manage.py migrate
python manage.py collectstatic --no-input 
python manage.py create_su
python manage.py compliance_initial_migrations

gunicorn --workers=3 \
    --threads=2 \
    --reload \
    --bind=0.0.0.0:6969 \
    --access-logfile - \
    config.wsgi:application

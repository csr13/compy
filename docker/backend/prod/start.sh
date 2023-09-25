#!/bin/sh

set -e 

settings=config.prod.settings

cd /src;

python manage.py makemigrations --settings=$settings
python manage.py migrate --settings=$settings
python manage.py collectstatic --no-input --settings=$settings
python manage.py create_su --settings=$settings
python manage.py compliance_initial_migrations --settings=$settings


gunicorn --workers=3 \
    --threads=2 \
    --reload \
    --bind=0.0.0.0:6969 \
    --access-logfile - \
    config.prod.wsgi_prod:application

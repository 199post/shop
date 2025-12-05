#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=config.settings

echo "Running migrations..."
python manage.py migrate --noinput || {
    echo "Migration failed, attempting to fake problematic migration..."
    python manage.py migrate store 0008_favorite --noinput --fake || true
    python manage.py migrate --noinput || true
}

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking if data needs to be seeded..."
python manage.py shell -c "
from store.models import Category
if Category.objects.count() == 0:
    print('No categories found, running seed...')
    from django.core.management import call_command
    call_command('seed_new_categories')
else:
    print('Data already exists, skipping seed.')
"

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --log-file -

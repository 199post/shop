#!/bin/bash
set -e

echo "Running migrations..."
# Try normal migration first, if it fails on store_favorite, fake it
python manage.py migrate --noinput || {
    echo "Migration failed, attempting to fake problematic migration..."
    python manage.py migrate store 0007_productimage --noinput --fake || true
    python manage.py migrate store 0008_favorite --noinput --fake || true
    python manage.py migrate --noinput
}

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Check if categories exist, if not - seed
echo "Checking if data needs to be seeded..."
python -c "
import django
django.setup()
from store.models import Category
if Category.objects.count() == 0:
    print('No categories found, running seed...')
    import subprocess
    subprocess.run(['python', 'manage.py', 'seed_new_categories'], check=True)
else:
    print('Data already exists, skipping seed.')
"

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --log-file -

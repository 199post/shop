#!/usr/bin/env bash
# Скрипт сборки для Render.com

set -o errexit

pip install -r requirements.txt

cd src
python manage.py collectstatic --noinput
python manage.py migrate

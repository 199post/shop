# Dockerfile
FROM python:3.11-slim

# ----- Базовые настройки Python -----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PYTHONPATH=/app

# ----- Системные зависимости (psycopg2, PostgreSQL client) -----
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ----- Рабочая директория -----
WORKDIR /app

# ----- Установка Python-зависимостей -----
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----- Код проекта (для прод-сборок) -----
# Локально этот код будет ЗАТЕРТ volume-ом ./src:/app,
# поэтому можно не переживать, что здесь старая версия.
COPY ./src /app

# Порт по умолчанию (для Railway / gunicorn)
EXPOSE 8080

# ----- Команда по умолчанию (prod-режим) -----
# Локально в docker-compose мы ПЕРЕОПРЕДЕЛИМ команду на runserver.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:${PORT:-8080}", "--log-file", "-"]

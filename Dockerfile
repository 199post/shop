# Базовый образ Python
FROM python:3.11-slim

# ===== Общие настройки Python =====
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PYTHONPATH=/app

# ===== Системные зависимости (для PostgreSQL / psycopg2) =====
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ===== Рабочая директория в контейнере =====
WORKDIR /app

# ===== Установка Python-зависимостей =====
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===== Копируем весь Django-проект (src содержит manage.py, config, store, accounts) =====
COPY ./src /app

# Railway обычно прокидывает PORT=8080, но укажем EXPOSE для наглядности
EXPOSE 8080

# ===== Команда старта контейнера =====
# 1) применяем миграции
# 2) сидируем данные (если товары уже есть — твоя команда пропустит)
# 3) собираем статику
# 4) запускаем gunicorn на порту $PORT (или 8080 по умолчанию)
CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py seed_db && \
    python manage.py collectstatic --noinput && \
    gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --log-file - \
    "]

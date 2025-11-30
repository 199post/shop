FROM python:3.11-slim

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Установка системных зависимостей для PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Рабочая папка в контейнере
WORKDIR /app

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект (src содержит manage.py и приложение)
COPY ./src /app

# Команда старта:
# 1) применяем миграции
# 2) сидируем данные (если БД пустая)
# 3) собираем статику
# 4) запускаем сервер (для Railway используется Procfile)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_db && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]

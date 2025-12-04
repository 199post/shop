# ------------------------------
# 1) Базовый образ Python
# ------------------------------
FROM python:3.11-slim

# ------------------------------
# 2) Настройки Python
# ------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PYTHONPATH=/app

# ------------------------------
# 3) Установка системных зависимостей
# ------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------
# 4) Рабочая директория
# ------------------------------
WORKDIR /app

# ------------------------------
# 5) Установка Python-зависимостей
# ------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------
# 6) Копируем весь проект
#    (Railway НЕ использует volumes, поэтому COPY обязателен)
#    В локальной разработке volume ./src:/app ПЕРЕЗАТРЁТ эти файлы
# ------------------------------
COPY ./src /app

# ------------------------------
# 7) EXPOSE — Railway проигнорирует,
#    но полезно для документации
# ------------------------------
EXPOSE 8080

# ------------------------------
# 8) Production CMD для Railway
#
#    ВНИМАНИЕ:
#    Обязательно используем `sh -c`, иначе ${PORT} не подставится!
# ------------------------------
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --log-file -"]

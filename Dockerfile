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
# 7) Делаем start.sh исполняемым
# ------------------------------
RUN chmod +x /app/start.sh

# ------------------------------
# 8) EXPOSE — документация порта
# ------------------------------
EXPOSE 8080

# ------------------------------
# 9) Production CMD
# ------------------------------
CMD ["/bin/bash", "/app/start.sh"]

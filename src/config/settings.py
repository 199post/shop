import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ===================== БАЗОВЫЕ НАСТРОЙКИ =====================

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key")

# DEBUG: 1 / 0 в переменной окружения
DEBUG = bool(int(os.environ.get("DEBUG", "1")))

# Хосты: берём из переменной окружения, по умолчанию локалхосты
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost 127.0.0.1 [::1]"
).split()

# Доверенные origin'ы для CSRF (Render + Railway + localhost)
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "https://localhost http://localhost https://*.railway.app https://*.onrender.com"
).split()

# Чтобы Django правильно понимал HTTPS за прокси Railway
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ===================== ПРИЛОЖЕНИЯ =====================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.categories_processor",
                "store.context_processors.footer_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ===================== БАЗА ДАННЫХ =====================

# Render передаёт DATABASE_URL, а для локальной разработки используем отдельные переменные
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("DB_NAME", BASE_DIR / "db.sqlite3"),
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", ""),
            "PORT": os.environ.get("DB_PORT", ""),
        }
    }

# ===================== ПАРОЛИ =====================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ===================== ЛОКАЛЬ =====================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===================== СТАТИКА =====================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ===================== МЕДИАФАЙЛЫ =====================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===================== АВТОРИЗАЦИЯ =====================

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"


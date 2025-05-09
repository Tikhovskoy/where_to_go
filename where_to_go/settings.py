import os
from pathlib import Path

# Базовая папка проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: секретный ключ из окружения (для dev fallback — sqlite-ключ)
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-fallback-secret-key'
)

# DEBUG-режим по переменной, по умолчанию False
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# ALLOWED_HOSTS берём из строки через запятую
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Приложения
INSTALLED_APPS = [
    # сторонние
    'tinymce',
    'adminsortable2',

    # стандартные
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # наши
    'core',
    'places',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise — для отдачи статики в production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'where_to_go.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'where_to_go.wsgi.application'


# База данных: из DATABASE_URL или sqlite по умолчанию
import dj_database_url  # pip install dj-database-url

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# Парольная валидация
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Локализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Статика
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'static_collected'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа (загружаемые файлы)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# TinyMCE
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': 700,
    'menubar': True,
    'plugins': (
        'advlist autolink lists link image charmap print preview anchor '
        'searchreplace visualblocks code fullscreen '
        'insertdatetime media table paste code help wordcount'
    ),
    'toolbar': (
        'undo redo | formatselect | bold italic underline strikethrough | '
        'alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | '
        'link image media | removeformat | code | help'
    ),
    'toolbar_mode': 'sliding',
    'branding': False,
}

# По умолчанию для новых моделей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

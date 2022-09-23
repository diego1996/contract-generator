"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3=!zu)1%$e*p4t@7m!l97y7aa+f)opipn&65b-3y$^1%v&oj=_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = [
    '*'
]

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'colorfield',
    'djmoney',
    'django_cleanup.apps.CleanupConfig',
    'contracts.apps.ContractsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/'

CSRF_TRUSTED_ORIGINS = [
    'http://contratos.observatoriodesaludvillavicencio.org',
    'https://contratos.observatoriodesaludvillavicencio.org',
    'https://web.observatoriodesaludvillavicencio.org',
    'https://ingeomaq.com'
    'https://www.ingeomaq.com'
]

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

CORS_ALLOW_ALL_ORIGINS = True

# Static and Media Minio S3 - django-minio-storage
INSTALLED_APPS += ['minio_storage']
MINIO_HTTPS = os.getenv('MINIO_HTTPS')
MINIO_HOST = os.getenv('MINIO_HOST')
MINIO_URL = os.getenv('MINIO_URL', '')
MINIO_PORT = os.getenv('MINIO_PORT')
MEDIA_BUCKET = os.getenv('MEDIA_BUCKET', '')
STATIC_BUCKET = os.getenv('STATIC_BUCKET')

# These settings should generally not be used:
MINIO_STORAGE_MEDIA_URL = f"https://{MINIO_URL}/{MEDIA_BUCKET}"
MINIO_STORAGE_STATIC_URL = f"https://{MINIO_URL}/{STATIC_BUCKET}"

if not DEBUG:
    DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
    STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
    MINIO_STORAGE_ENDPOINT = f"{MINIO_HOST}:{MINIO_PORT}"
    MINIO_STORAGE_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_STORAGE_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', '')
    MINIO_STORAGE_USE_HTTPS = MINIO_HTTPS
    MINIO_STORAGE_MEDIA_BUCKET_NAME = MEDIA_BUCKET
    MINIO_STORAGE_STATIC_BUCKET_NAME = STATIC_BUCKET

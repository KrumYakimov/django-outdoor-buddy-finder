"""
Django settings for outdoor_buddy project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from decouple import config
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', config("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', config('DEBUG')) == "True"

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', config('ALLOWED_HOSTS')).split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', config('CSRF_TRUSTED_ORIGINS', [])).split(',')



# Application definition

PROJECT_APPS = [
    "outdoor_buddy.accounts.apps.AccountsConfig",
    "outdoor_buddy.core.apps.CommonConfig",
    "outdoor_buddy.events.apps.EventsConfig",
    "outdoor_buddy.connections.apps.ConnectionsConfig",
    "outdoor_buddy.reviews.apps.ReviewsConfig",
    "outdoor_buddy.common",
]

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
] + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "outdoor_buddy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Default context processors
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processor
                "outdoor_buddy.utils.context_processors.add_profile_to_context",
            ],
        },
    },
]

WSGI_APPLICATION = "outdoor_buddy.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = (BASE_DIR / "static",)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.AppUser"

LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGIN_URL = reverse_lazy("signin")
LOGOUT_REDIRECT_URL = reverse_lazy("home")

# AWS SES Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", config("AWS_ACCESS_KEY"))
AWS_SECRET = os.getenv("AWS_SECRET", config("AWS_SECRET")),
AWS_BUCKET = os.getenv("AWS_SECRET", config("AWS_BUCKET")),
AWS_REGION = os.getenv("AWS_SECRET", config("AWS_REGION")),
EMAIL_SENDER = os.getenv("AWS_SECRET", config("EMAIL_SENDER")),
AWS_QUERYSTRING_AUTH = False  # Public access to files (optional)

# Media files
DEFAULT_FILE_STORAGE = "outdoor_buddy_finder.services.storage.S3Storage"  # "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# SMTP Server Settings
EMAIL_HOST = os.getenv("EMAIL_HOST", config("EMAIL_HOST")),
EMAIL_PORT = os.getenv("EMAIL_HOST", config("EMAIL_PORT")),
EMAIL_USE_TLS = os.getenv("EMAIL_HOST", config("EMAIL_USE_TLS")),
EMAIL_HOST_USER = os.getenv("EMAIL_HOST", config("EMAIL_HOST_USER")),
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST", config("EMAIL_HOST_PASSWORD")),
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST", config("DEFAULT_FROM_EMAIL")),

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Outdoor Buddy Finder",
    "DESCRIPTION": "Outdoor Buddy Finder is a platform created to unite outdoor enthusiasts",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # OTHER SETTINGS
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "outdoor_buddy": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
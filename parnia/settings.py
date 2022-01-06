# -*- coding: utf-8 -*-
#
# parnia/settings.py
#
"""
Project Setting File.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-il_n8(2*zw-qxq53nkb((cb0#75a%mqosih^28mp29o2b$1k$j"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #'django_filters',
    "django_extensions",  # to work with jupyter
    # 'django.contrib.admindocs' #for documentation purposes
    "rest_framework",
    "rest_framework.authtoken",
    "user_management",
    "course_management",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
	
    #'course_management.middleware.CountRequestsMiddleware',
]

ROOT_URLCONF = "parnia.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "parnia.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "Parnia",
        "USER": "postgres",
        "PASSWORD": "royapassword",
        "HOST": "127.0.0.1",
        "PORT": "5433",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "user_management.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 5,
    #'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "logs"))
not os.path.isdir(LOG_DIR) and os.mkdir(LOG_DIR, 0o0775)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s %(levelname)s %(name)s %(funcName)s "
                "[line:%(lineno)d] %(message)s"
            ),
        },
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": "True",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "omni_file": {
            "class": "common.loghandlers.DeferredRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filename": "/dev/null",
            "maxBytes": 50000000,  # 50 Meg bytes
            "backupCount": 5,
        },
        "api_file": {
            "class": "common.loghandlers.DeferredRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filename": "/dev/null",
            "maxBytes": 50000000,  # 50 Meg bytes
            "backupCount": 5,
        },
        "command_file": {
            "class": "common.loghandlers.DeferredRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filename": "/dev/null",
            "maxBytes": 50000000,  # 50 Meg bytes
            "backupCount": 5,
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "omni": {
            "handlers": (
                "omni_file",
                "mail_admins",
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "api": {
            "handlers": (
                "api_file",
                "mail_admins",
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "commands": {
            "handlers": (
                "command_file",
                "mail_admins",
            ),
            "level": "ERROR",
            "propagate": True,
        },
        "tests": {
            "handlers": (
                "omni_file",
                "mail_admins",
            ),
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

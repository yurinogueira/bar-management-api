"""
Django settings for HypeBack project.

Generated by "django-admin startproject" using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from datetime import timedelta
import os
from pathlib import Path
import sys
import urllib.parse

from django.core.management.utils import get_random_secret_key

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY = env.str("SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["0.0.0.0", "localhost"])
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://0.0.0.0:8000", "http://localhost:8000"],
)
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "content-disposition",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://0.0.0.0:8000", "http://localhost:8000"],
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "users",
    "companies",
    "core",
    "customers",
    "items",
    "members",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


# APLICATION SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
ROOT_URLCONF = "api.urls"
WSGI_APPLICATION = "api.wsgi.application"
WEATHERAPI_URL = env.str(
    "WEATHERAPI_URL", default="https://api.weatherapi.com/v1/current.json"
)
WEATHERAPI_KEY = env.str("WEATHERAPI_KEY", default="")

# DIRECTORY SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
STATIC_URL = urllib.parse.urljoin(env.str("STATIC_HOST", default=""), "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "api/static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_HOST = env.str("MEDIA_HOST", default="")
MEDIA_URL = env.str("MEDIA_URL", default="/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default="sqlite:///{}".format(os.path.join(BASE_DIR, "db.sqlite3")),
    ),
}

# Sessions
# ---------------------------------------------------------------------------------------------------------------------
# Cache to store session data if using the cache session backend.
SESSION_CACHE_ALIAS = "sessions"
# The module to store session data
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# A string like "example.com", or None for standard domain cookie.
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN", default=None)
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = not DEBUG


# CACHE
# ---------------------------------------------------------------------------------------------------------------------
CACHES = {
    "default": env.cache(
        "CACHES_DEFAULT_URL", default="locmemcache://unique-snowflake"
    ),
    "sessions": env.cache(
        "CACHES_SESSIONS_URL", default="locmemcache://unique-snowflake"
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "users.User"
USER_MODEL_NAME = "user"

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Django Rest Framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "PAGE_SIZE": 20,
    "DEFAULT_VERSION": env.str("RELEASE", "1.0.0"),
    "ALLOWED_VERSIONS": None,  # tuple
    "DATE_INPUT_FORMATS": [
        "%Y-%m-%dT%H:%M:%S.%f%z",  # '2006-10-25T14:30:59.000Z'
        "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
        "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
        "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
        "%Y-%m-%d",  # '2006-10-25'
        "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
        "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
        "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
        "%m/%d/%Y",  # '10/25/2006'
        "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
        "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
        "%m/%d/%y %H:%M",  # '10/25/06 14:30'
        "%m/%d/%y",  # '10/25/06'
    ],
    # Testing
    "TEST_REQUEST_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


# DRF Spectacular
# https://drf-spectacular.readthedocs.io/en/latest/
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Bar Management API",
    "DESCRIPTION": "Bar Management API Details",
    "VERSION": "1.0.0",
    "CAMELIZE_NAMES": True,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
}


# Django Rest Framework Simple JWT
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

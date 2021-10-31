"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default="default_secret_key_on_build").strip(
    '"'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default="0").strip('"')))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="").strip('"').split()


# Application definition

INSTALLED_APPS = [
    # Django Packages
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ThirdParty Packages
    "rest_framework",
    "dj_rest_auth",
    "django_filters",
    # Django Local Apps
    "users.apps.UsersConfig",
    "authentication.apps.AuthenticationConfig",
    "blog.apps.BlogConfig",
    # Local Packages
    "extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB_NAME", default="postgres").strip('"'),
        "USER": os.environ.get("POSTGRES_USER", default="postgres").strip('"'),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", default="postgres").strip('"'),
        "PORT": os.environ.get("POSTGRES_PORT", default="5432").strip('"'),
        "HOST": os.environ.get("POSTGRES_HOST", default="0.0.0.0").strip('"'),
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
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

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = "my-app-auth"
JWT_AUTH_REFRESH_COOKIE = "my-refresh-token"


OTP_EXPIRE = int(os.environ["OTP_EXPIRE"])  # per minutes

SMS = {
    "API-KEY": os.environ["SMS_API_KEY"],
    "OTP_LENGTH": os.environ["SMS_OTP_LENGTH"],
    "API_VERSION": os.environ["SMS_API_VERSION"],
    "API_HOST": os.environ["SMS_API_HOST"],
    "DEBUG_MODE": bool(int(os.environ.get("SMS_DEBUG_MODE", "0"))),
    "TEMPLATE": os.environ.get("SMS_TEMPLATE_NAME", ""),
}

AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ["ACCESS_TOKEN_LIFETIME"])),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ["REFRESH_TOKEN_LIFETIME"])),
}

PHONE_NUMBER_PATTERN = os.environ["PHONE_NUMBER_PATTERN"]
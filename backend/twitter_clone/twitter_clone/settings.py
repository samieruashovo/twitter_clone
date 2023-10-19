
from pathlib import Path
from datetime import timedelta

import dj_database_url
import environ
import os
env = environ.Env()
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z6xh*n0sk#n@756)d-8yreh9gqg5m$t^d^2rajw_c6u4vb-t+2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    "users",
    'tweets',
    'chat',
    'notifications',
    'community',
    'djoser',


    'cloudinary_storage',
    'cloudinary',
    'django_filters',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "twitter_clone.urls"

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

WSGI_APPLICATION = "twitter_clone.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "male_tweet.db.sqlite3",
    },
    "main_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "main_db.db.sqlite3",
    },
    "female_user_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "female_tweet.db.sqlite3",
    },
    "male_user_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR / "male_tweet.db.sqlite3",)
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = "/static/"

# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]
# MEDIA_URL = '/media/'

# MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'users.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('email')
EMAIL_HOST_PASSWORD = 'ilyvqakvwqmhhufn'

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    #   "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=4),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# DOMAIN = (env('domain'))
# SITE_NAME = ('Yes Twitter Clone')
# DJOSER CONFIG
DJOSER = {

    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "USERNAME_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",  # custom serializer
        "user": "users.serializers.UserCreateSerializer",
        "current_user": "djoser.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserSerializer",
    },
}

DATABASE_ROUTERS = [ "twitter_clone.routers.db_routers.TweetRouter"]
#  "twitter_clone.routers.db_routers.Default", , "twitter_clone.routers.db_routers.MainRouter"
# CORS_ALLOWED_ORIGINS = [

#     env('crossdomain')
#     # in dev mode
#     # "htpp://localhost:3000"
# ]
CORS_ALLOW_ALL_ORIGINS = True

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('cloud_name'),
    'API_KEY': env('api_key'),
    'API_SECRET': env('api_secret')
}
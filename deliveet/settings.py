"""
Django settings for deliveet project.
"""
import json
import os
from urllib.parse import urlparse

import dj_database_url
from decouple import config
from django.contrib import messages
from django.core.management.utils import get_random_secret_key
from django.template.context_processors import media
from environ import Env
from pathlib import Path

# Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Settings
env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# Secret Key
SECRET_KEY = env('DJANGO_SECRET_KEY', default=get_random_secret_key())

# Development mode
DEVELOPMENT_MODE = env.bool('DEVELOPMENT_MODE', default=False)

# Debug
DEBUG = env.bool('DJANGO_DEBUG', )

# Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'deliveet.live', 'deliveet-e6f379edca9d.herokuapp.com']

AUTH_USER_MODEL = 'accounts.UserAccount'

# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'theme.apps.ThemeConfig',
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'customers.apps.CustomersConfig',
    'courier.apps.CourierConfig',
    'finance.apps.FinanceConfig',
    'shipments.apps.ShipmentsConfig',
    'phonenumber_field',
    'widget_tweaks',
    'tailwind',
    'django_browser_reload',
    'channels',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# URL routes
ROOT_URLCONF = 'deliveet.urls'

# Templates
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
                'django.template.context_processors.media',
                'deliveet.utils.firebase_context_processor.firebase_config',
            ],
        },
    },
]

# WSGI/SERVER
WSGI_APPLICATION = 'deliveet.wsgi.application'

ASGI_APPLICATION = 'deliveet.asgi.application'

# Database
DATABASE_URL = env('DATABASE_URL', default=None)
if "DATABASE_URL" in os.environ:
    DATABASES = {
        'default': dj_database_url.config
        (default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': env('DATABASE_HOST', default='localhost'),
            'PORT': env('DATABASE_PORT', default='5432'),
        }
    }

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'theme/static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'theme')]

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ['127.0.0.1', 'localhost', ]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Message Notifications
MESSAGE_TAGS = {
    messages.DEBUG: 'amber',
    messages.INFO: 'blue',
    messages.SUCCESS: 'green',
    messages.WARNING: 'yellow',
    messages.ERROR: 'red',
}

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Wallet Settings
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')

# Phone Number Formats
PHONENUMBER_DEFAULT_REGION = 'NG'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

LOGIN_URL = 'accounts:signin'
LOGOUT_REDIRECT_URL = 'pages:app_home'

# Google Map
GOOGLE_MAP_API_KEY = env('GOOGLE_MAP_API_KEY')

# FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, "templates/snippets/delivit-1d2d5-firebase.json")

NOTIFICATION_URL = env('NOTIFICATION_URL', default='localhost:8000')

# Channels

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')]
        },
    },
}

FIREBASE_CONFIG = {
    'API_KEY': env('FIREBASE_API_KEY', default='None'),
    'AUTH_DOMAIN': env('FIREBASE_AUTH_DOMAIN', default='None'),
    'PROJECT_ID': env('FIREBASE_PROJECT_ID', default='None'),
    'STORAGE_BUCKET': env('FIREBASE_STORAGE_BUCKET', default='None'),
    'MESSAGING_SENDER_ID': env('FIREBASE_MESSAGING_SENDER_ID', default='None'),
    'APP_ID': env('FIREBASE_APP_ID', default='None'),
    'FIREBASE_TOKEN': env('FIREBASE_TOKEN', default='None'),
}

FIREBASE_SECRETS = {
    "type": config('FIREBASE_TYPE', default="service_account"),
    "project_id": config('FIREBASE_PROJECT_ID', default='None'),
    "private_key_id": config('FIREBASE_PRIVATE_KEY_ID', default='None'),
    "private_key": config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": config('FIREBASE_CLIENT_EMAIL', default='None'),
    "client_id": config('FIREBASE_CLIENT_ID', default='None'),
    "auth_uri": config('FIREBASE_AUTH_URI', default="https://accounts.google.com/o/oauth2/auth"),
    "token_uri": config('FIREBASE_TOKEN_URI', default="https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": config('FIREBASE_AUTH_PROVIDER_X509_CERT_URL', default="https://www.googleapis.com"
                                                                                          "/oauth2/v1/certs"),
    "client_x509_cert_url": config('FIREBASE_CLIENT_X509_CERT_URL', default='None'),
    "universe_domain": config('UNIVERSAL_DOMAIN', default='None')
}



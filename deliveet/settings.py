"""
Django settings for deliveet project.
"""
import os
from urllib.parse import urlparse

import dj_database_url
from django.contrib import messages
from django.core.management.utils import get_random_secret_key
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
            ],
        },
    },
]

# WSGI/SERVER
WSGI_APPLICATION = 'deliveet.wsgi.application'

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

# Email Setup
# EMAIL_BACKEND = 'django_ses.SESBackend'
# DEFAULT_FROM_EMAIL = env('AWS_SES_FROM_EMAIL')

# AWS_SES_ACCESS_KEY_ID = env('AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY = env('AWS_SES_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME')
# AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
# AWS_SES_FROM_EMAIL = env('AWS_SES_FROM_EMAIL')
# USE_SES_V2 = True

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

FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, "templates/snippets/firebase-messaging-sw.js")

"""
Django settings for deliveet project - Production Grade Delivery App
Upgraded to Django 5.2 with DRF, FastAPI, and production features
"""
import base64
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
import requests
from decouple import config
from django.contrib import messages
from django.core.management.utils import get_random_secret_key
from django.template.context_processors import media
from environ import Env

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
DEBUG = env.bool('DJANGO_DEBUG', default=DEVELOPMENT_MODE)

# Ensure ALLOWED_HOSTS is also set correctly
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '0.0.0.0', 'deliveet.live'])

AUTH_USER_MODEL = 'accounts.UserAccount'

# Application definition
INSTALLED_APPS = [
    # Daphne for ASGI
    'daphne',
    
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    
    # Project Apps
    'theme.apps.ThemeConfig',
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'customers.apps.CustomersConfig',
    'courier.apps.CourierConfig',
    'finance.apps.FinanceConfig',
    'shipments.apps.ShipmentsConfig',
    'pages.apps.PagesConfig',
    'profiles.apps.ProfilesConfig',
    'chat.apps.ChatConfig',
    'api.apps.ApiConfig',  # REST API
    'payments.apps.PaymentsConfig',  # Payment processing
    
    # Third-party packages
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'django_celery_beat',
    'django_celery_results',
    'django_extensions',
    'django_filters',
    'phonenumber_field',
    'widget_tweaks',
    'tailwind',
    'django_browser_reload',
    'channels',
    'storages',
    
    # Admin enhancements
    'django_admin_interface',
    'django_tables2',
    'import_export',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
                'deliveet.utils.remove_dark_classes.dark_mode_processor',
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
        'OPTIONS': {
            'min_length': 8,
        }
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
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'theme/static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ['127.0.0.1', 'localhost']

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

# ==========================================
# EMAIL CONFIGURATION
# ==========================================
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@deliveet.app')

# ==========================================
# PAYMENT INTEGRATION - MONNIFY
# ==========================================
MONNIFY_PUBLIC_KEY = env('MONNIFY_PUBLIC_KEY', default='')
MONNIFY_SECRET_KEY = env('MONNIFY_SECRET_KEY', default='')
MONNIFY_API_KEY = env('MONNIFY_API_KEY', default='')
MONNIFY_BASE_URL = env('MONNIFY_BASE_URL', default='https://api.monnify.com')
MONNIFY_CONTRACT_CODE = env('MONNIFY_CONTRACT_CODE', default='')

# Wallet Settings (Legacy Paystack)
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY', default='')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY', default='')

# Phone Number Formats
PHONENUMBER_DEFAULT_REGION = 'NG'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# Login/Logout URLs
LOGIN_URL = 'accounts:signin'
LOGOUT_REDIRECT_URL = 'pages:app_home'

# Google Map
GOOGLE_MAP_API_KEY = env('GOOGLE_MAP_API_KEY', default='')

NOTIFICATION_URL = env('NOTIFICATION_URL', default='localhost:8000')

# ==========================================
# DJANGO REST FRAMEWORK
# ==========================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'EXCEPTION_HANDLER': 'drf_standardized_errors.exception_handler.exception_handler',
}

# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JTI_CLAIM': 'jti',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'https://deliveet.live',
])

CORS_ALLOW_CREDENTIALS = True

# ==========================================
# CHANNELS CONFIGURATION
# ==========================================
ASGI_APPLICATION = 'deliveet.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [env('REDIS_URL', default='redis://localhost:6379')],
            'capacity': 1500,
            'expiry': 10,
        },
    },
}

# ==========================================
# CACHE CONFIGURATION
# ==========================================
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# ==========================================
# CELERY CONFIGURATION
# ==========================================
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=env('REDIS_URL', default='redis://localhost:6379'))
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=env('REDIS_URL', default='redis://localhost:6379'))
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# ==========================================
# AWS S3 STORAGE (Optional)
# ==========================================
USE_S3 = env.bool('USE_S3', default=False)

if USE_S3:
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_LOCATION = 'static'
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# ==========================================
# FIREBASE CONFIGURATION
# ==========================================
FIREBASE_CONFIG = {
    'API_KEY': env('FIREBASE_API_KEY', default='None'),
    'AUTH_DOMAIN': env('FIREBASE_AUTH_DOMAIN', default='None'),
    'PROJECT_ID': env('FIREBASE_PROJECT_ID', default='None'),
    'STORAGE_BUCKET': env('FIREBASE_STORAGE_BUCKET', default='None'),
    'MESSAGING_SENDER_ID': env('FIREBASE_MESSAGING_SENDER_ID', default='None'),
    'APP_ID': env('FIREBASE_APP_ID', default='None'),
    'FIREBASE_TOKEN': env('FIREBASE_TOKEN', default='None'),
}

FIREBASE_PRIVATE_KEY_BASE64 = config('FIREBASE_PRIVATE_KEY', default=None)

if FIREBASE_PRIVATE_KEY_BASE64:
    FIREBASE_PRIVATE_KEY = base64.b64decode(FIREBASE_PRIVATE_KEY_BASE64).decode('unicode_escape')
else:
    FIREBASE_PRIVATE_KEY = None

FIREBASE_SECRETS = {
    "type": config('FIREBASE_TYPE', default="service_account"),
    "project_id": config('FIREBASE_PROJECT_ID', default='None'),
    "private_key_id": config('FIREBASE_PRIVATE_KEY_ID', default='None'),
    "private_key": FIREBASE_PRIVATE_KEY,
    "client_email": config('FIREBASE_CLIENT_EMAIL', default='None'),
    "client_id": config('FIREBASE_CLIENT_ID', default='None'),
    "auth_uri": config('FIREBASE_AUTH_URI', default="https://accounts.google.com/o/oauth2/auth"),
    "token_uri": config('FIREBASE_TOKEN_URI', default="https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": config('FIREBASE_AUTH_PROVIDER_X509_CERT_URL', default="https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": config('FIREBASE_CLIENT_X509_CERT_URL', default='None'),
    "universe_domain": config('UNIVERSAL_DOMAIN', default='None')
}

# ==========================================
# SECURITY SETTINGS
# ==========================================
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=not DEBUG)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=not DEBUG)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 86400 * 7  # 7 days

# HTTPS & Security Headers
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "unpkg.com"),
    "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "fonts.googleapis.com"),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "fonts.gstatic.com"),
    "connect-src": ("'self'", "localhost:8000", "127.0.0.1:8000"),
}

X_FRAME_OPTIONS = 'DENY'

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    'https://deliveet.live',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
])

# ==========================================
# LOGGING & MONITORING
# ==========================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
    },
}

# Sentry Configuration (optional)
SENTRY_DSN = env('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=env('ENVIRONMENT', default='development'),
    )

# ==========================================
# BUSINESS LOGIC SETTINGS
# ==========================================
COURIER_EARN_PERCENTAGE = env('COURIER_EARN_PERCENTAGE', default='0.9')
DELIVERY_RADIUS_KM = env.float('DELIVERY_RADIUS_KM', default=50.0)
DEFAULT_DELIVERY_FEE = env.float('DEFAULT_DELIVERY_FEE', default=1000.0)
MIN_ORDER_VALUE = env.float('MIN_ORDER_VALUE', default=1000.0)
MAX_DELIVERY_TIME_HOURS = env.int('MAX_DELIVERY_TIME_HOURS', default=24)

# ==========================================
# ADMIN INTERFACE
# ==========================================
ADMIN_INTERFACE_THEME = 'modern'

# ==========================================
# DATABASE CONNECTION POOL (Production)
# ==========================================
if not DEBUG:
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
    }

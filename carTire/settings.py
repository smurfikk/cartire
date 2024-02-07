import logging
import os
import sys
from pathlib import Path
from os import environ

BASE_DIR = Path(__file__).resolve().parent.parent

if not environ.get('SECRET_KEY'):
    from dotenv import load_dotenv

    load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
logs_bot_token = environ.get('logs_bot_token')
logs_chat_id = int(environ.get('logs_chat_id'))

DEBUG = int(environ.get('DEBUG', default=0))

ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', "").split()

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'shop',
    'api',
    'corsheaders',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'carTire.urls'

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

WSGI_APPLICATION = 'carTire.wsgi.application'

DATABASES = {
    "default": {
        'ENGINE': "django.db.backends.mysql",
        'NAME': environ.get('MYSQL_DB'),
        'USER': environ.get('MYSQL_USER'),
        'PASSWORD': environ.get('MYSQL_PASSWORD'),
        'HOST': environ.get('MYSQL_HOST'),
        'PORT': environ.get('MYSQL_PORT'),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

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

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'logs/error.log'
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['console', 'file']
        }
    }
}

if DEBUG:
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = 'static/'

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = "/media/"
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = 'media/'

# if not DEBUG:
#     REST_FRAMEWORK = {
#         'DEFAULT_PERMISSION_CLASSES': [
#             'rest_framework.permissions.IsAuthenticated',
#         ],
#         'DEFAULT_AUTHENTICATION_CLASSES': [
#             'rest_framework.authentication.TokenAuthentication',
#         ],
#     }

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

logger = logging.getLogger("info_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/info.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY', 
    'django-insecure-4-(r41q64e-)#rk_urwj$4n+%59yunqsprx+j@49jikacbk(v)'
)

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = []

LOCAL_APPS = ['compliance_projects']

INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static-files/'

STATIC_ROOT = "/var/www/html/static-files/"

CELERY_BROKER_URL = "redis://backend_redis:6379"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================
# Logging
# =============================================================

if not os.path.exists(BASE_DIR / "logs"):
    os.mkdir(BASE_DIR / "logs")

LOG_FILE = BASE_DIR / "logs" / "debug.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}


# ========================================================
# Databases
# ========================================================


DB_NAME = os.environ["POSTGRES_DB"]

DB_USER = os.environ["POSTGRES_USER"]

DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]

DB_HOST = os.environ["DB_HOST"]

DB_PORT = os.environ["DB_PORT"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "PASSWORD": DB_PASSWORD,
    }        
}


# ========================================================
# MEDIA
# ========================================================


MEDIA_ROOT = BASE_DIR / ""

MEDIA_URL = "media/"

"""
Settings for Project
"""
import time
import os
import sys
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

IS_DEV = os.getenv("IS_DEV", "True").strip().lower() == "true"
IS_STAG = os.getenv("IS_STAG", "False").strip().lower() == "true"
IS_PROD = os.getenv("IS_PROD", "False").strip().lower() == "true"

DEBUG = IS_DEV or IS_STAG
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None

if IS_DEV:
    print("----- Running App in DEVELOPMENT Mode -----", file=sys.stderr)
    SECRET_KEY = "django-insecure-#=eo81$*nm53y&)i*64vbv(z2+y9_8%0_^2qgijv7*^s3&nl0^"
    ALLOWED_HOSTS = ["*"]
elif IS_STAG:
    print("----- Running App in STAGING Mode -----", file=sys.stderr)
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(" ")
else:
    print(
        f"----- Running App in PROD Mode at {time.time()} -----",
        file=sys.stderr,
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "").strip().lower()
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# Fetch CSRF_TRUSTED_ORIGINS from environment variables
env_origins = os.environ.get("CSRF_TRUSTED_ORIGINS")

if env_origins:
    CSRF_TRUSTED_ORIGINS = env_origins.split(",")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_numeric_filter",
    "compressor",
    "crispy_forms",
    "django_filters",
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "cropperjs",
    "corsheaders",
    "ui",
    "accounts",
    "main",
    "locations",
    "inventory",
    "providers",
    "charges",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.is_mobile_context",
                "core.context_processors.sbadmin2_sidebar_data",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
AUTH_USER_MODEL = "accounts.MyUser"
CRISPY_TEMPLATE_PACK = "bootstrap4"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
    "DATETIME_FORMAT": "iso-8601",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Urban Transit Facilities API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "CONTACT": {
        "url": "https://chartr.in",
        "name": "Chartr Mobility",
        "email": "contact@chartr.in",
    },
    "SERVERS": [
        {
            "url": "http://localhost:8000/",
            "description": "Localhost",
        },
        {
            "url": "https://dev-urban-transit-facilities-api.chartr.in/",
            "description": "Staging",
        },
        {
            "url": "https://urban-transit-facilities-api.chartr.in/",
            "description": "Production",
        },
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
    },
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",
    "SWAGGER_UI_FAVICON_HREF": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png",
    "CAMELIZE_NAMES": True,
}

PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "IN"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365) if IS_DEV else timedelta(days=30),
}

SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

if IS_DEV:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("DB_NAME", ""),
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASS", ""),
            "HOST": "localhost",
            "PORT": "",
        }
    }

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
# STATIC_URL = "https://cdn-001.chartr.in/urban-transit-facilities/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = "login_redirects"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

if not IS_PROD:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False

if IS_STAG or IS_PROD:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs", "django", "django.log"),
                "when": "D",  # this specifies the interval
                "interval": 1,  # defaults to 1, only necessary for other values
                "backupCount": 5,  # how many backup file to keep, 10 days
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }

ELK_SECRET_TOKEN = os.getenv("ELK_SECRET_TOKEN", "").strip()
ELK_SERVER_URL = os.getenv("ELK_SERVER_URL", "").strip().lower()
ELASTIC_APM_ENABLED = (
    os.getenv("ELASTIC_APM_ENABLED", "False").strip().lower() == "true"
)

if ELASTIC_APM_ENABLED:
    INSTALLED_APPS.append("elasticapm.contrib.django")

ELASTIC_APM = {
    "SERVICE_NAME": "urban-transit-facilities",
    "SERVER_URL": f"{ELK_SERVER_URL}",
    "SERVER_CERT": f"{BASE_DIR}/elk.chartr.in.crt",
    "SECRET_TOKEN": f"{ELK_SECRET_TOKEN}",
    "SERVER_TIMEOUT": "5s",
    "LOG_LEVEL": "critical",
    "CLOUD_PROVIDER": False,
    "DEBUG": DEBUG,
    "ELASTIC_APM_ENABLED": ELASTIC_APM_ENABLED,
}

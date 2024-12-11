import datetime
import os
from pathlib import Path

from config.env_reader import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = env.SECRET_KEY
DEBUG = False

ALLOWED_HOSTS = env.ALLOWED_HOSTS

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom apps
    # *your apps list here*
    # Packages
    "corsheaders",
    "drf_spectacular",
    "rest_framework",
    "storages",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    # example for using postgres
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": env.DB_NAME,
    #     "USER": env.DB_USER,
    #     "PASSWORD": env.DB_PASSWORD,
    #     "HOST": env.DB_HOST,
    #     "PORT": env.DB_PORT,
    # },
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": str(env.CACHE_DB),
    }
}

# Django has default user model, but you can create your own and override like this:
# AUTH_USER_MODEL = "<path-to-custom-model>"

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

# Rest framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 8,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "<Project-name> API",
    # more here: https://drf-spectacular.readthedocs.io/en/latest/settings.html
}

SIMPLE_JWT = {
    # Can be adjusted
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# S3
AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = env.AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
AWS_PRESIGNED_EXPIRY = env.AWS_PRESIGNED_EXPIRY
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": ""}
AWS_S3_REGION_NAME = env.AWS_S3_REGION_NAME

# Bucket URL or CloudFront distribution root URL
AWS_S3_CUSTOM_DOMAIN = env.AWS_S3_CUSTOM_DOMAIN
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_S3_ROOT_URL = env.AWS_S3_ROOT_URL

# s3 public media settings
PUBLIC_MEDIA_LOCATION = f"{AWS_S3_ROOT_URL}media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "util.s3.s3utils.PublicMediaStorage"

# s3 private media settings
PRIVATE_MEDIA_LOCATION = f"{AWS_S3_ROOT_URL}private"
PRIVATE_FILE_STORAGE = "util.s3.s3utils.PrivateMediaStorage"


# Static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True


# Environments
DEVELOPMENT = "development"
PRODUCTION = "production"
ENVIRONMENT = env.ENVIRONMENT


# Logging
LOGGING_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGGING_DIR, exist_ok=True)


# Utility to get rotating file handler
def get_rotating_file_handler(
    filename, level="DEBUG" if ENVIRONMENT == DEVELOPMENT else "ERROR"
):
    return {
        "level": level,  # Production should use INFO or higher
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(LOGGING_DIR, f"{filename}.log"),
        "maxBytes": 10485760,  # 10 MB
        "backupCount": 3,  # Keep last 3 log files
        "formatter": "simple",
    }


# Utility to configure app-specific loggers
def get_logger_desc(handler, level="DEBUG" if ENVIRONMENT == DEVELOPMENT else "ERROR"):
    return {
        "handlers": [handler],
        "level": level,
        "propagate": True,
    }


APP_LOGGERS = ("app",)  # Replace with actual app names

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"message": "%(message)s", "logger": "%(name)s"}',
        },
        "simple": {"format": "[{levelname}] {asctime}s - {message}", "style": "{"},
    },
    "handlers": {
        **{k: get_rotating_file_handler(k) for k in APP_LOGGERS},
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGGING_DIR, f"error.log"),
            "formatter": "simple",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        **{k: get_logger_desc(k) for k in APP_LOGGERS},
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True  # allow browser do CORS with credential
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = env.CSRF_TRUSTED_ORIGINS

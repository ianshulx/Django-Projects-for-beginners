import os
from .settings import *
from .settings import BASE_DIR

# Use a fallback secret key for development

# Define the hostname without a trailing slash
WEBSITE_DEFAULT_HOSTNAME = os.getenv("WEBSITE_DEFAULT_HOSTNAME")

ALLOWED_HOSTS = [WEBSITE_DEFAULT_HOSTNAME, "localhost"]

CSRF_TRUSTED_ORIGINS = ["https://" + WEBSITE_DEFAULT_HOSTNAME]

DEBUG = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# Stacti files work

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent


# Use WhiteNoise for static file management in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Define static files directory for `collectstatic`
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Ensure additional static directories (used during development)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Ensure this path exists
    os.path.join(BASE_DIR, "static/Routes"),
]


# Static files URL
STATIC_URL = "/static/"


# Media files (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")



database = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING' )


db = dict(item.split("=") for item in database.split(" "))

# Use environment variables for sensitive database credentials
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db["dbname"],
        "USER": db["user"],
        "PASSWORD": db["password"],
        "PORT": db["port"],
        "HOST": db["host"],
        "OPTIONS": {"sslmode": "require"},
    }
}



# Logging configuration (optional, helps in debugging production issues)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django_error.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

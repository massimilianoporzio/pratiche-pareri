import os

from dotenv import load_dotenv

from .common import *

load_dotenv()

DEBUG = os.getenv("DEBUG", "0") == "1"
print(f"DEBUG ORA VALE: {DEBUG}")
PRODUCTION = os.environ.get("PRODUCTION", "0") == "1"
SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret-key")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(" ")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pratiche_pareri",
        "USER": "pratiche_pareri",
        "PASSWORD": "massichiara07",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

LOGGING["formatters"]["colored"] = {
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
    "datefmt": "%d-%m-%Y %H:%M:%S",
}
LOGGING["loggers"]["pratiche"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["formatter"] = "colored"

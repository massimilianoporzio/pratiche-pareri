import os

from dotenv import load_dotenv

from .common import *

load_dotenv()

DEBUG = os.environ.get("DEBUG", "0") == "1"
PRODUCTION = os.environ.get("PRODUCTION", "0") == "1"
SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret-key")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(" ")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pratiche_pareri_prod",
        "USER": "pratiche",
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
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

JAZZMIN_SETTINGS["hide_apps"] = [
    "cities_light",
    "sites",
]

# 1. Aggiungere il nuovo handler 'file'
LOGGING["handlers"]["file"] = {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "formatter": "standard",
    "filename": "E:/prod/logs/pratiche_pareri/pratiche_pareri_log",
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
    "backupCount": 5,
}

# 2. Modificare il logger 'root' per usare l'handler 'file'
LOGGING["root"]["handlers"] = ["file"]

# 3. Aggiungere il logger vuoto per i messaggi non specifici
LOGGING["loggers"][""] = {
    "level": "INFO",
    "handlers": ["file"],
    "propagate": False,
}

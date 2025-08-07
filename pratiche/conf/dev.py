from . common import *

from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.environ.get("DEBUG", "0") == "1"
PRODUCTION = os.environ.get("PRODUCTION", "0") == "1"
SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret-key")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(" ")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pratiche',
        'USER': 'postgres',
        'PASSWORD': 'massichiara07',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
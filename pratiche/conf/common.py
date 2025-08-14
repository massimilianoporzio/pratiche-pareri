import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Application definition


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
]

THIRD_PARTY_APPS_BEFORE_DJANGO = [
    "jazzmin",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
    "cities_light",
]

APPS = ["users", "pareri", "datoriLavoro"]

# Impostazioni di django-cities-light
CITIES_LIGHT_TRANSLATION_LANGUAGES = ["it"]
CITIES_LIGHT_INCLUDE_COUNTRIES = ["IT"]
# CITIES_LIGHT_INCLUDE_CITY_TYPES = ["PPL", "PPLA", "PPLA2", "PPLA3", "PPLA4"]
CITIES_LIGHT_CITY_SOURCES = [
    "http://download.geonames.org/export/dump/cities500.zip",
    # Oppure, per una copertura ancora più ampia, usa cities500
    # 'http://download.geonames.org/export/dump/cities500.zip',
]
CITIES_LIGHT_ENABLE_GEOCODING = True

INSTALLED_APPS = THIRD_PARTY_APPS_BEFORE_DJANGO + DJANGO_APPS + THIRD_PARTY_APPS + APPS

SITE_ID = 1


JAZZMIN_SETTINGS = {
    # css per cambiare qualche elemento
    "custom_css": "css/admin.css",
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Pratiche & Pareri",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Pratiche & Pareri",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Pratiche & Pareri",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/icon.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "images/logo2.png",
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "images/logo2.png",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle  bg-transparent",
    # Welcome text on the login screen
    "welcome_sign": "Benvenuti su Pratiche&Pareri",
    # Copyright on the footer
    "copyright": "Massimiliano Porzio",
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    # abilita traduzione in jazzmin
    "i18n_enabled": True,
    # icons for apps:
    "icons": {
        "cities_light.cityProxy": "fas fa-city",
        "cities_light.countryProxy": "fas fa-earth-europe",
        "cities_light.regionProxy": "fas fa-map-marker-alt",
        "pareri.tipoOrigine": "fas fa-building-columns",
        "pareri.espertoRadioprotezione": "fas fa-radiation",
        "pareri.tipoPratica": "fas fa-file-invoice",
        "pareri.tipoProcesso": "fas fa-gear",
        "users.customuser": "fas fa-user",
        "auth.Group": "fas fa-users",
        "datoriLavoro.sede": "fas fa-location-dot",
        "datoriLavoro.datoreLavoro": "fas fa-user-tie",
    },
    # "usermenu_links": [
    #     {"name": "Logout", "url": "/admin/logout/", "icon": "fas fa-power-off"},
    # ],
    # Aggiungi questa linea per disabilitare il link di logout predefinito
    "show_logout": False,
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-pink",
    # "accent": "accent-pink",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-maroon",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Assicurati che sia qui
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "crum.CurrentRequestUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

ROOT_URLCONF = "pratiche.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pratiche.context_processors.project_context",  # Aggiungi il tuo context processor qui
            ],
        },
    },
]

WSGI_APPLICATION = "pratiche.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "it"

TIME_ZONE = "Europe/Rome"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("it", "Italiano"),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Aggiungi questa riga per dire a Django dove cercare i tuoi file statici personalizzati
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Il percorso dove Django raccoglierà tutti i file statici in produzione
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s -%(name)s -  - %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    "loggers": {
        logger_name: {
            "level": "WARNING",
            "propagate": True,
        }
        for logger_name in (
            "django",
            "django.request",
            "django.db.backends",
            "django.template",
            "django.security",
            "pratiche",
            "users",
        )
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

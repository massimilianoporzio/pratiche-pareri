# import logging

import logging

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from pratiche.admin import custom_admin_site

if settings.PRODUCTION:
    # test the logger
    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path(
        "",
        RedirectView.as_view(url="admin/login/", permanent=False),
        name="home",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]


if not settings.PRODUCTION:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

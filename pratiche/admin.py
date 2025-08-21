# tuo_progetto/admin.py
from django.contrib import admin
from django.contrib.admin.templatetags.admin_modify import (
    register as admin_modify,
    submit_row,
)
from django.contrib.admin.templatetags.base import InclusionAdminNode

from users.forms import CustomAuthenticationForm

# Nome del gruppo che avrà accesso completo
FULL_ACCESS_GROUP_NAME = "Full Access Admin"


# Definisci la lista delle app autorizzate per gli altri superuser
AUTHORIZED_APPS = [
    "pareri",
    # Aggiungi qui gli 'app_label' delle app che vuoi mostrare
]


class CustomAdminSite(admin.AdminSite):
    login_form = CustomAuthenticationForm

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Controlla se l'utente appartiene al gruppo "Full Access Admin"
        user_has_full_access_group = (
            request.user.is_superuser
            and request.user.groups.filter(name=FULL_ACCESS_GROUP_NAME).exists()
        )

        if user_has_full_access_group:
            return app_list
        else:
            return [app for app in app_list if app["app_label"] in AUTHORIZED_APPS]


# Crea un'istanza dell'AdminSite personalizzato
custom_admin_site = CustomAdminSite(name="custom_admin")


def custom_submit_row(context):
    """
    Display the row of buttons for delete and save.
    """
    ctx = submit_row(context)
    ctx.update({"show_close": True})
    return ctx


@admin_modify.tag(name="submit_row")
def submit_row_tag(parser, token):
    return InclusionAdminNode(
        parser, token, func=custom_submit_row, template_name="submit_line.html"
    )


class ActiveModelAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)

    def changelist_view(self, request, extra_context=None):
        if "is_active__exact" not in request.GET:
            q = request.GET.copy()
            q["is_active__exact"] = "1"
            request.GET = q
            request.META["QUERY_STRING"] = request.GET.urlencode()
        return super().changelist_view(request, extra_context=extra_context)

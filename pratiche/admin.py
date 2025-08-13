# tuo_progetto/admin.py
from django.contrib import admin
from django.contrib.admin.templatetags.admin_modify import (
    register as admin_modify,
    submit_row,
)
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from pareri.models import TipoOrigine
from users.models import CustomUser

# Nome del gruppo che avrà accesso completo
FULL_ACCESS_GROUP_NAME = "Full Access Admin"


# Definisci la lista delle app autorizzate per gli altri superuser
AUTHORIZED_APPS = [
    "pareri",
    # Aggiungi qui gli 'app_label' delle app che vuoi mostrare
]


class CustomAdminSite(admin.AdminSite):
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


# Annulla la registrazione del modello  Group dall'admin di default
admin.site.unregister(Group)


@admin.register(Group, site=custom_admin_site)
class CustomGroupAdmin(admin.ModelAdmin):
    pass  # Lascia vuoto per usare la configurazione di default


# Per personalizzare l'admin del tuo CustomUser, puoi estendere UserAdmin
@admin.register(CustomUser, site=custom_admin_site)
class CustomUserAdmin(UserAdmin):
    # I campi da visualizzare nella lista degli utenti nell'admin
    list_display = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "is_staff",
        "is_active",
    )
    # I campi da usare per la ricerca
    search_fields = ("email", "first_name", "last_name")
    # I filtri laterali
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "gender")

    # Ridefinisci fieldsets usando la funzione di traduzione
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "gender")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Ridefinisci add_fieldsets usando la funzione di traduzione
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "gender",
                    "is_staff",
                    "is_active",
                    "groups",
                ),
            },
        ),
    )

    def changeform_view(self, request, object_id=..., form_url=..., extra_context=...):
        extra_context = extra_context or {}
        extra_context["show_close"] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

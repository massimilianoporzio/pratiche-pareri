# tuo_progetto/admin.py
from cities_light.models import City, Country, Region
from django.contrib import admin
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


# Crea le classi ModelAdmin per i modelli di cities_light
# Puoi personalizzare le liste di visualizzazione e i filtri qui
@admin.register(City, site=custom_admin_site)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "region")
    list_filter = ("country", "region")
    search_fields = ("name",)


@admin.register(Region, site=custom_admin_site)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(Country, site=custom_admin_site)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code2")
    search_fields = ("name", "code2")


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


@admin.register(TipoOrigine, site=custom_admin_site)
class TipoOrigineAdmin(admin.ModelAdmin):
    fields = ("nome",)

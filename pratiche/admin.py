# tuo_progetto/admin.py
from cities_light.models import City, Country, Region
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import CustomUser

# Specifica qui l'username del superuser che deve avere accesso completo
FULL_ACCESS_SUPERUSER_USERNAME = "massimiliano.porzio"

# Definisci la lista delle app autorizzate per gli altri superuser
AUTHORIZED_APPS = [
    "auth",
    # Aggiungi qui gli 'app_label' delle app che vuoi mostrare
]


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Se l'utente non è un superuser o ha l'username con accesso completo,
        # restituisci la lista completa delle app
        if (
            not request.user.is_superuser
            or request.user.username == FULL_ACCESS_SUPERUSER_USERNAME
        ):
            return app_list
        else:
            # Altrimenti, filtra la lista per mostrare solo le app autorizzate
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

    # Aggiungi il campo 'gender' ai fieldsets per la modifica/visualizzazione
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("gender",)}),)
    # Aggiungi il campo 'gender' ai add_fieldsets per la creazione di nuovi utenti
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("gender",)}),)

    def changeform_view(self, request, object_id=..., form_url=..., extra_context=...):
        extra_context = extra_context or {}
        extra_context["show_close"] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

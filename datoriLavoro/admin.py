from django.contrib import admin

from datoriLavoro.forms import DatoreLavoroForm
from pratiche.admin import ActiveModelAdminMixin, custom_admin_site

from .models import CityProxy, CountryProxy, DatoreLavoro, RegionProxy, Sede


@admin.register(CityProxy, site=custom_admin_site)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "region")
    list_filter = ("country", "region")
    search_fields = ("name",)


@admin.register(RegionProxy, site=custom_admin_site)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    search_fields = ("name",)

    class Meta:
        verbose_name_plural = "Regioni/Stati"


@admin.register(CountryProxy, site=custom_admin_site)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code2")
    search_fields = ("name", "code2")


# Register your models here.
@admin.register(Sede, site=custom_admin_site)
class SedeAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    list_display = ("nome", "indirizzo", "citta")
    fields = ("nome", "indirizzo", "citta", "is_active")
    search_fields = ("nome", "indirizzo", "citta")
    list_filter = ("is_active",)


@admin.register(DatoreLavoro, site=custom_admin_site)
class DatoreLavoroAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    form = DatoreLavoroForm  # Associa la form qui
    list_display = ("ragione_sociale", "p_iva", "codice_fiscale")
    fields = ("ragione_sociale", "p_iva", "codice_fiscale", "sedi", "is_active")
    search_fields = ("ragione_sociale", "p_iva", "codice_fiscale", "sedi__nome")
    list_filter = ("is_active",)

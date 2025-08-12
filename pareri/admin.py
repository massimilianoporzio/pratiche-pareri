from django.contrib import admin

from pareri.models import EspertoRadioprotezione, TipoPratica, TipoProcesso
from pratiche.admin import custom_admin_site


@admin.register(TipoProcesso, site=custom_admin_site)
class TipoProcessoAdmin(admin.ModelAdmin):
    fields = ("nome", "descrizione")
    list_display = ("nome", "descrizione")


@admin.register(EspertoRadioprotezione, site=custom_admin_site)
class EspertoRadioprotezioneAdmin(admin.ModelAdmin):
    fields = ("numero_iscrizione", "full_name")
    list_display = ("numero_iscrizione", "full_name")
    search_fields = ("numero_iscrizione", "full_name")


@admin.register(TipoPratica, site=custom_admin_site)
class TipoPraticaAdmin(admin.ModelAdmin):
    fields = ("nome", "descrizione")
    list_display = ("nome", "descrizione")

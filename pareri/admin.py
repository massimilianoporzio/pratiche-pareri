from django.contrib import admin

from pareri.models import EspertoRadioprotezione, TipoOrigine, TipoPratica, TipoProcesso
from pratiche.admin import ActiveModelAdminMixin, custom_admin_site


@admin.register(TipoProcesso, site=custom_admin_site)
class TipoProcessoAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    list_filter = ("is_active",)
    fields = ("nome", "descrizione", "is_active")
    list_display = ("nome", "descrizione")


@admin.register(EspertoRadioprotezione, site=custom_admin_site)
class EspertoRadioprotezioneAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    list_filter = ("is_active",)
    fields = ("numero_iscrizione", "full_name", "is_active")
    list_display = ("numero_iscrizione", "full_name")
    search_fields = ("numero_iscrizione", "full_name")


@admin.register(TipoPratica, site=custom_admin_site)
class TipoPraticaAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    list_filter = ("is_active",)
    fields = ("nome", "descrizione", "is_active")
    list_display = (
        "nome",
        "descrizione",
    )


@admin.register(TipoOrigine, site=custom_admin_site)
class TipoOrigineAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    list_filter = ("is_active",)
    fields = ("nome", " is_active")

from django.contrib import admin

from pareri.models import TipoProcesso
from pratiche.admin import custom_admin_site


@admin.register(TipoProcesso, site=custom_admin_site)
class TipoProcessoAdmin(admin.ModelAdmin):
    fields = ("nome", "descrizione")
    list_display = ("nome", "descrizione")

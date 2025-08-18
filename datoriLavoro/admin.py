# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from pratiche.admin import ActiveModelAdminMixin, custom_admin_site

from .models import (
    CityProxy,
    CountryProxy,
    DatoreLavoro,
    DatoreLavoroSede,
    RegionProxy,
    Sede,
)


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


class DatoreLavoroSedeInlineFormset(forms.BaseInlineFormSet):
    # Ripristina la versione più semplice e sicura
    def clean(self):
        super().clean()

        legal_office_count = 0

        for form in self.forms:
            if not form.cleaned_data.get("DELETE", False):
                if form.cleaned_data.get("is_sede_legale", False):
                    legal_office_count += 1

        if legal_office_count == 0:
            raise ValidationError(
                "Ogni datore di lavoro deve avere almeno una sede legale."
            )

        if legal_office_count > 1:
            raise ValidationError("Un datore di lavoro può avere solo una sede legale.")


class DatoreLavoroSedeInlineForm(forms.ModelForm):
    class Meta:
        model = DatoreLavoroSede
        fields = ("sede", "is_sede_legale")


class DatoreLavoroSedeInline(admin.TabularInline):
    model = DatoreLavoroSede
    formset = DatoreLavoroSedeInlineFormset

    extra = 0
    verbose_name = "Sede associata"
    verbose_name_plural = "Sedi associate"


class DatoreLavoroAdminForm(forms.ModelForm):
    class Meta:
        model = DatoreLavoro
        fields = ("ragione_sociale", "p_iva", "codice_fiscale", "is_active")


@admin.register(DatoreLavoro, site=custom_admin_site)
class DatoreLavoroAdmin(admin.ModelAdmin, ActiveModelAdminMixin):
    form = DatoreLavoroAdminForm  # Associa la form qui
    inlines = [DatoreLavoroSedeInline]
    list_display = ("ragione_sociale", "p_iva", "codice_fiscale")
    fields = ("ragione_sociale", "p_iva", "codice_fiscale", "is_active")
    search_fields = ("ragione_sociale", "p_iva", "codice_fiscale", "sedi__nome")
    list_filter = ("is_active",)

    def get_inline_instances(self, request, obj=None):
        """
        Controlla se ci sono già sedi associate e imposta extra = 0.
        Se non ci sono sedi, imposta extra = 1 per forzare la visualizzazione della riga.
        """
        inlines = super().get_inline_instances(request, obj)
        for inline in inlines:
            if isinstance(inline, DatoreLavoroSedeInline):
                # Se l'oggetto esiste e ha già delle sedi associate, non mostrare la riga extra
                if obj and obj.datorelavorosede_set.exists():
                    inline.extra = 0
                # Se l'oggetto è nuovo (obj è None) o non ha sedi, mostrare 1 riga extra
                else:
                    inline.extra = 1
        return inlines

    def save_model(self, request, obj, form, change):
        # Assicurati che l'istanza principale sia salvata prima
        # di salvare le relazioni.
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # A differenza della versione precedente, qui salviamo
        # prima il formset, poi recuperiamo i dati per l'aggiornamento.

        # 1. Salva i formset in linea
        super().save_related(request, form, formsets, change)

        # 2. Esegui la logica di business dopo il salvataggio
        datore_lavoro = form.instance
        legal_sede_pk = None

        # Trova la PK della sede legale che l'utente ha selezionato.
        # Poiché i formset sono già stati salvati,
        # possiamo interrogare il database.
        try:
            legal_sede = datore_lavoro.datorelavorosede_set.get(is_sede_legale=True)
            legal_sede_pk = legal_sede.pk
        except DatoreLavoroSede.DoesNotExist:
            legal_sede_pk = None
        except DatoreLavoroSede.MultipleObjectsReturned:
            # Gestisce il caso di errore in cui la validazione lato client fallisce.
            # Rimuove tutti i flag tranne il primo (o un altro a tua scelta).
            legal_sedes = datore_lavoro.datorelavorosede_set.filter(is_sede_legale=True)
            if legal_sedes.exists():
                legal_sede_pk = legal_sedes.first().pk
                legal_sedes.exclude(pk=legal_sede_pk).update(is_sede_legale=False)

        # Se è stata trovata una sede legale, aggiorna tutte le altre.
        if legal_sede_pk:
            datore_lavoro.datorelavorosede_set.all().exclude(pk=legal_sede_pk).update(
                is_sede_legale=False
            )


class SedeAdminForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Controlla se il form è stato aperto in una finestra pop-up
        # (ovvero, se l'URL contiene il parametro `_popup=1`)
        if self.request and self.request.GET.get("_popup"):
            # Se siamo nel form di creazione di una Sede tramite pop-up,
            # controlliamo le condizioni per spuntare 'is_sede_legale'.
            # L'assunto è che il pop-up dal DatoreLavoro indichi una nuova sede
            # che deve essere legale.
            # Questo è un'euristica, non un controllo a livello di database.
            self.initial["is_sede_legale"] = True


@admin.register(Sede, site=custom_admin_site)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("nome", "indirizzo", "citta")
    list_filter = ["citta"]
    search_fields = ("nome", "indirizzo", "citta__name")
    fields = ("nome", "indirizzo", "citta")

    def response_add(self, request, obj, post_url_continue=None):
        msg = _("La %(name)s '%(obj)s' è stata creata con successo.") % {
            "name": self.opts.verbose_name,
            "obj": obj,
        }
        self.message_user(request, msg, level=messages.SUCCESS)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        msg = _("La %(name)s '%(obj)s' è stata modificata con successo.") % {
            "name": self.opts.verbose_name,
            "obj": obj,
        }
        self.message_user(request, msg, level=messages.SUCCESS)
        return super().response_change(request, obj)

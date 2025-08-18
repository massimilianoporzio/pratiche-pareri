# -*- coding: utf-8 -*-
import logging

import codicefiscale as cf
from cities_light.models import City, Country, Region
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from verify_vat_number.vies import get_from_eu_vies

from utils.model import Model as MyModel

# Crea le classi ModelAdmin per i modelli di cities_light

logger = logging.getLogger(__name__)


class CityProxy(City):
    class Meta:
        proxy = True
        verbose_name = "Città"
        verbose_name_plural = "Città"
        app_label = "cities_light"


class RegionProxy(Region):
    class Meta:
        proxy = True
        verbose_name = "Regione/Stato"
        verbose_name_plural = "Regioni/Stati"
        app_label = "cities_light"


class CountryProxy(Country):
    class Meta:
        proxy = True
        verbose_name = "Nazione"
        verbose_name_plural = "Nazioni"
        app_label = "cities_light"


# Create your models here.
class Sede(MyModel):
    nome = models.CharField(max_length=100, blank=False, default="---")
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    citta = models.ForeignKey(
        CityProxy,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_("Città"),
    )

    def __str__(self):
        result = self.nome if self.nome else "Anonima"
        return result + " - " + str(self.citta)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedi"


def validate_p_iva_italiana(value):

    try:
        data = get_from_eu_vies("IT" + value)
        logger.info("P IVA VALIDA? %s", data)

    except Exception:

        raise ValidationError(
            _("%(value)s non è una Partita IVA italiana valida."),
            params={"value": value},
        )


def validate_codice_fiscale(value):
    if not cf.isvalid(value):
        raise ValidationError(
            _("%(value)s non è un Codice Fiscale valido."),
            params={"value": value},
        )


class DatoreLavoro(MyModel):
    ragione_sociale = models.CharField(
        max_length=255,
        verbose_name=_("Ragione Sociale"),
        blank=True,
    )
    p_iva = models.CharField(
        max_length=11,
        verbose_name=_("Partita IVA"),
        blank=True,
        validators=[validate_p_iva_italiana],
    )
    codice_fiscale = models.CharField(
        max_length=16,
        verbose_name=_("Codice Fiscale"),
        blank=True,
        validators=[validate_codice_fiscale],
    )
    # La relazione M2M passa per il modello intermedio
    sedi = models.ManyToManyField(
        Sede,
        through="DatoreLavoroSede",
        related_name="datori_lavoro",
        verbose_name=_("Sedi"),
    )

    def __str__(self):
        return self.ragione_sociale or self.p_iva or self.codice_fiscale

    class Meta:
        verbose_name = "Datore di Lavoro"
        verbose_name_plural = "Datori di Lavoro"

    def save(self, *args, **kwargs):
        # Assicurati che il codice fiscale sia sempre in maiuscolo
        if self.codice_fiscale:
            self.codice_fiscale = self.codice_fiscale.upper()
        super().save(*args, **kwargs)


class DatoreLavoroSede(models.Model):
    datore_lavoro = models.ForeignKey(
        DatoreLavoro, on_delete=models.CASCADE, blank=True, null=True
    )
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    is_sede_legale = models.BooleanField(default=False, verbose_name=_("Sede Legale?"))

    class Meta:
        # Vincolo per garantire che una Sede possa essere "sede legale"
        # solo per un Datore di Lavoro.
        constraints = [
            UniqueConstraint(
                fields=["sede", "is_sede_legale"],
                name="unique_legal_office_for_each_sede",
                condition=Q(is_sede_legale=True),
            )
        ]
        unique_together = (
            "datore_lavoro",
            "sede",
        )  # vincolo per dire che la stessa sede non può essere associata due volte allo stesso datore di lavoro
        verbose_name = "Sede associata"
        verbose_name_plural = "Sedi asscociate"

    def clean(self):
        # Impedisce di impostare is_sede_legale a True se la sede
        # è già sede legale per un altro datore di lavoro.
        if self.is_sede_legale:
            qs = DatoreLavoroSede.objects.filter(sede=self.sede, is_sede_legale=True)
            # Se stiamo modificando un'associazione esistente, escludiamola.
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError(
                    "Questa sede è già impostata come sede legale per un altro datore di lavoro."
                )

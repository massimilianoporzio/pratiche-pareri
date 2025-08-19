# core/management/commands/dump_static.py

import argparse  # Aggiungi questo import
import json
import os
from datetime import datetime

from cities_light.models import City, Country, Region, SubRegion
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.utils import timezone  # Aggiungi questo import per gestire i fusi orari


class Command(BaseCommand):
    help = "Esegue un dump completo dei dati statici."

    def add_arguments(self, parser):
        parser.add_argument(
            "timestamp", type=str, help="Timestamp da usare per la cartella di output."
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Avvio del dump completo dei dati statici...")
        )

        timestamp_str = options["timestamp"]
        output_dir = os.path.join(settings.BASE_DIR, "fixtures", timestamp_str)
        os.makedirs(output_dir, exist_ok=True)

        models_to_dump = [
            Country,
            Region,
            SubRegion,
            City,
        ]

        for model in models_to_dump:
            data_to_dump = list(model.objects.all())
            output_file_name = os.path.join(
                output_dir, f"dump_{model.__name__.lower()}_{timestamp_str}.json"
            )
            serialized_data = serialize(
                "json", data_to_dump, indent=2, use_natural_foreign_keys=True
            )
            with open(output_file_name, "w", encoding="utf-8") as out:
                out.write(serialized_data)
            self.stdout.write(
                self.style.SUCCESS(f"Dump completato per {model.__name__}.")
            )

# core/management/commands/dump_incrementale.py

import argparse  # Aggiungi questo import
import json
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.db.models import QuerySet
from django.db.utils import ProgrammingError
from django.utils import timezone  # Aggiungi questo import per gestire i fusi orari

from datoriLavoro.models import DatoreLavoro, DatoreLavoroSede, Sede
from users.models import CustomUser

LAST_DUMP_FILE = "last_dump_time.json"


class Command(BaseCommand):
    help = "Esegue un dump incrementale dei dati modificati dall'ultima esecuzione."

    def add_arguments(self, parser):
        parser.add_argument(
            "timestamp", type=str, help="Timestamp da usare per la cartella di output."
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Avvio del dump incrementale..."))

        last_dump_time = None
        if os.path.exists(LAST_DUMP_FILE):
            with open(LAST_DUMP_FILE, "r") as f:
                data = json.load(f)
                last_dump_time_str = data.get("last_dump_time")
                if last_dump_time_str:
                    last_dump_time = datetime.fromisoformat(last_dump_time_str)
        else:
            self.stdout.write(
                self.style.WARNING(
                    "File di tracciamento non trovato. Eseguo un dump completo."
                )
            )
            last_dump_time = datetime.min

        timestamp_str = options["timestamp"]
        current_time = timezone.now()

        output_dir = os.path.join(settings.BASE_DIR, "fixtures", timestamp_str)
        os.makedirs(output_dir, exist_ok=True)

        models_to_dump = [
            DatoreLavoro,
            Sede,
            DatoreLavoroSede,
            CustomUser,
        ]

        for model in models_to_dump:
            data_to_dump = list(model.objects.filter(updated_at__gt=last_dump_time))
            output_file_name = os.path.join(
                output_dir,
                f"incremental_dump_{model.__name__.lower()}_{timestamp_str}.json",
            )
            serialized_data = serialize(
                "json", data_to_dump, indent=2, use_natural_foreign_keys=True
            )
            with open(output_file_name, "w", encoding="utf-8") as out:
                out.write(serialized_data)
            self.stdout.write(
                self.style.SUCCESS(f"Dump completato per {model.__name__}.")
            )

        # Aggiorna il file di tracciamento
        with open(LAST_DUMP_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_dump_time": current_time.isoformat()}, f)

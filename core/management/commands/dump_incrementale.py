import json
import os
from datetime import datetime

from cities_light.models import City, Country, Region
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.db.models import QuerySet
from django.db.utils import ProgrammingError

# NOTA: Non importare le classi Proxy dal tuo file DatoriLavoro.models
from datoriLavoro.models import DatoreLavoro, DatoreLavoroSede, Sede

# Il file per tracciare l'ultima data di dump
LAST_DUMP_FILE = "last_dump_time.json"


class Command(BaseCommand):
    help = "Esegue un dump incrementale dei dati modificati dall'ultima esecuzione."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Avvio del dump incrementale..."))

        # 1. Carica l'ultima data di dump
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
                    "File di tracciamento non trovato. Eseguo un dump completo per i modelli senza timestamp."
                )
            )
            last_dump_time = datetime.min

        current_time = datetime.now()

        # 2. Definisci tutti i modelli da esportare
        models_to_dump = [
            DatoreLavoro,
            DatoreLavoroSede,
            Sede,
            City,
            Region,
            Country,
        ]

        all_data = []
        for model in models_to_dump:
            self.stdout.write(f"Eseguo il dump per il modello: {model.__name__}")
            try:
                # 3. Controlla se il modello ha i campi di data
                if hasattr(model, "updated_at") or hasattr(model, "created_at"):
                    # Logica per i modelli con timestamp
                    modified_data = QuerySet(model).all()
                    if hasattr(model, "updated_at"):
                        modified_data = modified_data.filter(
                            updated_at__gte=last_dump_time
                        )
                    if hasattr(model, "created_at"):
                        # Aggiungi i nuovi record creati
                        modified_data = modified_data | model.objects.filter(
                            created_at__gte=last_dump_time
                        )

                    if modified_data.exists():
                        all_data.extend(list(modified_data.distinct()))
                        self.stdout.write(
                            f"Trovati {modified_data.distinct().count()} record modificati per {model.__name__}."
                        )
                else:
                    # Logica per i modelli senza timestamp (come quelli di cities_light)
                    self.stdout.write(
                        self.style.WARNING(
                            f"Il modello {model.__name__} non ha i campi di data. Eseguo un dump completo."
                        )
                    )
                    all_data.extend(list(model.objects.all()))
            except ProgrammingError:
                self.stdout.write(
                    self.style.ERROR(
                        f"Errore nel recupero dei dati per {model.__name__}. Potrebbe non esistere la tabella."
                    )
                )
                continue

        if not all_data:
            self.stdout.write(self.style.SUCCESS("Nessun nuovo dato da esportare."))
            return

        # 4. Serializza i dati e salva il file
        output_file_name = (
            f'incremental_dump_{current_time.strftime("%Y-%m-%d_%H%M%S")}.json'
        )
        try:
            serialized_data = serialize(
                "json", all_data, indent=2, use_natural_foreign_keys=True
            )
            with open(output_file_name, "w") as out:
                out.write(serialized_data)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Errore nella serializzazione: {e}"))
            return

        self.stdout.write(
            self.style.SUCCESS(f"Dump completato. File: {output_file_name}")
        )

        # 5. Aggiorna il file di tracciamento
        with open(LAST_DUMP_FILE, "w") as f:
            json.dump({"last_dump_time": current_time.isoformat()}, f)

        self.stdout.write(self.style.SUCCESS("Data dell'ultimo dump aggiornata."))

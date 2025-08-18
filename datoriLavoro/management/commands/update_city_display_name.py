from cities_light.models import City
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Updates the display_name of cities based on updated region names."

    def handle(self, *args, **options):
        self.stdout.write("Updating city display names...")
        cities = City.objects.all()
        total_cities = cities.count()

        for i, city in enumerate(cities):
            # Ricostruisci il display_name in base alle tue preferenze
            # Assicurati che il tuo campo 'region' sia chiamato in modo appropriato
            city.display_name = f"{city.name}, {city.region.name}, {city.country.name}"
            city.save()

            # Feedback per l'utente
            if (i + 1) % 100 == 0 or (i + 1) == total_cities:
                self.stdout.write(f"Updated {i + 1} of {total_cities} cities.")

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all city display names.")
        )

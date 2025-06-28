from django.core.management.base import BaseCommand
from api.models import LevelTitle
import os
import json

class Command(BaseCommand):
    help = "Carga los títulos de nivel desde el JSON a la base de datos"

    def handle(self, *args, **kwargs):
        fixture_path = os.path.join(os.path.dirname(__file__), "../../fixtures/level_titles.json")
        fixture_path = os.path.abspath(fixture_path)
        with open(fixture_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                LevelTitle.objects.update_or_create(
                    level=item["level"],
                    defaults={"title": item["title"]}
                )
        self.stdout.write(self.style.SUCCESS("Títulos de nivel cargados correctamente."))

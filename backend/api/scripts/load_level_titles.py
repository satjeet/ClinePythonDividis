import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dividis.settings")
django.setup()

from api.models import LevelTitle

def load_titles():
    fixture_path = os.path.join(os.path.dirname(__file__), "../fixtures/level_titles.json")
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            LevelTitle.objects.update_or_create(
                level=item["level"],
                defaults={"title": item["title"]}
            )
    print("Títulos de nivel cargados correctamente.")

if __name__ == "__main__":
    load_titles()

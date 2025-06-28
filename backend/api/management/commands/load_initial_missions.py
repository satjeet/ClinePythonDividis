from django.core.management.base import BaseCommand
from django.core.management import call_command
from api.models import Mission

class Command(BaseCommand):
    help = "Carga las misiones iniciales desde el fixture solo si no existen"

    def handle(self, *args, **options):
        try:
            if Mission.objects.exists():
                self.stdout.write(self.style.WARNING("Misiones iniciales ya existen. No se cargan duplicados."))
            else:
                self.stdout.write(self.style.NOTICE("Cargando misiones iniciales desde el fixture..."))
                call_command('loaddata', 'api/fixtures/initial_missions.json')
                if Mission.objects.exists():
                    self.stdout.write(self.style.SUCCESS("Misiones iniciales cargadas correctamente."))
                else:
                    self.stdout.write(self.style.ERROR("No se cargaron misiones. Revisa el fixture y los módulos referenciados."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falló la carga de misiones: {e}"))
            raise

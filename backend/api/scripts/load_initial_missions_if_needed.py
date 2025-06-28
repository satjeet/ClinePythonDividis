from django.core.management import call_command
from api.models import Mission

def run():
    try:
        if Mission.objects.exists():
            print("[INFO] Misiones iniciales ya existen. No se cargan duplicados.")
        else:
            print("[INFO] Cargando misiones iniciales desde el fixture...")
            call_command('loaddata', 'api/fixtures/initial_missions.json')
            if Mission.objects.exists():
                print("[SUCCESS] Misiones iniciales cargadas correctamente.")
            else:
                print("[ERROR] No se cargaron misiones. Revisa el fixture y los módulos referenciados.")
    except Exception as e:
        print(f"[ERROR] Falló la carga de misiones: {e}")
        raise

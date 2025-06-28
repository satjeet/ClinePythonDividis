from api.models import Mission
from collections import defaultdict

def run():
    # Agrupa por (title, frequency, module)
    missions = Mission.objects.all()
    seen = defaultdict(list)
    for m in missions:
        key = (m.title.strip().lower(), m.frequency, str(m.module_id) if m.module_id else None)
        seen[key].append(m)

    deleted = 0
    for key, items in seen.items():
        if len(items) > 1:
            # Deja el primero, borra los demás
            for m in items[1:]:
                print(f"Borrando duplicado: {m.title} ({m.id})")
                m.delete()
                deleted += 1
    print(f"Total misiones duplicadas eliminadas: {deleted}")

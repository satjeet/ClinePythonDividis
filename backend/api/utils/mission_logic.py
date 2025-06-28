from api.models import Mission, MissionProgress, ModuleProgress, Declaration

def check_and_complete_missions(user, module, pillar=None):
    """
    Evalúa y completa las misiones del módulo para el usuario según requisitos.
    Si la misión requiere un pilar, solo se completa si hay declaración en ese pilar.
    """
    module_missions = Mission.objects.filter(module=module)
    for mission in module_missions:
        requisitos = getattr(mission, "requirements", [])
        cumple_requisitos = True
        for req in requisitos:
            if req.get("type") == "mission":
                prev_mission_id = req.get("id")
                prev_mp = MissionProgress.objects.filter(user=user, mission_id=prev_mission_id, state="completed").first()
                if not prev_mp:
                    cumple_requisitos = False
                    break
            if req.get("type") == "module":
                mod_id = req.get("id")
                mod_prog = ModuleProgress.objects.filter(user=user, module_id=mod_id, state="unlocked").first()
                if not mod_prog:
                    cumple_requisitos = False
                    break
            if req.get("type") == "pillar":
                pillar_id = req.get("id")
                decl = Declaration.objects.filter(user=user, module=module, pillar=pillar_id).exists()
                if not decl:
                    cumple_requisitos = False
                    break
        if cumple_requisitos:
            mp, created = MissionProgress.objects.get_or_create(user=user, mission=mission)
            if mp.state != "completed":
                mp.complete()
                mp.save()

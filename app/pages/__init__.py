# Re-exporta vistas del dashboard / Re-exports dashboard page views

from app.pages.resumen  import Tab1_ResumenEjecutivo
from app.pages.fanzones import Tab2_FanZones
from app.pages.fases    import Tab3_Fases
from app.pages.equipos  import Tab4_Equipos
from app.pages.explorer import Tab5_Explorer

__all__ = [
    "Tab1_ResumenEjecutivo",
    "Tab2_FanZones",
    "Tab3_Fases",
    "Tab4_Equipos",
    "Tab5_Explorer",
]

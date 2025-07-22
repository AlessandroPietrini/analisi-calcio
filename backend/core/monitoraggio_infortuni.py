from typing import List, Optional
from pydantic import BaseModel

class Infortunio(BaseModel):
    tipo: str           # es. "distorsione", "lesione muscolare"
    data_inizio: str    # es. "2025-07-15"
    durata_stimata_giorni: int
    gravita: str        # es. "leggero", "moderato", "grave"
    note: Optional[str] = None

class ImpegnoAtleta(BaseModel):
    data: str           # es. "2025-07-20"
    tipo: str           # es. "allenamento", "visita medica"
    descrizione: Optional[str] = None

class MonitoraggioAtleta(BaseModel):
    nome: str
    infortuni: List[Infortunio]
    impegni: List[ImpegnoAtleta]



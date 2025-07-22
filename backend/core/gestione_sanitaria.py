from typing import List
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional

class CuraMedica(BaseModel):
    paziente: str
    descrizione: Optional[str] = None
    # aggiungi qui altri campi se ce ne sono, ad esempio:
    # durata: Optional[int] = None
    # tipo: Optional[str] = None

class PianoRecupero(BaseModel):
    nome: str
    durata_giorni: int
    descrizione: str

class AppuntamentoMedico(BaseModel):
    data: str  # es. "2025-07-20"
    luogo: str
    tipo: str  # visita, fisioterapia, etc.

class ProgressiRecupero(BaseModel):
    data: str
    stato: str  # es. miglioramento, stabile, peggioramento

class Macchinario(BaseModel):
    nome: str
    produttore: str
    costo: float
    rendimento: float  # es. percentuale di efficacia

class CuraMedica(BaseModel):
    paziente: str
    piani_recupero: List[PianoRecupero]
    appuntamenti: List[AppuntamentoMedico]
    progressi: List[ProgressiRecupero]
    macchinari_usati: List[Macchinario]

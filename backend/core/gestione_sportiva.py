from pydantic import BaseModel

class PrestazioneAtleta(BaseModel):
    nome: str
    partita: str
    minuti_giocati: int
    gol: int
    assist: int
    passaggi_riusciti: int
    km_percorsi: float
    valutazione_coach: float


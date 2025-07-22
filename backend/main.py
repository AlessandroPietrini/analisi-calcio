from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from backend.core.modulo_suggerito import suggerisci_modulo
from backend.core.gestione_sanitaria import CuraMedica
from backend.core.monitoraggio_infortuni import MonitoraggioAtleta
from backend.core.database import database
from backend.core.models import cure_mediche
from backend.core.models import prestazioni_atleti
from backend.core.gestione_sportiva import PrestazioneAtleta
from backend.ml.api_model import router as ml_router

# --- CONFIGURAZIONE APP ---
app = FastAPI()

# --- ABILITA CORS ---
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE EVENTS ---
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class PlayerAdvanced(BaseModel):
    name: str
    fatigue: float        # da 0 a 1
    trust: float          # da 0 a 1
    minutes_played: int
    recent_injuries: int

# --- MODELLO GIOCATORE ---
class Player(BaseModel):
    name: str
    position: str
    fatigue: float
    trust: float
    minutes_played: int
    injuries: int
    performance_rating: float

# --- ROTAZIONE GIOCATORI ---
@app.post("/decisione/rotazione")
def rotazione_giocatore(player: Player):
    if player.fatigue > 0.7:
        return {"decision": "RIPOSO", "reason": "Alto affaticamento"}
    elif player.trust < 0.4:
        return {"decision": "ROTATIONE", "reason": "Bassa fiducia nel club"}
    return {"decision": "TITOLARE", "reason": "Stabile e in buona forma"}

# --- SUGGERISCI MODULO ---
@app.post("/schema/suggerito")
def schema_ottimale(giocatori: List[Player]):
    giocatori_dict = [g.dict() for g in giocatori]
    modulo = suggerisci_modulo(giocatori_dict)
    return {"modulo_suggerito": modulo}

# --- GESTIONE CURE MEDICHE (DATABASE) ---
@app.post("/cura/aggiungi")
async def aggiungi_cura(cura: CuraMedica):
    query = cure_mediche.insert().values(
        paziente=cura.paziente,
        descrizione=getattr(cura, 'descrizione', None)
        # altri campi qui, se presenti
    )
    last_record_id = await database.execute(query)
    return {"message": "Cura medica aggiunta con successo", "id": last_record_id}

@app.get("/cura/{id}")
async def leggi_cura(id: int):
    query = cure_mediche.select().where(cure_mediche.c.id == id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Cura medica non trovata")
    return dict(result)

@app.get("/cure")
async def tutte_cure():
    query = cure_mediche.select()
    results = await database.fetch_all(query)
    return [dict(r) for r in results]

# --- GESTIONE MONITORAGGIO (SOLO IN MEMORIA) ---
monitoraggi = []

@app.post("/monitoraggio/aggiungi")
def aggiungi_monitoraggio(monitoraggio: MonitoraggioAtleta):
    monitoraggi.append(monitoraggio)
    return {"message": "Monitoraggio atleta aggiunto", "id": len(monitoraggi) - 1}

@app.get("/monitoraggio/{id}")
def leggi_monitoraggio(id: int):
    if 0 <= id < len(monitoraggi):
        return monitoraggi[id]
    raise HTTPException(status_code=404, detail="Monitoraggio non trovato")

@app.get("/monitoraggi")
def tutti_monitoraggi():
    return monitoraggi
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Benvenuto</title>
        </head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>API Progetto Analisi Calcio</h1>
            <p>Vai su <a href="/docs">/docs</a> per usare le API.</p>
        </body>
    </html>
    """
# --- GESTIONE PRESTAZIONI ATLETI ---

@app.post("/prestazione/aggiungi")
async def aggiungi_prestazione(prestazione: PrestazioneAtleta):
    query = prestazioni_atleti.insert().values(**prestazione.dict())
    record_id = await database.execute(query)
    return {"message": "Prestazione salvata", "id": record_id}

@app.get("/prestazione/{id}")
async def leggi_prestazione(id: int):
    query = prestazioni_atleti.select().where(prestazioni_atleti.c.id == id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Prestazione non trovata")
    return dict(result)

@app.get("/prestazioni")
async def tutte_prestazioni():
    query = prestazioni_atleti.select()
    results = await database.fetch_all(query)
    return [dict(r) for r in results]

@app.post("/analisi/prestazione")
def analisi_prestazione(player: Player):
    valutazione = []

    if player.fatigue > 0.8:
        valutazione.append("⚠️ Affaticamento elevato")
    if player.trust < 0.4:
        valutazione.append("❗ Fiducia bassa")
    if player.minutes_played > 270:
        valutazione.append("🕒 Troppi minuti giocati")
    if player.injuries > 0:
        valutazione.append("🚑 Infortuni recenti")
    if player.performance_rating >= 8.0:
        valutazione.append("⭐ Prestazione eccellente")
    elif player.performance_rating < 5.5:
        valutazione.append("📉 Prestazione sotto la media")

    if not valutazione:
        valutazione.append("✅ Stato fisico e mentale positivo")

    return {
        "giocatore": player.name,
        "valutazione": valutazione
    }
def valuta_giocatore_avanzato(player: PlayerAdvanced):
    valutazioni = []
    decisione = "TITOLARE"

    # Controllo affaticamento
    if player.fatigue > 0.7:
        valutazioni.append("⚠️ Affaticamento elevato")
    
    # Controllo fiducia
    if player.trust < 0.4:
        valutazioni.append("❗ Fiducia bassa")

    # Minuti giocati
    if player.minutes_played > 300:
        valutazioni.append("🕒 Troppi minuti giocati")

    # Infortuni recenti
    if player.recent_injuries > 0:
        valutazioni.append("🚑 Infortuni recenti")

    # Decisione tattica basata sui parametri
    if player.fatigue > 0.8 or player.recent_injuries > 1:
        decisione = "RIPOSO"
    elif player.trust < 0.3:
        decisione = "ROTATIONE"
    elif player.minutes_played > 350:
        decisione = "UTILIZZO LIMITATO"
    else:
        decisione = "TITOLARE"

    return {
        "giocatore": player.name,
        "valutazione": valutazioni,
        "decisione": decisione
    }

@app.post("/decisione/avanzata")
def decisione_avanzata(player: PlayerAdvanced):
    risultato = valuta_giocatore_avanzato(player)
    return risultato

app.include_router(ml_router)
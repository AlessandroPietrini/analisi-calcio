from fastapi import APIRouter
from pydantic import BaseModel, Field
import joblib
import os

router = APIRouter()

class PlayerInput(BaseModel):
    minuti: int = Field(..., ge=0, le=200, description="Minuti giocati (0-200)")
    partite_ultime_2_settimane: int = Field(..., ge=0, le=10, description="Partite nelle ultime 2 settimane (0-10)")

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(model_path)

@router.post("/predict")
def predict(data: PlayerInput):
    print(f"Ricevuta richiesta con dati: {data}")
    features = [[data.minuti, data.partite_ultime_2_settimane]]
    prediction = model.predict(features)[0]
    print(f"Predizione: {prediction}")
    return {"affaticamento_predetto": round(prediction, 3)}


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Dati di esempio
data = pd.DataFrame({
    "minuti": [90, 70, 60, 30, 20, 10, 100, 110, 85, 50],
    "partite_ultime_2_settimane": [3, 2, 4, 1, 1, 0, 5, 5, 3, 2],
    "affaticamento": [0.9, 0.7, 0.65, 0.4, 0.3, 0.1, 0.95, 0.98, 0.85, 0.5]
})

X = data[["minuti", "partite_ultime_2_settimane"]]
y = data["affaticamento"]

# Crea e addestra il modello
model = RandomForestRegressor()
model.fit(X, y)

# Percorso di salvataggio del modello
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump(model, model_path)

print("✅ Modello salvato con successo in:", model_path)


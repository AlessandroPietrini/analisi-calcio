import pandas as pd
import numpy as np
import os

campo_lunghezza = 105
campo_larghezza = 68
num_giocatori = 22
durata = 90  # secondi
freq = 1     # frequenza campionamento

np.random.seed(42)

# Posizioni iniziali casuali
pos_iniziali = np.column_stack((
    np.random.uniform(0, campo_lunghezza, num_giocatori),
    np.random.uniform(0, campo_larghezza, num_giocatori)
))

# Movimento simulato
def spostamento(prev_pos):
    delta = np.random.normal(0, 1.5, size=prev_pos.shape)
    nuova_pos = prev_pos + delta
    nuova_pos[:, 0] = np.clip(nuova_pos[:, 0], 0, campo_lunghezza)
    nuova_pos[:, 1] = np.clip(nuova_pos[:, 1], 0, campo_larghezza)
    return nuova_pos

records = []
pos_correnti = pos_iniziali.copy()

for t in range(0, durata, freq):
    for giocatore_id in range(1, num_giocatori + 1):
        x, y = pos_correnti[giocatore_id - 1]
        velocita = np.random.uniform(0, 7)  # m/s
        sprint = 1 if velocita > 6 else 0
        passaggi_chiave = np.random.poisson(0.2)
        records.append({
            "tempo": t,
            "giocatore": giocatore_id,
            "x_pos": x,
            "y_pos": y,
            "velocita": velocita,
            "sprint": sprint,
            "passaggi_chiave": passaggi_chiave
        })
    pos_correnti = spostamento(pos_correnti)

df = pd.DataFrame(records)

# 📊 Calcolo "Indice di Incisività" fittizio
def calcola_indice(row):
    base = row['velocita'] * 2
    bonus_sprint = row['sprint'] * 10
    bonus_passaggi = row['passaggi_chiave'] * 8
    return min(100, base + bonus_sprint + bonus_passaggi)

df['indice_incisivita'] = df.apply(calcola_indice, axis=1)

# 🔽 Salva dati
os.makedirs("data", exist_ok=True)
df.to_csv("data/movimenti_giocatori.csv", index=False)

# 📌 Mostra ultimi valori
ultimo = df[df["tempo"] == df["tempo"].max()]
print(ultimo[["giocatore", "velocita", "sprint", "passaggi_chiave", "indice_incisivita"]])

print("✅ Dati salvati e indice calcolato.")


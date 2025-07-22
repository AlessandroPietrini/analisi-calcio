import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

# === Parametri campo ===
CAMPO_LUNGHEZZA = 105  # metri
CAMPO_LARGHEZZA = 68   # metri

# === Caricamento dati simulati ===
try:
    df = pd.read_csv("data/movimenti_giocatori.csv")  # Sostituibile con sorgenti reali
    logging.info("Dati movimento caricati correttamente.")
except FileNotFoundError:
    logging.error("File non trovato. Assicurati che 'movimenti_giocatori.csv' sia nella cartella /data")
    exit(1)

# === Calcolo velocità per ogni giocatore ===
df = df.sort_values(by=["giocatore", "tempo"])
df["velocità"] = 0.0

for g in df["giocatore"].unique():
    dati_g = df[df["giocatore"] == g]
    dx = dati_g["x_pos"].diff()
    dy = dati_g["y_pos"].diff()
    dt = dati_g["tempo"].diff()
    v = np.sqrt(dx**2 + dy**2) / dt
    df.loc[dati_g.index, "velocità"] = v

# === Riconoscimento spazi liberi (snapshot finale) ===
ultimo_frame = df[df["tempo"] == df["tempo"].max()]
heatmap = np.zeros((CAMPO_LUNGHEZZA, CAMPO_LARGHEZZA))

for _, r in ultimo_frame.iterrows():
    x = int(min(CAMPO_LUNGHEZZA-1, r["x_pos"]))
    y = int(min(CAMPO_LARGHEZZA-1, r["y_pos"]))
    heatmap[x, y] += 1

# Spazi vuoti = zone con valori bassi nella heatmap
plt.imshow(heatmap.T, origin="lower", cmap="coolwarm", extent=[0, CAMPO_LUNGHEZZA, 0, CAMPO_LARGHEZZA])
plt.title("Mappa delle presenze - Aree meno occupate = spazi liberi")
plt.xlabel("Lunghezza campo (m)")
plt.ylabel("Larghezza campo (m)")
plt.colorbar(label="Presenza giocatori")
plt.grid(True)
plt.show()

# === Analisi base affaticamento (inverso della velocità media) ===
fatigue_scores = df.groupby("giocatore")["velocità"].mean().reset_index()
fatigue_scores["affaticamento_stimato"] = 1 / fatigue_scores["velocità"]
print("\nAffaticamento stimato per giocatore:")
print(fatigue_scores[["giocatore", "affaticamento_stimato"]])


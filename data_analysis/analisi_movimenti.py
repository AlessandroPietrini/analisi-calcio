import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Parametri campo
campo_lunghezza = 105
campo_larghezza = 68
num_giocatori = 22
durata = 90  # secondi
freq = 1  # ogni secondo

# Simulazione movimenti giocatori
np.random.seed(42)  # per riproducibilità

# Genera posizioni iniziali casuali per tutti i giocatori (in campo)
pos_iniziali = np.column_stack((
    np.random.uniform(0, campo_lunghezza, num_giocatori),
    np.random.uniform(0, campo_larghezza, num_giocatori)
))

# Funzione per simulare piccoli spostamenti ogni secondo
def spostamento(prev_pos):
    delta = np.random.normal(0, 1.5, size=prev_pos.shape)  # movimenti piccoli
    nuova_pos = prev_pos + delta
    # Limita posizioni ai confini del campo
    nuova_pos[:,0] = np.clip(nuova_pos[:,0], 0, campo_lunghezza)
    nuova_pos[:,1] = np.clip(nuova_pos[:,1], 0, campo_larghezza)
    return nuova_pos

# Costruzione dataframe dati posizioni nel tempo
records = []
pos_correnti = pos_iniziali.copy()

for t in range(0, durata, freq):
    for giocatore_id in range(1, num_giocatori+1):
        x, y = pos_correnti[giocatore_id-1]
        records.append({"tempo": t, "giocatore": giocatore_id, "x_pos": x, "y_pos": y})
    pos_correnti = spostamento(pos_correnti)

df = pd.DataFrame(records)

# Esempio: visualizza posizioni all’ultimo frame
ultimo_t = df['tempo'].max()
subset = df[df['tempo'] == ultimo_t]

plt.figure(figsize=(10,6.5))
plt.scatter(subset['x_pos'], subset['y_pos'], c='blue', label='Giocatori')
for _, r in subset.iterrows():
    plt.text(r['x_pos'], r['y_pos'], str(r['giocatore']), fontsize=8)
plt.xlim(0, campo_lunghezza)
plt.ylim(0, campo_larghezza)
plt.title(f"Posizioni giocatori al tempo {ultimo_t} secondi")
plt.xlabel("Lunghezza campo (m)")
plt.ylabel("Larghezza campo (m)")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()

# Analisi base: calcola distanza media tra ogni giocatore e i suoi compagni di squadra all’ultimo tempo
def distanza(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

distanze_medie = []
for g in range(1, num_giocatori+1):
    p = subset[subset['giocatore'] == g][['x_pos','y_pos']].values[0]
    # Squadra 1: giocatori 1-11, Squadra 2: giocatori 12-22
    if g <= 11:
        compagni = subset[(subset['giocatore'] >= 1) & (subset['giocatore'] <= 11) & (subset['giocatore'] != g)]
    else:
        compagni = subset[(subset['giocatore'] >= 12) & (subset['giocatore'] <= 22) & (subset['giocatore'] != g)]
    dists = [distanza(p, comp[['x_pos','y_pos']].values) for _, comp in compagni.iterrows()]
    dist_media = np.mean(dists)
    distanze_medie.append({"giocatore": g, "distanza_media_compagni": dist_media})

df_distanze = pd.DataFrame(distanze_medie)
print(df_distanze)

# Grafico distanza media compagni per giocatore
plt.bar(df_distanze['giocatore'], df_distanze['distanza_media_compagni'])
plt.xlabel("Giocatore")
plt.ylabel("Distanza media dai compagni (m)")
plt.title("Distanza media dai compagni all'ultimo secondo")
plt.show()

import os

# Crea la cartella "data" se non esiste
os.makedirs("data", exist_ok=True)

# Salva i dati in CSV
df.to_csv("data/movimenti_giocatori.csv", index=False)

if os.path.exists("data/movimenti_giocatori.csv"):
    print("✅ File salvato correttamente.")
else:
    print("❌ Errore nel salvataggio.")


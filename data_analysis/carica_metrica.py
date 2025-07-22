import pandas as pd
import json
import os

base_path = "data/metrica/sample_game_1"

# Carica dati tracking
tracking_home = pd.read_csv(os.path.join(base_path, "tracking_home.csv"))
tracking_away = pd.read_csv(os.path.join(base_path, "tracking_away.csv"))

# Carica dati eventi
with open(os.path.join(base_path, "events.json")) as f:
    events = json.load(f)

print(tracking_home.head())
print(tracking_away.head())
print(events[0])  # Stampa primo evento per dare un’occhiata

base_path = "data/metrica/sample_game_1"

tracking_home = pd.read_csv(os.path.join(base_path, "Sample_Game_1_RawTrackingData_Home_Team.csv"))
tracking_away = pd.read_csv(os.path.join(base_path, "Sample_Game_1_RawTrackingData_Away_Team.csv"))

print(tracking_home.head())
print(tracking_away.head())

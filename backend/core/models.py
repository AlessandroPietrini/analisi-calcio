from sqlalchemy import Table, Column, Integer, String, Float, MetaData

metadata = MetaData()

cure_mediche = Table(
    "cure_mediche",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("paziente", String, nullable=False),
    Column("descrizione", String),
    # Aggiungi altre colonne se serve, ad esempio:
    # Column("data_inizio", String),
    # Column("durata", Integer),
    # Column("costo", Float),
)
prestazioni_atleti = Table(
    "prestazioni_atleti",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String),
    Column("partita", String),
    Column("minuti_giocati", Integer),
    Column("gol", Integer),
    Column("assist", Integer),
    Column("passaggi_riusciti", Integer),
    Column("km_percorsi", Float),
    Column("valutazione_coach", Float)
) 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Tema Scuro Leggibile
st.set_page_config(page_title="Analisi Calcio", layout="wide", initial_sidebar_state="auto")

st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .st-cf {
        color: #f0f2f6 !important;
    }
    .css-18e3th9 {
        background-color: #0e1117 !important;
    }
    .css-1v0mbdj {
        background-color: #0e1117 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard Analisi Calcio")
st.markdown("Benvenuto nella piattaforma interattiva per l'analisi calcistica.")

menu = st.sidebar.selectbox("Seleziona Sezione", [
    "🏃 Statistiche Giocatori",
    "💊 Dati Medici",
    "🧠 Tattica & Moduli",
    "🔥 Indice di Incisività",
    "📁 Upload Nuovi Dati"
])

if menu == "🏃 Statistiche Giocatori":
    st.header("Statistiche Individuali")

    try:
        df = pd.read_csv("dati_esempio.csv")
        st.success("⚽ Caricato file dati_esempio.csv di default.")
    except Exception:
        st.error("Errore nel caricamento del file di esempio.")
        st.stop()

    uploaded_file = st.file_uploader("Oppure carica un file CSV o Parquet", type=["csv", "parquet"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_parquet(uploaded_file)

    ruolo = st.selectbox("Filtra per ruolo", df['Ruolo'].unique())
    df_filtrato = df[df['Ruolo'] == ruolo]

    giocatore = st.selectbox("Scegli un giocatore", df_filtrato['Nome'].unique())
    df_giocatore = df_filtrato[df_filtrato['Nome'] == giocatore]

    st.subheader("Statistiche Giocatore Selezionato")
    st.dataframe(df_giocatore)

    st.subheader("Radar Statistiche Tecniche")
    radar_cols = ["Velocità", "Tiri", "Passaggi", "Dribbling", "Difesa"]
    radar_stats = df_giocatore[radar_cols].iloc[0]
    st.bar_chart(radar_stats)

    st.subheader("Trend Prestazioni")
    prestazioni = df_giocatore[["Match1", "Match2", "Match3", "Match4", "Match5"]].T
    prestazioni.columns = [giocatore]
    st.line_chart(prestazioni)

elif menu == "💊 Dati Medici":
    st.header("Dati Medici e Infortuni")
    st.markdown("Analisi infortuni storici e tempi di recupero del giocatore.")

    try:
        df_medici = pd.read_csv("dati_medici.csv")
        giocatori = df_medici['Nome'].unique()
        giocatore_sel = st.selectbox("Scegli un giocatore", giocatori)

        dati_giocatore = df_medici[df_medici['Nome'] == giocatore_sel]

        st.subheader(f"Infortuni di {giocatore_sel}")
        st.dataframe(dati_giocatore)

        # Barplot: Giorni di stop per infortunio
        fig1, ax1 = plt.subplots()
        sns.barplot(data=dati_giocatore, x="Data", y="GiorniStop", hue="TipoInfortunio", ax=ax1)
        ax1.set_title(f"Giorni di Stop per Infortunio - {giocatore_sel}", color="white")
        ax1.set_ylabel("Giorni di Stop")
        ax1.set_xlabel("Data Infortunio")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        # Pie chart: Tipi di infortunio
        st.subheader("Distribuzione Tipi di Infortunio")
        tipo_counts = dati_giocatore['TipoInfortunio'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(tipo_counts, labels=tipo_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax2.axis('equal')
        st.pyplot(fig2)

        # Suggerimento medico personalizzato (simulato)
        st.subheader("💡 Suggerimento Medico")
        ultimo_infortunio = dati_giocatore.sort_values("Data").iloc[-1]
        suggerimento = ""

        if "muscolare" in ultimo_infortunio['TipoInfortunio'].lower():
            suggerimento = "Incrementare fisioterapia + monitoraggio carichi di lavoro."
        elif "distorsione" in ultimo_infortunio['TipoInfortunio'].lower():
            suggerimento = "Lavoro propriocettivo e rinforzo articolare."
        else:
            suggerimento = "Mantenere carichi progressivi e controlli settimanali."

        st.info(f"📅 Ultimo infortunio: {ultimo_infortunio['TipoInfortunio']} il {ultimo_infortunio['Data']}")
        st.success(f"✅ Suggerimento: {suggerimento}")

    except FileNotFoundError:
        st.warning("⚠️ Il file `dati_medici.csv` non è stato trovato nella directory del progetto.")

elif menu == "🧠 Tattica & Moduli":
    st.header("Soluzioni Tattiche")
    st.markdown("Diagrammi tattici, heatmap di posizione, comparazioni tra moduli...")

elif menu == "🔥 Indice di Incisività":
    st.header("Indice di Incisività")
    st.markdown("Visualizzazione dell'indice sviluppato per ogni calciatore.")
    st.line_chart([0.2, 0.4, 0.6, 0.9])  # dati di esempio

elif menu == "📁 Upload Nuovi Dati":
    st.header("Carica Nuovi Dati")
    st.markdown("Permetti il caricamento di file CSV o Parquet per aggiornare il database.")


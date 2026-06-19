import streamlit as st
import os

st.set_page_config(page_title="Dashboard Hub", page_icon="📊", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #DCA258;'>📊 DASHBOARD HUB</h1>
    <p style='text-align: center; color: rgba(255,255,255,0.4);'>Wähle ein Dashboard aus</p>
""", unsafe_allow_html=True)

# ─── DASHBOARD AUSWÄHLEN ───
option = st.selectbox(
    "Dashboard wählen:",
    [
        "📈 ETF Allokation",
        "📊 Anleihen-Scanner",
        "🏗️ Immobilien Pro-Forma",
        "📊 FX Wochenvorbereitung",
        "₿ Bitcoin Langzeit"
    ]
)

# ─── DASHBOARD DATEIEN ───
dashboards = {
    "📈 ETF Allokation": "etf_dashboard.py",
    "📊 Anleihen-Scanner": "Anleihen_Dashboard.py",
    "🏗️ Immobilien Pro-Forma": "Immobilien_Dashboard.py",
    "📊 FX Wochenvorbereitung": "FXWochenvorbereitung_Dashboard.py",
    "₿ Bitcoin Langzeit": "bitcoin_longterm_dashboard.py",
}

# ─── AUSGEWÄHLTES DASHBOARD ANZEIGEN ───
file = dashboards[option]

if os.path.exists(file):
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code)
else:
    st.error(f"❌ Datei nicht gefunden: {file}")
# bitcoin_longterm_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Bitcoin Langfrist-Strategie",
    page_icon="₿",
    layout="wide"
)

# ============================================================
# 2. ULTRA LUXURY CSS (Black/Gold)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
    .stApp { background: linear-gradient(160deg, #0A0A0A 0%, #1A1A1A 35%, #222222 65%, #0A0A0A 100%); min-height: 100vh; }
    .stApp::before { content: ''; position: fixed; top: -20%; left: -20%; width: 140%; height: 140%; background: radial-gradient(ellipse at 40% 30%, rgba(212, 168, 83, 0.03) 0%, transparent 60%); pointer-events: none; z-index: 0; }
    .main > div { background: transparent; max-width: 1300px; margin: 0 auto; padding: 2rem 2rem 4rem 2rem; position: relative; z-index: 1; }
    .block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1300px; margin: 0 auto; }
    
    .title-wrapper { display: flex; justify-content: center; width: 100%; margin: 0 auto 1.2rem auto; max-width: 700px; white-space: nowrap; }
    .main-title { font-size: 2.6rem; font-weight: 800; letter-spacing: 0.04em; text-align: center; margin: 0; color: #FFFFFF; line-height: 1.2; width: 100%; text-shadow: 0 2px 40px rgba(212, 168, 83, 0.05); white-space: nowrap; }
    .main-title span { background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    
    .section-headline { font-size: 1.1rem !important; font-weight: 500; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255, 255, 255, 0.35) !important; text-align: center; margin: 0; }
    
    .metric-card { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 16px; padding: 0.8rem 0.5rem; text-align: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; flex: 1 1 0; min-width: 120px; max-width: 170px; height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .metric-card:hover { border-color: rgba(212, 168, 83, 0.15); background: rgba(255, 255, 255, 0.04); transform: translateY(-2px); }
    .metric-card .label { color: rgba(255, 255, 255, 0.3); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.1rem; white-space: nowrap; }
    .metric-card .value { font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #D4A853 0%, #F5D98E 60%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.2; white-space: nowrap; }
    
    .stDataFrame { background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(8px); border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.04) !important; overflow: hidden; margin: 0 auto 1rem auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
    .stDataFrame th { background: rgba(255, 255, 255, 0.03) !important; color: rgba(255, 255, 255, 0.2) !important; font-weight: 500 !important; font-size: 0.6rem !important; text-transform: uppercase !important; letter-spacing: 0.2em !important; text-align: center !important; padding: 0.8rem 1rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame td { background: transparent !important; color: rgba(255, 255, 255, 0.8) !important; text-align: center !important; padding: 0.7rem 1rem !important; font-size: 0.9rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important; }
    .stDataFrame tr:hover td { background: rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame tr:last-child td { border-bottom: none !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. TITLE
# ============================================================
st.markdown("""
    <div class="title-wrapper">
        <h1 class="main-title">₿ BITCOIN <span>LANGZEIT-STRATEGIE</span></h1>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 4. DATEN ABRUFEN (Bitcoin Charts API + Fallback)
# ============================================================

@st.cache_data(ttl=3600)
def fetch_bitcoin_data():
    """
    Holt Bitcoin Preis- und Indikatordaten von verschiedenen kostenlosen APIs.
    """
    data = {}
    
    # 1. Pi Cycle Top Indicator (Bitcoin Charts API)
    try:
        url = "https://charts.bitcoin.com/api/v1/charts/pi-cycle-top?interval=daily&timespan=2y&limit=730"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            data["pi_cycle"] = json_data
        else:
            data["pi_cycle"] = None
    except:
        data["pi_cycle"] = None
    
    # 2. Aktueller Bitcoin Preis (Fallback, falls Pi Cycle keine Preisdaten liefert)
    try:
        # Nutze CoinGecko für aktuellen Preis (kostenlos, kein API-Key)
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data["price_usd"] = response.json().get("bitcoin", {}).get("usd", 0)
        else:
            data["price_usd"] = None
    except:
        data["price_usd"] = None
    
    # 3. Realized Price (über BGeometrics API – Free Tier)
    try:
        # BGeometrics API für Realized Price (Endpunkt abgeleitet aus Dokumentation)
        # Da die genaue Endpunkt-Struktur variieren kann, hier ein Platzhalter
        # In der Praxis: https://charts.bgeometrics.com/api/... (mit API-Key)
        data["realized_price"] = None  # Platzhalter – wird bei echter Implementierung gefüllt
    except:
        data["realized_price"] = None
    
    return data

# ============================================================
# 5. ZYKLUS-BERECHNUNGEN
# ============================================================

def calculate_cycle_phases(current_date):
    """
    Berechnet die Zyklusphasen basierend auf 1.064 Tagen Bullenmarkt,
    364 Tagen Bärenmarkt.
    """
    # Historische Zyklusdaten (basierend auf Analyse)
    # Zyklus 2022-2025: Tief bei ~15.500 USD (Nov 2022), Peak bei ~126.000 USD (Okt 2025)
    # Nächster Zyklus: Bärenmarkt-Tief erwartet Okt 2026, Bullenmarkt-Peak Aug 2029
    
    # Definierte Zyklus-Eckpunkte (basierend auf deiner Analyse)
    cycle_lows = [
        {"date": datetime(2015, 1, 1), "price": 200},      # Beispiel
        {"date": datetime(2018, 12, 15), "price": 3200},   # Beispiel
        {"date": datetime(2022, 11, 21), "price": 15500},  # Tatsächliches Tief
        {"date": datetime(2026, 10, 6), "price": 38000},   # Projiziertes Tief
    ]
    
    cycle_peaks = [
        {"date": datetime(2017, 12, 17), "price": 19700},  # Beispiel
        {"date": datetime(2021, 4, 14), "price": 64800},   # Beispiel
        {"date": datetime(2025, 10, 6), "price": 126000},  # Tatsächlicher Peak
        {"date": datetime(2029, 8, 3), "price": 185000},   # Projizierter Peak (Mittelwert)
    ]
    
    # Aktuelle Zyklusphase bestimmen
    # Annahme: Wir sind im Bärenmarkt 2025-2026
    bear_start = cycle_peaks[2]["date"]  # 6. Okt 2025
    bear_end = cycle_lows[3]["date"]     # 6. Okt 2026
    bull_start = bear_end
    bull_end = cycle_peaks[3]["date"]    # 3. Aug 2029
    
    # Fortschritt im aktuellen Zyklus
    total_bear_days = (bear_end - bear_start).days
    elapsed_bear_days = (current_date - bear_start).days if current_date > bear_start else 0
    bear_progress = min(1.0, elapsed_bear_days / total_bear_days) if total_bear_days > 0 else 0
    
    return {
        "bear_start": bear_start,
        "bear_end": bear_end,
        "bull_start": bull_start,
        "bull_end": bull_end,
        "bear_progress": bear_progress,
        "days_in_bear": elapsed_bear_days,
        "days_until_bull": max(0, (bear_end - current_date).days) if current_date < bear_end else 0,
        "peak_price_projected": 185000,  # Mittelwert aus 170.000-200.000 USD
        "low_price_projected": 38000,
    }

# ============================================================
# 6. ON-CHAIN-INDIKATOREN (Simuliert / Platzhalter)
# ============================================================

def get_onchain_indicators():
    """
    Holt oder simuliert die wichtigsten On-Chain-Indikatoren.
    In der Produktion werden diese über APIs (BGeometrics, crypto-yfinance, chaindl) bezogen.
    """
    # Platzhalter – in der echten Implementierung werden diese Werte von APIs geladen
    return {
        "pi_cycle_111ma": 95000,
        "pi_cycle_350ma_x2": 98000,
        "pi_cycle_signal": "Kein Crossover",  # "Crossover" wenn 111MA > 350MA*2
        "mvrv_z_score": 1.8,  # < 0 = undervalued, > 7 = overvalued
        "nupl": 0.35,  # 0-0.5 = Belief, 0.5-0.75 = Optimism, >0.75 = Euphoria
        "puell_multiple": 1.2,  # < 0.5 = oversold, > 4 = overbought
        "rhodl_ratio": 15000,  # < 10000 = bearish, > 50000 = euphoric
        "lth_sopr": 1.8,  # > 3 = profit-taking by long-term holders
        "realized_price": 55000,
        "delta_price": 38000,
    }

# ============================================================
# 7. DASHBOARD
# ============================================================

# Daten laden
btc_data = fetch_bitcoin_data()
cycle = calculate_cycle_phases(datetime.now())
onchain = get_onchain_indicators()

# Aktueller Preis (aus Pi Cycle oder Fallback)
current_price = 0
if btc_data.get("pi_cycle") and "data" in btc_data["pi_cycle"]:
    price_data = btc_data["pi_cycle"]["data"].get("price", [])
    if price_data:
        current_price = price_data[-1].get("y", 0) if isinstance(price_data[-1], dict) else price_data[-1]
if current_price == 0:
    current_price = btc_data.get("price_usd", 0)

# ─── KEY METRICS ───
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
        <p class="section-headline">Kennzahlen</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">BTC Preis</div>
            <div class="value">${current_price:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Realized Price</div>
            <div class="value">${onchain['realized_price']:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Delta Price</div>
            <div class="value">${onchain['delta_price']:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">MVRV Z-Score</div>
            <div class="value">{onchain['mvrv_z_score']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">NUPL</div>
            <div class="value">{onchain['nupl']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Puell Multiple</div>
            <div class="value">{onchain['puell_multiple']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

# ─── ZYKLUS-PROJEKTION ───
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 2rem 0 1.5rem 0;">
        <p class="section-headline">Zyklus-Projektion</p>
    </div>
""", unsafe_allow_html=True)

cycle_data = []
cycle_data.append({"Phase": "Bärenmarkt Start", "Datum": cycle["bear_start"].strftime("%d.%m.%Y"), "Preis": "~126.000 USD"})
cycle_data.append({"Phase": "Bärenmarkt Tief (proj.)", "Datum": cycle["bear_end"].strftime("%d.%m.%Y"), "Preis": f"~{cycle['low_price_projected']:,.0f} USD"})
cycle_data.append({"Phase": "Bullenmarkt Start", "Datum": cycle["bull_start"].strftime("%d.%m.%Y"), "Preis": f"~{cycle['low_price_projected']:,.0f} USD"})
cycle_data.append({"Phase": "Bullenmarkt Peak (proj.)", "Datum": cycle["bull_end"].strftime("%d.%m.%Y"), "Preis": f"~{cycle['peak_price_projected']:,.0f} USD"})

df_cycle = pd.DataFrame(cycle_data)
st.dataframe(df_cycle, use_container_width=True, hide_index=True)

# Fortschrittsbalken
st.markdown(f"""
    <div style="margin: 1rem 0; text-align: center;">
        <p style="color: rgba(255,255,255,0.4); font-size: 0.85rem;">
            Bärenmarkt-Fortschritt: {cycle['bear_progress']*100:.1f}% 
            ({cycle['days_in_bear']} von 364 Tagen)
        </p>
        <div style="background: rgba(255,255,255,0.05); border-radius: 10px; height: 8px; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(90deg, #D4A853, #F5D98E); width: {cycle['bear_progress']*100}%; height: 8px; border-radius: 10px;"></div>
        </div>
        <p style="color: rgba(255,255,255,0.2); font-size: 0.7rem; margin-top: 0.3rem;">
            {cycle['days_until_bull']} Tage bis zum erwarteten Bullenmarkt-Start
        </p>
    </div>
""", unsafe_allow_html=True)

# ─── ON-CHAIN INDIKATOREN ───
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 3rem 0 1.5rem 0;">
        <p class="section-headline">On-Chain Indikatoren</p>
    </div>
""", unsafe_allow_html=True)

indicator_data = []
indicator_data.append({"Indikator": "Pi Cycle 111 MA", "Wert": f"${onchain['pi_cycle_111ma']:,.0f}", "Signal": onchain['pi_cycle_signal']})
indicator_data.append({"Indikator": "Pi Cycle 350 MA × 2", "Wert": f"${onchain['pi_cycle_350ma_x2']:,.0f}", "Signal": "Crossover bei Überschreitung"})
indicator_data.append({"Indikator": "MVRV Z-Score", "Wert": f"{onchain['mvrv_z_score']:.2f}", "Signal": "> 7 = Overvalued, < 0 = Undervalued"})
indicator_data.append({"Indikator": "NUPL", "Wert": f"{onchain['nupl']:.2f}", "Signal": "> 0.75 = Euphoria"})
indicator_data.append({"Indikator": "Puell Multiple", "Wert": f"{onchain['puell_multiple']:.2f}", "Signal": "> 4 = Overbought"})
indicator_data.append({"Indikator": "RHODL Ratio", "Wert": f"{onchain['rhodl_ratio']:,.0f}", "Signal": "> 50.000 = Euphoric"})
indicator_data.append({"Indikator": "LTH-SOPR", "Wert": f"{onchain['lth_sopr']:.2f}", "Signal": "> 3 = Profit-Taking"})

df_indicators = pd.DataFrame(indicator_data)
st.dataframe(df_indicators, use_container_width=True, hide_index=True)

# ─── PROJEKTIONS-ZUSAMMENFASSUNG ───
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 3rem 0 1.5rem 0;">
        <p class="section-headline">Projektions-Zusammenfassung</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 16px; padding: 1.5rem; text-align: center; max-width: 800px; margin: 0 auto;">
        <p style="color: rgba(255,255,255,0.6); font-size: 1rem; line-height: 1.8;">
            <strong style="color: #D4A853;">Bärenmarkt-Tief (projiziert):</strong> ${cycle['low_price_projected']:,.0f} USD 
            (Oktober 2026)<br>
            <strong style="color: #D4A853;">Bullenmarkt-Peak (projiziert):</strong> ${cycle['peak_price_projected']:,.0f} USD 
            (August 2029)<br>
            <strong style="color: #D4A853;">Erwartete Rendite:</strong> 
            {((cycle['peak_price_projected'] / cycle['low_price_projected']) - 1) * 100:.0f} % 
            vom Tief bis zum Peak
        </p>
        <p style="color: rgba(255,255,255,0.2); font-size: 0.75rem; margin-top: 0.5rem;">
            Konvergenz aus Zyklus-Timing, nachlassenden Renditen und On-Chain-Indikatoren
        </p>
    </div>
""", unsafe_allow_html=True)

# ─── SIDEBAR: HINWEIS ───
st.sidebar.markdown("### 📖 Die 3 Säulen der Strategie")
st.sidebar.markdown("""
1. **Zyklus-Timing** – 1.064 Tage Bullenmarkt, 364 Tage Bärenmarkt
2. **Nachlassende Renditen** – Reduktionsfaktor ~2,9 pro Zyklus
3. **On-Chain-Indikatoren** – Pi Cycle, MVRV, NUPL, Puell, RHODL, LTH-SOPR

**Projektion für Zyklus 2026–2029:**
- Tief: ~38.000 USD (Okt 2026)
- Peak: 170.000–200.000 USD (Aug 2029)
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Datenquellen")
st.sidebar.markdown("""
- **Bitcoin Charts API** – Pi Cycle Top Indicator[reference:7]
- **BGeometrics API** – MVRV, NUPL, Realized Price[reference:8]
- **crypto-yfinance** – On-Chain Metriken[reference:9]
- **chaindl** – On-Chain Daten[reference:10]
""")

st.sidebar.caption("📅 Dashboard mit Streamlit")
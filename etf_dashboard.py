# etf_dashboard.py
import streamlit as st
import pandas as pd
import json
import os
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="ETF Allokation Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. PERFEKTES CSS – MIT AUSREICHEND ABSTAND NACH OBEN
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    /* ─── HAUPTSEITE ─── */
    .stApp {
        background: linear-gradient(160deg, #0A0A0A 0%, #1A1A1A 35%, #222222 65%, #0A0A0A 100%);
        min-height: 100vh;
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: -20%;
        left: -20%;
        width: 140%;
        height: 140%;
        background: radial-gradient(ellipse at 40% 30%, rgba(212, 168, 83, 0.03) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    .main > div {
        background: transparent;
        max-width: 820px;
        margin: 0 auto;
        padding: 5rem 2rem 4rem 2rem;  /* ← padding-top erhöht auf 5rem */
        position: relative;
        z-index: 1;
    }

    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 4rem;
        max-width: 820px;
        margin: 0 auto;
    }

    /* ─── SIDEBAR ─── */
    .css-1d391kg, .css-1lcbmhc {
        background: rgba(10, 10, 10, 0.92) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    .sidebar .stMarkdown { color: rgba(255, 255, 255, 0.7) !important; }
    .sidebar h1, .sidebar h2, .sidebar h3 { color: #D4A853 !important; font-weight: 600 !important; letter-spacing: 0.05em; }
    .sidebar .stNumberInput label {
        color: rgba(255, 255, 255, 0.25) !important;
        font-size: 0.65rem !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .sidebar .stNumberInput input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        padding: 0.6rem 0.75rem !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease;
    }
    .sidebar .stNumberInput input:focus {
        border-color: #D4A853 !important;
        background: rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 0 0 4px rgba(212, 168, 83, 0.06) !important;
    }
    .sidebar .stButton > button {
        background: linear-gradient(135deg, #D4A853 0%, #B8923A 100%) !important;
        color: #0A0A0A !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 2.2rem !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        box-shadow: 0 4px 20px rgba(212, 168, 83, 0.15) !important;
        transition: all 0.3s ease;
        letter-spacing: 0.05em;
        margin: 0.5rem 0 0 0 !important;
    }
    .sidebar .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(212, 168, 83, 0.3) !important;
        background: linear-gradient(135deg, #E8C06A 0%, #D4A853 100%) !important;
    }
    .sidebar .stAlert {
        background: rgba(212, 168, 83, 0.06) !important;
        border: 1px solid rgba(212, 168, 83, 0.1) !important;
        border-radius: 10px !important;
        color: #F5D98E !important;
        font-size: 0.8rem !important;
        padding: 0.5rem !important;
        text-align: center;
    }
    .sidebar .stMarkdown p {
        color: rgba(255, 255, 255, 0.35) !important;
        font-size: 0.75rem !important;
        line-height: 1.7;
    }
    .sidebar .stMarkdown strong {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    .sidebar .stCaption {
        color: rgba(255, 255, 255, 0.06) !important;
        font-size: 0.5rem !important;
        text-align: center;
        letter-spacing: 0.1em;
    }

    /* ─── TITEL – PERFEKT ZENTRIERT, MEHR ABSTAND NACH OBEN ─── */
    .title-wrapper {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 0 auto 2.5rem auto;
        max-width: 620px;
        padding: 0;
    }
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-align: center;
        margin: 0;
        color: #FFFFFF;
        line-height: 1.2;
        width: 100%;
        text-shadow: 0 2px 40px rgba(212, 168, 83, 0.05);
    }
    .main-title span {
        background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ─── TABS ─── */
    .stTabs { margin-top: 0.5rem; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        justify-content: center;
        background: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        margin: 0 auto 2rem auto;
        max-width: 500px;
        padding-bottom: 0.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: rgba(255, 255, 255, 0.2) !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.15em;
        padding: 0.6rem 1.8rem !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab"]:hover { color: rgba(255, 255, 255, 0.5) !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #D4A853 !important;
        border-bottom-color: #D4A853 !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 0.5rem !important; }

    /* ─── SIGNAL-BOX ─── */
    .signal-box {
        text-align: center;
        margin: 0 auto 2.5rem auto;
        padding: 1.8rem 2rem;
        max-width: 440px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .signal-box:hover {
        border-color: rgba(212, 168, 83, 0.1);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5);
    }
    .signal-box .signal-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        color: rgba(255, 255, 255, 0.2);
        margin: 0 0 0.3rem 0;
    }
    .signal-box .signal-value {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        letter-spacing: 0.04em;
    }
    .signal-box .signal-detail {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.2);
        margin: 0.3rem 0 0 0;
        letter-spacing: 0.05em;
    }

    /* ─── SECTION TITLE ─── */
    .section-title {
        text-align: center;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        color: rgba(255, 255, 255, 0.1);
        margin: 0 0 1.5rem 0;
        font-weight: 500;
    }

    /* ─── ALLOKATION ─── */
    .allocation-grid {
        display: flex;
        justify-content: center;
        gap: 1.8rem;
        margin: 0 auto 2.5rem auto;
        flex-wrap: wrap;
        max-width: 620px;
        width: 100%;
    }
    .allocation-item {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        text-align: center;
        flex: 1 1 0;
        min-width: 120px;
        max-width: unset;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.4s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .allocation-item:hover {
        border-color: rgba(212, 168, 83, 0.15);
        background: rgba(255, 255, 255, 0.04);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
    }
    .allocation-item .label {
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 0 0 0.25rem 0;
        text-align: center;
    }
    .allocation-item .value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #D4A853 0%, #F5D98E 60%, #D4A853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.2;
        text-align: center;
        text-shadow: 0 2px 30px rgba(212, 168, 83, 0.1);
    }
    .allocation-item .ticker {
        color: rgba(255, 255, 255, 0.1);
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        margin: 0.2rem 0 0 0;
        text-transform: uppercase;
        font-weight: 500;
        text-align: center;
    }

    /* ─── TABELLE ─── */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        overflow: hidden;
        margin: 0 auto 1rem auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .stDataFrame th {
        background: rgba(255, 255, 255, 0.03) !important;
        color: rgba(255, 255, 255, 0.2) !important;
        font-weight: 500 !important;
        font-size: 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.2em !important;
        text-align: center !important;
        padding: 0.8rem 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
    }
    .stDataFrame td {
        background: transparent !important;
        color: rgba(255, 255, 255, 0.6) !important;
        text-align: center !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.9rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important;
    }
    .stDataFrame tr:hover td {
        background: rgba(255, 255, 255, 0.03) !important;
    }
    .stDataFrame tr:last-child td {
        border-bottom: none !important;
    }

    /* ─── EXPANDER ─── */
    .streamlit-expanderHeader {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
        color: rgba(255, 255, 255, 0.15) !important;
        font-size: 0.65rem !important;
        letter-spacing: 0.12em;
        text-align: center;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem !important;
        margin: 0.5rem auto 0 auto;
        max-width: 320px;
        display: flex;
        justify-content: center;
        text-transform: uppercase;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.02) !important;
        border-color: rgba(212, 168, 83, 0.1) !important;
        color: rgba(255, 255, 255, 0.3) !important;
    }
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.01) !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.02) !important;
        border-top: none !important;
        padding: 0.8rem 1.2rem !important;
        color: rgba(255, 255, 255, 0.2) !important;
        font-size: 0.75rem !important;
        line-height: 1.8;
        text-align: center;
        max-width: 600px;
        margin: 0 auto;
    }
    .streamlit-expanderContent a {
        color: #D4A853 !important;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .streamlit-expanderContent a:hover {
        text-decoration: underline;
        color: #F5D98E !important;
    }

    /* ─── RESPONSIVE ─── */
    @media (max-width: 640px) {
        .allocation-grid { flex-direction: column; align-items: center; gap: 0.8rem; }
        .allocation-item { width: 100%; max-width: 200px; min-height: 120px; flex: none; }
        .main-title { font-size: 1.8rem; }
        .signal-box .signal-value { font-size: 1.8rem; }
        .main > div { padding: 3rem 1rem 3rem 1rem; }
        .stTabs [data-baseweb="tab"] { padding: 0.5rem 1.2rem !important; font-size: 0.7rem !important; }
        .title-wrapper { max-width: 100%; }
        .allocation-grid { max-width: 100%; }
    }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar { width: 3px; background: #0A0A0A; }
    ::-webkit-scrollbar-thumb { background: rgba(212, 168, 83, 0.2); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(212, 168, 83, 0.4); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. SPEICHER-FUNKTIONEN (unverändert)
# ============================================================
DATA_FILE = "manual_indicators.json"

def load_manual_values():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "Fear & Greed": None,
        "AAII Bull": None,
        "Put/Call Ratio": None,
        "GT50SPX": None,
        "GT200SPX": None,
        "NAHILO": None
    }

def save_manual_values(values):
    with open(DATA_FILE, "w") as f:
        json.dump(values, f)

# ============================================================
# 4. INDIKATOREN BEWERTEN (unverändert)
# ============================================================
def evaluate_indicators(indicators):
    scores = {}
    thresholds = {
        "Fear & Greed": {"oversold": 20, "overbought": 80},
        "AAII Bull": {"oversold": 25, "overbought": 55},
        "Put/Call Ratio": {"oversold": 0.75, "overbought": 1.25, "inverted": True},
        "GT50SPX": {"oversold": 20, "overbought": 80},
        "GT200SPX": {"oversold": 20, "overbought": 80},
        "NAHILO": {"oversold": 20, "overbought": 80},
    }
    
    for name, value in indicators.items():
        if value is None:
            scores[name] = 0
            continue
        if not isinstance(value, (int, float)):
            scores[name] = 0
            continue
        
        t = thresholds.get(name, {"oversold": 20, "overbought": 80})
        
        if name == "Put/Call Ratio":
            if value <= t["oversold"]:
                scores[name] = 1
            elif value >= t["overbought"]:
                scores[name] = -1
            else:
                scores[name] = 0
        else:
            if value <= t["oversold"]:
                scores[name] = -1
            elif value >= t["overbought"]:
                scores[name] = 1
            else:
                scores[name] = 0
    
    return scores

# ============================================================
# 5. ALLOKATION (unverändert)
# ============================================================
def get_allocation(scores):
    oversold = sum(1 for s in scores.values() if s == -1)
    overbought = sum(1 for s in scores.values() if s == 1)
    total = len(scores)
    
    if oversold >= 5:
        return {"growth": 70, "dividends": 20, "gold": 10}, "BULLISH", oversold, total
    elif overbought >= 5:
        return {"growth": 30, "dividends": 60, "gold": 10}, "BEARISH", oversold, total
    else:
        return {"growth": 50, "dividends": 40, "gold": 10}, "NEUTRAL", oversold, total

# ============================================================
# 6. SIDEBAR (unverändert)
# ============================================================
manual_values = load_manual_values()

st.sidebar.markdown("### Indikatoren")

fg_default = manual_values.get("Fear & Greed", 0.0) or 0.0
aaii_default = manual_values.get("AAII Bull", 0.0) or 0.0
pc_default = manual_values.get("Put/Call Ratio", 0.0) or 0.0
gt50_default = manual_values.get("GT50SPX", 0.0) or 0.0
gt200_default = manual_values.get("GT200SPX", 0.0) or 0.0
nahilo_default = manual_values.get("NAHILO", 0.0) or 0.0

fg_input = st.sidebar.number_input("Fear & Greed", min_value=0.0, max_value=100.0, value=float(fg_default), step=1.0, format="%.0f")
aaii_input = st.sidebar.number_input("AAII Bullish %", min_value=0.0, max_value=100.0, value=float(aaii_default), step=0.1, format="%.1f")
pc_input = st.sidebar.number_input("Put/Call Ratio", min_value=0.0, max_value=5.0, value=float(pc_default), step=0.01, format="%.2f")
gt50_input = st.sidebar.number_input("GT50SPX %", min_value=0.0, max_value=100.0, value=float(gt50_default), step=0.1, format="%.1f")
gt200_input = st.sidebar.number_input("GT200SPX %", min_value=0.0, max_value=100.0, value=float(gt200_default), step=0.1, format="%.1f")
nahilo_input = st.sidebar.number_input("NAHILO %", min_value=0.0, max_value=100.0, value=float(nahilo_default), step=0.1, format="%.1f")

if st.sidebar.button("Speichern"):
    values = {
        "Fear & Greed": fg_input,
        "AAII Bull": aaii_input,
        "Put/Call Ratio": pc_input,
        "GT50SPX": gt50_input,
        "GT200SPX": gt200_input,
        "NAHILO": nahilo_input
    }
    save_manual_values(values)
    st.sidebar.success("✅ Gespeichert")

indicators = {
    "Fear & Greed": fg_input if fg_input > 0 else None,
    "AAII Bull": aaii_input if aaii_input > 0 else None,
    "Put/Call Ratio": pc_input if pc_input > 0 else None,
    "GT50SPX": gt50_input if gt50_input > 0 else None,
    "GT200SPX": gt200_input if gt200_input > 0 else None,
    "NAHILO": nahilo_input if nahilo_input > 0 else None,
}

# ============================================================
# 7. DASHBOARD
# ============================================================
scores = evaluate_indicators(indicators)
allocation, signal_text, oversold, total = get_allocation(scores)

# ─── TABS ───
tab1, tab2 = st.tabs(["📊 Übersicht", "📋 Indikatoren"])

# ============================================================
# TAB 1: ÜBERSICHT
# ============================================================
with tab1:
    st.markdown("""
        <div class="title-wrapper">
            <h1 class="main-title">SMARTE <span>ETF ALLOKATION</span></h1>
        </div>
    """, unsafe_allow_html=True)

    # Signal
    if signal_text == "BULLISH":
        signal_color = "#4CAF50"
        signal_bg = "rgba(76, 175, 80, 0.06)"
    elif signal_text == "BEARISH":
        signal_color = "#EF5350"
        signal_bg = "rgba(239, 83, 80, 0.06)"
    else:
        signal_color = "#D4A853"
        signal_bg = "rgba(212, 168, 83, 0.06)"

    st.markdown(f"""
        <div class="signal-box" style="background: {signal_bg}; border-color: {signal_color}22;">
            <p class="signal-label">Marktsignal</p>
            <p class="signal-value" style="color: {signal_color};">{signal_text}</p>
            <p class="signal-detail">{oversold} von {total} Indikatoren oversold</p>
        </div>
    """, unsafe_allow_html=True)

    # Allokation
    st.markdown('<p class="section-title">Empfehlung für den Folgemonat</p>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="allocation-grid">
            <div class="allocation-item">
                <p class="label">🚀 Wachstum</p>
                <p class="value">{allocation['growth']}%</p>
                <p class="ticker">RPG</p>
            </div>
            <div class="allocation-item">
                <p class="label">💎 Dividenden</p>
                <p class="value">{allocation['dividends']}%</p>
                <p class="ticker">GLDV</p>
            </div>
            <div class="allocation-item">
                <p class="label">🥇 Gold</p>
                <p class="value">{allocation['gold']}%</p>
                <p class="ticker">SGLN</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Datenquellen
    with st.expander("📖 Datenquellen"):
        st.markdown("""
            <div style="text-align: center;">
                <strong>Fear & Greed</strong> – <a href="https://edition.cnn.com/markets/fear-and-greed" target="_blank">CNN</a><br>
                <strong>AAII Bullish</strong> – <a href="https://www.aaii.com/sentimentsurvey" target="_blank">AAII</a><br>
                <strong>Put/Call Ratio</strong> – <a href="https://stockcharts.com/" target="_blank">StockCharts</a> / <a href="https://www.cboe.com/" target="_blank">CBOE</a><br>
                <strong>GT50SPX, GT200SPX, NAHILO</strong> – <a href="https://stockcharts.com/" target="_blank">StockCharts</a> (<code>!GT50SPX</code>, <code>!GT200SPX</code>, <code>$NAHILO</code>)
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# TAB 2: INDIKATOREN
# ============================================================
with tab2:
    st.markdown('<p class="section-title" style="margin-top: 0;">Indikatoren-Übersicht</p>', unsafe_allow_html=True)

    data = []
    for name, value in indicators.items():
        if value is None:
            display_value = "—"
            status = "nicht verfügbar"
        else:
            score = scores.get(name, 0)
            if score == -1:
                status = "🟢 oversold"
            elif score == 1:
                status = "🔴 overbought"
            else:
                status = "🟡 neutral"
            
            if name == "Put/Call Ratio":
                display_value = f"{value:.2f}"
            else:
                display_value = f"{value:.1f} %"
        
        data.append({"Indikator": name, "Wert": display_value, "Signal": status})

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================
# SIDEBAR: ERKLÄRUNG
# ============================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### Wie funktioniert es?")

st.sidebar.markdown("""
1. **6 Indikatoren** monatlich auswerten.
2. Jeder Indikator:
   - 🟢 oversold
   - 🟡 neutral
   - 🔴 overbought
3. **5+ oversold** → 70/20/10
4. **5+ overbought** → 30/60/10
5. **Sonst** → 50/40/10
""")

st.sidebar.markdown("### Die ETFs")
st.sidebar.markdown("""
- **RPG** – Invesco S&P 500 Pure Growth  
- **GLDV** – SPDR S&P Global Dividend Aristocrats  
- **SGLN** – iShares Physical Gold ETC
""")

st.sidebar.markdown("---")
st.sidebar.caption(f"{datetime.now().strftime('%d.%m.%Y %H:%M')}")
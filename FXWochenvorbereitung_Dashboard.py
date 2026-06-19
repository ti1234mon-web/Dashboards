# fx_weekly_dashboard.py
import streamlit as st
import pandas as pd
import itertools

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="FX Wochenvorbereitung",
    page_icon="📊",
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
    .css-1d391kg, .css-1lcbmhc { background: rgba(10, 10, 10, 0.92) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.04) !important; }
    .sidebar .stMarkdown { color: rgba(255, 255, 255, 0.7) !important; }
    .sidebar h1, .sidebar h2, .sidebar h3 { color: #D4A853 !important; font-weight: 600 !important; }
    .sidebar .stSelectbox label { color: rgba(255, 255, 255, 0.25) !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.12em; }
    .sidebar .stSelectbox select { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; border-radius: 10px !important; color: #FFFFFF !important; padding: 0.4rem 0.75rem !important; }
    .sidebar .stTextArea label { color: rgba(255, 255, 255, 0.25) !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.12em; }
    .sidebar .stTextArea textarea { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; border-radius: 10px !important; color: #FFFFFF !important; padding: 0.4rem 0.75rem !important; }
    .sidebar .stButton > button { background: linear-gradient(135deg, #D4A853 0%, #B8923A 100%) !important; color: #0A0A0A !important; border: none !important; border-radius: 10px !important; padding: 0.5rem 2.2rem !important; font-weight: 700 !important; box-shadow: 0 4px 20px rgba(212, 168, 83, 0.15) !important; transition: all 0.3s ease; }
    .sidebar .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(212, 168, 83, 0.3) !important; background: linear-gradient(135deg, #E8C06A 0%, #D4A853 100%) !important; }
    
    .title-wrapper { display: flex; justify-content: center; width: 100%; margin: 0 auto 1.2rem auto; max-width: 700px; white-space: nowrap; }
    .main-title { font-size: 2.6rem; font-weight: 800; letter-spacing: 0.04em; text-align: center; margin: 0; color: #FFFFFF; line-height: 1.2; width: 100%; text-shadow: 0 2px 40px rgba(212, 168, 83, 0.05); white-space: nowrap; }
    .main-title span { background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    
    .section-headline { font-size: 1.1rem !important; font-weight: 500; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255, 255, 255, 0.35) !important; text-align: center; margin: 0; }
    
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
        <h1 class="main-title">📊 FX <span>WOCHENVORBEREITUNG</span></h1>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# 4. SIDEBAR: MANUELLE EINGABEN
# ============================================================

BIAS_OPTIONS = ["Bullish", "Eher Bullish", "Neutral", "Range", "Eher Bearish", "Bearish", "Profit Taking"]
BIAS_OPTIONS_SIMPLE = ["Bullish", "Bearish", "Neutral", "Range"]
BIAS_OPTIONS_FUNDAMENTAL = ["Bullish", "Eher Bullish", "Neutral", "Eher Bearish", "Bearish"]

G8_CURRENCIES = ["USD", "EUR", "GBP", "AUD", "NZD", "CHF", "JPY", "CAD"]

# ─── 1. NOTIZEN (FUNDAMENTAL) ───
st.sidebar.markdown("### 📝 1. Notizen (Fundamental)")

fundamental_notes = {}
fundamental_bias = {}
for ccy in G8_CURRENCIES:
    st.sidebar.markdown(f"**{ccy}**")
    fundamental_notes[ccy] = st.sidebar.text_area(
        f"Notizen {ccy}",
        key=f"fund_notes_{ccy}",
        height=60,
        placeholder=f"Wirtschaftsdaten, Reden, Events für {ccy}..."
    )
    fundamental_bias[ccy] = st.sidebar.selectbox(
        f"Bias {ccy}",
        options=BIAS_OPTIONS_FUNDAMENTAL,
        key=f"fund_bias_{ccy}"
    )

# ─── 2. INTERMARKET ───
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌍 2. Intermarket Bias")

oil_bias = st.sidebar.selectbox("Öl", options=BIAS_OPTIONS_SIMPLE, key="oil")
gold_bias = st.sidebar.selectbox("Gold", options=BIAS_OPTIONS_SIMPLE, key="gold")

st.sidebar.markdown("**Aktienindizes**")
indices = ["CAC40", "DAX40", "IBEX35", "FTSE100", "NIKKEI225", "NASDAQ", "S&P500", "ASX200"]
indices_bias = {}
for idx in indices:
    indices_bias[idx] = st.sidebar.selectbox(idx, options=BIAS_OPTIONS_SIMPLE, key=f"idx_{idx}")

st.sidebar.markdown("**Anleihen (10Y)**")
bonds = ["US10Y", "DE10Y", "GB10Y", "CH10Y", "CA10Y", "JP10Y", "AU10Y", "NZ10Y"]
bonds_bias = {}
for bond in bonds:
    bonds_bias[bond] = st.sidebar.selectbox(bond, options=BIAS_OPTIONS_SIMPLE, key=f"bond_{bond}")

# ─── 3. SENTIMENT ───
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 3. Sentiment (COT G8)")

sentiment_bias = {}
for ccy in G8_CURRENCIES:
    sentiment_bias[ccy] = st.sidebar.selectbox(
        f"{ccy}",
        options=BIAS_OPTIONS_SIMPLE,
        key=f"sent_{ccy}"
    )

st.sidebar.markdown("**Risk-On / Risk-Off**")
risk_on_off = st.sidebar.selectbox("Risk-On/Off", options=["Risk-On", "Risk-Off", "Neutral"], key="risk")

# ─── 4. ALLGEMEINER BIAS ───
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 4. Allgemeiner Bias")

general_bias = {}
for ccy in G8_CURRENCIES:
    general_bias[ccy] = st.sidebar.selectbox(
        f"{ccy}",
        options=BIAS_OPTIONS,
        key=f"gen_{ccy}"
    )

# ─── 5. SPEICHERN / AKTUALISIEREN ───
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Trades berechnen", use_container_width=True):
    st.session_state["calculate"] = True
else:
    if "calculate" not in st.session_state:
        st.session_state["calculate"] = False

# ============================================================
# 5. HAUPTBEREICH
# ============================================================

st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
        <p class="section-headline">Notizen (Fundamental)</p>
    </div>
""", unsafe_allow_html=True)

notes_data = []
for ccy in G8_CURRENCIES:
    notes_data.append({
        "Währung": ccy,
        "Bias": fundamental_bias[ccy],
        "Notizen": fundamental_notes[ccy][:80] + "..." if len(fundamental_notes[ccy]) > 80 else fundamental_notes[ccy]
    })
df_notes = pd.DataFrame(notes_data)
st.dataframe(df_notes, use_container_width=True, hide_index=True)

# ─── TRADE-SYNTHESE ───
if st.session_state.get("calculate", False):
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 4rem 0 1.5rem 0;">
            <p class="section-headline">🔥 Optimale Swing Trades (aus Allgemeinem Bias)</p>
        </div>
    """, unsafe_allow_html=True)

    # Mapping der Biases auf numerische Werte
    bias_map = {
        "Bullish": 3,
        "Eher Bullish": 2,
        "Neutral": 0,
        "Range": 0,
        "Eher Bearish": -2,
        "Bearish": -3,
        "Profit Taking": 0
    }

    # ---- ALLE PAARE AUS DEN G8-WÄHRUNGEN (56 Stück) ----
    # Reihenfolge für die Standard-Notation: USD als Basis für Major-Paare,
    # sonst alphabetisch oder nach Handelsvolumen.
    # Wir priorisieren: EUR, GBP, AUD, NZD, USD, CAD, CHF, JPY
    # (d.h. wenn beide Währungen in dieser Liste sind, wird die frühere als Basis genommen)
    priority = ["EUR", "GBP", "AUD", "NZD", "USD", "CAD", "CHF", "JPY"]

    def get_pair_name(ccy1, ccy2):
        # Bestimme, welche Währung als Basis (erste) genommen wird
        if priority.index(ccy1) < priority.index(ccy2):
            return f"{ccy1}{ccy2}", ccy1, ccy2
        else:
            return f"{ccy2}{ccy1}", ccy2, ccy1

    all_pairs = []
    for ccy1, ccy2 in itertools.combinations(G8_CURRENCIES, 2):
        pair_name, base, quote = get_pair_name(ccy1, ccy2)
        all_pairs.append((base, quote, pair_name))

    # Sortiere Paare nach Basiswährung (z.B. alle EUR-Paare zusammen)
    all_pairs.sort(key=lambda x: (priority.index(x[0]), priority.index(x[1])))

    # Trades berechnen
    trades = []
    for base, quote, pair in all_pairs:
        bias_base = general_bias.get(base, "Neutral")
        bias_quote = general_bias.get(quote, "Neutral")

        val_base = bias_map.get(bias_base, 0)
        val_quote = bias_map.get(bias_quote, 0)

        # Richtung basierend auf den Werten
        if val_base > 0 and val_quote <= 0:
            direction = "Long"
            grund = f"{base} {bias_base} + {quote} {bias_quote}"
        elif val_quote > 0 and val_base <= 0:
            direction = "Short"
            grund = f"{quote} {bias_quote} + {base} {bias_base}"
        elif val_base > 0 and val_quote > 0:
            if val_base > val_quote:
                direction = "Long + Range"
                grund = f"{base} stärker {bias_base} vs {quote} {bias_quote}"
            elif val_quote > val_base:
                direction = "Short + Range"
                grund = f"{quote} stärker {bias_quote} vs {base} {bias_base}"
            else:
                direction = "Range"
                grund = f"Beide {bias_base}"
        elif val_base < 0 and val_quote < 0:
            if val_base < val_quote:
                direction = "Short + Range"
                grund = f"{base} schwächer {bias_base} vs {quote} {bias_quote}"
            elif val_quote < val_base:
                direction = "Long + Range"
                grund = f"{quote} schwächer {bias_quote} vs {base} {bias_base}"
            else:
                direction = "Range"
                grund = f"Beide {bias_base}"
        elif val_base < 0 and val_quote == 0:
            direction = "Short + Range"
            grund = f"{base} {bias_base} + {quote} Range"
        elif val_quote < 0 and val_base == 0:
            direction = "Long + Range"
            grund = f"{quote} {bias_quote} + {base} Range"
        elif val_base == 0 and val_quote == 0:
            direction = "Range"
            grund = f"Beide Range / Neutral"
        else:
            direction = "Neutral"
            grund = f"Kein klarer Bias"

        # Emoji für Richtung
        if "Long" in direction:
            emoji = "🟢"
        elif "Short" in direction:
            emoji = "🔴"
        else:
            emoji = "🟡"

        trades.append({
            "Paar": pair,
            "Richtung": f"{emoji} {direction}",
            "Grund": grund
        })

    df_trades = pd.DataFrame(trades)

    # Alle 56 Paare in einer Tabelle anzeigen
    st.dataframe(df_trades, use_container_width=True, hide_index=True)

    # ─── ZUSAMMENFASSUNG DER BIASES ───
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 4rem 0 1.5rem 0;">
            <p class="section-headline">📊 Allgemeiner Bias pro Währung</p>
        </div>
    """, unsafe_allow_html=True)

    bias_data = []
    for ccy in G8_CURRENCIES:
        bias_data.append({
            "Währung": ccy,
            "Allgemeiner Bias": general_bias[ccy],
            "Fundamental": fundamental_bias[ccy],
            "Sentiment (COT)": sentiment_bias[ccy]
        })
    df_bias = pd.DataFrame(bias_data)
    st.dataframe(df_bias, use_container_width=True, hide_index=True)

    # ─── INTERMARKET ÜBERSICHT ───
    st.markdown("""
        <div style="display: flex; justify-content: center; width: 100%; margin: 4rem 0 1.5rem 0;">
            <p class="section-headline">🌍 Intermarket & Sentiment</p>
        </div>
    """, unsafe_allow_html=True)

    intermarket_data = []
    intermarket_data.append({"Asset": "Öl", "Bias": oil_bias})
    intermarket_data.append({"Asset": "Gold", "Bias": gold_bias})
    for idx, val in indices_bias.items():
        intermarket_data.append({"Asset": idx, "Bias": val})
    for bond, val in bonds_bias.items():
        intermarket_data.append({"Asset": bond, "Bias": val})
    intermarket_data.append({"Asset": "Risk-On/Off", "Bias": risk_on_off})

    df_intermarket = pd.DataFrame(intermarket_data)
    st.dataframe(df_intermarket, use_container_width=True, hide_index=True)

else:
    st.info("👈 Bitte alle Biases in der Sidebar eintragen und auf **'Trades berechnen'** klicken.")

# ─── SIDEBAR: HINWEIS ───
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Wie funktioniert es?")
st.sidebar.markdown("""
1. **Fundamental** – Notizen + Bias pro Währung
2. **Intermarket** – Bias für Rohstoffe, Aktien, Anleihen
3. **Sentiment** – COT G8 + Risk-On/Off
4. **Allgemeiner Bias** – deine finale Einschätzung
5. **Trades berechnen** – aus Allgemeinem Bias werden die optimalen Paare abgeleitet
""")

st.sidebar.caption("📅 Dashboard mit Streamlit")
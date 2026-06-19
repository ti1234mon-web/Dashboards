# immobilien_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Immobilien Pro-Forma",
    page_icon="🏗️",
    layout="wide"
)

# ============================================================
# 2. ULTRA LUXURY CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
    .stApp { background: linear-gradient(160deg, #0A0A0A 0%, #1A1A1A 35%, #222222 65%, #0A0A0A 100%); min-height: 100vh; }
    .stApp::before { content: ''; position: fixed; top: -20%; left: -20%; width: 140%; height: 140%; background: radial-gradient(ellipse at 40% 30%, rgba(212, 168, 83, 0.03) 0%, transparent 60%); pointer-events: none; z-index: 0; }
    .main > div { background: transparent; max-width: 1200px; margin: 0 auto; padding: 2.5rem 2rem 4rem 2rem; position: relative; z-index: 1; }
    .block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1200px; margin: 0 auto; }
    .css-1d391kg, .css-1lcbmhc { background: rgba(10, 10, 10, 0.92) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.04) !important; }
    .sidebar .stMarkdown { color: rgba(255, 255, 255, 0.7) !important; }
    .sidebar h1, .sidebar h2, .sidebar h3 { color: #D4A853 !important; font-weight: 600 !important; }
    .sidebar .stNumberInput label { color: rgba(255, 255, 255, 0.25) !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.12em; }
    .sidebar .stNumberInput input { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; border-radius: 10px !important; color: #FFFFFF !important; padding: 0.6rem 0.75rem !important; }
    .sidebar .stSlider label { color: rgba(255, 255, 255, 0.25) !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.12em; }
    .sidebar .stSlider .st-bk { background: rgba(212, 168, 83, 0.2) !important; }
    .sidebar .stSlider .st-bw { background: #D4A853 !important; }
    .sidebar .stButton > button { background: linear-gradient(135deg, #D4A853 0%, #B8923A 100%) !important; color: #0A0A0A !important; border: none !important; border-radius: 10px !important; padding: 0.5rem 2.2rem !important; font-weight: 700 !important; box-shadow: 0 4px 20px rgba(212, 168, 83, 0.15) !important; transition: all 0.3s ease; }
    .sidebar .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(212, 168, 83, 0.3) !important; background: linear-gradient(135deg, #E8C06A 0%, #D4A853 100%) !important; }
    
    /* ─── TITEL ─── */
    .title-wrapper {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 0 auto 1.2rem auto;
        max-width: 700px;
        white-space: nowrap;
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
        white-space: nowrap;
    }
    .main-title span {
        background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ─── METRIC CARDS ─── */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 0.8rem 0.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        flex: 1 1 0;
        min-width: 120px;
        max-width: 170px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-card:hover { border-color: rgba(212, 168, 83, 0.15); background: rgba(255, 255, 255, 0.04); transform: translateY(-2px); }
    .metric-card .label { color: rgba(255, 255, 255, 0.3); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.1rem; white-space: nowrap; }
    .metric-card .value { font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #D4A853 0%, #F5D98E 60%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.2; white-space: nowrap; }

    /* ─── TABELLE ─── */
    .stDataFrame { background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(8px); border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.04) !important; overflow: hidden; margin: 0 auto 1rem auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
    .stDataFrame th { background: rgba(255, 255, 255, 0.03) !important; color: rgba(255, 255, 255, 0.2) !important; font-weight: 500 !important; font-size: 0.6rem !important; text-transform: uppercase !important; letter-spacing: 0.2em !important; text-align: center !important; padding: 0.8rem 1rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame td { background: transparent !important; color: rgba(255, 255, 255, 0.8) !important; text-align: center !important; padding: 0.7rem 1rem !important; font-size: 0.9rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important; }
    .stDataFrame tr:hover td { background: rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame tr:last-child td { border-bottom: none !important; }

    /* ─── SECTION-ÜBERSCHRIFTEN (Flexbox) ─── */
    .section-headline {
        font-size: 1.1rem !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: rgba(255, 255, 255, 0.35) !important;
        text-align: center;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. DASHBOARD
# ============================================================

st.markdown("""
    <div class="title-wrapper">
        <h1 class="main-title">🏗️ IMMOBILIEN <span>PRO-FORMA</span></h1>
    </div>
""", unsafe_allow_html=True)

# ─── SIDEBAR: PARAMETER ───
st.sidebar.markdown("### ⚙️ Objektdaten")

purchase_price = st.sidebar.number_input(
    "💰 Kaufpreis (€)",
    min_value=50000,
    max_value=5000000,
    value=500000,
    step=5000,
    format="%d"
)

down_payment_pct = st.sidebar.slider(
    "💵 Anzahlung (%)",
    min_value=10,
    max_value=50,
    value=30,
    step=1
)

annual_rent = st.sidebar.number_input(
    "📈 Jahresbruttomiete (Jahr 1, €)",
    min_value=1000,
    max_value=50000000,
    value=28800,
    step=1000
)

rent_increase = st.sidebar.slider(
    "📈 Mietsteigerung pro Jahr (%)",
    min_value=0.0,
    max_value=10.0,
    value=5.0,
    step=0.5
) / 100

vacancy_pct = st.sidebar.slider(
    "🏚️ Leerstandsquote (%)",
    min_value=0,
    max_value=20,
    value=0,
    step=1
) / 100

expense_pct = st.sidebar.slider(
    "🔧 Bewirtschaftungskosten (%)",
    min_value=20,
    max_value=60,
    value=40,
    step=1
) / 100

annuity_rate = st.sidebar.number_input(
    "🏦 Annuitätszins (Darlehen) (%)",
    min_value=0.5,
    max_value=15.0,
    value=3.7,
    step=0.1,
    format="%.1f"
) / 100

holding_years = st.sidebar.slider(
    "📅 Betrachtungszeitraum (Jahre)",
    min_value=5,
    max_value=30,
    value=20,
    step=1
)

# ─── BERECHNUNGEN ───
down_payment = purchase_price * (down_payment_pct / 100)
debt = purchase_price - down_payment
ltv = debt / purchase_price

years = list(range(1, holding_years + 1))
gross_rent = []
vacancy = []
effective_income = []
expenses = []
noi = []
annuity = []
cash_flow = []
coc_return_pct = []

for i, year in enumerate(years):
    if i == 0:
        rent = annual_rent
    else:
        rent = annual_rent * (1 + rent_increase) ** i
    gross_rent.append(rent)
    vac = rent * vacancy_pct
    vacancy.append(vac)
    eff = rent - vac
    effective_income.append(eff)
    exp = rent * expense_pct
    expenses.append(exp)
    noi_val = eff - exp
    noi.append(noi_val)
    ann = debt * annuity_rate
    annuity.append(ann)
    cf = noi_val - ann
    cash_flow.append(cf)
    coc = (cf / down_payment) * 100 if down_payment > 0 else 0
    coc_return_pct.append(coc)

df = pd.DataFrame({
    "Jahr": years,
    "Bruttomiete": gross_rent,
    "Leerstand": vacancy,
    "Einnahmen": effective_income,
    "Ausgaben": expenses,
    "NOI": noi,
    "Annuität": annuity,
    "Cashflow": cash_flow,
    "CoC %": coc_return_pct
})

cap_rate = (noi[0] / purchase_price) * 100 if purchase_price > 0 else 0
dcr = noi[0] / annuity[0] if annuity[0] > 0 else 0

exit_years = [5, 10, 15, 20, holding_years]
exit_data = []
for y in exit_years:
    if y <= holding_years:
        cum_cf = sum(cash_flow[:y])
        exit_price = purchase_price + (2 * down_payment) + cum_cf
        exit_coc = (exit_price / down_payment) * 100 if down_payment > 0 else 0
        exit_data.append({
            "Exit nach (Jahre)": y,
            "Kumulierter CF": cum_cf,
            "Exit-Verkaufspreis": exit_price,
            "Exit CoC %": exit_coc
        })
    else:
        exit_data.append({
            "Exit nach (Jahre)": y,
            "Kumulierter CF": None,
            "Exit-Verkaufspreis": None,
            "Exit CoC %": None
        })
df_exit = pd.DataFrame(exit_data)

# ─── HAUPTBEREICH ───

# 1. KEY METRICS
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 0.1rem 0 1.5rem 0;">
        <p class="section-headline">Kennzahlen</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Kaufpreis</div>
            <div class="value">€{purchase_price:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Eigenkapital</div>
            <div class="value">€{down_payment:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Fremdkapital</div>
            <div class="value">€{debt:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">Cap Rate (J1)</div>
            <div class="value">{cap_rate:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">DCR (J1)</div>
            <div class="value">{dcr:.2f}x</div>
        </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">CoC Return (J1)</div>
            <div class="value">{coc_return_pct[0]:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

# 2. CASHFLOW-TABELLE
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 4rem 0 1.5rem 0;">
        <p class="section-headline">Jährlicher Cashflow</p>
    </div>
""", unsafe_allow_html=True)

df_display = df.copy()
for col in ["Bruttomiete", "Leerstand", "Einnahmen", "Ausgaben", "NOI", "Annuität", "Cashflow"]:
    df_display[col] = df_display[col].apply(lambda x: f"€{x:,.0f}")
df_display["CoC %"] = df_display["CoC %"].apply(lambda x: f"{x:.2f}%")

st.dataframe(df_display, use_container_width=True, hide_index=True)

# 3. EXIT-ANALYSE
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 2rem 0 1.5rem 0;">
        <p class="section-headline">Exit-Szenarien</p>
    </div>
""", unsafe_allow_html=True)

df_exit_display = df_exit.copy()
df_exit_display["Kumulierter CF"] = df_exit_display["Kumulierter CF"].apply(lambda x: f"€{x:,.0f}" if x else "-")
df_exit_display["Exit-Verkaufspreis"] = df_exit_display["Exit-Verkaufspreis"].apply(lambda x: f"€{x:,.0f}" if x else "-")
df_exit_display["Exit CoC %"] = df_exit_display["Exit CoC %"].apply(lambda x: f"{x:.2f}%" if x else "-")

st.dataframe(df_exit_display, use_container_width=True, hide_index=True)

# 4. VISUALISIERUNG
st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin: 2rem 0 1.5rem 0;">
        <p class="section-headline">Entwicklung</p>
    </div>
""", unsafe_allow_html=True)

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Bar(x=df["Jahr"], y=df["Cashflow"], name="Cashflow", marker_color="#D4A853"),
    secondary_y=False
)

fig.add_trace(
    go.Scatter(x=df["Jahr"], y=df["CoC %"], name="CoC Return %", mode="lines+markers", line=dict(color="#F5D98E", width=3)),
    secondary_y=True
)

fig.update_xaxes(
    title_text="Jahr",
    title_font=dict(color="rgba(255,255,255,0.4)", size=12),
    gridcolor="rgba(255,255,255,0.05)",
    title_standoff=15
)

fig.update_yaxes(
    title_text="Cashflow (€)",
    secondary_y=False,
    title_font=dict(color="rgba(255,255,255,0.4)", size=12),
    gridcolor="rgba(255,255,255,0.05)",
    title_standoff=15
)

fig.update_yaxes(
    title_text="CoC Return (%)",
    secondary_y=True,
    title_font=dict(color="rgba(255,255,255,0.4)", size=12),
    gridcolor="rgba(255,255,255,0.05)",
    title_standoff=15
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF"),
    showlegend=False,
    hovermode="x unified",
    height=400,
    margin=dict(l=30, r=30, t=10, b=30)
)

st.plotly_chart(fig, use_container_width=True)

# ─── SIDEBAR: ERKLÄRUNG ───
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Definitionen")
st.sidebar.markdown("""
- **NOI** – Net Operating Income (Einnahmen - Ausgaben)
- **Cap Rate** – NOI / Kaufpreis
- **DCR** – Debt Coverage Ratio (NOI / Annuität)
- **CoC** – Cash on Cash (Cashflow / Eigenkapital)
- **Exit CoC** – (Verkaufspreis + CF) / Eigenkapital
""")

st.sidebar.caption("📅 Dashboard mit Streamlit")
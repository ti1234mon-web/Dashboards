import streamlit as st

st.set_page_config(
    page_title="Dashboard Hub",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center; color: #DCA258;'>📊 DASHBOARD HUB</h1>
    <p style='text-align: center; color: rgba(255,255,255,0.4);'>Wähle ein Dashboard</p>
    <hr style='border-color: rgba(255,255,255,0.1);'>
""", unsafe_allow_html=True)

# ─── DASHBOARD-LISTE ───
dashboards = {
    "📈 ETF Allokation": "etf_dashboard.py",
    "📊 Anleihen-Scanner": "Anleihen_Dashboard.py",
    "🏗️ Immobilien Pro-Forma": "Immobilien_Dashboard.py",
    "📊 FX Wochenvorbereitung": "FXWochenvorbereitung_Dashboard.py",
    "₿ Bitcoin Langzeit": "bitcoin_longterm_dashboard.py",
}

# ─── KARTEN ANSICHT ───
cols = st.columns(3, gap="medium")

for i, (name, file) in enumerate(dashboards.items()):
    with cols[i % 3]:
        st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
                padding: 2rem 1rem;
                text-align: center;
                transition: all 0.3s ease;
                height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                <div style="font-size: 2.8rem;">{name.split()[0]}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 1.1rem; font-weight: 500; margin-top: 0.3rem;">{name}</div>
                <div style="color: rgba(255,255,255,0.15); font-size: 0.65rem; margin-top: 0.5rem;">{file}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🔓 Öffnen", key=f"btn_{i}"):
            st.switch_page(file)
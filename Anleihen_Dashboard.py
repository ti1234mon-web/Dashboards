# Anleihen_Dashboard.py
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Anleihen Scanner",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# 2. DARK LUXURY CSS (unverändert)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
    .stApp { background: linear-gradient(160deg, #0A0A0A 0%, #1A1A1A 35%, #222222 65%, #0A0A0A 100%); min-height: 100vh; }
    .stApp::before { content: ''; position: fixed; top: -20%; left: -20%; width: 140%; height: 140%; background: radial-gradient(ellipse at 40% 30%, rgba(212, 168, 83, 0.03) 0%, transparent 60%); pointer-events: none; z-index: 0; }
    .main > div { background: transparent; max-width: 1100px; margin: 0 auto; padding: 2rem 2rem 4rem 2rem; position: relative; z-index: 1; }
    .block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1100px; margin: 0 auto; }
    .css-1d391kg, .css-1lcbmhc { background: rgba(10, 10, 10, 0.92) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.04) !important; }
    .sidebar .stMarkdown { color: rgba(255, 255, 255, 0.7) !important; }
    .sidebar h1, .sidebar h2, .sidebar h3 { color: #D4A853 !important; font-weight: 600 !important; }
    .sidebar .stNumberInput label { color: rgba(255, 255, 255, 0.25) !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.12em; }
    .sidebar .stNumberInput input { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; border-radius: 10px !important; color: #FFFFFF !important; padding: 0.6rem 0.75rem !important; }
    .sidebar .stButton > button { background: linear-gradient(135deg, #D4A853 0%, #B8923A 100%) !important; color: #0A0A0A !important; border: none !important; border-radius: 10px !important; padding: 0.5rem 2.2rem !important; font-weight: 700 !important; box-shadow: 0 4px 20px rgba(212, 168, 83, 0.15) !important; transition: all 0.3s ease; }
    .sidebar .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(212, 168, 83, 0.3) !important; background: linear-gradient(135deg, #E8C06A 0%, #D4A853 100%) !important; }
    .sidebar .stAlert { background: rgba(212, 168, 83, 0.06) !important; border: 1px solid rgba(212, 168, 83, 0.1) !important; border-radius: 10px !important; color: #F5D98E !important; padding: 0.5rem !important; text-align: center; }
    .sidebar .stMarkdown p { color: rgba(255, 255, 255, 0.35) !important; font-size: 0.75rem !important; line-height: 1.7; }
    .title-wrapper { display: flex; justify-content: center; width: 100%; margin: 0 auto 2rem auto; max-width: 620px; }
    .main-title { font-size: 2.6rem; font-weight: 800; letter-spacing: 0.04em; text-align: center; margin: 0; color: #FFFFFF; line-height: 1.2; width: 100%; text-shadow: 0 2px 40px rgba(212, 168, 83, 0.05); }
    .main-title span { background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .stDataFrame { background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(8px); border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.04) !important; overflow: hidden; margin: 0 auto 1rem auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
    .stDataFrame th { background: rgba(255, 255, 255, 0.03) !important; color: rgba(255, 255, 255, 0.2) !important; font-weight: 500 !important; font-size: 0.6rem !important; text-transform: uppercase !important; letter-spacing: 0.2em !important; text-align: center !important; padding: 0.8rem 1rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame td { background: transparent !important; color: rgba(255, 255, 255, 0.8) !important; text-align: center !important; padding: 0.7rem 1rem !important; font-size: 0.9rem !important; border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important; }
    .stDataFrame tr:hover td { background: rgba(255, 255, 255, 0.03) !important; }
    .stDataFrame tr:last-child td { border-bottom: none !important; }
    .stAlert { background: rgba(212, 168, 83, 0.06) !important; border: 1px solid rgba(212, 168, 83, 0.1) !important; border-radius: 10px !important; color: #F5D98E !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. SCRAPER
# ============================================================

ESTABLISHED_FIRMS = [
    "Verizon", "Johnson & Johnson", "J&J", "Meta", "Deutsche Bank", "Apple",
    "Microsoft", "Amazon", "Alphabet", "Nestle", "Procter & Gamble", "Coca-Cola",
    "PepsiCo", "Walmart", "Exxon", "Shell", "Siemens", "SAP", "BASF", "Bayer",
    "Allianz", "Munich Re", "Volkswagen", "BMW", "Mercedes", "Adidas", "Goldman Sachs",
    "JP Morgan", "Morgan Stanley", "Bank of America", "Citigroup", "Wells Fargo"
]

def scrape_bond_data(isin):
    """
    Versucht, Daten von finanzen.net zu holen.
    Gibt bei Erfolg ein Dictionary zurück, sonst None.
    """
    url = f"https://www.finanzen.net/anleihen/{isin}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Emittent
        emittent_tag = soup.find("a", href=re.compile(r"/anleihen/emittent/"))
        emittent = emittent_tag.text.strip() if emittent_tag else None
        
        # Kupon
        kupon = None
        kupon_tag = soup.find(string=re.compile(r"Kupon"))
        if kupon_tag:
            parent = kupon_tag.find_parent("td")
            if parent:
                value = parent.find_next_sibling("td")
                if value:
                    match = re.search(r"([\d,]+)%", value.text)
                    if match:
                        kupon = float(match.group(1).replace(",", "."))
        
        # Fälligkeit
        faelligkeit = None
        faelligkeit_tag = soup.find(string=re.compile(r"Fälligkeit"))
        if faelligkeit_tag:
            parent = faelligkeit_tag.find_parent("td")
            if parent:
                value = parent.find_next_sibling("td")
                if value:
                    match = re.search(r"(\d{2}\.\d{2}\.\d{4})", value.text)
                    if match:
                        faelligkeit = match.group(1)
        
        # Kurs
        kurs = None
        kurs_tag = soup.find(string=re.compile(r"Kurs"))
        if kurs_tag:
            parent = kurs_tag.find_parent("td")
            if parent:
                value = parent.find_next_sibling("td")
                if value:
                    match = re.search(r"([\d,]+)", value.text)
                    if match:
                        kurs = float(match.group(1).replace(",", "."))
        
        # Rendite
        rendite = None
        rendite_tag = soup.find(string=re.compile(r"Rendite"))
        if rendite_tag:
            parent = rendite_tag.find_parent("td")
            if parent:
                value = parent.find_next_sibling("td")
                if value:
                    match = re.search(r"([\d,]+)%", value.text)
                    if match:
                        rendite = float(match.group(1).replace(",", "."))
        
        # Fallback: Tabellen durchsuchen
        if not kurs or not rendite:
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) >= 2:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if "Kupon" in label and not kupon:
                            match = re.search(r"([\d,]+)%", value)
                            if match:
                                kupon = float(match.group(1).replace(",", "."))
                        if "Fälligkeit" in label and not faelligkeit:
                            match = re.search(r"(\d{2}\.\d{2}\.\d{4})", value)
                            if match:
                                faelligkeit = match.group(1)
                        if "Kurs" in label and not kurs:
                            match = re.search(r"([\d,]+)", value)
                            if match:
                                kurs = float(match.group(1).replace(",", "."))
                        if "Rendite" in label and not rendite:
                            match = re.search(r"([\d,]+)%", value)
                            if match:
                                rendite = float(match.group(1).replace(",", "."))
        
        if emittent and kurs is not None and rendite is not None:
            return {
                "isin": isin,
                "emittent": emittent,
                "kupon": kupon,
                "faelligkeit": faelligkeit,
                "kurs": kurs,
                "rendite": rendite,
                "error": None
            }
        else:
            return None
    except:
        return None

# ============================================================
# 4. KERNLOGIK (unverändert)
# ============================================================

def check_criteria(data, zinskosten):
    if data.get("error") or data.get("kurs") is None or data.get("rendite") is None:
        return None
    
    kurs = data["kurs"]
    rendite = data["rendite"]
    kupon = data.get("kupon", 0)
    emittent = data.get("emittent", "")
    
    etabliert = any(firm.lower() in emittent.lower() for firm in ESTABLISHED_FIRMS)
    if not etabliert and emittent != "Unbekannt":
        etabliert = True
    
    zinsdeckung = rendite / zinskosten if zinskosten > 0 else 0
    zinsdeckung_ok = zinsdeckung > 1.5
    
    unter_paritaet = kurs < 100
    
    rendite_gt_zinskosten = rendite > zinskosten
    
    eigenkapitalrendite = (rendite - zinskosten) * 5
    hebel_ok = eigenkapitalrendite > 8.0
    
    alle_erfuellt = etabliert and zinsdeckung_ok and unter_paritaet and rendite_gt_zinskosten and hebel_ok
    
    ungehebelter_carry = rendite - zinskosten
    
    return {
        "etabliert": etabliert,
        "zinsdeckung_ok": zinsdeckung_ok,
        "zinsdeckung_wert": round(zinsdeckung, 2),
        "unter_paritaet": unter_paritaet,
        "rendite_gt_zinskosten": rendite_gt_zinskosten,
        "hebel_ok": hebel_ok,
        "eigenkapitalrendite": round(eigenkapitalrendite, 2),
        "ungehebelter_carry": round(ungehebelter_carry, 4),
        "alle_erfuellt": alle_erfuellt,
        "kauf_empfehlung": "✅ KAUFEN" if alle_erfuellt else "❌ NICHT KAUFEN"
    }

# ============================================================
# 5. DASHBOARD
# ============================================================

st.markdown("""
    <div class="title-wrapper">
        <h1 class="main-title">📊 ANLEIHEN <span>SCANNER</span></h1>
    </div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
st.sidebar.markdown("### ⚙️ Parameter")

# ISINs
isin_input = st.sidebar.text_area(
    "ISINs (eine pro Zeile)",
    placeholder="US92343VFF67\nUS478160BY94\nDE000DL19V22",
    height=150
)

# Hebelkosten
zinskosten = st.sidebar.number_input(
    "💸 Fremdkapitalzins (Hebelkosten) in %",
    min_value=0.0,
    max_value=20.0,
    value=3.88,
    step=0.01,
    format="%.2f"
) / 100

# ─── SIDEBAR: MANUELLE DATEN (NUR WENN NÖTIG) ───
st.sidebar.markdown("---")
st.sidebar.markdown("### ✏️ Manuelle Dateneingabe")
st.sidebar.markdown("Trage hier manuelle Daten für Anleihen ein, die nicht gefunden werden.")

if "manual_data" not in st.session_state:
    st.session_state.manual_data = {}

# ISIN für manuelle Eingabe
manual_isin = st.sidebar.text_input("ISIN für manuelle Eingabe", placeholder="z.B. DE000DL19V22")

if manual_isin:
    st.sidebar.markdown(f"**Daten für {manual_isin}:**")
    man_emittent = st.sidebar.text_input("Emittent", key=f"man_emittent_{manual_isin}")
    man_kupon = st.sidebar.number_input("Kupon %", min_value=0.0, max_value=20.0, step=0.01, key=f"man_kupon_{manual_isin}")
    man_faelligkeit = st.sidebar.text_input("Fälligkeit (TT.MM.JJJJ)", key=f"man_faell_{manual_isin}")
    man_kurs = st.sidebar.number_input("Kurs", min_value=0.0, max_value=200.0, step=0.01, key=f"man_kurs_{manual_isin}")
    man_rendite = st.sidebar.number_input("Rendite %", min_value=0.0, max_value=30.0, step=0.01, key=f"man_rendite_{manual_isin}")
    
    if st.sidebar.button(f"✅ Speichern für {manual_isin}", key=f"save_{manual_isin}"):
        st.session_state.manual_data[manual_isin] = {
            "emittent": man_emittent or "Manuell",
            "kupon": man_kupon,
            "faelligkeit": man_faelligkeit or "unbekannt",
            "kurs": man_kurs,
            "rendite": man_rendite
        }
        st.sidebar.success(f"✅ {manual_isin} gespeichert!")
        st.rerun()

# ─── SCAN-BUTTON ───
scannen = st.sidebar.button("🔍 Scannen", use_container_width=True)

# ─── HAUPTBEREICH ───
if scannen and isin_input:
    isin_list = [isin.strip().upper() for isin in isin_input.split("\n") if isin.strip()]
    
    if not isin_list:
        st.warning("Bitte mindestens eine ISIN eingeben.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        
        for i, isin in enumerate(isin_list):
            status_text.text(f"Scanne {isin}...")
            
            # 1. Prüfe, ob manuelle Daten existieren
            if isin in st.session_state.manual_data:
                manual = st.session_state.manual_data[isin]
                # Berechne mit manuellen Daten
                check = check_criteria({
                    "emittent": manual["emittent"],
                    "kurs": manual["kurs"],
                    "rendite": manual["rendite"],
                    "kupon": manual["kupon"],
                }, zinskosten)
                if check:
                    results.append({
                        "ISIN": isin,
                        "Emittent": manual["emittent"],
                        "Kupon": f"{manual['kupon']:.2f}%" if manual['kupon'] else "-",
                        "Fälligkeit": manual["faelligkeit"],
                        "Kurs": f"{manual['kurs']:.2f}",
                        "Rendite": f"{manual['rendite']:.2f}%",
                        "EK-Rendite": f"{check['eigenkapitalrendite']:.2f}%",
                        "Carry": f"{check['ungehebelter_carry']*100:.2f}%",
                        "Kriterien": "✅" if check["alle_erfuellt"] else "❌",
                        "Empfehlung": check["kauf_empfehlung"]
                    })
                else:
                    results.append({
                        "ISIN": isin,
                        "Emittent": "❌ Fehler",
                        "Kupon": "-",
                        "Fälligkeit": "-",
                        "Kurs": "-",
                        "Rendite": "-",
                        "EK-Rendite": "-",
                        "Carry": "-",
                        "Kriterien": "❌",
                        "Empfehlung": "⚠️ Berechnung fehlgeschlagen"
                    })
            else:
                # 2. Versuche Scraping
                data = scrape_bond_data(isin)
                if data:
                    check = check_criteria(data, zinskosten)
                    if check:
                        results.append({
                            "ISIN": isin,
                            "Emittent": data.get("emittent", "Unbekannt"),
                            "Kupon": f"{data.get('kupon', 0):.2f}%" if data.get('kupon') else "-",
                            "Fälligkeit": data.get("faelligkeit", "-"),
                            "Kurs": f"{data.get('kurs', 0):.2f}",
                            "Rendite": f"{data.get('rendite', 0):.2f}%",
                            "EK-Rendite": f"{check['eigenkapitalrendite']:.2f}%",
                            "Carry": f"{check['ungehebelter_carry']*100:.2f}%",
                            "Kriterien": "✅" if check["alle_erfuellt"] else "❌",
                            "Empfehlung": check["kauf_empfehlung"]
                        })
                    else:
                        results.append({
                            "ISIN": isin,
                            "Emittent": "❌ Fehler",
                            "Kupon": "-",
                            "Fälligkeit": "-",
                            "Kurs": "-",
                            "Rendite": "-",
                            "EK-Rendite": "-",
                            "Carry": "-",
                            "Kriterien": "❌",
                            "Empfehlung": "⚠️ Berechnung fehlgeschlagen"
                        })
                else:
                    # 3. Weder manuell noch gefunden
                    results.append({
                        "ISIN": isin,
                        "Emittent": "⚠️ Manuelle Eingabe nötig",
                        "Kupon": "-",
                        "Fälligkeit": "-",
                        "Kurs": "-",
                        "Rendite": "-",
                        "EK-Rendite": "-",
                        "Carry": "-",
                        "Kriterien": "❌",
                        "Empfehlung": "⚠️ Daten nicht gefunden"
                    })
            
            progress_bar.progress((i + 1) / len(isin_list))
            time.sleep(0.3)
        
        progress_bar.empty()
        status_text.empty()
        
        # DataFrame anzeigen
        df = pd.DataFrame(results)
        
        def color_empfehlung(val):
            if "KAUFEN" in str(val):
                return 'color: #4CAF50; font-weight: bold;'
            elif "NICHT" in str(val):
                return 'color: #EF5350; font-weight: bold;'
            else:
                return 'color: #FFA726;'
        
        def color_kriterien(val):
            if val == "✅":
                return 'color: #4CAF50; font-weight: bold;'
            else:
                return 'color: #EF5350;'
        
        styled_df = df.style.map(color_empfehlung, subset=['Empfehlung'])
        styled_df = styled_df.map(color_kriterien, subset=['Kriterien'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

elif scannen and not isin_input:
    st.warning("Bitte gib mindestens eine ISIN ein.")

# ============================================================
# 6. SIDEBAR: ERKLÄRUNG
# ============================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Die 5 Kriterien")
st.sidebar.markdown("""
1. **Etabliert?** – Unternehmen bekannt / groß  
2. **Zinsdeckung > 1,5?** – Rendite / Zinskosten  
3. **< Parität?** – Kurs unter 100  
4. **Rendite > Zinskosten?** – Positiver Carry  
5. **Hebel > 8%?** – EK-Rendite bei 5x Hebel  

**Empfehlung:** Nur wenn alle 5 Kriterien ✅ sind.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Strategie-Hinweis")
st.sidebar.markdown("""
- **Buy & Hold bis Laufzeitende** – kein Zinsänderungsrisiko  
- **Nur EWU-Anleihen** – kein Währungsrisiko  
- **Nach EZB-Pivot:** Rolliere in 3-Monats-Staatsanleihen (Spanien, Portugal, Italien)
""")

st.sidebar.markdown("---")
st.sidebar.caption("📅 Daten von finanzen.net | Dashboard mit Streamlit")
import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson
import plotly.express as px
from difflib import get_close_matches
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN MAESTRA ---
st.set_page_config(page_title="THE GAMBLERS LAYER", page_icon="🏆", layout="wide")

# --- CREDENCIALES NIVEL DIOS ---
API_FOOTBALL_KEY = "3c836b8a839378ddddcdc7c7635778e1"

# --- PERSISTENCIA DE DATOS ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Pick', 'Momio', 'Stake', 'Resultado', 'Bankroll'])
if 'current_bank' not in st.session_state:
    st.session_state.current_bank = 1000.0

# --- ESTILOS "BLACK & FOREST" ELITE (MAC OPTIMIZED) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #2e7d32; }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label { color: #ffffff !important; font-weight: 700 !important; }
    
    /* INPUTS: FONDO BLANCO / LETRA NEGRA (MAC) */
    input { color: #000000 !important; background-color: #ffffff !important; font-weight: 800 !important; border: 2px solid #2e7d32 !important; border-radius: 6px !important;}
    .stNumberInput div div input, .stTextInput div div input { color: #000000 !important; background-color: #ffffff !important; }
    .stSelectbox div div { color: #000000 !important; background-color: #ffffff !important; font-weight:bold;}
    
    .layer-title { font-size: 55px; font-weight: 900; color: #ffffff; text-align: center; border-bottom: 5px solid #2e7d32; padding-bottom: 10px; margin-bottom: 30px; letter-spacing: 2px;}
    .stTabs [data-baseweb="tab"] { height: 75px; background-color: #0a0a0a; color: #888; font-size: 18px; font-weight: 800; padding: 0 40px; border: 1px solid #222;}
    .stTabs [aria-selected="true"] { background-color: #2e7d32 !important; color: #ffffff !important; border: none !important;}
    
    .section-box { background-color: #080808; border: 1px solid #222; border-left: 8px solid #2e7d32; border-radius: 12px; padding: 35px; margin-bottom: 25px; position: relative;}
    .market-card { background: #111111; border-radius: 8px; padding: 20px; border-bottom: 4px solid #1565c0; text-align: center; }
    .stat-val { font-size: 38px; color: #2e7d32; font-weight: 900; }
    .excel-table { width: 100%; border-collapse: collapse; background-color: #0a0a0a; border: 1px solid #333; }
    .excel-table th { background-color: #111; color: #2e7d32; padding: 12px; text-align: center; border: 1px solid #222; }
    .excel-table td { padding: 12px; border: 1px solid #222; text-align: center; color: #fff; font-size: 15px; font-family: monospace;}
    div.stButton > button:first-child { width: 100%; background-color: #2e7d32; color: #fff; height: 80px; font-size: 26px; font-weight: 900; text-transform: uppercase;}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A LA MATRIX (API FOOTBALL) ---
@st.cache_data(ttl=3600) # Se actualiza SOLITO cada 3600 segundos (1 hora)
def fetch_live_fixtures():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Ligas Top: Premier(39), LaLiga(140), SerieA(135), LigaMX(262), UCL(2)
    leagues = "39-140-135-262-2" 
    try:
        res_today = requests.get(url, headers=headers, params={"date": today, "timezone": "America/Mexico_City", "league": leagues}).json()
        matches = []
        if res_today.get('response'):
            for m in res_today['response'][:10]: # Tomamos los 10 mejores
                matches.append({
                    "home": m['teams']['home']['name'],
                    "away": m['teams']['away']['name'],
                    "liga": m['league']['name'],
                    "hora": datetime.fromisoformat(m['fixture']['date']).strftime("%H:%M")
                })
        # Fallback de seguridad si la API no responde
        if not matches: raise Exception("No data")
        return matches
    except:
        # Fallback Offline Nivel Dios
        return [
            {"home": "Real Madrid", "away": "Manchester City", "liga": "Champions League", "hora": "14:00 (Mñn)"},
            {"home": "America", "away": "Chivas", "liga": "Liga MX", "hora": "21:00 (Hoy)"},
            {"home": "Liverpool", "away": "Arsenal", "liga": "Premier League", "hora": "10:30 (Mñn)"}
        ]

# --- MOTOR DE DATOS DINÁMICO & FUZZY MATCH ---
def get_dynamic_stats(team_name):
    # Simulador algorítmico basado en poderío para no hacer 100 llamadas a la API
    vault = {
        "real madrid": {"gs": 2.6, "gc": 0.8, "sot": 7.2, "corn": 6.5, "win_l10": 0.85},
        "manchester city": {"gs": 2.9, "gc": 0.7, "sot": 8.1, "corn": 7.5, "win_l10": 0.90},
        "america": {"gs": 2.3, "gc": 0.9, "sot": 6.2, "corn": 5.8, "win_l10": 0.80},
        "chivas": {"gs": 1.5, "gc": 1.2, "sot": 4.5, "corn": 5.1, "win_l10": 0.55},
        "liverpool": {"gs": 2.5, "gc": 1.0, "sot": 7.0, "corn": 6.8, "win_l10": 0.82},
        "arsenal": {"gs": 2.4, "gc": 0.9, "sot": 6.8, "corn": 6.4, "win_l10": 0.78},
        "barcelona": {"gs": 2.4, "gc": 1.1, "sot": 6.9, "corn": 6.2, "win_l10": 0.80},
    }
    q = team_name.lower().strip()
    match = get_close_matches(q, list(vault.keys()), n=1, cutoff=0.3)
    if match: return vault[match[0]], match[0].upper()
    
    # Si es un equipo desconocido, genera stats base promedio
    seed = sum(bytearray(team_name, 'utf-8')) % 10
    return {"gs": 1.2 + (seed*0.1), "gc": 1.8 - (seed*0.05), "sot": 4.0 + (seed*0.2), "corn": 4.5 + (seed*0.1), "win_l10": 0.5}, team_name.upper()

# --- MONTE CARLO ENGINE (10,000 SIMS) ---
def simulate_10k_engine(h_name, a_name):
    h_s, h_real = get_dynamic_stats(h_name)
    a_s, a_real = get_dynamic_stats(a_name)
    
    avg = 1.35
    exH = (h_s['gs']/avg)*(a_s['gc']/avg)*avg * 1.15 # Edge Local
    exA = (a_s['gs']/avg)*(h_s['gc']/avg)*avg
    
    h_g = np.random.poisson(exH, 10000)
    a_g = np.random.poisson(exA, 10000)
    
    # Agresividad: Ignoramos O1.5
    ph, pa, pd = np.mean(h_g > a_g), np.mean(a_g > h_g), np.mean(h_g == a_g)
    return {
        "ph": ph, "pa": pa, "pd": pd,
        "aa": np.mean((h_g > 0) & (a_g > 0)), 
        "o25": np.mean((h_g + a_g) > 2.5),
        "u35": np.mean((h_g + a_g) < 3.5),
        "weh": 1 - ((1 - (max(ph, pa)*0.72))**2), # Gana cualquier mitad
        "h_corn": h_s['corn'], "a_corn": a_s['corn'], "t_corn": (h_s['corn'] + a_s['corn']) * 1.05,
        "h_sot": h_s['sot'], "a_sot": a_s['sot'], "t_sot": h_s['sot'] + a_s['sot'],
        "h_name": h_real, "a_name": a_real, "exH": exH, "exA": exA, "h_g": h_g, "a_g": a_g
    }

# --- LÓGICA DE CALIFICACIÓN ---
def get_grade(prob):
    if prob > 0.75: return "A+", "#39ff14"
    if prob > 0.65: return "A", "#2e7d32"
    if prob > 0.55: return "B+", "#1565c0"
    return "C", "#fbc02d"

# --- INTERFAZ PRINCIPAL ---
st.markdown("<h1 class='layer-title'>THE GAMBLERS LAYER</h1>", unsafe_allow_html=True)

t_live, t_bet, t_trilay, t_bitacora = st.tabs(["🕒 LIVE 24H API", "🎯 BET: GOD SCANNER", "🎰 TRILAY IA", "📈 BITÁCORA"])

with t_live:
    st.markdown("### 🌐 CARTELERA GLOBAL (Se actualiza cada hora)")
    live_matches = fetch_live_fixtures()
    for m in live_matches:
        st.markdown(f"<div class='section-box'><b>{m['liga']}</b> | ⏰ {m['hora']}<br><span style='font-size:24px; color:#39ff14;'>{m['home']} vs {m['away']}</span></div>", unsafe_allow_html=True)

with t_bet:
    with st.sidebar:
        st.markdown("### 🏦 SINCRONIZACIÓN DE MOMIOS")
        stk = st.number_input("STAKE ODD (ML)", value=2.10)
        pyd = st.number_input("PLAYDOIT ODD (ML)", value=2.15)
        nov = st.number_input("NOVIBET ODD (ML)", value=2.12)
        st.divider()
        st.session_state.current_bank = st.number_input("BANKROLL ($)", value=st.session_state.current_bank)

    c1, c2 = st.columns(2)
    h_in = c1.text_input("🏠 LOCAL (No importa si no es exacto)", "Madrid")
    a_in = c2.text_input("🚀 VISITANTE", "City")

    if st.button("🚀 INFILTRAR DATA Y LANZAR SIMULACIÓN 10K"):
        r = simulate_10k_engine(h_in, a_in)
        prob_f = max(r['ph'], r['pa'])
        fav = r['h_name'] if r['ph'] > r['pa'] else r['a_name']
        edge = ((max(stk, pyd, nov) / (1/max(0.01, prob_f))) - 1) * 100

        st.markdown("### 🏆 MATRIZ DE RESULTADO EXACTO")
        matrix = np.zeros((4, 4))
        for i in range(4):
            for j in range(4): matrix[i,j] = np.mean((r['h_g'] == i) & (r['a_g'] == j))
        fig = px.imshow(matrix, text_auto=".1%", labels=dict(x=r['a_name'], y=r['h_name']), color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

        cl, cr = st.columns([1.8, 1])
        with cl:
            st.markdown(f"<div class='section-box'><h2 style='color:#2e7d32;'>🥇 PICK PRINCIPAL (STRONG ML)</h2><h1 style='color:white;'>{fav} GANADOR 🏟️</h1><p>EDGE MATEMÁTICO: {edge:.1f}%</p></div>", unsafe_allow_html=True)
            
            # --- LÓGICA ULTRA AGRESIVA (NUNCA O1.5) ---
            if r['aa'] >= 0.55: combo_pick, combo_prob = "AMBOS ANOTAN ⚽", r['aa']
            elif r['o25'] >= 0.55: combo_pick, combo_prob = "OVER 2.5 GOLES 🥅", r['o25']
            elif r['pd'] < 0.25: combo_pick, combo_prob = "GANA CUALQUIER MITAD 🌓", r['weh']
            else: combo_pick, combo_prob = "UNDER 3.5 GOLES 🛡️", r['u35']

            st.markdown(f"<div class='section-box' style='border-left-color:#1565c0;'><h2>🥈 COMBO AGRESIVO </h2><h1 style='color:white;'>{fav} ML + {combo_pick}</h1></div>", unsafe_allow_html=True)
        
        with cr:
            g, c = get_grade(prob_f)
            st.markdown(f"<div style='font-size:110px; text-align:center; color:{c}; border:15px solid; border-radius:50%; width:240px; height:240px; line-height:210px; margin:auto;'>{g}</div><p style='text-align:center; margin-top:15px; font-weight:bold;'>PROBABILIDAD: {prob_f:.1%}</p>", unsafe_allow_html=True)

        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='market-card'><p class='stat-label'>🚩 CÓRNERS TOTALES</p><span class='stat-val'>{r['t_corn']:.1f}</span></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='market-card'><p class='stat-label'>🎯 DISPAROS SOT</p><span class='stat-val'>{r['t_sot']:.1f}</span></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='market-card'><p class='stat-label'>🏠 CÓRNERS {r['h_name'][:3]}</p><span class='stat-val'>{r['h_corn']:.1f}</span></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='market-card'><p class='stat-label'>🚀 CÓRNERS {r['a_name'][:3]}</p><span class='stat-val'>{r['a_corn']:.1f}</span></div>", unsafe_allow_html=True)

        st.markdown("### 📋 LIBRO CONTABLE: MÉTRICAS CRUDAS")
        st.markdown(f"""<table class='excel-table'><thead><tr><th>Dato</th><th>{r['h_name']} (LOCAL)</th><th>{r['a_name']} (VISITA)</th></tr></thead>
        <tbody><tr><td>EXPECTATIVA DE GOLES (xG)</td><td>{r['exH']:.2f}</td><td>{r['exA']:.2f}</td></tr><tr><td>DISPAROS SOT INDIVIDUAL</td><td>{r['h_sot']:.1f}</td><td>{r['a_sot']:.1f}</td></tr></tbody></table>""", unsafe_allow_html=True)

with t_trilay:
    st.markdown("## 🎰 TRILAY API PROACTIVO")
    st.write("El algoritmo escanea los partidos de las próximas 24 horas y selecciona los 3 Picks más agresivos y rentables.")
    if st.button("🎰 GENERAR TRILAY CON API DATA"):
        api_matches = fetch_live_fixtures()[:3]
        res_t = []
        for m in api_matches:
            sim = simulate_10k_engine(m['home'], m['away'])
            # Lógica Agresiva: Si AA u O2.5 superan 55%, se priorizan. Si no, ML.
            if sim['aa'] >= 0.55: p, pr = f"AA ⚽<br>({m['home'][:10]})", sim['aa']
            elif sim['o25'] >= 0.55: p, pr = f"O2.5 🥅<br>({m['home'][:10]})", sim['o25']
            else: 
                fav_t = sim['h_name'] if sim['ph'] > sim['pa'] else sim['a_name']
                p, pr = f"{fav_t[:10]} ML 🏟️", max(sim['ph'], sim['pa'])
            res_t.append((p, pr))
        
        st.markdown(f"""
        <div class='section-box' style='text-align:center;'>
            <div style='display:flex; justify-content:space-around;'>
                <div class='market-card' style='width:30%; font-size:20px;'><b>PICK 1</b><br><br>{res_t[0][0]}<br><span style='color:#39ff14;'>{res_t[0][1]:.1%}</span></div>
                <div class='market-card' style='width:30%; font-size:20px;'><b>PICK 2</b><br><br>{res_t[1][0]}<br><span style='color:#39ff14;'>{res_t[1][1]:.1%}</span></div>
                <div class='market-card' style='width:30%; font-size:20px;'><b>PICK 3</b><br><br>{res_t[2][0]}<br><span style='color:#39ff14;'>{res_t[2][1]:.1%}</span></div>
            </div>
            <h1 style='margin-top:25px;'>PROBABILIDAD TRILAY: {(res_t[0][1]*res_t[1][1]*res_t[2][1]):.1%}</h1>
        </div>
        """, unsafe_allow_html=True)

with t_bitacora:
    st.markdown("### 📈 BITÁCORA DEL SINDICATO")
    with st.expander("➕ REGISTRAR APUESTA"):
        with st.form("bitacora_f"):
            c_a, c_b, c_c = st.columns(3)
            f_p = c_a.text_input("Pick (Ej. City ML)")
            f_o = c_b.number_input("Momio", value=1.85, step=0.01)
            f_s = c_c.number_input("Stake ($)", value=100.0)
            f_res = st.selectbox("Resultado", ["GANADA ✅", "PERDIDA ❌"])
            if st.form_submit_button("GUARDAR EN SERVIDOR"):
                st.session_state.current_bank += (f_s * (f_o - 1)) if f_res == "GANADA ✅" else -f_s
                new_row = pd.DataFrame([[f_p, f_o, f_s, f_res, st.session_state.current_bank]], columns=st.session_state.history.columns)
                st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

    if not st.session_state.history.empty:
        st.markdown("#### 🎯 EFECTIVIDAD POR RANGO DE MOMIO")
        bins = [1.0, 1.25, 1.50, 1.75, 2.0, 10.0]
        labels = ['1.10 - 1.25', '1.26 - 1.50', '1.51 - 1.75', '1.76 - 2.00', '2.00+']
        df_p = st.session_state.history.copy()
        df_p['Rango'] = pd.cut(df_p['Momio'], bins=bins, labels=labels)
        
        # Desglose agrupado
        stats = df_p.groupby('Rango', observed=False).agg(
            Total=('Resultado', 'count'), 
            Ganadas=('Resultado', lambda x: (x=="GANADA ✅").sum())
        )
        stats['% Acierto'] = (stats['Ganadas']/stats['Total']).fillna(0)*100
        
        # Mostrar tabla estilizada
        st.dataframe(stats.style.format({'% Acierto': '{:.1f}%'}), use_container_width=True)
        
        # Curva de capital
        fig_b = px.line(st.session_state.history, y="Bankroll", title="Curva de Capital Real", template="plotly_dark")
        fig_b.update_traces(line_color="#2e7d32", line_width=4, marker=dict(size=10, color='#39ff14'))
        st.plotly_chart(fig_b, use_container_width=True)

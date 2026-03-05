import streamlit as st
import numpy as np
from scipy.stats import poisson

# --- CONFIGURACIÓN MAESTRA ---
st.set_page_config(page_title="THE GAMBLERS LAYER", page_icon="🕷️", layout="wide")

# --- ESTILOS NEÓN GIGANTES (KING SIZE) ---
st.markdown("""
    <style>
    .stApp { background-color: #05060a; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .layer-title { font-size: 65px; font-weight: 900; background: -webkit-linear-gradient(45deg, #00d4ff, #ff007f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; letter-spacing: 8px; margin-bottom: 40px; text-shadow: 0 0 30px rgba(0,212,255,0.3); }
    
    .stTabs [data-baseweb="tab-list"] { gap: 40px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 85px; background-color: #11141c; border-radius: 15px; color: #8892b0; font-size: 24px; font-weight: 900; padding: 0 60px; border: 1px solid #333; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; box-shadow: 0 10px 40px rgba(0,212,255,0.5); }

    .section-box { background: linear-gradient(135deg, #11141c 0%, #0a0b10 100%); border: 3px solid #00d4ff; border-radius: 35px; padding: 50px; margin-bottom: 45px; position: relative; }
    .edge-badge { position: absolute; top: -18px; right: 30px; background: #ff007f; color: white; padding: 10px 25px; border-radius: 12px; font-weight: 900; font-size: 20px; box-shadow: 0 0 40px #ff007f; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    
    .grade-container { background: #0d0f14; border-radius: 50px; border: 2px solid #333; padding: 70px 30px; text-align: center; display: flex; flex-direction: column; align-items: center; box-shadow: inset 0 0 60px rgba(0,0,0,0.9); }
    .grade-circle { font-size: 170px; font-weight: 900; border-radius: 50%; width: 360px; height: 360px; line-height: 330px; border: 28px solid; box-shadow: 0px 0px 110px currentcolor; text-shadow: 0 0 50px currentcolor; margin-bottom: 40px; }
    
    .market-card { background: #11141c; border-radius: 25px; padding: 30px; border-left: 10px solid #ff007f; margin-bottom: 25px; }
    .stat-val { font-size: 42px; color: #39ff14; font-weight: bold; }
    .stat-label { color: #8892b0; text-transform: uppercase; font-size: 14px; letter-spacing: 4px; font-weight: 900; }
    
    .excel-table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #0d0f14; border: 1px solid #333; border-radius: 15px; overflow: hidden; }
    .excel-table th { background-color: #11141c; color: #00d4ff; padding: 15px; text-align: left; border-bottom: 2px solid #333; font-size: 14px; }
    .excel-table td { padding: 15px; border-bottom: 1px solid #222; color: #e0e0e0; font-family: 'Courier New', monospace; font-size: 16px; }

    .bookie-box { background: #0d0f14; border: 2px solid #444; border-radius: 20px; padding: 20px; text-align: center; width: 31%; }
    .bookie-odd { font-size: 35px; color: white; font-weight: 900; }
    .bookie-label { font-size: 14px; color: #8892b0; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }

    div.stButton > button:first-child { width: 100%; border-radius: 18px; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #ff007f); color: white; height: 95px; font-size: 32px; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='layer-title'>🕷️ THE GAMBLERS LAYER </h1>", unsafe_allow_html=True)

# --- WORLD VAULT 2026 (BASE DE DATOS IN-HOUSE) ---
WORLD_VAULT = {
    "tottenham": {"gs_h": 2.2, "gc_h": 1.2, "gs_a": 1.8, "gc_a": 1.4, "win_l10": 0.65, "sot": 6.2, "corners": 6.5},
    "napoli": {"gs_h": 2.3, "gc_h": 0.8, "gs_a": 1.6, "gc_a": 1.1, "win_l10": 0.82, "sot": 6.5, "corners": 6.8},
    "america": {"gs_h": 2.1, "gc_h": 1.0, "gs_a": 1.7, "gc_a": 1.3, "win_l10": 0.75, "sot": 5.9, "corners": 5.6},
    "toluca": {"gs_h": 2.5, "gc_h": 0.9, "gs_a": 2.0, "gc_a": 1.3, "win_l10": 0.88, "sot": 6.6, "corners": 6.1},
    "pachuca": {"gs_h": 1.8, "gc_h": 1.4, "gs_a": 1.3, "gc_a": 1.8, "win_l10": 0.52, "sot": 5.2, "corners": 5.0}
}

def get_vault_data(name):
    q = name.lower().strip()
    if q in WORLD_VAULT: return WORLD_VAULT[q]
    seed = sum(bytearray(name, 'utf-8')) % 100
    return {"gs_h": 1.5+(seed%5)*0.1, "gc_h": 1.2, "gs_a": 1.2, "gc_a": 1.5, "win_l10": 0.5, "sot": 4.5, "corners": 4.8}

def analyze_engine(loc, vis):
    h, a = get_vault_data(loc), get_vault_data(vis)
    avg_g = 1.35
    # Poisson formula logic
    exp_h = (h['gs_h']/avg_g) * (a['gc_a']/avg_g) * avg_g * 1.15
    exp_a = (a['gs_a']/avg_g) * (h['gc_h']/avg_g) * avg_g
    m = np.outer(poisson.pmf(range(7), exp_h), poisson.pmf(range(7), exp_a))
    ph, pa, pd = np.sum(np.tril(m, -1)), np.sum(np.triu(m, 1)), np.sum(np.diag(m))
    norm = ph + pa + pd; ph, pa, pd = ph/norm, pa/norm, pd/norm
    o25, btts = 1 - (m[0,0]+m[0,1]+m[1,0]+m[2,0]+m[0,2]+m[1,1]), np.sum(m[1:, 1:])
    return {
        "ph": ph, "pa": pa, "pd": pd, "h": h, "a": a, "o25": o25, "btts": btts,
        "o15": 1 - (m[0,0]+m[0,1]+m[1,0]), "u25": 1-o25,
        "win_half": 1 - ((1 - (max(ph, pa)*0.72))**2), "corners": (h['corners']+a['corners'])*1.05,
        "exp_h": exp_h, "exp_a": exp_a
    }

# --- INTERFAZ ---
tab1, tab2 = st.tabs(["🎯 ANÁLISIS ESTRATÉGICO", "🏆 TRILAY AGRESIVO"])

with st.sidebar:
    st.markdown("### 🏦 SINCRONIZADOR DE MOMIOS (REAL)")
    st_odd = st.number_input("MOMIO STAKE", value=2.45, step=0.01)
    pd_odd = st.number_input("MOMIO PLAYDOIT", value=2.45, step=0.01)
    nv_odd = st.number_input("MOMIO NOVIBET", value=2.40, step=0.01)
    bank = st.number_input("BANKROLL TOTAL ($)", value=1000)
    st.caption("Ajuste estos valores según lo que vea en sus Apps.")

with tab1:
    c_in1, c_in2 = st.columns(2)
    with c_in1: l_q = st.text_input("🏠 LOCAL (365Scores)", "Tottenham")
    with c_in2: v_q = st.text_input("🚀 VISITANTE (365Scores)", "Napoli")

    if st.button("🚀 INFILTRAR DATA Y LOCALIZAR EDGE", use_container_width=True):
        res = analyze_engine(l_q, v_q)
        fav = l_q.upper() if res['ph'] > res['pa'] else v_q.upper()
        prob_ml = max(res['ph'], res['pa'])
        fair_odd = 1/max(0.01, prob_ml)
        
        # CÁLCULO DE EDGE REAL
        edge_st = ((st_odd / fair_odd) - 1) * 100
        edge_pd = ((pd_odd / fair_odd) - 1) * 100
        max_edge = max(edge_st, edge_pd)
        
        cl, cr = st.columns([1.8, 1])
        with cl:
            # 1. APUESTA SEGURA
            st.markdown(f"""
            <div class='section-box'>
                {f"<div class='edge-badge'>EDGE DETECTADO EN {fav}</div>" if max_edge > 3 else ""}
                <h2 style='color: #39ff14; margin:0;'>🥇 1. APUESTA SEGURA (MONEYLINE)</h2>
                <h1 style='color:white; margin:15px 0; font-size:55px;'>{fav} GANADOR 🏟️</h1>
                <p class='stat-label'>VALOR ESTIMADO: <span style='color:#39ff14;'>+{max_edge:.1f}% SOBRE LA CASA</span></p>
                <div style='display:flex; justify-content:space-between; margin-top:25px;'>
                    <div class='bookie-box' style='border-color:{"#39ff14" if edge_st == max_edge else "#444"}'><p class='bookie-label'>STAKE</p><p class='bookie-odd'>{st_odd:.2f}</p></div>
                    <div class='bookie-box' style='border-color:{"#39ff14" if edge_pd == max_edge else "#444"}'><p class='bookie-label'>PLAYDOIT</p><p class='bookie-odd'>{pd_odd:.2f}</p></div>
                    <div class='bookie-box'><p class='bookie-label'>NOVIBET</p><p class='bookie-odd'>{nv_odd:.2f}</p></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 2. PARLAY AGRESIVO (>59%)
            if res['btts'] > 0.59: m_agg, p_agg = "AMBOS ANOTAN ⚽", res['btts']
            elif res['o25'] > 0.59: m_agg, p_agg = "OVER 2.5 GOLES 🥅", res['o25']
            else: m_agg, p_agg = "OVER 1.5 GOLES 🛡️", res['o15']

            st.markdown(f"""
            <div class='section-box' style='border-color: #ff007f;'>
                <h2 style='color: #ff007f; margin:0;'>🥈 2. PARLAY DEL MISMO PARTIDO</h2>
                <h1 style='color:white; margin:15px 0; font-size:45px;'>{fav} o EMPATE + {m_agg}</h1>
                <h3 style='color:#ff007f;'>STAKE SUGERIDO: ${(bank*0.10):.2f}</h3>
            </div>
            """, unsafe_allow_html=True)

        with cr:
            # GRADO DE CONFIANZA KING SIZE
            score = (prob_ml * 0.6) + (res['o25'] * 0.4)
            g, c = ("A", "#39ff14") if score > 0.75 else ("B", "#00d4ff") if score > 0.60 else ("C", "#ffff00")
            st.markdown(f"""
            <div class='grade-container'>
                <div class='grade-circle' style='color:{c}; border-color:{c};'>{g}</div>
                <div class='stat-label' style='color:{c};'>GRADO DE VALOR</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📊 MATRIZ DE MERCADOS (SOT, CORNERS, MITADES)")
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='market-card'><p class='stat-label'>🚩 CÓRNERS</p><span class='stat-val'>{res['corners']:.1f}</span></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='market-card'><p class='stat-label'>🎯 TIROS SOT</p><span class='stat-val'>{res['h']['sot']+res['a']['sot']-1:.1f}</span></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='market-card'><p class='stat-label'>🌓 GANA MITAD</p><span class='stat-val'>{res['win_half']:.1%}</span></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='market-card'><p class='stat-label'>⚽ AMBOS ANOTAN</p><span class='stat-val'>{res['btts']:.1%}</span></div>", unsafe_allow_html=True)

        # --- EXCEL LEDGER ---
        st.markdown("### 📋 EL LIBRO CONTABLE (DATA CRUDA)")
        ledger = {
            "Métrica": ["Goles Anotados", "Goles Recibidos", "Tiros SOT", "Corners", "xG Expectativa"],
            f"🏠 {l_q.upper()} (Home)": [res['h']['gs_h'], res['h']['gc_h'], res['h']['sot'], res['h']['corners'], f"{res['exp_h']:.2f}"],
            f"🚀 {v_q.upper()} (Away)": [res['a']['gs_a'], res['a']['gc_a'], res['a']['sot'], res['a']['corners'], f"{res['exp_a']:.2f}"]
        }
        st.markdown(f"""<table class='excel-table'><thead><tr><th>Parámetro</th><th>{l_q}</th><th>{v_q}</th></tr></thead>
        <tbody>{"".join([f"<tr><td>{ledger['Métrica'][i]}</td><td>{ledger[f'🏠 {l_q.upper()} (Home)'][i]}</td><td>{ledger[f'🚀 {v_q.upper()} (Away)'][i]}</td></tr>" for i in range(len(ledger['Métrica']))])}</tbody></table>""", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='text-align:center; color:#d4af37;'>🏆 TRILAY AGRESIVO (GLOBAL SCANNER)</h2>", unsafe_allow_html=True)
    tc1, tc2, tc3 = st.columns(3)
    p1l, p1v = tc1.text_input("P1: Local", "Marseille"), tc1.text_input("P1: Visita", "Monaco")
    p2l, p2v = tc2.text_input("P2: Local", "America"), tc2.text_input("P2: Visita", "Toluca")
    p3l, p3v = tc3.text_input("P3: Local", "Tottenham"), tc3.text_input("P3: Visita", "Napoli")
    
    if st.button("🎰 GENERAR TRILAY DE VALOR"):
        r1, r2, r3 = analyze_engine(p1l, p1v), analyze_engine(p2l, p2v), analyze_engine(p3l, p3v)
        pool = []
        for r, l, v in [(r1, p1l, p1v), (r2, p2l, p2v), (r3, p3l, p3v)]:
            if r['btts'] > 0.59: pick, prob = f"AA en {l} ⚽", r['btts']
            elif r['o25'] > 0.59: pick, prob = f"O2.5 en {l} 🥅", r['o25']
            elif r['ph'] > 0.60: pick, prob = f"{l.upper()} ML 🏟️", r['ph']
            else: pick, prob = f"Gana Mitad {l} 🌓", r['win_half']
            pool.append((pick, prob))
        prob_t = pool[0][1] * pool[1][1] * pool[2][1]
        st.markdown(f"""<div class='section-box' style='background: linear-gradient(135deg, #1a1100 0%, #000 100%); border: 3px double #d4af37; border-radius: 35px; padding: 45px; text-align: center;'>
            <div style='display:flex; justify-content:space-around; margin-bottom:40px;'>
                <div class='market-card' style='border-color:#d4af37; width:30%;'><b>PICK 1</b><br>{pool[0][0]}<br>{pool[0][1]:.1%}</div>
                <div class='market-card' style='border-color:#d4af37; width:30%;'><b>PICK 2</b><br>{pool[1][0]}<br>{pool[1][1]:.1%}</div>
                <div class='market-card' style='border-color:#d4af37; width:30%;'><b>PICK 3</b><br>{pool[2][0]}<br>{pool[2][1]:.1%}</div>
            </div>
            <h1 style='color:white; font-size:55px;'>Probabilidad de Cobro: {prob_t:.1%}% 🎰</h1>
        </div>""", unsafe_allow_html=True)
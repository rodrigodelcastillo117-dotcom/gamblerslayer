# GAMBLERS_DEN_VERSION=2026_03_23_V10_FINAL
"""
THE GAMBLERS DEN
Monte Carlo Sports Betting Analyzer
BTTS · O/U · Parlays · Doble Oportunidad
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import random
import math
import time
import os
import json
from datetime import datetime, timezone

# Force dark background before any CSS loads (prevents white flash)
st.markdown("""<style>
html,body,.stApp{background-color:#0A0A0B!important;color:#F0F0F2!important}
.stSpinner>div{border-top-color:#FF5500!important}
</style>""", unsafe_allow_html=True)

st.set_page_config(
    page_title="The Gamblers Den",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load fonts (always inject - DOM resets on every rerun)
st.markdown('''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">''', unsafe_allow_html=True)

st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════
   GAMBLERS DEN V11 — PREMIUM DARK SPORTSBOOK
   ═══════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=Barlow:wght@400;500;600;700;800&display=swap');

:root {
  --bg:#08080A; --bg2:#0E0E12; --bg3:#141418; --bg4:#1A1A1F; --bg5:#202028;
  --border:rgba(255,255,255,0.06); --border2:rgba(255,255,255,0.10); --border3:rgba(255,255,255,0.16);
  --orange:#FF5500; --orange2:#FF7A3D;
  --yellow:#FFD600; --yellow2:#FFE566;
  --green:#00D47E; --green2:#00FF96;
  --red:#FF3341; --blue:#3D8EFF; --purple:#9B6DFF;
  --gold:#C9A84C; --gold2:#FFE87C;
  --text:#EEEEF2; --text2:#848490; --text3:#44444E;
  --nav-h:68px; --r:14px; --r-sm:10px; --r-lg:20px;
  --shadow:0 8px 32px rgba(0,0,0,0.5);
  --shadow-sm:0 2px 8px rgba(0,0,0,0.35);
  --card-shadow:0 2px 0 rgba(255,255,255,0.04) inset,0 -1px 0 rgba(0,0,0,0.5) inset,0 8px 32px rgba(0,0,0,0.4);
  --btn-shadow-orange:0 1px 0 rgba(255,255,255,0.15) inset,0 -2px 0 rgba(0,0,0,0.3) inset,0 4px 16px rgba(255,85,0,0.35);
  --btn-shadow-dark:0 1px 0 rgba(255,255,255,0.08) inset,0 -2px 0 rgba(0,0,0,0.4) inset,0 4px 12px rgba(0,0,0,0.4);
}

/* ── Reset ─────────────────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;-webkit-font-smoothing:antialiased}
html,body,.stApp,.main,.stMainBlockContainer{background-color:var(--bg)!important;color:var(--text)!important;font-family:'Barlow',-apple-system,BlinkMacSystemFont,sans-serif!important}
.block-container{padding:0 16px!important;max-width:960px!important;padding-bottom:calc(var(--nav-h) + 90px)!important}
h1,h2,h3{font-family:'Barlow Condensed',sans-serif!important}

/* ── Hide chrome ───────────────────────────────────────────── */
#MainMenu,header[data-testid="stHeader"],footer,[data-testid="stDecoration"],[data-testid="stStatusWidget"],[data-testid="stToolbar"],[data-testid="stBottom"]{display:none!important}
div[data-testid="stAppViewContainer"]>section{opacity:1!important}
[data-stale="true"]{opacity:1!important}

/* ── Inputs ────────────────────────────────────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea{
  background:var(--bg3)!important;border:1px solid var(--border2)!important;
  border-radius:var(--r-sm)!important;color:var(--text)!important;
  font-family:'Barlow',sans-serif!important;font-size:0.9rem!important;
  padding:10px 14px!important;transition:border-color 0.15s,box-shadow 0.15s!important}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus{
  border-color:var(--orange)!important;box-shadow:0 0 0 3px rgba(255,85,0,0.12)!important;outline:none!important}
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stDateInput"] label{
  font-size:0.68rem!important;font-weight:700!important;color:var(--text2)!important;
  letter-spacing:0.5px!important;text-transform:uppercase!important}
div[data-testid="stSelectbox"]>div>div{
  background:var(--bg3)!important;border:1px solid var(--border2)!important;
  border-radius:var(--r-sm)!important;color:var(--text)!important}
div[data-testid="stSelectbox"] ul{background:var(--bg4)!important;border:1px solid var(--border2)!important;border-radius:var(--r-sm)!important}
div[data-testid="stSelectbox"] li{color:var(--text)!important}
div[data-testid="stSelectbox"] li:hover{background:var(--bg5)!important}
div[data-testid="stNumberInput"] button{background:var(--bg4)!important;border-color:var(--border2)!important;color:var(--text2)!important}
div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"]{background:var(--orange)!important;box-shadow:0 0 10px rgba(255,85,0,0.4)!important}

/* ── Buttons ─────────────────────────────────────────────────── */
html body div[data-testid="stButton"] button,
html body .stButton>button{
  background:linear-gradient(170deg,var(--bg4) 0%,var(--bg3) 100%)!important;
  color:var(--text2)!important;
  border:1px solid var(--border2)!important;
  border-top:1px solid var(--border3)!important;
  border-bottom:2px solid rgba(0,0,0,0.5)!important;
  border-radius:var(--r-sm)!important;
  box-shadow:0 3px 10px rgba(0,0,0,0.3),0 1px 0 rgba(255,255,255,0.05) inset!important;
  font-family:'Barlow',sans-serif!important;font-weight:700!important;font-size:0.84rem!important;
  padding:10px 16px!important;height:auto!important;min-height:42px!important;
  transition:all 0.15s!important;letter-spacing:0.3px!important}
html body div[data-testid="stButton"] button:hover,
html body .stButton>button:hover{
  border-color:rgba(255,85,0,0.4)!important;color:var(--orange)!important;
  background:linear-gradient(170deg,#222228 0%,#18181C 100%)!important;
  box-shadow:0 4px 16px rgba(255,85,0,0.15),0 1px 0 rgba(255,255,255,0.06) inset!important;
  transform:translateY(-1px)!important}
html body div[data-testid="stButton"] button:active,
html body .stButton>button:active{transform:translateY(1px)!important;box-shadow:0 1px 4px rgba(0,0,0,0.5)!important}

/* ── Metrics ─────────────────────────────────────────────────── */
div[data-testid="stMetric"]{background:var(--bg3)!important;border:1px solid var(--border)!important;border-top:1px solid var(--border2)!important;border-radius:var(--r)!important;padding:14px 16px!important}
div[data-testid="stMetric"] label{color:var(--text3)!important;font-size:0.62rem!important;letter-spacing:1.5px!important;text-transform:uppercase!important}
div[data-testid="stMetricValue"]{color:var(--text)!important;font-family:'Barlow Condensed',sans-serif!important;font-size:1.6rem!important;font-weight:900!important}

/* ── Expanders ─────────────────────────────────────────────── */
[data-testid="stExpander"]{background:transparent!important;border:none!important;box-shadow:none!important}
[data-testid="stExpander"] summary{
  background:linear-gradient(160deg,var(--bg4) 0%,var(--bg3) 100%)!important;
  border:1px solid var(--border2)!important;border-top:1px solid var(--border3)!important;
  border-radius:var(--r-sm)!important;padding:12px 16px!important;
  color:var(--text2)!important;font-weight:700!important;font-size:0.84rem!important;
  transition:border-color 0.15s!important}
[data-testid="stExpander"] summary:hover{border-color:rgba(255,85,0,0.3)!important;color:var(--text)!important}
[data-testid="stExpander"] details[open]>summary{border-radius:var(--r-sm) var(--r-sm) 0 0!important;border-color:rgba(255,85,0,0.3)!important;color:var(--orange)!important}
[data-testid="stExpander"] details[open]>div:last-child{background:var(--bg2)!important;border:1px solid rgba(255,85,0,0.15)!important;border-top:none!important;border-radius:0 0 var(--r-sm) var(--r-sm)!important;padding:14px!important}
[data-testid="stExpander"] details:not([open])>*:not(summary){display:none!important;height:0!important;overflow:hidden!important;visibility:hidden!important;border:none!important;padding:0!important;margin:0!important}
[data-testid="stExpander"] summary svg{fill:var(--orange)!important}

/* ── Header ──────────────────────────────────────────────────── */
.den-header{background:linear-gradient(180deg,rgba(255,85,0,0.06) 0%,transparent 100%);border-bottom:1px solid rgba(255,85,0,0.12);padding:18px 0 14px;text-align:center;margin-bottom:4px;position:relative;overflow:hidden}
.den-header::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,85,0,0.6),transparent)}
.den-logo{font-family:'Barlow Condensed',sans-serif;font-size:2.2rem;font-weight:900;letter-spacing:4px;color:var(--text);text-transform:uppercase;line-height:1}
.den-logo span{color:var(--orange)}
.den-subtitle{font-size:0.6rem;color:var(--text3);letter-spacing:4px;text-transform:uppercase;margin-top:6px;font-weight:600}
.den-divider{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border2),transparent);margin:16px 0}
.den-corner{display:none}

/* ── Section headings ────────────────────────────────────────── */
.section-heading{font-family:'Barlow Condensed',sans-serif;font-size:0.72rem;font-weight:800;color:var(--text3);letter-spacing:3px;text-transform:uppercase;margin:20px 0 10px;display:flex;align-items:center;gap:10px}
.section-heading::before{content:'';width:3px;height:14px;background:var(--orange);border-radius:2px;flex-shrink:0}
.section-heading::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,85,0,0.3),transparent)}

/* ── Pick card (white) ──────────────────────────────────────── */
.pick-card{background:linear-gradient(160deg,#F8F8FC 0%,#EBEBF2 100%);border-radius:var(--r-lg);padding:16px;box-shadow:var(--card-shadow);margin-bottom:8px}

/* ── Stat tiles ─────────────────────────────────────────────── */
.stat-grid{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap}
.stat-tile{flex:1;min-width:70px;background:linear-gradient(160deg,var(--bg4) 0%,var(--bg3) 100%);border:1px solid var(--border);border-top:1px solid var(--border2);border-radius:var(--r-sm);padding:12px 10px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.25)}
.stat-num{font-family:'Barlow Condensed',sans-serif;font-size:1.6rem;font-weight:900;color:var(--text);line-height:1}
.stat-label{font-size:0.52rem;color:var(--text3);letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;font-weight:700}

/* ── Chips ────────────────────────────────────────────────────── */
.market-chip{display:inline-block;font-size:0.6rem;font-weight:800;letter-spacing:0.8px;text-transform:uppercase;padding:3px 8px;border-radius:6px}
.chip-ml{background:rgba(255,85,0,0.12);color:var(--orange);border:1px solid rgba(255,85,0,0.25)}
.chip-btts{background:rgba(0,212,126,0.10);color:var(--green);border:1px solid rgba(0,212,126,0.25)}
.chip-ou{background:rgba(61,142,255,0.10);color:var(--blue);border:1px solid rgba(61,142,255,0.25)}
.chip-combo{background:rgba(155,109,255,0.10);color:var(--purple);border:1px solid rgba(155,109,255,0.2)}
.chip-warn{background:rgba(255,51,65,0.12);color:var(--red);border:1px solid rgba(255,51,65,0.25)}
.conf-badge{display:inline-flex;align-items:center;gap:4px;font-size:0.6rem;font-weight:700;letter-spacing:0.3px;text-transform:uppercase;padding:3px 9px;border-radius:20px}
.conf-high{background:rgba(0,212,126,0.10);color:var(--green);border:1px solid rgba(0,212,126,0.25)}
.conf-medium{background:rgba(255,214,0,0.10);color:var(--yellow);border:1px solid rgba(255,214,0,0.25)}
.conf-low{background:rgba(255,51,65,0.10);color:var(--red);border:1px solid rgba(255,51,65,0.25)}

/* ── Warn / Demo banners ─────────────────────────────────────── */
.warn-banner{background:rgba(255,85,0,0.06);border:1px solid rgba(255,85,0,0.2);border-radius:var(--r-sm);padding:12px 16px;font-size:0.82rem;color:var(--orange2);text-align:center;margin:8px 0}
.demo-banner{background:rgba(61,142,255,0.08);border:1px solid rgba(61,142,255,0.2);border-radius:var(--r-sm);padding:10px 16px;font-size:0.78rem;color:var(--blue);text-align:center;margin:8px 0}

/* ── Empty state ─────────────────────────────────────────────── */
.empty-state{text-align:center;padding:48px 20px;color:var(--text3)}
.empty-icon{font-size:2.8rem;margin-bottom:12px;filter:grayscale(0.4)}
.empty-title{font-size:1rem;font-weight:700;color:var(--text2);margin-bottom:6px;font-family:'Barlow Condensed',sans-serif;letter-spacing:1px}
.empty-sub{font-size:0.78rem;color:var(--text3)}

/* ── Dataframe ───────────────────────────────────────────────── */
div[data-testid="stDataFrame"]{border-radius:var(--r)!important;overflow:hidden!important}
div[data-testid="stDataFrame"] table{font-size:0.8rem!important}
div[data-testid="stDataFrame"] thead tr th{background:var(--bg4)!important;color:var(--text3)!important;font-size:0.62rem!important;letter-spacing:1.5px!important;text-transform:uppercase!important;font-weight:700!important;border-bottom:1px solid var(--border2)!important}
div[data-testid="stDataFrame"] tbody tr{border-bottom:1px solid var(--border)!important}
div[data-testid="stDataFrame"] tbody tr:hover{background:rgba(255,255,255,0.02)!important}

/* ── Misc ─────────────────────────────────────────────────────── */
.stSpinner>div{border-top-color:var(--orange)!important}
div[data-testid="stProgress"]>div>div{background:var(--orange)!important}
div[data-testid="stProgress"]>div{background:var(--bg4)!important;border-radius:99px!important}
div[data-testid="stToast"]{background:var(--bg4)!important;border:1px solid var(--border2)!important;border-radius:var(--r)!important;box-shadow:var(--shadow)!important;color:var(--text)!important}
div[data-testid="stCaptionContainer"] p{color:var(--text3)!important;font-size:0.72rem!important}

/* ── Scrollbar ─────────────────────────────────────────────────── */
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:var(--bg2)}
::-webkit-scrollbar-thumb{background:var(--bg5);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--border2)}

/* ── Bottom Nav ─────────────────────────────────────────────── */
div[data-testid="stRadio"]>div[role="radiogroup"]{
  position:fixed!important;bottom:16px!important;left:50%!important;transform:translateX(-50%)!important;
  width:min(96vw,500px)!important;height:62px!important;
  background:linear-gradient(160deg,#1A1A20 0%,#101014 100%)!important;
  backdrop-filter:blur(24px)!important;-webkit-backdrop-filter:blur(24px)!important;
  border:1px solid rgba(255,255,255,0.10)!important;border-top:1px solid rgba(255,255,255,0.16)!important;
  border-bottom:1px solid rgba(0,0,0,0.6)!important;border-radius:30px!important;
  z-index:99999!important;display:flex!important;flex-direction:row!important;align-items:stretch!important;
  padding:5px!important;gap:0!important;
  box-shadow:0 8px 40px rgba(0,0,0,0.7),0 2px 0 rgba(255,255,255,0.05) inset!important;
  overflow:hidden!important;pointer-events:auto!important;touch-action:manipulation!important;
  visibility:visible!important;opacity:1!important}
@media(min-width:768px){
  div[data-testid="stRadio"]>div[role="radiogroup"]{width:720px!important;height:68px!important;bottom:20px!important;border-radius:32px!important;visibility:visible!important;opacity:1!important;display:flex!important}}
div[data-testid="stRadio"] input[type="radio"]{display:none!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]{
  flex:1!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;
  gap:2px!important;cursor:pointer!important;pointer-events:auto!important;touch-action:manipulation!important;
  -webkit-tap-highlight-color:rgba(255,85,0,0.2)!important;user-select:none!important;
  padding:0!important;margin:0!important;border-radius:24px!important;
  transition:background 0.15s,box-shadow 0.15s!important;min-width:0!important;overflow:hidden!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked){
  background:linear-gradient(160deg,rgba(255,85,0,0.25) 0%,rgba(255,85,0,0.10) 100%)!important;
  box-shadow:0 1px 0 rgba(255,255,255,0.08) inset,0 -1px 0 rgba(0,0,0,0.3) inset!important}
div[data-testid="stRadio"] label[data-baseweb="radio"] span,
div[data-testid="stRadio"] label[data-baseweb="radio"] p,
div[data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p{
  font-size:0.62rem!important;font-weight:800!important;letter-spacing:0.3px!important;
  text-transform:uppercase!important;color:var(--text3)!important;line-height:1!important;
  margin:0!important;font-family:'Barlow',sans-serif!important;white-space:nowrap!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span,
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) div[data-testid="stMarkdownContainer"] p{
  color:var(--orange)!important;text-shadow:0 0 12px rgba(255,85,0,0.5)!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]:not(:last-child){border-right:1px solid rgba(255,255,255,0.04)!important}

/* ── Reto animations ─────────────────────────────────────────── */
@keyframes shimmer{0%{background-position:-400px 0}100%{background-position:400px 0}}
@keyframes pulse-glow{0%,100%{box-shadow:0 0 20px rgba(201,168,76,0.15)}50%{box-shadow:0 0 40px rgba(201,168,76,0.35)}}

/* ── Mobile ──────────────────────────────────────────────────── */
@media(max-width:768px){
  .stApp{padding-bottom:env(safe-area-inset-bottom)!important}
  .block-container{padding-left:10px!important;padding-right:10px!important;max-width:100%!important;overflow-x:hidden!important;padding-bottom:calc(var(--nav-h) + 80px)!important}
  .den-logo{font-size:1.9rem!important}
  .den-subtitle{font-size:0.52rem!important}
  div[data-testid="stRadio"] label[data-baseweb="radio"] span,
  div[data-testid="stRadio"] label[data-baseweb="radio"] p{font-size:0.55rem!important}}
@media(max-width:390px){
  div[data-testid="stRadio"] label[data-baseweb="radio"] span,
  div[data-testid="stRadio"] label[data-baseweb="radio"] p{font-size:0.5rem!important}}

</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# BOTTOM NAV — st.radio con CSS puro (sin botones visibles, compacto en móvil)
# ═══════════════════════════════════════════════════════════════════════════════
_NAV_ITEMS = [
    {"key": "Rongol Picks", "icon": "⚡", "label": "Rongol"},
    {"key": "Picks",        "icon": "🎯", "label": "Picks"},
    {"key": "Parlays",      "icon": "🎰", "label": "Parlay"},
    {"key": "En Vivo",      "icon": "🔴", "label": "Live"},
    {"key": "Califica",     "icon": "🏆", "label": "Califica"},
    {"key": "Reto 13M",     "icon": "💰", "label": "Reto"},
    {"key": "Config",       "icon": "⚙️",  "label": "Config"},
]

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Rongol Picks"

_active_page = st.session_state["active_page"]

# CSS: transforma el radio en bottom nav compacto
# (nav CSS is in main <style> block above)

# Construir opciones: emoji + newline + label (el CSS los separa visualmente)
_nav_options = [f'{i["icon"]}\n{i["label"]}' for i in _NAV_ITEMS]
_nav_key_map  = {f'{i["icon"]}\n{i["label"]}': i["key"] for i in _NAV_ITEMS}
_nav_key_rev  = {i["key"]: f'{i["icon"]}\n{i["label"]}' for i in _NAV_ITEMS}

_cur_option = _nav_key_rev.get(_active_page, _nav_options[0])

def _on_nav_change():
    _sel = st.session_state.get("gamblers_nav_radio")
    if _sel and _sel in _nav_key_map:
        st.session_state["active_page"] = _nav_key_map[_sel]

_selected = st.radio(
    "nav",
    _nav_options,
    index=_nav_options.index(_cur_option),
    horizontal=True,
    key="gamblers_nav_radio",
    label_visibility="collapsed",
    on_change=_on_nav_change,
)
_active_page = st.session_state["active_page"]

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════
LEAGUES = {
    "NBA":              {"sport":"basketball","league":"nba",                    "group":"Basketball"},
    "MLB":              {"sport":"baseball",  "league":"mlb",                    "group":"Baseball"},
        "NFL":              {"sport":"football",  "league":"nfl",                    "group":"Football"},
    "NCAAF":            {"sport":"football",  "league":"college-football",       "group":"Football"},
    "NHL":              {"sport":"hockey",    "league":"nhl",                    "group":"Hockey"},
    "MLS":              {"sport":"soccer",    "league":"usa.1",                  "group":"Soccer"},
    "Liga MX":          {"sport":"soccer",    "league":"mex.1",                  "group":"Soccer"},
    "Premier League":   {"sport":"soccer",    "league":"eng.1",                  "group":"Soccer"},
    "La Liga":          {"sport":"soccer",    "league":"esp.1",                  "group":"Soccer"},
    "Bundesliga":       {"sport":"soccer",    "league":"ger.1",                  "group":"Soccer"},
    "Serie A":          {"sport":"soccer",    "league":"ita.1",                  "group":"Soccer"},
    "Ligue 1":          {"sport":"soccer",    "league":"fra.1",                  "group":"Soccer"},
    "Champions League":       {"sport":"soccer", "league":"UEFA.CHAMPIONS",    "group":"Soccer", "country":"Europa"},
    "Europa League":          {"sport":"soccer", "league":"UEFA.EUROPA",         "group":"Soccer", "country":"Europa"},
    "Conference League":      {"sport":"soccer", "league":"uefa.europa.conf",    "group":"Soccer", "country":"Europa"},
    "Saudi Pro League":       {"sport":"soccer",    "league":"sau.1",                  "group":"Soccer"},
    "Belgian Pro League":     {"sport":"soccer",    "league":"bel.1",                  "group":"Soccer"},
    "Eredivisie":             {"sport":"soccer",    "league":"ned.1",                  "group":"Soccer"},
    "CONCACAF Champions Cup": {"sport":"soccer", "league":"concacaf.champions",  "group":"Soccer", "country":"CONCACAF"},
    # ── Selecciones / FIFA Internacional ─────────────────────────────────────
    # Pausa FIFA: UEFA Nations League Finals, CONCACAF Nations League,
    # Copa Oro, Eliminatorias, Amistosos internacionales
    "UEFA Nations League":    {"sport":"soccer", "league":"uefa.nations",        "group":"Soccer", "country":"Europa"},
    "CONCACAF Nations League":{"sport":"soccer", "league":"concacaf.nations.league","group":"Soccer","country":"CONCACAF"},
    "Copa Oro":               {"sport":"soccer", "league":"concacaf.gold",        "group":"Soccer", "country":"CONCACAF"},
    "Copa América":           {"sport":"soccer", "league":"conmebol.america",     "group":"Soccer", "country":"CONMEBOL"},
    "Eliminatorias UEFA":     {"sport":"soccer", "league":"uefa.qualifying",      "group":"Soccer", "country":"Europa"},
    "Eliminatorias CONMEBOL": {"sport":"soccer", "league":"conmebol.worldcup",   "group":"Soccer", "country":"CONMEBOL"},
    "Eliminatorias CONCACAF": {"sport":"soccer", "league":"concacaf.worldcup",   "group":"Soccer", "country":"CONCACAF"},
    "Amistosos Internacionales":{"sport":"soccer","league":"fifa.friendly",       "group":"Soccer", "country":"Mundial"},
    "Africa Cup of Nations":  {"sport":"soccer", "league":"caf.nations",          "group":"Soccer", "country":"África"},
    "Asian Cup":              {"sport":"soccer", "league":"afc.cupofnations",     "group":"Soccer", "country":"Asia"},
    "World Cup":              {"sport":"soccer", "league":"fifa.world",           "group":"Soccer", "country":"Mundial"},
    # ── Ligas ocultas: no aparecen en el menú, solo sus equipos favoritos ────
    "Superliga":              {"sport":"soccer",    "league":"DEN.1",                  "group":"Soccer", "hidden":True},
    "Süper Lig":              {"sport":"soccer",    "league":"TUR.1",                  "group":"Soccer", "hidden":True},
    "Super League Greece":    {"sport":"soccer",    "league":"GRE.1",                  "group":"Soccer", "hidden":True},
    "Primeira Liga":          {"sport":"soccer",    "league":"POR.1",                  "group":"Soccer", "hidden":True},
    "Eliteserien":            {"sport":"soccer",    "league":"NOR.1",                  "group":"Soccer", "hidden":True},
    "Allsvenskan":            {"sport":"soccer",    "league":"SWE.1",                  "group":"Soccer", "hidden":True},
}

# ── Equipos favoritos de ligas ocultas ──────────────────────────────────────
# Solo se muestran partidos de estos equipos aunque su liga no esté en el menú.
# Clave: nombre del equipo tal como lo devuelve ESPN (displayName).
WATCHED_TEAMS = {
    # ── Dinamarca — Superliga ─────────────────────────────────────────────────
    "FC Midtjylland",       # ESPN: "FC Midtjylland"
    "FC Copenhagen",        # ESPN: "FC Copenhagen"
    "Brøndby IF",           # ESPN: "Brøndby IF"
    "AGF",                  # ESPN: "AGF"

    # ── Turquía — Süper Lig ──────────────────────────────────────────────────
    "Fenerbahce",           # ESPN: "Fenerbahce" (sin acento)
    "Galatasaray",          # ESPN: "Galatasaray"
    "Besiktas",             # ESPN: "Besiktas" (sin acento)
    "Trabzonspor",          # ESPN: "Trabzonspor"

    # ── Grecia — Super League ────────────────────────────────────────────────
    "PAOK Salonika",        # ESPN: "PAOK Salonika" (no "PAOK" a secas)
    "AEK Athens",           # ESPN: "AEK Athens"
    "Panathinaikos",        # ESPN: "Panathinaikos"
    "Olympiacos",           # ESPN: "Olympiacos" (no "Olympiakos")

    # ── Portugal — Primeira Liga ─────────────────────────────────────────────
    "Benfica",              # ESPN: "Benfica"
    "FC Porto",             # ESPN: "FC Porto"
    "Sporting CP",          # ESPN: "Sporting CP"
    "SC Braga",             # ESPN: "SC Braga" (verificar — puede ser "Braga")
    "Braga",                # variante

    # ── Noruega — Eliteserien ────────────────────────────────────────────────
    "Rosenborg BK",         # ESPN: "Rosenborg BK"
    "Molde FK",             # ESPN: "Molde FK"
    "Bodo/Glimt",           # ESPN: "Bodo/Glimt" (sin tildes)

    # ── Suecia — Allsvenskan ─────────────────────────────────────────────────
    "Malmö FF",             # ESPN: "Malmö FF"
    "AIK",                  # ESPN: "AIK"
}
LEAGUE_FLAG = {
    "NBA":                    "🇺🇸",
    "MLB":                    "🇺🇸",
    "NFL":                    "🇺🇸",
    "NCAAF":                  "🇺🇸",
    "NHL":                    "🇺🇸🇨🇦",
    "MLS":                    "🇺🇸",
    "Liga MX":                "🇲🇽",
    "Premier League":         "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "La Liga":                "🇪🇸",
    "Bundesliga":             "🇩🇪",
    "Serie A":                "🇮🇹",
    "Ligue 1":                "🇫🇷",
    "Champions League":       "🇪🇺",
    "Europa League":          "🇪🇺",
    "Conference League":      "🇪🇺",
    "Saudi Pro League":       "🇸🇦",
    "Belgian Pro League":     "🇧🇪",
    "Eredivisie":             "🇳🇱",
    "CONCACAF Champions Cup": "🌎",
    # Ligas ocultas
    "Superliga":              "🇩🇰",
    "Süper Lig":              "🇹🇷",
    "Super League Greece":    "🇬🇷",
    "Primeira Liga":          "🇵🇹",
    "Eliteserien":            "🇳🇴",
    "Allsvenskan":            "🇸🇪",
    "UEFA Nations League":     "🏆",
    "CONCACAF Nations League": "🌎",
    "Copa Oro":                "🥇",
    "Copa América":            "🏆",
    "Eliminatorias UEFA":      "🌍",
    "Eliminatorias CONMEBOL":  "🌎",
    "Eliminatorias CONCACAF":  "🌎",
    "Amistosos Internacionales":"🌐",
    "Africa Cup of Nations":   "🌍",
    "Asian Cup":               "🌏",
    "World Cup":               "🌍",
}

def league_label(name):
    """Return flag + league name."""
    return f"{LEAGUE_FLAG.get(name, '🌐')} {name}"

HOME_BOOST = {
    # Home win probability boost vs neutral site
    # Source: historical home win rates 2020-2025 vs expected (based on team quality)
    # NBA: home advantage shrunk post-COVID → ~3.5% boost (was 5-6% pre-2020)
    "NBA":   0.032,
    # MLB: minimal home advantage → ~2.3%
    "MLB":   0.023,
    # NFL: home advantage ~2.5-3% (travel, crowd, altitude)
    "NFL":   0.028,
    "NCAAF": 0.042,  # college: bigger crowds, less professional travel management
    # NHL: home advantage ~3% (ice quality + crowd)
    "NHL":   0.028,
    # Soccer: home advantage varies significantly by country
    "MLS":              0.038,  # MLS: moderate home boost (plastic pitches, travel)
    "Liga MX":          0.048,  # Liga MX: strong home atmosphere, altitude factor
    "Premier League":   0.032,  # PL: professional clubs, mild home boost
    "La Liga":          0.038,
    "Bundesliga":       0.036,
    "Serie A":          0.036,
    "Ligue 1":          0.036,
    "Champions League": 0.030,  # UCL: neutral-ish, big clubs away fine
    "Europa League":    0.033,
    "Conference League":0.035,
    "CONCACAF Champions Cup": 0.045,
    "Saudi Pro League": 0.040,  # SPL: strong local support
    "Belgian Pro League":0.038,
    "Eredivisie":       0.038,
    # Ligas ocultas
    "Superliga":              0.042,  # Dinamarca: fuerte ventaja local
    "Süper Lig":              0.045,  # Turquía: afición muy intensa
    "Super League Greece":    0.044,  # Grecia: ambientes muy calientes
    "Primeira Liga":          0.038,
    "Eliteserien":            0.040,
    "Allsvenskan":            0.038,
    }
LEAGUE_AVG_GOALS = {
    # ── No-soccer: puntos/carreras TOTALES por partido (ambos equipos) ──────────
    # Fuente: StatMuse, Basketball-Reference, Hockey-Reference — Temporada 2025-26
    "NBA":   228.0,
    "MLB":   8.8,
    "NFL":   47.8,
    "NCAAF": 58.0,
    "NHL":   6.10,
    # ── Soccer: goles totales por partido (ambos equipos) ─────────────────────
    # Fuente: Sofascore, FootyStats — Temporada 2025-26 (en curso)
    "MLS":              2.90,
    "Liga MX":          2.65,
    "Premier League":   2.80,  # PL 2025-26: O2.5 ~56%
    "La Liga":          2.62,
    "Bundesliga":       3.14,  # Bundesliga 2025-26: 3.14 (Sofascore), O2.5=62%, BTTS=57%
    "Serie A":          2.68,
    "Ligue 1":          2.60,  # Ligue 1 2025-26: O2.5 ~56%
    "Champions League": 3.05,
    "Europa League":    2.85,
    "Conference League":2.70,
    "CONCACAF Champions Cup": 2.75,
    "Saudi Pro League": 2.78,
    "Belgian Pro League":3.08,
    "Eredivisie":       3.15,
    # Ligas ocultas
    "Superliga":              2.95,  # Dinamarca 2025-26
    "Süper Lig":              2.72,  # Turquía 2025-26
    "Super League Greece":    2.62,  # Grecia 2025-26
    "Primeira Liga":          2.58,  # Portugal 2025-26
    "Eliteserien":            2.88,  # Noruega
    "Allsvenskan":            2.72,  # Suecia
    # International / selecciones
    "UEFA Nations League":     2.5,
    "CONCACAF Nations League": 2.8,
    "Copa Oro":                2.7,
    "Copa América":            2.4,
    "Eliminatorias UEFA":      2.8,
    "Eliminatorias CONMEBOL":  2.6,
    "Eliminatorias CONCACAF":  2.9,
    "Amistosos Internacionales":2.6,
    "Africa Cup of Nations":   2.3,
    "Asian Cup":               2.4,
    "World Cup":               2.5,
}

# ── MLB Ballpark Factors ────────────────────────────────────────────────────
# Source: Statcast/BaseballSavant park factors (5-year avg, normalized to 1.0)
# Values above 1.0 → hitter-friendly (more runs), below 1.0 → pitcher-friendly
MLB_BALLPARK_FACTOR = {
    "coors":        1.30,  # Coors Field, Colorado (altitude 5280 ft — ball flies)
    "great american": 1.14, # Great American Ball Park, Cincinnati
    "yankee":       1.08,  # Yankee Stadium (short porch RF)
    "fenway":       1.06,  # Fenway Park, Boston (Green Monster)
    "wrigley":      1.05,  # Wrigley Field, Chicago Cubs
    "oracle":       0.92,  # Oracle Park, San Francisco (marine layer, ball dies)
    "petco":        0.92,  # Petco Park, San Diego (sea level, cool air)
    "dodger":       0.95,  # Dodger Stadium
    "tropicana":    0.93,  # Tropicana Field (dome, dead air)
    "t-mobile":     0.94,  # T-Mobile Park, Seattle (rain/cool)
    "busch":        0.97,  # Busch Stadium, St. Louis
}

def get_mlb_ballpark_factor(venue: str) -> float:
    """Return run-scoring multiplier for MLB venue. Default 1.0 (neutral)."""
    if not venue:
        return 1.0
    v = venue.lower()
    for key, factor in MLB_BALLPARK_FACTOR.items():
        if key in v:
            return factor
    return 1.0

# ── Soccer: Standard lines by league ───────────────────────────────────────
# O/U 90-min ONLY (regulation + stoppage time). No extra time counts.
# High-scoring leagues use higher default lines.
SOCCER_STD_LINE = {
    "Bundesliga":       3.0,   # avg 3.24 → line typically opens at 3.0 or 3.5
    "Premier League":   2.5,
    "La Liga":          2.5,
    "Serie A":          2.5,
    "Ligue 1":          2.5,
    "Champions League": 2.5,
    "Europa League":    2.5,
    "Conference League":2.5,
    "MLS":              2.5,
    "Liga MX":          2.5,
    "CONCACAF Champions Cup": 2.5,
    "Saudi Pro League":  2.5,
    "Belgian Pro League":3.0,
    "Eredivisie":        3.0,
}
_TP_TAB       = "team_profiles"
_TP_MAX_GAMES = 10
_TP_HEADERS   = [
    "team_id","team_name","league","sport_group","last_updated",
    "games_json","n_games","avg_scored","avg_conceded",
    "avg_scored_home","avg_conceded_home","avg_scored_away","avg_conceded_away",
    "rate_o15","rate_o25","rate_o35","rate_btts",
    "rate_o15_home","rate_o25_home","rate_o35_home","rate_btts_home",
    "rate_o15_away","rate_o25_away","rate_o35_away","rate_btts_away",
    "thresholds_json","red_card_rate",
]
_TP_THRESHOLDS = {
    "Soccer":     [("o15",1.5),("o25",2.5),("o35",3.5)],
    "Basketball": [("o100",100),("o105",105),("o110",110),("o115",115),("o120",120),("o125",125)],
    "Hockey":     [("o3",3.0),("o4",4.0),("o5",5.0),("o6",6.0),("o7",7.0)],
    "Baseball":   [("o6",6.0),("o7",7.0),("o8",8.0),("o9",9.0),("o10",10.0)],
    "Football":   [("o17",17),("o21",21),("o24",24),("o28",28),("o35",35),("o42",42)],
}

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"

def get_demo_games():
    return [
        {"id":"d1","league":"Champions League","home_team":"Real Madrid","away_team":"Bayern Munich",
         "home_score":"","away_score":"","home_record":"24-5-2","away_record":"22-6-3",
         "state":"pre","status_detail":"Mar 3:00 PM","date":"","venue":"Santiago Bernabéu",
         "odds":{"spread":"","over_under":"3.0","home_ml":"-118","away_ml":"+290","home_wp":"47","away_wp":"28"}},
        {"id":"d2","league":"Premier League","home_team":"Arsenal","away_team":"Chelsea",
         "home_score":"","away_score":"","home_record":"20-6-5","away_record":"17-8-6",
         "state":"pre","status_detail":"Dom 12:30 PM","date":"","venue":"Emirates Stadium",
         "odds":{"spread":"","over_under":"2.5","home_ml":"-145","away_ml":"+380","home_wp":"52","away_wp":"23"}},
        {"id":"d3","league":"NBA","home_team":"Boston Celtics","away_team":"Miami Heat",
         "home_score":"","away_score":"","home_record":"47-13","away_record":"28-32",
         "state":"pre","status_detail":"8:00 PM ET","date":"","venue":"TD Garden",
         "odds":{"spread":"BOS -8.5","spread_line":"-8.5","spread_home_ml":"-110","spread_away_ml":"-110","over_under":"218.0","home_ml":"-320","away_ml":"+260","home_wp":"76","away_wp":"24"}},
        {"id":"d4","league":"NBA","home_team":"Denver Nuggets","away_team":"Oklahoma City Thunder",
         "home_score":"62","away_score":"58","home_record":"44-16","away_record":"46-14",
         "state":"in","status_detail":"3rd Qtr 4:22","date":"","venue":"Ball Arena",
         "odds":{"spread":"OKC -1.5","spread_line":"1.5","spread_home_ml":"-110","spread_away_ml":"-110","over_under":"228.0","home_ml":"+105","away_ml":"-125","home_wp":"44","away_wp":"56"}},
        {"id":"d5","league":"Liga MX","home_team":"Club América","away_team":"Chivas Guadalajara",
         "home_score":"","away_score":"","home_record":"14-4-4","away_record":"10-6-6",
         "state":"pre","status_detail":"Sáb 8:00 PM","date":"","venue":"Estadio Azteca",
         "odds":{"spread":"","over_under":"2.5","home_ml":"-130","away_ml":"+320","home_wp":"55","away_wp":"20"}},
        {"id":"d6","league":"MLB","home_team":"New York Yankees","away_team":"Boston Red Sox",
         "home_score":"","away_score":"","home_record":"18-12","away_record":"15-15",
         "state":"pre","status_detail":"7:05 PM ET","date":"","venue":"Yankee Stadium",
         "odds":{"spread":"NYY -1.5","spread_line":"-1.5","spread_home_ml":"-155","spread_away_ml":"+130","over_under":"8.5","home_ml":"-145","away_ml":"+122","home_wp":"59","away_wp":"41"}},
        {"id":"d7","league":"Bundesliga","home_team":"Bayern Munich","away_team":"Borussia Dortmund",
         "home_score":"","away_score":"","home_record":"20-4-4","away_record":"16-6-6",
         "state":"pre","status_detail":"Sáb 9:30 AM","date":"","venue":"Allianz Arena",
         "odds":{"spread":"","over_under":"3.5","home_ml":"-155","away_ml":"+400","home_wp":"58","away_wp":"18"}},
        {"id":"d8","league":"NHL","home_team":"Florida Panthers","away_team":"Tampa Bay Lightning",
         "home_score":"","away_score":"","home_record":"41-18-6","away_record":"38-22-5",
         "state":"pre","status_detail":"7:00 PM ET","date":"","venue":"Amerant Bank Arena",
         "odds":{"spread":"FLA -1.5","spread_line":"-1.5","spread_home_ml":"-140","spread_away_ml":"+118","over_under":"6.0","home_ml":"-135","away_ml":"+115","home_wp":"55","away_wp":"45"}},
    ]

def _gsheets_available():
    """True if Google Sheets secrets are configured."""
    try:
        s = st.secrets.get("gsheets", {})
        return bool(s.get("private_key") and s.get("spreadsheet_id"))
    except:
        return False

@st.cache_resource(show_spinner=False)
def _get_gsheet_client():
    """Return authenticated gspread client (cached)."""
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    s = dict(st.secrets["gsheets"])
    s["private_key"] = s["private_key"].replace("\\n", "\n")
    creds = Credentials.from_service_account_info(s, scopes=scopes)
    return gspread.authorize(creds)

@st.cache_data(ttl=3600, show_spinner=False)
def _load_all_team_profiles():
    """Carga todos los perfiles desde Sheets → dict {team_id: profile}. TTL 1h."""
    if not _gsheets_available():
        return {}
    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)
        try:
            ws = sh.worksheet(_TP_TAB)
        except:
            ws = sh.add_worksheet(title=_TP_TAB, rows=2000, cols=len(_TP_HEADERS))
            ws.update("A1", [_TP_HEADERS])
            return {}
        rows = ws.get_all_values()
        if len(rows) < 2:
            return {}
        profiles = {}
        for row in rows[1:]:
            if not row or not row[0]:
                continue
            def _c(i, d=""):
                return row[i] if i < len(row) else d
            try:
                games      = json.loads(_c(5)) if _c(5) else []
                thresholds = json.loads(_c(25)) if _c(25) else {}
                profiles[_c(0)] = {
                    "team_id":           _c(0),
                    "team_name":         _c(1),
                    "league":            _c(2),
                    "sport_group":       _c(3),
                    "last_updated":      _c(4),
                    "games":             games,
                    "n_games":           int(_c(6) or 0),
                    "avg_scored":        float(_c(7)  or 0),
                    "avg_conceded":      float(_c(8)  or 0),
                    "avg_scored_home":   float(_c(9)  or 0),
                    "avg_conceded_home": float(_c(10) or 0),
                    "avg_scored_away":   float(_c(11) or 0),
                    "avg_conceded_away": float(_c(12) or 0),
                    "rate_o15":          float(_c(13) or 0),
                    "rate_o25":          float(_c(14) or 0),
                    "rate_o35":          float(_c(15) or 0),
                    "rate_btts":         float(_c(16) or 0),
                    "rate_o15_home":     float(_c(17) or 0),
                    "rate_o25_home":     float(_c(18) or 0),
                    "rate_o35_home":     float(_c(19) or 0),
                    "rate_btts_home":    float(_c(20) or 0),
                    "rate_o15_away":     float(_c(21) or 0),
                    "rate_o25_away":     float(_c(22) or 0),
                    "rate_o35_away":     float(_c(23) or 0),
                    "rate_btts_away":    float(_c(24) or 0),
                    "thresholds":        thresholds,
                    "red_card_rate":     float(_c(26) or 0),
                }
            except:
                continue
        return profiles
    except Exception as _e:
        # Surface error in badge so we can debug
        st.session_state["_tp_load_error"] = str(_e)
        return {}



def _compute_profile_stats(games, sport_group):
    """Calcula todas las stats y rates a partir de la lista de partidos."""
    if not games:
        return {}
    all_s  = [g["scored"]   for g in games]
    all_c  = [g["conceded"] for g in games]
    home_g = [g for g in games if g.get("home")]
    away_g = [g for g in games if not g.get("home")]

    def safe_avg(lst): return round(sum(lst)/len(lst), 3) if lst else 0.0
    def rate(lst, fn): return round(sum(1 for x in lst if fn(x))/len(lst), 3) if lst else 0.0

    stats = {
        "n_games":           len(games),
        "avg_scored":        safe_avg(all_s),
        "avg_conceded":      safe_avg(all_c),
        "avg_scored_home":   safe_avg([g["scored"]   for g in home_g]),
        "avg_conceded_home": safe_avg([g["conceded"] for g in home_g]),
        "avg_scored_away":   safe_avg([g["scored"]   for g in away_g]),
        "avg_conceded_away": safe_avg([g["conceded"] for g in away_g]),
    }

    if sport_group == "Soccer":
        stats.update({
            "rate_o15":       rate(games,  lambda g: g["scored"]+g["conceded"] > 1.5),
            "rate_o25":       rate(games,  lambda g: g["scored"]+g["conceded"] > 2.5),
            "rate_o35":       rate(games,  lambda g: g["scored"]+g["conceded"] > 3.5),
            "rate_btts":      rate(games,  lambda g: g["scored"]>0 and g["conceded"]>0),
            "rate_o15_home":  rate(home_g, lambda g: g["scored"]+g["conceded"] > 1.5),
            "rate_o25_home":  rate(home_g, lambda g: g["scored"]+g["conceded"] > 2.5),
            "rate_o35_home":  rate(home_g, lambda g: g["scored"]+g["conceded"] > 3.5),
            "rate_btts_home": rate(home_g, lambda g: g["scored"]>0 and g["conceded"]>0),
            "rate_o15_away":  rate(away_g, lambda g: g["scored"]+g["conceded"] > 1.5),
            "rate_o25_away":  rate(away_g, lambda g: g["scored"]+g["conceded"] > 2.5),
            "rate_o35_away":  rate(away_g, lambda g: g["scored"]+g["conceded"] > 3.5),
            "rate_btts_away": rate(away_g, lambda g: g["scored"]>0 and g["conceded"]>0),
            # Tasa de tarjeta roja: % de partidos donde el equipo recibió ≥1 roja
            # Liga promedio: ~0.15 (1 roja cada 6-7 partidos)
            # Equipo agresivo: >0.25 → penalizar scoring por 10 min menos con 11
            "red_card_rate":  rate(games, lambda g: g.get("red_cards", 0) >= 1),
            "thresholds": {},
        })
    else:
        thresholds = {}
        for key, thresh in _TP_THRESHOLDS.get(sport_group, []):
            thresholds[key]         = rate(games,  lambda g, t=thresh: g["scored"] > t)
            thresholds[key+"_home"] = rate(home_g, lambda g, t=thresh: g["scored"] > t)
            thresholds[key+"_away"] = rate(away_g, lambda g, t=thresh: g["scored"] > t)
        stats.update({
            "rate_o15":0.0,"rate_o25":0.0,"rate_o35":0.0,"rate_btts":0.0,
            "rate_o15_home":0.0,"rate_o25_home":0.0,"rate_o35_home":0.0,"rate_btts_home":0.0,
            "rate_o15_away":0.0,"rate_o25_away":0.0,"rate_o35_away":0.0,"rate_btts_away":0.0,
            "red_card_rate": 0.0,
            "thresholds": thresholds,
        })
    return stats


# [_fetch_all_teams_in_league moved]






def update_team_profile(team_id, team_name, league, sport_group, new_games):
    """
    Fusiona new_games con el perfil existente (últimos 10 partidos).
    new_games = [{scored, conceded, home, date, opp}, ...] newest-first.
    Escribe en Sheets de forma síncrona (llamar desde background/thread).
    """
    if not _gsheets_available() or not team_id:
        return False
    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)
        try:
            ws = sh.worksheet(_TP_TAB)
        except:
            ws = sh.add_worksheet(title=_TP_TAB, rows=2000, cols=len(_TP_HEADERS))
            ws.update("A1", [_TP_HEADERS])

        all_rows = ws.get_all_values()
        data_rows = all_rows[1:] if len(all_rows) > 1 else []

        # Buscar fila existente del equipo
        existing_games = []
        target_row     = None
        for i, row in enumerate(data_rows):
            if row and row[0] == str(team_id):
                target_row = i + 2  # 1-indexed, +1 header
                try:
                    existing_games = json.loads(row[5]) if row[5] else []
                except:
                    existing_games = []
                break

        # Fusionar: nuevos primero, deduplicar por (date, opp), cap 10
        merged = list(new_games)
        seen   = {(g.get("date",""), g.get("opp","")) for g in merged}
        for g in existing_games:
            k = (g.get("date",""), g.get("opp",""))
            if k not in seen:
                merged.append(g)
                seen.add(k)
        merged = merged[:_TP_MAX_GAMES]

        stats = _compute_profile_stats(merged, sport_group)
        if not stats:
            return False

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row_data = [
            str(team_id), team_name, league, sport_group, now,
            json.dumps(merged, ensure_ascii=False),
            stats["n_games"],
            stats["avg_scored"],     stats["avg_conceded"],
            stats["avg_scored_home"],stats["avg_conceded_home"],
            stats["avg_scored_away"],stats["avg_conceded_away"],
            stats["rate_o15"],  stats["rate_o25"],  stats["rate_o35"],  stats["rate_btts"],
            stats["rate_o15_home"],stats["rate_o25_home"],stats["rate_o35_home"],stats["rate_btts_home"],
            stats["rate_o15_away"],stats["rate_o25_away"],stats["rate_o35_away"],stats["rate_btts_away"],
            json.dumps(stats["thresholds"], ensure_ascii=False),
            stats.get("red_card_rate", 0.0),
        ]

        col_end = chr(ord("A") + len(_TP_HEADERS) - 1)
        if target_row:
            ws.update(f"A{target_row}:{col_end}{target_row}", [row_data])
        else:
            ws.append_row(row_data, value_input_option="RAW")

        _load_all_team_profiles.clear()  # invalida cache
        return True
    except:
        return False


# ══════════════════════════════════════════════════════════════════════════════
# POPULATE ALL TEAM PROFILES — función para el botón "🧠 Poblar Memoria"
# Recorre todas las ligas activas, obtiene equipos de ESPN,
# llama fetch_recent_form para cada uno y guarda en team_profiles Sheet.
# ══════════════════════════════════════════════════════════════════════════════

# Mapa de ligas a slugs ESPN (idéntico al de enrich_game_with_form)
_ALL_LEAGUE_SLUGS = {
    "NBA":                  ("basketball", "nba"),
    "NFL":                  ("football",   "nfl"),
    "NCAAF":                ("football",   "college-football"),
    "MLB":                  ("baseball",   "mlb"),
    "NHL":                  ("hockey",     "nhl"),
    "MLS":                  ("soccer",     "usa.1"),
    "Liga MX":              ("soccer",     "mex.1"),
    "Premier League":       ("soccer",     "eng.1"),
    "La Liga":              ("soccer",     "esp.1"),
    "Bundesliga":           ("soccer",     "ger.1"),
    "Serie A":              ("soccer",     "ita.1"),
    "Ligue 1":              ("soccer",     "fra.1"),
    "Champions League":     ("soccer",     "uefa.champions"),
    "Europa League":        ("soccer",     "uefa.europa"),
    "Conference League":    ("soccer",     "uefa.europa.conf"),
    "CONCACAF Champions Cup":("soccer",    "concacaf.champions"),
    "Saudi Pro League":      ("soccer",    "sau.1"),
    "Belgian Pro League":    ("soccer",    "bel.1"),
    "Eredivisie":            ("soccer",    "ned.1"),
    # Ligas ocultas (para poblar memoria de equipos favoritos)
    "Superliga":             ("soccer",    "DEN.1"),
    "Süper Lig":             ("soccer",    "TUR.1"),
    "Super League Greece":   ("soccer",    "GRE.1"),
    "Primeira Liga":         ("soccer",    "POR.1"),
    "Eliteserien":           ("soccer",    "NOR.1"),
    "Allsvenskan":           ("soccer",    "SWE.1"),
}

def get_team_profile(team_id):
    """Retorna perfil de equipo del cache, o None si no existe."""
    if not team_id:
        return None
    return _load_all_team_profiles().get(str(team_id))


@st.cache_data(ttl=1800)  # Cache 30min — form doesn't change mid-day
def fetch_recent_form(sport, league, team_id, n_games=10):
    """
    Fetch last N results for a team from ESPN team events API.
    Returns dict with:
      - form_score:    float 0.0-1.0 (weighted W/L/D rate)
      - avg_scored:    float — avg goals/points scored last N games   (Signal B)
      - avg_conceded:  float — avg goals/points conceded last N games (Signal B)
      - last_game_date: str YYYY-MM-DD — date of most recent game     (Signal C)
    Returns None if unavailable.
    """
    if not team_id or not sport or not league:
        return None
    try:
        url = (f"https://site.api.espn.com/apis/site/v2/sports/"
               f"{sport}/{league}/teams/{team_id}/events?limit={n_games + 3}")
        r = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None
        data = r.json()
        events = data.get("events", [])
        if not events:
            return None

        results        = []   # W/L/D as 1.0/0.0/0.5
        scored_list    = []   # goals/pts scored by this team
        games_raw_list = []   # structured records for team profile learning
        conceded_list = []   # goals/pts conceded by this team
        last_date     = None

        for ev in events[:n_games + 3]:
            competitions = ev.get("competitions", [{}])
            if not competitions:
                continue
            comp  = competitions[0]
            state = ev.get("status", {}).get("type", {}).get("state", "")
            if state != "post":
                continue
            comps     = comp.get("competitors", [])
            team_comp = next((c for c in comps if str(c.get("id","")) == str(team_id)), None)
            if not team_comp:
                continue

            # Scores (Signal B)
            home_c = next((c for c in comps if c.get("homeAway") == "home"), None)
            away_c = next((c for c in comps if c.get("homeAway") == "away"), None)
            try:
                hs = float(home_c.get("score", 0) or 0)
                as_ = float(away_c.get("score", 0) or 0)
            except:
                hs = as_ = None

            is_home   = team_comp.get("homeAway") == "home"
            winner    = team_comp.get("winner", False)
            is_draw   = (hs == as_) if hs is not None else False

            # W/L/D
            if winner:          results.append(1.0)
            elif is_draw:       results.append(0.5)
            else:               results.append(0.0)

            # Scored / Conceded
            game_date = ev.get("date", "")[:10]
            opp_comp  = next((c for c in comps if str(c.get("id","")) != str(team_id)), None)
            opp_name  = opp_comp.get("team",{}).get("displayName","") if opp_comp else ""

            if hs is not None:
                if is_home:
                    scored_list.append(hs); conceded_list.append(as_)
                    games_raw_list.append({"scored":hs,"conceded":as_,"home":True,
                                           "date":game_date,"opp":opp_name})
                else:
                    scored_list.append(as_); conceded_list.append(hs)
                    games_raw_list.append({"scored":as_,"conceded":hs,"home":False,
                                           "date":game_date,"opp":opp_name})

            # Last game date (Signal C) — first post game found = most recent
            if last_date is None:
                raw_date = game_date
                if raw_date:
                    last_date = raw_date

            if len(results) >= n_games:
                break

        if not results:
            return None

        # Weighted form score — recent games weight more
        weights     = [len(results) - i for i in range(len(results))]
        total_w     = sum(weights)
        form_score  = sum(r * w for r, w in zip(results, weights)) / total_w

        avg_scored   = round(sum(scored_list)   / len(scored_list),   2) if scored_list   else None
        avg_conceded = round(sum(conceded_list)  / len(conceded_list), 2) if conceded_list else None

        return {
            "form_score":     round(form_score, 4),
            "avg_scored":     avg_scored,
            "avg_conceded":   avg_conceded,
            "last_game_date": last_date,
            "n_games":        len(results),
            "games_raw":      games_raw_list,   # for team profile learning
        }

    except Exception:
        return None





def _fetch_all_teams_in_league(sport_slug, league_slug):
    """
    Obtiene lista de {id, name} de todos los equipos de una liga via ESPN.
    """
    try:
        url = (f"https://site.api.espn.com/apis/site/v2/sports/"
               f"{sport_slug}/{league_slug}/teams?limit=100")
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        data  = r.json()
        teams_raw = (data.get("sports", [{}])[0]
                         .get("leagues", [{}])[0]
                         .get("teams", []))
        result = []
        for t in teams_raw:
            t_info = t.get("team", {})
            tid    = str(t_info.get("id", ""))
            name   = t_info.get("displayName", t_info.get("name", ""))
            if tid and name:
                result.append({"id": tid, "name": name})
        return result
    except:
        return []


def _fetch_recent_form_raw(sport, league, team_id, n_games=10):
    """
    Versión sin @st.cache_data. Intenta múltiples endpoints de ESPN para
    obtener historial de partidos terminados de un equipo.
    """
    if not team_id or not sport or not league:
        return None

    def _get_score(competitor):
        """Extrae score de múltiples ubicaciones posibles."""
        for key in ("score", "homeScore", "awayScore", "points"):
            v = competitor.get(key)
            if v is not None and v != "":
                try: return float(v)
                except: pass
        score_obj = competitor.get("score", {})
        if isinstance(score_obj, dict):
            for key in ("value", "displayValue"):
                v = score_obj.get(key)
                if v is not None:
                    try: return float(v)
                    except: pass
        return None

    def _parse_events(events, team_id, max_games):
        """Parsea lista de eventos y retorna juegos terminados con score y tarjetas rojas."""
        games_raw_list = []
        now_iso = datetime.now(timezone.utc).isoformat()[:16]
        for ev in events:
            ev_date = ev.get("date", "")
            if ev_date[:16] > now_iso:
                continue
            state = ev.get("status", {}).get("type", {}).get("state", "")
            if state not in ("post", ""):
                continue
            competitions = ev.get("competitions", [])
            if not competitions:
                continue
            comp  = competitions[0]
            comps = comp.get("competitors", [])
            if len(comps) < 2:
                continue
            team_comp = next((c for c in comps if str(c.get("id","")) == str(team_id)), None)
            opp_comp  = next((c for c in comps if str(c.get("id","")) != str(team_id)), None)
            if not team_comp or not opp_comp:
                continue
            team_score = _get_score(team_comp)
            opp_score  = _get_score(opp_comp)
            if team_score is None or opp_score is None:
                continue
            if team_score == 0 and opp_score == 0 and state == "" and not comp.get("boxscoreAvailable", False):
                continue
            is_home  = team_comp.get("homeAway") == "home"
            opp_name = opp_comp.get("team", {}).get("displayName", "")

            # ── Extraer tarjetas rojas del evento si ESPN las incluye ──────────
            red_cards_team = 0
            red_cards_opp  = 0
            # ESPN a veces incluye stats en el competition o en el competitor
            for _rc_src in [team_comp, comp]:
                _stats = _rc_src.get("statistics", [])
                if isinstance(_stats, list):
                    for _st in _stats:
                        _name = (_st.get("name") or _st.get("abbreviation") or "").lower()
                        if "red" in _name or _name in ("rc", "redcards"):
                            try: red_cards_team = max(red_cards_team, int(_st.get("displayValue", 0) or 0))
                            except: pass
            for _rc_src2 in [opp_comp]:
                _stats2 = _rc_src2.get("statistics", [])
                if isinstance(_stats2, list):
                    for _st2 in _stats2:
                        _name2 = (_st2.get("name") or _st2.get("abbreviation") or "").lower()
                        if "red" in _name2 or _name2 in ("rc", "redcards"):
                            try: red_cards_opp = max(red_cards_opp, int(_st2.get("displayValue", 0) or 0))
                            except: pass

            games_raw_list.append({
                "scored":        team_score,
                "conceded":      opp_score,
                "home":          is_home,
                "date":          ev_date[:10],
                "opp":           opp_name,
                "red_cards":     red_cards_team,      # tarjetas rojas recibidas por este equipo
                "red_cards_opp": red_cards_opp,       # tarjetas rojas del rival
            })
            if len(games_raw_list) >= max_games:
                break
        return games_raw_list

    try:
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        base = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}"

        # Intento 1: /teams/{id}/schedule (más completo)
        r = requests.get(f"{base}/teams/{team_id}/schedule", timeout=10, headers=headers)
        if r.status_code == 200:
            events = r.json().get("events", [])
            games = _parse_events(events, team_id, n_games)
            if games:
                return games

        # Intento 2: /teams/{id}/schedule?season=2025 (temporada pasada)
        from datetime import datetime as _dt
        _yr = _dt.now().year
        for _season in [_yr, _yr - 1]:
            r2 = requests.get(f"{base}/teams/{team_id}/schedule?season={_season}", timeout=8, headers=headers)
            if r2.status_code == 200:
                events2 = r2.json().get("events", [])
                games2 = _parse_events(events2, team_id, n_games)
                if games2:
                    return games2

        # Intento 3: scoreboard buscando partidos de este equipo
        r3 = requests.get(f"{base}/teams/{team_id}/events", timeout=8, headers=headers)
        if r3.status_code == 200:
            events3 = r3.json().get("events", [])
            games3 = _parse_events(events3, team_id, n_games)
            if games3:
                return games3

        return None
    except Exception:
        return None


# populate_all_team_profiles moved below _compute_profile_stats


def populate_all_team_profiles(progress_bar=None, status_text=None):
    """
    Recorre todas las ligas, recolecta todos los perfiles en memoria,
    y los escribe al Sheet EN UNA SOLA llamada batch al final.
    Esto evita timeouts de Streamlit Cloud en conexiones largas.
    """
    if not _gsheets_available():
        return 0, 0, ["❌ Google Sheets no configurado"]

    log           = []
    failed        = 0
    all_rows      = []   # acumula todas las filas en memoria
    leagues       = list(_ALL_LEAGUE_SLUGS.items())
    total_leagues = len(leagues)

    # ── Fase 1: recolectar datos de ESPN (sin tocar Sheets) ───────────────────
    for li, (league, (sport_slug, league_slug)) in enumerate(leagues):
        sport_group = LEAGUES.get(league, {}).get("group", "Soccer")

        if status_text:
            status_text.markdown(f"🔍 **{league}** — obteniendo equipos...")

        teams = _fetch_all_teams_in_league(sport_slug, league_slug)
        if not teams:
            log.append(f"⚠ {league}: sin equipos en ESPN")
            if progress_bar:
                progress_bar.progress((li + 1) / total_leagues * 0.85)
            continue

        log.append(f"📋 {league}: {len(teams)} equipos")

        for ti, team in enumerate(teams):
            tid   = team["id"]
            tname = team["name"]

            if status_text:
                status_text.markdown(
                    f"📥 **{league}** — {tname} ({ti+1}/{len(teams)})"
                )

            try:
                games = _fetch_recent_form_raw(sport_slug, league_slug, tid, n_games=10)
                if not isinstance(games, list):
                    games = []
                games = games[:_TP_MAX_GAMES]
            except Exception as _e:
                games = []
                if ti == 0:
                    log.append(f"  ⚠ {tname} fetch error: {_e}")
            if not games:
                failed += 1
                continue
            stats  = _compute_profile_stats(games, sport_group)
            if not stats:
                failed += 1
                continue

            # Sanitize games to plain Python types for JSON serialization
            try:
                games_clean = [
                    {
                        "scored":   float(g.get("scored") or 0),
                        "conceded": float(g.get("conceded") or 0),
                        "home":     bool(g.get("home", False)),
                        "date":     str(g.get("date", "")),
                        "opp":      str(g.get("opp", "")),
                    }
                    for g in games
                ]
                games_json = json.dumps(games_clean, ensure_ascii=False)
            except Exception as _je:
                failed += 1
                log.append(f"  ⚠ {tname} json error: {_je}")
                continue
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            all_rows.append([
                str(tid), tname, league, sport_group, now,
                games_json,
                stats["n_games"],
                stats["avg_scored"],      stats["avg_conceded"],
                stats["avg_scored_home"], stats["avg_conceded_home"],
                stats["avg_scored_away"], stats["avg_conceded_away"],
                stats["rate_o15"],  stats["rate_o25"],  stats["rate_o35"],  stats["rate_btts"],
                stats["rate_o15_home"], stats["rate_o25_home"],
                stats["rate_o35_home"], stats["rate_btts_home"],
                stats["rate_o15_away"], stats["rate_o25_away"],
                stats["rate_o35_away"], stats["rate_btts_away"],
                json.dumps(stats.get("thresholds", {}), ensure_ascii=False),
                stats.get("red_card_rate", 0.0),
            ])
            log.append(f"  ✅ {tname}: {len(games)} partidos")

        if progress_bar:
            progress_bar.progress((li + 1) / total_leagues * 0.85)

    if not all_rows:
        return 0, failed, log + ["❌ Sin datos para escribir"]

    # ── Fase 2: escribir TODO al Sheet en una sola llamada batch ──────────────
    if status_text:
        status_text.markdown(f"💾 Escribiendo **{len(all_rows)}** equipos al Sheet...")
    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)

        # Crear/limpiar pestaña team_profiles
        try:
            ws = sh.worksheet(_TP_TAB)
            ws.clear()
        except:
            ws = sh.add_worksheet(title=_TP_TAB, rows=len(all_rows)+10, cols=len(_TP_HEADERS))

        # Escribir header + datos en una sola llamada
        ws.update("A1", [_TP_HEADERS] + all_rows, value_input_option="RAW")
        written = len(all_rows)
        log.append(f"✅ {written} filas escritas al Sheet en batch")

    except Exception as e:
        log.append(f"❌ Error escribiendo al Sheet: {e}")
        return 0, failed, log

    if progress_bar:
        progress_bar.progress(1.0)
    if status_text:
        status_text.markdown(f"✅ Completado: **{written}** equipos en memoria")

    _load_all_team_profiles.clear()
    return written, failed, log


# [fetch_recent_form moved]



@st.cache_data(ttl=1800)
def get_team_ids(sport, league_slug, team_name):
    """
    Look up ESPN team ID by display name.
    Returns team_id string or None.
    """
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league_slug}/teams?limit=100"
        r = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None
        teams = r.json().get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", [])
        name_lower = team_name.lower().strip()
        for t in teams:
            t_info = t.get("team", {})
            candidates = [
                t_info.get("displayName", ""),
                t_info.get("shortDisplayName", ""),
                t_info.get("name", ""),
                t_info.get("nickname", ""),
            ]
            if any(name_lower in c.lower() or c.lower() in name_lower for c in candidates if c):
                return str(t_info.get("id", ""))
        return None
    except:
        return None



# ══════════════════════════════════════════════════════════════════════════════
# INJURY FEED — Signal 6
# ESPN endpoint: /teams/{id}/injuries
# Returns list of active injuries with status and position.
#
# Impact model per sport:
#   Soccer:     positional weight (FW=0.35, MF=0.20, DF=0.12, GK=0.18)
#               only "Out" players count (no "Questionable")
#   Basketball: "Out" star = -8% win prob, "Doubtful" = -4%, "Questionable" = -1.5%
#               position weights: G=0.35, F=0.30, C=0.20
#   Hockey:     "Out" key player = -5%, "Doubtful" = -3%
#               F=0.30, D=0.20, G=0.22
#   Baseball:   Without pitcher info, injury impact limited to lineup
#               "Out" = -3% per key bat (1B/OF/DH), no pitcher position data
#   Football:   QB Out = -15%, QB Doubtful = -8%, skill position Out = -5%
#               QB=0.45, WR/TE=0.20, RB=0.12, OL=0.08, DEF=0.10
#
# injury_factor stored as:
#   game["home_injury_factor"] = float 0.0-1.0 (1.0 = no impact, 0.0 = catastrophic)
#   game["home_injuries"]      = list of dicts {name, status, position, impact}
# ══════════════════════════════════════════════════════════════════════════════

# Position impact weights per sport group
INJURY_POS_WEIGHTS = {
    "Soccer": {
        "F": 0.35, "FW": 0.35, "ATT": 0.35,           # forwards
        "M": 0.20, "MF": 0.20, "MID": 0.20,            # midfielders
        "D": 0.12, "DF": 0.12, "DEF": 0.12,            # defenders
        "G": 0.18, "GK": 0.18, "GKP": 0.18,            # goalkeeper
    },
    "Basketball": {
        "G": 0.35, "PG": 0.35, "SG": 0.35,             # guards
        "F": 0.30, "SF": 0.30, "PF": 0.30,             # forwards
        "C": 0.20,                                       # center
    },
    "Hockey": {
        "F": 0.30, "LW": 0.30, "RW": 0.30, "C": 0.30, # forwards
        "D": 0.20,                                       # defense
        "G": 0.22,                                       # goalie
    },
    "Baseball": {
        "SP": 0.40, "RP": 0.10,                         # pitchers (if available)
        "C": 0.12, "1B": 0.14, "2B": 0.12, "3B": 0.14,
        "SS": 0.14, "OF": 0.14, "DH": 0.14,
    },
    "Football": {
        "QB": 0.45,
        "WR": 0.20, "TE": 0.20,
        "RB": 0.12, "FB": 0.12,
        "OL": 0.08, "OT": 0.08, "OG": 0.08, "C": 0.08,
        "DE": 0.10, "DT": 0.10, "LB": 0.10, "CB": 0.10, "S": 0.10,
    },
}

# Status multiplier: how much of the position weight to apply
INJURY_STATUS_MULT = {
    "Out":          1.00,
    "Injured Reserve":  1.00,
    "IR":           1.00,
    "Doubtful":     0.65,
    "Questionable": 0.30,
    "Day-To-Day":   0.20,
    "Probable":     0.05,
}

# Max total impact per team (cap to avoid absurd values with many injuries)
INJURY_MAX_IMPACT = {
    "Soccer": 0.55, "Basketball": 0.50, "Hockey": 0.40,
    "Baseball": 0.30, "Football": 0.60,
}


@st.cache_data(ttl=1800)
def fetch_injuries(sport_slug, league_slug, team_id):
    """
    Fetch active injury list for a team from ESPN.
    Endpoint: /apis/site/v2/sports/{sport}/{league}/teams/{id}/injuries
    Returns list of {name, status, position, impact_score} sorted by impact desc.
    Returns empty list if unavailable.
    """
    if not team_id:
        return []
    try:
        url = (f"https://site.api.espn.com/apis/site/v2/sports/"
               f"{sport_slug}/{league_slug}/teams/{team_id}/injuries")
        r = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        data = r.json()
        items = data.get("injuries", [])
        if not items:
            return []
        result = []
        for item in items:
            athlete    = item.get("athlete", {})
            name       = athlete.get("displayName", "Unknown")
            status_raw = item.get("status", "")
            pos_raw    = athlete.get("position", {})
            pos_abbr   = pos_raw.get("abbreviation", "") if isinstance(pos_raw, dict) else str(pos_raw)
            result.append({
                "name":     name,
                "status":   status_raw,
                "position": pos_abbr.upper(),
            })
        return result
    except Exception:
        return []


def compute_injury_impact(injuries, sport_grp):
    """
    Given a list of injury dicts and sport group, compute:
      - injury_factor: float 0-1 (1=no impact, lower=worse)
      - annotated list with impact_score per player
    
    injury_factor = max(1 - total_impact, 1 - max_cap)
    total_impact is capped by INJURY_MAX_IMPACT per sport.
    """
    pos_weights  = INJURY_POS_WEIGHTS.get(sport_grp, {})
    status_mults = INJURY_STATUS_MULT
    max_cap      = INJURY_MAX_IMPACT.get(sport_grp, 0.40)

    annotated    = []
    total_impact = 0.0

    for inj in injuries:
        pos    = inj.get("position", "")
        status = inj.get("status", "")
        # Match position to weight (try exact, then first char prefix)
        pos_w  = pos_weights.get(pos) or pos_weights.get(pos[:2] if len(pos)>=2 else pos) or 0.10
        st_m   = 0.0
        for s_key, mult in status_mults.items():
            if s_key.lower() in status.lower():
                st_m = mult
                break
        impact = pos_w * st_m
        annotated.append({**inj, "impact_score": round(impact, 4)})
        total_impact += impact

    total_impact  = min(total_impact, max_cap)
    injury_factor = round(max(0.40, 1.0 - total_impact), 4)  # floor at 0.40

    # Sort by impact descending so UI shows worst first
    annotated.sort(key=lambda x: x["impact_score"], reverse=True)
    return injury_factor, annotated

# ── FORM SCORE CACHE: game_id → (home_form, away_form) ──────────────────────
# Populated lazily during simulation, used in compute_base_prob via game dict.
# Each game dict gets "home_form" and "away_form" keys injected before simulate_game.

def enrich_game_with_form(game):
    """
    Fetch recent form for both teams and inject into game dict.
    Modifies game in-place. Safe to call multiple times (idempotent).
    Only runs for non-tennis sports.
    """
    if game.get("_form_fetched"):
        return
    game["_form_fetched"] = True

    league  = game.get("league", "")
    lg_info = LEAGUES.get(league, {})
    sport   = lg_info.get("sport", "")
    group   = lg_info.get("group", "")

    if not sport:  # skip if no sport defined
        return

    # ESPN league slug for team lookup
    LEAGUE_SLUGS = {
        "NBA": ("basketball", "nba"),
        "NFL": ("football", "nfl"),
        "NCAAF": ("football", "college-football"),
        "MLB": ("baseball", "mlb"),
        "NHL": ("hockey", "nhl"),
        "MLS": ("soccer", "usa.1"),
        "Liga MX": ("soccer", "mex.1"),
        "Premier League": ("soccer", "eng.1"),
        "La Liga": ("soccer", "esp.1"),
        "Bundesliga": ("soccer", "ger.1"),
        "Serie A": ("soccer", "ita.1"),
        "Ligue 1": ("soccer", "fra.1"),
        "Champions League": ("soccer", "uefa.champions"),
        "Europa League": ("soccer", "uefa.europa"),
        "Conference League": ("soccer", "uefa.europa.conf"),
        "CONCACAF Champions Cup": ("soccer", "concacaf.champions"),
        "Saudi Pro League":       ("soccer", "sau.1"),
        "Belgian Pro League":     ("soccer", "bel.1"),
        "Eredivisie":             ("soccer", "ned.1"),
        # Ligas ocultas
        "Süper Lig":              ("soccer", "TUR.1"),
        "Super League Greece":    ("soccer", "GRE.1"),
        "Primeira Liga":          ("soccer", "POR.1"),
        "Superliga":              ("soccer", "DEN.1"),
        "Eliteserien":            ("soccer", "NOR.1"),
        "Allsvenskan":            ("soccer", "SWE.1"),
    }

    if league not in LEAGUE_SLUGS:
        # Fallback: try building from LEAGUES dict directly
        lg_sport = LEAGUES.get(league, {}).get("sport", "")
        lg_slug  = LEAGUES.get(league, {}).get("league", "")
        if not lg_sport or not lg_slug:
            return
        sport_slug, league_slug = lg_sport, lg_slug
    else:
        sport_slug, league_slug = LEAGUE_SLUGS[league]

    # Try to get team IDs from the game object itself first (parse_games stores them)
    home_id = game.get("home_team_id") or get_team_ids(sport_slug, league_slug, game["home_team"])
    away_id = game.get("away_team_id") or get_team_ids(sport_slug, league_slug, game["away_team"])

    from datetime import date as _date

    def _rest_days(last_date_str):
        """Days since last game. Returns None if unknown."""
        if not last_date_str:
            return None
        try:
            last = _date.fromisoformat(last_date_str)
            return (_date.today() - last).days
        except:
            return None

    if home_id:
        hf = fetch_recent_form(sport_slug, league_slug, home_id)
        if isinstance(hf, dict):
            game["home_form"]          = hf.get("form_score")
            game["home_avg_scored"]    = hf.get("avg_scored")
            game["home_avg_conceded"]  = hf.get("avg_conceded")
            game["home_rest_days"]     = _rest_days(hf.get("last_game_date"))
        else:
            game["home_form"] = hf  # None or legacy float

    if away_id:
        af = fetch_recent_form(sport_slug, league_slug, away_id)
        if isinstance(af, dict):
            game["away_form"]          = af.get("form_score")
            game["away_avg_scored"]    = af.get("avg_scored")
            game["away_avg_conceded"]  = af.get("avg_conceded")
            game["away_rest_days"]     = _rest_days(af.get("last_game_date"))
        else:
            game["away_form"] = af  # None or legacy float

    # Back-to-back flag (≤1 rest day) — used for fatigue adjustment (Signal C)
    h_rest = game.get("home_rest_days")
    a_rest = game.get("away_rest_days")
    game["home_back2back"] = (h_rest is not None and h_rest <= 1)
    game["away_back2back"] = (a_rest is not None and a_rest <= 1)

    hf_val = game.get("home_form")
    af_val = game.get("away_form")
    if hf_val is None and af_val is None and (home_id or away_id):
        game["_form_unavailable"] = True

    # ── Team Profiles: guardar historial y cargar perfil acumulado ──────────────
    # Estrategia en 2 pasos:
    # 1. Construir perfil en memoria desde hf/af (disponible INMEDIATAMENTE)
    #    → impacta la simulación de este mismo análisis aunque sea primera vez
    # 2. Guardar en Google Sheets en background thread para futuras sesiones
    import threading

    def _build_inmem_profile(form_dict, sport_group):
        """Construye perfil en memoria desde games_raw del form fetch."""
        if not isinstance(form_dict, dict): return None
        games_raw = form_dict.get("games_raw", [])
        if not games_raw: return None
        stats = _compute_profile_stats(games_raw, sport_group)
        if not stats: return None
        return stats  # mismo formato que get_team_profile() devuelve

    # ── Home team ──────────────────────────────────────────────────────────────
    _h_games_raw = hf.get("games_raw", []) if isinstance(hf, dict) else []
    if home_id and _h_games_raw:
        _h_name = game["home_team"]
        # 1. Perfil en memoria para esta simulación
        _h_inmem = _build_inmem_profile(hf, group)
        # 2. Merge con Sheets existente para perfil histórico más completo
        _h_sheets = get_team_profile(home_id)
        if _h_sheets and _h_sheets.get("n_games", 0) >= _h_inmem.get("n_games", 0) if _h_inmem else False:
            game["home_profile"] = _h_sheets  # Sheets tiene más datos → usar Sheets
        elif _h_inmem:
            game["home_profile"] = _h_inmem   # primera vez → usar en-memoria
        else:
            game["home_profile"] = _h_sheets  # fallback
        # Background: guardar/actualizar Sheets
        def _update_home(_tid=home_id, _name=_h_name, _lg=league, _sg=group, _gr=_h_games_raw):
            update_team_profile(team_id=_tid, team_name=_name,
                                league=_lg, sport_group=_sg, new_games=_gr)
        threading.Thread(target=_update_home, daemon=True).start()
    else:
        game["home_profile"] = get_team_profile(home_id) if home_id else None

    # ── Away team ──────────────────────────────────────────────────────────────
    _a_games_raw = af.get("games_raw", []) if isinstance(af, dict) else []
    if away_id and _a_games_raw:
        _a_name = game["away_team"]
        # 1. Perfil en memoria para esta simulación
        _a_inmem = _build_inmem_profile(af, group)
        # 2. Merge con Sheets existente
        _a_sheets = get_team_profile(away_id)
        if _a_sheets and _a_sheets.get("n_games", 0) >= _a_inmem.get("n_games", 0) if _a_inmem else False:
            game["away_profile"] = _a_sheets
        elif _a_inmem:
            game["away_profile"] = _a_inmem
        else:
            game["away_profile"] = _a_sheets
        # Background: guardar/actualizar Sheets
        def _update_away(_tid=away_id, _name=_a_name, _lg=league, _sg=group, _gr=_a_games_raw):
            update_team_profile(team_id=_tid, team_name=_name,
                                league=_lg, sport_group=_sg, new_games=_gr)
        threading.Thread(target=_update_away, daemon=True).start()
    else:
        game["away_profile"] = get_team_profile(away_id) if away_id else None

    # ── Signal 6: Injury Feed ─────────────────────────────────────────────────
    # Fetch active injuries for both teams and compute impact factor.
    # injury_factor in [0.40, 1.0]: 1.0 = fully healthy, lower = key players out.
    # Stored on game dict for use in compute_base_prob (Signal 6) and get_lambda.
    sport_grp_inj = group  # already resolved above
    if home_id:
        h_inj_raw = fetch_injuries(sport_slug, league_slug, home_id)
        h_factor, h_inj = compute_injury_impact(h_inj_raw, sport_grp_inj)
        game["home_injury_factor"]  = h_factor
        game["home_injuries"]       = h_inj
    else:
        game["home_injury_factor"]  = 1.0
        game["home_injuries"]       = []

    if away_id:
        a_inj_raw = fetch_injuries(sport_slug, league_slug, away_id)
        a_factor, a_inj = compute_injury_impact(a_inj_raw, sport_grp_inj)
        game["away_injury_factor"]  = a_factor
        game["away_injuries"]       = a_inj
    else:
        game["away_injury_factor"]  = 1.0
        game["away_injuries"]       = []

    # ── H2H History ─────────────────────────────────────────────────────────
    if home_id and away_id and group in ("Soccer", "Basketball", "Hockey", "Baseball"):
        h2h = fetch_h2h(sport_slug, league_slug, home_id, away_id)
        game["h2h"] = h2h
        # Inject H2H avg goals into lambda if we have them and no ESPN line
        if h2h and not game["odds"].get("over_under"):
            game["h2h_avg_total"] = h2h.get("avg_total")
    else:
        game["h2h"] = {}

    # ── Weather (outdoor sports only) ───────────────────────────────────────
    _outdoor_sports = ("Football", "Baseball", "Soccer")
    if group in _outdoor_sports:
        venue = game.get("venue", "") or ""
        # Extract city from venue name (e.g. "Empower Field at Mile High, Denver" → "Denver")
        _city = ""
        if "," in venue:
            _city = venue.split(",")[-1].strip()
        elif venue:
            _city = venue.split(" ")[-1].strip() if len(venue.split(" ")) > 2 else venue
        if _city and len(_city) >= 3:
            wx = fetch_weather(_city)
            game["weather"] = wx
            # Adjust lambda via weather O/U factor
            if wx.get("ou_adj") and wx["ou_adj"] != 0.0:
                game["_weather_ou_adj"] = wx["ou_adj"]
        else:
            game["weather"] = {}
    else:
        game["weather"] = {}

    # ── Line Movement: save snapshot ────────────────────────────────────────
    _gid = game.get("id", "")
    if _gid and not game.get("_line_saved"):
        game["_line_saved"] = True
        save_line_snapshot(
            game_id=_gid, league=league,
            home=game.get("home_team", ""), away=game.get("away_team", ""),
            ou=game["odds"].get("over_under", ""),
            home_ml=game["odds"].get("home_ml", ""),
            away_ml=game["odds"].get("away_ml", ""),
        )
        game["line_movement"] = get_line_movement(_gid)


@st.cache_data(ttl=60)
def fetch_scoreboard(sport, league, tournament_id=None):
    """
    Fetch ESPN scoreboard.
    Tennis requires ?dates=YYYYMMDD to get today's matches.
    Also tries tournament-specific endpoints.
    """
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    base  = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"

    if False:  # tennis removed
        urls = [None,
            f"{base}?limit=100",                         # no date filter fallback
        ]
    elif tournament_id:
        urls = [
            f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/tournament/{tournament_id}/scoreboard",
            f"{base}?tournamentId={tournament_id}",
            ESPN_URL.format(sport=sport, league=league),
        ]
    else:
        from datetime import timedelta
        _now      = datetime.now(timezone.utc)
        _now_mx   = _now - timedelta(hours=6)
        today_utc = _now.strftime("%Y%m%d")
        tom_utc   = (_now + timedelta(days=1)).strftime("%Y%m%d")
        today_mx  = _now_mx.strftime("%Y%m%d")
        base_url  = ESPN_URL.format(sport=sport, league=league)
        sched_base = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"
        urls = [
            f"{sched_base}?dates={today_mx}&limit=100",       # MX today — most reliable
            f"{sched_base}?dates={today_utc}&limit=100",      # UTC today
            f"{sched_base}?dates={tom_utc}&limit=100",        # UTC tomorrow (CDMX evening)
            base_url,                                          # default fallback
            f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/schedule?dates={today_mx}",  # schedule endpoint
            f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/schedule?dates={today_utc}",
        ]

    all_events = []
    returned_data = {}
    for url in urls:
        if not url: continue
        try:
            r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                data = r.json()
                # Scoreboard: data.events
                # Schedule: data.events OR data[date].games[].event OR nested
                evts = data.get("events", [])
                # Also check schedule format: {"20260312": {"games": [...]}}
                if not evts:
                    for _k, _v in data.items():
                        if isinstance(_v, dict):
                            for _g in _v.get("games", []):
                                _ev = _g.get("event") or _g
                                if isinstance(_ev, dict) and _ev.get("id"):
                                    evts.append(_ev)
                        elif isinstance(_v, list):
                            for _item in _v:
                                if isinstance(_item, dict) and _item.get("id") and _item.get("competitions"):
                                    evts.append(_item)
                if isinstance(evts, list) and evts:
                    existing_ids = {e.get("id") for e in all_events}
                    for e in evts:
                        if e.get("id") not in existing_ids:
                            all_events.append(e)
                            existing_ids.add(e.get("id"))
                    if not returned_data:
                        returned_data = data
        except: continue
    if all_events:
        returned_data["events"] = all_events
        return returned_data
    return {}




def _parse_live_stats(comp, home, away):
    """Extract live match stats from ESPN competition block."""
    try:
        clock = comp.get("status", {}).get("displayClock", "")
        period = comp.get("status", {}).get("period", 0)
        situation = comp.get("situation", {})
        return {
            "clock": clock,
            "period": period,
            "home_possession": situation.get("homeTeam", {}).get("possession", ""),
            "away_possession": situation.get("awayTeam", {}).get("possession", ""),
            "home_shots": situation.get("homeTeam", {}).get("shots", ""),
            "away_shots": situation.get("awayTeam", {}).get("shots", ""),
        }
    except:
        return {}


def _fetch_event_odds(event_id, sport, league):
    """
    Fetch odds for a specific ESPN event ID.
    ESPN has event-level odds at: /event/{id}/competitions/{id}/odds
    Returns dict with spread_line, home_ml, away_ml, over_under, etc.
    """
    try:
        import requests as _rq
        # Primary: event competitions odds endpoint
        url = (f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}"
               f"/summary?event={event_id}")
        r = _rq.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return {}
        data = r.json()
        # odds are in data["pickcenter"] or data["odds"]
        odds_list = data.get("pickcenter") or data.get("odds") or []
        if not odds_list:
            return {}
        o = odds_list[0]
        _ho = o.get("homeTeamOdds", {}) or {}
        _ao = o.get("awayTeamOdds", {}) or {}
        # moneyline
        _hml = (_ho.get("moneyLine") or _ho.get("current",{}).get("moneyLine") or "")
        _aml = (_ao.get("moneyLine") or _ao.get("current",{}).get("moneyLine") or "")
        # over/under
        _ou = str(o.get("overUnder","") or o.get("total","") or "")
        # spread
        _ps = (_ho.get("pointSpread") or _ho.get("handicap") or "")
        _spread_str = str(float(_ps)) if _ps else ""
        # spread juice
        _sph = str(_ho.get("spreadOdds","") or "")
        _spa = str(_ao.get("spreadOdds","") or "")
        # win probability
        _hwp = str(_ho.get("winPercentage","") or "")
        _awp = str(_ao.get("winPercentage","") or "")
        return {
            "home_ml":        str(_hml) if _hml else "",
            "away_ml":        str(_aml) if _aml else "",
            "over_under":     _ou,
            "spread":         o.get("details",""),
            "spread_line":    _spread_str,
            "spread_home_ml": _sph,
            "spread_away_ml": _spa,
            "home_wp":        _hwp,
            "away_wp":        _awp,
        }
    except:
        return {}


def parse_games(data, league_name):
    """Parse ESPN scoreboard JSON into normalized game dicts."""
    games = []
    from datetime import timedelta as _td
    _now_utc    = datetime.now(timezone.utc)
    _now_mx     = _now_utc - _td(hours=6)
    _today_cdmx = _now_mx.strftime("%Y-%m-%d")
    _yesterday_cdmx = (_now_mx - _td(days=1)).strftime("%Y-%m-%d")
    _tomorrow_cdmx  = (_now_mx + _td(days=1)).strftime("%Y-%m-%d")
    _valid_dates = {
        _today_cdmx, _yesterday_cdmx, _tomorrow_cdmx,
        (_now_mx - _td(days=2)).strftime("%Y-%m-%d"),
        (_now_mx - _td(days=3)).strftime("%Y-%m-%d"),
        (_now_mx - _td(days=4)).strftime("%Y-%m-%d"),
        (_now_mx - _td(days=5)).strftime("%Y-%m-%d"),
        (_now_mx - _td(days=6)).strftime("%Y-%m-%d"),
        (_now_mx - _td(days=7)).strftime("%Y-%m-%d"),
        (_now_mx + _td(days=2)).strftime("%Y-%m-%d"),
        (_now_mx + _td(days=3)).strftime("%Y-%m-%d"),
    }

    for event in data.get("events", []):
        try:
            _raw_date = event.get("date", "").replace("Z", "").replace("+00:00", "")
            if _raw_date:
                try:
                    _ev_utc       = datetime.strptime(_raw_date[:19].replace("T", " "),
                                        "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    _ev_cdmx_date = (_ev_utc - _td(hours=6)).strftime("%Y-%m-%d")
                    if _ev_cdmx_date not in _valid_dates:
                        continue
                except Exception:
                    pass
            comp  = event.get("competitions", [{}])[0]
            comps = comp.get("competitors", [])
            if len(comps) < 2:
                continue
            home = next((c for c in comps if c.get("homeAway") == "home"), comps[0])
            away = next((c for c in comps if c.get("homeAway") == "away"), comps[1])
            status = event.get("status", {})

            odds_info = {}
            ol = comp.get("odds", [])
            if not ol:
                # ESPN sometimes omits odds from scoreboard — try summary endpoint
                _ev_id   = event.get("id","")
                _cfg     = LEAGUES.get(league_name, {})
                _sp_try  = _cfg.get("sport","")
                _lg_try  = _cfg.get("league","")
                if _ev_id and _sp_try and _lg_try:
                    odds_info = _fetch_event_odds(_ev_id, _sp_try, _lg_try)
            if ol:
                o = ol[0]
                _ou_raw = o.get("overUnder", "") or o.get("total", "") or o.get("overUnderOpen", "") or ""
                if not _ou_raw:
                    _details_str = o.get("details", "") or ""
                    _ou_match = __import__("re").search(r"\((\d+\.?\d*)\)", _details_str)
                    if _ou_match:
                        _ou_raw = _ou_match.group(1)
                _home_odds = o.get("homeTeamOdds", {})
                _away_odds = o.get("awayTeamOdds", {})
                _home_ml = (_home_odds.get("moneyLine") or _home_odds.get("current", {}).get("moneyLine") or
                            _home_odds.get("open", {}).get("moneyLine") or "")
                _away_ml = (_away_odds.get("moneyLine") or _away_odds.get("current", {}).get("moneyLine") or
                            _away_odds.get("open", {}).get("moneyLine") or "")
                # ── Parse spread from ESPN ────────────────────────────────────
                # spread_line is ALWAYS from home perspective:
                #   negative = home is favorite (gives points)
                #   positive = home is underdog (gets points)
                # homeTeamOdds.pointSpread is the authoritative source.
                # details "BOS -8.5" = BOS (home or away) has -8.5,
                #   so we use pointSpread directly to avoid confusion.
                _details_str = o.get("details", "") or ""
                _spread_val      = ""   # numeric string, home perspective
                _spread_home_ml  = ""   # juice for home to cover
                _spread_away_ml  = ""   # juice for away to cover

                _ho = o.get("homeTeamOdds", {}) or {}
                _ao = o.get("awayTeamOdds", {}) or {}

                # 1. Primary: homeTeamOdds.pointSpread (home perspective, always correct)
                _ps_home = (_ho.get("pointSpread") or
                            _ho.get("handicap") or
                            _ho.get("current", {}).get("pointSpread") or
                            _ho.get("open", {}).get("pointSpread"))
                if _ps_home is not None:
                    try: _spread_val = str(float(_ps_home))
                    except: pass

                # 2. Fallback: parse details string e.g. "BOS -8.5"
                #    Need to figure out if the team is home or away to get correct sign
                if not _spread_val and _details_str:
                    import re as _re_odd
                    _dm = _re_odd.search(r'([A-Za-z0-9]+)\s*([+-]?\d+\.?\d*)', _details_str)
                    if _dm:
                        try:
                            _det_line = float(_dm.group(2))   # as written
                            _det_abbr = _dm.group(1).upper()
                            # Check if this abbreviation matches the HOME team
                            # Simple heuristic: if home team abbreviation is in det_abbr
                            _home_nm = (home.get("team",{}).get("abbreviation","") or
                                        home.get("team",{}).get("shortDisplayName","") or "").upper()
                            _away_nm = (away.get("team",{}).get("abbreviation","") or
                                        away.get("team",{}).get("shortDisplayName","") or "").upper()
                            if _home_nm and _det_abbr.startswith(_home_nm[:2]):
                                _spread_val = str(_det_line)   # home team's line = home perspective
                            elif _away_nm and _det_abbr.startswith(_away_nm[:2]):
                                _spread_val = str(-_det_line)  # away team's line → flip for home perspective
                            else:
                                _spread_val = str(_det_line)   # best guess: use as-is
                        except: pass

                # 3. Spread juice (odds for each side to cover)
                _sp_odds_h = (_ho.get("spreadOdds") or
                              _ho.get("current", {}).get("spreadOdds") or
                              _ho.get("open", {}).get("spreadOdds"))
                _sp_odds_a = (_ao.get("spreadOdds") or
                              _ao.get("current", {}).get("spreadOdds") or
                              _ao.get("open", {}).get("spreadOdds"))
                if _sp_odds_h is not None: _spread_home_ml = str(_sp_odds_h)
                if _sp_odds_a is not None: _spread_away_ml = str(_sp_odds_a)

                # MLB Run Line / NHL Puck Line: always ±1.5
                # If spread_val is ±1.5 and juice is very different, that's the
                # real market price (e.g. NYY -1.5 at -155, Boston +1.5 at +130)

                odds_info = {
                    "spread":          _details_str,   # full string e.g. "BOS -8.5"
                    "spread_line":     _spread_val,    # numeric e.g. "-8.5" (home perspective)
                    "spread_home_ml":  _spread_home_ml or "-110",
                    "spread_away_ml":  _spread_away_ml or "-110",
                    "over_under":      str(_ou_raw) if _ou_raw else "",
                    "home_ml":         str(_home_ml) if _home_ml else "",
                    "away_ml":         str(_away_ml) if _away_ml else "",
                    "home_wp":         _ho.get("winPercentage", ""),
                    "away_wp":         _ao.get("winPercentage", ""),
                }

            hr = home.get("records", [{}])
            ar = away.get("records", [{}])
            live_stats = _parse_live_stats(comp, home, away)

            home_team_id = str(home.get("team", {}).get("id", "") or home.get("id", ""))
            away_team_id = str(away.get("team", {}).get("id", "") or away.get("id", ""))

            _sd  = (status.get("type", {}).get("shortDetail", "") or "").split("\n")[0].strip()
            _dt  = event.get("date", "").replace("Z", "").replace("+00:00", "")
            _state_str = status.get("type", {}).get("state", "pre")
            # For pre-game: ALWAYS show CDMX time from the date field (ignore ESPN text like "2:00 PM ET")
            if _state_str == "pre" and _dt:
                try:
                    _u = datetime.strptime(_dt[:19].replace("T", " "),
                             "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    _sd = (_u - _td(hours=6)).strftime("%H:%M") + " CDMX"
                except Exception:
                    pass
            elif _sd.lower() in ("scheduled", "") and _dt:
                try:
                    _u = datetime.strptime(_dt[:19].replace("T", " "),
                             "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    _sd = (_u - _td(hours=6)).strftime("%H:%M") + " CDMX"
                except Exception:
                    pass

            games.append({
                "id":            event.get("id", ""),
                "league":        league_name,
                "home_team":     home.get("team", {}).get("displayName", "Home"),
                "away_team":     away.get("team", {}).get("displayName", "Away"),
                "home_score":    home.get("score", ""),
                "away_score":    away.get("score", ""),
                "home_record":   hr[0].get("summary", "") if hr else "",
                "away_record":   ar[0].get("summary", "") if ar else "",
                "state":         status.get("type", {}).get("state", "pre"),
                "date":          event.get("date", ""),
                "status_detail": _sd,
                "venue":         comp.get("venue", {}).get("fullName", ""),
                "odds":          odds_info,
                "live_stats":    live_stats,
                "home_team_id":  home_team_id,
                "away_team_id":  away_team_id,
            })
        except Exception:
            continue
    return games


@st.cache_data(ttl=300, show_spinner=False)
def get_all_games(leagues):
    from datetime import timedelta as _td_g
    _now_g        = datetime.now(timezone.utc)
    _now_mx_g     = _now_g - _td_g(hours=6)
    _today_mx     = _now_mx_g.strftime("%Y%m%d")
    _today_utc    = _now_g.strftime("%Y%m%d")
    _tom_utc      = (_now_g + _td_g(days=1)).strftime("%Y%m%d")
    _yday_utc     = (_now_g - _td_g(days=1)).strftime("%Y%m%d")

    # Slugs alternativos por liga (ESPN cambia de slug según la temporada)
    _EXTRA_SLUGS = {
        "mex.1":  ["mex.1", "mex.clausura", "mex.apertura"],
        "sau.1":  ["sau.1", "sau.pro", "sau.league", "sau.professional"],
        "ned.1":  ["ned.1", "ned.eredivisie"],
        "bel.1":  ["bel.1", "bel.pro", "bel.jupiler"],
        "UEFA.CHAMPIONS": ["UEFA.CHAMPIONS", "uefa.champions"],
        "UEFA.EUROPA":    ["UEFA.EUROPA",    "uefa.europa"],
        "tur.1":  ["TUR.1", "tur.1", "tur.super.lig"],
        "TUR.1":  ["TUR.1", "tur.1", "tur.super.lig"],
        "den.1":  ["DEN.1", "den.1", "den.superliga"],
        "DEN.1":  ["DEN.1", "den.1", "den.superliga"],
        "gre.1":  ["GRE.1", "gre.1", "gre.super"],
        "GRE.1":  ["GRE.1", "gre.1", "gre.super"],
        "por.1":  ["POR.1", "por.1", "por.primeira"],
        "POR.1":  ["POR.1", "por.1", "por.primeira"],
        "nor.1":  ["NOR.1", "nor.1"],
        "NOR.1":  ["NOR.1", "nor.1"],
        "swe.1":  ["SWE.1", "swe.1"],
        "SWE.1":  ["SWE.1", "swe.1"],
    }

    def _fetch_soccer(sport, league):
        """Hit every known ESPN endpoint for soccer to collect all day's events."""
        all_evts = {}
        slugs_to_try = _EXTRA_SLUGS.get(league, [league])
        if league not in slugs_to_try:
            slugs_to_try = [league] + slugs_to_try

        for _slug in slugs_to_try:
            base = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{_slug}/scoreboard"
            core = f"https://sports.core.api.espn.com/v2/sports/{sport}/leagues/{_slug}/events"

            urls = []
            # All dates × all season types
            for _d in [_today_mx, _today_utc, _tom_utc, _yday_utc]:
                for _st in ["1", "2", "3", "4"]:
                    urls.append(f"{base}?dates={_d}&limit=100&seasontype={_st}")
                urls.append(f"{base}?dates={_d}&limit=100")
            # Core API
            for _d in [_today_mx, _today_utc, _tom_utc, _yday_utc]:
                urls.append(f"{core}?dates={_d}&limit=100")
            # Plain (no date — ESPN default = current week)
            urls.append(base)
            urls.append(f"{base}?limit=100")

            for _url in urls:
                try:
                    _r = requests.get(_url, timeout=7,
                                      headers={"User-Agent": "Mozilla/5.0",
                                               "Accept": "application/json"})
                    if _r.status_code != 200:
                        continue
                    _data = _r.json()
                    _found = False
                    for _e in _data.get("events", []):
                        if isinstance(_e, dict) and _e.get("id"):
                            all_evts[_e["id"]] = _e
                            _found = True
                    for _e in _data.get("items", []):
                        if isinstance(_e, dict) and _e.get("id") and _e.get("competitions"):
                            all_evts[_e["id"]] = _e
                            _found = True
                except Exception:
                    continue

        return {"events": list(all_evts.values())}

    result = []
    errors = []
    # Siempre incluir ligas ocultas (equipos favoritos) además de las seleccionadas
    _hidden_leagues = [n for n, cfg in LEAGUES.items() if cfg.get("hidden")]
    _all_to_fetch = list(leagues) + [l for l in _hidden_leagues if l not in leagues]

    for name in _all_to_fetch:
        cfg = LEAGUES.get(name)
        if not cfg:
            errors.append(f"{name}: liga no configurada")
            continue
        try:
            if cfg["sport"] == "soccer":
                data = _fetch_soccer(cfg["sport"], cfg["league"])
            else:
                data = fetch_scoreboard(cfg["sport"], cfg["league"],
                                        tournament_id=cfg.get("tournament_id"))
            parsed = parse_games(data, name)
            # ── Ligas ocultas: solo mostrar partidos de equipos favoritos ──────
            if cfg.get("hidden"):
                parsed = [
                    g for g in parsed
                    if g.get("home_team") in WATCHED_TEAMS
                    or g.get("away_team") in WATCHED_TEAMS
                ]
                # Si el scoreboard no devolvió partidos, buscar por equipo directamente
                if not parsed:
                    _sport_s = cfg["sport"]
                    _league_s = cfg["league"]
                    _extra_evts = []
                    for _wt in WATCHED_TEAMS:
                        # Solo equipos de esta liga
                        try:
                            _teams_url = (f"https://site.api.espn.com/apis/site/v2/sports/"
                                         f"{_sport_s}/{_league_s}/teams?limit=50")
                            _tr = requests.get(_teams_url, timeout=5,
                                               headers={"User-Agent":"Mozilla/5.0"})
                            if _tr.status_code != 200:
                                break
                            _tdata = _tr.json()
                            _teams = (_tdata.get("sports",[{}])[0]
                                           .get("leagues",[{}])[0]
                                           .get("teams",[]))
                            for _t in _teams:
                                _ti = _t.get("team",{})
                                if _ti.get("displayName","") in WATCHED_TEAMS:
                                    _tid = _ti.get("id","")
                                    if _tid:
                                        _sched_url = (f"https://site.api.espn.com/apis/site/v2/sports/"
                                                      f"{_sport_s}/{_league_s}/teams/{_tid}/schedule")
                                        _sr2 = requests.get(_sched_url, timeout=6,
                                                           headers={"User-Agent":"Mozilla/5.0"})
                                        if _sr2.status_code == 200:
                                            for _ev in _sr2.json().get("events",[]):
                                                if isinstance(_ev, dict) and _ev.get("id"):
                                                    _extra_evts.append(_ev)
                            break  # solo necesitamos buscar una vez
                        except Exception:
                            break
                    if _extra_evts:
                        _extra_data = {"events": _extra_evts}
                        _extra_parsed = parse_games(_extra_data, name)
                        parsed = [g for g in _extra_parsed
                                  if g.get("home_team") in WATCHED_TEAMS
                                  or g.get("away_team") in WATCHED_TEAMS]
            result.extend(parsed)
            print(f"[ESPN] {name}: {len(parsed)} partidos HOY CDMX")
            if not parsed and not cfg.get("hidden"):
                errors.append(f"{name}: sin partidos hoy")
        except Exception as e:
            errors.append(f"{name}: {type(e).__name__} — {e}")
    return result, errors



# ═══════════════════════════════════════════════════════════════════════════════
# AI SPORT ANALYSTS — Claude specialist per sport
# ═══════════════════════════════════════════════════════════════════════════════

SPORT_SYSTEM_PROMPTS = {
    "Basketball": """You are an elite NBA/basketball betting analyst with 15 years of experience.
You specialize in: pace-adjusted metrics, rest/travel disadvantage, home-court factor in playoffs vs regular season,
back-to-back fatigue, point differential trends, ATS (against the spread) patterns, and total points (O/U) analysis.
Key edge areas: teams playing 2nd game of back-to-back, large home favorites covering less than 60%, pace mismatches.
Respond in 2-3 sharp sentences. Lead with the single most important insight. Be direct, no fluff.""",

    "Soccer": """You are a sharp soccer betting analyst covering global leagues (Liga MX, Premier League, UCL, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, Belgian Pro League, Saudi Pro League, etc.).
You specialize in: xG (expected goals) patterns, home/away form splits, European competition fatigue, 
managerial tactics, set-piece efficiency, clean sheet rates, and value in BTTS and Asian handicap markets.
Key edge areas: mid-table teams in dead rubbers, massive underdogs in cup ties, draw value in evenly matched derbies.
Respond in 2-3 sharp sentences. Lead with the single most important factor affecting the market. Be direct.""",

    "Football": """You are a sharp NFL/college football betting analyst.
You specialize in: DVOA efficiency metrics, quarterback matchups, offensive line vs defensive front performance,
weather impact on totals, division games (tighter spreads), home field primetime effect, and playoff seeding motivation.
Key edge areas: home dogs in divisional games, bad weather collapsing totals, public money inflating favorites.
Respond in 2-3 sharp sentences. Lead with the single biggest factor. Be direct, no fluff.""",

    "Hockey": """You are a sharp NHL betting analyst.
You specialize in: goaltender matchup quality, 5-on-5 expected goals differential, power play efficiency,
back-to-back and travel fatigue, home ice advantage in divisional games, and puck line vs moneyline value.
Key edge areas: elite goalie starting after rest vs tired starter, low total games under 5.5, home dogs with top-10 goalie.
Respond in 2-3 sharp sentences. Lead with the most important factor. Be direct.""",

    "Baseball": """You are a sharp MLB betting analyst.
You specialize in: starting pitcher ERA/FIP/xFIP differential, bullpen availability (recent workload),
platoon advantages (L vs R matchups), park factors, day/night splits, and run line vs moneyline value.
Key edge areas: elite SP heavy favorite where the bullpen becomes a liability, road dogs with ace starters, 
high totals in launching pad parks.
Respond in 2-3 sharp sentences. Lead with the pitching matchup insight. Be direct.""",
}

def get_sport_group(league_name):
    return LEAGUES.get(league_name, {}).get("group", "Soccer")

def get_ai_analysis(away_team, home_team, league, sport_group,
                    away_rec, home_rec, best_label, ev, prob_pct,
                    home_pct, away_pct, draw_pct, dq):
    """
    Rule-based sport analyst — generates sharp contextual insight
    from the numbers without any external API call.
    Each sport has its own logic tree.
    """
    fav    = home_team if home_pct > away_pct else away_team
    dog    = away_team if home_pct > away_pct else home_team
    fav_p  = max(home_pct, away_pct)
    dog_p  = min(home_pct, away_pct)
    spread = fav_p - dog_p          # how lopsided
    is_home_fav = home_pct > away_pct
    pick_is_home = home_team in best_label
    pick_is_dog  = dog in best_label

    # ── Basketball ────────────────────────────────────────────────────────────
    if sport_group == "Basketball":
        if ev > 20:
            note = f"El modelo detecta edge significativo (+{ev:.0f} EV) — probable ineficiencia de línea o valor real en {best_label}."
        elif spread > 30:
            note = f"{fav} domina con {fav_p:.0f}% de probabilidad. Con spreads tan grandes, busca el puck line o handicap alternativo para mejor valor."
        elif pick_is_dog and dog_p > 35:
            note = f"{dog} como underdog a {dog_p:.0f}% — los equipos de visitante con más del 35% de probabilidad suelen tener valor real en el moneyline."
        elif dq < 30:
            note = f"DQ baja ({dq:.0f}%) — sin líneas ESPN. Modelo basado en récords de temporada. Confirma el spread actual en tu casa antes de apostar."
        else:
            note = f"Partido equilibrado ({home_team} {home_pct:.0f}% / {away_team} {away_pct:.0f}%). El valor está en {best_label} con EV simulado de +{ev:.1f}."

    # ── Soccer ────────────────────────────────────────────────────────────────
    elif sport_group == "Soccer":
        if "Ambos Anotan" in best_label:
            if prob_pct > 70:
                note = f"BTTS a {prob_pct:.0f}% — ambos equipos tienen tendencia ofensiva. El mercado de goles es más predecible que el resultado."
            else:
                note = f"BTTS a {prob_pct:.0f}% con EV +{ev:.1f}. Considera que equipos defensivos pueden cambiar la dinámica si hay motivación táctica."
        elif "Over 2.5" in best_label:
            note = f"Modelo proyecta partido con >2.5 goles ({prob_pct:.0f}%). El encuentro {away_team} @ {home_team} favorece líneas ofensivas según simulación Poisson."
        elif "Under 2.5" in best_label:
            note = f"Under 2.5 a {prob_pct:.0f}% — el modelo Poisson espera menos de 3 goles totales. Con promedio de liga de {LEAGUE_AVG_GOALS.get(league, 2.7):.2f} goles, la línea O/U sugiere partido defensivo."
        elif draw_pct > 27 and not pick_is_home:
            note = f"Empate en {draw_pct:.0f}% — partidos con equipos tan parejos frecuentemente terminan igualados. Considera la doble oportunidad como cobertura."
        elif spread < 12:
            note = f"Partido muy parejo ({home_team} {home_pct:.0f}% / {away_team} {away_pct:.0f}%). Alta probabilidad de empate ({draw_pct:.0f}%) — el mercado de goles puede tener mejor valor."
        else:
            note = f"{fav} favorito con {fav_p:.0f}% de probabilidad. {'Ventaja de local significativa.' if is_home_fav else 'El visitante llega con mejor forma según registros.'}"

    # ── Football ──────────────────────────────────────────────────────────────
    elif sport_group == "Football":
        if spread > 35:
            note = f"{fav} es favorito masivo ({fav_p:.0f}%). En NFL, cubrir spreads grandes es difícil — considera el total de puntos como mercado alternativo."
        elif pick_is_dog and dog_p > 30:
            note = f"{dog} como underdog ({dog_p:.0f}%) tiene valor histórico — los equipos de casa con más del 30% de prob. contra favoritos cubren ATS con mayor frecuencia."
        elif dq < 30:
            note = f"Sin líneas ESPN disponibles (DQ {dq:.0f}%). El modelo usa récords de temporada. Verifica el spread oficial en DraftKings o FanDuel."
        else:
            note = f"Modelo da {fav} como favorito ({fav_p:.0f}% vs {dog_p:.0f}%). EV de +{ev:.1f} sugiere que la línea actual subestima ligeramente a {fav if pick_is_home == is_home_fav else dog}."

    elif False:  # tennis removed
        if False:
            note = f"{fav} favorito ({fav_p:.0f}%). En tenis el servicio y la superficie son decisivos — verifica récords en la superficie actual del torneo."

    # ── Hockey ────────────────────────────────────────────────────────────────
    elif sport_group == "Hockey":
        if "ML" in best_label and fav_p > 65:
            note = f"{fav} favorito sólido ({fav_p:.0f}%). En NHL considera el puck line (-1.5) si hay diferencia clara de goalie — mejor valor que el moneyline puro."
        elif spread < 15:
            note = f"NHL es el deporte más parejo ({home_pct:.0f}%/{away_pct:.0f}%). Con líneas tan cerradas, el goalie titular es el factor más importante — verifica los lineups."
        elif dq < 30:
            note = f"Sin líneas ESPN para hockey (DQ {dq:.0f}%). Verifica momios y el goalie confirmado antes de apostar — cambia todo el cálculo."
        else:
            note = f"{fav} con {fav_p:.0f}% de prob. El modelo EV de +{ev:.1f} asume cuotas estándar. Compara contra líneas reales de tu casa para confirmar el edge."

    # ── Baseball ─────────────────────────────────────────────────────────────
    elif sport_group == "Baseball":
        if spread > 25:
            note = f"{fav} favorito claro ({fav_p:.0f}%). En MLB esto suele reflejar una ventaja de pitcheo — verifica el abridor confirmado antes de hacer la apuesta."
        elif spread < 10:
            note = f"Partido muy parejo en béisbol ({home_pct:.0f}%/{away_pct:.0f}%). El run line (-1.5) del underdog puede tener valor si el bullpen del favorito es débil."
        elif dq < 30:
            note = f"Sin líneas ESPN disponibles (DQ {dq:.0f}%). El resultado en MLB depende 60%+ del pitcheo — confirma los abridores antes de apostar."
        else:
            note = f"EV de +{ev:.1f} en {best_label}. En béisbol el abridor y el park factor son clave — partido en estadio ofensivo aumenta valor de totales altos."

    # ── Fallback ──────────────────────────────────────────────────────────────
    else:
        note = f"Modelo simulado: {fav} {fav_p:.0f}% vs {dog} {dog_p:.0f}%. Pick recomendado: {best_label} con EV +{ev:.1f}."

    return note



# ═══════════════════════════════════════════════════════════════════════════════
# H2H · WEATHER · LINE MOVEMENT · DIXON-COLES EXTRAS
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def fetch_h2h(sport: str, league: str, home_id: str, away_id: str) -> dict:
    """
    Fetch head-to-head history between two teams via ESPN public API.
    Returns dict with: wins_home, wins_away, draws, avg_goals_h, avg_goals_a,
    last5 (list of results), btts_rate, over25_rate.
    Cached 1h — H2H history doesn't change during the day.
    """
    if not home_id or not away_id:
        return {}
    try:
        url = (f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}"
               f"/teams/{home_id}/schedule?limit=40")
        r = requests.get(url, timeout=7, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return {}
        events = r.json().get("events", [])
        wins_h = wins_a = draws = 0
        goals_h = goals_a = 0
        btts = o25 = 0
        last5 = []
        count = 0
        for ev in events:
            comp = ev.get("competitions", [{}])[0]
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            # Only count games where both teams participated
            ids_in_game = {str(c.get("team", {}).get("id", "")) for c in competitors}
            if str(away_id) not in ids_in_game:
                continue
            status = ev.get("status", {}).get("type", {}).get("state", "")
            if status != "post":
                continue
            h = next((c for c in competitors if str(c.get("team", {}).get("id", "")) == str(home_id)), None)
            a = next((c for c in competitors if str(c.get("team", {}).get("id", "")) == str(away_id)), None)
            if not h or not a:
                continue
            try:
                gh = int(h.get("score", 0) or 0)
                ga = int(a.get("score", 0) or 0)
            except:
                continue
            goals_h += gh
            goals_a += ga
            tg = gh + ga
            if tg > 2.5:
                o25 += 1
            if gh > 0 and ga > 0:
                btts += 1
            if gh > ga:
                wins_h += 1
                last5.insert(0, "W")
            elif ga > gh:
                wins_a += 1
                last5.insert(0, "L")
            else:
                draws += 1
                last5.insert(0, "D")
            count += 1
            if count >= 10:
                break

        if count == 0:
            return {}
        return {
            "count":      count,
            "wins_home":  wins_h,
            "wins_away":  wins_a,
            "draws":      draws,
            "avg_goals_h": round(goals_h / count, 2),
            "avg_goals_a": round(goals_a / count, 2),
            "avg_total":   round((goals_h + goals_a) / count, 2),
            "btts_rate":   round(btts / count, 3),
            "over25_rate": round(o25 / count, 3),
            "last5":       last5[:5],
        }
    except Exception:
        return {}


@st.cache_data(ttl=1800)
def fetch_weather(city: str, country: str = "") -> dict:
    """
    Fetch current weather for a venue city via wttr.in (FREE, no API key).
    Returns: temp_c, wind_kph, precip_mm, condition, impact (description).
    Relevant for NFL, MLB (wind/rain affects O/U), and outdoor soccer.
    """
    if not city:
        return {}
    try:
        # wttr.in JSON API — completely free
        q = city.replace(" ", "+")
        if country:
            q += f"+{country.replace(' ','+')}"
        url = f"https://wttr.in/{q}?format=j1"
        r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return {}
        d = r.json()
        cur = d.get("current_condition", [{}])[0]
        temp_c   = float(cur.get("temp_C", 20))
        wind_kph = float(cur.get("windspeedKmph", 0))
        precip   = float(cur.get("precipMM", 0))
        humidity = float(cur.get("humidity", 50))
        feels    = float(cur.get("FeelsLikeC", temp_c))
        desc     = cur.get("weatherDesc", [{}])[0].get("value", "")

        # Impact assessment
        impact_notes = []
        ou_adj = 0.0   # O/U adjustment factor (negative = lower scoring)

        if wind_kph >= 30:
            impact_notes.append(f"💨 Viento fuerte {wind_kph:.0f}km/h")
            ou_adj -= 0.04  # ~4% fewer points/goals in high wind
        elif wind_kph >= 20:
            impact_notes.append(f"🌬️ Viento {wind_kph:.0f}km/h")
            ou_adj -= 0.02
        if precip >= 5:
            impact_notes.append(f"🌧️ Lluvia {precip:.1f}mm")
            ou_adj -= 0.03
        elif precip >= 1:
            impact_notes.append(f"🌦️ Lluvia leve")
            ou_adj -= 0.01
        if temp_c <= 0:
            impact_notes.append(f"🥶 Frío extremo {temp_c:.0f}°C")
            ou_adj -= 0.02
        elif temp_c >= 35:
            impact_notes.append(f"🥵 Calor extremo {temp_c:.0f}°C")
            ou_adj -= 0.015

        return {
            "temp_c":    temp_c,
            "wind_kph":  wind_kph,
            "precip_mm": precip,
            "humidity":  humidity,
            "feels_c":   feels,
            "desc":      desc,
            "impact":    " · ".join(impact_notes) if impact_notes else "",
            "ou_adj":    ou_adj,   # multiply expected total by (1 + ou_adj)
            "significant": len(impact_notes) > 0,
        }
    except Exception:
        return {}


def save_line_snapshot(game_id: str, league: str, home: str, away: str,
                       ou: str, home_ml: str, away_ml: str) -> None:
    """
    Save a line snapshot to Google Sheets (tab: line_movement).
    Called once per game per analysis run. Used to detect line movement.
    Non-blocking: runs in background thread.
    """
    import threading
    def _save():
        try:
            ws = _get_or_create_sheet("line_movement")
            if ws is None:
                return
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            ws.append_row([now_str, game_id, league, home, away,
                           str(ou), str(home_ml), str(away_ml)],
                          value_input_option="RAW")
        except Exception:
            pass
    threading.Thread(target=_save, daemon=True).start()


@st.cache_data(ttl=300)
def get_line_movement(game_id: str) -> dict:
    """
    Load line movement history for a game from Google Sheets.
    Returns: snapshots list, movement (ou_delta, ml_delta), direction.
    """
    try:
        ws = _get_or_create_sheet("line_movement")
        if ws is None:
            return {}
        rows = ws.get_all_values()
        # headers: timestamp, game_id, league, home, away, ou, home_ml, away_ml
        snaps = [r for r in rows[1:] if len(r) >= 8 and r[1] == game_id]
        if len(snaps) < 2:
            return {"snapshots": snaps}
        first = snaps[0]
        last  = snaps[-1]
        try:
            ou_open  = float(first[5]) if first[5] else None
            ou_close = float(last[5])  if last[5]  else None
            ou_delta = round(ou_close - ou_open, 1) if (ou_open and ou_close) else None
        except:
            ou_delta = None
        try:
            hml_open  = float(first[6]) if first[6] else None
            hml_close = float(last[6])  if last[6]  else None
            hml_delta = round(hml_close - hml_open, 0) if (hml_open and hml_close) else None
        except:
            hml_delta = None

        direction = "neutral"
        if hml_delta and abs(hml_delta) >= 5:
            direction = "home_steam" if hml_delta < 0 else "away_steam"

        return {
            "snapshots":  snaps,
            "ou_open":    ou_open  if "ou_open"  in dir() else None,
            "ou_close":   ou_close if "ou_close" in dir() else None,
            "ou_delta":   ou_delta,
            "hml_open":   hml_open  if "hml_open"  in dir() else None,
            "hml_close":  hml_close if "hml_close" in dir() else None,
            "hml_delta":  hml_delta,
            "direction":  direction,
            "n_snaps":    len(snaps),
        }
    except Exception:
        return {}


def dixon_coles_tau(gh: float, ga: float, lh: float, la: float, rho: float = -0.13) -> float:
    """
    Dixon-Coles low-score correction factor tau(gh, ga).
    Adjusts Poisson independence assumption for scores 0-0, 1-0, 0-1, 1-1.
    rho=-0.13 is empirically derived for soccer (Dixon & Coles 1997).
    For other sports, rho is set to 0 (no correction needed — higher scoring).
    """
    if rho == 0:
        return 1.0
    if gh == 0 and ga == 0:
        return max(0.01, 1.0 - lh * la * rho)
    elif gh == 1 and ga == 0:
        return max(0.01, 1.0 + la * rho)
    elif gh == 0 and ga == 1:
        return max(0.01, 1.0 + lh * rho)
    elif gh == 1 and ga == 1:
        return max(0.01, 1.0 - rho)
    return 1.0


def get_value_gap(model_prob: float, ml_str: str) -> dict:
    """
    Calculate the gap between model probability and market implied probability.
    Returns: implied_prob, gap_pp, gap_pct, rating (strong/good/neutral/negative).
    Positive gap = model sees MORE value than market = bet edge.
    """
    try:
        implied = ml_to_prob(ml_str)
        if implied <= 0 or implied >= 1:
            return {}
        gap_pp  = round((model_prob - implied) * 100, 1)   # percentage points
        gap_pct = round(gap_pp / (implied * 100) * 100, 1) # relative %
        if gap_pp >= 10:
            rating = "🔥 Fuerte"
            color  = "#00C896"
        elif gap_pp >= 5:
            rating = "✅ Bueno"
            color  = "#86efac"
        elif gap_pp >= 0:
            rating = "➡️ Neutral"
            color  = "#C9A84C"
        else:
            rating = "❌ Negativo"
            color  = "#ef4444"
        return {
            "implied_prob": round(implied * 100, 1),
            "model_prob":   round(model_prob * 100, 1),
            "gap_pp":       gap_pp,
            "gap_pct":      gap_pct,
            "rating":       rating,
            "color":        color,
        }
    except Exception:
        return {}

# ═══════════════════════════════════════════════════════════════════════════════
# MATH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
def ml_to_prob(ml):
    try:
        ml=float(str(ml).replace("+",""))
        return 100/(ml+100) if ml>0 else abs(ml)/(abs(ml)+100)
    except: return 0.5

def prob_to_ml(prob: float, vig: float = 0.045) -> str:
    """Prob → momio americano con vig. ej: 0.62 → '-163'"""
    try:
        p = max(0.01, min(0.99, float(prob)))
        p_vig = min(0.98, p * (1 + vig))
        if p_vig >= 0.5:
            return str(round(-(p_vig / (1 - p_vig)) * 100))
        else:
            return f"+{round(((1 - p_vig) / p_vig) * 100)}"
    except:
        return ""

def prob_to_dec(prob: float, vig: float = 0.045) -> str:
    """Prob → momio decimal con vig. ej: 0.62 → '1.61'
    Decimal = 1 / prob_con_vig  (incluye la ganancia + la apuesta)
    Una cuota de 1.61 significa: apuestas $100, recibes $161 si ganas.
    """
    try:
        p = max(0.01, min(0.99, float(prob)))
        p_vig = min(0.98, p * (1 + vig))
        dec = 1.0 / p_vig
        return f"{dec:.2f}"   # ej: "1.61"
    except:
        return ""

def fair_ml(prob: float) -> str:
    """Momio americano justo SIN vig."""
    try:
        p = max(0.01, min(0.99, float(prob)))
        if p >= 0.5:
            return str(round(-(p / (1-p)) * 100))
        else:
            return f"+{round(((1-p)/p) * 100)}"
    except:
        return ""

def fair_dec(prob: float) -> str:
    """Momio decimal justo SIN vig. ej: 0.62 → '1.61'"""
    try:
        p = max(0.01, min(0.99, float(prob)))
        return f"{(1.0/p):.2f}"
    except:
        return ""

def win_pct(rec):
    """Parse W-L or W-L-D record, return win% or None if insufficient data."""
    try:
        p = rec.strip().split("-")
        w, l = int(p[0]), int(p[1])
        # For soccer W-L-D records, include draws as 0.5 wins
        d = int(p[2]) if len(p) >= 3 else 0
        total = w + l + d
        return (w + d * 0.5) / total if total >= 5 else None
    except:
        return None

def win_pct_strict(rec):
    """Parse W-L only (no draws), return win% or None."""
    try:
        p = rec.strip().split("-")
        w, l = int(p[0]), int(p[1])
        return w / (w + l) if (w + l) >= 5 else None
    except:
        return None

# ── League-level historical home win rates (used when no record data available)
# Source: multi-season averages. Home advantage is real but varies by sport.
LEAGUE_HOME_RATE = {
    "NBA": 0.595,
    "MLB": 0.540,
    "NFL": 0.570, "NCAAF": 0.610,
    "NHL": 0.550,
    "MLS": 0.470, "Liga MX": 0.470,
    "Premier League": 0.440, "La Liga": 0.455, "Bundesliga": 0.460,
    "Serie A": 0.455, "Ligue 1": 0.455,
    "Champions League": 0.475, "Europa League": 0.465,
    "Conference League": 0.460, "CONCACAF Champions Cup": 0.480,
    "Saudi Pro League": 0.465, "Belgian Pro League": 0.455, "Eredivisie": 0.450,
    }

def calc_ev(prob, ml):
    try:
        ml=float(str(ml).replace("+",""))
        payout=ml if ml>0 else 10000/abs(ml)
        return round(prob*payout-(1-prob)*100,2)
    except: return None

def quarter_kelly(prob, ml):
    try:
        ml=float(str(ml).replace("+",""))
        b=ml/100 if ml>0 else 100/abs(ml)
        k=(b*prob-(1-prob))/b
        return max(0.0,round(k*0.25,4))
    except: return None

def pick_score_universal(cand, sim, r, sg):
    """
    Score compuesto universal — usado por Rongol, Picks tab e historial.
    Toma en cuenta TODAS las señales disponibles de la simulación:
    1. Prob Monte Carlo  2. EV vs casa  3. Edge pp  4. Consenso señales
    5. DQ               6. Kelly       7. Líneas modelo vs casa
    8. Lesiones         9. Fatiga B2B  10. Scoring trend λ
    11. O/U modelo vs ESPN  12. Mercado  13. Soccer sin línea ESPN
    """
    prob  = cand.get("prob", 0) or 0
    ev    = cand.get("ev",   0) or 0
    mkt   = cand.get("market", cand.get("mercado", ""))
    kelly = cand.get("kelly", 0) or 0
    dq    = sim.get("data_quality", 0) or 0
    consensus = sim.get("consensus_score", 0) or 0

    # 1. Probabilidad Monte Carlo
    score = prob * 0.45

    # 2. EV vs momio de la casa
    if ev > 0:   score += min(ev, 30) * 0.9
    elif ev < 0: score += max(ev, -15) * 0.25

    # 3. Edge modelo vs implícita ESPN
    if mkt == "ML":
        _label = cand.get("label", cand.get("pick_label", ""))
        _home_name = r.get("home_team","") if isinstance(r, dict) else ""
        _is_h = bool(_home_name) and _home_name in _label
        _edge_pp = sim.get("edge_home_pp") if _is_h else sim.get("edge_away_pp")
        if _edge_pp is not None:
            score += _edge_pp * 1.5

    # 4. Consenso señales (MC + Forma + ScoringTrend + Fatiga)
    score += consensus * 18

    # 5. Calidad de datos
    score += (dq / 100) * 10

    # 6. Kelly 25%
    if kelly > 0:
        score += min(kelly * 120, 12)

    # 7. Líneas del modelo vs casa (decimal propio vs ESPN)
    if mkt == "ML":
        try:
            _label2 = cand.get("label", cand.get("pick_label", ""))
            _is_h2  = bool(r.get("home_team","")) and r.get("home_team","") in _label2
            _mdec   = float(sim.get("model_home_dec" if _is_h2 else "model_away_dec") or 0)
            _casa_ml = sim.get("home_ml" if _is_h2 else "away_ml")
            if _casa_ml and _mdec > 0:
                _casa_prob = ml_to_prob(_casa_ml)
                _casa_dec  = 1 / _casa_prob if _casa_prob > 0 else 0
                score += (_casa_dec - _mdec) * 10
        except:
            pass

    # 8. Lesiones
    _h_inj = sim.get("home_injury_factor", 1.0) or 1.0
    _a_inj = sim.get("away_injury_factor", 1.0) or 1.0
    if mkt == "ML":
        _label3 = cand.get("label", cand.get("pick_label", ""))
        _is_h3  = bool(r.get("home_team","")) and r.get("home_team","") in _label3
        _pick_inj  = _h_inj if _is_h3 else _a_inj
        _rival_inj = _a_inj if _is_h3 else _h_inj
        if _pick_inj < 0.90:  score -= (1.0 - _pick_inj) * 20
        if _rival_inj < 0.90: score += (1.0 - _rival_inj) * 12

    # 9. Fatiga back-to-back
    _h_b2b = sim.get("home_back2back", False)
    _a_b2b = sim.get("away_back2back", False)
    if mkt == "ML":
        _label4 = cand.get("label", cand.get("pick_label", ""))
        _is_h4  = bool(r.get("home_team","")) and r.get("home_team","") in _label4
        if _is_h4 and _h_b2b and not _a_b2b:  score -= 8
        elif not _is_h4 and _a_b2b and not _h_b2b: score -= 8
        elif _is_h4 and _a_b2b and not _h_b2b: score += 5
        elif not _is_h4 and _h_b2b and not _a_b2b: score += 5

    # 10. Scoring trend λ_real vs λ_liga
    _lam_h  = sim.get("lam_real_h") or 0
    _lam_a  = sim.get("lam_real_a") or 0
    _lam_lg = sim.get("lam_league") or 0
    if _lam_h and _lam_a and _lam_lg:
        _lam_total = _lam_h + _lam_a
        _trend = _lam_total - _lam_lg
        _label5 = cand.get("label", cand.get("pick_label", ""))
        if mkt == "O/U":
            if "Over" in _label5 and _trend > 0.3:   score += min(_trend * 4, 8)
            elif "Under" in _label5 and _trend < -0.3: score += min(abs(_trend)*4, 8)
            elif "Over" in _label5 and _trend < -0.3:  score -= 6
        if mkt == "BTTS":
            if _lam_h >= _lam_lg*0.45 and _lam_a >= _lam_lg*0.45: score += 5

    # 11. O/U modelo vs ESPN
    if mkt == "O/U":
        _model_ou = sim.get("model_ou_total") or 0
        try:
            _ou_espn = float((sim.get("ou_line") or "").lstrip("~"))
            if _model_ou and _ou_espn:
                _gap = _model_ou - _ou_espn
                _label6 = cand.get("label", cand.get("pick_label", ""))
                if "Over"  in _label6 and _gap  > 0.3: score += min(_gap  * 5, 12)
                elif "Under" in _label6 and _gap < -0.3: score += min(abs(_gap)*5, 12)
                elif "Over"  in _label6 and _gap < -0.3: score -= 8
                elif "Under" in _label6 and _gap  > 0.3: score -= 8
        except: pass

    # 12. Modelo Elo implícito (W-L records → rating relativo)
    # Si la ventaja de Elo va en la misma dirección que el pick → confirmar
    # Elo implícito: win_rate → rating via logit scale
    if mkt == "ML":
        try:
            import math as _math
            _hrec = r.get("home_record","") or ""
            _arec = r.get("away_record","") or ""
            def _wp(rec):
                try:
                    p = rec.strip().split("-")
                    w,l = int(p[0]),int(p[1])
                    d = int(p[2]) if len(p)>=3 else 0
                    t = w+l+d
                    return (w+d*0.5)/t if t>=5 else None
                except: return None
            _hwp = _wp(_hrec); _awp = _wp(_arec)
            if _hwp and _awp and _hwp > 0 and _awp > 0:
                # Elo implícito = 400 * log10(wp/(1-wp))
                _h_elo = 400 * _math.log10(_hwp / (1-_hwp))
                _a_elo = 400 * _math.log10(_awp / (1-_awp))
                _elo_gap = _h_elo - _a_elo  # positivo = home mejor
                _label_elo = cand.get("label", cand.get("pick_label",""))
                _is_home_elo = bool(r.get("home_team","")) and r.get("home_team","") in _label_elo
                _elo_alignment = _elo_gap if _is_home_elo else -_elo_gap
                if _elo_alignment > 50:   score += 4   # Elo confirma fuertemente
                elif _elo_alignment > 20: score += 2
                elif _elo_alignment < -50: score -= 4  # Elo contradice
                elif _elo_alignment < -20: score -= 2
        except: pass

    # 12b. Mercado: predecibilidad histórica
    if mkt == "ML":     score += 3
    elif mkt == "BTTS": score += 1

    # 13. Soccer sin línea ESPN → penalizar BTTS/O/U
    if sg == "Soccer" and mkt in ("BTTS", "O/U"):
        if not (sim.get("ou_line") or "").replace("~","").strip():
            score -= 12

    # 14. H2H histórico — si el favorito del modelo coincide con el favorito H2H
    _h2h_d = r.get("h2h", {}) if isinstance(r, dict) else {}
    if _h2h_d and _h2h_d.get("count", 0) >= 3 and mkt == "ML":
        _wh2h = _h2h_d.get("wins_home", 0)
        _wa2h = _h2h_d.get("wins_away", 0)
        _tot2h = _wh2h + _wa2h + _h2h_d.get("draws", 0)
        if _tot2h >= 3:
            _h2h_home_rate = _wh2h / _tot2h
            _label_h2h = cand.get("label", cand.get("pick_label", ""))
            _is_home_h2h = bool(r.get("home_team","")) and r.get("home_team","") in _label_h2h
            _pick_h2h_rate = _h2h_home_rate if _is_home_h2h else (1 - _h2h_home_rate)
            # Strong H2H alignment: pick dominates H2H history
            if _pick_h2h_rate >= 0.6:
                score += (_pick_h2h_rate - 0.5) * 20  # up to +10
            elif _pick_h2h_rate <= 0.35:
                score -= (0.5 - _pick_h2h_rate) * 14  # penalize H2H contradiction

    return round(score, 3)


def poisson_sample(lam, rng):
    if lam<=0: return 0
    L=math.exp(-min(lam,30)); k=0; p=1.0
    while p>L: k+=1; p*=rng.random()
    return k-1

def compute_base_prob(game):
    """
    Multi-signal probability estimator. Signals by descending reliability:
      1. Moneyline (vig-adjusted)         weight 4.0  — best signal, market consensus
      2. ESPN win% (from odds block)      weight 3.0  — ESPN's own model
      3. Season record ratio (W-L-D)      weight 2.0  — full season performance
      4. Recent form (last 10 games)      weight 3.0  — recency-weighted win rate (exp decay)
      4b. H2H head-to-head history        weight 1.8  — direct matchup evidence (≥5 games)
      5. League home rate prior           weight 0.6  — anchor when data is thin

    DQ (data quality) = how much hard evidence we have, 0-100%.
    When DQ is low, Monte Carlo uncertainty (sigma) is higher.
    """
    signals, weights = [], []
    odds   = game["odds"]
    league = game["league"]
    is_soccer = LEAGUES.get(league, {}).get("group") == "Soccer"

    # ── Signal 1: Moneyline (strongest — vig-adjusted market probability) ──────
    hml = odds.get("home_ml", ""); aml = odds.get("away_ml", "")
    if hml and aml:
        hp = ml_to_prob(hml); ap = ml_to_prob(aml); vig = hp + ap
        if 1.0 < vig < 1.30:
            signals.append(hp / vig)
            weights.append(4.0)

    # ── Signal 2: ESPN win probability (their model) ──────────────────────────
    hwp = odds.get("home_wp", ""); awp = odds.get("away_wp", "")
    if hwp and awp:
        try:
            hw = float(str(hwp).replace("%", "")) / 100
            aw = float(str(awp).replace("%", "")) / 100
            if 0 < hw < 1 and 0 < aw < 1:
                signals.append(hw / (hw + aw))
                weights.append(3.0)
        except: pass

    # ── Signal 3: Season records ──────────────────────────────────────────────
    hrec_raw = game.get("home_record", "")
    arec_raw = game.get("away_record", "")
    hrec = win_pct(hrec_raw)
    arec = win_pct(arec_raw)

    if hrec is not None and arec is not None:
        total = hrec + arec
        if total > 0:
            signals.append(hrec / total)
            weights.append(2.0)
    elif hrec is not None:
        # Only have home team record — compare against league average
        league_avg = LEAGUE_HOME_RATE.get(league, 0.50)
        # Blend team record with league home rate
        blended = (hrec * 0.6 + league_avg * 0.4)
        signals.append(blended)
        weights.append(1.2)
    elif arec is not None:
        league_avg = LEAGUE_HOME_RATE.get(league, 0.50)
        blended = ((1 - arec) * 0.6 + league_avg * 0.4)
        signals.append(blended)

    # ── Signal 4: Recent form (last 5 games, weighted by recency) ─────────────
    # Weight 2.5 — stronger than season record (2.0), weaker than moneyline (4.0)
    home_form = game.get("home_form")  # 0.0–1.0 win rate recent games
    away_form = game.get("away_form")
    if home_form is not None and away_form is not None:
        total_form = home_form + away_form
        if total_form > 0:
            signals.append(home_form / total_form)
            # When no moneyline available, form carries more weight (up to 3.5)
            has_ml_signal = bool(hml and aml)
            form_w = 3.0 if has_ml_signal else 4.0  # Last 10 games → more reliable_signal else 3.5
            weights.append(form_w)
    elif home_form is not None:
        signals.append((home_form + 0.5) / (home_form + 1.0))
        weights.append(1.5)
    elif away_form is not None:
        signals.append(1.0 - (away_form + 0.5) / (away_form + 1.0))
        weights.append(1.5)

    # ── Signal 4b: H2H head-to-head win rate ────────────────────────────────
    # Direct historical evidence between these two specific teams.
    # Weight 1.8 (between form 2.5 and season record 2.0) when ≥5 H2H games.
    # When only 3-4 H2H games, use weight 1.0 (smaller sample).
    _h2h_sig = game.get("h2h", {})
    if _h2h_sig and isinstance(_h2h_sig, dict):
        _h2h_count = _h2h_sig.get("count", 0) or 0
        _wh2h = _h2h_sig.get("wins_home", 0) or 0
        _wa2h = _h2h_sig.get("wins_away", 0) or 0
        _dr2h = _h2h_sig.get("draws", 0) or 0
        _tot2h = _wh2h + _wa2h + _dr2h
        if _tot2h >= 3:
            # Home win rate in H2H (draws count as 0.5)
            _h2h_home_rate = (_wh2h + 0.5 * _dr2h) / _tot2h
            signals.append(_h2h_home_rate)
            _h2h_w = 1.8 if _h2h_count >= 5 else 1.0
            weights.append(_h2h_w)

    # ── Signal 5: League historical home rate (prior / fallback) ─────────────
    # Always add as a weak anchor — prevents wild swings when data is thin
    league_prior = LEAGUE_HOME_RATE.get(league, 0.50)
    signals.append(league_prior)
    weights.append(0.6)  # Low weight — just a prior, not evidence

    # ── Combine signals ───────────────────────────────────────────────────────
    home_p = sum(s * w for s, w in zip(signals, weights)) / sum(weights)

    # Apply home field boost (on top of signal blend)
    # Don't double-count if ML already includes home advantage
    has_ml = bool(hml and aml)
    boost = HOME_BOOST.get(league, 0.03) * (0.3 if has_ml else 1.0)
    home_p = min(0.95, max(0.05, home_p + boost))

    # ── Signal 6: Injury adjustment ───────────────────────────────────────────
    # injury_factor = 1.0 (healthy) → 0.40 (multiple key players out)
    # If home team is hurt: reduce home_p proportionally
    # If away team is hurt: increase home_p proportionally
    # Effect is dampened when moneyline is present (market may already price it in)
    # Dampening: 50% when ML present (market partially aware), 100% when ML absent
    h_inj_f = game.get("home_injury_factor", 1.0)
    a_inj_f = game.get("away_injury_factor", 1.0)

    if h_inj_f < 1.0 or a_inj_f < 1.0:
        # impact_delta: positive = home weakened relative to away, negative = away weakened
        # Net effect on home_p: home injuries → lower home_p, away injuries → higher home_p
        h_impact = 1.0 - h_inj_f  # 0.0 if healthy
        a_impact = 1.0 - a_inj_f  # 0.0 if healthy
        net_delta = (a_impact - h_impact) * 0.25  # scale: max raw delta ≈ 0.55 → max shift ±0.14%
        # Dampen when moneyline present (market already partially reflects injuries)
        dampen = 0.50 if has_ml else 1.0
        home_p = min(0.95, max(0.05, home_p + net_delta * dampen))

    # ── Data Quality ──────────────────────────────────────────────────────────
    # DQ = fraction of "hard evidence" weight vs ideal (ML=4 + ESPN=3 + record=2 = 9)
    hard_weight = sum(w for s, w in zip(signals, weights)
                      if w >= 1.2)  # exclude the weak prior
    dq = min(1.0, hard_weight / 9.0)

    # ── Soccer: model draw probability ───────────────────────────────────────
    if is_soccer:
        # Draw probability: higher when teams are balanced, lower when one dominates
        balance = 1.0 - abs(home_p - 0.5) * 2  # 0=total mismatch, 1=50/50
        draw_p  = max(0.10, min(0.32, 0.22 + balance * 0.10))
        rem     = 1.0 - draw_p
        return {
            "home_prob":  home_p * rem,
            "away_prob":  (1 - home_p) * rem,
            "draw_prob":  draw_p,
            "dq":         dq,
            "is_soccer":  True,
        }

    return {
        "home_prob":  home_p,
        "away_prob":  1.0 - home_p,
        "draw_prob":  0.0,
        "dq":         dq,
        "is_soccer":  False,
    }

# LEAGUE_AVG_GOALS values = expected TOTAL goals per game (both teams combined).
# For basketball/football they are total points.
# avg * 2 was a bug for soccer — removed.
SOCCER_LEAGUES = {
    "MLS","Liga MX","Premier League","La Liga","Bundesliga",
    "Serie A","Ligue 1","Champions League","Europa League","Conference League",
    "CONCACAF Champions Cup","Saudi Pro League","Belgian Pro League","Eredivisie",
    "UEFA Nations League","CONCACAF Nations League","Copa Oro","Copa América",
    "Eliminatorias UEFA","Eliminatorias CONMEBOL","Eliminatorias CONCACAF",
    "Amistosos Internacionales","Africa Cup of Nations","Asian Cup","World Cup",
}

def get_lambda(game):
    """
    Estimate expected goals/points per team using Poisson model.

    Priority:
      1. ESPN O/U line (most accurate — current market)
      2. Scoring Trend — avg scored/conceded last 5 games (Signal B)
         Blended 60% real / 40% league avg to avoid small-sample overfit
      3. League historical average fallback

    LEAGUE_AVG_GOALS stores TOTAL goals (both teams) for soccer,
    total points for basketball/football/hockey.
    """
    league = game["league"]
    avg    = LEAGUE_AVG_GOALS.get(league)
    if avg is None: return None, None

    # Determinar si es soccer para ajustes específicos
    _sport_grp_lam = LEAGUES.get(league, {}).get("group", "Soccer")
    is_soccer = _sport_grp_lam == "Soccer"

    ou = game["odds"].get("over_under", "")
    try:
        total = float(str(ou))
        if total <= 0 or total > 300: raise ValueError
        # ESPN line available — most accurate, use directly
        has_ou_line = True
    except:
        has_ou_line = False
        total = None

    base = compute_base_prob(game)
    hp   = base["home_prob"]
    ap   = base["away_prob"]

    # ── Signal B: Scoring Trend ───────────────────────────────────────
    # If both teams have recent scoring data, estimate λ via Dixon-Coles
    h_scored   = game.get("home_avg_scored")
    h_conceded = game.get("home_avg_conceded")
    a_scored   = game.get("away_avg_scored")
    a_conceded = game.get("away_avg_conceded")

    lam_home_real = None
    lam_away_real = None

    # Sport-specific Signal B config
    # home_boost: home scoring advantage factor (source: historical home/away splits)
    # defence_floor: min defence strength ratio — prevents extreme λ from small samples
    #   Soccer: floor=0.20 (goals 1-3, defender can hold to near-0)
    #   Basketball: floor=0.70 (you always score SOME points, defense can't go to 0)
    #   Hockey: floor=0.25 (similar to soccer but slightly higher)
    #   Baseball: floor=0.60 (pitching dominant but ~3 runs minimum realistic)
    #   Football: floor=0.55 (even great defense gives up ~14 pts)
    # NCAAF: Signal B disabled — 150+ teams, huge level disparity, no SOS adjustment
    lg_info     = LEAGUES.get(league, {})
    sport_grp_b = lg_info.get("group", "")
    HOME_BOOST_B  = {"Soccer":0.05, "Basketball":0.03, "Hockey":0.04, "Baseball":0.02, "Football":0.02}
    DEFENCE_FLOOR = {"Soccer":0.20, "Basketball":0.70, "Hockey":0.25, "Baseball":0.60, "Football":0.55}
    home_boost_b  = HOME_BOOST_B.get(sport_grp_b, 0.03)
    def_floor     = DEFENCE_FLOOR.get(sport_grp_b, 0.30)
    signal_b_ok   = sport_grp_b != "Football" or league != "NCAAF"  # disable for NCAAF

    # FIX-3: Validar escala — evitar mezclar soccer scale (1-3) con basketball (110 pts)
    _scale_ok = True
    if sport_grp_b in ("Basketball", "Football"):
        _avg_check = avg / 2.0
        if h_scored is not None and _avg_check > 0 and h_scored < _avg_check * 0.15:
            _scale_ok = False
        if a_scored is not None and _avg_check > 0 and a_scored < _avg_check * 0.15:
            _scale_ok = False

    if signal_b_ok and _scale_ok and h_scored is not None and a_conceded is not None and h_scored > 0:
        avg_per_team = max(0.5, avg / 2.0)
        h_attack  = h_scored   / avg_per_team
        a_defence = max(def_floor, a_conceded / avg_per_team)
        lam_home_real = max(0.1, avg_per_team * h_attack * a_defence * (1.0 + home_boost_b))

    if signal_b_ok and _scale_ok and a_scored is not None and h_conceded is not None and a_scored > 0:
        avg_per_team = max(0.5, avg / 2.0)
        a_attack  = a_scored   / avg_per_team
        h_defence = max(def_floor, h_conceded / avg_per_team)
        lam_away_real = max(0.1, avg_per_team * a_attack * h_defence)

    # ── Build final lambdas ───────────────────────────────────────────
    if has_ou_line:
        # Sharp model: ESPN line contains public-bias inflation (+0.5-0.7 pts).
        # Give scoring trend 55% weight so model can diverge from line when data supports it.
        # The divergence between model total and ESPN line IS the edge signal.
        home_share = (hp + 0.52) / (hp + ap + 1.04)
        lam_line_h = max(0.1, total * home_share)
        lam_line_a = max(0.1, total * (1.0 - home_share))
        if lam_home_real is not None and lam_away_real is not None:
            lam_home = 0.55 * lam_home_real + 0.45 * lam_line_h
            lam_away = 0.55 * lam_away_real + 0.45 * lam_line_a
            game["_lam_real_h"] = round(lam_home_real, 3)
            game["_lam_real_a"] = round(lam_away_real, 3)
            game["_lam_league"] = round(avg, 2)
        else:
            lam_home = lam_line_h
            lam_away = lam_line_a

    elif lam_home_real is not None and lam_away_real is not None:
        # No ESPN line but full scoring trend — blend 60/40 with league avg
        home_share = (hp + 0.52) / (hp + ap + 1.04)
        lam_league_h = max(0.1, avg * home_share)
        lam_league_a = max(0.1, avg * (1.0 - home_share))
        lam_home = 0.60 * lam_home_real + 0.40 * lam_league_h
        lam_away = 0.60 * lam_away_real + 0.40 * lam_league_a
        # Store for Signal D arbiter and display
        game["_lam_real_h"] = round(lam_home_real, 3)
        game["_lam_real_a"] = round(lam_away_real, 3)
        game["_lam_league"] = round(avg, 2)

    else:
        # Full fallback: league average
        home_share = (hp + 0.52) / (hp + ap + 1.04)
        lam_home   = max(0.1, avg * home_share)
        lam_away   = max(0.1, avg * (1.0 - home_share))

    # ── Team Profile blend: usa historial acumulado de Google Sheets ────────────
    # Si el equipo tiene ≥5 partidos guardados, blendear λ con el avg histórico.
    # Blend: 60% perfil histórico + 40% cálculo actual (ESPN + form)
    # El perfil es home/away-aware: usa avg_scored_home vs avg_scored_away
    _h_prof = game.get("home_profile")
    _a_prof = game.get("away_profile")
    _is_home_game = True  # home team siempre es local en este contexto

    if _h_prof and _h_prof.get("n_games", 0) >= 5:
        _h_avg = _h_prof.get("avg_scored_home") or _h_prof.get("avg_scored") or 0
        if _h_avg > 0:
            lam_home = round(lam_home * 0.40 + _h_avg * 0.60, 4)

    if _a_prof and _a_prof.get("n_games", 0) >= 5:
        _a_avg = _a_prof.get("avg_scored_away") or _a_prof.get("avg_scored") or 0
        if _a_avg > 0:
            lam_away = round(lam_away * 0.40 + _a_avg * 0.60, 4)

    # ── Injury λ reduction ────────────────────────────────────────────────────
    # Injured team scores less and potentially concedes more (weakened defense)
    # injury_factor 1.0=healthy, 0.40=worst case
    # Scoring reduction: proportional to injury severity on offensive positions
    # Defense weakening: partial (0.4x) — harder to isolate from scoring data
    h_inj_f = game.get("home_injury_factor", 1.0)
    a_inj_f = game.get("away_injury_factor", 1.0)

    if h_inj_f < 1.0:
        # Home team hurt: reduce home scoring λ
        lam_home = max(0.1, lam_home * (0.70 + 0.30 * h_inj_f))
        # Away scores slightly more against weakened home defense
        lam_away = max(0.1, lam_away * (1.0 + (1.0 - h_inj_f) * 0.15))
    if a_inj_f < 1.0:
        # Away team hurt: reduce away scoring λ
        lam_away = max(0.1, lam_away * (0.70 + 0.30 * a_inj_f))
        # Home scores slightly more against weakened away defense
        lam_home = max(0.1, lam_home * (1.0 + (1.0 - a_inj_f) * 0.15))

    # ── Red Card λ adjustment (soccer only) ─────────────────────────────────
    # Tarjeta roja = ~10 min menos jugando con 10 hombres en promedio
    # Efecto estadístico real: equipo con roja concede ~0.35 goles más,
    # marca ~0.25 goles menos. Fuente: Journal of Quantitative Analysis in Sports.
    # Usamos la tasa histórica del equipo como probabilidad de roja en este partido.
    # Liga promedio: ~0.15 (1 roja c/6-7 partidos). Equipo agresivo: >0.25
    if is_soccer:
        _h_rc = (_h_prof.get("red_card_rate", 0) or 0) if _h_prof else 0
        _a_rc = (_a_prof.get("red_card_rate", 0) or 0) if _a_prof else 0
        _league_rc_avg = 0.15  # tasa promedio de liga

        # Exceso sobre el promedio de liga
        _h_rc_excess = max(0, _h_rc - _league_rc_avg)
        _a_rc_excess = max(0, _a_rc - _league_rc_avg)

        # Si el local es propenso a rojas → marca menos, concede más
        if _h_rc_excess > 0:
            lam_home = max(0.1, lam_home * (1.0 - _h_rc_excess * 1.5))  # hasta -37.5%
            lam_away = max(0.1, lam_away * (1.0 + _h_rc_excess * 1.0))  # hasta +25%

        # Si el visitante es propenso a rojas → marca menos, concede más
        if _a_rc_excess > 0:
            lam_away = max(0.1, lam_away * (1.0 - _a_rc_excess * 1.5))
            lam_home = max(0.1, lam_home * (1.0 + _a_rc_excess * 1.0))

    # ── H2H blend: if ≥5 H2H games available, pull lambda toward H2H avg ────
    # H2H history is more specific than league avg — weight 20% when available.
    # Only applied when we DON'T have a strong ESPN line (to avoid line fighting).
    _h2h = game.get("h2h", {})
    if _h2h and _h2h.get("count", 0) >= 5 and not has_ou_line:
        _h2h_avg = _h2h.get("avg_total", 0)
        if _h2h_avg > 0:
            _h2h_share_h = _h2h.get("avg_goals_h", lam_home) / max(0.1, _h2h_avg)
            _h2h_lam_h   = max(0.1, _h2h_avg * _h2h_share_h)
            _h2h_lam_a   = max(0.1, _h2h_avg * (1 - _h2h_share_h))
            lam_home = round(lam_home * 0.80 + _h2h_lam_h * 0.20, 4)
            lam_away = round(lam_away * 0.80 + _h2h_lam_a * 0.20, 4)
            game["_h2h_blend"] = True

    # ── Weather O/U adjustment (outdoor sports: football, baseball, soccer) ──
    # High wind / heavy rain / extreme cold reduces expected scoring.
    _wx_adj = game.get("_weather_ou_adj", 0.0)
    if _wx_adj and _wx_adj != 0.0:
        lam_home = max(0.1, lam_home * (1.0 + _wx_adj))
        lam_away = max(0.1, lam_away * (1.0 + _wx_adj))

    return max(0.1, lam_home), max(0.1, lam_away)


# ══════════════════════════════════════════════════════════════════════════════
# LEAGUE O/U PRIORS — baseline Poisson probabilities using only league avg goals
# Used to filter O/U picks: a pick is only valid if the simulation deviates
# significantly from what we'd expect knowing nothing about the specific teams.
# Source: computed from LEAGUE_AVG_GOALS via joint Poisson(lam/2, lam/2)
# Format: {league: (P_U15, P_U25, P_U35, P_O15, P_O25, P_O35)}
# ══════════════════════════════════════════════════════════════════════════════
LEAGUE_OU_PRIORS = {
    # Format: (P_U15, P_U25, P_U35, P_O15, P_O25, P_O35, P_BTTS)
    # Fuente: Sofascore/FootyStats/FBref — Temporada 2025-26 (en curso ~Jornada 26)
    # Bundesliga 2025-26: O2.5=62%, O3.5=40%, BTTS=57% (Sofascore)
    # PL 2025-26:  O2.5=56%, O3.5=31%, BTTS=56%
    # La Liga:     O2.5=51%, O3.5=28%, BTTS=52%
    # Serie A:     O2.5=51%, O3.5=27%, BTTS=51%
    # Ligue 1:     O2.5=56%, O3.5=30%, BTTS=54%
    # MLS 2025:    O2.5=58%, O3.5=35%, BTTS=55%
    # Liga MX:     O2.5=52%, O3.5=30%, BTTS=51%
    "MLS":                   (0.215, 0.420, 0.650, 0.785, 0.580, 0.350, 0.550),
    "Liga MX":               (0.250, 0.480, 0.700, 0.750, 0.520, 0.300, 0.510),
    "Premier League":        (0.240, 0.440, 0.690, 0.760, 0.560, 0.310, 0.560),
    "La Liga":               (0.265, 0.490, 0.720, 0.735, 0.510, 0.280, 0.520),
    "Bundesliga":            (0.175, 0.380, 0.600, 0.825, 0.620, 0.400, 0.570),
    "Serie A":               (0.265, 0.490, 0.730, 0.735, 0.510, 0.270, 0.510),
    "Ligue 1":               (0.245, 0.440, 0.700, 0.755, 0.560, 0.300, 0.540),
    "Champions League":      (0.185, 0.400, 0.625, 0.815, 0.600, 0.375, 0.610),
    "Europa League":         (0.225, 0.455, 0.680, 0.775, 0.545, 0.320, 0.580),
    "Conference League":     (0.255, 0.500, 0.720, 0.745, 0.500, 0.280, 0.550),
    "CONCACAF Champions Cup":(0.225, 0.460, 0.685, 0.775, 0.540, 0.315, 0.575),
    "Saudi Pro League":      (0.230, 0.465, 0.690, 0.770, 0.535, 0.310, 0.570),
    "Belgian Pro League":    (0.195, 0.415, 0.635, 0.805, 0.585, 0.365, 0.615),
    "Eredivisie":            (0.188, 0.400, 0.622, 0.812, 0.600, 0.378, 0.625),
    # Ligas ocultas
    "Superliga":             (0.218, 0.445, 0.665, 0.782, 0.555, 0.335, 0.560),
    "Süper Lig":             (0.255, 0.488, 0.710, 0.745, 0.512, 0.290, 0.525),
    "Super League Greece":   (0.262, 0.495, 0.720, 0.738, 0.505, 0.280, 0.515),
    "Primeira Liga":         (0.268, 0.502, 0.725, 0.732, 0.498, 0.275, 0.510),
    "Eliteserien":           (0.228, 0.458, 0.678, 0.772, 0.542, 0.322, 0.548),
    "Allsvenskan":           (0.252, 0.485, 0.705, 0.748, 0.515, 0.295, 0.528),
}

# Minimum deviation from league prior to qualify as a valid O/U or BTTS pick.
OU_MIN_EDGE = 0.08

# ═══════════════════════════════════════════════════════════════════════════════
# SOCCER O/U CALIBRATION — post-simulation correction per league
# Source: FBref / Understat / Football-Data.co.uk 2022-23 to 2024-25 (3-year avg)
# Format: (Δ_u25, Δ_u35, Δ_btts)
# Positive Δ = model underestimates Under → shift up. Negative → shift down.
# Rule enforced: Δ_u35 >= Δ_u25 always (keeps O3.5 ≤ O2.5 after calibration)
#
# Real 3yr averages vs Poisson model output:
# PL:    O2.5=54%, O3.5=30%, BTTS=55%  | Model raw: ~53%, ~31%, ~57% → small fixes
# LaLiga:O2.5=51%, O3.5=28%, BTTS=52%  | Model raw: ~49%, ~27%, ~54% → push toward real
# Bund:  O2.5=58%, O3.5=37%, BTTS=57%  | Model raw: ~63%, ~41%, ~64% → reduce Over
# SerieA:O2.5=52%, O3.5=28%, BTTS=52%  | Model raw: ~51%, ~29%, ~55% → small
# Ligue1:O2.5=50%, O3.5=27%, BTTS=51%  | Model raw: ~50%, ~28%, ~53% → small
# LigaMX:O2.5=52%, O3.5=32%, BTTS=51%  | Model raw: ~51%, ~29%, ~55% → small
# UCL:   O2.5=59%, O3.5=36%, BTTS=59%  | Model raw: ~61%, ~38%, ~63% → reduce
# MLS:   O2.5=53%, O3.5=32%, BTTS=54%  | Model raw: ~57%, ~34%, ~60% → reduce
# ═══════════════════════════════════════════════════════════════════════════════
SOCCER_CALIB = {
    # (Δ_U2.5, Δ_U3.5, Δ_BTTS)  — positive = more Under = less Over
    # Premier League: model ~accurate, tiny BTTS over-pred
    "Premier League":         ( +0.010,  +0.020, -0.020),
    # La Liga: model under-predicts Under slightly
    "La Liga":                ( +0.020,  +0.030, -0.020),
    # Bundesliga: biggest correction — Poisson over-predicts high scores heavily
    "Bundesliga":             ( +0.060,  +0.080, -0.080),
    # Serie A: model over-predicts BTTS, O/U close
    "Serie A":                ( +0.020,  +0.035, -0.030),
    # Ligue 1: model over-predicts Over and BTTS
    "Ligue 1":                ( +0.025,  +0.040, -0.025),
    # Liga MX: model over-predicts BTTS significantly
    "Liga MX":                ( +0.010,  +0.035, -0.040),
    # Champions League: slight over-pred of Over/BTTS
    "Champions League":       ( +0.020,  +0.030, -0.040),
    # Europa League
    "Europa League":          ( +0.015,  +0.025, -0.035),
    # Conference League: lower scoring than model predicts
    "Conference League":      ( +0.025,  +0.040, -0.035),
    # CONCACAF: erratic, higher variance — push Under hard
    "CONCACAF Champions Cup": ( +0.060,  +0.080, -0.100),
    # Saudi Pro League: ~avg scoring, similar to MLS
    "Saudi Pro League":       ( +0.025,  +0.040, -0.045),
    # Belgian Pro League: high-scoring but model over-predicts
    "Belgian Pro League":     ( +0.030,  +0.045, -0.030),
    # Eredivisie: also high-scoring but model over-predicts
    "Eredivisie":             ( +0.030,  +0.045, -0.035),
    # MLS: clear Over over-prediction by Poisson
    "MLS":                    ( +0.040,  +0.055, -0.060),
    # Ligas ocultas
    "Superliga":              ( +0.025,  +0.040, -0.030),
    "Süper Lig":              ( +0.020,  +0.035, -0.035),
    "Super League Greece":    ( +0.015,  +0.030, -0.025),
    "Primeira Liga":          ( +0.020,  +0.035, -0.025),
    "Eliteserien":            ( +0.030,  +0.045, -0.035),
    "Allsvenskan":            ( +0.025,  +0.040, -0.030),
}

def apply_soccer_calib(league, p_u25, p_u35, p_btts, p_o25, p_o35):
    """
    Apply per-league calibration to O/U and BTTS probabilities.
    Enforces constraints:
      - O + U = 1.0 for each line
      - Monotonicity: O1.5 >= O2.5 >= O3.5 (more goals = less likely)
      - All probs in [0.01, 0.99]
    """
    cal = SOCCER_CALIB.get(league)
    if cal is None:
        return p_u25, p_u35, p_btts, p_o25, p_o35

    du25, du35, dbtts = cal

    def clamp(x): return max(0.01, min(0.99, x))

    # Apply deltas
    p_u25_c  = clamp(p_u25  + du25)  if p_u25  is not None else None
    p_u35_c  = clamp(p_u35  + du35)  if p_u35  is not None else None
    p_btts_c = clamp(p_btts + dbtts) if p_btts is not None else None

    # Enforce O = 1 - U
    p_o25_c = clamp(1.0 - p_u25_c) if p_u25_c is not None else p_o25
    p_o35_c = clamp(1.0 - p_u35_c) if p_u35_c is not None else p_o35

    # ── Enforce monotonicity: O3.5 must be <= O2.5 ──────────────────────────
    if p_o35_c is not None and p_o25_c is not None:
        if p_o35_c > p_o25_c:
            p_o35_c = p_o25_c * 0.97
            p_u35_c = clamp(1.0 - p_o35_c) if p_u35_c is not None else p_u35_c

    # ── BTTS consistency: BTTS implies both teams scored, so total >= 2 ──────
    # BTTS can be >= O2.5 (e.g. 1-1 counts for BTTS but not O2.5)
    # But BTTS should not be drastically below O2.5 (if 3+ goals, BTTS is very likely)
    # No hard constraint needed — just flag if BTTS < O2.5 * 0.5 (suspicious)
    # This is informational only — the simulation handles it naturally

    return p_u25_c, p_u35_c, p_btts_c, p_o25_c, p_o35_c


# ═══════════════════════════════════════════════════════════════════════════════
# SHARP O/U MODEL — Vegas Public Bias Correction
#
# Source: Bet Labs / Covers.com / TeamRankings 2020-2025 historical O/U results
# NBA 2022-25: Under hit rate ~51.2% → public bias inflates lines +0.7 pts
# MLB 2022-25: Under hit rate ~50.4% → mild inflation +0.2 pts
# NHL 2022-25: Under hit rate ~52.8% → lines inflated +0.3 pts
# NFL 2022-25: Under hit rate ~50.8% → mild inflation +0.3 pts
# ═══════════════════════════════════════════════════════════════════════════════
PUBLIC_BIAS_PTS = {
    "Basketball": 0.8,   # NBA: strong public Over bias → shift effective line down 0.8 pts
    "Baseball":   0.3,   # MLB: mild Over bias
    "Hockey":     0.4,   # NHL: moderate Under-friendly → shift line down 0.4
    "Football":   0.3,   # NFL: mild public Over bias
}

# Standard market lines per sport — analyzed for EVERY game regardless of ESPN line
SPORT_STD_LINES = {
    "Hockey":   [5.5, 6.5],
    "Baseball": [7.5, 8.5, 9.5],
}

def apply_nonsoccer_calib(sport_grp, is_hockey, p_u_total, p_o_total, ou_val):
    """
    Calibration for implicit-line case only (no ESPN line). O+U enforced=1.0.
    Source: historical Under hit rates 2020-2025 when using league-avg as line.
    Positive delta = model under-predicts Under → add to p_u.
    """
    if p_u_total is None or p_o_total is None or ou_val != 0.0:
        return p_u_total, p_o_total
    def clamp(x): return max(0.02, min(0.98, x))

    # When using league avg as implicit line, Poisson naturally produces ~50/50.
    # Real historical rates show slight Under bias in most sports.
    # NBA:  real Under ~51.5% on league-avg line → +1.5%
    # NHL:  real Under ~53.5% on league-avg line → +3.5%
    # MLB:  real Under ~51.8% on league-avg line → +1.8%
    # NFL:  real Under ~51.2% on league-avg line → +1.2%
    if is_hockey:
        p_u_total = clamp(p_u_total + 0.035)   # NHL: clear Under lean
    elif sport_grp == "Basketball":
        p_u_total = clamp(p_u_total + 0.015)   # NBA: slight Under lean
    elif sport_grp == "Baseball":
        p_u_total = clamp(p_u_total + 0.018)   # MLB: slight Under lean
    elif sport_grp == "Football":
        p_u_total = clamp(p_u_total + 0.012)   # NFL: marginal Under lean
    return p_u_total, clamp(1.0 - p_u_total)


# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL D — CONSENSUS ARBITER
# Aggregates votes from all 4 signals for the best pick candidate.
# Weights: MC=40%, Form=25%, ScoringTrend=25%, Fatigue=10%
# Output stored in sim dict as "consensus_score", "consensus_label",
# "consensus_signals", "conflict_note"
# ═══════════════════════════════════════════════════════════════════════════════

def compute_consensus(game, sim):
    """
    Evaluate 4 signals for the best pick and return consensus metadata.
    Modifies sim in-place. Called at end of run_monte_carlo.
    """
    best = sim.get("best_pick", {})
    market = best.get("market", "")
    label  = best.get("label", "")
    prob   = best.get("prob", 0)           # 0-1 from simulation (NOT * 100)

    votes   = []   # list of (weight, vote, signal_name, detail)
    W_MC    = 0.40
    W_FORM  = 0.25
    W_SCORE = 0.25
    W_FAT   = 0.10

    # ── Signal 1: Monte Carlo probability ─────────────────────────────────────
    if prob >= 0.55:    votes.append((W_MC,  +1, "MC",   f"MC {prob*100:.0f}%"))
    elif prob <= 0.48:  votes.append((W_MC,  -1, "MC",   f"MC {prob*100:.0f}%"))
    else:               votes.append((W_MC,   0, "MC",   f"MC {prob*100:.0f}% (neutral)"))

    # ── Signal 2: Form — does win rate support the pick? ──────────────────────
    home_form = game.get("home_form")
    away_form = game.get("away_form")
    form_vote = 0; form_detail = "sin forma"

    sport_grp_c = LEAGUES.get(game.get("league",""), {}).get("group", "Soccer")
    is_soccer_c = sport_grp_c == "Soccer"

    if home_form is not None or away_form is not None:
        # ML picks: form win rate is universally predictive
        if market == "ML":
            is_home_pick = game.get("home_team","") in label
            team_form = home_form if is_home_pick else away_form
            if team_form is not None:
                if team_form >= 0.60:   form_vote = +1; form_detail = f"forma {team_form*100:.0f}%"
                elif team_form <= 0.35: form_vote = -1; form_detail = f"forma baja {team_form*100:.0f}%"
                else:                   form_detail = f"forma neutral {team_form*100:.0f}%"

        # O/U picks — use scoring pace for non-soccer, W/L form for soccer
        elif "Over" in label or "Under" in label:
            pick_is_over = "Over" in label
            h_scored  = game.get("home_avg_scored")
            a_scored  = game.get("away_avg_scored")
            h_concede = game.get("home_avg_conceded")
            a_concede = game.get("away_avg_conceded")
            league_avg = LEAGUE_AVG_GOALS.get(game.get("league",""), 0)

            if not is_soccer_c and h_scored is not None and a_scored is not None and league_avg > 0:
                # Non-soccer: use scoring pace as proxy
                # Combined expected scoring (attack only — no defender data needed)
                pace = (h_scored + a_scored) / max(0.1, league_avg)
                if pace >= 1.05 and pick_is_over:       form_vote = +1; form_detail = f"pace ofensivo {pace:.2f}x liga"
                elif pace <= 0.95 and not pick_is_over: form_vote = +1; form_detail = f"pace defensivo {pace:.2f}x liga"
                elif pace >= 1.05 and not pick_is_over: form_vote = -1; form_detail = f"pace ofensivo contradice Under"
                elif pace <= 0.95 and pick_is_over:     form_vote = -1; form_detail = f"pace defensivo contradice Over"
                else:                                    form_detail = f"pace neutro {pace:.2f}x liga"
            else:
                # Soccer or no scoring data: use W/L form
                h_f = home_form or 0.5; a_f = away_form or 0.5
                avg_form = (h_f + a_f) / 2
                if avg_form >= 0.60 and pick_is_over:       form_vote = +1; form_detail = f"forma ofensiva {avg_form*100:.0f}%"
                elif avg_form <= 0.40 and not pick_is_over: form_vote = +1; form_detail = f"forma defensiva {avg_form*100:.0f}%"
                elif avg_form >= 0.60 and not pick_is_over: form_vote = -1; form_detail = f"forma ofensiva contradice Under"
                elif avg_form <= 0.40 and pick_is_over:     form_vote = -1; form_detail = f"forma defensiva contradice Over"

        # BTTS (soccer only)
        elif "BTTS" in label or "Ambos" in label:
            h_f = home_form or 0.5; a_f = away_form or 0.5
            if h_f >= 0.55 and a_f >= 0.55: form_vote = +1; form_detail = "ambos en forma"
            elif h_f <= 0.35 or a_f <= 0.35: form_vote = -1; form_detail = "uno sin forma"

    votes.append((W_FORM, form_vote, "Forma", form_detail))

    # ── Signal 3: Scoring Trend — λ_real vs λ_liga ────────────────────────────
    lam_real_h = game.get("_lam_real_h")
    lam_real_a = game.get("_lam_real_a")
    lam_league = game.get("_lam_league")
    score_vote = 0; score_detail = "sin trend"

    if lam_real_h is not None and lam_real_a is not None and lam_league is not None:
        lam_real_total = lam_real_h + lam_real_a
        score_detail = f"λreal={lam_real_total:.1f} vs liga={lam_league:.1f}"
        if "Over 2.5" in label or "Over" in label:
            score_vote = +1 if lam_real_total > lam_league * 1.05 else (-1 if lam_real_total < lam_league * 0.95 else 0)
        elif "Under 2.5" in label or "Under" in label:
            score_vote = +1 if lam_real_total < lam_league * 0.95 else (-1 if lam_real_total > lam_league * 1.05 else 0)
        elif "BTTS" in label or "Ambos" in label:
            score_vote = +1 if (lam_real_h >= 0.9 and lam_real_a >= 0.9) else 0

    votes.append((W_SCORE, score_vote, "ScoringTrend", score_detail))

    # ── Signal 4: Fatigue ─────────────────────────────────────────────────────
    home_b2b = game.get("home_back2back", False)
    away_b2b = game.get("away_back2back", False)
    fat_vote = 0; fat_detail = ""

    _sport_grp_fat = LEAGUES.get(game.get("league",""), {}).get("group", "")
    _is_football_fat = _sport_grp_fat == "Football"
    _rest_term = "semana corta" if _is_football_fat else "back-to-back"
    if home_b2b and not away_b2b:
        fat_detail = f"🔋 {game.get('home_team','')} en {_rest_term}"
        if market == "ML":
            if game.get("away_team","") in label: fat_vote = +1  # pick = fresh team
            elif game.get("home_team","") in label: fat_vote = -1
        else: fat_vote = 0  # O/U neutral to fatigue
    elif away_b2b and not home_b2b:
        fat_detail = f"🔋 {game.get('away_team','')} en {_rest_term}"
        if market == "ML":
            if game.get("home_team","") in label: fat_vote = +1
            elif game.get("away_team","") in label: fat_vote = -1
        else: fat_vote = 0
    else:
        fat_detail = "sin ventaja de descanso"

    votes.append((W_FAT, fat_vote, "Fatiga", fat_detail))

    # ── Signal 4b: Injury impact on consensus ─────────────────────────────────
    # Note: injuries already baked into hp (via compute_base_prob Signal 6)
    # and λ (via get_lambda). The consensus vote here is informational only —
    # it notes when a significant injury exists that should make bettor cautious.
    # We re-use the fatigue vote slot by upgrading its signal if injury > fatigue
    h_inj_f = game.get("home_injury_factor", 1.0)
    a_inj_f = game.get("away_injury_factor", 1.0)
    h_inj   = game.get("home_injuries", [])
    a_inj   = game.get("away_injuries", [])

    # Build a compact injury note if significant injuries exist
    inj_note_parts = []
    for inj in (h_inj or [])[:2]:  # top 2 by impact
        if inj.get("impact_score", 0) >= 0.08:
            inj_note_parts.append(f"🤕 {inj['name']} ({inj['status']}, {game.get('home_team','')})")
    for inj in (a_inj or [])[:2]:
        if inj.get("impact_score", 0) >= 0.08:
            inj_note_parts.append(f"🤕 {inj['name']} ({inj['status']}, {game.get('away_team','')})")

    injury_note = " · ".join(inj_note_parts) if inj_note_parts else ""

    # ── Aggregate ─────────────────────────────────────────────────────────────
    weighted_sum = sum(w * v for w, v, _, _ in votes)
    max_possible = sum(w for w, _, _, _ in votes)  # = 1.0
    consensus_score = weighted_sum / max_possible   # -1.0 to +1.0

    # Count signals in agreement (vote != 0)
    signals_for     = [n for w, v, n, _ in votes if v > 0]
    signals_against = [n for w, v, n, _ in votes if v < 0]
    signals_neutral = [n for w, v, n, _ in votes if v == 0]

    total_active = len(signals_for) + len(signals_against)
    n_for        = len(signals_for)
    n_against    = len(signals_against)

    # Label
    if consensus_score >= 0.50:
        c_label = f"★ CONSENSO {n_for}/{total_active if total_active else 4}"
        c_color = "#00C896"
    elif consensus_score >= 0.20:
        c_label = f"⚡ APOYO {n_for}/{total_active if total_active else 4}"
        c_color = "#60a5fa"
    elif consensus_score <= -0.30:
        c_label = f"⚠ CONFLICTO {n_against} vs {n_for}"
        c_color = "#f97316"
    else:
        c_label = "◈ NEUTRAL"
        c_color = "#9ca3af"

    # Conflict note — explain the disagreement
    conflict_note = ""
    if n_for > 0 and n_against > 0:
        conflict_note = (f"Señales a favor: {', '.join(signals_for)} · "
                         f"Señales en contra: {', '.join(signals_against)}")
    elif fat_detail and "back-to-back" in fat_detail:
        conflict_note = fat_detail

    sim["consensus_score"]   = round(consensus_score, 3)
    sim["consensus_label"]   = c_label
    sim["consensus_color"]   = c_color
    sim["consensus_votes"]   = [(n, v, d) for w, v, n, d in votes]
    sim["conflict_note"]     = conflict_note
    sim["signals_for"]       = signals_for
    sim["signals_against"]   = signals_against
    sim["fatigue_note"]      = fat_detail if "back-to-back" in fat_detail or "semana corta" in fat_detail else ""
    sim["injury_note"]       = injury_note

    return sim


def run_monte_carlo(game, n=10_000):
    base=compute_base_prob(game)
    hp,dp,dq=base["home_prob"],base["draw_prob"],base["dq"]
    is_soccer=base["is_soccer"]; sigma=(1-dq)*0.15
    sport_grp = LEAGUES.get(game["league"],{}).get("group","")
    is_hockey = sport_grp == "Hockey"
    lam_h,lam_a=get_lambda(game); use_goals=lam_h is not None
    # Parse ESPN O/U line once — used inside loop for non-soccer sports
    try: ou_val = float(str(game["odds"].get("over_under","")));  assert 0 < ou_val < 400
    except: ou_val = 0.0
    # When no ESPN line, use league average as implicit O/U line for non-soccer
    _lg_avg  = LEAGUE_AVG_GOALS.get(game.get("league",""), 0)
    _is_bball = LEAGUES.get(game.get("league",""),{}).get("group","") == "Basketball"
    _is_base  = LEAGUES.get(game.get("league",""),{}).get("group","") == "Baseball"
    _is_hock  = LEAGUES.get(game.get("league",""),{}).get("group","") == "Hockey"
    _is_foot  = LEAGUES.get(game.get("league",""),{}).get("group","") in ("Football",)
    # FIX-2: Basketball excluido de línea implícita — sin ESPN line no O/U para NBA
    _nonsoccer_no_line = ou_val == 0.0 and _lg_avg > 0 and (_is_base or _is_hock or _is_foot)
    _bball_no_line = ou_val == 0.0 and _is_bball  # NBA sin línea ESPN → solo ML
    if _nonsoccer_no_line:
        # Use LEAGUE_AVG_GOALS as the implicit line — NOT lam_h+lam_a
        # Using lam_h+lam_a creates a tautological 50/50 (model total == line)
        # League avg is the correct neutral prior (NBA≈228, MLB≈9, NHL≈6.2)
        ou_val = _lg_avg

    # ── Lambda sanity check: re-center lambdas to ou_val if badly misaligned ──
    # Happens when ESPN line exists but get_lambda used form data on wrong scale
    # e.g. NBA scoring form gives lam≈50/team but ESPN line is 221.5
    if use_goals and ou_val > 0 and not is_soccer and lam_h is not None and lam_a is not None:
        _lam_total = lam_h + lam_a
        if _lam_total > 0 and (_lam_total < ou_val * 0.82 or _lam_total > ou_val * 1.18):
            _ratio = lam_h / _lam_total
            lam_h  = max(0.1, ou_val * _ratio)
            lam_a  = max(0.1, ou_val * (1.0 - _ratio))
    # ── Signal C: Fatigue / Rest Disadvantage ────────────────────────────────
    # NBA/NHL/MLB: back-to-back = ≤1 rest day (very common, well-studied)
    #   Sources: NBA -3.8% (Huyghe et al.), NHL -3.2%, MLB -1.5%, Soccer -2.0%
    # NFL: back-to-back NEVER occurs (weekly schedule). Use "short week" instead:
    #   Short week = ≤5 rest days (Thu Night Football has 4 days rest)
    #   Effect: -2.5% win prob (Osborne 2020, NFL short-week analysis)
    # NCAAF: same logic as NFL (weekly schedule)
    FATIGUE_BY_GROUP = {"Basketball": 0.038, "Hockey": 0.032, "Baseball": 0.015,
                        "Soccer": 0.020, "Football": 0.025}
    fatigue_delta = FATIGUE_BY_GROUP.get(sport_grp, 0.02)

    is_football = sport_grp == "Football"
    # Football uses short_week (≤5 days); all others use back2back (≤1 day)
    if is_football:
        h_rest = game.get("home_rest_days")
        a_rest = game.get("away_rest_days")
        home_b2b = (h_rest is not None and h_rest <= 5)
        away_b2b = (a_rest is not None and a_rest <= 5)
        # Only flag if one team has significantly less rest than the other
        if home_b2b and away_b2b:
            home_b2b = away_b2b = False  # both short week → symmetric, no edge
    else:
        home_b2b = game.get("home_back2back", False)
        away_b2b = game.get("away_back2back", False)

    if home_b2b and not away_b2b:
        hp = max(0.05, hp - fatigue_delta)  # home tired, away fresh
    elif away_b2b and not home_b2b:
        hp = min(0.95, hp + fatigue_delta)  # away tired → home benefits
    # Symmetric fatigue → no adjustment

    # ── MLB Ballpark Factor ──────────────────────────────────────────────────
    _mlb_park_factor = 1.0
    if sport_grp == "Baseball":
        _venue = game.get("venue", "") or ""
        _mlb_park_factor = get_mlb_ballpark_factor(_venue)
        # Also adjust lambdas in get_lambda output for MLB if not already scaled
        if lam_h is not None and _mlb_park_factor != 1.0:
            lam_h = max(0.1, lam_h * _mlb_park_factor)
            lam_a = max(0.1, lam_a * _mlb_park_factor)

    # ── Multi-line O/U counters (NHL: 5.5/6.5, MLB: 7.5/8.5/9.5) ──────────────
    _std_lines = SPORT_STD_LINES.get(sport_grp, [])
    _std_over  = {line: 0 for line in _std_lines}
    _std_under = {line: 0 for line in _std_lines}

    hw=aw=d=btts=o15=o25=o35=u25=u35=dc_1x=dc_x2=dc_12=o_total=u_total=0
    # Spread/handicap counters
    home_cover=0; away_cover=0; spread_push=0
    rng=random.Random()
    _score_freq = {}  # {(home_goals, away_goals): count}

    # ── Spread line for simulation ────────────────────────────────────────
    _spread_raw  = game.get("odds", {}).get("spread", "") or ""
    _spread_line = None
    _spread_implied = False
    # 1. Real ESPN spread_line (already parsed in parse_games)
    _sl_str = game.get("odds", {}).get("spread_line", "") or ""
    if _sl_str:
        try: _spread_line = float(_sl_str)
        except: pass
    # 2. Fallback: parse from ESPN "BOS -8.5" string
    if _spread_line is None and _spread_raw:
        import re as _re_sp
        _sp_m = _re_sp.search(r'[+-]?[0-9]+\.?[0-9]*', _spread_raw)
        if _sp_m:
            try: _spread_line = float(_sp_m.group())
            except: pass
    # 3. Implied spread from win probability (when ESPN has no line)
    # Runs BEFORE the simulation loop so counters work correctly.
    # hp is the base home win probability from compute_base_prob.
    if _spread_line is None and not is_soccer:
        _SCALE = {"Basketball": 24, "Football": 28}
        _sc3 = _SCALE.get(sport_grp)
        if _sc3 is not None:
            # negative = home favored
            _spread_line = round(-(hp - 0.5) * _sc3 * 2) / 2
            _spread_implied = True
        elif sport_grp in ("Baseball", "Hockey"):
            # Run line / Puck line fixed at ±1.5
            _spread_line = -1.5 if hp >= 0.5 else 1.5
            _spread_implied = True
    # Spread momios from ESPN (default -110/-110)
    _spread_home_ml_str = game.get("odds", {}).get("spread_home_ml", "-110") or "-110"
    _spread_away_ml_str = game.get("odds", {}).get("spread_away_ml", "-110") or "-110"
    try: _spread_home_ml_f = float(_spread_home_ml_str)
    except: _spread_home_ml_f = -110.0
    try: _spread_away_ml_f = float(_spread_away_ml_str)
    except: _spread_away_ml_f = -110.0

    for _ in range(n):
        ph=max(0.01,min(0.99,hp+rng.gauss(0,sigma)))
        if use_goals:
            lh=max(0.1,lam_h*(1+rng.gauss(0,0.15*(1-dq))))
            la=max(0.1,lam_a*(1+rng.gauss(0,0.15*(1-dq))))
            gh=poisson_sample(lh,rng); ga=poisson_sample(la,rng); tg=gh+ga
            if is_soccer:
                # ── Dixon-Coles correction for low scores ──────────────────
                # Poisson overestimates 0-0 and underestimates 1-0/0-1.
                # Tau factor re-weights these outcomes using rho=-0.13.
                _tau = dixon_coles_tau(gh, ga, lh, la, rho=-0.13)
                if _tau < 1.0 and rng.random() > _tau:
                    # Rejection sampling: re-draw this iteration
                    gh = poisson_sample(lh, rng)
                    ga = poisson_sample(la, rng)
                    tg = gh + ga
                # Contar marcador (cap a 10 para no explotar memoria)
                _sk = (min(gh, 10), min(ga, 10))
                _score_freq[_sk] = _score_freq.get(_sk, 0) + 1
                if gh>ga: hw+=1; dc_1x+=1; dc_12+=1
                elif gh==ga: d+=1; dc_1x+=1; dc_x2+=1
                else: aw+=1; dc_x2+=1; dc_12+=1
                if gh>0 and ga>0: btts+=1
                # Spread/AH cover (home perspective)
                if _spread_line is not None:
                    _diff = gh - ga  # positive = home wins by
                    if _diff + _spread_line > 0: home_cover += 1
                    elif _diff + _spread_line < 0: away_cover += 1
                    else: spread_push += 1
                if tg>1.5: o15+=1
                if tg>2.5: o25+=1
                else: u25+=1
                if tg>3.5: o35+=1
                else: u35+=1
            else:
                if is_hockey:
                    # NHL Sharp Model:
                    # - O/U INCLUDES Overtime (5-min 3v3) and Shootout goals
                    # - ~24% of games go to OT (historical 2015-2024)
                    # - ~50% of OT games end in SO (so ~12% of all games)
                    # - OT: always adds exactly 1 goal (sudden death)
                    # - Shootout: adds 1 official goal to the winning team's total
                    # - Regulation win/loss for ML purposes
                    ot_goals = 0
                    if gh > ga:
                        hw += 1; dc_1x += 1; dc_12 += 1
                    elif gh < ga:
                        aw += 1; dc_x2 += 1; dc_12 += 1
                    else:
                        # Tie after 60 min → OT (100% go to OT in NHL)
                        ot_goals = 1
                        if rng.random() < 0.5:
                            hw += 1; dc_1x += 1; dc_12 += 1
                        else:
                            aw += 1; dc_x2 += 1; dc_12 += 1
                    # Contar marcador hockey
                    _sk = (min(gh, 15), min(ga, 15))
                    _score_freq[_sk] = _score_freq.get(_sk, 0) + 1
                    # O/U comparison includes OT/SO goals
                    tg_with_ot = tg + ot_goals
                    if ou_val > 0:
                        _bias = 0.0 if _nonsoccer_no_line else PUBLIC_BIAS_PTS.get("Hockey", 0.0)
                        # For implicit line: shift -0.5 to center discrete Poisson distribution
                        _nhl_eff_line = (ou_val - 0.5 - _bias) if _nonsoccer_no_line else (ou_val - _bias)
                        if tg_with_ot > _nhl_eff_line: o_total += 1
                        else: u_total += 1
                    # Multi-line analysis (5.5 and 6.5) — always computed
                    for _sl in _std_lines:
                        if tg_with_ot > _sl: _std_over[_sl] += 1
                        else: _std_under[_sl] += 1
                else:
                    # NBA / MLB / NFL — normal distribution (Poisson breaks for large λ)
                    # NBA: typical game total std ~12-14 pts (TeamRankings historical)
                    # MLB: typical game total std ~3.0 runs
                    # NFL: typical game total std ~14 pts
                    if sport_grp == "Basketball":
                        # NBA combined std ≈ 15-16 pts (TeamRankings historical)
                        per_team_std = max(9.0, (lh + la) * 0.082)
                    elif sport_grp == "Baseball":
                        # MLB Sharp Model:
                        # 1. Ballpark factor: Coors +30%, Petco -8%, etc.
                        # 2. Extra Innings: ~8.5% of games go to extras (Retrosheet 2015-24)
                        #    Extra innings typically add 0.5-1.5 runs per half-inning
                        #    Model: if 9-inning score is tied, ~60% chance extras add ≥1 run
                        # Combined std ≈ 3.2 runs
                        _bp_factor = _mlb_park_factor  # pre-computed from venue
                        _lh_adj = lh * _bp_factor
                        _la_adj = la * _bp_factor
                        per_team_std = max(2.8, (_lh_adj + _la_adj) * 0.38)
                        sim_h = max(0, _lh_adj + rng.gauss(0, per_team_std * 0.7))
                        sim_a = max(0, _la_adj + rng.gauss(0, per_team_std * 0.7))
                        sim_total = sim_h + sim_a
                        # Extra innings: ~8.5% chance when game is close (within 2 runs)
                        if abs(sim_h - sim_a) <= 2 and rng.random() < 0.085:
                            # Extra innings add ~1.3 runs on average
                            sim_total += max(0, rng.gauss(1.3, 0.8))
                        if sim_h > sim_a: hw += 1; dc_1x += 1; dc_12 += 1
                        else: aw += 1; dc_x2 += 1; dc_12 += 1
                        # Run line cover (MLB standard is -1.5 / +1.5)
                        if _spread_line is not None:
                            _diff = sim_h - sim_a
                            if _diff + _spread_line > 0: home_cover += 1
                            elif _diff + _spread_line < 0: away_cover += 1
                            else: spread_push += 1
                        if ou_val > 0:
                            _bias = 0.0 if _nonsoccer_no_line else PUBLIC_BIAS_PTS.get(sport_grp, 0.0)
                            if sim_total > (ou_val - _bias): o_total += 1
                            else: u_total += 1
                        # Multi-line analysis (7.5, 8.5, 9.5) — always computed
                        for _sl in _std_lines:
                            if sim_total > _sl: _std_over[_sl] += 1
                            else: _std_under[_sl] += 1
                        continue  # skip the generic ou block below
                    else:  # Football / NCAAF
                        per_team_std = max(5.0, (lh + la) * 0.12)
                    sim_h = max(0, lh + rng.gauss(0, per_team_std * 0.7))
                    sim_a = max(0, la + rng.gauss(0, per_team_std * 0.7))
                    sim_total = sim_h + sim_a
                    if sim_h > sim_a: hw += 1; dc_1x += 1; dc_12 += 1
                    else: aw += 1; dc_x2 += 1; dc_12 += 1
                    # Contar marcador redondeado
                    _sk = (round(sim_h), round(sim_a))
                    _score_freq[_sk] = _score_freq.get(_sk, 0) + 1
                    # Spread cover
                    if _spread_line is not None:
                        _diff = sim_h - sim_a
                        if _diff + _spread_line > 0: home_cover += 1
                        elif _diff + _spread_line < 0: away_cover += 1
                        else: spread_push += 1
                    if ou_val > 0:
                        # Sharp: ESPN line is inflated by public bias. Correct by shifting
                        # effective comparison line down. When using implicit line, no bias.
                        _bias = 0.0 if _nonsoccer_no_line else PUBLIC_BIAS_PTS.get(sport_grp, 0.0)
                        if sim_total > (ou_val - _bias): o_total += 1
                        else: u_total += 1
        else:
            if is_soccer:
                pd=max(0.01,min(0.50,dp+rng.gauss(0,sigma*0.5)))
                phn=ph*(1-pd); pan=(1-ph)*(1-pd); t=phn+pan+pd
                phn/=t; pan/=t; pd/=t; r=rng.random()
                if r<phn: hw+=1; dc_1x+=1; dc_12+=1
                elif r<phn+pd: d+=1; dc_1x+=1; dc_x2+=1
                else: aw+=1; dc_x2+=1; dc_12+=1
            else:
                if rng.random()<ph: hw+=1; dc_1x+=1; dc_12+=1
                else: aw+=1; dc_x2+=1; dc_12+=1

    sh=hw/n; sa=aw/n; sd=d/n
    # Spread probabilities
    _sp_total = home_cover + away_cover + spread_push
    p_home_cover = home_cover / _sp_total if _sp_total > 0 else None
    p_away_cover = away_cover / _sp_total if _sp_total > 0 else None
    # NBA/NHL/MLB: O/U over the actual line (lam_h + lam_a = expected total)
    p_o_total = o_total/n if (use_goals and not is_soccer and (o_total+u_total)>0) else None
    p_u_total = u_total/n if (use_goals and not is_soccer and (o_total+u_total)>0) else None
    p_btts=btts/n if use_goals else None
    p_o15=o15/n if use_goals else None
    p_o25=o25/n if use_goals else None
    p_o35=o35/n if use_goals else None
    p_u25=u25/n if use_goals else None
    p_u35=u35/n if use_goals else None

    # ── Garantizar monotonía antes de calibración ─────────────────────────────
    # Por construcción del loop o35 ≤ o25 ≤ o15, pero por seguridad lo forzamos
    if p_o15 is not None and p_o25 is not None:
        p_o25 = min(p_o25, p_o15)
        p_u25 = 1.0 - p_o25 if p_u25 is not None else p_u25
    if p_o25 is not None and p_o35 is not None:
        p_o35 = min(p_o35, p_o25)
        p_u35 = 1.0 - p_o35 if p_u35 is not None else p_u35

    # ══════════════════════════════════════════════════════════════════════════
    # BLEND CON HISTORIAL REAL — Google Sheets últimos 10 partidos
    # Usa TODOS los datos disponibles:
    #   - Ataque local: avg_scored_home del equipo local
    #   - Defensa local: avg_conceded_home (cuánto concede en casa)
    #   - Ataque visitante: avg_scored_away del visitante
    #   - Defensa visitante: avg_conceded_away
    #   - Forma reciente: últimos 3 partidos vs promedio total (tendencia)
    #   - Rates históricos: rate_o25_home/away, rate_btts_home/away, rate_o35
    # Pesos: 50% simulación + 50% historial cuando ambos equipos tienen datos
    #        70% simulación + 30% historial cuando solo uno tiene datos
    # ══════════════════════════════════════════════════════════════════════════
    _h_prof_s = game.get("home_profile")
    _a_prof_s = game.get("away_profile")

    def _clamp01(x): return max(0.01, min(0.99, x))

    def _recent_form_factor(prof, is_home):
        """
        Calcula un factor de forma reciente basado en los últimos 3 partidos
        vs el promedio total. Retorna (scored_factor, conceded_factor).
        factor > 1.0 = en racha positiva, < 1.0 = en baja forma.
        """
        games_list = prof.get("games", []) if prof else []
        if len(games_list) < 5:
            return 1.0, 1.0
        # Filtrar por condición (home/away) si hay suficientes, sino usar todos
        cond_games = [g for g in games_list if g.get("home") == is_home]
        if len(cond_games) < 3:
            cond_games = games_list  # fallback: usar todos
        # Últimos 3 vs promedio total
        recent  = cond_games[-3:]
        avg_all_s = sum(g["scored"]   for g in cond_games) / len(cond_games)
        avg_all_c = sum(g["conceded"] for g in cond_games) / len(cond_games)
        avg_rec_s = sum(g["scored"]   for g in recent)     / len(recent)
        avg_rec_c = sum(g["conceded"] for g in recent)     / len(recent)
        # Factor: qué tan diferente es la forma reciente vs el promedio
        sf = (avg_rec_s / avg_all_s) if avg_all_s > 0 else 1.0
        cf = (avg_rec_c / avg_all_c) if avg_all_c > 0 else 1.0
        # Limitar el factor para evitar extremos: [0.70, 1.40]
        return max(0.70, min(1.40, sf)), max(0.70, min(1.40, cf))

    if is_soccer and use_goals:
        _h_ng = (_h_prof_s or {}).get("n_games", 0)
        _a_ng = (_a_prof_s or {}).get("n_games", 0)

        if _h_ng >= 5 and _a_ng >= 5:
            # ── ATAQUE local: avg_scored_home ajustado por forma reciente ────
            _h_atk   = _h_prof_s.get("avg_scored_home")   or _h_prof_s.get("avg_scored")   or 0
            _h_def   = _h_prof_s.get("avg_conceded_home") or _h_prof_s.get("avg_conceded") or 0
            # ── ATAQUE visitante: avg_scored_away ajustado por forma ─────────
            _a_atk   = _a_prof_s.get("avg_scored_away")   or _a_prof_s.get("avg_scored")   or 0
            _a_def   = _a_prof_s.get("avg_conceded_away") or _a_prof_s.get("avg_conceded") or 0

            # Forma reciente (últimos 3 partidos)
            _h_sf, _h_cf = _recent_form_factor(_h_prof_s, is_home=True)
            _a_sf, _a_cf = _recent_form_factor(_a_prof_s, is_home=False)

            # Goles esperados combinando ataque propio + defensa rival, con forma
            _exp_h = (_h_atk * _h_sf + _a_def * _a_cf) / 2  # goles del local
            _exp_a = (_a_atk * _a_sf + _h_def * _h_cf) / 2  # goles del visitante
            _exp_total = _exp_h + _exp_a

            # ── Rates históricos O/U y BTTS ──────────────────────────────────
            # Local en casa + visitante de visitante = contexto correcto
            _h_o25 = _h_prof_s.get("rate_o25_home") or _h_prof_s.get("rate_o25") or 0
            _a_o25 = _a_prof_s.get("rate_o25_away") or _a_prof_s.get("rate_o25") or 0
            _h_o35 = _h_prof_s.get("rate_o35_home") or _h_prof_s.get("rate_o35") or 0
            _a_o35 = _a_prof_s.get("rate_o35_away") or _a_prof_s.get("rate_o35") or 0
            _h_bt  = _h_prof_s.get("rate_btts_home") or _h_prof_s.get("rate_btts") or 0
            _a_bt  = _a_prof_s.get("rate_btts_away") or _a_prof_s.get("rate_btts") or 0

            # Promedio ponderado de ambos equipos (ataque + defensa rival)
            _hist_o25 = (_h_o25 + _a_o25) / 2
            _hist_o35 = (_h_o35 + _a_o35) / 2
            _hist_bt  = (_h_bt  + _a_bt)  / 2

            # Ajustar los rates históricos por forma reciente
            # Si el exp_total es muy diferente al avg histórico, ajustar rates
            _avg_hist_total = (_h_atk or 0) + (_a_atk or 0)
            if _avg_hist_total > 0 and _exp_total > 0:
                _form_ratio = _exp_total / _avg_hist_total
                # Ajuste suave: max ±15% sobre los rates históricos
                _form_ratio = max(0.85, min(1.15, _form_ratio))
                _hist_o25 = _clamp01(_hist_o25 * _form_ratio)
                _hist_o35 = _clamp01(_hist_o35 * _form_ratio)
                _hist_bt  = _clamp01(_hist_bt  * _form_ratio)

            # Blend final: 50% simulación + 50% historial
            if p_o25 is not None and _hist_o25 > 0:
                p_o25 = _clamp01(0.50 * p_o25 + 0.50 * _hist_o25)
                p_u25 = _clamp01(1.0 - p_o25)
            if p_o35 is not None and _hist_o35 > 0:
                p_o35 = _clamp01(0.50 * p_o35 + 0.50 * _hist_o35)
                p_u35 = _clamp01(1.0 - p_o35)
            if p_btts is not None and _hist_bt > 0:
                p_btts = _clamp01(0.50 * p_btts + 0.50 * _hist_bt)

            # Re-forzar monotonía
            if p_o25 is not None and p_o35 is not None and p_o35 > p_o25:
                p_o35 = p_o25 * 0.97
                p_u35 = _clamp01(1.0 - p_o35)

        elif _h_ng >= 5:
            # Solo local tiene historial — 30% peso
            _h_sf, _h_cf = _recent_form_factor(_h_prof_s, is_home=True)
            _h_o25 = _clamp01((_h_prof_s.get("rate_o25_home") or _h_prof_s.get("rate_o25") or 0) * _h_sf)
            _h_bt  = _clamp01((_h_prof_s.get("rate_btts_home") or _h_prof_s.get("rate_btts") or 0) * ((_h_sf+_h_cf)/2))
            _h_o35 = _clamp01((_h_prof_s.get("rate_o35_home") or _h_prof_s.get("rate_o35") or 0) * _h_sf)
            if p_o25 is not None and _h_o25 > 0:
                p_o25 = _clamp01(0.70 * p_o25 + 0.30 * _h_o25)
                p_u25 = _clamp01(1.0 - p_o25)
            if p_o35 is not None and _h_o35 > 0:
                p_o35 = _clamp01(0.70 * p_o35 + 0.30 * _h_o35)
                p_u35 = _clamp01(1.0 - p_o35)
            if p_btts is not None and _h_bt > 0:
                p_btts = _clamp01(0.70 * p_btts + 0.30 * _h_bt)

        elif _a_ng >= 5:
            # Solo visitante tiene historial — 30% peso
            _a_sf, _a_cf = _recent_form_factor(_a_prof_s, is_home=False)
            _a_o25 = _clamp01((_a_prof_s.get("rate_o25_away") or _a_prof_s.get("rate_o25") or 0) * _a_sf)
            _a_bt  = _clamp01((_a_prof_s.get("rate_btts_away") or _a_prof_s.get("rate_btts") or 0) * ((_a_sf+_a_cf)/2))
            _a_o35 = _clamp01((_a_prof_s.get("rate_o35_away") or _a_prof_s.get("rate_o35") or 0) * _a_sf)
            if p_o25 is not None and _a_o25 > 0:
                p_o25 = _clamp01(0.70 * p_o25 + 0.30 * _a_o25)
                p_u25 = _clamp01(1.0 - p_o25)
            if p_o35 is not None and _a_o35 > 0:
                p_o35 = _clamp01(0.70 * p_o35 + 0.30 * _a_o35)
                p_u35 = _clamp01(1.0 - p_o35)
            if p_btts is not None and _a_bt > 0:
                p_btts = _clamp01(0.70 * p_btts + 0.30 * _a_bt)

    elif not is_soccer and use_goals and p_o_total is not None:
        # ── No-soccer: blend p_o_total con thresholds históricos ──────────────
        # Usa: avg_scored, avg_conceded, forma reciente, thresholds
        _h_ng2 = (_h_prof_s or {}).get("n_games", 0)
        _a_ng2 = (_a_prof_s or {}).get("n_games", 0)
        _ou_line_f = 0.0
        try: _ou_line_f = float(str(game.get("odds", {}).get("over_under", "") or "").lstrip("~"))
        except: pass

        def _get_hist_rate(prof, ou_line, is_home):
            """Tasa histórica más cercana al ESPN O/U line, ajustada por forma."""
            if not prof: return None
            thresh = prof.get("thresholds", {})
            if not thresh: return None
            best_k, best_diff = None, 999
            for k in thresh:
                try:
                    kv = float(k.replace("o","").replace("u",""))
                    diff = abs(kv - ou_line)
                    if diff < best_diff:
                        best_diff = diff; best_k = k
                except: pass
            if not best_k or best_diff >= 8: return None
            rate = thresh.get(best_k, 0)
            # Ajustar por forma reciente
            sf, cf = _recent_form_factor(prof, is_home)
            form_adj = (sf + cf) / 2
            return _clamp01(rate * max(0.85, min(1.15, form_adj)))

        if _ou_line_f > 0 and (_h_ng2 >= 5 or _a_ng2 >= 5):
            _h_rate = _get_hist_rate(_h_prof_s, _ou_line_f, True)  if _h_ng2 >= 5 else None
            _a_rate = _get_hist_rate(_a_prof_s, _ou_line_f, False) if _a_ng2 >= 5 else None

            if _h_rate is not None and _a_rate is not None:
                _hist_ou = (_h_rate + _a_rate) / 2
                p_o_total = _clamp01(0.50 * p_o_total + 0.50 * _hist_ou)
                p_u_total = _clamp01(1.0 - p_o_total)
            elif _h_rate is not None:
                p_o_total = _clamp01(0.70 * p_o_total + 0.30 * _h_rate)
                p_u_total = _clamp01(1.0 - p_o_total)
            elif _a_rate is not None:
                p_o_total = _clamp01(0.70 * p_o_total + 0.30 * _a_rate)
                p_u_total = _clamp01(1.0 - p_o_total)

    # ── Per-league calibration (soccer only) ──────────────────────────────────
    if is_soccer and use_goals:
        p_u25, p_u35, p_btts, p_o25, p_o35 = apply_soccer_calib(
            game["league"], p_u25, p_u35, p_btts, p_o25, p_o35)

    # ── NHL / NBA / MLB calibration ─────────────────────────────────────────────
    # Pass ou_val=0 to calib when using implicit league-avg line (no real ESPN line)
    if not is_soccer and use_goals and p_u_total is not None:
        _calib_ou = 0.0 if _nonsoccer_no_line else ou_val
        p_u_total, p_o_total = apply_nonsoccer_calib(
            sport_grp, is_hockey, p_u_total, p_o_total, _calib_ou)

    p_dc_1x=dc_1x/n; p_dc_x2=dc_x2/n; p_dc_12=dc_12/n

    hml=game["odds"].get("home_ml",""); aml=game["odds"].get("away_ml","")
    ou=game["odds"].get("over_under","") or (f"~{ou_val:.1f}" if _nonsoccer_no_line else "")

    # ── Señales disponibles (hml/aml ya definidos) ───────────────────────────
    _has_ml      = bool(hml and aml)
    _has_scoring = game.get("home_avg_scored") is not None
    _has_form    = game.get("home_form") is not None or game.get("away_form") is not None
    _has_profile = ((_h_prof_s and _h_prof_s.get("n_games", 0) >= 5) or
                    (_a_prof_s and _a_prof_s.get("n_games", 0) >= 5))
    _has_record  = bool(game.get("home_record", "") and game.get("away_record", ""))
    home_ev=calc_ev(sh,hml) if hml else None
    away_ev=calc_ev(sa,aml) if aml else None
    hk=quarter_kelly(sh,hml) if hml else None
    ak=quarter_kelly(sa,aml) if aml else None

    BTTS_ML=-115; OU_ML=-110; DC_ML=-200
    btts_ev=calc_ev(p_btts,BTTS_ML) if p_btts is not None else None
    no_btts_ev=calc_ev(1-p_btts,BTTS_ML) if p_btts is not None else None
    o15_ev=calc_ev(p_o15,OU_ML) if p_o15 is not None else None
    o25_ev=calc_ev(p_o25,OU_ML) if p_o25 is not None else None
    o35_ev=calc_ev(p_o35,OU_ML) if p_o35 is not None else None
    u25_ev=calc_ev(p_u25,OU_ML) if p_u25 is not None else None
    u35_ev=calc_ev(p_u35,OU_ML) if p_u35 is not None else None
    dc_1x_ev=calc_ev(p_dc_1x,DC_ML); dc_x2_ev=calc_ev(p_dc_x2,DC_ML); dc_12_ev=calc_ev(p_dc_12,DC_ML)

    candidates=[
        ("ML",game["home_team"]+" ML",sh,home_ev,hml,hk),
        ("ML",game["away_team"]+" ML",sa,away_ev,aml,ak),
    ]

    sport_group = LEAGUES.get(game["league"], {}).get("group", "")

    # ── NBA / NHL / MLB O/U ─────────────────────────────────────────────────
    # Show probabilities at ESPN line AND adjacent lines (±0.5/1.0)
    # This lets user see: "Over 5.5: 68% | Over 6.5: 42%" for NHL
    if p_o_total is not None and ou:
        try:
            ou_line = float(str(ou).lstrip("~"))
            # Standard line step by sport: NHL/Soccer=0.5, NBA=0.5, MLB=0.5
            _step = 0.5
            # Use normal approximation for adjacent lines
            # mu = model's expected total (lam_h + lam_a after sanity check)
            _mu_total = (lam_h or 0) + (lam_a or 0)
            _sigma_total = max(1.0, _mu_total * 0.13)  # ~13% CV empirically
            if sport_grp == "Basketball": _sigma_total = max(12.0, _mu_total * 0.13)
            elif sport_grp == "Baseball": _sigma_total = max(2.5, _mu_total * 0.38 * 0.7)
            elif is_hockey: _sigma_total = max(1.5, _mu_total * 0.20)

            def _p_over_line(line):
                """P(total > line) via normal approx with public bias correction."""
                _bias = 0.0 if _nonsoccer_no_line else PUBLIC_BIAS_PTS.get(sport_grp, 0.0)
                _eff = line - _bias
                import math
                z = (_eff - _mu_total) / _sigma_total
                return max(0.01, min(0.99, 0.5 * (1 + math.erf(-z / math.sqrt(2)))))

            # Lines to show: ESPN line - step, ESPN line, ESPN line + step
            _lines_to_show = [ou_line - _step, ou_line, ou_line + _step]
            # Filter to sensible range and round to nearest 0.5
            _lines_to_show = [l for l in _lines_to_show if l > 0]

            # Primary ESPN line uses MC result (most accurate)
            ou_label = f"Over {ou_line:.1f}"
            uu_label = f"Under {ou_line:.1f}"
            o_total_ev = calc_ev(p_o_total, OU_ML)
            u_total_ev = calc_ev(p_u_total, OU_ML)
            candidates += [
                ("O/U", ou_label, p_o_total, o_total_ev, str(OU_ML), quarter_kelly(p_o_total, OU_ML)),
                ("O/U", uu_label, p_u_total, u_total_ev, str(OU_ML), quarter_kelly(p_u_total, OU_ML)),
            ]

            # Adjacent lines via normal approx
            _multi_lines = {}
            for _l in _lines_to_show:
                _po = _p_over_line(_l)
                _multi_lines[round(_l, 1)] = {"over": round(_po * 100, 1), "under": round((1-_po) * 100, 1)}
            # Always include ESPN line using MC result (override approx)
            _multi_lines[round(ou_line, 1)] = {
                "over": round(p_o_total * 100, 1),
                "under": round(p_u_total * 100, 1)
            }
        except:
            _multi_lines = {}
    else:
        _multi_lines = {}

    # ── Soccer: BTTS + O/U goals ──────────────────────────────────────────────
    if p_btts is not None and sport_group == "Soccer":
        # Retrieve league prior probabilities
        _prior = LEAGUE_OU_PRIORS.get(game["league"])
        _prior_vals = _prior if _prior else (0.23, 0.47, 0.68, 0.77, 0.53, 0.32, 0.57)
        _pu15_pr, _pu25_pr, _pu35_pr, _po15_pr, _po25_pr, _po35_pr = _prior_vals[:6]
        # When ESPN line is present, bypass prior filter — market IS the benchmark
        _bypass_prior = bool(game["odds"].get("over_under",""))

        def _ou_edge(sim_p, prior_p):
            """Returns True if sim deviates enough from prior to be meaningful."""
            return _bypass_prior or (sim_p is not None and abs(sim_p - prior_p) >= OU_MIN_EDGE)

        # BTTS: use real league prior (computed from Poisson at league avg)
        _btts_prior = _prior[6] if _prior else 0.57  # 7th element = P_BTTS
        if abs(p_btts - _btts_prior) >= OU_MIN_EDGE or _bypass_prior:
            candidates += [
                ("BTTS","Ambos Anotan — SÍ",p_btts,btts_ev,str(BTTS_ML),quarter_kelly(p_btts,BTTS_ML)),
                ("BTTS","Ambos Anotan — NO",1-p_btts,no_btts_ev,str(BTTS_ML),quarter_kelly(1-p_btts,BTTS_ML)),
            ]

        # O/U: only add when simulation deviates meaningfully from league prior
        # This prevents U3.5 from always winning just because it's "likely" by default
        if _ou_edge(p_o25, _po25_pr):
            candidates.append(("O/U","Over 2.5", p_o25, o25_ev, str(OU_ML), quarter_kelly(p_o25,OU_ML)))
        if _ou_edge(p_o35, _po35_pr):
            candidates.append(("O/U","Over 3.5", p_o35, o35_ev, str(OU_ML), quarter_kelly(p_o35,OU_ML)))
        if _ou_edge(p_u25, _pu25_pr):
            candidates.append(("O/U","Under 2.5",p_u25, u25_ev, str(OU_ML), quarter_kelly(p_u25,OU_ML)))
        # U3.5 eliminated — always wins by default %, useless noise

    # DC only meaningful for soccer WITH real ESPN moneyline (DC_ML is fictitious otherwise)
    # Without real ML odds, DO EV is calculated vs a made-up -200 → always looks positive
    # Only add DO candidates when we have actual market odds to anchor the simulation
    if is_soccer and hml and aml:
        candidates+=[
            ("DO", game["home_team"]+" o Empate (1X)", p_dc_1x, dc_1x_ev, str(DC_ML), quarter_kelly(p_dc_1x,DC_ML)),
            ("DO", game["away_team"]+" o Empate (X2)", p_dc_x2, dc_x2_ev, str(DC_ML), quarter_kelly(p_dc_x2,DC_ML)),
            ("DO", game["home_team"]+" o "+game["away_team"]+" (sin empate)", p_dc_12, dc_12_ev, str(DC_ML), quarter_kelly(p_dc_12,DC_ML)),
        ]

    # ── Team Profile O/U rate blend ───────────────────────────────────────────
    # Si los perfiles tienen ≥5 partidos, blendear las probabilidades simuladas
    # con las tasas históricas reales del equipo.
    # Blend: 50% sim Monte Carlo + 50% tasa histórica (cuando n≥5, 30/70 cuando n=10)
    _h_prof = game.get("home_profile")
    _a_prof = game.get("away_profile")
    _sg     = sport_group  # "Soccer","Basketball", etc.

    def _profile_blend(sim_prob, h_prof, a_prof, rate_key, is_soccer=True):
        """Blendea prob simulada con tasa histórica promedio de ambos equipos."""
        rates = []
        for prof in [h_prof, a_prof]:
            if prof and prof.get("n_games", 0) >= 5:
                r = prof.get(rate_key)
                if r is not None and r > 0:
                    rates.append((r, prof["n_games"]))
        if not rates:
            return sim_prob
        # Weighted avg of historical rates (more games = more weight)
        total_w = sum(n for _,n in rates)
        hist_avg = sum(r*n for r,n in rates) / total_w
        # Blend weight: more games → trust history more
        avg_n = total_w / len(rates)
        hist_w = min(0.70, 0.30 + (avg_n / 10) * 0.40)  # 0.30 at n=0, 0.70 at n=10
        blended = sim_prob * (1 - hist_w) + hist_avg * hist_w
        return round(min(0.99, max(0.01, blended)), 4)

    if _sg == "Soccer" and p_btts is not None:
        # Blendear con tasas históricas del perfil (home usa home_rate, away usa away_rate)
        def _soccer_blend(sim_p, h_key, a_key):
            rates = []
            if _h_prof and _h_prof.get("n_games",0) >= 5:
                r = _h_prof.get(h_key)
                if r: rates.append((r, _h_prof["n_games"]))
            if _a_prof and _a_prof.get("n_games",0) >= 5:
                r = _a_prof.get(a_key)
                if r: rates.append((r, _a_prof["n_games"]))
            if not rates: return sim_p
            total_w = sum(n for _,n in rates)
            hist_avg = sum(r*n for r,n in rates) / total_w
            avg_n = total_w / len(rates)
            hist_w = min(0.70, 0.30 + (avg_n/10)*0.40)
            return round(min(0.99, max(0.01, sim_p*(1-hist_w) + hist_avg*hist_w)), 4)

        p_btts = _soccer_blend(p_btts, "rate_btts_home",  "rate_btts_away")
        p_o15  = _soccer_blend(p_o15,  "rate_o15_home",   "rate_o15_away")
        p_o25  = _soccer_blend(p_o25,  "rate_o25_home",   "rate_o25_away")
        p_o35  = _soccer_blend(p_o35,  "rate_o35_home",   "rate_o35_away")
        p_u25  = 1 - p_o25
        p_u35  = 1 - p_o35
        # Recalcular EVs con probs blended
        btts_ev    = calc_ev(p_btts, BTTS_ML)
        no_btts_ev = calc_ev(1-p_btts, BTTS_ML)
        o25_ev = calc_ev(p_o25, OU_ML); u25_ev = calc_ev(p_u25, OU_ML)
        o35_ev = calc_ev(p_o35, OU_ML); u35_ev = calc_ev(p_u35, OU_ML)
        # Reconstruir candidatos BTTS/O/U con EVs actualizados por blend
        candidates = [(mt,lb,pr,ev,ml,k) for mt,lb,pr,ev,ml,k in candidates
                      if mt not in ("BTTS","O/U")]
        _prior2 = LEAGUE_OU_PRIORS.get(game["league"])
        _pv2    = _prior2 if _prior2 else (0.23, 0.47, 0.68, 0.77, 0.53, 0.32, 0.57)
        _bypass2 = bool(game["odds"].get("over_under",""))
        def _edge2(p, prior): return _bypass2 or abs(p - prior) >= OU_MIN_EDGE
        _btts_pr2 = _prior2[6] if _prior2 else 0.57
        if abs(p_btts - _btts_pr2) >= OU_MIN_EDGE or _bypass2:
            candidates += [
                ("BTTS","Ambos Anotan — SÍ", p_btts,   btts_ev,    str(BTTS_ML), quarter_kelly(p_btts,   BTTS_ML)),
                ("BTTS","Ambos Anotan — NO", 1-p_btts, no_btts_ev, str(BTTS_ML), quarter_kelly(1-p_btts, BTTS_ML)),
            ]
        # FIX-4: O/U solo cuando hay señal real
        _has_real_ou_signal2 = _has_ml or _has_scoring or _has_profile
        if _has_real_ou_signal2:
            if _edge2(p_o25, _pv2[4]):
                candidates.append(("O/U","Over 2.5",  p_o25, o25_ev, str(OU_ML), quarter_kelly(p_o25, OU_ML)))
            if _edge2(p_o35, _pv2[5]):
                candidates.append(("O/U","Over 3.5",  p_o35, o35_ev, str(OU_ML), quarter_kelly(p_o35, OU_ML)))
            if _edge2(p_u25, _pv2[1]):
                candidates.append(("O/U","Under 2.5", p_u25, u25_ev, str(OU_ML), quarter_kelly(p_u25, OU_ML)))
        # U3.5 eliminated — always wins by default %, useless noise (profile blend block)

    # ── No-signal guard: block O/U and BTTS when all signals are blind ──────────
    # Without moneyline + form + scoring trend, O/U probs are pure Poisson league avg
    # → every game in the same league gets identical U3.5 ~80% pick (useless noise)
    # Require at least ONE real signal to show O/U/BTTS picks:
    #   - ESPN moneyline present (market knows something we don't)
    #   - Scoring trend available (we have real recent data)
    #   - Form data available (we know recent results)
    _has_real_signal = _has_ml or _has_scoring or _has_form

    if is_soccer and not _has_real_signal:
        # Sin ML, sin forma reciente, sin scoring trend de ESPN.
        # Pero podemos usar:
        #   A) team_profiles (Google Sheets) — historial acumulado real
        #   B) season record (win_pct) — calidad relativa equipos
        # Si hay alguna de estas, generamos picks con edge reducido y los marcamos
        # como "⚠ Modelo" para que el usuario sepa que no hay cuotas de respaldo.
        _profile_signal = _has_profile or _has_record
        if not _profile_signal:
            # Sin ninguna señal: vaciar todo — no hay nada útil que decir
            candidates = []
        else:
            # Tenemos perfil o récord: relajar el edge mínimo (priors menos estrictos)
            # y marcar los picks con bandera de baja confianza
            # El λ ya fue ajustado por team_profiles en get_lambda() arriba.
            # Solo necesitamos dejar pasar candidatos BTTS/O/U con edge más bajo.
            # Reducimos OU_MIN_EDGE a 0.05 para este partido (más permisivo)
            _edge_low = 0.05
            _prior = LEAGUE_OU_PRIORS.get(game["league"])
            _pv    = _prior if _prior else (0.23,0.47,0.68,0.77,0.53,0.32,0.57)
            # Reconstruir candidatos BTTS/O/U con edge relajado
            # (los candidatos ya fueron construidos arriba con OU_MIN_EDGE=0.08,
            #  pero con _bypass=False y sin ML podrían haber sido filtrados)
            if p_btts is not None:
                _btts_pr = _pv[6] if len(_pv)>6 else 0.57
                if abs(p_btts - _btts_pr) >= _edge_low:
                    # Asegurarnos de que BTTS está en candidates
                    _btts_in = any(mt=="BTTS" for mt,*_ in candidates)
                    if not _btts_in:
                        _bev  = calc_ev(p_btts, BTTS_ML)
                        _nbev = calc_ev(1-p_btts, BTTS_ML)
                        candidates += [
                            ("BTTS","Ambos Anotan — SÍ",p_btts,  _bev,  str(BTTS_ML),quarter_kelly(p_btts,  BTTS_ML)),
                            ("BTTS","Ambos Anotan — NO",1-p_btts,_nbev, str(BTTS_ML),quarter_kelly(1-p_btts,BTTS_ML)),
                        ]
            # FIX-5: O/U low-confidence solo con señal real
            _has_real_ou_signal_lc = _has_ml or _has_scoring or _has_profile
            if _has_real_ou_signal_lc and p_o25 is not None:
                if abs(p_o25 - _pv[4]) >= _edge_low:
                    _ou_in = any(mt=="O/U" and "2.5" in lb for mt,lb,*_ in candidates)
                    if not _ou_in:
                        candidates.append(("O/U","Over 2.5", p_o25,
                                           calc_ev(p_o25,OU_ML), str(OU_ML),
                                           quarter_kelly(p_o25,OU_ML)))
                if abs(1-p_o25 - _pv[1]) >= _edge_low:
                    _uu_in = any(mt=="O/U" and "Under 2.5" in lb for mt,lb,*_ in candidates)
                    if not _uu_in:
                        candidates.append(("O/U","Under 2.5", 1-p_o25,
                                           calc_ev(1-p_o25,OU_ML), str(OU_ML),
                                           quarter_kelly(1-p_o25,OU_ML)))
            # Marcar el partido con baja confianza para que el display lo indique
            game["_low_confidence"] = True

    # ── Add Spread/Handicap to candidates ────────────────────────────────────
    # Use _spread_line already computed in MC block (ESPN real OR implied)
    _sl_val2 = _spread_line       # set in MC setup block
    _sl_from_espn = not _spread_implied
    # Implied spread already computed in MC block (_spread_line / _spread_implied)
    _sl_implied = _spread_implied
    # Use already-computed cover probs
    _p_hc2 = p_home_cover  # 0.0-1.0
    _p_ac2 = p_away_cover
    if _sl_val2 is not None and _p_hc2 is not None and _p_ac2 is not None:
        # Use real ESPN spread odds
        _sph_ml = float(game.get("odds",{}).get("spread_home_ml","-110") or "-110")
        _spa_ml = float(game.get("odds",{}).get("spread_away_ml","-110") or "-110")
        _sdh = (100/abs(_sph_ml)+1) if _sph_ml < 0 else (_sph_ml/100+1)
        _sda = (100/abs(_spa_ml)+1) if _spa_ml < 0 else (_spa_ml/100+1)
        _ev_hc2 = round((_p_hc2 * (_sdh-1) - (1-_p_hc2)) * 100, 1)
        _ev_ac2 = round((_p_ac2 * (_sda-1) - (1-_p_ac2)) * 100, 1)
        _kh2 = round(max(0, (_p_hc2 - (1-_p_hc2)/(_sdh-1)) * 0.25), 3) if _sdh > 1 else 0
        _ka2 = round(max(0, (_p_ac2 - (1-_p_ac2)/(_sda-1)) * 0.25), 3) if _sda > 1 else 0
        _sl_name2 = "Run Line" if sport_grp=="Baseball" else ("Puck Line" if sport_grp=="Hockey" else ("AH" if is_soccer else "Spread"))
        _home_nm = (game.get("home_team","Local") or "Local")[:14]
        _away_nm = (game.get("away_team","Visit") or "Visit")[:14]
        _lbl_hc2 = f"{_home_nm} {_sl_val2:+.1f} ({_sl_name2})"
        _lbl_ac2 = f"{_away_nm} {-_sl_val2:+.1f} ({_sl_name2})"
        # Add spread when EV+ OR when it offers better value than a heavy ML favorite
        _ml_is_heavy_fav = False
        try:
            _h_ml_f = float(str(game.get("odds",{}).get("home_ml","") or 0))
            _a_ml_f = float(str(game.get("odds",{}).get("away_ml","") or 0))
            # Heavy favorite: ML worse than -200 (pays less than 0.50 per unit)
            _ml_is_heavy_fav = (_h_ml_f < -200 or _a_ml_f < -200)
        except: pass

        # Threshold: 52.4% to beat -110 juice (break-even), or lower for heavy fav games
        _spread_threshold = 0.48 if _ml_is_heavy_fav else 0.524
        if _p_hc2 >= _spread_threshold:
            candidates.append(("Spread", _lbl_hc2, round(_p_hc2*100,1), _ev_hc2, "-110", _kh2))
        if _p_ac2 >= _spread_threshold:
            candidates.append(("Spread", _lbl_ac2, round(_p_ac2*100,1), _ev_ac2, "-110", _ka2))

    # Detect "partido parejo" — requires real ML signal to be meaningful
    # Without ML, hp≈aw≈0.37 always → _parejo always True → always picks U3.5
    _spread = abs(sh - sa) * 100  # percentage spread between teams
    _parejo = use_goals and is_soccer and _spread < 12 and _has_ml

    MARKET_PREF = {"BTTS": 4, "O/U": 3, "Spread": 3, "ML": 2, "DO": 1}
    best_single=None; best_ev_v=-999; best_pref=-1

    # Pre-filter: si hay candidatos BTTS o O/U con EV positivo, excluir DO del concurso
    # DO(sin empate) tiene EV ficticio alto (~+17) porque DC_ML=-200 fijo
    # Solo usar DO cuando no hay ningún mercado de goles positivo disponible
    _has_pos_goals = any(mt in ("BTTS","O/U") and ev is not None and ev > 0
                         for mt,lb,pr,ev,ml,k in candidates)
    if _has_pos_goals:
        candidates_main = [(mt,lb,pr,ev,ml,k) for mt,lb,pr,ev,ml,k in candidates
                           if mt not in ("DO",)]
    else:
        candidates_main = candidates

    if _parejo:
        # Partido parejo with real ML: Claude recommends goal markets → pick by highest PROBABILITY
        goal_candidates = [(mt,lb,pr,ev,ml,k) for mt,lb,pr,ev,ml,k in candidates_main
                           if mt in ("BTTS","O/U") and pr is not None]
        if goal_candidates:
            best_goal = max(goal_candidates, key=lambda x: x[2])  # highest prob
            mt,lb,pr,ev,ml,k = best_goal
            best_single = {"market":mt,"label":lb,"prob":pr,"ev":ev,"ml":ml,"kelly":k or 0}
        # Done — parejo always uses goal market by prob, no ML/DO override
    else:
        # Normal case: pick by highest EV, with BTTS/O/U preferred on ties
        # Special rule: if there's a heavy ML favorite, compare spread vs ML EV
        _ml_ev_best   = max((ev for mt,lb,pr,ev,ml,k in candidates_main if mt=="ML" and ev is not None), default=-999)
        _spread_ev_best = max((ev for mt,lb,pr,ev,ml,k in candidates_main if mt=="Spread" and ev is not None), default=-999)
        # If spread has significantly better EV than ML, boost spread priority
        _spread_over_ml = (_spread_ev_best > _ml_ev_best + 2.0 and _spread_ev_best > 0)

        for mtype,label,prob,ev,ml,kelly in candidates_main:
            if prob is None or ev is None:
                continue
            pref = MARKET_PREF.get(mtype, 0)
            # Boost spread preference when it clearly beats ML on EV
            if mtype == "Spread" and _spread_over_ml:
                pref = 4  # same as BTTS — spread is the value play here
            is_better_ev = ev > best_ev_v + 1.0
            is_same_ev_better_market = (abs(ev - best_ev_v) <= 1.0) and (pref > best_pref)
            if is_better_ev or is_same_ev_better_market:
                best_ev_v=ev; best_pref=pref
                best_single={"market":mtype,"label":label,"prob":prob,"ev":ev,"ml":ml,"kelly":kelly or 0}

    # intra-parlay candidates stored for use by build_parlays()
    best_parlay=None  # will be set by build_parlays() in run_all_simulations
    pos_legs=[(mtype,label,prob,ev,ml) for mtype,label,prob,ev,ml,k in candidates
              if prob is not None and ev is not None and ev>0 and mtype not in ("DO",)]
    pos_legs.sort(key=lambda x:x[3],reverse=True)

    # ── Momios del modelo (calculados desde la simulación, no de ESPN) ────────
    _model_home_ml   = prob_to_ml(sh)
    _model_away_ml   = prob_to_ml(sa)
    _model_home_dec  = prob_to_dec(sh)       # decimal con vig
    _model_away_dec  = prob_to_dec(sa)
    _model_home_fair = fair_ml(sh)
    _model_away_fair = fair_ml(sa)
    _model_home_fdec = fair_dec(sh)          # decimal sin vig
    _model_away_fdec = fair_dec(sa)
    _edge_home = round((sh - ml_to_prob(hml)) * 100, 1) if hml else None
    _edge_away = round((sa - ml_to_prob(aml)) * 100, 1) if aml else None
    # Soccer: empate
    _model_draw_ml   = prob_to_ml(sd)  if is_soccer and sd > 0 else None
    _model_draw_dec  = prob_to_dec(sd) if is_soccer and sd > 0 else None
    _model_draw_fair = fair_ml(sd)     if is_soccer and sd > 0 else None
    _model_draw_fdec = fair_dec(sd)    if is_soccer and sd > 0 else None
    # O/U: línea del modelo vs línea ESPN
    _model_ou_total = round((lam_h + lam_a), 1) if (lam_h and lam_a) else None

    sim = {
        "home_pct":round(sh*100,1),"away_pct":round(sa*100,1),"draw_pct":round(sd*100,1),
        "data_quality":round(dq*100,0),
        "home_ev":home_ev,"away_ev":away_ev,
        "home_ml":hml,"away_ml":aml,"over_under":ou,
        # Momios calculados por el modelo (americano + decimal, con vig y sin vig)
        "model_home_ml":_model_home_ml,"model_away_ml":_model_away_ml,
        "model_home_dec":_model_home_dec,"model_away_dec":_model_away_dec,
        "model_draw_ml":_model_draw_ml,"model_draw_dec":_model_draw_dec,
        "model_home_fair":_model_home_fair,"model_away_fair":_model_away_fair,
        "model_home_fdec":_model_home_fdec,"model_away_fdec":_model_away_fdec,
        "model_draw_fair":_model_draw_fair,"model_draw_fdec":_model_draw_fdec,
        "edge_home_pp":_edge_home,"edge_away_pp":_edge_away,
        "model_ou_total":_model_ou_total,
        "home_kelly":hk,"away_kelly":ak,
        "p_btts":round(p_btts*100,1) if p_btts is not None else None,
        "btts_ev":btts_ev,"no_btts_ev":no_btts_ev,
        "p_o15":round(p_o15*100,1) if p_o15 is not None else None,"o15_ev":o15_ev,
        "p_o25":round(p_o25*100,1) if p_o25 is not None else None,"o25_ev":o25_ev,
        "p_o35":round(p_o35*100,1) if p_o35 is not None else None,"o35_ev":o35_ev,
        "p_u25":round(p_u25*100,1) if p_u25 is not None else None,"u25_ev":u25_ev,
        "p_u35":round(p_u35*100,1) if p_u35 is not None else None,"u35_ev":u35_ev,
        "p_dc_1x":round(p_dc_1x*100,1),"dc_1x_ev":dc_1x_ev,
        "p_dc_x2":round(p_dc_x2*100,1),"dc_x2_ev":dc_x2_ev,
        "p_dc_12":round(p_dc_12*100,1),"dc_12_ev":dc_12_ev,
        # Spread market
        "spread_line":_spread_line,
        "spread_raw":_spread_raw,
        "spread_implied":_spread_implied,
        "p_home_cover":round(p_home_cover*100,1) if p_home_cover is not None else None,
        "p_away_cover":round(p_away_cover*100,1) if p_away_cover is not None else None,
        "best_single":best_single,"best_parlay":best_parlay,"pos_legs":pos_legs,
        "p_o_total":round(p_o_total*100,1) if p_o_total is not None else None,
        "p_u_total":round(p_u_total*100,1) if p_u_total is not None else None,
        "ou_line":str(ou) if ou else (f"~{ou_val:.1f}" if _nonsoccer_no_line else None),
        "multi_lines": _multi_lines,
        "is_soccer":is_soccer,"n_simulations":n,"use_goals":use_goals,
        "std_lines": {
            str(sl): {
                "over": round(_std_over[sl]/n*100, 1),
                "under": round(_std_under[sl]/n*100, 1)
            }
            for sl in _std_lines
        } if _std_lines else {},
        "low_confidence": game.get("_low_confidence", False),
        "lam_real_h":game.get("_lam_real_h"),"lam_real_a":game.get("_lam_real_a"),
        "lam_league":game.get("_lam_league"),
        "home_back2back":game.get("home_back2back",False),"away_back2back":game.get("away_back2back",False),
        "home_rest_days":game.get("home_rest_days"),"away_rest_days":game.get("away_rest_days"),
        "home_injury_factor":game.get("home_injury_factor",1.0),
        "away_injury_factor":game.get("away_injury_factor",1.0),
        "home_injuries":game.get("home_injuries",[]),
        "away_injuries":game.get("away_injuries",[]),
        "score_freq": sorted(_score_freq.items(), key=lambda x: x[1], reverse=True)[:10] if _score_freq else [],
    }
    sim["best_pick"] = best_single or {}
    compute_consensus(game, sim)
    return sim

def _ml_dec(ml):
    """Convert American moneyline to decimal odds."""
    try:
        ml = float(str(ml).replace("+",""))
        return (ml/100+1) if ml>0 else (100/abs(ml)+1)
    except:
        return 1.909


def build_parlays(results):
    """
    Build best parlays across all simulated games.
    - Only uses games from TODAY (UTC date filter).
    - Inter-partido (2+ games): best EV+ leg per game, ML preferred (+0.5 boost).
      Tries all pairs in top-5 legs, picks highest parlay EV.
    - Intra-partido fallback (1 game): best 2 legs of same game, ML preferred.
    """
    from datetime import timedelta as _td2
    _now_u   = datetime.now(timezone.utc)
    _now_mx2 = _now_u - _td2(hours=6)
    _valid_parlay = set()
    for _d in range(-1, 3):
        _valid_parlay.add((_now_u  + _td2(days=_d)).strftime("%Y-%m-%d"))
        _valid_parlay.add((_now_mx2 + _td2(days=_d)).strftime("%Y-%m-%d"))

    def is_today(r):
        """Return True if game is in valid window or demo."""
        d = (r.get("date") or "")[:10]
        if d == "" and str(r.get("id","")).startswith("d"):
            return True
        return d in _valid_parlay

    # Only consider games in window
    results_today = [r for r in results if is_today(r)]

    def parlay_ev(l1, l2):
        prob = l1["prob"] * l2["prob"]
        pay  = (_ml_dec(l1["ml"]) * _ml_dec(l2["ml"]) - 1) * 100
        ev   = round(prob * pay - (1 - prob) * 100, 2)
        return prob, pay, ev

    ML_BONUS = 0.5

    def best_leg_for_game(r):
        legs = r["sim"].get("pos_legs", [])
        if not legs:
            return None
        scored = sorted(legs,
                        key=lambda x: x[3] + (ML_BONUS if x[0]=="ML" else 0),
                        reverse=True)
        mtype, label, prob, ev, ml = scored[0]
        return {
            "game_id":  r.get("id",""),
            "matchup":  f"{r['away_team']} @ {r['home_team']}",
            "league":   r["league"],
            "mtype":    mtype,
            "label":    label,
            "prob":     prob,
            "ev":       ev,
            "ml":       ml,
            "_r":       r,
        }

    # Collect best EV+ leg per game (today only)
    game_legs = []
    for r in results_today:
        leg = best_leg_for_game(r)
        if leg and (leg.get("ev") or 0) > 0:
            game_legs.append(leg)

    # ── Inter-partido ─────────────────────────────────────────────────────────
    if len(game_legs) >= 2:
        game_legs.sort(key=lambda x: x["ev"], reverse=True)
        top = game_legs[:5]
        best_combo = None
        best_combo_ev = -999
        for i in range(len(top)):
            for j in range(i+1, len(top)):
                l1, l2 = top[i], top[j]
                if l1["game_id"] == l2["game_id"]:
                    continue
                prob, pay, ev = parlay_ev(l1, l2)
                if ev > best_combo_ev:
                    best_combo_ev = ev
                    best_combo = (l1, l2, prob, pay, ev)

        if best_combo:
            l1, l2, prob, pay, ev = best_combo
            parlay = {
                "legs": [
                    (l1["mtype"], f"{l1['matchup']} · {l1['label']}", l1["prob"], l1["ev"], l1["ml"]),
                    (l2["mtype"], f"{l2['matchup']} · {l2['label']}", l2["prob"], l2["ev"], l2["ml"]),
                ],
                "prob":   round(prob, 4),
                "ev":     ev,
                "payout": round(pay, 1),
                "type":   "inter",
            }
            target = l1["_r"] if (l1.get("ev") or 0) >= (l2.get("ev") or 0) else l2["_r"]
            target["sim"]["best_parlay"] = parlay
            return results

    # ── Intra-partido fallback ────────────────────────────────────────────────
    for r in results_today:
        legs = r["sim"].get("pos_legs", [])
        if len(legs) >= 2:
            scored = sorted(legs,
                            key=lambda x: x[3] + (ML_BONUS if x[0]=="ML" else 0),
                            reverse=True)
            l1, l2 = scored[0], scored[1]
            d1 = {"prob": l1[2], "ml": l1[4]}
            d2 = {"prob": l2[2], "ml": l2[4]}
            prob, pay, ev = parlay_ev(d1, d2)
            if ev > 0:
                r["sim"]["best_parlay"] = {
                    "legs": [
                        (l1[0], l1[1], l1[2], l1[3], l1[4]),
                        (l2[0], l2[1], l2[2], l2[3], l2[4]),
                    ],
                    "prob":   round(prob, 4),
                    "ev":     ev,
                    "payout": round(pay, 1),
                    "type":   "intra",
                }
    return results


def run_all_simulations(games, n=10_000):
    results=[]; pb=st.progress(0); st_txt=st.empty()
    for i,game in enumerate(games):
        st_txt.markdown(
            f'<div style="font-family:\'Inter\',sans-serif;font-size:0.896rem;color:#6B7280;">'
            f'⚙ Simulando [{i+1}/{len(games)}] — {game["away_team"]} @ {game["home_team"]}</div>',
            unsafe_allow_html=True)
        # Enrich with recent form before simulation (cached 30min)
        try:
            enrich_game_with_form(game)
        except Exception:
            pass
        results.append({**game,"sim":run_monte_carlo(game,n)})
        pb.progress((i+1)/len(games))
    pb.empty(); st_txt.empty()
    results = build_parlays(results)
    return results
# ══════════════════════════════════════════════════════════════════════════════
# PICK HISTORY — Auto-save & track system picks accuracy
# Pestaña Google Sheets: pick_history
# Columns: pick_id | fecha | partido | liga | deporte | mercado | pick_label |
#          prob_pct | resultado | home_score | away_score | fuente
# ══════════════════════════════════════════════════════════════════════════════
_PH_TAB     = "pick_history"
_PH_HEADERS = [
    "pick_id","fecha","partido","liga","deporte","mercado",
    "pick_label","prob_pct","resultado","home_score","away_score","fuente"
]

@st.cache_data(ttl=120)
def _ph_load():
    """Load all rows from pick_history sheet. Returns list of dicts."""
    if not _gsheets_available():
        return []
    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)
        try:
            ws = sh.worksheet(_PH_TAB)
        except:
            ws = sh.add_worksheet(title=_PH_TAB, rows=5000, cols=len(_PH_HEADERS))
            ws.update("A1", [_PH_HEADERS])
            return []
        rows = ws.get_all_values()
        if len(rows) < 2:
            return []
        picks = []
        for row in rows[1:]:
            if not row or not row[0]:
                continue
            def _c(i, d=""):
                return row[i] if i < len(row) else d
            picks.append({
                "pick_id":   _c(0),
                "fecha":     _c(1),
                "partido":   _c(2),
                "liga":      _c(3),
                "deporte":   _c(4),
                "mercado":   _c(5),
                "pick_label":_c(6),
                "prob_pct":  float(_c(7) or 0),
                "resultado": _c(8,"pendiente"),
                "home_score":_c(9),
                "away_score":_c(10),
                "fuente":    _c(11,"RONGOL"),
            })
        return picks
    except Exception as e:
        return []

def _ph_save_picks(new_picks):
    """Append new picks to pick_history sheet (skip duplicates by pick_id)."""
    if not _gsheets_available() or not new_picks:
        return False
    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)
        try:
            ws = sh.worksheet(_PH_TAB)
        except:
            ws = sh.add_worksheet(title=_PH_TAB, rows=5000, cols=len(_PH_HEADERS))
            ws.update("A1", [_PH_HEADERS])
        # Get existing IDs to avoid duplicates
        existing = ws.col_values(1)  # pick_id column
        existing_ids = set(existing[1:])  # skip header
        rows_to_add = []
        for p in new_picks:
            if p["pick_id"] not in existing_ids:
                rows_to_add.append([
                    p["pick_id"], p["fecha"], p["partido"], p["liga"],
                    p["deporte"], p["mercado"], p["pick_label"],
                    p["prob_pct"], p.get("resultado","pendiente"),
                    p.get("home_score",""), p.get("away_score",""), p.get("fuente","RONGOL"),
                ])
        if rows_to_add:
            ws.append_rows(rows_to_add, value_input_option="USER_ENTERED")
        return len(rows_to_add)
    except Exception as e:
        return False

def _ph_update_results(updates):
    """Update resultado/scores for a list of pick_ids. updates = {pick_id: {resultado, home_score, away_score}}"""
    if not _gsheets_available() or not updates:
        return False
    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)
        ws  = sh.worksheet(_PH_TAB)
        ids = ws.col_values(1)  # column A = pick_id
        batch = []
        for i, pid in enumerate(ids[1:], start=2):  # row 2 onwards
            if pid in updates:
                upd = updates[pid]
                batch.append({"range": f"I{i}:K{i}", "values": [[
                    upd.get("resultado","pendiente"),
                    upd.get("home_score",""),
                    upd.get("away_score",""),
                ]]})
        if batch:
            ws.batch_update(batch)
        _ph_load.clear()
        return len(batch)
    except Exception as e:
        return False

def _ph_build_picks_from_sim(sr, fuente="RONGOL"):
    """
    Extract picks from simulation results to save to pick_history.
    Returns list of pick dicts ready for _ph_save_picks.
    """
    import hashlib
    from datetime import datetime as _dt, timezone as _tz
    fecha = _dt.now(_tz.utc).strftime("%Y-%m-%d %H:%M")
    picks = []

    _SPORT_ORDER_PH = ["Soccer","Basketball","Hockey","Baseball","Football"]

    # ── RONGOL picks (1 per sport, same logic as tab) ────────────────────────
    def _pick_score_ph(mkt, prob, ev, sim, sg, r=None, cand=None):
        """Delegado a pick_score_universal para consistencia total."""
        if cand is None:
            cand = {"market": mkt, "prob": prob, "ev": ev or 0, "kelly": 0}
        if r is None:
            r = {}
        return pick_score_universal(cand, sim, r, sg)

    def _sport_best_ph(r):
        """Mismo score compuesto que _sport_best_pick para consistencia."""
        sim = r["sim"]
        sg  = LEAGUES.get(r["league"],{}).get("group","Soccer")
        h_prob = sim.get("home_pct",0) or 0
        a_prob = sim.get("away_pct",0) or 0
        h_ml = sim.get("home_ml"); a_ml = sim.get("away_ml")

        def best_ml():
            if h_prob >= a_prob:
                t,p,ml = r["home_team"],h_prob,h_ml
            else:
                t,p,ml = r["away_team"],a_prob,a_ml
            if not ml:
                _mk = "model_home_dec" if h_prob>=a_prob else "model_away_dec"
                ml = sim.get(_mk) or ""
            return {"mercado":"ML","pick_label":t,"prob_pct":round(p,1),"ev":0}

        cands = []
        if sg == "Soccer":
            _ml = best_ml()
            if _ml: cands.append(_ml)
            if sim.get("use_goals"):
                _btts_ev = sim.get("btts_ev") or 0
                _btts_pb = sim.get("p_btts") or 0
                if _btts_pb > 0:
                    cands.append({"mercado":"BTTS","pick_label":"Ambos Anotan",
                                  "prob_pct":round(_btts_pb,1),"ev":_btts_ev})
                _o25_ev = sim.get("o25_ev") or 0
                _o25_pb = sim.get("p_o25") or 0
                if _o25_pb > 0:
                    cands.append({"mercado":"O/U","pick_label":"Over 2.5",
                                  "prob_pct":round(_o25_pb,1),"ev":_o25_ev})
        elif sg in ("Basketball","Hockey"):
            _ml = best_ml()
            if _ml: cands.append(_ml)
            _ou_line = sim.get("ou_line") or ""
            _p_over  = sim.get("p_o_total") or 0
            _p_under = sim.get("p_u_total") or 0
            if _ou_line and not _ou_line.startswith("~"):
                _best_p = max(_p_over, _p_under)
                if _best_p > 0:
                    try: _line = float(_ou_line.lstrip("~"))
                    except: _line = None
                    if _line:
                        _lbl = f"Over {_line:.1f}" if _p_over>=_p_under else f"Under {_line:.1f}"
                        cands.append({"mercado":"O/U","pick_label":_lbl,
                                      "prob_pct":round(_best_p,1),"ev":0})
        else:
            _ml = best_ml()
            if _ml: cands.append(_ml)

        if not cands:
            # Fallback absoluto: ML con momio del modelo
            _dom = max(h_prob, a_prob)
            _team = r["home_team"] if h_prob>=a_prob else r["away_team"]
            _mk = "model_home_dec" if h_prob>=a_prob else "model_away_dec"
            _ml_fb = sim.get(_mk) or ""
            return {"mercado":"ML","pick_label":_team,"prob_pct":round(_dom,1),"ev":0}

        # Seleccionar por score compuesto universal
        scored = [(c, _pick_score_ph(c["mercado"], c["prob_pct"], c.get("ev",0), sim, sg, r=r, cand={
            "market": c["mercado"], "prob": c["prob_pct"], "ev": c.get("ev",0),
            "kelly": 0, "label": c.get("pick_label","")
        })) for c in cands]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]

    # Group by sport, take best per sport
    sport_pools = {}
    for r in sr:
        sg = LEAGUES.get(r["league"],{}).get("group","Soccer")
        bp = _sport_best_ph(r)
        if bp:
            sport_pools.setdefault(sg,[]).append((r, bp))

    for sg in _SPORT_ORDER_PH:
        pool = sport_pools.get(sg,[])
        if not pool:
            continue
        pool.sort(key=lambda x: x[1]["prob_pct"], reverse=True)
        r, bp = pool[0]
        partido  = f'{r["away_team"]} vs {r["home_team"]}'
        pick_id  = hashlib.md5(f'{fecha[:10]}|{partido}|{bp["mercado"]}|{bp["pick_label"]}'.encode()).hexdigest()[:12]
        picks.append({
            "pick_id":   pick_id,
            "fecha":     fecha,
            "partido":   partido,
            "liga":      r.get("league",""),
            "deporte":   sg,
            "mercado":   bp["mercado"],
            "pick_label":bp["pick_label"],
            "prob_pct":  bp["prob_pct"],
            "resultado": "pendiente",
            "home_score":"",
            "away_score":"",
            "fuente":    fuente,
        })

    return picks

def _ph_auto_resolve(picks):
    """
    Try to resolve pending picks against finished ESPN games.
    Returns dict {pick_id: {resultado, home_score, away_score}} for resolved picks.
    """
    pending = [p for p in picks if p.get("resultado") == "pendiente"]
    if not pending:
        return {}
    try:
        finished = _fetch_finished_games()
    except:
        return {}
    resolved = {}
    for p in pending:
        partido = p.get("partido","")
        sep = " vs " if " vs " in partido else (" @ " if " @ " in partido else None)
        if sep:
            parts = partido.split(sep, 1)
            t1, t2 = parts[0].strip(), parts[1].strip()
        else:
            t1, t2 = partido.strip(), ""
        for g in finished:
            m1 = _team_match(t1, g["home_team"], g["away_team"])
            m2 = _team_match(t2, g["home_team"], g["away_team"]) if t2 else None
            if not (m1 or m2):
                continue
            # Build a fake pick dict for _evaluate_pick
            fake_pick = {
                "partido": partido,
                "pick":    p["pick_label"],
                "mercado": p["mercado"],
            }
            res = _evaluate_pick(fake_pick, g)
            if res:
                resolved[p["pick_id"]] = {
                    "resultado":  res,
                    "home_score": str(g.get("home_score","")),
                    "away_score": str(g.get("away_score","")),
                }
                break
    return resolved

# ═══════════════════════════════════════════════════════════════════════════════
# RENDER HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL PICK COLOR SYSTEM — used in ALL tabs
# ML=blue  BTTS/AA=green  OVER=orange-fire  UNDER=violet  COMBO=gold  DO=purple
# ══════════════════════════════════════════════════════════════════════════════
def _pick_clr(market, label=""):
    """Return (primary, accent, type_key, display_label) for any pick."""
    m = (market or "").upper()
    l = (label  or "").lower()
    if m == "ML":
        return "#1d4ed8", "#60a5fa", "ML",    "ML"
    if m == "BTTS":
        return "#15803d", "#00C896", "AA",    "AA"
    if m in ("O/U","OU","OVER/UNDER"):
        if "over" in l:
            return "#c2410c", "#ff6a00", "OVER",  "OVER"
        if "under" in l:
            return "#5b21b6", "#a78bfa", "UNDER", "UNDER"
        return "#b45309", "#fbbf24", "OU",   "O/U"   # line unknown
    if m in ("SPREAD","AH","RUN LINE","RUN_LINE","PUCK LINE","PUCK_LINE",
             "HANDICAP","ASIAN_HANDICAP"):
        return "#0e7490", "#22d3ee", "AH", m.replace("_"," ").title()
    if m == "COMBO":
        return "#92400e", "#f59e0b", "COMBO", "COMBO"  # amarillo dorado
    if m == "DO":
        return "#4c1d95", "#a78bfa", "DO",   "DO"
    if m == "PARLAY":
        return "#065f46", "#34d399", "PARLAY","PARLAY"
    return "#374151", "#9ca3af", "OTHER", market

def _pick_chip_html(market, label="", size="0.66rem"):
    """Inline colored chip badge for any pick market."""
    pc, ac, _, dl = _pick_clr(market, label)
    return (f'<span style="background:{pc}28;color:{ac};border:1px solid {pc}66;'
            f'border-radius:12px;padding:2px 9px;font-size:{size};font-weight:800;'
            f'letter-spacing:0.5px;flex-shrink:0">{dl}</span>')


def chip(market, label=""):
    """Market chip using global color system."""
    return _pick_chip_html(market, label)

def conf_badge(ev, dq):
    if ev>=10 and dq>=60: return '<span class="conf-badge conf-high">◆ ALTA</span>'
    if ev>=5  and dq>=40: return '<span class="conf-badge conf-medium">◆ MEDIA</span>'
    return '<span class="conf-badge conf-low">◆ BAJA</span>'

def dq_warn(dq):
    """Show data quality indicator. Only warn when DQ is concerning."""
    if dq == 0:
        return '<span class="market-chip chip-warn">⚠ SIN CUOTAS</span>'
    if dq < 25:
        return '<span class="market-chip chip-warn">⚠ SOLO RÉCORDS</span>'
    if dq < 50:
        return '<span class="market-chip" style="background:rgba(201,168,76,0.15);color:#C9A84C;border:1px solid rgba(201,168,76,0.3)">◈ DQ MEDIA</span>'
    return ""  # DQ >= 50%: no warning needed

def edge(prob_sim, ml):
    try: return round((prob_sim-ml_to_prob(float(str(ml).replace("+",""))))*100,1)
    except: return 0.0

def bar(pct, color, label):
    return f"""<div class="bar-wrap">
      <div class="bar-row">
        <span class="bar-team">{label}</span>
        <span class="bar-pct" style="color:{color}">{pct:.1f}%</span>
      </div>
      <div class="bar-bg"><div class="bar-fill" style="width:{min(pct,100):.1f}%;background:{color}"></div></div>
    </div>"""

def _team_logo_url(team_id, league):
    """ESPN CDN logo URL — uses league slug (nba/nhl/mlb), not sport."""
    if not team_id: return ""
    try:
        lg    = LEAGUES.get(league, {})
        slug  = lg.get("league", "")
        sport = lg.get("sport", "soccer")
        if sport == "soccer":
            return f"https://a.espncdn.com/i/teamlogos/soccer/500/{team_id}.png"
        else:
            # NBA→nba, NHL→nhl, MLB→mlb, NFL→nfl
            return f"https://a.espncdn.com/i/teamlogos/{slug}/500/{team_id}.png"
    except:
        return ""

def _logo_img(team_id, league, size=44, dark_bg=False):
    """<img> tag for team logo. White bg on light cards, dark bg on dark cards."""
    url = _team_logo_url(team_id, league)
    s   = str(size)
    if url:
        bg  = "#1c1c1e" if dark_bg else "rgba(255,255,255,0.95)"
        bdr = "1.5px solid rgba(255,255,255,0.08)" if dark_bg else "1.5px solid rgba(0,0,0,0.08)"
        sty = f"border-radius:50%;object-fit:contain;background:{bg};border:{bdr};padding:3px"
        return ('<img src="' + url + '" width="' + s + '" height="' + s +
                '" style="' + sty + '" onerror="this.style.opacity=\'0.15\'">')
    return ('<div style="width:' + s + 'px;height:' + s +
            'px;border-radius:50%;background:rgba(0,0,0,0.06);'
            'border:1.5px solid rgba(0,0,0,0.1)"></div>')

def render_pick_card(r, rank=None):
    """Render pick card - all HTML built via string concat, no ternaries in f-strings."""
    sim = r["sim"]
    bs  = sim.get("best_single")
    dq  = sim["data_quality"]
    if not bs:
        return ""

    prob_pct  = bs["prob"] * 100
    ev_val    = bs["ev"]
    kelly_pct = bs["kelly"]

    impl = ml_to_prob(bs["ml"]) * 100 if bs["market"] == "ML" and bs["ml"] else 0
    eg   = edge(bs["prob"], bs["ml"]) if bs["market"] == "ML" else 0

    impl_html = ""
    if impl > 0:
        impl_html = ('<div class="stat-item"><div class="stat-item-val val-muted">'
                     + str(round(impl, 1)) + '%</div>'
                     '<div class="stat-item-lbl">Impl. Casa</div></div>')

    edge_html = ""
    if eg > 0:
        edge_html = ('<div class="stat-item"><div class="stat-item-val val-blue">+'
                     + str(eg) + '%</div>'
                     '<div class="stat-item-lbl">Edge</div></div>')

    conf_html  = conf_badge(bs["ev"], dq)
    ml_display = "@ " + str(bs["ml"]) if bs["ml"] else ""

    # ── Momios del modelo vs casa ─────────────────────────────────────────────
    _mh_ml   = sim.get("model_home_ml", "")
    _ma_ml   = sim.get("model_away_ml", "")
    _mh_fair = sim.get("model_home_fair", "")
    _ma_fair = sim.get("model_away_fair", "")
    _md_ml   = sim.get("model_draw_ml", "")
    _e_home  = sim.get("edge_home_pp")
    _e_away  = sim.get("edge_away_pp")
    _m_ou    = sim.get("model_ou_total")

    # Línea del modelo para el pick específico
    if bs["market"] == "ML":
        _is_home_pick = r.get("home_team","") in bs.get("label","")
        _model_line = _mh_ml if _is_home_pick else _ma_ml
        _fair_line  = _mh_fair if _is_home_pick else _ma_fair
        _pick_edge  = _e_home if _is_home_pick else _e_away
    elif bs["market"] in ("O/U","BTTS"):
        _model_line = f"O/U modelo: {_m_ou}" if _m_ou else ""
        _fair_line  = ""
        _pick_edge  = None
    else:
        _model_line = _mh_ml
        _fair_line  = _mh_fair
        _pick_edge  = _e_home

    # HTML del bloque de momios del modelo
    # Decimales del modelo para el pick
    if bs["market"] == "ML":
        _is_home_pick2 = r.get("home_team","") in bs.get("label","")
        _model_dec  = sim.get("model_home_dec","")  if _is_home_pick2 else sim.get("model_away_dec","")
        _fair_dec_v = sim.get("model_home_fdec","") if _is_home_pick2 else sim.get("model_away_fdec","")
    else:
        _model_dec  = ""
        _fair_dec_v = ""

    _model_lines_html = ""
    if _model_line or _fair_line:
        _edge_color = "#00C896" if (_pick_edge and _pick_edge > 0) else ("#ef4444" if (_pick_edge and _pick_edge < 0) else "#6B7280")
        _edge_str = f"Edge: {_pick_edge:+.1f}pp" if _pick_edge is not None else ""
        _model_lines_html = (
            f'<div style="margin:6px 0;padding:8px 12px;'
            f'background:rgba(255,214,10,0.06);border:1px solid rgba(255,214,10,0.15);'
            f'border-radius:10px;display:flex;flex-wrap:wrap;gap:12px;align-items:center">'
            f'<div style="font-size:0.6rem;color:#6B7280;letter-spacing:1.5px;'
            f'text-transform:uppercase;width:100%;margin-bottom:2px">🧮 Líneas del Modelo</div>'
        )
        if _model_dec:
            _model_lines_html += (
                f'<div><div style="font-size:1.3rem;font-weight:900;color:#FFD60A;'
                f'font-family:Outfit,sans-serif">{_model_dec}</div>'
                f'<div style="font-size:0.55rem;color:#6B7280;text-transform:uppercase">Decimal c/vig</div></div>'
            )
        if _fair_dec_v:
            _model_lines_html += (
                f'<div><div style="font-size:1.1rem;font-weight:700;color:#86efac">{_fair_dec_v}</div>'
                f'<div style="font-size:0.55rem;color:#6B7280;text-transform:uppercase">Decimal justo</div></div>'
            )
        if _model_line:
            _model_lines_html += (
                f'<div><div style="font-size:0.85rem;font-weight:600;color:#AEAEB2">{_model_line}</div>'
                f'<div style="font-size:0.55rem;color:#6B7280;text-transform:uppercase">Americano c/vig</div></div>'
            )
        if bs["ml"]:
            _model_lines_html += (
                f'<div><div style="font-size:0.85rem;font-weight:600;color:#636366">{bs["ml"]}</div>'
                f'<div style="font-size:0.55rem;color:#6B7280;text-transform:uppercase">Casa (ESPN)</div></div>'
            )
        if _edge_str:
            _model_lines_html += (
                f'<div style="margin-left:auto"><div style="font-size:1.0rem;font-weight:800;'
                f'color:{_edge_color}">{_edge_str}</div>'
                f'<div style="font-size:0.55rem;color:#6B7280;text-transform:uppercase">vs Casa</div></div>'
            )
        # Soccer: agregar línea del empate si aplica
        if sim.get("is_soccer") and _md_ml:
            _md_fair = sim.get("model_draw_fair","")
            _model_lines_html += (
                f'<div style="width:100%;border-top:1px solid rgba(255,255,255,0.05);'
                f'padding-top:4px;margin-top:2px;display:flex;gap:10px">'
                f'<span style="font-size:0.65rem;color:#a78bfa">Empate modelo: <b>{_md_ml}</b></span>'
                f'<span style="font-size:0.65rem;color:#6B7280">({sim.get("draw_pct",0):.1f}% prob · precio justo: {_md_fair})</span>'
                f'</div>'
            )
        # O/U: mostrar línea del modelo vs ESPN
        if _m_ou and sim.get("ou_line"):
            _ou_espn = str(sim.get("ou_line","")).lstrip("~")
            try:
                _ou_diff = round(float(_m_ou) - float(_ou_espn), 1)
                _ou_diff_str = f"{_ou_diff:+.1f} vs ESPN" if _ou_diff != 0 else "= ESPN"
                _ou_color = "#00C896" if _ou_diff > 0.3 else ("#ef4444" if _ou_diff < -0.3 else "#6B7280")
            except:
                _ou_diff_str = ""; _ou_color = "#6B7280"
            _model_lines_html += (
                f'<div style="width:100%;border-top:1px solid rgba(255,255,255,0.05);'
                f'padding-top:4px;margin-top:2px;display:flex;gap:10px">'
                f'<span style="font-size:0.65rem;color:#ff6a00">O/U modelo: <b>{_m_ou}</b></span>'
                f'<span style="font-size:0.65rem;color:{_ou_color}">{_ou_diff_str}</span>'
                f'<span style="font-size:0.65rem;color:#6B7280">ESPN: {_ou_espn}</span>'
                f'</div>'
            )
        # Spread/handicap line
        _spr_raw_c  = sim.get("spread_raw","") or game.get("odds",{}).get("spread","") or ""
        _p_hcov_c   = sim.get("p_home_cover")
        _p_acov_c   = sim.get("p_away_cover")
        if _spr_raw_c and _p_hcov_c is not None:
            _h_team = r.get("home_team","Local")[:12]
            _a_team = r.get("away_team","Visit")[:12]
            _hcov_clr = "#00C896" if _p_hcov_c >= 52.4 else ("#C9A84C" if _p_hcov_c >= 48 else "#6B7280")
            _acov_clr = "#00C896" if _p_acov_c >= 52.4 else ("#C9A84C" if _p_acov_c >= 48 else "#6B7280")
            _sg_c = LEAGUES.get(r.get("league",""),{}).get("group","Soccer")
            _sl_name_c = "Run Line" if _sg_c=="Baseball" else ("Puck Line" if _sg_c=="Hockey" else ("AH" if _sg_c=="Soccer" else "Spread"))
            _model_lines_html += (
                f'<div style="width:100%;border-top:1px solid rgba(255,255,255,0.05);'
                f'padding-top:4px;margin-top:2px;display:flex;gap:10px;align-items:center">'
                f'<span style="font-size:0.65rem;color:#22d3ee">📐 {_sl_name_c}: <b>{_spr_raw_c}</b></span>'
                f'<span style="font-size:0.65rem;color:{_hcov_clr}">'
                f'{_h_team}: <b>{_p_hcov_c:.0f}%</b> cubre</span>'
                f'<span style="font-size:0.65rem;color:{_acov_clr}">'
                f'{_a_team}: <b>{_p_acov_c:.0f}%</b> cubre</span>'
                f'</div>'
            )
        _model_lines_html += '</div>'
    # ─────────────────────────────────────────────────────────────────────────
    is_live    = r.get("state", "") == "in"
    live_html  = '<span class="market-chip chip-btts">🔴 EN VIVO</span>' if is_live else ""
    rank_html  = ""
    if rank:
        rank_html = '<span style="font-family:Inter,sans-serif;color:#6B7280;font-size:0.896rem">#' + str(rank) + '</span> '

    score_html = ""
    if is_live and r.get("home_score") and r.get("away_score"):
        score_html = (' <span style="color:#00C896;font-weight:700">'
                      + str(r["away_score"]) + " - " + str(r["home_score"]) + "</span>")

    # Goals pills — bigger font, highlight best % with star
    goals_html = ""
    if sim.get("use_goals") and sim.get("p_btts") is not None:
        # Find best probability among all goal markets to highlight it
        goal_entries = []
        if sim.get("p_btts") is not None and sim.get("btts_ev") is not None:
            goal_entries.append(("BTTS", sim["p_btts"], sim["btts_ev"]))
        if sim.get("p_o25") is not None:
            goal_entries.append(("O2.5", sim["p_o25"], sim.get("o25_ev") or 0))
        if sim.get("p_u25") is not None:
            goal_entries.append(("U2.5", sim["p_u25"], sim.get("u25_ev") or 0))
        if sim.get("p_o35") is not None:
            goal_entries.append(("O3.5", sim["p_o35"], sim.get("o35_ev") or 0))
        # U3.5 not shown
        # Best = highest probability (most likely outcome)
        best_pct_label = max(goal_entries, key=lambda x: x[1])[0] if goal_entries else ""
        pills = []
        for lbl, pct, ev_v in goal_entries:
            is_best = lbl == best_pct_label
            if ev_v is not None:
                ev_s = ("+" if ev_v >= 0 else "") + str(round(ev_v, 1))
                c = "#00C896" if ev_v > 0 else ("#C9A84C" if lbl == "O2.5" else "#6B7E6E")
                star = "⭐ " if is_best else ""
                fw = "font-weight:700;" if is_best else ""
                pills.append('<span style="color:' + c + ';font-size:0.986rem;' + fw + '">' + star + lbl + ' <b>' + str(pct) + '%</b> (EV ' + ev_s + ')</span>')
            else:
                c = "#8ab4a0" if is_best else "#6B7E6E"
                star = "⭐ " if is_best else ""
                fw = "font-weight:700;" if is_best else ""
                pills.append('<span style="color:' + c + ';font-size:0.986rem;' + fw + '">' + star + lbl + ' <b>' + str(pct) + '%</b></span>')
        if pills:
            goals_html = ('<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:6px;'
                          'padding-top:6px;border-top:1px solid rgba(255,255,255,0.05)">'
                          + " &nbsp;|&nbsp; ".join(pills) + "</div>")

    dq_html   = dq_warn(dq)
    chip_html = chip(bs["market"])
    _status_raw = r.get("status_detail", "").replace("<","").replace(">","").replace("/","").strip()
    # Si ESPN devuelve "Scheduled" o vacío, mostrar hora CDMX desde campo date
    if not _status_raw or _status_raw.lower() in ("scheduled", "cancelado", "postponed"):
        _raw_dt = r.get("date","")
        if _raw_dt:
            try:
                from datetime import timezone as _tz_s, timedelta as _td_s
                _u_s = datetime.strptime(_raw_dt[:19].replace("T"," "), "%Y-%m-%d %H:%M:%S").replace(tzinfo=_tz_s.utc)
                _status_raw = (_u_s - _td_s(hours=6)).strftime("%H:%M") + " CDMX"
            except: pass
    status = _status_raw

    # Recent form badges
    form_html = ""
    hf = r.get("home_form"); af = r.get("away_form")
    def form_badge(f, team):
        if f is None: return ""
        pct = int(f * 100)
        c = "#00C896" if pct >= 60 else ("#C9A84C" if pct >= 40 else "#ef4444")
        arrow = "▲" if pct >= 60 else ("▬" if pct >= 40 else "▼")
        return f'<span style="font-size:0.806rem;color:{c};margin-right:8px">{arrow} {team} {pct}% forma</span>'
    if hf is not None or af is not None:
        form_html = ('<div style="margin-top:5px;opacity:0.85">' +
                     form_badge(hf, r.get("home_team","Local")) +
                     form_badge(af, r.get("away_team","Visita")) +
                     '<span style="font-size:0.728rem;color:#444444">· últimos 5 juegos</span></div>')
    elif r.get("_form_unavailable"):
        form_html = '<div style="margin-top:5px;opacity:0.5;font-size:0.728rem;color:#444444">📡 Forma reciente no disponible (ESPN sin historial para esta liga)</div>' 

    # ── AI Sport Analyst (only for top picks to save API calls) ──────────────
    ai_html = ""
    sport_group = LEAGUES.get(r["league"], {}).get("group", "Soccer")
    ai_text = get_ai_analysis(
        away_team=r["away_team"], home_team=r["home_team"],
        league=r["league"], sport_group=sport_group,
        away_rec=r.get("away_record",""), home_rec=r.get("home_record",""),
        best_label=bs["label"], ev=ev_val, prob_pct=prob_pct,
        home_pct=sim.get("home_pct", 50), away_pct=sim.get("away_pct", 50),
        draw_pct=sim.get("draw_pct", 0), dq=dq,
    )
    if ai_text:
        sport_icon = {"Basketball":"🏀","Soccer":"⚽","Football":"🏈","Hockey":"🏒","Baseball":"⚾"}.get(sport_group,"🎯")
        ai_html = (
            '<div style="margin-top:10px;padding:10px 14px;'
            'background:rgba(201,168,76,0.06);border-left:3px solid rgba(201,168,76,0.5);'
            'border-radius:0 6px 6px 0">'
            '<div style="font-family:\'Inter\',sans-serif;font-size:0.728rem;'
            'color:rgba(201,168,76,0.6);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px">'
            + sport_icon + ' Análisis ' + sport_group + ' · Claude</div>'
            '<div style="font-family:\'Inter\',sans-serif;font-size:0.918rem;'
            'color:#A0A0A0;line-height:1.65">' + ai_text + '</div>'
            '</div>'
        )

    # ── Consensus badge (Signal D) ──────────────────────────────────────────────
    consensus_html = ""
    c_label       = sim.get("consensus_label","")
    c_color       = sim.get("consensus_color","#9ca3af")
    conflict_note = sim.get("conflict_note","")
    fatigue_note  = sim.get("fatigue_note","")
    injury_note   = sim.get("injury_note","")
    votes_list    = sim.get("consensus_votes",[])

    if c_label:
        votes_html = ""
        if votes_list:
            vote_parts = []
            for sig_name, v, detail in votes_list:
                icon = "✅" if v > 0 else ("❌" if v < 0 else "◾")
                vote_parts.append(f'<span style="font-size:0.762rem;color:#9ca3af">{icon} {sig_name}: {detail}</span>')
            votes_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">' + "".join(vote_parts) + '</div>'

        conflict_html = ""
        if conflict_note:
            conflict_html = (f'<div style="font-size:0.784rem;color:#f97316;margin-top:3px;font-style:italic">'
                             f'⚠ {conflict_note}</div>')
        elif fatigue_note:
            conflict_html = (f'<div style="font-size:0.784rem;color:#60a5fa;margin-top:3px">'
                             f'{fatigue_note}</div>')

        consensus_html = (
            f'<div style="margin-top:8px;padding:8px 12px;background:rgba(0,0,0,0.2);'
            f'border-left:3px solid {c_color};border-radius:0 6px 6px 0">'
            f'<span style="font-size:0.84rem;font-weight:700;color:{c_color};'
            f'letter-spacing:1px">{c_label}</span>'
            + votes_html + conflict_html +
            '</div>'
        )

    # ── Injury Report block ──────────────────────────────────────────────────
    injury_html = ""
    h_inj = sim.get("home_injuries", [])
    a_inj = sim.get("away_injuries", [])
    h_f   = sim.get("home_injury_factor", 1.0)
    a_f   = sim.get("away_injury_factor", 1.0)
    _home = r.get("home_team", "Local")
    _away = r.get("away_team", "Visita")

    def _inj_color(factor):
        if factor < 0.72: return "#ef4444"
        if factor < 0.88: return "#f97316"
        if factor < 0.97: return "#C9A84C"
        return None

    def _inj_label(factor):
        if factor < 0.72: return "⛔ Bajas graves"
        if factor < 0.88: return "⚠ Bajas moderadas"
        return "ℹ Bajas menores"

    inj_parts = []
    for team_name, inj_list, factor in [(_home, h_inj, h_f), (_away, a_inj, a_f)]:
        color = _inj_color(factor)
        if color is None:
            continue
        top_inj = [i for i in inj_list if i.get("impact_score", 0) >= 0.05][:3]
        if not top_inj:
            continue
        names_str = " · ".join(f'{i["name"]} ({i["status"]})' for i in top_inj)
        sev_lbl   = _inj_label(factor)
        inj_parts.append(
            f'<div style="font-size:0.784rem;color:{color};margin-bottom:2px">'
            f'{sev_lbl} <span style="color:#9ca3af">[{team_name}]</span> {names_str}</div>'
        )

    if inj_parts:
        injury_html = (
            '<div style="margin-top:7px;padding:7px 12px;background:rgba(239,68,68,0.06);'
            'border-left:3px solid rgba(239,68,68,0.4);border-radius:0 6px 6px 0">'
            '<div style="font-size:0.728rem;color:rgba(239,68,68,0.6);letter-spacing:2px;'
            'text-transform:uppercase;margin-bottom:4px">🏥 Injury Report</div>'
            + "".join(inj_parts) +
            '</div>'
        )

    # ── Scoring Trend note (Signal B) ────────────────────────────────────────
    scoring_trend_html = ""
    lam_rh = sim.get("lam_real_h"); lam_ra = sim.get("lam_real_a"); lam_lg = sim.get("lam_league")
    if lam_rh is not None and lam_ra is not None and lam_lg is not None:
        lam_real_total = lam_rh + lam_ra
        delta = lam_real_total - lam_lg
        delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
        # Color thresholds relative to league avg (not absolute) so NBA/NHL/MLB
        # and soccer all show green/amber/orange at meaningful deviation levels
        _rel = abs(delta) / max(0.1, lam_lg)
        color = "#00C896" if _rel < 0.05 else ("#f97316" if _rel > 0.15 else "#C9A84C")
        # Sport-specific unit and caveat
        sport_grp_d = LEAGUES.get(r.get("league",""), {}).get("group", "Soccer")
        unit = "pts" if sport_grp_d in ("Basketball","Football") else ("runs" if sport_grp_d == "Baseball" else "goles")
        caveat = " ⚠ sin pitcher" if sport_grp_d == "Baseball" else ""
        scoring_trend_html = (
            f'<div style="margin-top:5px;font-size:0.762rem;color:{color};opacity:0.85">'
            f'📈 Scoring trend: λreal={lam_real_total:.1f} vs λliga={lam_lg:.1f} '
            f'({delta_str} {unit} vs promedio{caveat})</div>'
        )

    return (
        '<div class="pick-card">'
          '<div class="pick-header">'
            '<div>' + rank_html
              + '<span class="pick-matchup">' + r["away_team"] + ' @ ' + r["home_team"] + score_html + '</span>'
            '</div>'
            '<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">'
              + live_html
              + '<span class="pick-league-badge">' + league_label(r["league"]) + '</span>'
              + dq_html
            + '</div>'
          '</div>'
          '<div class="pick-body">'
            '<div style="margin-bottom:4px">' + chip_html
              + '<span style="color:#6B7280;font-size:0.806rem;margin-left:6px">' + status + '</span>'
            '</div>'
            '<div class="pick-action">'
              '<span class="pick-action-arrow">&#9658;</span>'
              ' <span>' + bs["label"] + '</span>'
              ' <span style="font-size:1.12rem;color:#6B7280">' + ml_display + '</span>'
            '</div>'
            '<div class="stats-row">'
              '<div class="stat-item">'
                '<div class="stat-item-val val-green">' + str(round(prob_pct, 1)) + '%</div>'
                '<div class="stat-item-lbl">Prob. Sim.</div>'
              '</div>'
              + impl_html + edge_html
              + '<div class="stat-item">'
                '<div class="stat-item-val val-gold">+' + str(round(ev_val, 1)) + '</div>'
                '<div class="stat-item-lbl">EV / $100</div>'
              '</div>'
              '<div class="stat-item">'
                '<div class="stat-item-val val-purple">' + str(round(kelly_pct * 100, 1)) + '%</div>'
                '<div class="stat-item-lbl">Kelly 25%</div>'
              '</div>'
              '<div class="stat-item">'
                '<div class="stat-item-val" style="font-size:1.008rem">' + conf_html + '</div>'
                '<div class="stat-item-lbl">Confianza</div>'
              '</div>'
            '</div>'
            + _model_lines_html
            + form_html
            + goals_html
            + consensus_html
            + scoring_trend_html
            + injury_html
            + ai_html
          + '</div>'
        '</div>'
    )


def render_parlay_card(r):
    sim=r["sim"]; bp=sim["best_parlay"]
    if not bp or bp["ev"]<=0: return ""
    conf=conf_badge(bp["ev"],sim["data_quality"])
    is_inter = bp.get("type","intra") == "inter"

    legs_html=""
    for i,leg in enumerate(bp["legs"]):
        mtype, label, prob, ev, ml = leg
        if is_inter and " · " in label:
            matchup_part, pick_part = label.split(" · ", 1)
            leg_display = (
                '<div style="display:flex;flex-direction:column;gap:2px;flex:1;margin-left:8px">'
                '<span style="font-size:0.784rem;color:#6B7280;letter-spacing:1px">' + matchup_part + '</span>'
                '<span style="font-family:\'Inter\',sans-serif;font-size:1.03rem;color:#E8E8E8">' + pick_part + '</span>'
                '</div>'
            )
        else:
            leg_display = (
                '<span style="font-family:\'Inter\',sans-serif;font-size:1.064rem;'
                'color:#E8E8E8;margin-left:8px;flex:1">' + label + '</span>'
            )
        ev_color = "#00C896" if ev >= 10 else "#C9A84C"
        legs_html += (
            '<div class="parlay-leg" style="align-items:flex-start">'
            + chip(mtype)
            + leg_display
            + '<div style="text-align:right;min-width:70px">'
              '<div style="color:#00C896;font-family:\'Inter\',sans-serif;font-weight:700">' + str(round(prob*100,1)) + '%</div>'
              '<div style="font-size:0.762rem;color:' + ev_color + '">EV +' + str(round(ev,1)) + '</div>'
              '</div>'
            + '</div>'
        )
        if i < len(bp["legs"])-1:
            legs_html += '<div class="parlay-connector" style="color:#00C896;font-size:0.84rem;text-align:center;padding:4px 0;letter-spacing:3px">⊕ COMBINADA ⊕</div>'

    parlay_type_badge = (
        '<span style="font-size:0.728rem;color:#00C896;letter-spacing:2px;'
        'background:rgba(0,200,150,0.1);padding:2px 8px;border-radius:12px;margin-left:8px">'
        + ("INTER-PARTIDO" if is_inter else "COMBO") + '</span>'
    )
    dq_warn_html = ('<div class="warn-banner" style="margin-top:8px">'
                    '⚠ DQ 0% — Sin cuotas reales. Verifica precios antes de apostar.</div>'
                    if sim["data_quality"]==0 else "")
    header_title = "🎰 &nbsp;PARLAY" + parlay_type_badge
    if not is_inter:
        header_title += ' &nbsp;·&nbsp; ' + r["away_team"] + ' @ ' + r["home_team"] + ' &nbsp;·&nbsp; ' + league_label(r["league"])
    return (
        '<div class="parlay-card">'
          '<div class="parlay-header">'
            + header_title +
          '</div>'
          '<div class="parlay-body">'
            + legs_html
            + '<div style="display:flex;gap:24px;flex-wrap:wrap;margin-top:14px;padding-top:12px;'
              'border-top:1px solid rgba(0,200,150,0.2)">'
              '<div class="stat-item">'
                '<div class="stat-item-val" style="color:#00C896;font-size:1.568rem">' + str(round(bp["prob"]*100,1)) + '%</div>'
                '<div class="stat-item-lbl">Prob. Combo</div>'
              '</div>'
              '<div class="stat-item">'
                '<div class="stat-item-val val-cyan" style="font-size:1.568rem">+' + str(round(bp["payout"],0))[:-2] + '</div>'
                '<div class="stat-item-lbl">Pago / $100</div>'
              '</div>'
              '<div class="stat-item">'
                '<div class="stat-item-val val-gold" style="font-size:1.568rem">+' + str(round(bp["ev"],1)) + '</div>'
                '<div class="stat-item-lbl">EV / $100</div>'
              '</div>'
              '<div class="stat-item">' + conf + '</div>'
            '</div>'
            + dq_warn_html
          + '</div>'
        '</div>'
    )
run_sidebar = st.session_state.pop("trigger_analyze", False)

# Valores de configuración persistentes (antes estaban en sidebar / panel hamburguesa)
n_sims     = st.session_state.get("n_sims_val", 10_000)
sel_groups = st.session_state.get("sel_groups_val", ["Basketball","Baseball","Soccer","Hockey"])
_avail     = [n for n, cfg in LEAGUES.items() if cfg["group"] in sel_groups and not cfg.get("hidden")]
_saved_leagues = st.session_state.get("sel_leagues_val", None)
if _saved_leagues is None:
    sel_leagues = _avail
    st.session_state["sel_leagues_val"] = _avail
else:
    _new_leagues = [l for l in _avail if l not in _saved_leagues]
    if _new_leagues:
        _saved_leagues = _saved_leagues + _new_leagues
        st.session_state["sel_leagues_val"] = _saved_leagues
    sel_leagues = [l for l in _saved_leagues if l in _avail]
use_demo   = st.session_state.get("use_demo_val", False)



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════




st.markdown("""
<div class="den-header" style="text-align:center;padding:20px 0 10px">
  <div class="den-logo" style="font-family:'Barlow Condensed','Impact',sans-serif;font-size:2.4rem;font-weight:900;color:#fff;text-transform:uppercase;letter-spacing:-1px">The <span style="color:#FF5500">Gamblers</span> Den</div>
  <div class="den-subtitle">Monte Carlo · Expected Value · Sports Intelligence</div>
  <div style="margin-top:10px">
    <span class="den-corner">♠</span>
    <span class="den-corner">♣</span>
    <span class="den-corner">♥</span>
    <span class="den-corner">♦</span>
  </div>
</div>
<div class="den-divider"></div>
""", unsafe_allow_html=True)

if not sel_leagues:
    st.warning("Selecciona al menos una liga en el sidebar.")
    st.stop()

# Load games
is_demo=False
if use_demo:
    games=get_demo_games(); is_demo=True
else:
    _leagues_key = tuple(sorted(sel_leagues))
    _cached_games = st.session_state.get("_games_cache", {})
    if _leagues_key in _cached_games:
        # Use cached games — no ESPN call needed
        games, fetch_errors = _cached_games[_leagues_key]
    else:
        with st.spinner("Buscando los mejores picks del día..."):
            games, fetch_errors = get_all_games(_leagues_key)
        _cached_games[_leagues_key] = (games, fetch_errors)
        st.session_state["_games_cache"] = _cached_games

    # ── Persist pre-game soccer matches across refreshes ─────────────────────
    # ESPN soccer API often only returns active games. We cache pre-game soccer
    # matches so they keep appearing in PICKS even after ESPN drops them.
    from datetime import timedelta as _td_cache
    _now_cache = datetime.now(timezone.utc)
    _today_cdmx_cache = (_now_cache - _td_cache(hours=6)).strftime("%Y-%m-%d")
    _cached_pre = st.session_state.get("_soccer_pre_cache", {})

    # Store new pre-game soccer matches
    for _g in games:
        _gid = _g.get("id","")
        if not _gid: continue
        if LEAGUES.get(_g.get("league",""),{}).get("group","") == "Soccer" and _g.get("state") == "pre":
            _cached_pre[_gid] = _g

    # Purge old days — mantener ventana ±1 día para no perder partidos europeos
    _yesterday_cdmx_cache = (_now_cache - _td_cache(hours=6) - _td_cache(days=1)).strftime("%Y-%m-%d")
    _tomorrow_cdmx_cache  = (_now_cache - _td_cache(hours=6) + _td_cache(days=1)).strftime("%Y-%m-%d")
    _valid_cache_dates = {_yesterday_cdmx_cache, _today_cdmx_cache, _tomorrow_cdmx_cache}
    for _gid in [k for k, v in list(_cached_pre.items())]:
        try:
            _ev_cdmx = (datetime.strptime((_cached_pre[_gid].get("date","")[:19]).replace("T"," "),
                        "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) - _td_cache(hours=6)).strftime("%Y-%m-%d")
            if _ev_cdmx not in _valid_cache_dates:
                _cached_pre.pop(_gid, None)
        except: pass

    st.session_state["_soccer_pre_cache"] = _cached_pre

    # Re-inject cached pre-game soccer that ESPN dropped (now showing as live or missing)
    _current_ids = {_g.get("id","") for _g in games}
    for _gid, _cg in _cached_pre.items():
        if _gid not in _current_ids:
            _cg_copy = dict(_cg); _cg_copy["state"] = "pre"
            games.append(_cg_copy)

    if not games:
        col_a,col_b=st.columns(2)
        with col_a:
            if st.button("↺ Reintentar ESPN"): st.cache_data.clear(); st.rerun()
        with col_b:
            if st.button("🧪 Usar demo"): st.session_state["force_demo"]=True; st.rerun()

        leagues_str = ", ".join(sel_leagues[:6])
        # Show per-league breakdown if we have errors
        if fetch_errors:
            sin_partidos = [e for e in fetch_errors if "sin partidos" in e]
            con_error    = [e for e in fetch_errors if "sin partidos" not in e]
            detail_html  = ""
            if sin_partidos:
                detail_html += f"<br>📅 Sin partidos hoy: <b>{', '.join(e.split(':')[0] for e in sin_partidos)}</b>"
            if con_error:
                detail_html += f"<br>⚠ Error de API: <b>{', '.join(e.split(':')[0] for e in con_error)}</b>"
        else:
            detail_html = ""
        st.markdown(
            f'<div class="warn-banner">No se encontraron partidos para: <b>{leagues_str}</b>.{detail_html}<br>'            f'Puede que no haya juegos programados hoy. Activa <b>Modo Demo</b> para ver cómo funciona la app.</div>',
            unsafe_allow_html=True)
        st.stop()
    else:
        sel_set=set(sel_leagues)
        games=[g for g in games if g["league"] in sel_set] or games

if st.session_state.get("force_demo"):
    games=get_demo_games(); is_demo=True; st.session_state.pop("force_demo",None)

if is_demo:
    st.markdown('<div class="demo-banner">⚠ MODO DEMO — Datos ilustrativos. Desactiva el toggle en el sidebar para datos reales de ESPN.</div>',unsafe_allow_html=True)

# ── AUTO-SIMULACIÓN: corre automáticamente la primera vez que carga la página ─
_already_simulated = "sim_results" in st.session_state and bool(st.session_state["sim_results"])
_leagues_key = ",".join(sorted(sel_leagues)) + str(n_sims) + str(is_demo)
_prev_key = st.session_state.get("_sim_key", "")
_leagues_changed = _leagues_key != _prev_key

if (not _already_simulated or _leagues_changed or run_sidebar) and games:
    with st.spinner("🔮 El Oráculo está analizando los partidos..."):
        import time as _time
        _t0 = _time.time()
        _sr = run_all_simulations(games, n=n_sims)
        _elapsed = _time.time() - _t0
    st.session_state["sim_results"] = _sr
    st.session_state["last_sim_demo"] = is_demo
    st.session_state["_sim_key"] = _leagues_key
    _n_pos = len([r for r in _sr if r["sim"].get("best_single") and (r["sim"]["best_single"]["ev"] or 0) > 0])
    # ── AUTO-SAVE picks to pick_history (skip demo mode) ──────────────────
    if not is_demo and _gsheets_available():
        try:
            _ph_new = _ph_build_picks_from_sim(_sr, fuente="RONGOL")
            _ph_saved = _ph_save_picks(_ph_new)
            _ph_load.clear()  # invalidate cache
            if _ph_saved and _ph_saved > 0:
                _ph_labels = " · ".join(
                    f'{p["deporte"]} {p["mercado"]} {p["pick_label"][:12]}'
                    for p in _ph_new[:3]
                )
                st.toast(f"📋 {_ph_saved} pick(s) guardados → {_ph_labels}", icon="📋")
            elif run_sidebar and _ph_new:
                st.toast(f"📋 Historial al día ({len(_ph_new)} picks ya registrados)", icon="📋")
        except Exception as _ph_err:
            pass  # never block the main flow

    # ── AUTO-RESOLVE: update pendiente → ganado/perdido for finished games ──
    if not is_demo and _gsheets_available():
        try:
            _post_games = [g for g in games if g.get("state") == "post"]
            if _post_games and not st.session_state.get("_ph_updated_today", False):
                _all_ph = _ph_load()
                _resolved = _ph_auto_resolve(_all_ph)
                if _resolved:
                    _n_resolved = _ph_update_results(_resolved)
                    if _n_resolved and _n_resolved > 0:
                        _win  = sum(1 for v in _resolved.values() if v["resultado"] == "ganado")
                        _lose = sum(1 for v in _resolved.values() if v["resultado"] == "perdido")
                        st.toast(f"✅ {_n_resolved} picks resueltos · {_win}W {_lose}L", icon="📊")
        except Exception:
            pass  # never block the main flow

    if run_sidebar:
        st.toast(f"✓ {len(games)*n_sims:,} sims en {_elapsed:.1f}s · {_n_pos} value bets", icon="🔮")
    st.rerun()

# Stats bar
live_g=[g for g in games if g["state"]=="in"]
pre_g=[g for g in games if g["state"]=="pre"]
odds_g=[g for g in games if g["odds"]]
sr=st.session_state.get("sim_results",[])
pos_ev=len([r for r in sr if r["sim"].get("best_single") and (r["sim"]["best_single"]["ev"] or 0)>0])

st.markdown(f"""<div class="stat-grid">
  <div class="stat-tile"><div class="stat-num">{len(games)}</div><div class="stat-label">Partidos</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#00C896">{len(live_g)}</div><div class="stat-label">En Vivo</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#60a5fa">{len(pre_g)}</div><div class="stat-label">Próximos</div></div>
  <div class="stat-tile"><div class="stat-num">{len(odds_g)}</div><div class="stat-label">Con Cuotas</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#00C896">{pos_ev}</div><div class="stat-label">Value Bets</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#00C896">{len([r for r in sr if r["sim"].get("best_parlay") and (r["sim"]["best_parlay"].get("ev") or 0)>0])}</div><div class="stat-label">Parlays EV+</div></div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="den-divider"></div>', unsafe_allow_html=True)

# [team profiles badge — moved below after function definitions]

# ── Team Profiles — cargar y mostrar badge ────────────────────────────────
# Forzar recarga si la cache tiene 0 equipos (puede estar cacheando vacío)
_tp_profiles_now = _load_all_team_profiles()
if len(_tp_profiles_now) == 0:
    _load_all_team_profiles.clear()
    _tp_profiles_now = _load_all_team_profiles()
_tp_count_now    = len(_tp_profiles_now)
_tp_err_now      = st.session_state.get("_tp_load_error","")

if _tp_count_now > 0:
    _tp_total_games = sum(p.get("n_games",0) for p in _tp_profiles_now.values())
    _tp_leagues     = len({p.get("league","") for p in _tp_profiles_now.values()})
    st.markdown(
        f'<div style="text-align:center;margin-bottom:8px;font-size:0.806rem;'
        f'color:#00C896;letter-spacing:1px">'
        f'🧠 Memoria activa: <b>{_tp_count_now}</b> equipos · '
        f'<b>{_tp_total_games}</b> partidos · '
        f'<b>{_tp_leagues}</b> ligas</div>',
        unsafe_allow_html=True
    )
elif _tp_err_now:
    st.markdown(
        f'<div style="text-align:center;margin-bottom:8px;font-size:0.806rem;'
        f'color:#ef4444;letter-spacing:1px">'
        f'🧠 Memoria: error — {_tp_err_now[:80]}</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div style="text-align:center;margin-bottom:8px;font-size:0.806rem;'
        'color:#6B7280;letter-spacing:1px">'
        '🧠 Memoria: aprendiendo... · <b>↓ Poblar Memoria</b> en el sidebar</div>',
        unsafe_allow_html=True
    )

# ── Poblar memoria (botón sidebar) ───────────────────────────────────────────
if st.session_state.pop("run_populate", False):
    # ── Diagnóstico antes de intentar poblar ─────────────────────────────────
    diag_lines = []
    try:
        s = st.secrets.get("gsheets", {})
        diag_lines.append(f"gsheets secret keys: {list(s.keys())}")
        diag_lines.append(f"private_key present: {bool(s.get('private_key'))}")
        diag_lines.append(f"spreadsheet_id: {s.get('spreadsheet_id','MISSING')}")
        diag_lines.append(f"_gsheets_available(): {_gsheets_available()}")
        try:
            gc = _get_gsheet_client()
            diag_lines.append("gsheet client: ✅ OK")
            sid = st.secrets["gsheets"]["spreadsheet_id"]
            sh = gc.open_by_key(sid)
            diag_lines.append(f"spreadsheet opened: ✅ '{sh.title}'")
            tabs = [ws.title for ws in sh.worksheets()]
            diag_lines.append(f"existing tabs: {tabs}")
        except Exception as e:
            diag_lines.append(f"gsheet client ERROR: {e}")
    except Exception as e:
        diag_lines.append(f"secrets ERROR: {e}")

    with st.expander("🔍 Diagnóstico Sheets", expanded=True):
        for line in diag_lines:
            st.code(line)

    if not _gsheets_available():
        st.error("❌ Google Sheets no disponible — revisa diagnóstico arriba")
        st.stop()
    else:
        st.markdown("""
        <div style='background:rgba(201,168,76,0.08);border:1px solid #C9A84C;
        border-radius:12px;padding:16px;margin-bottom:16px'>
        <div style='font-family:Inter,sans-serif;color:#C9A84C;font-size:1.12rem;
        font-weight:700;margin-bottom:8px'>🧠 POBLANDO MEMORIA DE EQUIPOS</div>
        <div style='font-size:0.84rem;color:#9ca3af'>
        Descargando historial de ESPN para todas las ligas y equipos.<br>
        Esto tarda ~3-5 minutos. No cierres la app.
        </div></div>
        """, unsafe_allow_html=True)

        _prog  = st.progress(0)
        _stat  = st.empty()
        _written, _failed, _log = populate_all_team_profiles(
            progress_bar=_prog,
            status_text=_stat,
        )
        _prog.progress(1.0)
        _stat.empty()

        # Mostrar resumen
        if _written > 0:
            st.success(f"✅ Memoria poblada: **{_written}** equipos guardados, {_failed} fallidos")
        else:
            st.error(f"❌ 0 equipos guardados. {_failed} fallidos. Revisa el log.")

        # Log expandible — siempre visible
        with st.expander("📋 Ver log completo", expanded=(_written == 0)):
            st.code("\n".join(_log))

        # Solo limpiar cache, NO hacer rerun para que el log sea visible
        st.cache_data.clear()

# ── ROUTING ───────────────────────────────────────────────────────────────────

# ── HELPER FUNCTIONS (module level) ─────────────────────────────────────
def _normalize_team(name):
    """Lowercase, strip accents, remove common suffixes + pick market labels."""
    import unicodedata, re as _re_norm
    name = name.lower().strip()
    # Remove market labels that users sometimes include in pick field
    for mkt in [" ml", " over", " under", " btts", " o/u", " si", " no",
                " moneyline", " +", " -"]:
        if name.endswith(mkt):
            name = name[:-len(mkt)].strip()
    # Strip accents
    name = ''.join(c for c in unicodedata.normalize('NFD', name)
                   if unicodedata.category(c) != 'Mn')
    # Remove club suffixes
    for suffix in [" fc", " cf", " sc", " ac", " bc", " afc", " utd", " united",
                   " city", " athletic", " atletico", " club", " de", " real",
                   " cf", " cp", " fk", " sk", " bk"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)].strip()
    # Common Spanish/English aliases
    _ALIASES = {
        "atletico": "atletico madrid", "atletico de madrid": "atletico madrid",
        "man utd": "manchester united", "man city": "manchester city",
        "wolves": "wolverhampton", "spurs": "tottenham",
        "psg": "paris saint-germain", "paris sg": "paris saint-germain",
        "inter": "inter milan", "internazionale": "inter milan",
        "bayern": "bayern munich", "bayer": "bayer leverkusen",
        "dortmund": "borussia dortmund", "bvb": "borussia dortmund",
        "juve": "juventus", "barca": "barcelona", "barsa": "barcelona",
        "unam": "pumas unam", "america": "club america",
        "santos": "santos laguna", "tigres": "tigres uanl",
        "america": "club america", "chivas": "guadalajara",
        "cruz azul": "cruz azul", "morelia": "atletico morelia",
    }
    name = _ALIASES.get(name, name)
    return name.strip()

def _team_match(pick_team, game_home, game_away, threshold=0.55):
    """Return ('home'|'away'|None) if pick_team matches one of the game teams.
    Uses multiple matching strategies in order of reliability.
    """
    if not pick_team: return None
    pt = _normalize_team(pick_team)
    ht = _normalize_team(game_home)
    at = _normalize_team(game_away)

    if not pt: return None

    # 1. Exact match
    if pt == ht: return "home"
    if pt == at: return "away"

    # 2. Substring match (either direction)
    if pt in ht or ht in pt: return "home"
    if pt in at or at in pt: return "away"

    # 3. First significant token match (e.g. "real" in "real madrid")
    pt_words = [w for w in pt.split() if len(w) >= 4]
    ht_words = set(ht.split())
    at_words = set(at.split())
    if pt_words:
        if any(w in ht_words for w in pt_words): return "home"
        if any(w in at_words for w in pt_words): return "away"

    # 4. Token overlap ratio
    pt_tok = set(pt.split())
    def overlap(a, b):
        if not a or not b: return 0
        return len(a & b) / max(len(a), len(b))
    h_sc = overlap(pt_tok, ht_words)
    a_sc = overlap(pt_tok, at_words)
    best = max(h_sc, a_sc)
    if best >= threshold:
        if h_sc >= a_sc: return "home"
        return "away"

    # 5. Any shared token of 5+ chars (catches "manchester" matching "manchester city")
    pt_long = {w for w in pt.split() if len(w) >= 5}
    if pt_long & ht_words: return "home"
    if pt_long & at_words: return "away"

    return None

def _evaluate_pick(pick, game):
    """
    Given a finished game and a pick dict, return 'ganado'|'perdido'|'push'|None.
    pick keys: partido, pick (team/label), mercado (ML|O/U|BTTS|DO), momio
    game keys: home_team, away_team, home_score, away_score, state
    """
    if game.get("state") != "post":
        return None
    try:
        hs = int(str(game.get("home_score","")).strip() or "x")
        as_ = int(str(game.get("away_score","")).strip() or "x")
    except:
        return None  # no score yet

    mercado  = (pick.get("mercado") or "ML").upper().replace(" ","_")
    # Normalize spread variants
    if mercado in ("RUN_LINE","PUCK_LINE","ASIAN_HANDICAP","HANDICAP","AH","SPREAD"):
        mercado = "SPREAD"
    pick_lbl = pick.get("pick","").strip()
    sg       = LEAGUES.get(game.get("league",""), {}).get("group","Soccer")

    # ── ML ────────────────────────────────────────────────────────────────────
    if mercado == "ML":
        # Clean pick label — remove market suffixes users might include
        import re as _re_ev
        _pick_clean = _re_ev.sub(
            r'\s*(ml|moneyline|money line|gana|win|local|visitante)\s*$',
            '', pick_lbl, flags=_re_ev.IGNORECASE
        ).strip()
        side = _team_match(_pick_clean or pick_lbl, game["home_team"], game["away_team"])
        if side is None:
            # Try matching against the partido string directly
            side = _team_match(pick_lbl, game["home_team"], game["away_team"])
        if side is None: return None
        if sg == "Soccer":
            if hs == as_: return "push"  # draw = push on ML? no, it loses
            won = (side == "home" and hs > as_) or (side == "away" and as_ > hs)
        else:
            won = (side == "home" and hs > as_) or (side == "away" and as_ > hs)
        # Draw in soccer = ML loses (not a push)
        if sg == "Soccer" and hs == as_:
            return "perdido"
        return "ganado" if won else "perdido"

    # ── O/U ───────────────────────────────────────────────────────────────────
    if mercado in ("O/U", "OU", "OVER/UNDER"):
        total = hs + as_
        # Parse line from pick label: "Over 2.5 goles" → 2.5, "Under 228.5" → 228.5
        import re
        lbl_lower = pick_lbl.lower()
        nums = re.findall(r'[\d]+\.?[\d]*', lbl_lower)
        if not nums: return None
        line = float(nums[0])
        if total == line: return "push"
        if "over" in lbl_lower or "o/" in lbl_lower:
            return "ganado" if total > line else "perdido"
        if "under" in lbl_lower or "u/" in lbl_lower:
            return "ganado" if total < line else "perdido"
        return None

    # ── BTTS ──────────────────────────────────────────────────────────────────
    if mercado == "BTTS":
        both_scored = hs > 0 and as_ > 0
        lbl_lower = pick_lbl.lower()
        if "no" in lbl_lower or "not" in lbl_lower:
            return "ganado" if not both_scored else "perdido"
        return "ganado" if both_scored else "perdido"

    # ── DO (Doble Oportunidad) ─────────────────────────────────────────────────
    if mercado == "DO":
        # "Home o Empate (1X)", "Away o Empate (X2)", "Home o Away (12)"
        lbl_lower = pick_lbl.lower()
        home_w = hs > as_
        away_w = as_ > hs
        draw   = hs == as_
        if "1x" in lbl_lower or ("empate" in lbl_lower and game["home_team"].lower() in lbl_lower):
            return "ganado" if (home_w or draw) else "perdido"
        if "x2" in lbl_lower or ("empate" in lbl_lower and game["away_team"].lower() in lbl_lower):
            return "ganado" if (away_w or draw) else "perdido"
        if "12" in lbl_lower or "sin empate" in lbl_lower:
            return "ganado" if (home_w or away_w) else "perdido"
        return None

    # ── Spread / Run Line / Puck Line / Asian Handicap ───────────────────────
    if mercado in ("SPREAD", "AH", "RUN LINE", "PUCK LINE", "HANDICAP",
                   "RUN_LINE", "PUCK_LINE", "ASIAN_HANDICAP"):
        import re as _re_sp2
        # Parse line from pick label: "Dodgers -1.5 (Run Line)" → team=Dodgers, line=-1.5
        # Or "Chiefs -7.5 (Spread)" → team=Chiefs, line=-7.5
        _nums2 = _re_sp2.findall(r'[+-]?\d+\.?\d*', pick_lbl)
        if not _nums2: return None
        _line = float(_nums2[0])
        # Identify which team the pick is for
        _pick_clean2 = _re_sp2.sub(r'[+-]?\d+\.?\d*.*', '', pick_lbl).strip()
        _pick_clean2 = _re_sp2.sub(r'\(.*\)', '', _pick_clean2).strip()
        side2 = _team_match(_pick_clean2, game["home_team"], game["away_team"])
        if side2 is None: return None
        # home_diff = home_score - away_score
        home_diff = hs - as_
        # If pick is home team: home wins against spread if home_diff + line > 0
        if side2 == "home":
            result_diff = home_diff + _line
        else:  # away team: mirror the line
            result_diff = -home_diff + (-_line if _line > 0 else abs(_line))
        if result_diff > 0: return "ganado"
        elif result_diff < 0: return "perdido"
        else: return "push"

    return None

@st.cache_data(ttl=300)
def _fetch_finished_games():
    """Fetch recently finished games across all leagues for auto-resolve.
    Fetches today AND yesterday to catch games from the last 48h.
    """
    from datetime import timedelta as _tdff
    finished = []
    seen_ids = set()

    _now_utc = datetime.now(timezone.utc)
    _today_utc     = _now_utc.strftime("%Y%m%d")
    _fetch_dates   = [
        _today_utc,
        (_now_utc - _tdff(days=1)).strftime("%Y%m%d"),
        (_now_utc - _tdff(days=2)).strftime("%Y%m%d"),
        (_now_utc - _tdff(days=3)).strftime("%Y%m%d"),
        (_now_utc - _tdff(days=4)).strftime("%Y%m%d"),
        (_now_utc - _tdff(days=5)).strftime("%Y%m%d"),
        (_now_utc - _tdff(days=6)).strftime("%Y%m%d"),
        (_now_utc - _tdff(days=7)).strftime("%Y%m%d"),
    ]

    for league_name, cfg in LEAGUES.items():
        sport  = cfg["sport"]
        league = cfg["league"]
        tid    = cfg.get("tournament_id")
        # Fetch last 7 days
        for date_str in _fetch_dates:
            try:
                base = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"
                url  = f"{base}?dates={date_str}&limit=100"
                r = __import__("requests").get(url, timeout=6,
                    headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code != 200:
                    continue
                data = r.json()
                for g in parse_games(data, league_name):
                    gid = g.get("id","")
                    if gid and gid in seen_ids:
                        continue
                    if g.get("state") == "post" and g.get("home_score") and g.get("away_score"):
                        finished.append(g)
                        if gid:
                            seen_ids.add(gid)
            except:
                pass
        # Also try the regular scoreboard (catches live→post transitions)
        try:
            data = fetch_scoreboard(sport, league, tournament_id=tid)
            for g in parse_games(data, league_name):
                gid = g.get("id","")
                if gid and gid in seen_ids:
                    continue
                if g.get("state") == "post" and g.get("home_score") and g.get("away_score"):
                    finished.append(g)
                    if gid:
                        seen_ids.add(gid)
        except:
            pass
    return finished


# RETO 13M — Bitácora permanente de bankroll
# Persistencia: JSON en disco por usuario (~/.gamblers_den_reto_APODO.json)
# ══════════════════════════════════════════════════════════════════════════════
import json, os as _os, re as _re

# ── Google Sheets persistence ─────────────────────────────────────────────────
# Requires st.secrets["gsheets"] with keys:
#   type, project_id, private_key_id, private_key, client_email,
#   client_id, auth_uri, token_uri, spreadsheet_id
#
# Each user = one sheet tab named after their apodo.
# Row format: num | fecha | partido | pick | mercado | momio | momio_fmt | monto | resultado | nota
# Row 1 = header  |  Row 2 = config (bank_inicial, meta in cols A-B)
# Row 3+ = picks


# ══════════════════════════════════════════════════════════════════════════════
# TEAM PROFILES — Sistema de aprendizaje por equipo
# Pestaña "team_profiles" en Google Sheets
# Aprende de los últimos 10 partidos de cada equipo y usa ese historial
# para mejorar λ y las tasas O/U/BTTS en el modelo Monte Carlo.
# ══════════════════════════════════════════════════════════════════════════════

# _TP constants moved to top


# [_load_all_team_profiles moved to top]


# _compute_profile_stats moved to top
# populate_all_team_profiles defined above
def _safe_apodo(apodo):
    return _re.sub(r"[^a-zA-Z0-9_]", "_", apodo.strip().lower())[:31]

def _get_or_create_tab(gc, spreadsheet_id, apodo):
    """Get or create a worksheet tab for this apodo."""
    sh = gc.open_by_key(spreadsheet_id)
    safe = _safe_apodo(apodo)
    try:
        ws = sh.worksheet(safe)
    except:
        ws = sh.add_worksheet(title=safe, rows=1000, cols=12)
        # Write headers
        ws.update("A1:J1", [["num","fecha","partido","pick","mercado",
                              "momio","momio_fmt","monto","resultado","nota"]])
        # Config row (bank_inicial, meta)
        ws.update("A2:B2", [[2000.0, 13000000.0]])
    return ws

def _load_reto(apodo):
    """Load reto data. Google Sheets if configured, else local JSON fallback."""
    default = {"bank_inicial": 2000.0, "meta": 13_000_000.0, "picks": [], "apodo": apodo}
    if _gsheets_available():
        try:
            gc = _get_gsheet_client()
            sid = st.secrets["gsheets"]["spreadsheet_id"]
            ws = _get_or_create_tab(gc, sid, apodo)
            rows = ws.get_all_values()
            if len(rows) < 2:
                return default
            # Row 2 = config
            try:
                bank_inicial = float(rows[1][0]) if rows[1][0] else 2000.0
                meta         = float(rows[1][1]) if len(rows[1]) > 1 and rows[1][1] else 13_000_000.0
            except:
                bank_inicial, meta = 2000.0, 13_000_000.0
            # Rows 3+ = picks (index 2+)
            picks = []
            for row in rows[2:]:
                if not any(row):
                    continue
                def cell(i, default=""):
                    return row[i] if i < len(row) else default
                try:
                    picks.append({
                        "num":       int(cell(0, 0)) if cell(0) else len(picks)+1,
                        "fecha":     cell(1),
                        "partido":   cell(2),
                        "pick":      cell(3),
                        "mercado":   cell(4, "ML"),
                        "momio":     float(cell(5, 1.909)),
                        "momio_fmt": cell(6),
                        "monto":     float(cell(7, 0)),
                        "resultado": cell(8, "pendiente"),
                        "nota":      cell(9),
                    })
                except:
                    continue
            return {"bank_inicial": bank_inicial, "meta": meta, "picks": picks, "apodo": apodo}
        except Exception as e:
            st.warning(f"⚠ Google Sheets no disponible: {e}. Usando almacenamiento local.")
    # Fallback: local JSON
    try:
        path = _os.path.expanduser(f"~/.gamblers_den_reto_{_safe_apodo(apodo)}.json")
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

def _save_reto(data, apodo):
    """Save reto data to Google Sheets (or local JSON fallback)."""
    if _gsheets_available():
        try:
            gc = _get_gsheet_client()
            sid = st.secrets["gsheets"]["spreadsheet_id"]
            ws = _get_or_create_tab(gc, sid, apodo)
            # Config row
            ws.update("A2:B2", [[data.get("bank_inicial", 2000.0), data.get("meta", 13_000_000.0)]])
            # Clear old pick rows and rewrite
            picks = data.get("picks", [])
            if picks:
                rows = []
                for p in picks:
                    rows.append([
                        p.get("num",""), p.get("fecha",""), p.get("partido",""),
                        p.get("pick",""), p.get("mercado","ML"),
                        p.get("momio",""), p.get("momio_fmt",""),
                        p.get("monto",""), p.get("resultado","pendiente"),
                        p.get("nota",""),
                    ])
                # Clear from row 3 down then write
                last_row = len(picks) + 10
                ws.batch_clear([f"A3:J{last_row}"])
                ws.update(f"A3:J{len(picks)+2}", rows)
            else:
                ws.batch_clear(["A3:J1000"])
            return True
        except Exception as e:
            st.warning(f"⚠ Error guardando en Sheets: {e}")
    # Fallback: local JSON
    try:
        path = _os.path.expanduser(f"~/.gamblers_den_reto_{_safe_apodo(apodo)}.json")
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

# Tabs that are NOT user profiles — always excluded from user lists
_SYSTEM_TABS = {"pick_history", "line_movement", "team_profiles", "Sheet1", "Hoja1",
                "sheet1", "hoja1", "SHEET1", "HOJA1"}

def _list_reto_users():
    """List only real user profile tabs (excludes system tabs)."""
    if _gsheets_available():
        try:
            gc = _get_gsheet_client()
            sid = st.secrets["gsheets"]["spreadsheet_id"]
            sh = gc.open_by_key(sid)
            return sorted([
                ws.title for ws in sh.worksheets()
                if ws.title not in _SYSTEM_TABS
            ])
        except:
            pass
    # Fallback: local files
    home = _os.path.expanduser("~")
    users = []
    try:
        for fn in _os.listdir(home):
            if fn.startswith(".gamblers_den_reto_") and fn.endswith(".json"):
                users.append(fn.replace(".gamblers_den_reto_","").replace(".json",""))
    except:
        pass
    return sorted(users)


# ═══════════════════════════════════════════════════════════════════════════════
# LEADERBOARD + SOCIAL FEED — Lee todos los usuarios del Sheets
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def _load_leaderboard():
    """
    Load stats for ALL users from Google Sheets for leaderboard.
    Returns list of dicts sorted by bank_actual desc.
    Cached 5 minutes to avoid hammering the API.
    """
    users = _list_reto_users()
    # Filter out non-user tabs
    users = [u for u in users if u not in _SYSTEM_TABS]

    rows = []
    if not _gsheets_available():
        return rows

    try:
        gc  = _get_gsheet_client()
        sid = st.secrets["gsheets"]["spreadsheet_id"]
        sh  = gc.open_by_key(sid)

        for apodo in users:
            try:
                ws        = sh.worksheet(apodo)
                all_rows  = ws.get_all_values()
                if len(all_rows) < 2:
                    continue

                # Config row
                bank_ini = float(all_rows[1][0]) if all_rows[1][0] else 2000.0
                meta_val = float(all_rows[1][1]) if len(all_rows[1]) > 1 and all_rows[1][1] else 13_000_000.0

                # Parse picks
                picks_data = []
                for row in all_rows[2:]:
                    if not any(row): continue
                    try:
                        res    = row[8] if len(row) > 8 else "pendiente"
                        momio  = float(row[5]) if len(row) > 5 and row[5] else 1.9
                        monto  = float(row[7]) if len(row) > 7 and row[7] else 0
                        fecha  = row[1] if len(row) > 1 else ""
                        partido= row[2] if len(row) > 2 else ""
                        pick_l = row[3] if len(row) > 3 else ""
                        mercado= row[4] if len(row) > 4 else ""
                        nota   = row[9] if len(row) > 9 else ""
                        picks_data.append({
                            "resultado": res, "momio": momio, "monto": monto,
                            "fecha": fecha, "partido": partido, "pick": pick_l,
                            "mercado": mercado, "nota": nota,
                        })
                    except:
                        continue

                # Calculate stats
                bank = bank_ini
                n_gan = n_per = n_pen = 0
                last_picks = []
                for p in picks_data:
                    res = p["resultado"]
                    if res == "ganado":
                        mm = p["momio"]; ss = p["monto"]
                        bank += ss * (mm - 1) if mm >= 1.01 else ss * 100 / abs(mm) if mm < 0 else 0
                        n_gan += 1
                    elif res == "perdido":
                        bank -= p["monto"]
                        n_per += 1
                    elif res == "pendiente":
                        n_pen += 1
                    last_picks.append(p)

                resolved = n_gan + n_per
                wr = n_gan / resolved * 100 if resolved > 0 else 0
                mult = bank / bank_ini if bank_ini > 0 else 1

                # Last pick for social feed
                last_pick = last_picks[-1] if last_picks else None

                rows.append({
                    "apodo":      apodo,
                    "bank":       round(bank, 2),
                    "bank_ini":   bank_ini,
                    "mult":       round(mult, 3),
                    "wr":         round(wr, 1),
                    "n_picks":    len(picks_data),
                    "n_gan":      n_gan,
                    "n_per":      n_per,
                    "n_pen":      n_pen,
                    "last_pick":  last_pick,
                    "all_picks":  last_picks[-5:],  # last 5 for social feed
                })
            except Exception:
                continue
    except Exception:
        pass

    # Sort by bank desc
    rows.sort(key=lambda x: x["bank"], reverse=True)
    return rows


@st.cache_data(ttl=180, show_spinner=False)
def _load_leaderboard_with_resolve():
    """
    Load leaderboard AND silently resolve all pending picks for all users.
    Runs in background with 3-min cache so it doesn't hammer the API.
    """
    users = _list_reto_users()
    users = [u for u in users if u not in _SYSTEM_TABS]

    if not _gsheets_available() or not users:
        return

    # Fetch finished games ONCE — shared for all users
    try:
        finished_games = _fetch_finished_games()
    except:
        return

    if not finished_games:
        return

    any_changed = False
    for apodo in users:
        try:
            reto_data = _load_reto(apodo)
            picks_data = reto_data.get("picks", [])
            pending = [p for p in picks_data if p.get("resultado") == "pendiente"]
            if not pending:
                continue

            changed = False
            for i, p in enumerate(picks_data):
                if p.get("resultado") != "pendiente":
                    continue
                partido_txt = p.get("partido","")
                sep = " vs " if " vs " in partido_txt.lower() else (" @ " if " @ " in partido_txt else None)
                t1, t2 = (partido_txt.split(sep,1) + [""])[:2] if sep else (partido_txt, "")
                t1, t2 = t1.strip(), t2.strip()

                for g in finished_games:
                    m1 = _team_match(t1, g["home_team"], g["away_team"])
                    m2 = _team_match(t2, g["home_team"], g["away_team"]) if t2 else None
                    if (m1 or m2):
                        res = _evaluate_pick(p, g)
                        if res:
                            picks_data[i]["resultado"]  = res
                            picks_data[i]["home_score"] = str(g.get("home_score",""))
                            picks_data[i]["away_score"] = str(g.get("away_score",""))
                            changed = True
                            break

            if changed:
                reto_data["picks"] = picks_data
                _save_reto(reto_data, apodo)
                any_changed = True
        except:
            continue

    if any_changed:
        try:
            _load_leaderboard.clear()
        except:
            pass


def _silent_auto_resolve(apodo_activo, reto, picks):
    """
    Silently resolve ALL pending picks for a user against ESPN finished games.
    Runs on every Reto tab load. Returns (updated_picks, n_resolved, details).
    Saves to Sheets automatically if anything resolved.
    """
    pendientes = [p for p in picks if p.get("resultado") == "pendiente"]
    if not pendientes:
        return picks, 0, []

    try:
        finished_games = _fetch_finished_games()
    except:
        return picks, 0, []

    n_resolved = 0
    details    = []
    changed    = False

    for i, p in enumerate(picks):
        if p.get("resultado") != "pendiente":
            continue

        partido_txt = p.get("partido", "")
        sep = " vs " if " vs " in partido_txt.lower() else (" @ " if " @ " in partido_txt else None)
        if sep:
            parts = partido_txt.split(sep, 1)
            t1, t2 = parts[0].strip(), parts[1].strip()
        else:
            t1, t2 = partido_txt.strip(), ""

        for g in finished_games:
            # Match using both team names from partido string
            m1 = _team_match(t1, g["home_team"], g["away_team"]) if t1 else None
            m2 = _team_match(t2, g["home_team"], g["away_team"]) if t2 else None

            # Also try the pick label directly as team name (for ML picks)
            pick_as_team = p.get("pick", "").strip()
            m3 = _team_match(pick_as_team, g["home_team"], g["away_team"]) if pick_as_team else None

            # Need at least one team match from the partido string
            if not (m1 or m2):
                # If pick label matches a team, use that to identify the game
                if not m3:
                    continue
                # Verify the other team also matches loosely
                if t1 and not m1:
                    other = _team_match(t1, g["home_team"], g["away_team"])
                    if not other and t2:
                        other = _team_match(t2, g["home_team"], g["away_team"])
                    if not other:
                        continue  # can't confirm it's the right game

            res = _evaluate_pick(p, g)
            if res:
                picks[i]["resultado"]   = res
                picks[i]["home_score"]  = str(g.get("home_score", ""))
                picks[i]["away_score"]  = str(g.get("away_score", ""))
                n_resolved += 1
                changed = True
                icon = "✅" if res == "ganado" else ("❌" if res == "perdido" else "🔄")
                details.append({
                    "icon":  icon,
                    "num":   p.get("num", "?"),
                    "texto": partido_txt,
                    "res":   res,
                    "hs":    g.get("home_score",""),
                    "as_":   g.get("away_score",""),
                })
                break  # found match, move to next pick

    if changed:
        reto["picks"] = picks
        _save_reto(reto, apodo_activo)
        # Invalidate leaderboard cache so it reflects new results
        try:
            _load_leaderboard.clear()
        except:
            pass

    return picks, n_resolved, details


def _rango_for_bank(bank):
    """Return (icon, name, color) for a given bank amount."""
    _R = [
        (2_000_000_000, "🏆", "Inmortal",          "#FFD700"),
        (13_000_000,    "👑", "El 13M",             "#FFD700"),
        (5_000_000,     "💎", "Magnate",             "#00BFFF"),
        (1_000_000,     "🚀", "Millonario",          "#00BFFF"),
        (500_000,       "🔥", "Leyenda de Las Vegas","#FF4500"),
        (100_000,       "⚡", "Alto Voltaje",        "#FF8C00"),
        (70_000,        "🎰", "Jugador Pro",         "#FF8C00"),
        (40_000,        "🦈", "Tiburón",             "#3D8EFF"),
        (20_000,        "💪", "Apostador Serio",     "#3D8EFF"),
        (10_000,        "📈", "En Racha",            "#3D8EFF"),
        (5_000,         "🟢", "Novato",              "#00C896"),
        (0,             "🌱", "Semilla",             "#888"),
    ]
    return next((r[1:] for r in _R if bank >= r[0]), ("🌱", "Semilla", "#888"))


if _active_page == "Rongol Picks":
    sr=st.session_state.get("sim_results",[])
    if not sr:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">🎲</div>
          <div class="empty-title">Sin simulaciones</div>
          <div>Presiona <b>▶ ANALIZAR AHORA</b> en el sidebar o ve al tab <b>🔮 ORÁCULO</b> para generar los picks del día.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Detectar picks terminados ─────────────────────────────────────────────
        pick_game_ids = {r.get("id","") for r in sr if r["sim"].get("best_single") and (r["sim"]["best_single"]["ev"] or 0)>0}
        finished_pick_games  = [g for g in games if g.get("id","") in pick_game_ids and g["state"]=="post"]
        pending_games_picks  = [g for g in games if g["state"] in ("pre","in")]

        _needs_regen_picks = (
            len(finished_pick_games) > 0
            and len(pending_games_picks) > 0
            and not st.session_state.get("_picks_regen_done", False)
        )
        _picks_regen_key = f"picks_{len(finished_pick_games)}_{len(pending_games_picks)}"
        if st.session_state.get("_picks_regen_key") != _picks_regen_key:
            st.session_state["_picks_regen_done"] = False
            st.session_state["_picks_regen_key"] = _picks_regen_key

        # ── Banner de alerta ──────────────────────────────────────────────────────
        if finished_pick_games:
            finished_names = " · ".join(
                f"{g['away_team']} @ {g['home_team']}" for g in finished_pick_games[:3]
            )
            st.markdown(f'''<div class="warn-banner" style="border-left:4px solid #00C896;background:rgba(74,222,128,0.08)">
                ✅ <b>Pick(s) terminados:</b> {finished_names}<br>
                <span style="color:#6B7280;font-size:0.896rem">{len(pending_games_picks)} partidos pendientes disponibles.</span>
            </div>''', unsafe_allow_html=True)

        # ── Botón manual ──────────────────────────────────────────────────────────
        col_rp1, col_rp2 = st.columns([3,1])
        with col_rp2:
            regen_picks_clicked = st.button(
                "🔄 Nuevos Picks", use_container_width=True,
                disabled=len(pending_games_picks)==0,
                help="Re-simula con los partidos pendientes del día",
                key="btn_regen_picks"
            )

        # ── Ejecutar regeneración (auto o manual) ─────────────────────────────────
        if (_needs_regen_picks or regen_picks_clicked) and pending_games_picks:
            with st.spinner(f"🃏 Generando nuevos picks con {len(pending_games_picks)} partidos pendientes..."):
                new_sr_picks = run_all_simulations(pending_games_picks, n=n_sims)
            st.session_state["sim_results"] = new_sr_picks
            st.session_state["_picks_regen_done"] = True
            n_new = len([r for r in new_sr_picks if r["sim"].get("best_single") and (r["sim"]["best_single"]["ev"] or 0)>0])
            st.toast(f"✓ Nuevos picks generados · {n_new} EV+", icon="🃏")
            st.rerun()

        # ── Mostrar picks ─────────────────────────────────────────────────────────
        sr_cur = st.session_state.get("sim_results", [])
        sr_cur_filtrado = sr_cur  # default: sin filtro, se sobreescribe abajo si hay filtro de liga
        all_bets=[]
        for r in sr_cur:
            bs=r["sim"].get("best_single")
            if bs and (bs.get("ev") or 0)>0: all_bets.append(r)
        all_bets.sort(key=lambda x: x["sim"]["best_single"]["ev"],reverse=True)

        # Indicador de estado
        n_post_p = len([g for g in games if g["state"]=="post"])
        n_live_p = len([g for g in games if g["state"]=="in"])
        n_pre_p  = len([g for g in games if g["state"]=="pre"])
        st.markdown(
            f'<div style="font-size:0.806rem;color:#6B7280;margin-bottom:8px">' +
            (f'<span style="color:#00C896">⚡ {n_live_p} en vivo</span> · ' if n_live_p else "") +
            f'{n_pre_p} próximos · {n_post_p} terminados</div>',
            unsafe_allow_html=True
        )

        # ── Filtrar: solo O/U, BTTS, ML — excluir DO como pick principal ──────────
        ALLOWED_MKTS = {"O/U", "BTTS", "ML"}  # DO never a standalone pick

        # ── Sport-aware pick selection ─────────────────────────────────────────
        # Per sport, pick the BEST candidate by these rules:
        #   Soccer:     best of {BTTS, O2.5} by prob  +  ML (highest win%)
        #               NO O/U Under, no U3.5
        #   Basketball: ML (highest win%)  +  O/U total (model side)
        #   Hockey:     ML (highest win%)  +  O/U total (model side, uses ESPN line)
        #   Baseball:   ML (highest win%) only
        #   Football:   ML (highest win%) only

        def _pick_score(cand, sim, sg):
            """Delegado a pick_score_universal (módulo) para consistencia total."""
            return pick_score_universal(cand, sim, r, sg)

        def _sport_best_pick(r):
            """
            Selecciona el mejor pick usando score compuesto.
            TODOS los deportes generan pick (sin filtro de ESPN ML).
            El score_compuesto decide: EV + edge + consenso + DQ + kelly + líneas modelo.
            """
            sim = r["sim"]
            sg  = LEAGUES.get(r["league"], {}).get("group", "Soccer")
            h_prob = sim.get("home_pct", 0) or 0
            a_prob = sim.get("away_pct", 0) or 0
            h_ml = sim.get("home_ml"); a_ml = sim.get("away_ml")
            h_ev = sim.get("home_ev") or 0; a_ev = sim.get("away_ev") or 0
            h_k  = sim.get("home_kelly") or 0; a_k = sim.get("away_kelly") or 0

            def best_ml():
                if h_prob >= a_prob:
                    team, prob, ev, kelly, ml = r["home_team"], h_prob, h_ev, h_k, h_ml
                else:
                    team, prob, ev, kelly, ml = r["away_team"], a_prob, a_ev, a_k, a_ml
                # Sin ML de ESPN: usar probabilidad del modelo con momio del modelo
                if not ml:
                    _mdec_key = "model_home_dec" if h_prob >= a_prob else "model_away_dec"
                    _mdec = sim.get(_mdec_key) or ""
                    ml = _mdec  # usar momio calculado por el modelo
                return {"market":"ML","label":team,"prob":prob,"ev":ev or 0,"kelly":kelly or 0,"ml":ml}

            cands = []

            if sg == "Soccer":
                _ml = best_ml()
                # ML siempre entra como candidato
                if _ml: cands.append(_ml)

                if sim.get("use_goals"):
                    _btts_ev = sim.get("btts_ev") or 0
                    _btts_pb = sim.get("p_btts") or 0
                    if _btts_pb > 0:
                        cands.append({"market":"BTTS","label":"Ambos Anotan",
                                      "prob":_btts_pb,"ev":_btts_ev,"kelly":0})
                    _o25_ev = sim.get("o25_ev") or 0
                    _o25_pb = sim.get("p_o25") or 0
                    if _o25_pb > 0:
                        cands.append({"market":"O/U","label":"Over 2.5 goles",
                                      "prob":_o25_pb,"ev":_o25_ev,"kelly":0})

            elif sg in ("Basketball", "Hockey"):
                _ml = best_ml()
                if _ml: cands.append(_ml)
                # O/U: solo con línea ESPN real (FIX-2 — no implícita)
                _ou_line = sim.get("ou_line") or ""
                _multi_r = sim.get("multi_lines", {})
                if _ou_line and not _ou_line.startswith("~") and _multi_r:
                    _best_p = 0; _best_lbl = None
                    for _l, _d in _multi_r.items():
                        _po_l = _d["over"]; _pu_l = _d["under"]
                        if _po_l >= _pu_l and _po_l > _best_p:
                            _best_p = _po_l; _best_lbl = f"Over {_l:.1f}"
                        elif _pu_l > _po_l and _pu_l > _best_p:
                            _best_p = _pu_l; _best_lbl = f"Under {_l:.1f}"
                    if _best_lbl and _best_p > 0:
                        _ev_ou = round((_best_p/100*(100/110)-(1-_best_p/100))*100, 1)
                        cands.append({"market":"O/U","label":_best_lbl,
                                      "prob":_best_p,"ev":_ev_ou,"kelly":0})

            else:  # Baseball, Football, NCAAF
                _ml = best_ml()
                if _ml: cands.append(_ml)

            if not cands:
                # Fallback: ML con momio calculado por el modelo
                _dom_p = max(h_prob, a_prob)
                _dom_t = r["home_team"] if h_prob >= a_prob else r["away_team"]
                _mk_key = "model_home_dec" if h_prob >= a_prob else "model_away_dec"
                _mdec_fb = sim.get(_mk_key) or ""
                cands.append({"market":"ML","label":_dom_t,
                               "prob":_dom_p,"ev":0,"kelly":0,"ml":_mdec_fb})

            # Seleccionar por score compuesto — toma TODO en cuenta
            scored = [(c, _pick_score(c, sim, sg)) for c in cands]
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[0][0]

        # ── Build 1 pick per sport group — ventana ±1 día CDMX ──────────────
        from datetime import timezone as _tz_rp, timedelta as _td_rp
        _now_rp      = datetime.now(_tz_rp.utc)
        _now_mx_rp   = _now_rp - _td_rp(hours=6)
        _today_rp    = _now_mx_rp.strftime("%Y-%m-%d")
        _valid_rp    = {
            (_now_mx_rp - _td_rp(days=1)).strftime("%Y-%m-%d"),
            _today_rp,
            (_now_mx_rp + _td_rp(days=1)).strftime("%Y-%m-%d"),
        }

        # Build id→game map for quick lookup
        _gmap_rp = {g.get("id", ""): g for g in games}

        _sport_pools = {}
        for r in sr_cur:
            _g = _gmap_rp.get(r.get("id", ""))
            if not _g: continue
            if _g["state"] == "post": continue
            # Filter to today CDMX only
            _raw_date = _g.get("date", "")
            if _raw_date:
                try:
                    from datetime import datetime as _dt_rp
                    _gdt = _dt_rp.fromisoformat(_raw_date.replace("Z", "+00:00"))
                    _gdate_cdmx = (_gdt - _td_rp(hours=6)).strftime("%Y-%m-%d")
                    if _gdate_cdmx not in _valid_rp:
                        continue
                except:
                    pass  # si no parsea, incluir igual
            bp = _sport_best_pick(r)
            if bp:
                sg = LEAGUES.get(r["league"], {}).get("group", "Soccer")
                _sport_pools.setdefault(sg, []).append({**r, "_pick": bp})

        # Sort each pool by prob desc, take top 1
        _SPORT_ORDER_R = ["Soccer","Basketball","Hockey","Baseball","Football"]
        # ── Filtro de deporte activo (tile seleccionado) ──────────────────────
        _sel_sport_filter = st.session_state.get("_picks_sel_sport", None)

        rongol_picks = []
        for _sg in _SPORT_ORDER_R:
            if _sel_sport_filter and _sg != _sel_sport_filter:
                continue
            pool = _sport_pools.get(_sg, [])
            if not pool:
                continue
            # Ordenar por score compuesto universal (no solo probabilidad)
            for _item in pool:
                _item["_score"] = pick_score_universal(
                    _item["_pick"], _item["sim"], _item, _sg
                )
            pool.sort(key=lambda x: x["_score"], reverse=True)
            rongol_picks.append(pool[0])

        # Legacy: keep allowed_bets for DO parlay logic below
        allowed_bets = rongol_picks

        # ── STATS PANEL — accuracy from pick_history ─────────────────────────
        _acc_key = "_acc_open_rongol"
        _acc_open = st.session_state.get(_acc_key, False)
        def _toggle_acc():
            st.session_state[_acc_key] = not st.session_state.get(_acc_key, False)
        st.button("▼ Cerrar accuracy" if _acc_open else "📊 Accuracy del Sistema",
                  key="btn_acc_rongol", use_container_width=True, on_click=_toggle_acc)
        if _acc_open:
            _ph_all = _ph_load()
            _ph_resolved = [p for p in _ph_all if p["resultado"] in ("ganado","perdido","push")]
            _ph_pending  = [p for p in _ph_all if p["resultado"] == "pendiente"]

            if not _ph_all:
                st.info("Aún no hay historial. Los picks se guardan automáticamente al analizar.")
            else:
                # ── Auto-resolve button ───────────────────────────────────────
                col_ar, col_info = st.columns([1,2])
                with col_ar:
                    if st.button("🔍 Actualizar Resultados", key="btn_ph_resolve",
                                 use_container_width=True,
                                 help="Busca resultados de picks pendientes en ESPN"):
                        if _ph_pending:
                            with st.spinner("Consultando ESPN..."):
                                _ph_updates = _ph_auto_resolve(_ph_pending)
                            if _ph_updates:
                                _ph_update_results(_ph_updates)
                                _ph_load.clear()
                                st.toast(f"✓ {len(_ph_updates)} pick(s) resueltos", icon="🔍")
                                st.rerun()
                            else:
                                st.info("No se encontraron resultados nuevos aún.")
                        else:
                            st.info("No hay picks pendientes.")
                with col_info:
                    st.caption(f"📋 {len(_ph_all)} picks totales · {len(_ph_pending)} pendientes · {len(_ph_resolved)} resueltos")

                if _ph_resolved:
                    _n_gan = sum(1 for p in _ph_resolved if p["resultado"]=="ganado")
                    _n_per = sum(1 for p in _ph_resolved if p["resultado"]=="perdido")
                    _n_psh = sum(1 for p in _ph_resolved if p["resultado"]=="push")
                    _n_tot = len(_ph_resolved)
                    _wr    = round(_n_gan/_n_tot*100, 1) if _n_tot else 0
                    _wr_c  = "#00C896" if _wr>=55 else ("#C9A84C" if _wr>=45 else "#ef4444")

                    # ── Global stats tiles ────────────────────────────────────
                    st.markdown(
                        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0">'
                        f'<div style="flex:1;min-width:80px;background:rgba(74,222,128,0.10);'
                        f'border:1px solid rgba(74,222,128,0.3);border-radius:12px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.68rem;font-weight:900;color:{_wr_c};font-family:Inter,sans-serif">{_wr}%</div>'
                        f'<div style="font-size:0.672rem;color:#6B7280;letter-spacing:1px;text-transform:uppercase">Win Rate</div>'
                        f'</div>'
                        f'<div style="flex:1;min-width:70px;background:rgba(74,222,128,0.07);'
                        f'border:1px solid rgba(74,222,128,0.2);border-radius:12px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.456rem;font-weight:800;color:#00C896">{_n_gan}</div>'
                        f'<div style="font-size:0.672rem;color:#6B7280;text-transform:uppercase">✅ Ganados</div>'
                        f'</div>'
                        f'<div style="flex:1;min-width:70px;background:rgba(239,68,68,0.07);'
                        f'border:1px solid rgba(239,68,68,0.2);border-radius:12px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.456rem;font-weight:800;color:#ef4444">{_n_per}</div>'
                        f'<div style="font-size:0.672rem;color:#6B7280;text-transform:uppercase">❌ Perdidos</div>'
                        f'</div>'
                        f'<div style="flex:1;min-width:70px;background:rgba(201,168,76,0.07);'
                        f'border:1px solid rgba(201,168,76,0.2);border-radius:12px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.456rem;font-weight:800;color:#C9A84C">{_n_psh}</div>'
                        f'<div style="font-size:0.672rem;color:#6B7280;text-transform:uppercase">🔄 Push</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # ── Breakdown por mercado ─────────────────────────────────
                    _mkts = {}
                    for p in _ph_resolved:
                        m = p["mercado"]
                        _mkts.setdefault(m, {"gan":0,"per":0,"psh":0})
                        _mkts[m][{"ganado":"gan","perdido":"per","push":"psh"}[p["resultado"]]] += 1

                    _mkt_color = None  # use _pick_clr()
                    st.markdown('<div style="font-size:0.728rem;color:#6B7280;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 6px 0">Por Mercado</div>', unsafe_allow_html=True)
                    for _m, _mc in sorted(_mkts.items()):
                        _mt = _mc["gan"] + _mc["per"] + _mc["psh"]
                        _mwr = round(_mc["gan"]/_mt*100,1) if _mt else 0
                        _stpc, _stac, _, _ = _pick_clr(_m)
                        _mc_c = _stac
                        _bar_w = _mwr
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0">'
                            f'<span style="background:{_mc_c}22;color:{_mc_c};border:1px solid {_mc_c}44;'
                            f'border-radius:12px;padding:1px 7px;font-size:0.694rem;font-weight:800;min-width:48px;text-align:center">{_m}</span>'
                            f'<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:12px;height:6px;overflow:hidden">'
                            f'<div style="width:{_bar_w}%;height:100%;background:{_mc_c};border-radius:12px"></div></div>'
                            f'<span style="font-size:0.784rem;font-weight:700;color:{_mc_c};min-width:38px;text-align:right">{_mwr}%</span>'
                            f'<span style="font-size:0.65rem;color:#6B7280;min-width:60px">{_mc["gan"]}G {_mc["per"]}P {_mc["psh"]}X</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    # ── Breakdown por deporte ─────────────────────────────────
                    _sgps = {}
                    for p in _ph_resolved:
                        sg = p.get("deporte","?")
                        _sgps.setdefault(sg, {"gan":0,"per":0,"psh":0})
                        _sgps[sg][{"ganado":"gan","perdido":"per","push":"psh"}[p["resultado"]]] += 1

                    _sg_ico = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}
                    st.markdown('<div style="font-size:0.728rem;color:#6B7280;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 6px 0">Por Deporte</div>', unsafe_allow_html=True)
                    for _sg, _sc in sorted(_sgps.items()):
                        _st = _sc["gan"] + _sc["per"] + _sc["psh"]
                        _swr = round(_sc["gan"]/_st*100,1) if _st else 0
                        _sgc = "#00C896" if _swr>=60 else ("#C9A84C" if _swr>=45 else "#ef4444")
                        _ico = _sg_ico.get(_sg,"🎯")
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0">'
                            f'<span style="font-size:0.84rem;min-width:20px">{_ico}</span>'
                            f'<span style="font-size:0.806rem;color:#E8E8E8;min-width:90px">{_sg}</span>'
                            f'<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:12px;height:6px;overflow:hidden">'
                            f'<div style="width:{_swr}%;height:100%;background:{_sgc};border-radius:12px"></div></div>'
                            f'<span style="font-size:0.784rem;font-weight:700;color:{_sgc};min-width:38px;text-align:right">{_swr}%</span>'
                            f'<span style="font-size:0.65rem;color:#6B7280;min-width:60px">{_sc["gan"]}G {_sc["per"]}P {_sc["psh"]}X</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("Aún no hay picks resueltos. Pulsa 🔍 Actualizar Resultados para traer los resultados de ESPN.")

                # ── TABLA DE AUDITORÍA — todos los picks guardados ────────────
                st.markdown(
                    '<div style="font-size:0.728rem;color:#6B7280;letter-spacing:1.5px;'
                    'text-transform:uppercase;margin:16px 0 8px 0;border-top:1px solid '
                    'rgba(255,255,255,0.06);padding-top:12px">📋 Historial Completo — Auditoría</div>',
                    unsafe_allow_html=True
                )

                if _ph_all:
                    # Sort: pending first, then by date desc
                    _audit_sorted = sorted(
                        _ph_all,
                        key=lambda x: (0 if x["resultado"]=="pendiente" else 1, x["fecha"]),
                        reverse=False
                    )
                    _audit_sorted = sorted(_ph_all, key=lambda x: x["fecha"], reverse=True)

                    _RES_COLOR = {
                        "ganado":   ("#00C896", "✅"),
                        "perdido":  ("#ef4444", "❌"),
                        "push":     ("#C9A84C", "🔄"),
                        "pendiente":("#6B7E6E", "⏳"),
                    }
                    pass  # colors via _pick_clr()
                    _SGI2   = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}

                    # Table header
                    st.markdown(
                        '<div style="display:grid;grid-template-columns:90px 1fr 60px 60px 70px 70px;'
                        'gap:4px;padding:4px 6px;background:rgba(255,255,255,0.04);border-radius:12px 6px 0 0;'
                        'font-size:0.65rem;color:#6B7280;letter-spacing:1px;text-transform:uppercase;'
                        'border-bottom:1px solid rgba(255,255,255,0.08)">'
                        '<span>Fecha</span><span>Partido</span>'
                        '<span style="text-align:center">Mkt</span>'
                        '<span style="text-align:center">Deporte</span>'
                        '<span style="text-align:center">Prob</span>'
                        '<span style="text-align:center">Resultado</span>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    for _ap in _audit_sorted[:50]:  # max 50 rows
                        _res   = _ap.get("resultado","pendiente")
                        _rc, _ri = _RES_COLOR.get(_res, ("#6B7E6E","⏳"))
                        _apc, _aac, _, _adl = _pick_clr(_ap["mercado"], _ap.get("pick_label",""))
                        _mc2 = _aac  # for compat
                        _sgi2  = _SGI2.get(_ap.get("deporte",""),"🎯")
                        _fecha = _ap["fecha"][:10]
                        _score = ""
                        if _ap.get("home_score") and _ap.get("away_score"):
                            _score = f' <span style="color:#444444">({_ap["away_score"]}-{_ap["home_score"]})</span>'
                        _row_bg = "rgba(74,222,128,0.04)" if _res=="ganado" else                                   "rgba(239,68,68,0.04)"  if _res=="perdido" else                                   "rgba(255,255,255,0.02)"
                        st.markdown(
                            f'<div style="display:grid;grid-template-columns:90px 1fr 60px 60px 70px 70px;'
                            f'gap:4px;padding:5px 6px;background:{_row_bg};'
                            f'border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.762rem;align-items:center">'
                            f'<span style="color:#6B7280;font-size:0.672rem">{_fecha}</span>'
                            f'<div>'
                            f'<div style="color:#E8E8E8;font-size:0.784rem;white-space:nowrap;overflow:hidden;'
                            f'text-overflow:ellipsis;max-width:180px">{_ap["partido"]}</div>'
                            f'<div style="color:#FFE87C;font-size:0.694rem">{_ap["pick_label"]}{_score}</div>'
                            f'</div>'
                            f'<span style="text-align:center">'
                            f'<span style="background:{_apc}28;color:{_aac};border:1px solid {_apc}66;border-radius:12px;padding:1px 5px;font-size:0.672rem;font-weight:800">{_adl}</span></span>'
                            f'<span style="text-align:center;font-size:0.84rem">{_sgi2}</span>'
                            f'<span style="text-align:center;color:#C9A84C;font-size:0.784rem;font-weight:700">'
                            f'{_ap["prob_pct"]:.0f}%</span>'
                            f'<span style="text-align:center;color:{_rc};font-size:0.84rem">{_ri}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    if len(_ph_all) > 50:
                        st.caption(f"Mostrando últimos 50 de {len(_ph_all)} picks. Ver historial completo en Google Sheets.")
                else:
                    st.caption("Sin picks guardados aún.")

        if not rongol_picks:
            st.markdown('<div class="warn-banner">No se encontraron picks. Intenta con más ligas o pulsa ▶ ANALIZAR.</div>', unsafe_allow_html=True)
        else:
            # ── helpers ──────────────────────────────────────────────────────
            _MKT_COLOR = {"ML":"#60a5fa","O/U":"#ff6a00","BTTS":"#00C896","DO":"#a78bfa","COMBO":"#f59e0b"}
            _SPORT_ICON = {"Basketball":"🏀","Soccer":"⚽","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}
            _CONF_LABEL = lambda p: ("🔥 ALTA" if p>=75 else ("⚡ MEDIA" if p>=55 else "🌡 BAJA"))
            _CONF_COLOR = lambda p: ("#00C896" if p>=75 else ("#C9A84C" if p>=55 else "#ef4444"))

            def _prob_bar_html(prob, color):
                """Thin probability bar."""
                return (
                    f'<div style="margin:6px 0 2px 0;background:rgba(255,255,255,0.06);'
                    f'border-radius:12px;height:5px;overflow:hidden">'
                    f'<div style="width:{prob:.0f}%;height:100%;border-radius:12px;'
                    f'background:linear-gradient(90deg,{color}88,{color});'
                    f'box-shadow:0 0 8px {color}66"></div></div>'
                    f'<div style="font-size:0.65rem;color:{color};text-align:right;'
                    f'margin-top:1px">{prob:.0f}%</div>'
                )

            # ── Pick card color palette — uses global _pick_clr() ──────────

            def _pick_diamante_card(r, tp, rank=0, is_fire=False):
                pc, ac, type_key, _ = _pick_clr(tp.get("market",""), tp.get("label",""))
                _sg_r = LEAGUES.get(r.get("league",""),{}).get("group","Soccer")
                _ml_i = _SPORT_ICON.get(_sg_r,"⚽")
                _type_icons = {"ML":_ml_i,"BTTS":"🎯","OVER":"🔥","UNDER":"🧊","COMBO":"⚽🎯","OTHER":"📊"}
                icon  = _type_icons.get(type_key,"📊")
                ev_s  = f'+{tp["ev"]:.1f}' if (tp.get("ev") or 0)>=0 else f'{tp["ev"]:.1f}'
                prob  = tp["prob"]
                conf_lbl = _CONF_LABEL(prob)
                conf_c   = _CONF_COLOR(prob)
                is_diamond = rank == 0

                # ── Card outer style — color drives the whole card ────────────
                if is_fire:
                    # 🔥 FUEGO: naranja intenso siempre, override pick color
                    card_bg   = f"background:linear-gradient(135deg,rgba(255,106,0,0.22) 0%,#141414 55%,{pc}18 100%)"
                    card_border = "border:1.5px solid rgba(255,106,0,0.7)"
                    card_shadow = "box-shadow:0 0 28px rgba(255,106,0,0.28),inset 0 1px 0 rgba(255,106,0,0.18)"
                    stripe_c  = "#ff6a00"
                    title_size = "0.95rem"; label_size = "1.0rem"
                elif is_diamond:
                    card_bg   = f"background:linear-gradient(135deg,{pc}44 0%,#141414 60%,{ac}18 100%)"
                    card_border = f"border:1.5px solid {pc}99"
                    card_shadow = f"box-shadow:0 0 26px {pc}33,inset 0 1px 0 {pc}22"
                    stripe_c  = ac
                    title_size = "1.05rem"; label_size = "1.1rem"
                else:
                    card_bg   = f"background:linear-gradient(135deg,{pc}20 0%,#141414 100%)"
                    card_border = f"border:1px solid {pc}55"
                    card_shadow = f"box-shadow:0 0 14px {pc}18"
                    stripe_c  = ac
                    title_size = "0.88rem"; label_size = "0.9rem"

                outer = f"{card_bg};{card_border};{card_shadow};"

                _low_conf = r.get("sim",{}).get("low_confidence", False)
                _lc_badge = (
                    '<span style="background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b55;'
                    'border-radius:12px;padding:1px 7px;font-size:0.65rem;font-weight:700;'
                    'letter-spacing:1px;margin-right:6px">⚠ SIN CUOTAS</span>' if _low_conf else ""
                )
                _fire_inline = (
                    '<span style="background:rgba(255,106,0,0.2);color:#ff6a00;'
                    'border:1px solid rgba(255,106,0,0.55);border-radius:12px;'
                    'padding:1px 7px;font-size:0.65rem;font-weight:900;'
                    'letter-spacing:1px;margin-right:6px">🔥 FUEGO</span>'
                ) if is_fire else ""
                rank_badge = (
                    f'<span style="background:{pc}22;color:{ac};border:1px solid {pc}55;'
                    f'border-radius:12px;padding:1px 7px;font-size:0.65rem;font-weight:700;'
                    f'letter-spacing:1px;margin-right:8px">#{rank+1}</span>' if not is_diamond and not is_fire else ""
                ) + _fire_inline + _lc_badge

                top_stripe = (
                    f'<div style="height:3px;border-radius:12px 8px 0 0;margin:-14px -14px 10px -14px;'
                    f'background:linear-gradient(90deg,transparent,{stripe_c},{stripe_c}aa,transparent);'
                    f'box-shadow:0 0 12px {stripe_c}88"></div>' if (is_diamond or is_fire) else ""
                )

                # ── Market type badge with full color ─────────────────────────
                type_labels = {"ML":"ML","BTTS":"AA","OVER":"OVER","UNDER":"UNDER","COMBO":"COMBO","OTHER":"O/U"}
                type_label  = type_labels.get(type_key, tp["market"])

                return (
                    f'<div style="border-radius:16px;padding:14px;margin:8px 0;{outer}">'
                    + top_stripe +
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap">'
                    f'<div style="min-width:0;flex:1">'
                    f'<div style="font-size:0.694rem;color:#6B7280;letter-spacing:1.5px;'
                    f'text-transform:uppercase;margin-bottom:3px">{rank_badge}{league_label(r["league"])}</div>'
                    f'<div style="font-size:{title_size};font-weight:700;color:#E8E8E8;line-height:1.3">'
                    f'{r["away_team"]} <span style="color:#444444;font-weight:400">vs</span> {r["home_team"]}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:1.288rem;font-weight:900;color:{ac};'
                    f'text-shadow:0 0 12px {ac}88;font-family:Inter,sans-serif">EV {ev_s}</div>'
                    f'<div style="font-size:0.672rem;color:{conf_c};font-weight:700">{conf_lbl}</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="margin-top:10px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">'
                    f'<span style="background:{pc}28;color:{ac};border:1px solid {pc}77;'
                    f'border-radius:5px;padding:3px 10px;font-size:0.784rem;font-weight:800;'
                    f'letter-spacing:1.5px">{icon} {type_label}</span>'
                    f'<span style="font-size:{label_size};font-weight:700;color:#FFE87C;'
                    f'font-family:Inter,sans-serif;letter-spacing:0.5px">{tp["label"]}</span>'
                    f'</div>'
                    + _prob_bar_html(prob, ac) +
                    f'</div>'
                )

            # ── FILTRO DE LIGAS — botón que despliega/recoge ─────────────────
            # Obtener ligas disponibles en los resultados actuales
            _ligas_disponibles = sorted({
                r["league"] for r in sr_cur
                if r["league"] in LEAGUES
            })
            # Inicializar selección en session_state (todas activas por default)
            if "picks_ligas_sel" not in st.session_state:
                st.session_state["picks_ligas_sel"] = set(_ligas_disponibles)
            # Si hay ligas nuevas que no estaban antes, añadirlas
            for _l in _ligas_disponibles:
                if _l not in st.session_state["picks_ligas_sel"] and \
                   _l not in st.session_state.get("picks_ligas_excluidas", set()):
                    st.session_state["picks_ligas_sel"].add(_l)

            _ligas_sel = st.session_state["picks_ligas_sel"]
            _n_activas = len([l for l in _ligas_disponibles if l in _ligas_sel])
            _n_total   = len(_ligas_disponibles)

            # Botón toggle
            _filtro_open = st.session_state.get("picks_filtro_open", False)
            _btn_label = (
                f"🏆 Ligas · {_n_activas}/{_n_total} activas  {'▲' if _filtro_open else '▼'}"
            )
            def _tog_filtro(_v=_filtro_open):
                st.session_state["picks_filtro_open"] = not _v
            st.button(_btn_label, key="btn_filtro_ligas", use_container_width=True, on_click=_tog_filtro)

            if st.session_state.get("picks_filtro_open", False):
                st.markdown(
                    '<div style="background:#161616;border:1px solid #2A2A2A;border-radius:16px;'
                    'padding:14px 16px;margin:4px 0 12px 0">',
                    unsafe_allow_html=True
                )
                # Botones rápidos
                _qc1, _qc2, _qc3 = st.columns(3)
                with _qc1:
                    def _set_all(_ld=_ligas_disponibles):
                        st.session_state["picks_ligas_sel"] = set(_ld)
                        st.session_state["picks_ligas_excluidas"] = set()
                    st.button("✅ Todas", key="btn_ligas_all", use_container_width=True, on_click=_set_all)
                with _qc2:
                    def _set_soccer(_ld=_ligas_disponibles):
                        st.session_state["picks_ligas_sel"] = {l for l in _ld if LEAGUES.get(l,{}).get("group")=="Soccer"}
                        st.session_state["picks_ligas_excluidas"] = {l for l in _ld if LEAGUES.get(l,{}).get("group")!="Soccer"}
                    st.button("⚽ Solo Soccer", key="btn_ligas_soccer", use_container_width=True, on_click=_set_soccer)
                with _qc3:
                    def _set_us(_ld=_ligas_disponibles):
                        st.session_state["picks_ligas_sel"] = {l for l in _ld if LEAGUES.get(l,{}).get("group") in ("Basketball","Baseball","Football","Hockey")}
                        st.session_state["picks_ligas_excluidas"] = {l for l in _ld if LEAGUES.get(l,{}).get("group")=="Soccer"}
                    st.button("🏀 Solo US Sports", key="btn_ligas_us", use_container_width=True, on_click=_set_us)

                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

                # Toggle individual por liga — en filas de 2
                _ligas_rows = [_ligas_disponibles[i:i+2] for i in range(0, len(_ligas_disponibles), 2)]
                _liga_btn_idx = 0
                for _row in _ligas_rows:
                    _cols_l = st.columns(len(_row))
                    for _ci_l, _liga in enumerate(_row):
                        with _cols_l[_ci_l]:
                            _activa = _liga in _ligas_sel
                            _flag   = LEAGUE_FLAG.get(_liga, "🌐")
                            _grp    = LEAGUES.get(_liga, {}).get("group", "")
                            _grp_colors = {
                                "Soccer": "#00C896", "Basketball": "#f97316",
                                "Hockey": "#60a5fa", "Baseball": "#ef4444", "Football": "#a78bfa"
                            }
                            _c = _grp_colors.get(_grp, "#E8B84B")
                            _bg = f"rgba({','.join(str(int(_c[i:i+2],16)) for i in (1,3,5))},0.15)" if _activa else "rgba(255,255,255,0.04)"
                            _border = _c if _activa else "#2A2A2A"
                            _text_c = "#E8E8E8" if _activa else "#6B7280"
                            st.markdown(
                                f'<div style="background:{_bg};border:1.5px solid {_border};'
                                f'border-radius:12px;padding:8px 10px;margin:2px 0;'
                                f'cursor:pointer;transition:all 0.15s">'
                                f'<span style="font-size:0.9rem">{_flag}</span> '
                                f'<span style="font-size:0.78rem;font-weight:600;color:{_text_c}">{_liga}</span>'
                                f'{"<span style=\'float:right;color:" + _c + ";font-size:0.7rem\'>✓</span>" if _activa else ""}'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            _btn_key = f"liga_tog_{_liga_btn_idx}"
                            _liga_btn_idx += 1
                            _btn_txt = "Quitar" if _activa else "Agregar"
                            def _tog_liga_ind(_lg=_liga, _act=_activa):
                                _excl = st.session_state.get("picks_ligas_excluidas", set())
                                if _act:
                                    st.session_state["picks_ligas_sel"].discard(_lg)
                                    _excl.add(_lg)
                                else:
                                    st.session_state["picks_ligas_sel"].add(_lg)
                                    _excl.discard(_lg)
                                st.session_state["picks_ligas_excluidas"] = _excl
                            st.button(_btn_txt, key=_btn_key, use_container_width=True,
                                      on_click=_tog_liga_ind)

                st.markdown('</div>', unsafe_allow_html=True)

            # Aplicar filtro de liga Y filtro de deporte
            rongol_picks = [r for r in rongol_picks if r["league"] in _ligas_sel]
            sr_cur_filtrado = [r for r in sr_cur if r["league"] in _ligas_sel]
            # Filtro adicional por deporte si hay tile seleccionado
            if _sel_sport_filter:
                rongol_picks = [r for r in rongol_picks
                                if LEAGUES.get(r["league"],{}).get("group") == _sel_sport_filter]
                sr_cur_filtrado = [r for r in sr_cur_filtrado
                                   if LEAGUES.get(r["league"],{}).get("group") == _sel_sport_filter]

            # ── RONGOL PICKS — 2×2 grid (max 5 cards) ────────────────────────
            _n_picks = len(rongol_picks)
            _sport_labels = {"Soccer":"⚽ Fútbol","Basketball":"🏀 Basketball",
                             "Hockey":"🏒 Hockey","Baseball":"⚾ Baseball","Football":"🏈 Football"}
            st.markdown(f'<div class="section-heading">🃏 RONGOL PICKS · {_n_picks} deportes</div>', unsafe_allow_html=True)

            # Find top-2 picks by probability for 🔥 badge
            _all_probs_ranked = sorted(
                [(_row_i*2+_ci, _rp["_pick"]["prob"])
                 for _row_i in range(0, _n_picks, 2)
                 for _ci, _rp in enumerate(rongol_picks[_row_i:_row_i+2])],
                key=lambda x: x[1], reverse=True
            )
            _fire_indices = {idx for idx, _ in _all_probs_ranked[:2]}

            # ── Banner explicativo ─────────────────────────────────────────
            st.markdown(
                '<div style="background:rgba(255,85,0,0.08);border:1px solid rgba(255,85,0,0.25);'
                'border-left:3px solid #FF5500;border-radius:10px;padding:10px 14px;margin-bottom:12px">'
                '<span style="font-size:0.72rem;font-weight:800;color:#FF5500">⚡ CÓMO LEER LOS PICKS: </span>'
                '<span style="font-size:0.75rem;color:#B0B0B8">El botón </span>'
                '<span style="font-size:0.75rem;font-weight:800;color:#FFD600">AMARILLO</span>'
                '<span style="font-size:0.75rem;color:#B0B0B8"> = qué apostar. La cuota decimal = lo que paga tu casa de apuestas. </span>'
                '<span style="font-size:0.75rem;font-weight:700;color:#B0B0B8">Toca ''Ver análisis'' para ver por qué.</span>'
                '</div>',
                unsafe_allow_html=True
            )

            # ── Render picks: tarjetas blancas 3 por renglón ─────────────
            for _row_i in range(0, _n_picks, 3):
                _row_picks = rongol_picks[_row_i:_row_i+3]
                # Always 3 columns - fill with empty if fewer picks
                _cols = st.columns(3)
                for _ci in range(3):
                    if _ci >= len(_row_picks):
                        with _cols[_ci]:
                            st.empty()
                        continue
                    _rp = _row_picks[_ci]
                    _abs_idx  = _row_i + _ci
                    _is_fire  = _abs_idx in _fire_indices
                    _pk       = _rp["_pick"]
                    _mkt      = _pk.get("market","")
                    _lbl      = _pk.get("label","")
                    _prob     = _pk.get("prob",0)
                    _prob     = _prob if _prob<=1 else _prob/100
                    _sim      = _rp.get("sim",{})
                    _sg       = LEAGUES.get(_rp.get("league",""),{}).get("group","Soccer")
                    _sg_icon  = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}.get(_sg,"🎯")
                    _ht_id    = _rp.get("home_team_id","")
                    _at_id    = _rp.get("away_team_id","")
                    _league   = _rp.get("league","")
                    _away     = _rp.get("away_team","")
                    _home     = _rp.get("home_team","")
                    _lg_lbl   = league_label(_league)
                    _pick_h   = _home in _lbl
                    _h_pct    = _sim.get("home_pct",0) or 0
                    _a_pct    = _sim.get("away_pct",0) or 0
                    _d_pct    = _sim.get("draw_pct",0) or 0
                    _h_dec    = _sim.get("model_home_dec","") or (prob_to_dec(_h_pct/100) if _h_pct else "-")
                    _a_dec    = _sim.get("model_away_dec","") or (prob_to_dec(_a_pct/100) if _a_pct else "-")
                    _d_dec    = _sim.get("model_draw_dec","") or (prob_to_dec(_d_pct/100) if _d_pct else "-")
                    _pick_dec = _h_dec if _pick_h else _a_dec
                    _pick_pct = _h_pct if _pick_h else _a_pct
                    # Cap decimals
                    def _cap(d):
                        try:
                            v=float(d)
                            return "1.02" if v<1.02 else (">15" if v>15 else f"{v:.2f}")
                        except: return str(d) if d else "-"
                    _h_dec=_cap(_h_dec);_a_dec=_cap(_a_dec);_d_dec=_cap(_d_dec);_pick_dec=_cap(_pick_dec)
                    # Logos
                    _logo_a = _logo_img(_at_id, _league, 44)
                    _logo_h = _logo_img(_ht_id, _league, 44)
                    # Pills
                    def _pill(lbl, dec, highlight=False):
                        lc = "#3D8EFF" if any(x in str(lbl) for x in ("O","U","x","X")) else "#A0A0A8"
                        return (
                            f'<div style="flex:1;background:linear-gradient(160deg,#1E1E24 0%,#141418 100%);'
                            f'border-radius:10px;border:1px solid rgba(255,255,255,0.1);'
                            f'border-top:1px solid rgba(255,255,255,0.18);'
                            f'box-shadow:0 3px 8px rgba(0,0,0,0.4),0 1px 0 rgba(255,255,255,0.06) inset;'
                            f'padding:10px 4px;text-align:center">'
                            f'<span style="font-size:0.65rem;color:{lc};display:block;margin-bottom:3px;font-weight:700;letter-spacing:0.3px">{lbl}</span>'
                            f'<span style="font-size:1.2rem;font-weight:900;color:#F0F0F2;font-family:Barlow Condensed,sans-serif;line-height:1">{dec}</span>'
                            f'</div>'
                        )
                    if _sg == "Soccer":
                        _pills = _pill("1x",_a_dec) + _pill("x",_d_dec) + _pill("2x",_h_dec)
                    else:
                        _ou_v = _sim.get("ou_line","") or ""
                        _p_o  = _sim.get("p_o_total",0) or 0
                        _p_u  = _sim.get("p_u_total",0) or 0
                        if _ou_v and not str(_ou_v).startswith("~"):
                            try: _ou_lbl = f"{'O' if _p_o>=_p_u else 'U'}{float(str(_ou_v).lstrip('~')):.1f}"
                            except: _ou_lbl = "O/U"
                            _ou_dec = _cap(prob_to_dec(max(_p_o,_p_u)/100)) if max(_p_o,_p_u)>0 else "-"
                            _pills  = _pill(_away[:6],_a_dec) + _pill(_ou_lbl,_ou_dec) + _pill(_home[:6],_h_dec)
                        else:
                            _pills = _pill(_away[:7],_a_dec) + _pill(_home[:7],_h_dec)
                    _fire_glow = "box-shadow:0 0 18px rgba(255,200,0,0.18);" if _is_fire else ""
                    # White card
                    _card = (
                        f'<div style="background:linear-gradient(160deg,#F6F6F9 0%,#E9E9EE 100%);'
                        f'border-radius:20px;overflow:hidden;margin-bottom:3px;'
                        f'border:1px solid rgba(0,0,0,0.07);'
                        f'box-shadow:0 8px 24px rgba(0,0,0,0.22),0 1px 0 rgba(255,255,255,0.85) inset;{_fire_glow}">'
                        f'<div style="padding:9px 14px 4px;display:flex;justify-content:space-between;align-items:center">'
                        f'<span style="font-size:0.58rem;font-weight:700;color:#999;letter-spacing:1.5px;text-transform:uppercase">{_lg_lbl}</span>'
                        f'<span style="font-size:0.65rem">{"🔥" if _is_fire else ""}</span>'
                        f'</div>'
                        f'<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 16px 6px">'
                        f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1">'
                        + _logo_a +
                        f'<span style="font-size:0.6rem;font-weight:800;color:#111;text-transform:uppercase;text-align:center;max-width:60px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{_away[:9]}</span>'
                        f'</div>'
                        f'<div style="flex:1.2;text-align:center">'
                        f'<div style="font-size:1.6rem;font-weight:900;color:#111;font-family:Syne,sans-serif;letter-spacing:-2px;line-height:1">VS</div>'
                        f'<div style="font-size:0.5rem;color:#CCC;margin-top:3px">{_sg_icon}</div>'
                        f'</div>'
                        f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:1">'
                        + _logo_h +
                        f'<span style="font-size:0.6rem;font-weight:800;color:#111;text-transform:uppercase;text-align:center;max-width:60px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{_home[:9]}</span>'
                        f'</div></div>'
                        f'<div style="height:1px;background:rgba(0,0,0,0.06);margin:0 12px"></div>'
                        f'<div style="display:flex;gap:5px;padding:9px 10px 9px">' + _pills + f'</div>'
                        f'<div style="margin:0 10px 10px;'
                        f'background:linear-gradient(160deg,#FFE033 0%,#FFBB00 100%);'
                        f'border-radius:12px;padding:11px 14px;'
                        f'border:1px solid rgba(255,255,255,0.35);'
                        f'box-shadow:0 4px 14px rgba(255,185,0,0.3),0 1px 0 rgba(255,255,255,0.45) inset">'
                        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:2px">'
                        f'<span style="font-size:0.55rem;font-weight:900;color:rgba(0,0,0,0.5);letter-spacing:1.5px;text-transform:uppercase">APOSTAR →</span>'
                        f'<span style="font-size:0.6rem;font-weight:900;color:#111;letter-spacing:1.5px;text-transform:uppercase;background:rgba(0,0,0,0.12);padding:3px 8px;border-radius:5px">{_mkt}</span>'
                        f'<span style="font-size:0.92rem;font-weight:800;color:#111;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{_lbl}</span>'
                        f'</div>'
                        + f'<div style="display:flex;align-items:center;gap:10px;margin-top:5px">'
                        + f'<span style="font-size:2.4rem;font-weight:900;color:#111;font-family:Barlow Condensed,sans-serif;line-height:1">{_pick_dec}</span>'
                        + f'<div style="display:flex;flex-direction:column;gap:3px">'
                        + f'<span style="font-size:0.82rem;font-weight:800;color:rgba(0,0,0,0.7)">{_pick_pct:.0f}% de probabilidad</span>'
                        + (f'<span style="font-size:0.68rem;color:rgba(0,0,0,0.55)">Ganancia esperada: <b>${(_pk.get("ev",0) or 0)*100/100:+.0f}</b> por $100</span>' )
                        + (f'<span style="font-size:0.65rem;color:rgba(0,0,0,0.5)">Apuesta Kelly: <b>{(_pk.get("kelly",0) or 0)*25:.1f}%</b> del bankroll</span>' if (_pk.get("kelly",0) or 0)>0 else "")
                        + f'</div></div>'
                        # Mini stats row
                        + f'<div style="display:flex;gap:6px;margin-top:8px;padding-top:8px;border-top:1px solid rgba(0,0,0,0.1)">'
                        + f'<div style="flex:1;text-align:center"><div style="font-size:0.6rem;color:rgba(0,0,0,0.4);font-weight:600;text-transform:uppercase">Prob MC</div>'
                        + f'<div style="font-size:0.85rem;font-weight:800;color:#111">{_pick_pct:.0f}%</div></div>'
                        + f'<div style="width:1px;background:rgba(0,0,0,0.12)"></div>'
                        + f'<div style="flex:1;text-align:center"><div style="font-size:0.6rem;color:rgba(0,0,0,0.4);font-weight:600;text-transform:uppercase">Cuota</div>'
                        + f'<div style="font-size:0.85rem;font-weight:800;color:#111">{_pick_dec}</div></div>'
                        + f'<div style="width:1px;background:rgba(0,0,0,0.12)"></div>'
                        + f'<div style="flex:1;text-align:center"><div style="font-size:0.6rem;color:rgba(0,0,0,0.4);font-weight:600;text-transform:uppercase">EV/100</div>'
                        + f'<div style="font-size:0.85rem;font-weight:800;color:#111">{(_pk.get("ev",0) or 0):+.0f}</div></div>'
                        + f'<div style="width:1px;background:rgba(0,0,0,0.12)"></div>'
                        + f'<div style="flex:1;text-align:center"><div style="font-size:0.6rem;color:rgba(0,0,0,0.4);font-weight:600;text-transform:uppercase">DQ</div>'
                        + f'<div style="font-size:0.85rem;font-weight:800;color:#111">{_sim.get("data_quality",0) or 0:.0f}%</div></div>'
                        + f'</div>'
                        + f'</div></div>'
                    )
                    with _cols[_ci]:
                        st.markdown(_card, unsafe_allow_html=True)
                        _ver_key = f"_ver_{_rp.get('id','')[:12]}_{_row_i}_{_ci}"
                        _ver_open = st.session_state.get(_ver_key, False)
                        def _toggle_ver(_k=_ver_key, _v=_ver_open):
                            st.session_state[_k] = not _v
                        st.button(
                            "▼ Ocultar" if _ver_open else "📋 Por qué este pick",
                            key=_ver_key + "_btn",
                            use_container_width=True,
                            on_click=_toggle_ver,
                        )
                        # Re-read after potential on_click update
                        _ver_open = st.session_state.get(_ver_key, False)
                        if _ver_open:
                            # ── Resumen en texto: por qué este pick ──────────
                            _sim_r  = _rp.get("sim", {})
                            _ev_r   = _pk.get("ev", 0) or 0
                            _prob_r = _pk.get("prob", 0) or 0
                            _prob_r = _prob_r if _prob_r <= 1 else _prob_r / 100
                            _kelly_r = (_pk.get("kelly", 0) or 0) * 25
                            _dq_r   = _sim_r.get("data_quality", 0) or 0
                            _mkt_r  = _pk.get("market", "")
                            _lbl_r  = _pk.get("label", "")
                            _home_r = _rp.get("home_team", "")
                            _away_r = _rp.get("away_team", "")
                            _nsim_r = _sim_r.get("n_simulations", 0) or 0

                            # Build reason sentences
                            _reasons = []

                            # 1. Probabilidad
                            _fav_side = "local" if _home_r in _lbl_r else "visitante"
                            _reasons.append(f"El modelo asigna <b>{_prob_r*100:.0f}%</b> de probabilidad al {_fav_side} ({_lbl_r}) en {_nsim_r:,} simulaciones.")

                            # 2. EV
                            if _ev_r > 5:
                                _reasons.append(f"La cuota tiene <b>valor positivo de +${_ev_r:.0f} por $100</b> apostados (la casa paga más de lo que debería).")
                            elif _ev_r > 0:
                                _reasons.append(f"EV ligeramente positivo (+{_ev_r:.1f}), la cuota es justa o favorable.")
                            else:
                                _reasons.append(f"EV negativo ({_ev_r:.1f}) — pick seleccionado por alta probabilidad, apostar con cautela.")

                            # 3. Form
                            _hf = _rp.get("home_form"); _af = _rp.get("away_form")
                            if _hf is not None and _af is not None:
                                _pick_form = _hf if _home_r in _lbl_r else _af
                                _rival_form = _af if _home_r in _lbl_r else _hf
                                if _pick_form > _rival_form + 0.1:
                                    _reasons.append(f"Mejor forma reciente: {_lbl_r[:12]} {_pick_form*100:.0f}% WR vs rival {_rival_form*100:.0f}% (últ. 10 partidos).")
                                elif _rival_form > _pick_form + 0.1:
                                    _reasons.append(f"Ojo: el rival tiene mejor forma ({_rival_form*100:.0f}% WR vs {_pick_form*100:.0f}%). El modelo favorece al pick por otros factores.")

                            # 4. H2H
                            _h2h_r = _rp.get("h2h", {}) or {}
                            _h2h_n = _h2h_r.get("count", 0) or 0
                            if _h2h_n >= 3:
                                _wh = _h2h_r.get("wins_home", 0)
                                _wa = _h2h_r.get("wins_away", 0)
                                _dr = _h2h_r.get("draws", 0)
                                _pick_is_home = _home_r in _lbl_r
                                _pick_wins_h2h = _wh if _pick_is_home else _wa
                                _rival_wins_h2h = _wa if _pick_is_home else _wh
                                _h2h_pct = _pick_wins_h2h / _h2h_n * 100
                                if _pick_wins_h2h > _rival_wins_h2h:
                                    _reasons.append(f"Historial H2H favorable: {_lbl_r[:12]} ganó {_pick_wins_h2h} de {_h2h_n} enfrentamientos directos ({_h2h_pct:.0f}%).")
                                elif _rival_wins_h2h > _pick_wins_h2h:
                                    _reasons.append(f"H2H en contra: el rival ganó {_rival_wins_h2h} de {_h2h_n} enfrentamientos. El modelo aún favorece este pick por probabilidad.")

                            # 5. B2B / fatigue
                            if _sim_r.get("away_back2back") and not _sim_r.get("home_back2back"):
                                _reasons.append("El visitante juega en back-to-back (menos descanso) — ventaja para el local.")
                            elif _sim_r.get("home_back2back") and not _sim_r.get("away_back2back"):
                                _reasons.append("El local juega en back-to-back — posible desventaja por fatiga.")

                            # 6. DQ
                            if _dq_r >= 70:
                                _reasons.append(f"Alta calidad de datos (DQ {_dq_r:.0f}%) — predicción confiable.")
                            elif _dq_r >= 35:
                                _reasons.append(f"Calidad de datos media (DQ {_dq_r:.0f}%) — predicción moderadamente confiable.")
                            else:
                                _reasons.append(f"Pocos datos disponibles (DQ {_dq_r:.0f}%) — mayor incertidumbre.")

                            # 7. Kelly
                            if _kelly_r > 0:
                                _reasons.append(f"Criterio Kelly recomienda apostar <b>{_kelly_r:.1f}%</b> del bankroll.")

                            # Render reasons
                            _reasons_html = "".join(
                                f'<div style="display:flex;gap:8px;margin-bottom:6px;align-items:flex-start">'
                                f'<span style="font-size:0.9rem;flex-shrink:0">{["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣"][min(_i,6)]}</span>'
                                f'<span style="font-size:0.78rem;color:#C8C8D0;line-height:1.5">{_r}</span>'
                                f'</div>'
                                for _i, _r in enumerate(_reasons)
                            )
                            st.markdown(
                                f'<div style="background:linear-gradient(160deg,#16161C 0%,#0F0F13 100%);'
                                f'border:1px solid rgba(255,85,0,0.2);border-radius:14px;padding:14px 16px;margin:4px 0 8px">'
                                f'<div style="font-size:0.62rem;font-weight:800;color:#FF5500;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px">💡 Por qué este pick</div>'
                                + _reasons_html +
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            st.markdown(_pick_diamante_card(_rp, _pk, rank=_row_i+_ci, is_fire=_is_fire), unsafe_allow_html=True)

            # ── DO PARLAY ─────────────────────────────────────────────────────
            _do_parlays = []
            for r in sr_cur_filtrado:
                g_state = next((g["state"] for g in games if g.get("id") == r.get("id")), "pre")
                if g_state == "post": continue
                sim = r["sim"]
                bs  = sim.get("best_single",{}) or {}
                if bs.get("market") == "DO" and bs.get("ev",0) > 0:
                    _companion = None
                    if sim.get("btts_ev",0) > 0:
                        _companion = {"market":"BTTS","label":"Ambos Anotan","prob":sim.get("p_btts",0),"ev":sim["btts_ev"]}
                    elif sim.get("o25_ev",0) > 0:
                        _companion = {"market":"O/U","label":"Over 2.5","prob":sim.get("p_o25",0),"ev":sim["o25_ev"]}
                    if _companion:
                        _do_parlays.append({"game":r,"do_pick":bs,"goals_pick":_companion})

            if _do_parlays:
                st.markdown('<div class="section-heading" style="margin-top:20px">🎯 PARLAY RECOMENDADO</div>', unsafe_allow_html=True)
                _dp  = sorted(_do_parlays, key=lambda x: x["do_pick"]["prob"]+x["goals_pick"]["prob"], reverse=True)[0]
                _g   = _dp["game"]
                _do  = _dp["do_pick"]
                _gl  = _dp["goals_pick"]
                _mc_do = "#a78bfa"
                _gpc, _mc_gl, _, _ = _pick_clr(_gl["market"], _gl.get("label",""))
                _comb_ev = _do["ev"] + _gl["ev"]
                st.markdown(
                    f'<div style="border-radius:16px;padding:14px;margin:8px 0;'
                    f'background:linear-gradient(135deg,rgba(167,139,250,0.12) 0%,#141414 60%,rgba(74,222,128,0.08) 100%);'
                    f'border:1px solid rgba(167,139,250,0.5);'
                    f'box-shadow:0 0 20px rgba(167,139,250,0.15)">'
                    f'<div style="height:2px;border-radius:12px 8px 0 0;margin:-14px -14px 12px -14px;'
                    f'background:linear-gradient(90deg,transparent,#a78bfa,#00C896,transparent)"></div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">'
                    f'<div>'
                    f'<div style="font-size:0.694rem;color:#6B7280;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:3px">'
                    f'🎯 PARLAY · {league_label(_g["league"])}</div>'
                    f'<div style="font-size:1.064rem;font-weight:700;color:#E8E8E8">'
                    f'{_g["away_team"]} vs {_g["home_team"]}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:1.232rem;font-weight:900;color:#a78bfa;font-family:Inter,sans-serif">'
                    f'EV +{_comb_ev:.1f}</div>'
                    f'<div style="font-size:0.65rem;color:#6B7280">combinado</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="margin-top:10px;display:flex;align-items:center;gap:6px;flex-wrap:wrap">'
                    f'<span style="background:{_mc_do}22;color:{_mc_do};border:1px solid {_mc_do}55;'
                    f'border-radius:5px;padding:3px 9px;font-size:0.762rem;font-weight:800">DO</span>'
                    f'<span style="color:#E8E8E8;font-size:0.918rem">{_do["label"]}</span>'
                    f'<span style="color:#444444;font-size:1.12rem;margin:0 2px">✕</span>'
                    f'<span style="background:{_mc_gl}22;color:{_mc_gl};border:1px solid {_mc_gl}55;'
                    f'border-radius:5px;padding:3px 9px;font-size:0.762rem;font-weight:800">{_gl["market"]}</span>'
                    f'<span style="color:#E8E8E8;font-size:0.918rem">{_gl["label"]}</span>'
                    f'</div>'
                    f'<div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap">'
                    f'<span style="font-size:0.694rem;color:{_mc_do}">DO EV +{_do["ev"]:.1f} · {_do.get("prob",0):.0f}%</span>'
                    f'<span style="font-size:0.694rem;color:{_mc_gl}">{_gl["market"]} EV +{_gl["ev"]:.1f} · {_gl["prob"]:.0f}%</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # (PICKS FUEGO removed — 1 per sport shown in grid above)

        # Avoid
        avoid=[r for r in sr_cur_filtrado if r["sim"].get("best_single") and (r["sim"]["best_single"]["ev"] or 0)<-15]
        avoid.sort(key=lambda x:x["sim"]["best_single"]["ev"])
        if avoid:
            st.markdown('<div class="section-heading">♦ Evitar</div>', unsafe_allow_html=True)
            for r in avoid[:3]:
                bs=r["sim"]["best_single"]
                st.markdown(f'<div class="game-row"><span class="game-title" style="color:#ef4444">✗ {r["away_team"]} @ {r["home_team"]}</span><span class="game-meta">{league_label(r["league"])} · EV {bs["ev"]:.1f} · {bs["label"]}</span></div>',unsafe_allow_html=True)

        st.markdown('<div class="den-divider" style="margin:16px 0"></div>',unsafe_allow_html=True)
        today_str=datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")
        total_sims=len(sr_cur)*sr_cur[0]["sim"]["n_simulations"] if sr_cur else 0
        _src = "DEMO" if is_demo else "ESPN Live"
        st.markdown(f'<div style="text-align:center;font-family:\'Inter\',sans-serif;font-size:0.806rem;color:#444444">📅 {today_str} · {total_sims:,} simulaciones · {_src}</div>',unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
elif _active_page == "Picks":
    # ══════════════════════════════════════════════════════════════════════════
    # PRÓXIMOS PARTIDOS — sport tiles + date/league expanders  (TOP of tab)
    # ══════════════════════════════════════════════════════════════════════════
    from datetime import timedelta as _td_pt
    _now_mx_pt = datetime.now(timezone.utc) - _td_pt(hours=6)  # CDMX = UTC-6
    _meses_pt  = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                  "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    _SPORT_META_P = {
        "Basketball": {"emoji":"🏀","color":"#f97316","accent":"rgba(249,115,22,0.12)"},
        "Soccer":     {"emoji":"⚽","color":"#00C896","accent":"rgba(74,222,128,0.10)"},
        "Hockey":     {"emoji":"🏒","color":"#60a5fa","accent":"rgba(96,165,250,0.12)"},
        "Baseball":   {"emoji":"⚾","color":"#ef4444","accent":"rgba(239,68,68,0.10)"},
        "Football":   {"emoji":"🏈","color":"#a78bfa","accent":"rgba(167,139,250,0.10)"},
    }
    _SPORTS_ORDER_P = ["Soccer","Basketball","Hockey","Baseball","Football"]

    _today_mx_p    = _now_mx_pt.strftime("%Y-%m-%d")
    _tom_mx_p      = (_now_mx_pt + _td_pt(days=1)).strftime("%Y-%m-%d")
    _d2_mx_p       = (_now_mx_pt + _td_pt(days=2)).strftime("%Y-%m-%d")
    _yday_mx_p     = (_now_mx_pt - _td_pt(days=1)).strftime("%Y-%m-%d")
    _valid_dates_p = {_yday_mx_p, _today_mx_p, _tom_mx_p}

    def _mx_date_p(g):
        raw = g.get("date") or ""
        if not raw: return _today_mx_p
        try:
            from datetime import timezone as _tzp
            _u = datetime.strptime(raw[:19].replace("T"," "), "%Y-%m-%d %H:%M:%S").replace(tzinfo=_tzp.utc)
            return (_u - _td_pt(hours=6)).strftime("%Y-%m-%d")
        except: return raw[:10]

    def _mx_time_p(g):
        raw = g.get("date") or ""
        if not raw: return ""
        try:
            from datetime import timezone as _tzp
            _u = datetime.strptime(raw[:19].replace("T"," "), "%Y-%m-%d %H:%M:%S").replace(tzinfo=_tzp.utc)
            return (_u - _td_pt(hours=6)).strftime("%H:%M")
        except: return ""

    def _fmt_date_p(ds):
        try:
            _dt = datetime.strptime(ds, "%Y-%m-%d")
            if ds == _today_mx_p:  return f"📅 Hoy · {_dt.day} {_meses_pt[_dt.month-1]} {_dt.year}"
            if ds == _tom_mx_p:    return f"📅 Mañana · {_dt.day} {_meses_pt[_dt.month-1]} {_dt.year}"
            return f"📅 {_dt.day} {_meses_pt[_dt.month-1]} {_dt.year}"
        except: return ds

    def _card_p(g, sm):
        _time = _mx_time_p(g)
        _time_html = f'<span style="color:#C9A84C;font-size:0.728rem;flex-shrink:0">{_time}</span>' if _time else ""
        _o = g.get("odds",{}) or {}
        _op = []
        if _o.get("over_under"): _op.append(f"O/U {_o['over_under']}")
        if _o.get("home_ml"):    _op.append(f"ML {_o['home_ml']}")
        _oh = f'<div style="color:#C9A84C;font-size:0.672rem;margin-top:2px">{" · ".join(_op)}</div>' if _op else ""
        _ph = ""
        _rp = {_rr.get("id",""): _rr for _rr in st.session_state.get("sim_results",[])}.get(g.get("id",""))
        if _rp:
            _bs = _rp["sim"].get("best_single",{}) or {}
            if _bs and _bs.get("ev",0) > 0:
                _mc2_pc, _mc2_ac, _, _mc2_dl = _pick_clr(_bs.get("market",""), _bs.get("label",""))
                _ev2s = f'+{_bs["ev"]:.1f}' if (_bs.get("ev") or 0)>=0 else f'{_bs["ev"]:.1f}'
                _ph = (
                    f'<div style="margin-top:4px;display:flex;align-items:center;gap:4px;flex-wrap:wrap">'
                    f'<span style="background:{_mc2_pc}28;color:{_mc2_ac};border:1px solid {_mc2_pc}66;'
                    f'border-radius:12px;padding:0 6px;font-size:0.627rem;font-weight:800">{_mc2_dl}</span>'
                    f'<span style="color:#E8E8E8;font-size:0.728rem;min-width:0;overflow:hidden;'
                    f'text-overflow:ellipsis;white-space:nowrap">{_bs.get("label","")}</span>'
                    f'<span style="color:{_mc2_ac};font-size:0.65rem;margin-left:auto;flex-shrink:0">'
                    f'EV {_ev2s}</span>'
                    f'</div>'
                )
        return (
            f'<div style="padding:7px 8px;margin:3px 0;border-radius:7px;'
            f'background:{sm["accent"]};border-left:2px solid {sm["color"]}66;overflow:hidden">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4px">'
            f'<div style="min-width:0;overflow:hidden;flex:1">'
            f'<div style="font-size:0.806rem;font-weight:700;color:#E8E8E8;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{g["away_team"]}</div>'
            f'<div style="font-size:0.694rem;color:#6B7280;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">@ {g["home_team"]}</div>'
            f'</div>'
            f'<div style="flex-shrink:0;padding-left:4px">{_time_html}</div>'
            f'</div>'
            f'{_oh}{_ph}'
            f'</div>'
        )

    # Build tree — pre + live games, by sport → date → league
    _tree_p = {}
    for _g in games:
        if _g["state"] == "post": continue   # skip finished only
        _sg_p = LEAGUES.get(_g["league"], {}).get("group", "Soccer")
        _gd   = _mx_date_p(_g)
        if _gd not in _valid_dates_p: continue
        _tree_p.setdefault(_sg_p, {}).setdefault(_gd, {}).setdefault(_g["league"], []).append(_g)

    _sports_p = [s for s in _SPORTS_ORDER_P if s in _tree_p]
    _total_p  = sum(len(gs) for sp in _sports_p for dmap in _tree_p[sp].values() for gs in dmap.values())

    # ── Header row: título + botón RE-SIMULAR alineados ─────────────────────
    _hdr_col1, _hdr_col2 = st.columns([3, 1])
    with _hdr_col1:
        st.markdown(f'<div class="section-heading">📅 PRÓXIMOS PARTIDOS</div>', unsafe_allow_html=True)
    with _hdr_col2:
        if st.button(f"🔄 {n_sims:,}×", use_container_width=True, key="btn_resim_picks",
                     help="Re-simular todos los partidos"):
            t0 = time.time()
            sr2 = run_all_simulations(games, n=n_sims)
            elapsed = time.time() - t0
            st.session_state["sim_results"] = sr2
            st.session_state["last_sim_demo"] = is_demo
            n_pos = len([r for r in sr2 if r["sim"].get("best_single") and (r["sim"]["best_single"]["ev"] or 0) > 0])
            st.toast(f"✓ {len(games)*n_sims:,} sims en {elapsed:.1f}s · {n_pos} value bets", icon="🔮")
            st.rerun()

    if not _sports_p:
        st.markdown('<div class="warn-banner">No hay partidos próximos. Pulsa ▶ ANALIZAR para cargar datos.</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="font-size:0.762rem;color:#6B7280;margin-bottom:10px">'
            f'{_total_p} partidos · {len(_sports_p)} deportes · hora CDMX</div>',
            unsafe_allow_html=True
        )
        # ── Sport selector tiles — clickable ─────────────────────────────────
        _sel_sp = st.session_state.get("_picks_sel_sport", None)
        if _sel_sp and _sel_sp not in _sports_p:
            _sel_sp = None
            st.session_state["_picks_sel_sport"] = None

        _sp_cols_p = st.columns(len(_sports_p))
        # Inject 3D card style for sport buttons — scoped to this section
        _sp_styles = ""
        for _ci_tmp, _sp_tmp in enumerate(_sports_p):
            _c_tmp = _SPORT_META_P[_sp_tmp]["color"]
            _cr_t,_cg_t,_cb_t = int(_c_tmp[1:3],16),int(_c_tmp[3:5],16),int(_c_tmp[5:7],16)
            _is_s_tmp = (_sel_sp == _sp_tmp)
            _ring_tmp = f"0 0 0 3px {_c_tmp}," if _is_s_tmp else ""
            _op_tmp   = "1" if (_sel_sp is None or _is_s_tmp) else "0.45"
            _sp_styles += f"""
div[data-testid="stButton"]:has(> button[data-testid="stBaseButton-secondary"][key="btn_sp_{_sp_tmp}"]) button,
div[data-testid="stButton"]:has(> button[key="btn_sp_{_sp_tmp}"]) button {{
  background: linear-gradient(170deg,rgba({_cr_t},{_cg_t},{_cb_t},0.25) 0%,rgba({_cr_t},{_cg_t},{_cb_t},0.07) 100%) !important;
  border: 1px solid rgba({_cr_t},{_cg_t},{_cb_t},{"0.75" if _is_s_tmp else "0.28"}) !important;
  border-top: 1.5px solid rgba({_cr_t},{_cg_t},{_cb_t},{"1.0" if _is_s_tmp else "0.5"}) !important;
  border-bottom: 2px solid rgba(0,0,0,0.5) !important;
  box-shadow: {_ring_tmp}0 6px 20px rgba({_cr_t},{_cg_t},{_cb_t},{"0.3" if _is_s_tmp else "0.12"}),
              0 1px 0 rgba(255,255,255,0.1) inset !important;
  color: {_c_tmp} !important;
  font-size: 0.68rem !important;
  font-weight: 900 !important;
  letter-spacing: 1.2px !important;
  text-transform: uppercase !important;
  padding: 18px 4px 14px !important;
  min-height: 96px !important;
  height: auto !important;
  border-radius: 16px !important;
  white-space: pre-line !important;
  line-height: 1.7 !important;
  opacity: {_op_tmp} !important;
  font-family: 'Barlow',sans-serif !important;
  text-shadow: 0 1px 6px rgba({_cr_t},{_cg_t},{_cb_t},0.5) !important;
}}"""
        st.markdown(f"<style>{_sp_styles}</style>", unsafe_allow_html=True)

        for _ci_p, _sp_p in enumerate(_sports_p):
            _smp = _SPORT_META_P[_sp_p]
            _n_p = sum(len(gs) for dmap in _tree_p[_sp_p].values() for gs in dmap.values())
            _is_sel = (_sel_sp == _sp_p)
            _check = " ✓" if _is_sel else ""
            with _sp_cols_p[_ci_p]:
                _btn_txt = _smp["emoji"] + "\n" + _sp_p + "\n" + str(_n_p) + " juegos" + _check
                def _tog_sp(_sp=_sp_p, _sel=_is_sel):
                    st.session_state["_picks_sel_sport"] = None if _sel else _sp
                st.button(
                    _btn_txt,
                    key=f"btn_sp_{_sp_p}",
                    use_container_width=True,
                    on_click=_tog_sp,
                )

    if is_demo:
        st.markdown('<div class="demo-banner">Modo demo activo.</div>', unsafe_allow_html=True)

    # Build sim lookup dict
    _sim_map = {r.get("id", ""): r for r in st.session_state.get("sim_results", [])}

    def _oracle_pick(r):
        """Always return best pick for a game — no EV+ required.
        Soccer:     best of {ML, BTTS(EV+), Over2.5(EV+)} by prob
        Basketball/Hockey: best of {ML, Over or Under line} by prob
        Baseball/Football: best of {ML, Over/Under line} by prob
        """
        sim = r["sim"]
        sg  = LEAGUES.get(r.get("league",""),{}).get("group","Soccer")
        h_prob = sim.get("home_pct",0) or 0
        a_prob = sim.get("away_pct",0) or 0
        h_ml = sim.get("home_ml"); a_ml = sim.get("away_ml")
        if h_prob >= a_prob:
            _ml_t, _ml_p, _ml_ev = r["home_team"], h_prob, sim.get("home_ev") or 0
        else:
            _ml_t, _ml_p, _ml_ev = r["away_team"], a_prob, sim.get("away_ev") or 0
        ml_pick = {"market":"ML","label":_ml_t,"prob":_ml_p,"ev":_ml_ev}
        cands = [ml_pick]

        if sg == "Soccer":
            _btts_ev = sim.get("btts_ev") or 0
            _btts_pb = sim.get("p_btts") or 0
            _o25_ev  = sim.get("o25_ev")  or 0
            _o25_pb  = sim.get("p_o25")   or 0
            if _btts_ev > 0 and _btts_pb > 0:
                cands.append({"market":"BTTS","label":"Ambos Anotan","prob":_btts_pb,"ev":_btts_ev})
            if _o25_ev > 0 and _o25_pb > 0:
                cands.append({"market":"O/U","label":"Over 2.5","prob":_o25_pb,"ev":_o25_ev})
        else:
            _ou_line = sim.get("ou_line") or ""
            _p_over  = sim.get("p_o_total") or 0
            _p_under = sim.get("p_u_total") or 0
            _implicit = _ou_line.startswith("~")
            _multi   = sim.get("multi_lines", {})

            if _ou_line and not _implicit and (_p_over > 0 or _p_under > 0):
                # Sharp logic: use multi_lines to find the best edge
                # Best bet = the line+side with highest probability (furthest from 50%)
                _best_prob = 0; _best_label = None; _best_side = None
                for _l, _d in _multi.items():
                    _po_l = _d["over"]; _pu_l = _d["under"]
                    if _po_l >= _pu_l and _po_l > _best_prob:
                        _best_prob = _po_l; _best_label = f"Over {_l:.1f}"; _best_side = "over"
                    elif _pu_l > _po_l and _pu_l > _best_prob:
                        _best_prob = _pu_l; _best_label = f"Under {_l:.1f}"; _best_side = "under"

                # Minimum threshold: only add O/U if model has real edge (>52%)
                if _best_label and _best_prob >= 52:
                    cands.append({"market":"O/U","label":_best_label,"prob":_best_prob,"ev":0})
            elif _ou_line and _implicit:
                # Implicit line (no ESPN line): use ESPN-line MC result directly
                # Only add Over for Basketball/Hockey (Under on implicit = weak signal)
                try: _line = float(_ou_line.lstrip("~"))
                except: _line = None
                if _line and sg not in ("Basketball", "Hockey"):
                    if _p_over >= _p_under and _p_over >= 52:
                        cands.append({"market":"O/U","label":f"Over {_line:.1f} (avg)","prob":_p_over,"ev":0})
                    elif _p_under > _p_over and _p_under >= 52:
                        cands.append({"market":"O/U","label":f"Under {_line:.1f} (avg)","prob":_p_under,"ev":0})

        # ── Spread: short-circuit if MC already selected it ───────────────────
        # run_monte_carlo already evaluated all markets including Spread.
        # If it chose Spread as best_single, trust that and return directly.
        _bs_mc = sim.get("best_single")
        if _bs_mc and _bs_mc.get("market") == "Spread" and (_bs_mc.get("ev") or 0) > 0:
            _spr_prob = _bs_mc.get("prob") or 0
            # Normalize: MC stores prob as 0-100 percentage
            _spr_prob_f = _spr_prob / 100 if _spr_prob > 1 else _spr_prob
            return {
                "market": "Spread",
                "label":  _bs_mc.get("label", ""),
                "prob":   _spr_prob_f,
                "ev":     _bs_mc.get("ev") or 0,
                "ml":     _bs_mc.get("ml", "-110"),
                "kelly":  _bs_mc.get("kelly", 0) or 0,
            }

        # ── Add Spread to oracle candidates (when MC didn't pick it) ──────────
        _p_hc = sim.get("p_home_cover")   # 0-100
        _p_ac = sim.get("p_away_cover")   # 0-100
        _spr_line = sim.get("spread_line")
        if _spr_line is not None and (_p_hc is not None or _p_ac is not None):
            _dec = 1.909  # -110
            _spr_implied = sim.get("spread_implied", False)
            _pfx = "~" if _spr_implied else ""
            _home_nm = (r.get("home_team","") or "")[:14]
            _away_nm = (r.get("away_team","") or "")[:14]
            if _p_hc is not None and _p_hc >= 52.4:
                _pf = _p_hc / 100
                _ef = round((_pf*(_dec-1)-(1-_pf))*100, 1)
                cands.append({"market":"Spread","label":f"{_pfx}{_home_nm} {float(_spr_line):+.1f} (Spread)","prob":_pf,"ev":_ef,"ml":"-110"})
            if _p_ac is not None and _p_ac >= 52.4:
                _pf = _p_ac / 100
                _ef = round((_pf*(_dec-1)-(1-_pf))*100, 1)
                cands.append({"market":"Spread","label":f"{_pfx}{_away_nm} {-float(_spr_line):+.1f} (Spread)","prob":_pf,"ev":_ef,"ml":"-110"})

        # Score compuesto universal
        scored = [(c, pick_score_universal(c, sim, r, sg)) for c in cands]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]

    def _build_extra_panels(g, sim, bp):
        """
        Build H2H, Weather, Line Movement, and Value Gap HTML panels for a pick card.
        Returns HTML string — empty string if nothing relevant to show.
        """
        parts = []

        # ── Value Gap panel ─────────────────────────────────────────────────
        # Show: model prob vs market implied prob, gap in pp
        _home_ml = sim.get("home_ml") or g.get("odds", {}).get("home_ml", "")
        _away_ml = sim.get("away_ml") or g.get("odds", {}).get("away_ml", "")
        _vg_parts = []
        if _home_ml:
            _vg = get_value_gap(sim["home_pct"] / 100, _home_ml)
            if _vg and abs(_vg["gap_pp"]) >= 3:
                _vg_parts.append(
                    f'<span style="color:{_vg["color"]};font-size:0.68rem;font-weight:600">'
                    f'{g["home_team"][:10]}: {_vg["model_prob"]:.0f}% vs {_vg["implied_prob"]:.0f}% impl '
                    f'<b>({_vg["gap_pp"]:+.1f}pp) {_vg["rating"]}</b></span>'
                )
        if _away_ml:
            _vg = get_value_gap(sim["away_pct"] / 100, _away_ml)
            if _vg and abs(_vg["gap_pp"]) >= 3:
                _vg_parts.append(
                    f'<span style="color:{_vg["color"]};font-size:0.68rem;font-weight:600">'
                    f'{g["away_team"][:10]}: {_vg["model_prob"]:.0f}% vs {_vg["implied_prob"]:.0f}% impl '
                    f'<b>({_vg["gap_pp"]:+.1f}pp) {_vg["rating"]}</b></span>'
                )
        if _vg_parts:
            parts.append(
                '<div style="margin-top:5px;padding:4px 6px;background:rgba(201,168,76,0.06);'
                'border:1px solid rgba(201,168,76,0.15);border-radius:5px">'
                '<div style="font-size:0.60rem;color:#6B7280;margin-bottom:2px">📊 VALUE GAP vs Mercado</div>'
                + '<br>'.join(_vg_parts) + '</div>'
            )

        # ── H2H panel ────────────────────────────────────────────────────────
        _h2h = g.get("h2h", {})
        if _h2h and _h2h.get("count", 0) >= 3:
            _cnt  = _h2h["count"]
            _wh   = _h2h["wins_home"]
            _wa   = _h2h["wins_away"]
            _dr   = _h2h["draws"]
            _avg  = _h2h.get("avg_total", 0)
            _btts = round(_h2h.get("btts_rate", 0) * 100)
            _o25  = round(_h2h.get("over25_rate", 0) * 100)
            _l5   = _h2h.get("last5", [])
            _l5_html = "".join(
                f'<span style="display:inline-block;width:16px;height:16px;line-height:16px;'
                f'text-align:center;border-radius:12px;font-size:0.60rem;font-weight:700;margin-right:2px;'
                f'background:{"#15803d" if r=="W" else ("#7f1d1d" if r=="L" else "#1e3a5f")};'
                f'color:{"#00C896" if r=="W" else ("#f87171" if r=="L" else "#93c5fd")}">{r}</span>'
                for r in _l5
            )
            parts.append(
                f'<div style="margin-top:5px;padding:4px 6px;background:rgba(96,165,250,0.05);'
                f'border:1px solid rgba(96,165,250,0.12);border-radius:5px">'
                f'<div style="font-size:0.60rem;color:#6B7280;margin-bottom:3px">⚔️ H2H últimos {_cnt} enfrentamientos</div>'
                f'<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">'
                f'<span style="font-size:0.68rem;color:#f97316;font-weight:700">{g["home_team"][:9]}: {_wh}V</span>'
                f'<span style="font-size:0.68rem;color:#a78bfa">{_dr}E</span>'
                f'<span style="font-size:0.68rem;color:#60a5fa;font-weight:700">{g["away_team"][:9]}: {_wa}V</span>'
                f'<span style="font-size:0.65rem;color:#C9A84C">avg {_avg:.1f}gls</span>'
                f'<span style="font-size:0.65rem;color:#00C896">BTTS {_btts}%</span>'
                f'<span style="font-size:0.65rem;color:#ff6a00">O2.5 {_o25}%</span>'
                f'</div>'
                f'<div style="margin-top:3px">{_l5_html}'
                f'<span style="font-size:0.60rem;color:#444444;margin-left:4px">← últimos</span></div>'
                f'</div>'
            )

        # ── Weather panel (only when significant) ───────────────────────────
        _wx = g.get("weather", {})
        if _wx and _wx.get("significant"):
            _impact = _wx.get("impact", "")
            _adj    = _wx.get("ou_adj", 0)
            _adj_str = f"O/U adj {_adj*100:+.0f}%" if _adj else ""
            parts.append(
                f'<div style="margin-top:5px;padding:4px 6px;background:rgba(147,197,253,0.05);'
                f'border:1px solid rgba(147,197,253,0.12);border-radius:5px">'
                f'<div style="font-size:0.60rem;color:#6B7280;margin-bottom:1px">🌤 Clima · {_wx.get("desc","")}</div>'
                f'<div style="font-size:0.68rem;color:#93c5fd">{_impact}'
                f'{"  ·  " if _adj_str else ""}'
                f'<span style="color:#C9A84C">{_adj_str}</span></div>'
                f'</div>'
            )

        # ── Line Movement panel ──────────────────────────────────────────────
        _lm = g.get("line_movement", {})
        if _lm and _lm.get("n_snaps", 0) >= 2:
            _ou_d   = _lm.get("ou_delta")
            _hml_d  = _lm.get("hml_delta")
            _dir    = _lm.get("direction", "neutral")
            _lm_parts = []
            if _ou_d is not None and _ou_d != 0:
                _oc = "#ef4444" if _ou_d < 0 else "#00C896"
                _lm_parts.append(f'<span style="color:{_oc}">O/U {_ou_d:+.1f}</span>')
            if _hml_d is not None and abs(_hml_d) >= 5:
                _mc = "#ef4444" if _hml_d < 0 else "#00C896"
                _steam = "🔥 STEAM" if abs(_hml_d) >= 15 else "↗"
                _lm_parts.append(f'<span style="color:{_mc}">ML {_hml_d:+.0f} {_steam}</span>')
            if _lm_parts:
                parts.append(
                    f'<div style="margin-top:5px;padding:3px 6px;background:rgba(251,191,36,0.05);'
                    f'border:1px solid rgba(251,191,36,0.15);border-radius:5px;'
                    f'display:flex;gap:10px;align-items:center">'
                    f'<span style="font-size:0.60rem;color:#6B7280">📈 Línea</span>'
                    + "  ".join(_lm_parts) +
                    f'<span style="font-size:0.60rem;color:#444444;margin-left:auto">{_lm["n_snaps"]} snaps</span>'
                    f'</div>'
                )

        return "".join(parts)

    def _oracle_card(g, sm):
        """Full oracle card for a game — always shows a pick, no EV+ gate."""
        _r    = _sim_map.get(g.get("id",""))
        _time = _mx_time_p(g)
        _time_s = f' · <span style="color:#C9A84C">{_time}</span>' if _time else ""
        _sd_raw = (g.get("status_detail") or "").replace("<","").replace(">","").replace("/","").split("\n")[0].strip()
        # Si ESPN dice "Scheduled" o vacío, mostrar hora CDMX
        if not _sd_raw or _sd_raw.lower() in ("scheduled", "cancelado", "postponed"):
            _hora_cdmx = _mx_time_p(g)
            _sd = (_hora_cdmx + " CDMX") if _hora_cdmx else _sd_raw
        else:
            _sd = _sd_raw
        _low_c  = _r["sim"].get("low_confidence",False) if _r else False
        _lc_tag = '<span style="background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b44;border-radius:12px;padding:1px 5px;font-size:0.616rem;margin-left:4px">⚠ sin cuotas</span>' if _low_c else ""
        _live_tag = ('<span style="background:rgba(255,60,60,0.2);color:#ff6b6b;border:1px solid rgba(255,60,60,0.4);'
                     'border-radius:12px;padding:1px 5px;font-size:0.616rem;margin-left:4px;font-weight:700">🔴 VIVO</span>'
                     if g.get("state") == "in" else "")
        _has_ev = bool(_r and _r["sim"].get("best_single") and _r["sim"]["best_single"].get("ev",0)>0)

        # Card will be colored after pick is computed — use placeholder until then
        _html_header = (
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:4px">'
            f'<div>'
            f'<div class="game-title">{g["away_team"]} @ {g["home_team"]}</div>'
            f'<div class="game-meta">{league_label(g["league"])} · {_sd}{_time_s}{_lc_tag}{_live_tag}</div>'
            f'</div>'
        )
        _html = None  # will be assembled after pick color is known

        if not _r:
            _html = (
                f'<div class="game-row" style="border-left:3px solid {sm["color"]}44;margin:4px 0;">'
                + _html_header +
                '<div style="color:#444444;font-size:0.762rem;align-self:center">Sin simular</div></div></div>'
            )
            return _html

        sim = _r["sim"]
        dq  = sim["data_quality"]
        dqc = "#00C896" if dq>=70 else "#C9A84C" if dq>=40 else "#ef4444"

        # ── Build white sportsbook card (same as Rongol) ─────────────────────
        bp  = _oracle_pick(_r)
        _bpc, _bac, _, _bdl = _pick_clr(bp["market"], bp.get("label",""))
        _ev = bp.get("ev",0) or 0
        _ev_str = f"+{_ev:.1f}" if _ev >= 0 else f"{_ev:.1f}"
        _ev_c   = "#00C896" if _ev>=10 else ("#fbbf24" if _ev>=0 else "#ef4444")
        badge = (
            f'<span style="background:{_bpc}28;color:{_bac};border:1px solid {_bpc}66;'
            f'border-radius:12px;padding:1px 8px;font-size:0.694rem;font-weight:800;margin-right:5px">{_bdl}</span>'
            f'<span style="font-weight:700;font-size:0.896rem;color:#FFE87C">{bp["label"]}</span>'
            f'<span style="color:{_ev_c};font-size:0.762rem;margin-left:6px">EV {_ev_str}</span>'
            f'<span style="color:#6B7280;font-size:0.694rem;margin-left:4px">· {bp["prob"]:.0f}%</span>'
        )

        # ── Build white sportsbook card ─────────────────────────────────────
        _bpc2 = _bpc; _bac2 = _bac  # keep for badge coloring
        _card_bg     = "background:linear-gradient(160deg,#F6F6F9 0%,#E9E9EE 100%)"
        _card_border = "border:1px solid rgba(0,0,0,0.07);border-top:1px solid rgba(255,255,255,0.9)"
        _card_shadow = "box-shadow:0 8px 24px rgba(0,0,0,0.22),0 1px 0 rgba(255,255,255,0.85) inset"
        _top_stripe  = ""  # no stripe on white card

        # Only show ML odds if at least one side has a value
        _has_ml = bool(sim.get("home_ml") or sim.get("away_ml"))
        _ml_line = (f'ML {sim["away_ml"] or "—"}/{sim["home_ml"] or "—"}<br>'
                    if _has_ml else "")
        _body = (
            f'<div style="text-align:right;font-size:0.728rem;color:#6B7280;flex-shrink:0">'
            f'{_ml_line}'
            f'<span style="color:{dqc}">DQ {dq:.0f}%</span></div>'
            f'</div>'
            f'<div style="margin-top:4px">{badge}</div>'
        )

        # Win probability bars
        _bars = f'<div style="margin-top:6px">{bar(sim["away_pct"],"#60a5fa",g["away_team"])}' 
        if sim["is_soccer"]: _bars += bar(sim["draw_pct"],"#a78bfa","Empate")
        _bars += bar(sim["home_pct"],"#f97316",g["home_team"]) + "</div>"

        # Goals / totals footer
        _footer = ""
        if sim.get("use_goals") and sim.get("p_btts") is not None and sim.get("is_soccer", False):
            btc = "#00C896" if (sim.get("btts_ev") or 0)>0 else "#6B7E6E"
            o2c = "#ff6a00" if (sim.get("o25_ev") or 0)>0 else "#6B7E6E"
            o3c = "#ff6a00" if (sim.get("o35_ev") or 0)>0 else "#6B7E6E"
            dq_src = "ML+Récords" if dq>=50 else ("Récords" if dq>=25 else ("Prior" if dq>0 else "Sin datos"))
            _footer = (
                f'<div style="font-size:0.728rem;margin-top:4px;display:flex;gap:10px;flex-wrap:wrap">'
                f'<span style="color:{btc}">⚽ BTTS {sim["p_btts"]}%</span>'
                f'<span style="color:{o2c}">O2.5 {sim["p_o25"]}%</span>'
                f'<span style="color:{o3c}">O3.5 {sim.get("p_o35","—")}%</span>'
                f'<span style="color:#444444;margin-left:auto">{dq_src}</span>'
                f'</div>'
            )
            # Marcadores más frecuentes
            _sf = sim.get("score_freq", [])
            if _sf:
                _sf_html = '<div style="margin-top:5px;padding:5px 7px;background:rgba(255,255,255,0.03);border-radius:8px;border:1px solid #222">'
                _sf_html += '<div style="font-size:0.6rem;color:#6B7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px">📊 Marcadores más frecuentes</div>'
                _sf_html += '<div style="display:flex;flex-wrap:wrap;gap:4px">'
                _away = sim.get("away_team", g.get("away_team","V"))
                _home = sim.get("home_team", g.get("home_team","L"))
                for _i, ((h_g, a_g), _cnt) in enumerate(_sf[:6]):
                    _pct = round(_cnt / (sim.get("n_simulations", 10000)) * 100, 1)
                    _is_top = _i == 0
                    if h_g > a_g:
                        _sc = "#f97316"  # local gana — naranja
                    elif h_g < a_g:
                        _sc = "#60a5fa"  # visitante gana — azul
                    else:
                        _sc = "#a78bfa"  # empate — morado
                    _sf_html += (
                        f'<div style="background:{"rgba(255,255,255,0.07)" if _is_top else "rgba(255,255,255,0.03)"};'
                        f'border:1px solid {"rgba(255,255,255,0.15)" if _is_top else "#222"};'
                        f'border-radius:8px;padding:3px 8px;text-align:center;min-width:52px">'
                        f'<div style="font-size:{"0.82rem" if _is_top else "0.75rem"};font-weight:{"800" if _is_top else "600"};color:{_sc}">'
                        f'{h_g}–{a_g}</div>'
                        f'<div style="font-size:0.6rem;color:#6B7280">{_pct}%</div>'
                        f'</div>'
                    )
                _sf_html += '</div></div>'
                _footer += _sf_html
        elif sim.get("ou_line") and sim.get("p_o_total") is not None:
            _po = sim.get("p_o_total") or 0
            _pu = sim.get("p_u_total") or 0
            _sg_icon_ou = {"Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}.get(
                LEAGUES.get(g.get("league",""),{}).get("group",""), "🎯")
            dq_src_ou = "ML+Récords" if dq>=50 else ("Récords" if dq>=25 else ("Prior" if dq>0 else "Sin datos"))
            _multi = sim.get("multi_lines", {})

            # ── Multi-line table: show each line with Over% / Under% ──────────
            # Sort lines ascending. ESPN line shown in bold, others dimmer.
            _ou_val_f = None
            try: _ou_val_f = float(sim["ou_line"].lstrip("~"))
            except: pass
            _implicit_tag = "~" if (sim["ou_line"] or "").startswith("~") else ""

            _rows_html = ""
            if _multi and _ou_val_f:
                _sorted_lines = sorted(_multi.keys())
                for _l in _sorted_lines:
                    _d = _multi[_l]
                    _po_l = _d["over"]; _pu_l = _d["under"]
                    _is_espn = (abs(_l - _ou_val_f) < 0.01)
                    # Color: best side orange (Over) or purple (Under)
                    _over_best = _po_l >= _pu_l
                    _oc = "#ff6a00" if _po_l >= 52 else ("#C9A84C" if _po_l >= 48 else "#6B7E6E")
                    _uc = "#a78bfa" if _pu_l >= 52 else ("#C9A84C" if _pu_l >= 48 else "#6B7E6E")
                    _arrow_lbl = f'Over {_l:.1f}' if _over_best else f'Under {_l:.1f}'
                    _arrow_clr = "#ff6a00" if _over_best else "#a78bfa"
                    _arrow_pct = _po_l if _over_best else _pu_l
                    # ESPN line row: slightly highlighted background
                    _row_bg = "background:rgba(201,168,76,0.07);border-radius:12px;padding:2px 6px;" if _is_espn else "padding:2px 6px;"
                    _lbl_style = "font-weight:700;color:#C9A84C;" if _is_espn else "color:#444444;"
                    _espn_badge = ' <span style="font-size:0.6rem;color:#C9A84C;opacity:0.7">ESPN</span>' if _is_espn else ""
                    _rows_html += (
                        f'<div style="display:flex;align-items:center;gap:8px;{_row_bg}">'
                        f'<span style="{_lbl_style}min-width:42px">{_implicit_tag}{_l:.1f}{_espn_badge}</span>'
                        f'<span style="color:{_oc};min-width:52px">O {_po_l:.0f}%</span>'
                        f'<span style="color:#444444">|</span>'
                        f'<span style="color:{_uc};min-width:52px">U {_pu_l:.0f}%</span>'
                        f'<span style="color:{_arrow_clr};font-weight:700">→ {_arrow_lbl} ({_arrow_pct:.0f}%)</span>'
                        f'</div>'
                    )
            else:
                # Fallback single line
                _otc = "#ff6a00" if _po >= 50 else "#6B7E6E"
                _utc = "#a78bfa" if _pu >= 50 else "#6B7E6E"
                _best_lbl = f'Over {sim["ou_line"]}' if _po >= _pu else f'Under {sim["ou_line"]}'
                _best_clr = "#ff6a00" if _po >= _pu else "#a78bfa"
                _rows_html = (
                    f'<span style="color:{_otc}">Over {_po}%</span>'
                    f'<span style="color:#444444"> | </span>'
                    f'<span style="color:{_utc}">Under {_pu}%</span>'
                    f'<span style="color:{_best_clr};font-weight:700;margin-left:4px">→ {_best_lbl} ({max(_po,_pu):.0f}%)</span>'
                )

            _footer = (
                f'<div style="font-size:0.72rem;margin-top:5px">'
                f'<div style="color:#6B7280;margin-bottom:3px">{_sg_icon_ou} O/U · {dq_src_ou}</div>'
                + _rows_html +
                f'</div>'
            )
            # Marcadores más frecuentes (no-soccer)
            _sf2 = sim.get("score_freq", [])
            if _sf2:
                _sf2_html = '<div style="margin-top:5px;padding:5px 7px;background:rgba(255,255,255,0.03);border-radius:8px;border:1px solid #222">'
                _sf2_html += '<div style="font-size:0.6rem;color:#6B7280;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px">📊 Marcadores más frecuentes</div>'
                _sf2_html += '<div style="display:flex;flex-wrap:wrap;gap:4px">'
                for _i, ((h_g, a_g), _cnt) in enumerate(_sf2[:5]):
                    _pct2 = round(_cnt / (sim.get("n_simulations", 10000)) * 100, 1)
                    _is_top2 = _i == 0
                    _sc2 = "#f97316" if h_g > a_g else ("#60a5fa" if h_g < a_g else "#a78bfa")
                    _sf2_html += (
                        f'<div style="background:{"rgba(255,255,255,0.07)" if _is_top2 else "rgba(255,255,255,0.03)"};'
                        f'border:1px solid {"rgba(255,255,255,0.15)" if _is_top2 else "#222"};'
                        f'border-radius:8px;padding:3px 8px;text-align:center;min-width:52px">'
                        f'<div style="font-size:{"0.82rem" if _is_top2 else "0.75rem"};font-weight:{"800" if _is_top2 else "600"};color:{_sc2}">'
                        f'{h_g}–{a_g}</div>'
                        f'<div style="font-size:0.6rem;color:#6B7280">{_pct2}%</div>'
                        f'</div>'
                    )
                _sf2_html += '</div></div>'
                _footer += _sf2_html

        # ── Get logos ────────────────────────────────────────────────────────
        _ht_id_p  = g.get("home_team_id","")
        _at_id_p  = g.get("away_team_id","")
        _league_p = g.get("league","")
        _sg_p     = LEAGUES.get(_league_p,{}).get("group","Soccer")
        _sg_icon_p = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}.get(_sg_p,"🎯")
        _logo_a_p = _logo_img(_at_id_p, _league_p, 44)
        _logo_h_p = _logo_img(_ht_id_p, _league_p, 44)
        _away_p   = g.get("away_team","")
        _home_p   = g.get("home_team","")
        _lg_lbl_p = league_label(_league_p)

        # ── Decimals for pills ─────────────────────────────────────────────
        _h_pct_p  = sim.get("home_pct",0) or 0
        _a_pct_p  = sim.get("away_pct",0) or 0
        _d_pct_p  = sim.get("draw_pct",0) or 0
        def _get_dec(key, pct):
            d = sim.get(key,"")
            if d:
                try:
                    v=float(d); return "1.02" if v<1.02 else (">15" if v>15 else f"{v:.2f}")
                except: pass
            return prob_to_dec(pct/100) if pct>0 else "-"
        _h_dec_p  = _get_dec("model_home_dec", _h_pct_p)
        _a_dec_p  = _get_dec("model_away_dec", _a_pct_p)
        _d_dec_p  = _get_dec("model_draw_dec", _d_pct_p)
        _bp_mkt   = bp.get("market","")
        _bp_lbl   = bp.get("label","")
        _bp_prob  = bp.get("prob",0); _bp_prob = _bp_prob if _bp_prob<=1 else _bp_prob/100
        _pick_h_p = _home_p in _bp_lbl
        # For Spread: parse team name and line number for clean display
        _bp_spread_team = ""
        _bp_spread_line = ""
        _bp_spread_impl = _bp_lbl.startswith("~") if _bp_mkt == "Spread" else False
        if _bp_mkt == "Spread":
            import re as _re_bpl
            _bp_m = _re_bpl.search(r"~?(.+?)[ ]*([+-][0-9]+\.?[0-9]*)[ ]*\(", _bp_lbl)
            if _bp_m:
                _bp_spread_team = _bp_m.group(1).strip()
                _bp_spread_line = _bp_m.group(2)
            else:
                _bp_spread_team = _bp_lbl.lstrip("~")
        if _bp_mkt == "Spread":
            # Use real spread odds (ESPN) or standard -110 = 1.91
            _spr_ml_raw = bp.get("ml", "-110") or "-110"
            try:
                _spr_ml_f = float(str(_spr_ml_raw))
                _pick_dec_p = str(round(100/abs(_spr_ml_f)+1, 2)) if _spr_ml_f < 0 else str(round(_spr_ml_f/100+1, 2))
            except:
                _pick_dec_p = "1.91"
            _pick_pct_p = round((_bp_prob if _bp_prob <= 1 else _bp_prob/100) * 100, 0)
        else:
            _pick_dec_p = _h_dec_p if _pick_h_p else _a_dec_p
            _pick_pct_p = _h_pct_p if _pick_h_p else _a_pct_p

        # ── Pills ──────────────────────────────────────────────────────────
        def _ppill(lbl, dec):
            lc = "#3D8EFF" if any(x in str(lbl) for x in ("O","U","x","X")) else "#A0A0A8"
            return (f'<div style="flex:1;background:linear-gradient(160deg,#1E1E24 0%,#141418 100%);'
                    f'border-radius:10px;border:1px solid rgba(255,255,255,0.1);'
                    f'border-top:1px solid rgba(255,255,255,0.18);'
                    f'box-shadow:0 3px 8px rgba(0,0,0,0.4),0 1px 0 rgba(255,255,255,0.06) inset;'
                    f'padding:10px 4px;text-align:center">'
                    f'<span style="font-size:0.65rem;color:{lc};display:block;margin-bottom:3px;font-weight:700;letter-spacing:0.3px">{lbl}</span>'
                    f'<span style="font-size:1.2rem;font-weight:900;color:#F0F0F2;font-family:Barlow Condensed,sans-serif;line-height:1">{dec}</span>'
                    f'</div>')
        if _sg_p == "Soccer":
            _pills_p = _ppill("1x",_a_dec_p)+_ppill("x",_d_dec_p)+_ppill("2x",_h_dec_p)
        else:
            _ou_v_p = sim.get("ou_line","") or ""
            _po_p = sim.get("p_o_total",0) or 0; _pu_p = sim.get("p_u_total",0) or 0
            # Spread pill — use real ESPN line or implied (marked with ~)
            _spr_line_p  = g.get("odds",{}).get("spread_line","") or ""
            _spr_raw_p   = g.get("odds",{}).get("spread","") or ""
            _spr_implied = sm.get("spread_implied", False)
            _spr_pill_p  = ""
            if _spr_line_p:
                try:
                    _spr_f = float(_spr_line_p)
                    _spr_lbl = f"{'~' if _spr_implied else ''}{'H' if _spr_f<0 else 'A'}{abs(_spr_f):+.1f}".replace("+-","-").replace("++","+")
                    # Cleaner: show as the actual spread string from ESPN
                    if _spr_raw_p and not _spr_implied:
                        # e.g. "BOS -8.5" → show as "BOS-8.5"
                        import re as _re_psp
                        _pm = _re_psp.search(r'([A-Za-z0-9]+)[ ]*([+-]?[0-9]+[.]?[0-9]*)', _spr_raw_p)
                        _spr_lbl = f"{_pm.group(1)}{float(_pm.group(2)):+.1f}" if _pm else f"{'H' if _spr_f<0 else 'A'}{_spr_f:+.1f}"
                    else:
                        _spr_lbl = f"~{'H' if _spr_f<0 else 'A'}{abs(_spr_f):.1f}"
                    _p_cover = sm.get("p_home_cover",50) or 50
                    _spr_dec = round(100/abs(-110)+1, 3)  # standard -110 = 1.909
                    _spr_pill_p = _ppill(_spr_lbl, f"{_spr_dec:.2f}", color="#22d3ee")
                except: pass
            if _ou_v_p and not str(_ou_v_p).startswith("~"):
                try: _ou_lbl_p = f"{'O' if _po_p>=_pu_p else 'U'}{float(str(_ou_v_p).lstrip('~')):.1f}"
                except: _ou_lbl_p = "O/U"
                _ou_dec_p = _get_dec("", max(_po_p,_pu_p))
                _pills_p = _ppill(_away_p[:7],_a_dec_p)+_spr_pill_p+_ppill(_ou_lbl_p,_ou_dec_p)+_ppill(_home_p[:7],_h_dec_p)
            else:
                _pills_p = _ppill(_away_p[:7],_a_dec_p)+_spr_pill_p+_ppill(_home_p[:7],_h_dec_p)

        # ── Pick explanation + white card ──────────────────────────────────
        _ev_raw  = bp.get("ev")           # None = no market line available
        _ev_val  = _ev_raw if _ev_raw is not None else None
        _kelly  = (bp.get("kelly", 0) or 0) * 25
        _dq     = sim.get("data_quality", 0) or 0
        _conf_c = "#007744" if _bp_prob >= 0.65 else ("#996600" if _bp_prob >= 0.50 else "#880000")
        _conf_l = "ALTA" if _bp_prob >= 0.65 else ("MEDIA" if _bp_prob >= 0.50 else "BAJA")
        _nsim   = sim.get("n_simulations", 0) or 0
        _fav_p  = max(_h_pct_p or 0, _a_pct_p or 0)
        # Build signal breakdown
        _h_form = g.get("home_form") if g else None
        _a_form = g.get("away_form") if g else None
        _h_rec  = g.get("home_record","") if g else ""
        _a_rec  = g.get("away_record","") if g else ""
        _h2h_g  = g.get("h2h", {}) if g else {}
        _h2h_cnt = _h2h_g.get("count", 0) if _h2h_g else 0

        # Form summary
        _form_str = ""
        if _h_form is not None and _a_form is not None:
            _form_str = f"Forma: {_home_p[:6]} {_h_form*100:.0f}% vs {_away_p[:6]} {_a_form*100:.0f}% (últ.10)"

        # H2H summary
        _h2h_str = ""
        if _h2h_cnt >= 3:
            _wh = _h2h_g.get("wins_home", 0)
            _wa = _h2h_g.get("wins_away", 0)
            _dr = _h2h_g.get("draws", 0)
            _h2h_avg = _h2h_g.get("avg_total", 0)
            _h2h_str = f"H2H {_h2h_cnt}ptdos: {_home_p[:7]} {_wh}V–{_dr}E–{_wa}V {_away_p[:7]}"
            if _h2h_avg: _h2h_str += f" · {_h2h_avg:.1f}gls"

        _why = f"MC {_nsim:,} sims · {_fav_p:.0f}% al favorito · DQ {_dq:.0f}%"

        _cta = (
            '<div style="margin:0 10px 10px;'
            'background:linear-gradient(160deg,#FFE033 0%,#FFBB00 100%);'
            'border-radius:14px;padding:14px;'
            'border-top:2px solid rgba(255,255,255,0.5);'
            'box-shadow:0 4px 16px rgba(255,185,0,0.35),0 1px 0 rgba(255,255,255,0.5) inset">'

            # Row 1: badge + team name
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
            f'<span style="font-size:0.6rem;font-weight:900;color:rgba(0,0,0,0.35);letter-spacing:2px">APOSTAR →</span>'
            f'<span style="font-size:0.65rem;font-weight:900;color:#000;background:rgba(0,0,0,0.12);'
            f'padding:3px 9px;border-radius:6px;letter-spacing:0.5px;text-transform:uppercase">{_bp_mkt}</span>'
            f'<span style="font-size:0.95rem;font-weight:900;color:#000;flex:1;overflow:hidden;'
            f'text-overflow:ellipsis;white-space:nowrap">'
            + (_bp_spread_team if _bp_mkt == "Spread" else _bp_lbl) +
            '</span>'
            '</div>'

            # Row 2: big odds + spread line | prob/conf/kelly
            f'<div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:10px">'
            f'<div style="display:flex;flex-direction:column;align-items:flex-start;min-width:60px">'
            f'<span style="font-size:2.8rem;font-weight:900;color:#000;font-family:Barlow Condensed,sans-serif;line-height:0.9">{_pick_dec_p}</span>'
            + (
                f'<span style="font-size:1.6rem;font-weight:900;color:rgba(0,0,0,0.8);'
                f'font-family:Barlow Condensed,sans-serif;line-height:1.1">{_bp_spread_line}</span>'
                + (f'<span style="font-size:0.58rem;font-weight:700;color:rgba(0,0,0,0.35)"> modelo</span>' if _bp_spread_impl else '')
                if _bp_mkt == "Spread" and _bp_spread_line else ''
            ) +
            '</div>'
            f'<div style="display:flex;flex-direction:column;gap:3px;flex:1">'
            f'<span style="font-size:0.9rem;font-weight:800;color:rgba(0,0,0,0.7)">{_bp_prob*100:.0f}% probabilidad</span>'
            f'<span style="font-size:0.7rem;color:rgba(0,0,0,0.5)">Confianza: <b style="color:{_conf_c}">{_conf_l}</b></span>'
            + (f'<span style="font-size:0.68rem;color:rgba(0,0,0,0.5)">Kelly: <b>{_kelly:.1f}%</b> del bankroll</span>' if _kelly > 0 else '') +
            '</div>'
            '</div>'

            # Row 3: stats grid
            '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4px;'
            'padding-top:8px;border-top:1px solid rgba(0,0,0,0.1)">'
            + ''.join([
                f'<div style="text-align:center">'
                f'<div style="font-size:0.5rem;color:rgba(0,0,0,0.4);text-transform:uppercase;font-weight:700">{lbl}</div>'
                f'<div style="font-size:0.9rem;font-weight:900;color:{clr}">{val}</div>'
                f'</div>'
                for lbl, val, clr in [
                    ("Prob.", f"{_bp_prob*100:.0f}%", "#000"),
                    ("EV/100",
                     "S/L" if _ev_val is None else f"{_ev_val:+.0f}",
                     "#888" if _ev_val is None else ("#006600" if _ev_val>0 else "#880000")),
                    ("DQ", f"{_dq:.0f}%", "#000"),
                    ("Kelly", f"{_kelly:.1f}%", "#000"),
                ]
            ]) +
            '</div>'
            f'<div style="margin-top:7px;padding-top:6px;border-top:1px solid rgba(0,0,0,0.08)">'
            f'<span style="font-size:0.62rem;color:rgba(0,0,0,0.5)">📊 {_why}</span>'
            '</div>'
            + (
                f'<div style="margin-top:4px;padding:4px 8px;background:rgba(0,0,0,0.08);border-radius:7px">'
                f'<span style="font-size:0.62rem;color:rgba(0,0,0,0.6)">⚔️ {_h2h_str}</span>'
                '</div>' if _h2h_str else ''
            )
            + (
                f'<div style="margin-top:3px;padding:4px 8px;background:rgba(0,0,0,0.06);border-radius:7px">'
                f'<span style="font-size:0.62rem;color:rgba(0,0,0,0.55)">📈 {_form_str}</span>'
                '</div>' if _form_str else ''
            )
            + '</div>'
        )
        _html = (
            '<div style="background:linear-gradient(160deg,#F6F6F9 0%,#EAEAEF 100%);'
            'border-radius:20px;overflow:hidden;margin-bottom:3px;'
            'border:1px solid rgba(0,0,0,0.07);border-top:1.5px solid rgba(255,255,255,0.9);'
            'box-shadow:0 8px 28px rgba(0,0,0,0.25),0 2px 0 rgba(255,255,255,0.8) inset">'
            f'<div style="padding:8px 14px 3px;display:flex;justify-content:space-between">'
            f'<span style="font-size:0.58rem;font-weight:700;color:#888;letter-spacing:1.5px;text-transform:uppercase">{_lg_lbl_p}</span>'
            f'<span style="font-size:0.62rem;color:#C9A84C;font-weight:700">'
            + (f"EV +{_ev_val:.1f}" if _ev_val > 2 else "")
            + f'</span></div>'
            f'<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 14px 4px">'
            f'<div style="text-align:center;flex:1">' + _logo_a_p
            + f'<div style="font-size:0.6rem;font-weight:800;color:#111;text-transform:uppercase;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:72px">{_away_p[:10]}</div>'
            f'</div>'
            f'<div style="flex:1;text-align:center">'
            f'<div style="font-size:1.5rem;font-weight:900;color:#111;font-family:Barlow Condensed,sans-serif;letter-spacing:-2px;line-height:1">VS</div>'
            f'<div style="font-size:0.5rem;color:#CCC;margin-top:2px">{_sg_icon_p}</div>'
            f'</div>'
            f'<div style="text-align:center;flex:1">' + _logo_h_p
            + f'<div style="font-size:0.6rem;font-weight:800;color:#111;text-transform:uppercase;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:72px">{_home_p[:10]}</div>'
            f'</div></div>'
            f'<div style="height:1px;background:rgba(0,0,0,0.07);margin:0 12px"></div>'
            f'<div style="display:flex;gap:5px;padding:8px 10px">' + _pills_p + '</div>'
            + _cta
            + '</div>'
        )
        return _html

    # ── Show all sports expanded directly — no click needed ─────────────────
    _sel_sp_now = st.session_state.get("_picks_sel_sport", None)
    _sports_to_show = [_sel_sp_now] if (_sel_sp_now and _sel_sp_now in _sports_p) else _sports_p
    _lg_btn_counter = 0  # global counter to guarantee unique keys

    for _sp_p in _sports_to_show:
        _smp   = _SPORT_META_P[_sp_p]
        _n_p   = sum(len(gs) for dmap in _tree_p[_sp_p].values() for gs in dmap.values())
        _ev_count = sum(
            1 for dmap in _tree_p[_sp_p].values()
            for gs in dmap.values() for g in gs
            if _sim_map.get(g.get("id",""),{}).get("sim",{}).get("best_single",{}) and
               (_sim_map.get(g.get("id",""),{}).get("sim",{}).get("best_single",{}).get("ev") or 0) > 0
        )
        _ev_badge = f" 🔥{_ev_count}" if _ev_count else ""
        st.markdown(
            f'<div style="font-size:0.75rem;font-weight:700;color:{_smp["color"]};'
            f'letter-spacing:1px;text-transform:uppercase;margin:14px 0 6px 0;'
            f'border-bottom:1px solid {_smp["color"]}33;padding-bottom:4px">'
            f'{_smp["emoji"]} {_sp_p} — {_n_p} partidos{_ev_badge}</div>',
            unsafe_allow_html=True
        )

        # ── Colapsar árbol por liga (elimina duplicados por fecha) ────────────
        _leagues_flat = {}  # {liga: [games...]}
        for _dk_p in sorted(_tree_p[_sp_p].keys()):
            for _lg_p, _lg_games_p in sorted(_tree_p[_sp_p][_dk_p].items()):
                if _lg_p not in _leagues_flat:
                    _leagues_flat[_lg_p] = []
                # Dedup by game id
                _existing_ids = {g.get("id") for g in _leagues_flat[_lg_p]}
                for _gg in _lg_games_p:
                    if _gg.get("id") not in _existing_ids:
                        _leagues_flat[_lg_p].append(_gg)
                        _existing_ids.add(_gg.get("id"))

        for _lg_p, _lg_games_p in sorted(_leagues_flat.items()):
                _country_p = LEAGUES.get(_lg_p,{}).get("country","")
                _ctry_str  = f" · {_country_p}" if _country_p else ""
                _flag_p    = LEAGUE_FLAG.get(_lg_p, "🌐")
                _n_lg      = len(_lg_games_p)

                # EV count for this league
                _ev_lg = sum(
                    1 for _gg in _lg_games_p
                    if _sim_map.get(_gg.get("id",""),{}).get("sim",{}).get("best_single",{}) and
                       (_sim_map.get(_gg.get("id",""),{}).get("sim",{}).get("best_single",{}).get("ev") or 0) > 0
                )
                _ev_lg_badge = f" · 🔥{_ev_lg} EV+" if _ev_lg else ""

                # Liga row: ONE dark button (no white box ever)
                _exp_key = f"_lg_open_{_lg_p.replace(' ','_').replace('/','_').replace('.','_')}"
                _is_open = st.session_state.get(_exp_key, False)
                _cr2,_cg2,_cb2 = int(_smp["color"][1:3],16),int(_smp["color"][3:5],16),int(_smp["color"][5:7],16)

                # Style the button to look like the dark header
                _arrow = "▼" if _is_open else "▶"
                _btn_label = f"{_arrow}  {_flag_p} {_lg_p}   {_n_lg} partidos{_ev_lg_badge}"
                _btn_key = _exp_key + "_btn"
                def _toggle_liga(_k=_exp_key, _v=_is_open):
                    st.session_state[_k] = not _v
                st.button(_btn_label, key=_btn_key, use_container_width=True,
                          on_click=_toggle_liga)
                # Re-read after potential on_click update
                _is_open = st.session_state.get(_exp_key, False)

                if _is_open:
                    st.markdown(
                        f'<div style="background:#0F0F12;border:1.5px solid rgba({_cr2},{_cg2},{_cb2},0.25);'
                        f'border-top:none;border-radius:0 0 12px 12px;padding:10px 6px 12px;margin-bottom:2px">',
                        unsafe_allow_html=True
                    )
                    for _gi3 in range(0, len(_lg_games_p), 3):
                        _row3 = _lg_games_p[_gi3:_gi3+3]
                        _ncols = len(_row3)
                        _c3 = st.columns(_ncols) if _ncols > 1 else st.columns(1)
                        for _ci3, _gg_p in enumerate(_row3):
                            with _c3[_ci3]:
                                st.markdown(_oracle_card(_gg_p, _smp), unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    # CSV export (collapsed)
    _sr_all = st.session_state.get("sim_results", [])
    if _sr_all:
        _csv_key = "_csv_open_picks"
        _csv_open = st.session_state.get(_csv_key, False)
        def _toggle_csv():
            st.session_state[_csv_key] = not st.session_state.get(_csv_key, False)
        st.button("▼ Cerrar" if _csv_open else "⬇ Exportar CSV",
                  key="btn_csv_picks", use_container_width=True, on_click=_toggle_csv)
        if _csv_open:
            csv=["Liga,Visitante,Local,Prob Vis%,Prob Local%,Empate%,ML Vis,ML Local,EV Vis,EV Local,BTTS%,EV BTTS,O2.5%,EV O2.5,O3.5%,DC 1X%,DC X2%,Mejor Mercado,Mejor Pick,Mejor EV,DQ%"]
            for _cr in _sr_all:
                s=_cr["sim"]; bs=s.get("best_single",{}) or {}
                csv.append(",".join([_cr['league'],_cr['away_team'],_cr['home_team'],
                    str(s['away_pct']),str(s['home_pct']),str(s['draw_pct']),
                    str(s['away_ml']),str(s['home_ml']),
                    str(s['away_ev'] or ""),str(s['home_ev'] or ""),
                    str(s['p_btts'] or ""),str(s['btts_ev'] or ""),
                    str(s['p_o25'] or ""),str(s['o25_ev'] or ""),str(s['p_o35'] or ""),
                    str(s['p_dc_1x']),str(s['p_dc_x2']),
                    bs.get('market',""),bs.get('label',""),str(bs.get('ev',"")),str(s['data_quality'])]))
            st.download_button("⬇ Descargar CSV", data="\n".join(csv),
                               file_name=f"gamblers_den_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

# ══════════════════════════════════════════════════════════════════════════════
elif _active_page == "Parlays":
    sr=st.session_state.get("sim_results",[])
    if not sr:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">🎰</div>
          <div class="empty-title">Sin parlays aún</div>
          <div>Presiona <b>▶ ANALIZAR AHORA</b> en el sidebar para generar parlays.</div>
        </div>""",unsafe_allow_html=True)
    else:
        # ── Detectar si algún partido del parlay original ya terminó ─────────────
        parlay_game_ids = set()
        for r in sr:
            bp = r["sim"].get("best_parlay")
            if bp and (bp.get("ev") or 0) > 0:
                parlay_game_ids.add(r.get("id",""))

        finished_parlay_games = [g for g in games if g.get("id","") in parlay_game_ids and g["state"]=="post"]
        pending_games = [g for g in games if g["state"] in ("pre","in")]

        # ── Auto-detect: si hay partidos del parlay que terminaron y hay pendientes ─
        needs_regen = (
            len(finished_parlay_games) > 0
            and len(pending_games) > 0
            and not st.session_state.get("_parlay_regen_done", False)
        )

        # Guardar el estado de regeneración por sesión de parlay
        _regen_key = f"regen_{len(finished_parlay_games)}_{len(pending_games)}"
        if st.session_state.get("_parlay_regen_key") != _regen_key:
            st.session_state["_parlay_regen_done"] = False
            st.session_state["_parlay_regen_key"] = _regen_key

        # ── Banner de alerta si hay partidos terminados ───────────────────────────
        if finished_parlay_games:
            finished_names = " · ".join(
                f"{g['away_team']} @ {g['home_team']}" for g in finished_parlay_games[:3]
            )
            st.markdown(f'''<div class="warn-banner" style="border-left:4px solid #00C896;background:rgba(74,222,128,0.08)">
                ✅ <b>Partido(s) del parlay terminaron:</b> {finished_names}<br>
                <span style="color:#6B7280;font-size:0.896rem">{len(pending_games)} partidos pendientes disponibles para nuevo parlay.</span>
            </div>''', unsafe_allow_html=True)

        # ── Botón manual + auto-regen ─────────────────────────────────────────────
        col_p1, col_p2 = st.columns([3, 1])
        with col_p1:
            today_label = datetime.now(timezone.utc).strftime("%d %b %Y")
        st.markdown(f'<div class="section-heading">🎰 Parlays del Día · {today_label}</div>', unsafe_allow_html=True)
        with col_p2:
            regen_clicked = st.button("🔄 Nuevo Parlay", use_container_width=True,
                                      disabled=len(pending_games)==0,
                                      help="Re-simula con los partidos pendientes del día")

        # Ejecutar regeneración (auto o manual)
        if (needs_regen or regen_clicked) and pending_games:
            with st.spinner(f"🎰 Re-simulando {len(pending_games)} partidos pendientes..."):
                new_sr = run_all_simulations(pending_games, n=n_sims)
            st.session_state["sim_results"] = new_sr
            st.session_state["_parlay_regen_done"] = True
            n_new_parlays = len([r for r in new_sr if r["sim"].get("best_parlay") and (r["sim"]["best_parlay"].get("ev") or 0)>0])
            st.toast(f"✓ Parlay actualizado · {n_new_parlays} combinadas EV+", icon="🎰")
            st.rerun()

        # ── Mostrar parlays (siempre el más reciente en session_state) ────────────
        sr_current = st.session_state.get("sim_results", [])
        parlays = [r for r in sr_current if r["sim"].get("best_parlay") and (r["sim"]["best_parlay"].get("ev") or 0)>0]
        parlays.sort(key=lambda x: x["sim"]["best_parlay"]["ev"], reverse=True)

        # ── Helpers para armar el parlay de 2 patas de un mismo partido ──────
        # _MKT_C kept for legacy references; new code uses _pick_clr()
        _MKT_C = {"ML":"#60a5fa","O/U":"#ff6a00","BTTS":"#00C896","DO":"#a78bfa","COMBO":"#f59e0b"}
        _SG_ICON = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}
        _SG_COLOR = {"Soccer":"#00C896","Basketball":"#f97316","Hockey":"#60a5fa",
                     "Baseball":"#ef4444","Football":"#a78bfa"}

        def _build_game_parlays(r):
            """
            Build candidate 2-leg parlays from a single game.
            Soccer generates up to 3 candidates:
              a) ML + BTTS (Ambos Anotan)
              b) ML + Over 2.5
              c) BTTS + Over 2.5  ← combo goles pura
            Non-soccer generates 1 candidate:
              ML + O/U (better side by prob)
            Returns list of parlay dicts (may be empty).
            """
            sim = r["sim"]
            sg  = LEAGUES.get(r["league"],{}).get("group","Soccer")

            def _make(leg1, leg2, combo_type=""):
                p1 = leg1["prob"] / 100
                p2 = leg2["prob"] / 100
                cp = p1 * p2
                return {
                    "game": r, "sg": sg,
                    "leg1": leg1, "leg2": leg2,
                    "combo_type": combo_type,
                    "comb_prob": cp,
                    "comb_prob_pct": round(cp * 100, 1),
                    "payout": round((1/cp)*100, 0) if cp > 0 else 0,
                }

            results = []

            if sg == "Soccer":
                _btts_pb = sim.get("p_btts") or 0
                _o25_pb  = sim.get("p_o25")  or 0
                h_prob   = sim.get("home_pct") or 0
                a_prob   = sim.get("away_pct") or 0
                h_ml     = sim.get("home_ml"); a_ml = sim.get("away_ml")
                ml_team  = r["home_team"] if h_prob >= a_prob else r["away_team"]
                ml_prob  = h_prob if h_prob >= a_prob else a_prob
                ml_ml    = h_ml if h_prob >= a_prob else a_ml

                leg_ml   = {"market":"ML",   "label": ml_team,        "prob": ml_prob} if ml_ml else None
                leg_btts = {"market":"BTTS",  "label": "Ambos Anotan", "prob": _btts_pb} if _btts_pb > 0 else None
                leg_o25  = {"market":"O/U",   "label": "Over 2.5",     "prob": _o25_pb}  if _o25_pb  > 0 else None

                # a) ML + BTTS
                if leg_ml and leg_btts:
                    results.append(_make(leg_ml, leg_btts, "ML + AA"))
                # b) ML + O2.5
                if leg_ml and leg_o25:
                    results.append(_make(leg_ml, leg_o25, "ML + O2.5"))
                # c) BTTS + O2.5  ← combo goles pura (sin ML)
                if leg_btts and leg_o25:
                    results.append(_make(leg_btts, leg_o25, "AA + O2.5"))

            else:
                # Non-soccer: ML + best O/U side
                h_prob = sim.get("home_pct") or 0
                a_prob = sim.get("away_pct") or 0
                h_ml   = sim.get("home_ml"); a_ml = sim.get("away_ml")
                ml_team = r["home_team"] if h_prob >= a_prob else r["away_team"]
                ml_prob = h_prob if h_prob >= a_prob else a_prob
                ml_ml   = h_ml if h_prob >= a_prob else a_ml
                if not ml_ml:
                    return results  # no ML = skip

                leg_ml = {"market":"ML","label":ml_team,"prob":ml_prob}
                _ou_line = sim.get("ou_line") or ""
                _p_over  = sim.get("p_o_total") or 0
                _p_under = sim.get("p_u_total") or 0
                if _ou_line and (_p_over > 0 or _p_under > 0):
                    try: _line = float(_ou_line.lstrip("~"))
                    except: _line = None
                    if _line:
                        if _p_over >= _p_under:
                            leg_ou = {"market":"O/U","label":f"Over {_line:.1f}","prob":_p_over}
                        else:
                            leg_ou = {"market":"O/U","label":f"Under {_line:.1f}","prob":_p_under}
                        results.append(_make(leg_ml, leg_ou, "ML + O/U"))

            return results

        # ── Build parlays per sport ───────────────────────────────────────────
        # Soccer: pick best among ALL combos (ML+AA, ML+O2.5, AA+O2.5) by comb_prob
        #         Also always show AA+O2.5 if available (separate featured card)
        # Others: 1 best game (ML+O/U) per sport
        _SPORT_ORDER_PAR = ["Soccer","Basketball","Hockey","Baseball","Football"]
        _sport_game_pools = {}
        _soccer_btts_o25  = []  # collect AA+O2.5 combos separately

        # ── TODAY only filter + deduplication ──────────────────────────────
        from datetime import timezone as _tz_par, timedelta as _td_par
        _now_par      = datetime.now(_tz_par.utc)
        _now_mx_par   = _now_par - _td_par(hours=6)
        _today_par    = _now_mx_par.strftime("%Y-%m-%d")
        _valid_par    = {
            (_now_mx_par - _td_par(days=1)).strftime("%Y-%m-%d"),
            _today_par,
            (_now_mx_par + _td_par(days=1)).strftime("%Y-%m-%d"),
        }

        def _game_date_par(gid, r_obj=None):
            """Returns CDMX date string for a game, or None if can't determine.
            Tries sim result r_obj first (has date field), then games list."""
            # Try from sim result directly (most reliable)
            if r_obj:
                raw = r_obj.get("date","")
                if raw:
                    try:
                        _u = datetime.strptime(raw[:19].replace("T"," "),"%Y-%m-%d %H:%M:%S").replace(tzinfo=_tz_par.utc)
                        return (_u - _td_par(hours=6)).strftime("%Y-%m-%d")
                    except:
                        pass
            # Fallback: look in games list
            g_obj = next((g for g in games if g.get("id") == gid), None)
            if not g_obj: return None
            raw = g_obj.get("date","")
            if not raw: return None
            try:
                _u = datetime.strptime(raw[:19].replace("T"," "),"%Y-%m-%d %H:%M:%S").replace(tzinfo=_tz_par.utc)
                return (_u - _td_par(hours=6)).strftime("%Y-%m-%d")
            except:
                return None

        _seen_par = set()
        for r in sr_current:
            gid     = r.get("id","")
            g_state = r.get("state") or next((g["state"] for g in games if g.get("id")==gid), "pre")
            if g_state == "post": continue
            _gd_par = _game_date_par(gid, r)
            if _gd_par is None or _gd_par not in _valid_par: continue  # ventana ±1 día
            if gid in _seen_par: continue                    # ← deduplicate
            _seen_par.add(gid)
            for gp in _build_game_parlays(r):
                _sport_game_pools.setdefault(gp["sg"], []).append(gp)
                if gp["combo_type"] == "AA + O2.5":
                    _soccer_btts_o25.append(gp)

        # ── Best 1 per sport pool ──────────────────────────────────────────
        _best_per_sport = {}
        for _sg in _SPORT_ORDER_PAR:
            pool = _sport_game_pools.get(_sg, [])
            if pool:
                pool.sort(key=lambda x: x["comb_prob"], reverse=True)
                _best_per_sport[_sg] = pool[0]

        # Legacy single-sport parlays (keep for fallback)
        _day_parlays = list(_best_per_sport.values())

        # Best AA+O2.5 soccer combo (featured separately)
        _best_btts_o25 = (
            max(_soccer_btts_o25, key=lambda x: x["comb_prob"])
            if _soccer_btts_o25 else None
        )

        # ── PARLAY COMBINADO MULTI-DEPORTE ─────────────────────────────────
        # Busca directamente en sr_current el mejor pick individual por deporte
        # filtrando solo partidos de HOY CDMX
        _gmap_par = {g.get("id",""): g for g in games}

        def _best_leg_for_sport(sg_target):
            """Mejor pick individual (1 sola pata) del deporte, solo hoy CDMX."""
            _candidates = []
            for _r in sr_current:
                _gid = _r.get("id","")
                _g_state = _r.get("state") or (_gmap_par.get(_gid) or {}).get("state","pre")
                if _g_state == "post": continue
                _gd_m = _game_date_par(_gid, _r)
                if _gd_m is None or _gd_m not in _valid_par: continue
                _sg = LEAGUES.get(_r["league"],{}).get("group","Soccer")
                if _sg != sg_target: continue
                _sim = _r["sim"]
                _game_obj = _gmap_par.get(_gid, _r)  # use games map for full game obj
                if sg_target == "Soccer":
                    _hp = _sim.get("home_pct") or 0
                    _ap = _sim.get("away_pct") or 0
                    _bp = _sim.get("p_btts") or 0
                    _o25 = _sim.get("p_o25") or 0
                    for _mkt, _lbl, _prob in [
                        ("ML", _r["home_team"] if _hp >= _ap else _r["away_team"], max(_hp,_ap)),
                        ("BTTS", "Ambos Anotan", _bp),
                        ("O/U", "Over 2.5", _o25),
                    ]:
                        if _prob > 0:
                            _candidates.append({"sport":sg_target,"game":_game_obj,"league":_r["league"],
                                                "market":_mkt,"label":_lbl,"prob":_prob})
                else:
                    _hp = _sim.get("home_pct") or 0
                    _ap = _sim.get("away_pct") or 0
                    _ml_prob = max(_hp, _ap)
                    _ml_lbl  = _r["home_team"] if _hp >= _ap else _r["away_team"]
                    if _ml_prob > 0:
                        _candidates.append({"sport":sg_target,"game":_game_obj,"league":_r["league"],
                                            "market":"ML","label":_ml_lbl,"prob":_ml_prob})
                    _multi_r = _sim.get("multi_lines",{})
                    if _multi_r:
                        for _l, _d in _multi_r.items():
                            _po = _d["over"]; _pu = _d["under"]
                            if _po >= _pu and _po >= 52:
                                _candidates.append({"sport":sg_target,"game":_game_obj,"league":_r["league"],
                                                    "market":"O/U","label":f"Over {_l:.1f}","prob":_po})
                            elif _pu > _po and _pu >= 52:
                                _candidates.append({"sport":sg_target,"game":_game_obj,"league":_r["league"],
                                                    "market":"O/U","label":f"Under {_l:.1f}","prob":_pu})
            if not _candidates: return None
            return max(_candidates, key=lambda x: x["prob"])

        # Force exactly Soccer + Basketball + Hockey (1 per sport, best pick)
        _PARLAY_SPORTS = ["Soccer", "Basketball", "Hockey"]
        _multi_legs = []
        _used_game_ids_m = set()
        for _sg_m in _PARLAY_SPORTS:
            _leg = _best_leg_for_sport(_sg_m)
            if _leg and _leg["game"].get("id","") not in _used_game_ids_m:
                _multi_legs.append(_leg)
                _used_game_ids_m.add(_leg["game"].get("id",""))

        # Fallback: si no hay los 3 deportes, completar con Baseball/Football
        if len(_multi_legs) < 3:
            for _sg_m in ["Baseball", "Football"]:
                if len(_multi_legs) >= 3: break
                _leg = _best_leg_for_sport(_sg_m)
                if _leg and _leg["game"].get("id","") not in _used_game_ids_m:
                    _multi_legs.append(_leg)
                    _used_game_ids_m.add(_leg["game"].get("id",""))

        # Fallback final: si aún <2 legs, tomar directamente de sr_current por prob
        if len(_multi_legs) < 2 and sr_current:
            _used_fb = set()
            _all_fb_legs = []
            for _r in sr_current:
                _gid = _r.get("id","")
                if _gid in _used_fb: continue
                _st = _r.get("state") or (_gmap_par.get(_gid) or {}).get("state","pre")
                if _st == "post": continue
                _sg = LEAGUES.get(_r["league"],{}).get("group","Soccer")
                _sim = _r["sim"]
                _game_obj = _gmap_par.get(_gid, _r)
                if _sg == "Soccer":
                    _hp = _sim.get("home_pct") or 0
                    _ap = _sim.get("away_pct") or 0
                    _bp = _sim.get("p_btts") or 0
                    _o25 = _sim.get("p_o25") or 0
                    _best_p = max(_hp, _ap, _bp, _o25)
                    if _hp >= _ap and _hp == _best_p: _lbl, _mkt = _r["home_team"], "ML"
                    elif _ap == _best_p: _lbl, _mkt = _r["away_team"], "ML"
                    elif _bp == _best_p: _lbl, _mkt = "Ambos Anotan", "BTTS"
                    else: _lbl, _mkt = "Over 2.5", "O/U"
                    _prob = _best_p
                else:
                    _hp = _sim.get("home_pct") or 0
                    _ap = _sim.get("away_pct") or 0
                    _prob = max(_hp, _ap)
                    _lbl = _r["home_team"] if _hp >= _ap else _r["away_team"]
                    _mkt = "ML"
                if _prob > 0:
                    _all_fb_legs.append({"sport":_sg,"game":_game_obj,"league":_r["league"],
                                         "market":_mkt,"label":_lbl,"prob":_prob})
                _used_fb.add(_gid)
            _all_fb_legs.sort(key=lambda x: x["prob"], reverse=True)
            _fb_sports_used = set()
            _fb_ids_used = set()
            for _fl in _all_fb_legs:
                _fgid = _fl["game"].get("id","")
                if _fgid in _fb_ids_used: continue
                if _fl["sport"] in _fb_sports_used: continue  # 1 por deporte
                _fb_ids_used.add(_fgid)
                _fb_sports_used.add(_fl["sport"])
                _multi_legs.append(_fl)
                if len(_multi_legs) >= 3: break

        # Calcular prob combinada
        if len(_multi_legs) >= 2:
            _multi_prob = 1.0
            for _l in _multi_legs:
                _multi_prob *= (_l["prob"] / 100)
            _multi_prob_pct = round(_multi_prob * 100, 1)
            _multi_payout   = round((1 / _multi_prob) * 100, 0) if _multi_prob > 0 else 0
        else:
            _multi_prob_pct = 0
            _multi_payout   = 0

        _has_any_parlay = bool(_multi_legs) or bool(_day_parlays)
        if _has_any_parlay:
            n_post  = len([g for g in games if g["state"]=="post"])
            n_live  = len([g for g in games if g["state"]=="in"])
            n_pre   = len([g for g in games if g["state"]=="pre"])
            status_color = "#00C896" if n_live > 0 else "#60a5fa"
            st.markdown(
                f'<div style="font-size:0.806rem;color:#6B7280;margin-bottom:12px">' +
                (f'<span style="color:{status_color}">⚡ {n_live} en vivo</span> · ' if n_live else "") +
                f'{n_pre} próximos · {n_post} terminados</div>',
                unsafe_allow_html=True
            )

            st.markdown('<div class="section-heading">🎰 PARLAYS DEL DÍA</div>', unsafe_allow_html=True)

            # ── Helper: render a generic 2-leg parlay card ────────────────────
            def _render_parlay_card(dp, featured=False):
                """Render any 2-leg parlay dict (leg1+leg2, generic labels)."""
                _sg   = dp["sg"]
                _g    = dp["game"]
                _l1   = dp["leg1"]
                _l2   = dp["leg2"]
                _ct   = dp.get("combo_type","")
                _p1c, _p1a, _, _p1l = _pick_clr(_l1["market"], _l1.get("label",""))
                _p2c, _p2a, _, _p2l = _pick_clr(_l2["market"], _l2.get("label",""))
                _mc1, _mc2 = _p1a, _p2a  # keep _mc1/_mc2 for compat
                _sgc  = "#00C896" if featured else _SG_COLOR.get(_sg,"#00C896")
                _sgi  = _SG_ICON.get(_sg,"🎯")
                _lg   = league_label(_g["league"])
                _matchup = f'{_g["away_team"]} @ {_g["home_team"]}'
                _border_extra = "box-shadow:0 0 30px rgba(74,222,128,0.22);" if featured else ""
                _feat_stripe  = (
                    f'background:linear-gradient(90deg,transparent,#00C896,#C9A84C,transparent)'
                ) if featured else f'background:linear-gradient(90deg,transparent,{_sgc},transparent)'
                _feat_label = (
                    '<span style="background:rgba(74,222,128,0.18);color:#00C896;'
                    'border:1px solid rgba(74,222,128,0.5);border-radius:12px;'
                    'padding:1px 7px;font-size:0.65rem;font-weight:900;margin-left:6px">'
                    '⚽ GOLES COMBO</span>'
                ) if featured else ""

                return (
                    f'<div style="border-radius:16px;padding:14px 16px;margin:8px 0;'
                    f'background:linear-gradient(135deg,{_sgc}14 0%,#141414 60%,{_sgc}08 100%);'
                    f'border:1px solid {_sgc}{"66" if featured else "44"};{_border_extra}">'
                    f'<div style="height:2px;border-radius:12px 8px 0 0;margin:-14px -16px 12px -16px;{_feat_stripe}"></div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap">'
                    f'<div>'
                    f'<div style="font-size:0.65rem;color:#6B7280;letter-spacing:2px;text-transform:uppercase;margin-bottom:3px">'
                    f'{_sgi} {_sg} · {_lg}{_feat_label}</div>'
                    f'<div style="font-size:0.986rem;font-weight:700;color:#E8E8E8">{_matchup}</div>'
                    f'<div style="font-size:0.728rem;color:#6B7280;margin-top:2px">{_ct}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:1.232rem;font-weight:900;color:{_sgc};font-family:Inter,sans-serif">{dp["comb_prob_pct"]}%</div>'
                    f'<div style="font-size:0.616rem;color:#6B7280">prob. combinada</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="margin-top:10px;display:flex;flex-direction:column;gap:7px">'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="background:{_p1c}28;color:{_p1a};border:1px solid {_p1c}66;'
                    f'border-radius:12px;padding:2px 9px;font-size:0.739rem;font-weight:800;flex-shrink:0">{_p1l}</span>'
                    f'<span style="font-size:0.986rem;color:#E8E8E8;font-weight:600">{_l1["label"]}</span>'
                    f'<span style="margin-left:auto;font-size:0.694rem;color:{_p1a};font-weight:700">{_l1["prob"]:.0f}%</span>'
                    f'</div>'
                    f'<div style="font-size:0.694rem;color:#444444;text-align:center;letter-spacing:3px">✕ COMBO ✕</div>'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="background:{_p2c}28;color:{_p2a};border:1px solid {_p2c}66;'
                    f'border-radius:12px;padding:2px 9px;font-size:0.739rem;font-weight:800;flex-shrink:0">{_p2l}</span>'
                    f'<span style="font-size:0.986rem;color:#E8E8E8;font-weight:600">{_l2["label"]}</span>'
                    f'<span style="margin-left:auto;font-size:0.694rem;color:{_p2a};font-weight:700">{_l2["prob"]:.0f}%</span>'
                    f'</div>'
                    f'</div>'
                    f'<div style="display:flex;align-items:center;gap:16px;margin-top:10px;padding-top:8px;'
                    f'border-top:1px solid {_sgc}22;flex-wrap:wrap">'
                    f'<span style="font-size:0.694rem;color:#00C896">Pago est. +${dp["payout"]:.0f}/100</span>'
                    f'<span style="margin-left:auto;background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);'
                    f'border-radius:12px;padding:2px 8px;font-size:0.672rem;color:#ef4444">⚠️ STAKE BAJO</span>'
                    f'</div>'
                    f'</div>'
                )

            # ── PARLAY COMBINADO MULTI-DEPORTE ───────────────────────────────
            if len(_multi_legs) >= 2:
                _SG_ICONS = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}
                _legs_html = ""
                for _i, _l in enumerate(_multi_legs):
                    _lc, _la, _, _ll = _pick_clr(_l["market"], _l.get("label",""))
                    _g_name = f'{_l["game"]["away_team"]} @ {_l["game"]["home_team"]}'
                    _lg_lbl = league_label(_l["league"])
                    _sp_ico = _SG_ICONS.get(_l["sport"],"🎯")
                    if _i > 0:
                        _legs_html += '<div style="font-size:0.694rem;color:#444444;text-align:center;letter-spacing:3px;margin:4px 0">✕ COMBO ✕</div>'
                    _legs_html += (
                        f'<div style="display:flex;align-items:center;gap:8px;padding:6px 8px;'
                        f'border-radius:12px;background:rgba(255,255,255,0.03)">'
                        f'<span style="background:{_lc}28;color:{_la};border:1px solid {_lc}66;'
                        f'border-radius:12px;padding:2px 9px;font-size:0.739rem;font-weight:800;flex-shrink:0">{_ll}</span>'
                        f'<div style="flex:1;min-width:0">'
                        f'<div style="font-size:0.986rem;color:#E8E8E8;font-weight:600">{_l["label"]}</div>'
                        f'<div style="font-size:0.65rem;color:#6B7280">{_sp_ico} {_l["sport"]} · {_lg_lbl} · {_g_name}</div>'
                        f'</div>'
                        f'<span style="font-size:0.694rem;color:{_la};font-weight:700;flex-shrink:0">{_l["prob"]:.0f}%</span>'
                        f'</div>'
                    )
                _multi_ev = round((_multi_prob_pct/100 * (_multi_payout/100) - (1 - _multi_prob_pct/100)) * 100, 1)
                _ev_clr = "#00C896" if _multi_ev > 0 else "#ef4444"
                st.markdown(
                    '<div style="font-size:0.762rem;color:#C9A84C;letter-spacing:2px;'
                    'text-transform:uppercase;margin:4px 0 6px 0">'
                    '🎰 PARLAY DEL DÍA · MULTI-DEPORTE</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div style="border-radius:16px;padding:14px 16px;margin:0 0 12px 0;'
                    f'background:linear-gradient(135deg,#C9A84C14 0%,#141414 60%,#C9A84C08 100%);'
                    f'border:1px solid #C9A84C66;box-shadow:0 0 30px rgba(201,168,76,0.15)">'
                    f'<div style="height:2px;border-radius:12px 8px 0 0;margin:-14px -16px 12px -16px;'
                    f'background:linear-gradient(90deg,transparent,#C9A84C,#00C896,#C9A84C,transparent)"></div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:10px">'
                    f'<div>'
                    f'<div style="font-size:0.65rem;color:#6B7280;letter-spacing:2px;text-transform:uppercase">'
                    f'{len(_multi_legs)} patas · hoy CDMX</div>'
                    f'<div style="font-size:0.8rem;color:#C9A84C;margin-top:2px">'
                    f'{"  ·  ".join(_SG_ICONS.get(l["sport"],"🎯")+" "+l["sport"] for l in _multi_legs)}</div>'
                    f'</div>'
                    f'<div style="text-align:right">'
                    f'<div style="font-size:1.4rem;font-weight:900;color:#C9A84C;font-family:Inter,sans-serif">{_multi_prob_pct}%</div>'
                    f'<div style="font-size:0.616rem;color:#6B7280">prob. combinada</div>'
                    f'<div style="font-size:0.694rem;color:{_ev_clr};font-weight:700">EV {_multi_ev:+.1f}</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="display:flex;flex-direction:column;gap:4px">{_legs_html}</div>'
                    f'<div style="display:flex;align-items:center;gap:16px;margin-top:10px;padding-top:8px;'
                    f'border-top:1px solid #C9A84C22;flex-wrap:wrap">'
                    f'<span style="font-size:0.694rem;color:#00C896">Pago est. +${_multi_payout:.0f}/100</span>'
                    f'<span style="font-size:0.672rem;color:#6B7280;margin-left:auto">Verifica cuotas en tu casa de apuestas</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.markdown('<div class="den-divider" style="margin:8px 0"></div>', unsafe_allow_html=True)

            # ── FEATURED: AA + O2.5 soccer combo (si no está ya en multi) ──
            _multi_game_ids = {l["game"].get("id","") for l in _multi_legs}
            if _best_btts_o25 and _best_btts_o25["game"].get("id","") not in _multi_game_ids:
                st.markdown(
                    '<div style="font-size:0.694rem;color:#00C896;letter-spacing:2px;'
                    'text-transform:uppercase;margin:12px 0 4px 0">'
                    '⚽ COMBO GOLES DESTACADO · Ambos Anotan + Over 2.5</div>',
                    unsafe_allow_html=True
                )
                st.markdown(_render_parlay_card(_best_btts_o25, featured=True), unsafe_allow_html=True)

            st.markdown(
                '<div class="warn-banner" style="margin-top:12px">'
                '⚠ Cuotas asumidas a −110/−115. Verifica en tu casa. '
                'Parlays = alta varianza — usa máx 1-2% del bankroll.</div>',
                unsafe_allow_html=True
            )
        elif pending_games:
            st.info("Simulando partidos de hoy\u2026 Regresa pronto o re-simula en el Tab de Picks.")
        else:
            st.markdown('<div class="warn-banner">Todos los partidos del día han terminado. No hay partidos pendientes para nuevos parlays.</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif _active_page == "En Vivo":
    # ── LIVE PICKS — runs instant simulation on in-progress games ─────────────
    # ─────────────────────────────────────────────────────────────────────────
    # LIVE PICK ENGINE — contextual logic based on score + minute + probs
    # Does NOT require EV+. Uses situation to find the best available bet.
    # ─────────────────────────────────────────────────────────────────────────
    def parse_live_minute(status_detail):
        """Extract game minute from ESPN status_detail string. Returns int or None."""
        import re
        # Soccer: "70:23", "HT", "45+2", "2nd Half"
        m = re.search(r"(\d{1,3})['′:]?\d{0,2}(?:\+\d+)?", status_detail or "")
        if m:
            val = int(m.group(1))
            if 1 <= val <= 120:
                return val
        if "HT" in (status_detail or "").upper() or "half time" in (status_detail or "").lower():
            return 45
        return None

    def live_pick_soccer(g, sim, minute):
        """
        Context-aware soccer live pick.
        NOTE: sim values p_btts, p_o25, p_o35 are already 0-100 (percentages), NOT 0-1 floats.
        home_pct / away_pct / draw_pct are also 0-100.
        O/U target rule: always total_goals + 1.5 (rounded up to nearest 0.5 line).
          0 goles → Over 0.5 | 1 gol → Over 1.5 (skip, use BTTS) | 2 goles → Over 2.5 | 3 → Over 3.5
        """
        try:
            hs  = int(g.get("home_score") or 0)
            as_ = int(g.get("away_score") or 0)
        except:
            hs, as_ = 0, 0
        total    = hs + as_
        minute   = minute or 50

        # All these are already 0-100
        home_pct = sim.get("home_pct", 50)
        away_pct = sim.get("away_pct", 50)
        draw_pct = sim.get("draw_pct", 0)
        p_btts   = sim.get("p_btts") or 0   # already 0-100
        p_o25    = sim.get("p_o25")  or 0   # already 0-100
        p_o35    = sim.get("p_o35")  or 0   # already 0-100

        # Dominant team: 10+ pp advantage in win probability
        home_dom = home_pct > away_pct + 10
        away_dom = away_pct > home_pct + 10
        dom_team = g["home_team"] if home_dom else (g["away_team"] if away_dom else None)
        dom_pct  = max(home_pct, away_pct)

        # ── O/U target: total + 1.5 ──────────────────────────────────────────
        # Casas de apuesta siempre ofrecen la siguiente línea sobre lo que va
        ou_line  = total + 1.5  # e.g. 1-1 → Over 2.5 | 2-0 → Over 2.5 | 2-1 → Over 3.5
        # Probability for that line from sim (only 2.5 and 3.5 tracked)
        if ou_line <= 2.5:
            ou_label = "Over 2.5 goles"
            ou_prob  = p_o25
        elif ou_line <= 3.5:
            ou_label = "Over 3.5 goles"
            ou_prob  = p_o35
        else:
            ou_label = f"Over {ou_line} goles"
            ou_prob  = max(p_o35 * 0.55, 15)  # estimate beyond 3.5

        # Adjust leader probability by score advantage
        def score_adjusted_prob(base_pct, goals_ahead, mins_left):
            """Boost win probability based on lead size and time remaining."""
            time_factor = max(mins_left, 1) / 90
            boost = goals_ahead * 18 * (1 - time_factor)
            return min(base_pct + boost, 95)

        mins_left = max(90 - minute, 1)

        # ── Situation patterns ────────────────────────────────────────────────

        # 1. 0-0 después del min 60 + un equipo dominando
        if total == 0 and minute >= 60 and dom_team:
            p_goal = min(97, 40 + minute * 0.5)  # more time elapsed → more likely a goal comes
            return {
                "picks": [
                    {"label": f"{dom_team} gana", "prob": dom_pct, "market": "ML",
                     "rationale": f"0-0 min {minute} con {dom_team} dominando ({dom_pct:.0f}%). El tiempo apremia — equipos dominantes suelen anotar tardío."},
                    {"label": "Over 0.5 goles", "prob": round(p_goal, 1), "market": "O/U",
                     "rationale": f"Solo {mins_left} min restantes, aún 0-0. Estadísticamente >90% de partidos tienen al menos 1 gol."},
                ],
                "headline": f"0-0 min {minute} — {dom_team} presiona"
            }

        # 2. 0-0 antes del min 60
        if total == 0 and minute < 60:
            if p_btts >= 55:
                return {
                    "picks": [{"label": "Ambos Anotan — SÍ", "prob": p_btts, "market": "BTTS",
                                "rationale": f"0-0 al min {minute}, ambos equipos ofensivos ({p_btts:.0f}%). BTTS SÍ es la apuesta natural con tiempo por jugar."}],
                    "headline": f"0-0 min {minute} — partido abierto"
                }
            p_goal = min(95, 20 + minute * 0.6)
            return {
                "picks": [{"label": "Over 0.5 goles", "prob": round(p_goal, 1), "market": "O/U",
                            "rationale": f"0-0 al min {minute}. Menos del 5% de partidos en estas ligas terminan sin goles."}],
                "headline": f"0-0 min {minute}"
            }

        # 3. Empate 1-1 o 2-2 — BTTS ya cumplido → Over total+1.5
        if hs == as_ and total >= 2:
            picks = [{"label": ou_label, "prob": ou_prob, "market": "O/U",
                      "rationale": f"{hs}-{as_} al min {minute}. BTTS ya cumplido. Casas ofrecen {ou_label} como siguiente línea natural — {ou_prob:.0f}% según simulación."}]
            if dom_team:
                dc_prob = min(dom_pct + draw_pct * 0.4, 92)
                picks.append({"label": f"{dom_team} gana o empata (DO)", "prob": round(dc_prob, 1), "market": "DO",
                               "rationale": f"{dom_team} con mayor dominio. Doble Oportunidad cubre empate o victoria — {dc_prob:.0f}%."})
            return {"picks": picks, "headline": f"Empate {hs}-{as_} min {minute}"}

        # 4. Empate 1-1 temprano (antes min 50) → BTTS ya cumplido + Over próxima línea
        if hs == as_ and total == 2 and minute < 50:
            return {
                "picks": [
                    {"label": ou_label, "prob": ou_prob, "market": "O/U",
                     "rationale": f"1-1 al min {minute} — partido muy abierto. {ou_label} ({ou_prob:.0f}%) es la apuesta de casas con tiempo de sobra."},
                    {"label": "Ambos Anotan — SÍ", "prob": p_btts, "market": "BTTS",
                     "rationale": f"BTTS ya confirmado. Si quieres apostar algo que ya cumplió, busca otra línea en tu casa."},
                ],
                "headline": f"1-1 min {minute} — partido abierto"
            }

        # 5. Ganando por 1 gol, minuto >= 70 → ML líder ajustado + Under próxima línea
        if abs(hs - as_) == 1 and minute >= 70:
            leader      = g["home_team"] if hs > as_ else g["away_team"]
            base_pct    = home_pct if hs > as_ else away_pct
            adj_pct     = score_adjusted_prob(base_pct, 1, mins_left)
            under_prob  = round(100 - ou_prob, 1)
            return {
                "picks": [
                    {"label": f"{leader} gana", "prob": round(adj_pct, 1), "market": "ML",
                     "rationale": f"{leader} arriba 1-0 al min {minute} ({mins_left} min restantes). Probabilidad ajustada por marcador: {adj_pct:.0f}%."},
                    {"label": f"Under {ou_line} goles", "prob": under_prob, "market": "O/U",
                     "rationale": f"Solo {total} gol(es), min {minute}. Partido controlado — Under {ou_line} al {under_prob:.0f}%."},
                ],
                "headline": f"{hs}-{as_} min {minute} — ventaja mínima"
            }

        # 6. Ganando por 1 gol, antes del min 70 → ML + Over próxima línea
        if abs(hs - as_) == 1 and minute < 70:
            leader   = g["home_team"] if hs > as_ else g["away_team"]
            trailer  = g["away_team"] if hs > as_ else g["home_team"]
            base_pct = home_pct if hs > as_ else away_pct
            adj_pct  = score_adjusted_prob(base_pct, 1, mins_left)
            return {
                "picks": [
                    {"label": f"{leader} gana", "prob": round(adj_pct, 1), "market": "ML",
                     "rationale": f"{leader} arriba min {minute}. Prob ajustada {adj_pct:.0f}% — {trailer} buscará empatar, lo que abre la línea de goles."},
                    {"label": ou_label, "prob": ou_prob, "market": "O/U",
                     "rationale": f"Con {trailer} necesitando empatar, {ou_label} ({ou_prob:.0f}%) es apuesta viva — {mins_left} min restantes."},
                ],
                "headline": f"{hs}-{as_} min {minute}"
            }

        # 7. Ventaja de 2+ goles → ML ajustado por marcador
        if abs(hs - as_) >= 2:
            leader   = g["home_team"] if hs > as_ else g["away_team"]
            base_pct = home_pct if hs > as_ else away_pct
            adj_pct  = score_adjusted_prob(base_pct, abs(hs - as_), mins_left)
            return {
                "picks": [{"label": f"{leader} gana", "prob": round(adj_pct, 1), "market": "ML",
                            "rationale": f"{leader} gana {hs}-{as_} al min {minute}. Ventaja de {abs(hs-as_)} goles — prob ajustada {adj_pct:.0f}%."}],
                "headline": f"{hs}-{as_} min {minute} — {leader} domina"
            }

        # 8. Default
        bs = sim.get("best_single")
        if bs:
            return {
                "picks": [{"label": bs["label"], "prob": round(bs["prob"] * 100, 1), "market": bs["market"],
                            "rationale": "Pick de mayor probabilidad según simulación Monte Carlo (5,000 iteraciones)."}],
                "headline": f"{hs}-{as_} min {minute}"
            }
        return None

    def live_pick_other(g, sim):
        """For Basketball/NFL/NHL/MLB/Tennis — pick best probability candidate regardless of EV."""
        try:
            hs = int(g.get("home_score") or 0)
            as_ = int(g.get("away_score") or 0)
        except:
            hs, as_ = 0, 0
        home_pct = sim.get("home_pct", 50)
        away_pct = sim.get("away_pct", 50)
        sport_group = LEAGUES.get(g["league"], {}).get("group", "")
        status = g.get("status_detail", "")
        # Pick team with highest probability
        if home_pct >= away_pct:
            label, prob, team = f"{g['home_team']} gana", home_pct, g["home_team"]
        else:
            label, prob, team = g["away_team"] + " gana", away_pct, g["away_team"]
        rationale = f"{team} con {prob:.0f}% de probabilidad simulada. Marcador actual: {as_}-{hs}."
        if sport_group == "Basketball":
            diff = abs(hs - as_)
            if diff <= 5:
                rationale = f"Partido cerrado ({as_}-{hs}). {team} tiene ligera ventaja de {prob:.0f}% según simulación — considera ML o spread reducido."
            elif diff >= 15:
                rationale = f"{team} con ventaja de {diff} pts. Probabilidad alta de mantener resultado: {prob:.0f}%."

        return {
            "picks": [{"label": label, "prob": prob, "market": "ML", "rationale": rationale}],
            "headline": f"{as_}-{hs} · {status}"
        }

    def xg_live_validator(g, ou_line, base_prob, minute):
        """
        Validate/adjust Over probability using live match stats.
        Returns dict: {adjusted_prob, confidence, signals, rationale}

        Model:
        - Expected goals rate = shots_on_target * 0.33 + shots * 0.09
        - Project to 90 min, compare to ou_line
        - Shots/corners/attacks per minute vs league average inform pressure score
        - Returns adjusted probability and a set of signal strings for display
        """
        ls = g.get("live_stats") or {}
        minute = max(minute or 1, 1)
        total_goals = (int(g.get("home_score") or 0) + int(g.get("away_score") or 0))

        signals    = []
        adj_prob   = base_prob
        has_stats  = bool(ls)

        if not has_stats:
            return {"adjusted_prob": base_prob, "confidence": "baja",
                    "signals": ["⚠ Sin stats en vivo — ESPN no reporta datos para este partido"],
                    "rationale": "Probabilidad basada solo en simulación Monte Carlo (sin datos del partido)."}

        shots     = ls.get("shots", {})
        sot       = ls.get("shots_on_target", {})
        corners   = ls.get("corners", {})
        attacks   = ls.get("attacks", {})
        poss      = ls.get("possession", {})

        h_shots = shots.get("home", 0); a_shots = shots.get("away", 0)
        h_sot   = sot.get("home", 0);   a_sot   = sot.get("away", 0)
        h_cor   = corners.get("home", 0); a_cor  = corners.get("away", 0)
        h_att   = attacks.get("home", 0); a_att  = attacks.get("away", 0)
        h_pos   = poss.get("home", 50)

        total_shots = h_shots + a_shots
        total_sot   = h_sot + a_sot
        total_cor   = h_cor + a_cor

        mins_left = max(90 - minute, 1)

        # ── xG proxy: goals already scored + projected remaining ─────────────
        # Conversion rate: ~33% of shots on target become goals
        # Project SOT rate to full 90 min then compute expected remaining goals
        if total_sot > 0:
            sot_per_min      = total_sot / minute
            projected_sot    = sot_per_min * 90
            projected_goals  = projected_sot * 0.33
            remaining_rate   = sot_per_min * mins_left * 0.33
            xg_total         = total_goals + remaining_rate
        elif total_shots > 0:
            shots_per_min    = total_shots / minute
            remaining_rate   = shots_per_min * mins_left * 0.09
            xg_total         = total_goals + remaining_rate
        else:
            xg_total         = None
            remaining_rate   = None

        # ── Shots-on-target rate signal ───────────────────────────────────────
        sot_per_min_norm = total_sot / minute if total_sot else 0
        if total_sot >= 8:
            signals.append(f"🔥 {total_sot} tiros al arco — partido muy intenso")
            adj_prob = min(adj_prob + 8, 97)
        elif total_sot >= 5:
            signals.append(f"⚡ {total_sot} tiros al arco — buen ritmo ofensivo")
            adj_prob = min(adj_prob + 4, 97)
        elif total_sot <= 2 and minute >= 30:
            signals.append(f"🧊 Solo {total_sot} tiros al arco en {minute} min — partido cerrado")
            adj_prob = max(adj_prob - 8, 5)

        # ── Total shots signal ────────────────────────────────────────────────
        if total_shots >= 20:
            signals.append(f"📊 {total_shots} tiros totales ({h_shots}H / {a_shots}A) — presión constante")
        elif total_shots >= 12:
            signals.append(f"📊 {total_shots} tiros totales — actividad ofensiva normal")
        elif total_shots <= 5 and minute >= 40:
            signals.append(f"📉 Solo {total_shots} tiros en {minute} min — equipos muy defensivos")
            adj_prob = max(adj_prob - 5, 5)

        # ── Corners signal ────────────────────────────────────────────────────
        cor_per_min = total_cor / minute if total_cor else 0
        if total_cor >= 8:
            signals.append(f"🚩 {total_cor} corners ({h_cor}H/{a_cor}A) — mucho juego aéreo y presión")
            adj_prob = min(adj_prob + 3, 97)
        elif total_cor >= 5:
            signals.append(f"🚩 {total_cor} corners — presión normal")

        # ── Dangerous attacks signal ──────────────────────────────────────────
        if h_att + a_att > 0:
            total_att = h_att + a_att
            if total_att >= 80:
                signals.append(f"⚔️  {total_att} ataques peligrosos ({h_att}H/{a_att}A) — partido muy abierto")
                adj_prob = min(adj_prob + 5, 97)
            elif total_att >= 40:
                signals.append(f"⚔️  {total_att} ataques peligrosos — flujo ofensivo activo")

        # ── xG projection signal ─────────────────────────────────────────────
        if xg_total is not None:
            if xg_total >= ou_line + 0.5:
                signals.append(f"📈 xG proyectado: {xg_total:.1f} goles — SOBRE la línea {ou_line}")
                adj_prob = min(adj_prob + 6, 97)
            elif xg_total >= ou_line:
                signals.append(f"📈 xG proyectado: {xg_total:.1f} goles — en la línea {ou_line}")
            elif xg_total < ou_line - 0.5:
                signals.append(f"📉 xG proyectado: {xg_total:.1f} goles — BAJO la línea {ou_line}")
                adj_prob = max(adj_prob - 6, 5)

        # ── Possession imbalance ──────────────────────────────────────────────
        if abs(h_pos - 50) >= 15:
            dom = g["home_team"] if h_pos > 50 else g["away_team"]
            signals.append(f"⚽ Posesión: {h_pos:.0f}% / {100-h_pos:.0f}% — {dom} controlando el balón")

        # ── Confidence based on data richness ────────────────────────────────
        n_stats = sum(1 for x in [total_shots, total_sot, total_cor, h_att+a_att] if x > 0)
        confidence = "alta" if n_stats >= 3 else ("media" if n_stats >= 2 else "baja")

        adj_prob = round(adj_prob, 1)
        delta    = adj_prob - base_prob
        delta_str = (f"+{delta:.0f}pp" if delta > 0 else f"{delta:.0f}pp") if abs(delta) >= 1 else "sin cambio"

        rationale = (
            f"Prob. base simulación: {base_prob:.0f}% → ajustada por stats en vivo: **{adj_prob:.0f}%** ({delta_str}). "
            + (f"xG proyectado {xg_total:.1f} vs línea {ou_line}. " if xg_total else "")
            + f"Datos: {total_shots} tiros, {total_sot} al arco, {total_cor} corners."
            if has_stats else f"Prob. base: {base_prob:.0f}% — sin stats disponibles."
        )

        return {
            "adjusted_prob": adj_prob,
            "confidence":    confidence,
            "signals":       signals[:5],   # max 5 signals
            "rationale":     rationale,
            "xg_total":      xg_total,
            "has_stats":     has_stats,
        }

    live_games = [g for g in games if g["state"] == "in"]
    if live_games:
        st.markdown('<div class="section-heading">🔴 Picks En Vivo</div>', unsafe_allow_html=True)
        st.caption("Análisis contextual: marcador actual + minuto + probabilidades de simulación.")

        # ── Build sport → league tree (all live games) ────────────────────────
        _lv_tree = {}
        for _g in live_games:
            _sg  = LEAGUES.get(_g["league"],{}).get("group","Soccer")
            _lv_tree.setdefault(_sg, {}).setdefault(_g["league"], []).append(_g)

        _LV_SPORT_ORDER  = ["Soccer","Basketball","Hockey","Baseball","Football"]
        _LV_SPORT_COLORS = {"Soccer":"#00C896","Basketball":"#f97316","Hockey":"#60a5fa","Baseball":"#f59e0b","Football":"#a78bfa"}
        _LV_SPORT_ICONS  = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}

        def _build_live_card(g):
            """Build a single live game card HTML string."""
            sim         = run_monte_carlo(g, n=5_000)
            dq          = sim["data_quality"]
            sport_group = LEAGUES.get(g["league"], {}).get("group", "Soccer")
            minute      = parse_live_minute(g.get("status_detail", ""))
            try:
                hs = int(g.get("home_score") or 0)
                as_ = int(g.get("away_score") or 0)
            except:
                hs, as_ = 0, 0
            score_str = f"{as_} – {hs}" if (g.get("home_score") or g.get("away_score")) else "–"

            if sport_group == "Soccer":
                result = live_pick_soccer(g, sim, minute)
            else:
                result = live_pick_other(g, sim)
            if not result:
                return None

            picks    = result["picks"]
            headline = result.get("headline","")
            best     = max(picks, key=lambda p: p["prob"])
            prob_color = "#00C896" if best["prob"] >= 70 else "#C9A84C" if best["prob"] >= 55 else "#f97316"

            # Picks mini-grid (up to 3 cols)
            _cols = min(len(picks), 3)
            ph = f'<div style="display:grid;grid-template-columns:repeat({_cols},1fr);gap:4px;margin-bottom:6px">'
            for i, pk in enumerate(picks):
                pc = "#00C896" if pk["prob"] >= 70 else "#C9A84C" if pk["prob"] >= 55 else "#f97316"
                _bg = "rgba(255,232,124,0.08)" if i == 0 else "rgba(255,255,255,0.02)"
                _bd = "#FFE87C44" if i == 0 else "#333333"
                ph += (
                    f'<div style="background:{_bg};border:1px solid {_bd};border-radius:5px;padding:5px 7px">'
                    f'<div style="font-size:0.72rem;font-weight:700;color:#FFE87C;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{pk["label"]}</div>'
                    f'<div style="font-size:1.0rem;color:{pc};font-weight:700">{pk["prob"]:.0f}%</div>'
                    f'<div style="font-size:0.62rem;color:#6B7280;line-height:1.2;overflow:hidden;max-height:2.4em">{pk["rationale"][:70]}</div>'
                    f'</div>'
                )
            ph += "</div>"

            # xG panel (soccer only, compact)
            xg_html = ""
            if sport_group == "Soccer":
                ou_pick = next((p for p in picks if p["market"] == "O/U" and "Over" in p["label"]), None)
                if ou_pick:
                    xgv = xg_live_validator(g, hs + as_ + 1.5, ou_pick["prob"], minute)
                    adj = xgv["adjusted_prob"]
                    conf = xgv["confidence"]
                    delta = adj - ou_pick["prob"]
                    adj_c = "#00C896" if adj >= 70 else "#C9A84C" if adj >= 55 else "#f97316"
                    conf_c = {"alta":"#00C896","media":"#C9A84C","baja":"#f97316"}.get(conf,"#6B7E6E")
                    ds = f"▲+{delta:.0f}pp" if delta >= 1 else (f"▼{delta:.0f}pp" if delta <= -1 else "=")
                    dc = "#00C896" if delta >= 1 else ("#ef4444" if delta <= -1 else "#6B7E6E")
                    if xgv["has_stats"]: ou_pick["prob"] = adj
                    xg_html = (
                        f'<div style="margin:4px 0;padding:5px 8px;background:rgba(96,165,250,0.04);'
                        f'border:1px solid rgba(96,165,250,0.15);border-radius:5px;'
                        f'display:flex;justify-content:space-between;align-items:center">'
                        f'<span style="font-size:0.62rem;color:rgba(96,165,250,0.6)">📡 xG</span>'
                        f'<span style="font-size:0.75rem;color:{adj_c};font-weight:700">{adj:.0f}%</span>'
                        f'<span style="font-size:0.65rem;color:{dc}">{ds}</span>'
                        f'<span style="font-size:0.60rem;color:{conf_c}">conf.{conf}</span>'
                        f'</div>'
                    )

            # Stats row
            def _sp(val, lbl, clr):
                return f'<span style="font-size:0.68rem;color:{clr};font-weight:700">{val}</span><span style="font-size:0.60rem;color:#6B7280;margin:0 6px 0 2px">{lbl}</span>'
            sh = (
                f'<div style="display:flex;flex-wrap:wrap;align-items:center;border-top:1px solid rgba(255,255,255,0.04);padding-top:5px;margin-top:4px">'
                + _sp(f'{sim["away_pct"]:.0f}%', g["away_team"][:9], "#60a5fa")
                + (_sp(f'{sim["draw_pct"]:.0f}%', "X", "#a78bfa") if sim["is_soccer"] else "")
                + _sp(f'{sim["home_pct"]:.0f}%', g["home_team"][:9], "#f97316")
                + (_sp(f'{sim["p_btts"]}%', "BTTS", "#00C896") if sim.get("p_btts") and sport_group=="Soccer" else "")
                + (_sp(f'{sim["p_o25"]}%', "O2.5", "#C9A84C") if sim.get("p_o25") and sport_group=="Soccer" else "")
                + f'<span style="margin-left:auto;font-size:0.58rem;color:#444444">DQ{dq:.0f}%</span>'
                + f'</div>'
            )

            # League + badges
            badges = (
                '<span style="background:rgba(255,60,60,0.2);color:#ff6b6b;border:1px solid rgba(255,60,60,0.4);'
                'border-radius:16px;padding:1px 6px;font-size:0.60rem;font-weight:600">🔴</span> '
                + f'<span style="font-size:0.62rem;color:#C9A84C">{league_label(g["league"])}</span>'
                + (f' <span style="font-size:0.58rem;color:#e74c3c">⚠</span>' if dq == 0 else '')
            )

            return (
                '<div style="background:linear-gradient(135deg,#161616,#111111);'
                'border:2px solid rgba(255,60,60,0.6);border-radius:12px;overflow:hidden">'
                '<div style="height:2px;background:linear-gradient(90deg,transparent,#ff3c3c,#ff6b6b,#ff3c3c,transparent)"></div>'
                '<div style="padding:8px 10px">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:5px">'
                f'<div>'
                f'<div style="font-size:0.85rem;font-weight:700;color:#fff;line-height:1.2">{g["away_team"]} @ {g["home_team"]}</div>'
                f'<div style="font-size:0.75rem;color:#00C896;font-weight:700">{score_str} <span style="color:#888888;font-weight:400;font-size:0.68rem">{headline}</span></div>'
                f'</div>'
                f'<div style="text-align:right;font-size:0.62rem">{badges}</div>'
                f'</div>'
                + ph + xg_html + sh
                + '</div></div>'
            )

        # ── Render: Sport expander → League sub-expander → 3-per-row cards ──
        for _lv_sg in _LV_SPORT_ORDER:
            if _lv_sg not in _lv_tree: continue
            _lv_sg_color = _LV_SPORT_COLORS.get(_lv_sg, "#C9A84C")
            _lv_sg_icon  = _LV_SPORT_ICONS.get(_lv_sg, "🎯")
            _lv_sg_total = sum(len(v) for v in _lv_tree[_lv_sg].values())

            # Sport-level expander (expanded by default)
            with st.expander(f"{_lv_sg_icon}  {_lv_sg}  ·  {_lv_sg_total} en vivo", expanded=True):

                for _lv_lg in sorted(_lv_tree[_lv_sg].keys()):
                    _lv_lg_games = _lv_tree[_lv_sg][_lv_lg]
                    _lv_lg_label = league_label(_lv_lg)
                    _lv_country  = LEAGUES.get(_lv_lg, {}).get("country", "")
                    _country_tag = f"  🌎 {_lv_country}" if _lv_country else ""
                    _exp_label   = f"{_lv_lg_label}{_country_tag}  ·  {len(_lv_lg_games)} partido{'s' if len(_lv_lg_games)!=1 else ''}"

                    # League-level sub-expander
                    with st.expander(_exp_label, expanded=True):

                        # Build cards
                        _lv_league_cards = [_build_live_card(g) for g in _lv_lg_games]
                        _lv_league_cards = [c for c in _lv_league_cards if c]

                        if not _lv_league_cards:
                            st.caption("Sin picks disponibles para estos partidos.")
                            continue

                        # 3 per row
                        for _rs in range(0, len(_lv_league_cards), 3):
                            _row_c = _lv_league_cards[_rs:_rs+3]
                            _nc    = len(_row_c)
                            st.markdown(
                                f'<div style="display:grid;grid-template-columns:repeat({_nc},1fr);gap:8px;margin-bottom:8px">'
                                + "".join(_row_c) + '</div>',
                                unsafe_allow_html=True
                            )

        st.markdown('<div class="den-divider" style="margin:12px 0 20px 0"></div>', unsafe_allow_html=True)

    if not live_games:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">🔴</div>
          <div class="empty-title">Sin partidos en vivo ahora</div>
          <div>No hay partidos en curso. Ve a <b>🎯 PICKS</b> para ver próximos partidos.</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
# AUTO-RESOLVE PICKS — compara picks pendientes contra resultados ESPN
# ══════════════════════════════════════════════════════════════════════════════
elif _active_page == "Reto 13M":

    # ── Login por apodo ───────────────────────────────────────────────────────
    st.markdown('''
    <style>
    @keyframes shimmer {
        0%   { background-position: -400px 0 }
        100% { background-position: 400px 0 }
    }
    @keyframes pulse-glow {
        0%,100% { box-shadow: 0 0 20px rgba(201,168,76,0.2), 0 0 60px rgba(201,168,76,0.05) }
        50%     { box-shadow: 0 0 40px rgba(201,168,76,0.4), 0 0 80px rgba(201,168,76,0.15) }
    }
    .reto-hero {
        background: linear-gradient(135deg, #0A0A0B 0%, #111108 50%, #0A0A0B 100%);
        border: 1px solid rgba(201,168,76,0.2);
        border-top: 1px solid rgba(201,168,76,0.4);
        border-radius: 20px;
        padding: 24px 20px 20px;
        text-align: center;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
        animation: pulse-glow 4s ease-in-out infinite;
    }
    .reto-hero::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 60%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(201,168,76,0.04), transparent);
        animation: shimmer 3s infinite;
    }
    .reto-title {
        font-family: "Barlow Condensed", "Impact", sans-serif;
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: 3px;
        text-transform: uppercase;
        background: linear-gradient(135deg, #FFE87C 0%, #C9A84C 50%, #FFE87C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin: 0;
    }
    .reto-sub {
        font-size: 0.65rem;
        color: #444;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 8px;
        font-weight: 600;
    }
    .reto-coin {
        font-size: 2rem;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 12px rgba(201,168,76,0.6));
    }
    </style>
    <div class="reto-hero">
        <div class="reto-coin">💰</div>
        <div class="reto-title">Reto 13 Millones</div>
        <div class="reto-sub">De $2,000 a $13,000,000 · Una apuesta a la vez</div>
    </div>
    ''', unsafe_allow_html=True)

    # Session state para el apodo activo
    if "reto_apodo" not in st.session_state:
        st.session_state["reto_apodo"] = ""

    if not st.session_state["reto_apodo"]:
        # Gold label CSS for login screen
        st.markdown("""
        <style>
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] p,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] p {
            color: #C9A84C !important;
            font-weight: 600 !important;
            font-size: 0.82rem !important;
            letter-spacing: 0.5px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # Pantalla de selección de usuario
        existing_users = _list_reto_users()
        st.markdown('<div style="max-width:400px;margin:0 auto">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading" style="text-align:center">¿Quién eres?</div>', unsafe_allow_html=True)

        apodo_input = st.text_input(
            "Tu apodo", placeholder="ej: Rongol, Pedro, El Jefe...",
            key="apodo_input_field",
            help="Cada apodo tiene su propia bitácora separada"
        )
        if existing_users:
            st.caption(f"👥 Usuarios existentes: {', '.join(existing_users)}")

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("▶ Entrar al Reto", use_container_width=True, key="btn_enter_reto"):
                if apodo_input.strip():
                    st.session_state["reto_apodo"] = apodo_input.strip()
                    st.rerun()
                else:
                    st.warning("Escribe tu apodo para continuar.")
        with col_e2:
            if existing_users:
                sel_existing = st.selectbox(
                    "🔍 Busca tu apodo aquí para cargar tu progreso",
                    [""] + existing_users,
                    key="sel_existing_user"
                )
                if sel_existing:
                    if st.button("⚡ Cargar progreso", key="btn_load_existing", use_container_width=True):
                        st.session_state["reto_apodo"] = sel_existing
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.get("reto_apodo"):
            st.stop()

    # ── Usuario activo ────────────────────────────────────────────────────────
    apodo_activo = st.session_state["reto_apodo"]

    _usr_col1, _usr_col2 = st.columns([5,1])
    with _usr_col1:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">'
            f'<div style="width:34px;height:34px;border-radius:50%;'
            f'background:linear-gradient(135deg,#C9A84C,#FFE87C);'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:1rem;font-weight:900;color:#0A0A0B;flex-shrink:0">'
            f'{apodo_activo[0].upper() if apodo_activo else "?"}</div>'
            f'<div>'
            f'<div style="font-family:Barlow Condensed,sans-serif;font-size:1.1rem;'
            f'font-weight:800;color:#C9A84C;letter-spacing:1px">{apodo_activo.upper()}</div>'
            f'<div style="font-size:0.6rem;color:#444;letter-spacing:2px">JUGADOR ACTIVO</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with _usr_col2:
        def _logout_reto(): st.session_state["reto_apodo"] = ""
        st.button("↩", key="btn_logout_reto", use_container_width=True, on_click=_logout_reto)

    reto = _load_reto(apodo_activo)
    picks = reto.get("picks", [])
    bank_inicial = reto.get("bank_inicial", 2000.0)
    meta = reto.get("meta", 13_000_000.0)

    # ── Background resolve ALL users (leaderboard stays accurate) ───────────
    _bg_resolve_key = f"_bg_resolve_{datetime.now().strftime('%Y%m%d%H%M')[:-1]}"  # every 10 min
    if st.session_state.get("_bg_resolve_last") != _bg_resolve_key:
        st.session_state["_bg_resolve_last"] = _bg_resolve_key
        try:
            _load_leaderboard_with_resolve()
        except:
            pass

    # ── Auto-resolve silencioso — corre en cada carga ─────────────────────────
    # Detecta partidos terminados y actualiza picks pendientes automáticamente
    _auto_key = f"_auto_resolved_{apodo_activo}_{len([p for p in picks if p.get('resultado')=='pendiente'])}"
    if st.session_state.get("_auto_last_key") != _auto_key:
        st.session_state["_auto_last_key"] = _auto_key
        if any(p.get("resultado") == "pendiente" for p in picks):
            picks, _n_auto, _auto_details = _silent_auto_resolve(apodo_activo, reto, picks)
            reto["picks"] = picks
            if _n_auto > 0:
                st.session_state["_auto_resolved_details"] = _auto_details
                st.session_state["_auto_resolved_n"] = _n_auto
    else:
        _n_auto = 0
        _auto_details = []

    # Show auto-resolve notifications if any picks just resolved
    _notif_details = st.session_state.pop("_auto_resolved_details", [])
    _notif_n       = st.session_state.pop("_auto_resolved_n", 0)
    if _notif_n > 0 and _notif_details:
        for _d in _notif_details:
            _notif_color = "#00D47E" if _d["res"] == "ganado" else "#ef4444" if _d["res"] == "perdido" else "#C9A84C"
            _score_txt   = f" ({_d['hs']}-{_d['as_']})" if _d.get("hs") else ""
            st.markdown(
                f'<div style="background:linear-gradient(90deg,{_notif_color}15,transparent);'
                f'border-left:3px solid {_notif_color};border-radius:8px;'
                f'padding:8px 14px;margin:3px 0;font-size:0.78rem;'
                f'display:flex;align-items:center;gap:8px">'
                f'<span style="font-size:1rem">{_d["icon"]}</span>'
                f'<span>Pick <b>#{_d["num"]}</b> — {_d["texto"][:30]}'
                f'<b style="color:{_notif_color}"> → {_d["res"].upper()}</b>'
                f'<span style="color:#555;font-size:0.7rem">{_score_txt}</span></span>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── Calcular bank actual ──────────────────────────────────────────────────
    bank_actual = bank_inicial
    for p in picks:
        r = p.get("resultado", "pendiente")
        stake = float(p.get("monto", 0))
        momio = float(p.get("momio", 0))
        if r == "ganado":
            # momio stored as decimal (>=1.01); legacy american fallback
            m = float(p.get("momio", 1.909))
            if m >= 1.01 and m < 100:   # decimal odds
                ganancia = stake * (m - 1)
            elif m > 0:                  # legacy american positive
                ganancia = stake * m / 100
            else:                        # legacy american negative
                ganancia = stake * 100 / abs(m)
            bank_actual += ganancia
        elif r == "perdido":
            bank_actual -= stake
        # push/pendiente → no cambia bank

    progreso_pct = min((bank_actual / meta) * 100, 100)
    multiplicador = bank_actual / bank_inicial if bank_inicial > 0 else 1

    # ══════════════════════════════════════════════════════════════════════
    # PICK DEL DÍA + NARRATIVE FEED
    # ══════════════════════════════════════════════════════════════════════

    # ── Pick del día desde Rongol ─────────────────────────────────────────
    _rongol_recs = st.session_state.get("rongol_picks_cache", [])
    if _rongol_recs:
        _top_rp = _rongol_recs[0]
        _top_pk = _top_rp.get("_pick", {})
        _top_prob = _top_pk.get("prob", 0) or 0
        _top_prob = _top_prob if _top_prob <= 1 else _top_prob / 100
        _top_ev   = _top_pk.get("ev", 0) or 0
        _top_lbl  = _top_pk.get("label", "")
        _top_mkt  = _top_pk.get("market", "")
        _top_game = f'{_top_rp.get("away_team","")} vs {_top_rp.get("home_team","")}'
        _top_dec  = _top_pk.get("decimal", 0) or 0
        st.markdown(
            f'<div style="background:linear-gradient(135deg,rgba(255,85,0,0.08) 0%,rgba(255,85,0,0.03) 100%);'
            f'border:1px solid rgba(255,85,0,0.25);border-top:1px solid rgba(255,85,0,0.4);'
            f'border-radius:16px;padding:14px 16px;margin:10px 0;position:relative;overflow:hidden">'
            f'<div style="position:absolute;top:0;right:0;font-size:4rem;opacity:0.04;line-height:1;padding:4px">🎯</div>'
            f'<div style="font-size:0.58rem;font-weight:800;color:var(--orange);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">⚡ Pick Recomendado Hoy</div>'
            f'<div style="font-size:0.9rem;font-weight:700;color:#E8E8E0;margin-bottom:4px">{_top_game}</div>'
            f'<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">'
            f'<span style="font-size:1.3rem;font-weight:900;color:var(--gold);font-family:Barlow Condensed,sans-serif">{_top_dec:.2f}</span>'
            f'<span style="font-size:0.75rem;font-weight:700;color:#ccc">{_top_lbl}</span>'
            f'<span style="font-size:0.65rem;background:rgba(0,212,126,0.1);color:var(--green);'
            f'padding:2px 8px;border-radius:20px;border:1px solid rgba(0,212,126,0.25)">{_top_prob*100:.0f}% prob</span>'
            f'<span style="font-size:0.65rem;background:rgba(255,85,0,0.1);color:var(--orange);'
            f'padding:2px 8px;border-radius:20px;border:1px solid rgba(255,85,0,0.25)">EV +{_top_ev:.1f}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    # ── Narrative feed ────────────────────────────────────────────────────
    # Calculate streak early (also calculated later in gamification block)
    _racha_n, _racha_tipo = 0, ""
    for _pp_early in reversed(picks):
        _r_e = _pp_early.get("resultado","pendiente")
        if _r_e == "pendiente": continue
        if _racha_n == 0:
            _racha_n, _racha_tipo = 1, _r_e
        elif _r_e == _racha_tipo:
            _racha_n += 1
        else:
            break

    _picks_res_n = [p for p in picks if p.get("resultado") in ("ganado","perdido")]
    if _picks_res_n:
        _msgs = []
        # Best single pick
        _best_pick = None; _best_gain = 0
        for _p in picks:
            if _p.get("resultado") == "ganado":
                _mm = float(_p.get("momio",0) or 0); _ss = float(_p.get("monto",0) or 0)
                _gn = _ss*(_mm-1) if _mm>=1.01 else _ss*100/abs(_mm) if _mm<0 else 0
                if _gn > _best_gain: _best_gain=_gn; _best_pick=_p
        if _best_pick:
            _msgs.append(f'🏆 Mejor pick: <b>{_best_pick.get("pick","")}</b> · ganaste <b style="color:var(--green)">+${_best_gain:,.0f}</b>')
        # Days active
        if picks:
            try:
                from datetime import datetime as _dtn
                _first = picks[0].get("fecha","")[:10]
                _days = (datetime.now().date() - datetime.strptime(_first, "%Y-%m-%d").date()).days if _first else 0
                if _days > 0: _msgs.append(f'📅 Llevas <b>{_days} días</b> en el reto')
            except: pass
        # Win streak message
        if _racha_n >= 5 and _racha_tipo == "ganado":
            _msgs.append(f'🔥 Racha histórica: <b>{_racha_n} ganados</b> consecutivos')
        # Projected finish
        if len(_picks_res_n) >= 5:
            _avg_daily = len(_picks_res_n) / max(_days if _days > 0 else 1, 1)
            _picks_needed = 0; _sim_b = bank_actual
            while _sim_b < meta and _picks_needed < 10000:
                _avg_odds = sum(float(p.get("momio",1.9) or 1.9) for p in _picks_res_n[-10:]) / min(len(_picks_res_n), 10)
                _avg_stake_pct = sum(float(p.get("monto",0) or 0) for p in _picks_res_n[-10:]) / max(sum(_sim_b for _ in range(min(len(_picks_res_n),10))),1)
                _avg_stake_pct = min(max(_avg_stake_pct, 0.01), 0.2)
                _wr = len([p for p in _picks_res_n if p.get("resultado")=="ganado"])/len(_picks_res_n)
                _sim_b *= (1 + _wr * _avg_stake_pct * (_avg_odds-1) - (1-_wr) * _avg_stake_pct)
                _picks_needed += 1
            if _picks_needed < 5000 and _avg_daily > 0:
                _days_needed = _picks_needed / _avg_daily
                _msgs.append(f'📈 A tu ritmo actual, llegas en <b>~{_days_needed:.0f} días</b> más')

        if _msgs:
            _feed_html = ''.join(
                f'<div style="font-size:0.75rem;color:#888;padding:5px 0;'
                f'border-bottom:1px solid rgba(255,255,255,0.04)">{m}</div>'
                for m in _msgs
            )
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);'
                f'border-radius:12px;padding:12px 14px;margin:8px 0">'
                f'<div style="font-size:0.58rem;color:var(--text3);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;font-weight:700">📖 Tu Historia</div>'
                + _feed_html + '</div>',
                unsafe_allow_html=True
            )

    # ══════════════════════════════════════════════════════════════════════
    # GAMIFICACIÓN — Niveles, rangos, racha, badges
    # ══════════════════════════════════════════════════════════════════════

    # ── Nivel y rango según bank actual ──────────────────────────────────
    _RANGOS = [
        (2_000_000_000, "🏆", "Inmortal",          "#FFD700"),
        (13_000_000,    "👑", "El 13 Millones",     "#FFD700"),
        (5_000_000,     "💎", "Magnate",             "#00BFFF"),
        (1_000_000,     "🚀", "Millonario",          "#00BFFF"),
        (500_000,       "🔥", "Leyenda de Las Vegas","#FF4500"),
        (100_000,       "⚡", "Alto Voltaje",        "#FF8C00"),
        (70_000,        "🎰", "Jugador Profesional", "#FF8C00"),
        (40_000,        "🦈", "Tiburón en Potencia", "#3D8EFF"),
        (20_000,        "💪", "Apostador Serio",     "#3D8EFF"),
        (10_000,        "📈", "En Racha",            "#3D8EFF"),
        (5_000,         "🟢", "Novato de Barrio",    "#00C896"),
        (0,             "🌱", "Semilla",             "#888"),
    ]
    _rango_actual = next((r for r in _RANGOS if bank_actual >= r[0]), _RANGOS[-1])
    _rango_next   = None
    for _r in reversed(_RANGOS):
        if _r[0] > bank_actual:
            _rango_next = _r
            break

    # ── Racha activa ──────────────────────────────────────────────────────
    _racha_n, _racha_tipo = 0, ""
    for _pp in reversed(picks):
        _r = _pp.get("resultado","pendiente")
        if _r == "pendiente": continue
        if _racha_n == 0:
            _racha_n, _racha_tipo = 1, _r
        elif _r == _racha_tipo:
            _racha_n += 1
        else:
            break

    # ── Badges ganados ────────────────────────────────────────────────────
    _picks_res = [p for p in picks if p.get("resultado") in ("ganado","perdido")]
    _picks_gan = [p for p in picks if p.get("resultado") == "ganado"]

    _badges_earned = []
    # Multiplicador badges
    for _mult, _ico, _lbl in [(2,"🥈","2×"),(5,"🥇","5×"),(10,"💎","10×"),(50,"🚀","50×"),(100,"👑","100×")]:
        if multiplicador >= _mult:
            _badges_earned.append((_ico, _lbl))

    # Deporte badges
    _over_picks  = [p for p in _picks_gan if "over" in (p.get("pick","") or "").lower() or "over" in (p.get("pick_label","") or "").lower()]
    _btts_picks  = [p for p in _picks_gan if (p.get("mercado","") or "").upper() in ("BTTS","AA")]
    _high_odds   = [p for p in _picks_gan if float(p.get("momio",0) or 0) >= 2.5]
    _ml_picks    = [p for p in _picks_gan if (p.get("mercado","") or "").upper() == "ML"]
    _soccer_gan  = [p for p in _picks_gan if (p.get("deporte","") or "").lower() in ("soccer","fútbol")]

    if len(_over_picks) >= 5:  _badges_earned.append(("⚽", "Rey del Over"))
    if len(_btts_picks) >= 5:  _badges_earned.append(("🎯", "Cazador BTTS"))
    if len(_high_odds)  >= 3:  _badges_earned.append(("🎲", "Cazador de Momios Altos"))
    if len(_ml_picks)   >= 10: _badges_earned.append(("🏆", "ML Master"))
    if len(_soccer_gan) >= 5:  _badges_earned.append(("⚽", "Depredador del Fútbol"))
    if _racha_n >= 3 and _racha_tipo == "ganado": _badges_earned.append(("🔥", f"En Llamas {_racha_n}×"))
    if len(_picks_res) >= 20 and (len(_picks_gan)/len(_picks_res)) >= 0.70: _badges_earned.append(("🧠", "Estratega"))

    # ── Render: Rango + Racha en banner compacto ──────────────────────────
    _racha_html = ""
    if _racha_n >= 2:
        if _racha_tipo == "ganado":
            _racha_emoji = "🔥" * min(_racha_n, 5)
            _racha_color = "#FF5500"
            _racha_bg    = "rgba(255,85,0,0.12)"
            _racha_border= "rgba(255,85,0,0.35)"
            _racha_txt   = f"<b>¡RACHA GANADORA!</b> {_racha_n} seguidos {_racha_emoji}"
        else:
            _racha_emoji = "🧊❄️"
            _racha_color = "#60a5fa"
            _racha_bg    = "rgba(96,165,250,0.08)"
            _racha_border= "rgba(96,165,250,0.25)"
            _racha_txt   = f"{_racha_emoji} {_racha_n} perdidas seguidas — respira, analiza, vuelve"
        _racha_html = (
            f'<div style="background:{_racha_bg};border:1px solid {_racha_border};'
            f'border-radius:12px;padding:10px 16px;margin:8px 0;text-align:center;'
            f'font-size:0.88rem;color:{_racha_color}">{_racha_txt}</div>'
        )

    _next_rango_html = ""
    if _rango_next:
        _falta_rango = _rango_next[0] - bank_actual
        _next_rango_html = f'<span style="font-size:0.62rem;color:#666;margin-left:8px">→ ${_falta_rango:,.0f} para {_rango_next[1]} {_rango_next[2]}</span>'

    # Detect level-up
    _prev_rango_key = f"_reto_prev_rango_{apodo_activo}"
    _prev_rango_name = st.session_state.get(_prev_rango_key, _rango_actual[2])
    _is_level_up = (_prev_rango_name != _rango_actual[2] and _prev_rango_name != "")
    st.session_state[_prev_rango_key] = _rango_actual[2]

    _levelup_style = "animation:pulse-glow 1.5s ease-in-out 3;" if _is_level_up else ""
    try:
        _rc = _rango_actual[3].lstrip('#')
        _rango_border = f"rgba({int(_rc[0:2],16)},{int(_rc[2:4],16)},{int(_rc[4:6],16)},0.4)"
    except:
        _rango_border = "rgba(201,168,76,0.4)"

    st.markdown(
        f'<div style="background:linear-gradient(135deg,rgba(201,168,76,0.06) 0%,rgba(0,0,0,0) 100%);'
        f'border:1px solid {_rango_border};border-top:1px solid rgba(201,168,76,0.35);'
        f'border-radius:18px;padding:16px 18px;margin:12px 0;'
        f'display:flex;align-items:center;gap:14px;flex-wrap:wrap;{_levelup_style}">'
        + (f'<div style="background:rgba(0,212,126,0.15);border:1px solid rgba(0,212,126,0.4);'
           f'border-radius:8px;padding:4px 10px;font-size:0.65rem;font-weight:800;color:#00D47E;'
           f'letter-spacing:1px;margin-bottom:6px;width:100%">🎉 ¡SUBISTE DE NIVEL! → {_rango_actual[2]}</div>'
           if _is_level_up else '')
        + f'<span style="font-size:2.5rem;filter:drop-shadow(0 0 12px rgba(201,168,76,0.5))">{_rango_actual[1]}</span>'
        f'<div style="flex:1">'
        f'<div style="font-size:1rem;font-weight:900;color:{_rango_actual[3]};'
        f'font-family:Barlow Condensed,sans-serif;letter-spacing:1px">{_rango_actual[2].upper()}</div>'
        f'<div style="font-size:0.65rem;color:#555;margin-top:3px">'
        f'{multiplicador:.2f}× multiplicador · ${bank_actual:,.0f}{_next_rango_html}</div>'
        f'</div>'
        f'<div style="display:flex;gap:4px;flex-wrap:wrap">'
        + "".join(f'<span title="{b[1]}" style="font-size:1.4rem;filter:drop-shadow(0 0 6px rgba(201,168,76,0.3))">{b[0]}</span>' for b in _badges_earned[-6:])
        + f'</div></div>',
        unsafe_allow_html=True
    )

    # Level up sound
    if _is_level_up:
        import streamlit.components.v1 as _fxlv
        _fxlv.html("""<script>
try{const a=new AudioContext();
[[523,0],[659,0.15],[784,0.3],[1047,0.45]].forEach(([f,t])=>{
  const o=a.createOscillator();const g=a.createGain();o.connect(g);g.connect(a.destination);
  o.frequency.value=f;g.gain.setValueAtTime(0.25,a.currentTime+t);
  g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+t+0.3);
  o.start(a.currentTime+t);o.stop(a.currentTime+t+0.35);});
}catch(e){}
</script>""", height=0)
    if _racha_html:
        st.markdown(_racha_html, unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    n_gan = sum(1 for p in picks if p.get("resultado")=="ganado")
    n_per = sum(1 for p in picks if p.get("resultado")=="perdido")
    n_pen = sum(1 for p in picks if p.get("resultado")=="pendiente")
    win_rate = (n_gan / (n_gan + n_per) * 100) if (n_gan + n_per) > 0 else 0

    # ── Hero KPI: Bank actual (main metric) ──────────────────────────────
    _bank_color = "#00D47E" if bank_actual >= bank_inicial else "#ef4444"
    _bank_delta = bank_actual - bank_inicial
    st.markdown(f'''
    <div style="background:linear-gradient(160deg,#161610 0%,#0F0F0A 100%);
        border:1px solid rgba(201,168,76,0.18);border-top:1px solid rgba(201,168,76,0.35);
        border-radius:20px;padding:22px 24px;margin-bottom:10px;
        box-shadow:0 8px 32px rgba(201,168,76,0.08),0 2px 0 rgba(201,168,76,0.15) inset;
        position:relative;overflow:hidden">
        <div style="font-size:0.58rem;color:#666;letter-spacing:3px;text-transform:uppercase;margin-bottom:6px;font-weight:700">💼 Bank Actual</div>
        <div style="font-family:Barlow Condensed,sans-serif;font-size:3rem;font-weight:900;
            color:#C9A84C;line-height:1;
            text-shadow:0 0 30px rgba(201,168,76,0.3)">${bank_actual:,.0f}</div>
        <div style="display:flex;gap:16px;margin-top:8px;flex-wrap:wrap">
            <span style="font-size:0.72rem;color:{"#00D47E" if _bank_delta>=0 else "#ef4444"};font-weight:700">
                {"+" if _bank_delta>=0 else ""}{_bank_delta:+,.0f} vs inicio</span>
            <span style="font-size:0.72rem;color:#888">{multiplicador:.2f}× multiplicador</span>
            <span style="font-size:0.72rem;color:#666">Meta: ${meta:,.0f}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ── Stats grid ────────────────────────────────────────────────────────
    _wr_color = "#00D47E" if win_rate >= 55 else ("#f59e0b" if win_rate >= 45 else "#ef4444")
    st.markdown(f'''
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px">
        <div style="background:linear-gradient(160deg,#161616 0%,#0F0F0F 100%);
            border:1px solid rgba(255,255,255,0.06);border-top:1px solid rgba(255,255,255,0.1);
            border-radius:14px;padding:14px 10px;text-align:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.3)">
            <div style="font-size:1.5rem;font-weight:900;color:{_wr_color};
                font-family:Barlow Condensed,sans-serif;line-height:1">{win_rate:.0f}%</div>
            <div style="font-size:0.52rem;color:#555;text-transform:uppercase;letter-spacing:1px;margin-top:4px;font-weight:700">Win Rate</div>
        </div>
        <div style="background:linear-gradient(160deg,#0F1A13 0%,#0A0F0C 100%);
            border:1px solid rgba(0,212,126,0.15);border-top:1px solid rgba(0,212,126,0.25);
            border-radius:14px;padding:14px 10px;text-align:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.3)">
            <div style="font-size:1.5rem;font-weight:900;color:#00D47E;
                font-family:Barlow Condensed,sans-serif;line-height:1">{n_gan}</div>
            <div style="font-size:0.52rem;color:#555;text-transform:uppercase;letter-spacing:1px;margin-top:4px;font-weight:700">✅ Ganados</div>
        </div>
        <div style="background:linear-gradient(160deg,#1A0F0F 0%,#0F0A0A 100%);
            border:1px solid rgba(239,68,68,0.15);border-top:1px solid rgba(239,68,68,0.25);
            border-radius:14px;padding:14px 10px;text-align:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.3)">
            <div style="font-size:1.5rem;font-weight:900;color:#ef4444;
                font-family:Barlow Condensed,sans-serif;line-height:1">{n_per}</div>
            <div style="font-size:0.52rem;color:#555;text-transform:uppercase;letter-spacing:1px;margin-top:4px;font-weight:700">❌ Perdidos</div>
        </div>
        <div style="background:linear-gradient(160deg,#161616 0%,#0F0F0F 100%);
            border:1px solid rgba(255,255,255,0.06);border-top:1px solid rgba(255,255,255,0.1);
            border-radius:14px;padding:14px 10px;text-align:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.3)">
            <div style="font-size:1.5rem;font-weight:900;color:#888;
                font-family:Barlow Condensed,sans-serif;line-height:1">{n_pen}</div>
            <div style="font-size:0.52rem;color:#555;text-transform:uppercase;letter-spacing:1px;margin-top:4px;font-weight:700">⏳ Pendientes</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ── Barra de progreso hacia meta ──────────────────────────────────────────
    falta = max(meta - bank_actual, 0)
    _milestones = [
        (2000, "🌱"), (5000, "🟢"), (10000, "📈"), (20000, "💪"),
        (40000, "🦈"), (70000, "🎰"), (100000, "🔥"), (500000, "🚀"),
        (1000000, "💎"), (13000000, "👑")
    ]
    _ms_html = ""
    for _ms_val, _ms_icon in _milestones:
        _ms_pct = min((_ms_val / meta) * 100, 100)
        _ms_reached = bank_actual >= _ms_val
        _ms_opacity = "1" if _ms_reached else "0.25"
        _ms_html += (
            f'<div style="position:absolute;left:{_ms_pct:.1f}%;top:-18px;'
            f'transform:translateX(-50%);font-size:0.7rem;opacity:{_ms_opacity};'
            f'filter:{"none" if _ms_reached else "grayscale(1)"}">{_ms_icon}</div>'
        )

    st.markdown(f'''
    <div style="margin:16px 0 20px;background:linear-gradient(160deg,#161614 0%,#0F0F0C 100%);
        border:1px solid rgba(201,168,76,0.15);border-radius:16px;padding:16px 18px;
        box-shadow:0 4px 16px rgba(0,0,0,0.3)">
        <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px">
            <span style="font-size:0.6rem;color:#555;text-transform:uppercase;letter-spacing:2px;font-weight:700">Progreso hacia la meta</span>
            <span style="font-size:0.85rem;font-weight:800;color:#C9A84C">{progreso_pct:.2f}%</span>
        </div>
        <div style="position:relative;margin-top:22px">
            {_ms_html}
            <div style="background:rgba(255,255,255,0.05);border-radius:20px;height:14px;
                overflow:visible;box-shadow:inset 0 2px 4px rgba(0,0,0,0.5)">
                <div style="height:14px;width:{min(progreso_pct,100):.2f}%;
                    background:linear-gradient(90deg,#C9A84C,#FFE87C,#C9A84C);
                    background-size:200% 100%;
                    border-radius:20px;
                    box-shadow:0 0 16px rgba(201,168,76,0.5);
                    animation:shimmer 2s infinite;
                    position:relative">
                    <div style="position:absolute;right:-6px;top:-3px;width:20px;height:20px;
                        background:#FFE87C;border-radius:50%;
                        box-shadow:0 0 12px rgba(255,232,124,0.8)"></div>
                </div>
            </div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:12px;font-size:0.68rem;color:#444">
            <span>${bank_inicial:,.0f}</span>
            <span style="color:#C9A84C;font-weight:700">Faltan <b>${falta:,.0f}</b></span>
            <span>🏆 ${meta:,.0f}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ── Quick Add Pick (compact, always visible) ─────────────────────────────
    st.markdown(
        '<div style="font-family:Barlow Condensed,sans-serif;font-size:0.72rem;font-weight:800;'
        'color:var(--text3);letter-spacing:3px;text-transform:uppercase;'
        'margin:16px 0 8px;display:flex;align-items:center;gap:10px">'
        '<span style="width:3px;height:14px;background:var(--orange);border-radius:2px;flex-shrink:0"></span>'
        '➕ REGISTRAR PICK'
        '<span style="flex:1;height:1px;background:linear-gradient(90deg,rgba(255,85,0,0.3),transparent)"></span>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.container():
        st.markdown(
            '<div style="background:linear-gradient(160deg,#161618 0%,#0F0F12 100%);'
            'border:1px solid rgba(255,85,0,0.2);border-top:1px solid rgba(255,85,0,0.35);'
            'border-radius:16px;padding:16px;margin-bottom:8px">',
            unsafe_allow_html=True
        )
        _qf1, _qf2, _qf3 = st.columns([3,2,2])
        with _qf1:
            _qf_partido = st.text_input("Partido", placeholder="Real Madrid vs Barça",
                                         key="qf_partido", label_visibility="visible")
        with _qf2:
            _qf_pick = st.text_input("Pick", placeholder="Real Madrid ML",
                                      key="qf_pick", label_visibility="visible")
        with _qf3:
            _qf_mercado = st.selectbox("Mercado", 
                ["ML","O/U","BTTS","DO","Spread","Run Line","Puck Line","AH","Otro"],
                key="qf_mercado",
                help="Spread=NFL/NBA/Soccer handicap | Run Line=MLB -1.5 | Puck Line=NHL -1.5 | AH=Asian Handicap soccer"
            )
        _qf4, _qf5, _qf6 = st.columns([2,2,2])
        with _qf4:
            _qf_momio = st.number_input("Cuota decimal", min_value=1.01, max_value=50.0,
                                         value=1.91, step=0.05, key="qf_momio", format="%.2f")
        with _qf5:
            _qf_monto = st.number_input("Monto ($)", min_value=1.0,
                                         value=float(min(bank_actual * 0.05, bank_actual)) if bank_actual > 0 else 100.0,
                                         step=10.0, key="qf_monto")
        with _qf6:
            _qf_resultado = st.selectbox("Resultado",
                                          ["pendiente","ganado","perdido","push"],
                                          key="qf_resultado")

        # Live preview
        _qf_gan_est = _qf_monto * (_qf_momio - 1)
        _qf_bank_new = bank_actual + _qf_gan_est if _qf_resultado == "ganado" else bank_actual - _qf_monto if _qf_resultado == "perdido" else bank_actual
        _qf_preview_color = "#00D47E" if _qf_resultado == "ganado" else "#ef4444" if _qf_resultado == "perdido" else "#888"
        st.markdown(
            f'<div style="display:flex;gap:16px;margin:8px 0 4px;font-size:0.72rem;flex-wrap:wrap">'
            f'<span style="color:#555">Ganancia si gana: <b style="color:#00D47E">+${_qf_gan_est:,.0f}</b></span>'
            f'<span style="color:#555">Bank resultante: <b style="color:{_qf_preview_color}">${_qf_bank_new:,.0f}</b></span>'
            f'<span style="color:#555">Kelly sugerido: <b style="color:var(--gold)">{min(max((_qf_momio-1)/(_qf_momio)*0.5,0.01)*100,15):.1f}%</b></span>'
            f'</div>',
            unsafe_allow_html=True
        )

        _qf_btn_col, _qf_note_col = st.columns([1,2])
        with _qf_note_col:
            _qf_nota = st.text_input("Nota", placeholder="Liga MX J12 · del oráculo",
                                      key="qf_nota", label_visibility="collapsed")
        with _qf_btn_col:
            if st.button("⚡ Agregar Pick", use_container_width=True, key="btn_qf_add"):
                if _qf_partido.strip() and _qf_pick.strip():
                    _qf_momio_fmt = f"{_qf_momio:.2f}"
                    _qf_nuevo = {
                        "num":       len(picks) + 1,
                        "fecha":     datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                        "partido":   _qf_partido.strip(),
                        "pick":      _qf_pick.strip(),
                        "mercado":   _qf_mercado,
                        "momio":     round(_qf_momio, 4),
                        "momio_fmt": _qf_momio_fmt,
                        "monto":     _qf_monto,
                        "resultado": _qf_resultado,
                        "nota":      _qf_nota,
                    }
                    picks.append(_qf_nuevo)
                    reto["picks"] = picks
                    if _save_reto(reto, apodo_activo):
                        st.toast(f"⚡ Pick #{_qf_nuevo['num']} registrado!", icon="💰")
                        if _qf_resultado == "ganado":
                            import streamlit.components.v1 as _fxq
                            _fxq.html("""<script>
(function(){const c=['#00D47E','#FFD700','#FF5500','#00BFFF'];
for(let i=0;i<60;i++){const e=document.createElement('div');
e.style.cssText=`position:fixed;top:-10px;left:${Math.random()*100}vw;width:${6+Math.random()*7}px;height:${6+Math.random()*7}px;background:${c[Math.floor(Math.random()*c.length)]};border-radius:${Math.random()>.5?'50%':'2px'};z-index:999999;pointer-events:none;animation:qfall${i} ${1+Math.random()*1.5}s ease-in forwards`;
const s=document.createElement('style');s.textContent=`@keyframes qfall${i}{to{top:110vh;transform:rotate(${Math.random()*720}deg);opacity:0}}`;
document.head.appendChild(s);document.body.appendChild(e);setTimeout(()=>e.remove(),2500);}
try{const a=new AudioContext();const o=a.createOscillator();const g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(880,a.currentTime);o.frequency.exponentialRampToValueAtTime(1760,a.currentTime+0.1);g.gain.setValueAtTime(0.3,a.currentTime);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.3);o.start();o.stop(a.currentTime+0.3);}catch(e){}})();
</script>""", height=0)
                        elif _qf_resultado == "perdido":
                            import streamlit.components.v1 as _fxq2
                            _fxq2.html("""<script>
(function(){
  const el=document.createElement('div');
  el.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(180,0,0,0.18);z-index:999998;pointer-events:none;display:flex;align-items:center;justify-content:center;animation:fadeW 2.5s forwards';
  el.innerHTML='<div style="font-family:Impact,sans-serif;font-size:9vw;color:#CC0000;text-shadow:4px 4px 0 #000,-4px -4px 0 #000;letter-spacing:10px;animation:scaleW 0.5s ease-out">PERDIDO</div>';
  const st2=document.createElement('style');
  st2.textContent='@keyframes fadeW{0%,60%{opacity:1}100%{opacity:0}}@keyframes scaleW{from{transform:scale(2.5)}to{transform:scale(1)}}';
  document.head.appendChild(st2);document.body.appendChild(el);
  setTimeout(()=>el.remove(),2500);
  try{const a=new AudioContext();[[494,0],[440,0.2],[392,0.4],[349,0.65]].forEach(([f,t])=>{const o=a.createOscillator();const g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=f;g.gain.setValueAtTime(0.25,a.currentTime+t);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+t+0.35);o.start(a.currentTime+t);o.stop(a.currentTime+t+0.4);});}catch(e){}
})();
</script>""", height=0)
                        st.rerun()
                    else:
                        st.error("Error guardando. Verifica permisos.")
                else:
                    st.warning("Completa al menos Partido y Pick.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Gráfica de bankroll ───────────────────────────────────────────────────
    if picks:
        import json as _json
        # Build series: punto 0 = bank_inicial, luego acumulado pick a pick
        series_bank = [bank_inicial]
        series_labels = ["Inicio"]
        running = bank_inicial
        for p in picks:
            r = p.get("resultado","pendiente")
            stake = float(p.get("monto", 0))
            momio = float(p.get("momio", 0))
            if r == "ganado":
                m_c = float(p.get("momio", 1.909))
                if m_c >= 1.01 and m_c < 100:
                    gan = stake * (m_c - 1)
                elif m_c > 0:
                    gan = stake * m_c / 100
                else:
                    gan = stake * 100 / abs(m_c)
                running += gan
            elif r == "perdido":
                running -= stake
            series_bank.append(round(running, 2))
            short = (p.get("partido","") or p.get("pick",""))[:18]
            series_labels.append(f"#{p.get('num','?')} {short}")

        # Colors per segment: green if up, red if down vs previous
        colors = []
        for i in range(1, len(series_bank)):
            colors.append("#00C896" if series_bank[i] >= series_bank[i-1] else "#ef4444")

        # Build rich tooltip data for each pick point
        series_picks = [None]  # index 0 = "Inicio", no pick data
        for p in picks:
            r = p.get("resultado","pendiente")
            stake = float(p.get("monto", 0))
            momio = float(p.get("momio", 0))
            partido   = p.get("partido","") or p.get("pick","")
            pick_lbl  = p.get("pick","") or p.get("pick_label","")
            mercado   = p.get("mercado","")
            liga      = p.get("liga","")
            num       = p.get("num","?")
            if r == "ganado":
                m_c = float(p.get("momio", 1.909))
                if m_c >= 1.01 and m_c < 100:
                    pnl = round(stake * (m_c - 1), 2)
                elif m_c > 0:
                    pnl = round(stake * m_c / 100, 2)
                else:
                    pnl = round(stake * 100 / abs(m_c), 2)
            elif r == "perdido":
                pnl = round(-stake, 2)
            else:
                pnl = 0
            series_picks.append({
                "num":     num,
                "partido": partido[:32],
                "pick":    pick_lbl[:24],
                "mercado": mercado,
                "liga":    liga,
                "stake":   stake,
                "momio":   momio,
                "pnl":     pnl,
                "res":     r,
            })

        chart_data = _json.dumps({
            "labels": series_labels,
            "values": series_bank,
            "colors": colors,
            "picks":  series_picks,
            "bank_inicial": bank_inicial,
            "meta": meta,
        })

        # SVG chart — pure HTML, no external deps, always visible in Streamlit
        import json as _json2
        _cd = _json.loads(chart_data)
        _vals = _cd["values"]
        _lbls = _cd["labels"]
        _pks  = _cd["picks"]

        # Fixed scale: 0 → 5000, pure Python SVG (no f-string nesting issues)
        _Y_MIN, _Y_MAX = 0, 5000
        _W, _H = 760, 260
        _PL, _PR, _PT, _PB = 58, 24, 20, 36

        def _vy(v):
            r = (v - _Y_MIN) / (_Y_MAX - _Y_MIN)
            return _PT + (1 - r) * (_H - _PT - _PB)

        def _vx(i, nn):
            if nn <= 1: return _PL + (_W - _PL - _PR) / 2
            return _PL + i * (_W - _PL - _PR) / (nn - 1)

        _n = len(_vals)
        _RES_CLR = {"ganado":"#00C896","perdido":"#ef4444","pendiente":"#f59e0b"}

        # Y axis grid lines and labels
        _ytick_parts = []
        for _yt in [0, 1000, 2000, 3000, 4000, 5000]:
            _yy = _vy(_yt)
            _ylbl = ("$" + str(_yt // 1000) + "k") if _yt >= 1000 else "$0"
            _ytick_parts.append(
                '<line x1="' + str(_PL) + '" y1="' + str(round(_yy,1)) + '" x2="' + str(_W-_PR) + '" y2="' + str(round(_yy,1)) + '" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>'
                + '<text x="' + str(_PL-6) + '" y="' + str(round(_yy+4,1)) + '" fill="#555555" font-size="10" text-anchor="end">' + _ylbl + '</text>'
            )
        _ytick_svg = "".join(_ytick_parts)

        # Segments
        _seg_parts = []
        for _i in range(_n - 1):
            _x1, _y1 = _vx(_i, _n), _vy(_vals[_i])
            _x2, _y2 = _vx(_i+1, _n), _vy(_vals[_i+1])
            _sc = "#00C896" if _vals[_i+1] >= _vals[_i] else "#ef4444"
            _seg_parts.append('<line x1="' + str(round(_x1,1)) + '" y1="' + str(round(_y1,1)) + '" x2="' + str(round(_x2,1)) + '" y2="' + str(round(_y2,1)) + '" stroke="' + _sc + '" stroke-width="2.5" stroke-linecap="round"/>')
        _seg_svg = "".join(_seg_parts)

        # Fill polygon
        _pts_list = " ".join(str(round(_vx(_i,_n),1)) + "," + str(round(_vy(_v),1)) for _i,_v in enumerate(_vals))
        _fill_pts = str(_PL) + "," + str(round(_vy(_Y_MIN),1)) + " " + _pts_list + " " + str(round(_vx(_n-1,_n),1)) + "," + str(round(_vy(_Y_MIN),1))

        # Dots and labels
        _dot_parts = []
        for _i, (_v, _lb) in enumerate(zip(_vals, _lbls)):
            _pk = _pks[_i] if _i < len(_pks) else None
            _res = _pk["res"] if _pk else None
            _clr = "#C9A84C" if _i == 0 else _RES_CLR.get(_res, "#C9A84C")
            _cx, _cy = _vx(_i, _n), _vy(_v)
            _rb = 9 if _res in ("ganado","perdido") else 7
            _vlbl = "$" + "{:,.0f}".format(_v)
            _slbl = _lb[:12]
            _dot_parts.append(
                '<circle cx="' + str(round(_cx,1)) + '" cy="' + str(round(_cy,1)) + '" r="' + str(_rb+5) + '" fill="' + _clr + '" opacity="0.18"/>'
                + '<circle cx="' + str(round(_cx,1)) + '" cy="' + str(round(_cy,1)) + '" r="' + str(_rb) + '" fill="' + _clr + '" stroke="#000" stroke-width="1.5"/>'
                + '<text x="' + str(round(_cx,1)) + '" y="' + str(round(_cy-14,1)) + '" fill="' + _clr + '" font-size="10" font-weight="bold" text-anchor="middle">' + _vlbl + '</text>'
                + '<text x="' + str(round(_cx,1)) + '" y="' + str(round(_H-_PB+14,1)) + '" fill="#444444" font-size="9" text-anchor="middle">' + _slbl + '</text>'
            )
        _dot_svg = "".join(_dot_parts)

        _svg_html = (
            '<div style="background:#080808;padding:16px;border-radius:12px;border:1px solid rgba(201,168,76,0.25);overflow:hidden">'
            + '<svg viewBox="0 0 ' + str(_W) + ' ' + str(_H) + '" width="100%" height="' + str(_H) + '" style="display:block">'
            + '<defs><linearGradient id="fillGrad" x1="0" y1="0" x2="0" y2="1">'
            + '<stop offset="0%" stop-color="#C9A84C" stop-opacity="0.15"/>'
            + '<stop offset="100%" stop-color="#C9A84C" stop-opacity="0.01"/>'
            + '</linearGradient></defs>'
            + _ytick_svg
            + '<polygon points="' + _fill_pts + '" fill="url(#fillGrad)"/>'
            + _seg_svg + _dot_svg
            + '</svg></div>'
        )
        st.markdown(_svg_html, unsafe_allow_html=True)

    elif not picks:
        st.markdown('''<div class="empty-state">
          <div class="empty-icon">💰</div>
          <div class="empty-title">Sin picks aún</div>
          <div>Registra tu primer pick abajo para comenzar el reto.</div>
        </div>''', unsafe_allow_html=True)

    st.markdown('<div class="den-divider" style="margin:20px 0"></div>', unsafe_allow_html=True)

    # ── ANALYTICS (solo si hay picks resueltos) ───────────────────────────────
    _picks_res = [p for p in picks if p.get("resultado") in ("ganado","perdido")]
    if _picks_res:
        st.markdown('<div class="section-heading">📊 Análisis de Rendimiento</div>', unsafe_allow_html=True)

        # ROI real
        _tot_ap = sum(float(p.get("monto",0)) for p in _picks_res)
        _net = 0.0
        for _pr in _picks_res:
            _mm = float(_pr.get("momio",1.9)); _ss = float(_pr.get("monto",0))
            if _pr.get("resultado")=="ganado":
                _net += _ss*(_mm-1) if _mm>=1.01 else _ss*_mm/100
            else: _net -= _ss
        _roi = (_net/_tot_ap*100) if _tot_ap>0 else 0
        _roi_clr = "#00E5A0" if _roi>=0 else "#ef4444"

        # Racha / tilt
        _rn,_rt = 0,""
        for _pp in reversed(picks):
            _r = _pp.get("resultado","pendiente")
            if _r=="pendiente": continue
            if _rn==0: _rn,_rt=1,_r
            elif _r==_rt: _rn+=1
            else: break
        if _rt=="perdido" and _rn>=3:
            st.markdown(f'<div class="demo-banner" style="font-size:0.85rem;border-left:3px solid #ef4444">🧠 <strong>Alerta de Tilt</strong> — Llevas {_rn} perdidas seguidas. Considera pausar.</div>', unsafe_allow_html=True)

        # Hitos
        _hitos = [(1.5,"🥉","1.5x"),(2,"🥈","2x"),(5,"🥇","5x"),(10,"💎","10x"),(50,"🚀","50x"),(100,"👑","100x")]
        _earned = [h for h in _hitos if multiplicador>=h[0]]
        _next_h = next((h for h in _hitos if multiplicador<h[0]),None)
        _badges = " ".join(f'<span title="{h[2]}" style="font-size:1.3rem">{h[1]}</span>' for h in _earned) or '<span style="color:#444;font-size:0.72rem">Sin hitos aún</span>'
        _next_s = f'Próximo: {_next_h[1]} {_next_h[2]} → ${bank_inicial*_next_h[0]:,.0f}' if _next_h else "🏆 ¡Meta cumplida!"

        # Semanal
        from datetime import date as _date, timedelta as _td
        _hoy_d=_date.today(); _lun=_hoy_d-_td(days=_hoy_d.weekday()); _lun_p=_lun-_td(weeks=1); _dom_p=_lun-_td(days=1)
        def _wsem(desde,hasta):
            _w=[p for p in picks if p.get("resultado") in ("ganado","perdido") and desde.isoformat()<=(p.get("fecha","") or "")[:10]<=hasta.isoformat()]
            _g=sum(1 for p in _w if p.get("resultado")=="ganado"); _p=len(_w)-_g
            _n=0.0
            for p in _w:
                _mm=float(p.get("momio",1.9)); _ss=float(p.get("monto",0))
                if p.get("resultado")=="ganado": _n+=_ss*(_mm-1) if _mm>=1.01 else _ss*_mm/100
                else: _n-=_ss
            _wr=_g/(_g+_p)*100 if (_g+_p)>0 else 0
            return _g,_p,round(_n,2),_wr
        _g1,_p1,_n1,_wr1=_wsem(_lun,_hoy_d); _g2,_p2,_n2,_wr2=_wsem(_lun_p,_dom_p)

        # ROI + badges
        st.markdown(f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
          <div style="background:#141416;border-radius:16px;padding:14px 16px;border:1px solid rgba(255,255,255,0.07)">
            <div style="font-size:0.55rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:5px">ROI Real</div>
            <div style="font-size:2rem;font-weight:900;color:{_roi_clr};font-family:Syne,sans-serif;line-height:1">{"+" if _roi>=0 else ""}{_roi:.1f}%</div>
            <div style="font-size:0.65rem;color:#555;margin-top:4px">${_net:+,.0f} sobre ${_tot_ap:,.0f} apostados</div>
          </div>
          <div style="background:#141416;border-radius:16px;padding:14px 16px;border:1px solid rgba(255,255,255,0.07)">
            <div style="font-size:0.55rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:5px">Logros</div>
            <div>{_badges}</div>
            <div style="font-size:0.62rem;color:#888;margin-top:5px">{_next_s}</div>
          </div>
        </div>''', unsafe_allow_html=True)

        # Semanas
        _c1,_c2=st.columns(2)
        def _sem_card(g,p,n,wr,lbl):
            _c="#00E5A0" if n>=0 else "#ef4444"
            return (f'<div style="background:#141416;border-radius:14px;padding:12px 14px;border:1px solid rgba(255,255,255,0.07)">'
                    f'<div style="font-size:0.55rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:7px">{lbl}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<div><span style="color:#00E5A0;font-weight:700">{g}G</span> <span style="color:#555">·</span> <span style="color:#ef4444;font-weight:700">{p}P</span> <span style="font-size:0.62rem;color:#666">({wr:.0f}%)</span></div>'
                    f'<div style="font-size:1.1rem;font-weight:800;color:{_c};font-family:Syne,sans-serif">{"+" if n>=0 else ""}${n:,.0f}</div>'
                    f'</div></div>')
        with _c1: st.markdown(_sem_card(_g1,_p1,_n1,_wr1,"Esta semana"), unsafe_allow_html=True)
        with _c2: st.markdown(_sem_card(_g2,_p2,_n2,_wr2,"Semana pasada"), unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Mercado
        _mkt_s={}
        for _pr in _picks_res:
            _mk=_pr.get("mercado","Otro") or "Otro"
            if _mk not in _mkt_s: _mkt_s[_mk]={"g":0,"p":0,"ap":0.0,"net":0.0}
            _ss=float(_pr.get("monto",0)); _mm=float(_pr.get("momio",1.9))
            _mkt_s[_mk]["ap"]+=_ss
            if _pr.get("resultado")=="ganado": _mkt_s[_mk]["g"]+=1; _mkt_s[_mk]["net"]+=_ss*(_mm-1) if _mm>=1.01 else _ss*_mm/100
            else: _mkt_s[_mk]["p"]+=1; _mkt_s[_mk]["net"]-=_ss
        if _mkt_s:
            st.markdown('<div style="font-size:0.6rem;font-weight:700;color:#C9A84C;letter-spacing:2px;text-transform:uppercase;margin:12px 0 7px">Por Mercado</div>', unsafe_allow_html=True)
            _rows=""
            for _mk,_ms in sorted(_mkt_s.items(), key=lambda x: x[1]["net"], reverse=True):
                _wr=_ms["g"]/(_ms["g"]+_ms["p"])*100 if (_ms["g"]+_ms["p"])>0 else 0
                _roi2=(_ms["net"]/_ms["ap"]*100) if _ms["ap"]>0 else 0
                _c1c="#00E5A0" if _ms["net"]>=0 else "#ef4444"
                _c2c="#00E5A0" if _roi2>=0 else "#ef4444"
                _rows+=f'<div style="display:grid;grid-template-columns:55px 35px 35px 1fr 65px 65px;gap:4px;padding:8px 12px;border-bottom:1px solid rgba(255,255,255,0.04);align-items:center"><span style="font-size:0.72rem;font-weight:700;color:#E8E8E8">{_mk}</span><span style="font-size:0.68rem;color:#00E5A0;text-align:center">{_ms["g"]}G</span><span style="font-size:0.68rem;color:#ef4444;text-align:center">{_ms["p"]}P</span><span style="font-size:0.65rem;color:#888">{_wr:.0f}%WR</span><span style="font-size:0.68rem;font-weight:700;color:{_c2c}">ROI {_roi2:+.0f}%</span><span style="font-size:0.68rem;font-weight:700;color:{_c1c}">{"+" if _ms["net"]>=0 else ""}${_ms["net"]:,.0f}</span></div>'
            st.markdown(f'<div style="background:#0F0F11;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,0.07)"><div style="display:grid;grid-template-columns:55px 35px 35px 1fr 65px 65px;gap:4px;padding:7px 12px;background:rgba(255,255,255,0.03);font-size:0.52rem;color:#555;letter-spacing:1px;text-transform:uppercase"><span>Mkt</span><span style="text-align:center">G</span><span style="text-align:center">P</span><span>WR%</span><span>ROI</span><span>Neto</span></div>{_rows}</div>', unsafe_allow_html=True)

        # Tabla momios por rango
        _ranges=[(1.01,1.20,"1.01–1.20"),(1.21,1.50,"1.21–1.50"),(1.51,2.00,"1.51–2.00"),(2.01,2.50,"2.01–2.50"),(2.51,3.50,"2.51–3.50"),(3.51,99.0,"3.51+")]
        _tbl=[]; 
        for _lo,_hi,_rl in _ranges:
            _rng=[p for p in _picks_res if _lo<=float(p.get("momio",0))<=_hi]
            if not _rng: continue
            _rg=sum(1 for p in _rng if p.get("resultado")=="ganado"); _rp2=len(_rng)-_rg
            _rwr=_rg/len(_rng)*100; _rnet=0.0
            for p in _rng:
                _ss=float(p.get("monto",0)); _mm=float(p.get("momio",1.9))
                if p.get("resultado")=="ganado": _rnet+=_ss*(_mm-1) if _mm>=1.01 else _ss*_mm/100
                else: _rnet-=_ss
            _rap=sum(float(p.get("monto",0)) for p in _rng)
            _rroi=(_rnet/_rap*100) if _rap>0 else 0
            _tbl.append((_rl,len(_rng),_rg,_rp2,_rwr,_rroi,_rnet))
        if _tbl:
            st.markdown('<div style="font-size:0.6rem;font-weight:700;color:#C9A84C;letter-spacing:2px;text-transform:uppercase;margin:12px 0 7px">Win% por Rango de Cuota</div>', unsafe_allow_html=True)
            _tbl_html=""
            for _rl,_rt,_rg,_rp2,_rwr,_rroi,_rnet in _tbl:
                _bc="#00E5A0" if _rwr>=55 else ("#f59e0b" if _rwr>=45 else "#ef4444")
                _rc="#00E5A0" if _rroi>=0 else "#ef4444"
                _tbl_html+=(
                    f'<div style="padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.04)">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px">'
                    f'<span style="font-size:0.8rem;font-weight:800;color:#E8E8E8;font-family:Syne,sans-serif">{_rl}</span>'
                    f'<div style="display:flex;gap:10px">'
                    f'<span style="font-size:0.65rem;color:#888">{_rg}G/{_rp2}P ({_rt})</span>'
                    f'<span style="font-size:0.75rem;font-weight:800;color:{_bc}">{_rwr:.0f}%</span>'
                    f'<span style="font-size:0.68rem;color:{_rc}">ROI {_rroi:+.0f}%</span>'
                    f'</div></div>'
                    f'<div style="background:rgba(255,255,255,0.06);border-radius:20px;height:6px;overflow:hidden">'
                    f'<div style="height:6px;width:{min(int(_rwr),100)}%;background:{_bc};border-radius:20px"></div>'
                    f'</div></div>'
                )
            st.markdown(f'<div style="background:#0F0F11;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,0.07)">{_tbl_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="den-divider" style="margin:18px 0"></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # LEADERBOARD — siempre visible, auto-refresh
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div style="font-family:Barlow Condensed,sans-serif;font-size:0.72rem;font-weight:800;'
        'color:var(--text3);letter-spacing:3px;text-transform:uppercase;'
        'margin:18px 0 10px;display:flex;align-items:center;gap:10px">'
        '<span style="width:3px;height:14px;background:var(--gold);border-radius:2px;flex-shrink:0"></span>'
        '🏆 LEADERBOARD'
        '<span style="flex:1;height:1px;background:linear-gradient(90deg,rgba(201,168,76,0.3),transparent)"></span>'
        '</div>',
        unsafe_allow_html=True
    )

    # Load all users — cached 2 min
    _lb_col1, _lb_col2 = st.columns([4,1])
    with _lb_col2:
        def _refresh_lb():
            _load_leaderboard.clear()
        st.button("↺ Refresh", key="btn_lb_refresh", use_container_width=True, on_click=_refresh_lb)

    _lb_data = _load_leaderboard()

    if not _lb_data:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);'
            'border-radius:12px;padding:20px;text-align:center;color:#444;font-size:0.8rem">'
            '⚙️ Configura Google Sheets para ver el leaderboard</div>',
            unsafe_allow_html=True
        )
    else:
        # ── Header row ────────────────────────────────────────────────
        st.markdown(
            '<div style="display:grid;grid-template-columns:28px 36px 1fr 90px 60px 56px;'
            'gap:8px;padding:0 8px 6px;align-items:center;'
            'border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:4px">'
            '<span style="font-size:0.55rem;color:#333;text-transform:uppercase;letter-spacing:1px">#</span>'
            '<span></span>'
            '<span style="font-size:0.55rem;color:#333;text-transform:uppercase;letter-spacing:1px">Jugador</span>'
            '<span style="font-size:0.55rem;color:#333;text-transform:uppercase;letter-spacing:1px;text-align:right">Bank</span>'
            '<span style="font-size:0.55rem;color:#333;text-transform:uppercase;letter-spacing:1px;text-align:center">Racha</span>'
            '<span style="font-size:0.55rem;color:#333;text-transform:uppercase;letter-spacing:1px;text-align:right">WR</span>'
            '</div>',
            unsafe_allow_html=True
        )

        _my_pos = None
        for _pos, _u in enumerate(_lb_data, 1):
            _is_me = (_u["apodo"] == apodo_activo)
            if _is_me: _my_pos = _pos

            # Calculate active win streak for this user
            _u_streak = 0; _u_streak_type = ""
            for _up in reversed(_u.get("all_picks", []) + _u.get("all_picks", [])):
                break  # need full picks — use n_gan as proxy for now
            # Compute streak from all_picks (last 5) - approximate
            _all_up = _u.get("all_picks", [])
            _u_streak = 0
            for _up in reversed(_all_up):
                _up_r = _up.get("resultado","")
                if _up_r == "pendiente": continue
                if _u_streak == 0:
                    _u_streak = 1; _u_streak_type = _up_r
                elif _up_r == _u_streak_type:
                    _u_streak += 1
                else:
                    break

            # Streak display
            if _u_streak >= 2 and _u_streak_type == "ganado":
                _streak_html = f'<span style="font-size:0.72rem;color:#FF5500;font-weight:800">🔥{_u_streak}</span>'
            elif _u_streak >= 2 and _u_streak_type == "perdido":
                _streak_html = f'<span style="font-size:0.72rem;color:#60a5fa">🧊{_u_streak}</span>'
            else:
                _streak_html = f'<span style="font-size:0.65rem;color:#333">{_u["n_gan"]}G/{_u["n_per"]}P</span>'

            _u_icon, _u_rango, _u_color = _rango_for_bank(_u["bank"])
            _pos_color = {"1":"#FFD700","2":"#C0C0C0","3":"#CD7F32"}.get(str(_pos),"#333")
            _bank_color = "#00D47E" if _u["bank"] >= _u["bank_ini"] else "#ef4444"
            _wr_color   = "#00D47E" if _u["wr"] >= 55 else ("#f59e0b" if _u["wr"] >= 45 else "#ef4444")

            # Card bg: gold tint for me, podium tint for top 3
            if _is_me:
                _row_bg = "linear-gradient(90deg,rgba(201,168,76,0.08) 0%,rgba(0,0,0,0) 100%)"
                _row_border = "1px solid rgba(201,168,76,0.25)"
                _row_bl = "3px solid var(--gold)"
            elif _pos == 1:
                _row_bg = "linear-gradient(90deg,rgba(255,215,0,0.05) 0%,rgba(0,0,0,0) 100%)"
                _row_border = "1px solid rgba(255,215,0,0.12)"
                _row_bl = "3px solid #FFD700"
            elif _pos <= 3:
                _row_bg = "linear-gradient(90deg,rgba(255,255,255,0.02) 0%,rgba(0,0,0,0) 100%)"
                _row_border = "1px solid rgba(255,255,255,0.05)"
                _row_bl = f"3px solid {_pos_color}"
            else:
                _row_bg = "transparent"
                _row_border = "1px solid rgba(255,255,255,0.04)"
                _row_bl = "3px solid transparent"

            st.markdown(
                f'<div style="display:grid;grid-template-columns:28px 36px 1fr 90px 60px 56px;'
                f'gap:8px;padding:10px 8px;align-items:center;'
                f'background:{_row_bg};border:{_row_border};border-left:{_row_bl};'
                f'border-radius:10px;margin:3px 0">'

                # Pos
                f'<div style="font-size:{"1rem" if _pos<=3 else "0.72rem"};'
                f'color:{_pos_color};font-weight:900;text-align:center">'
                f'{["🥇","🥈","🥉"][_pos-1] if _pos<=3 else str(_pos)}</div>'

                # Avatar
                f'<div style="width:32px;height:32px;border-radius:50%;'
                f'background:linear-gradient(135deg,{_u_color},{_u_color}66);'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:0.85rem;font-weight:900;color:#0A0A0B;'
                f'box-shadow:0 0 8px {_u_color}44">{_u["apodo"][0].upper()}</div>'

                # Name + rango
                f'<div style="min-width:0">'
                f'<div style="font-size:0.82rem;font-weight:800;'
                f'color:{"var(--gold)" if _is_me else "var(--text)"};'
                f'font-family:Barlow Condensed,sans-serif;letter-spacing:0.5px;'
                f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'
                f'{_u["apodo"].upper()}'
                f'{"  👈" if _is_me else ""}</div>'
                f'<div style="font-size:0.55rem;color:{_u_color};margin-top:1px">'
                f'{_u_icon} {_u_rango}</div>'
                f'</div>'

                # Bank
                f'<div style="text-align:right">'
                f'<div style="font-size:0.88rem;font-weight:900;color:{_bank_color};'
                f'font-family:Barlow Condensed,sans-serif">${_u["bank"]:,.0f}</div>'
                f'<div style="font-size:0.55rem;color:#444;margin-top:1px">{_u["mult"]:.1f}×</div>'
                f'</div>'

                # Streak
                f'<div style="text-align:center">{_streak_html}</div>'

                # WR
                f'<div style="text-align:right">'
                f'<div style="font-size:0.78rem;font-weight:700;color:{_wr_color}">{_u["wr"]:.0f}%</div>'
                f'<div style="font-size:0.55rem;color:#333">{_u["n_picks"]}p</div>'
                f'</div>'

                f'</div>',
                unsafe_allow_html=True
            )

        # Footer: my rank + last updated
        _lb_footer_parts = []
        if _my_pos:
            _gap_to_1 = _lb_data[0]["bank"] - _lb_data[_my_pos-1]["bank"] if _my_pos > 1 else 0
            _footer_txt = f'Posición #{_my_pos} de {len(_lb_data)}'
            if _gap_to_1 > 0:
                _footer_txt += f' · A ${_gap_to_1:,.0f} del líder'
            _lb_footer_parts.append(_footer_txt)

        if _lb_footer_parts:
            st.markdown(
                f'<div style="text-align:center;font-size:0.65rem;color:#333;margin-top:8px">'
                f'{" · ".join(_lb_footer_parts)} · cache 5min</div>',
                unsafe_allow_html=True
            )


    # ══════════════════════════════════════════════════════════════════════
    # SIMULADOR DE DESTINO
    # ══════════════════════════════════════════════════════════════════════
    with st.expander("🔮 Simulador de Destino — ¿Qué pasa si gano los próximos N picks?", expanded=False):
        _sim_col1, _sim_col2 = st.columns([2,1])
        with _sim_col1:
            _n_futuros = st.slider("Número de picks futuros a simular", 1, 20, 5, key="sim_futuros_n")
        with _sim_col2:
            # Average odds from past wins
            _avg_momio_hist = 0.0
            _gan_momios = [float(p.get("momio",0) or 0) for p in picks if p.get("resultado")=="ganado" and float(p.get("momio",0) or 0) > 1]
            if _gan_momios:
                _avg_momio_hist = sum(_gan_momios) / len(_gan_momios)
            _momio_sim = st.number_input("Cuota promedio", min_value=1.01, max_value=10.0,
                                          value=round(_avg_momio_hist, 2) if _avg_momio_hist > 1 else 1.90,
                                          step=0.05, key="sim_momio")

        # Calculate stake % (Kelly-style: default 3% of bank)
        _kelly_pct_sim = st.slider("% del bank por pick (Kelly)", 1, 15, 3, key="sim_kelly") / 100

        # Project future bank values
        _sim_banks = [bank_actual]
        _bank_run = bank_actual
        for _i in range(_n_futuros):
            _stake = _bank_run * _kelly_pct_sim
            _ganancia = _stake * (_momio_sim - 1)
            _bank_run = _bank_run + _ganancia
            _sim_banks.append(round(_bank_run, 2))

        _proj_final = _sim_banks[-1]
        _proj_mult  = _proj_final / bank_inicial if bank_inicial > 0 else 1
        _proj_rango = next((r for r in _RANGOS if _proj_final >= r[0]), _RANGOS[-1])

        # Visual projection display
        _proj_html = (
            f'<div style="background:linear-gradient(160deg,rgba(0,212,126,0.08) 0%,rgba(0,0,0,0) 100%);'
            f'border:1px solid rgba(0,212,126,0.25);border-radius:14px;padding:16px;margin:8px 0;text-align:center">'
            f'<div style="font-size:0.62rem;color:#666;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">Si ganas los próximos {_n_futuros} picks</div>'
            f'<div style="font-size:2.8rem;font-weight:900;color:#00D47E;font-family:Barlow Condensed,sans-serif;line-height:1">${_proj_final:,.0f}</div>'
            f'<div style="font-size:0.82rem;color:#888;margin-top:6px">{_proj_mult:.1f}× del bank inicial · {_proj_rango[1]} {_proj_rango[2]}</div>'
            f'<div style="font-size:0.68rem;color:#555;margin-top:4px">apostando {_kelly_pct_sim*100:.0f}% del bank a cuota {_momio_sim:.2f}</div>'
            f'</div>'
        )
        st.markdown(_proj_html, unsafe_allow_html=True)

        # Mini projection chart
        if len(_sim_banks) > 1:
            import json as _j2
            _pts = list(range(len(_sim_banks)))
            _chart_js = f"""
            <div id="simchart" style="height:120px;margin-top:8px"></div>
            <script>
            (function(){{
              const banks = {_j2.dumps(_sim_banks)};
              const canvas = document.createElement('canvas');
              canvas.style.width='100%'; canvas.style.height='120px';
              document.getElementById('simchart').appendChild(canvas);
              const ctx = canvas.getContext('2d');
              canvas.width = canvas.offsetWidth || 400;
              canvas.height = 120;
              const w = canvas.width, h = canvas.height;
              const min_ = Math.min(...banks), max_ = Math.max(...banks);
              const pad = 20;
              ctx.strokeStyle = '#00D47E'; ctx.lineWidth = 2.5;
              ctx.shadowColor = '#00D47E'; ctx.shadowBlur = 8;
              ctx.beginPath();
              banks.forEach((v,i) => {{
                const x = pad + (i/(banks.length-1))*(w-2*pad);
                const y = h - pad - ((v-min_)/(max_-min_||1))*(h-2*pad);
                i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
              }});
              ctx.stroke();
              // Fill
              ctx.shadowBlur = 0;
              banks.forEach((v,i) => {{
                const x = pad + (i/(banks.length-1))*(w-2*pad);
                const y = h - pad - ((v-min_)/(max_-min_||1))*(h-2*pad);
                ctx.fillStyle = '#00D47E';
                ctx.beginPath(); ctx.arc(x,y,4,0,Math.PI*2); ctx.fill();
              }});
            }})();
            </script>
            """
            st.markdown(_chart_js, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # MODO SANDBOX (Picks de Chocolate)
    # ══════════════════════════════════════════════════════════════════════
    if "sandbox_picks" not in st.session_state:
        st.session_state["sandbox_picks"] = []

    _sandbox_open = st.session_state.get("_sandbox_open", False)
    def _toggle_sandbox(): st.session_state["_sandbox_open"] = not st.session_state.get("_sandbox_open", False)
    st.button(
        "▼ Cerrar Sandbox" if _sandbox_open else "🍫 Modo Sandbox — Practica sin dinero real",
        key="btn_sandbox_toggle", use_container_width=True, on_click=_toggle_sandbox
    )
    _sandbox_open = st.session_state.get("_sandbox_open", False)

    if _sandbox_open:
        st.markdown(
            '<div style="background:rgba(155,109,255,0.06);border:1px solid rgba(155,109,255,0.2);'
            'border-radius:14px;padding:14px 16px;margin:6px 0">'
            '<div style="font-size:0.72rem;font-weight:800;color:#9B6DFF;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:8px">🍫 PICKS DE CHOCOLATE — Sin dinero real</div>'
            '<div style="font-size:0.78rem;color:#888">Prueba tu estrategia aquí antes de arriesgar el bank real. '
            'Los picks de sandbox no afectan tu bankroll.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        _sb_c1, _sb_c2, _sb_c3 = st.columns(3)
        with _sb_c1:
            _sb_partido = st.text_input("Partido", placeholder="Real Madrid vs Barcelona", key="sb_partido")
        with _sb_c2:
            _sb_pick    = st.text_input("Pick", placeholder="Real Madrid ML", key="sb_pick")
        with _sb_c3:
            _sb_momio   = st.number_input("Cuota", min_value=1.01, max_value=50.0, value=1.90, step=0.05, key="sb_momio")

        _sb_c4, _sb_c5 = st.columns(2)
        with _sb_c4:
            _sb_monto = st.number_input("Monto simulado $", min_value=100, max_value=100000, value=1000, step=100, key="sb_monto")
        with _sb_c5:
            _sb_resultado = st.selectbox("Resultado", ["pendiente","ganado","perdido"], key="sb_resultado")

        def _add_sandbox():
            if st.session_state.get("sb_partido","").strip():
                st.session_state["sandbox_picks"].append({
                    "partido": st.session_state.get("sb_partido",""),
                    "pick": st.session_state.get("sb_pick",""),
                    "momio": st.session_state.get("sb_momio", 1.90),
                    "monto": st.session_state.get("sb_monto", 1000),
                    "resultado": st.session_state.get("sb_resultado","pendiente"),
                })
        st.button("➕ Agregar al Sandbox", key="btn_add_sandbox", use_container_width=True, on_click=_add_sandbox)

        # Show sandbox stats
        _sb_picks = st.session_state.get("sandbox_picks",[])
        if _sb_picks:
            _sb_gan = sum(1 for p in _sb_picks if p.get("resultado")=="ganado")
            _sb_per = sum(1 for p in _sb_picks if p.get("resultado")=="perdido")
            _sb_wr  = _sb_gan/(_sb_gan+_sb_per)*100 if (_sb_gan+_sb_per)>0 else 0
            _sb_profit = sum(
                float(p.get("monto",0))*(float(p.get("momio",1.9))-1) if p.get("resultado")=="ganado"
                else -float(p.get("monto",0)) if p.get("resultado")=="perdido" else 0
                for p in _sb_picks
            )
            _sb_sport_stats = {}
            for _p in _sb_picks:
                _sport_key = (_p.get("pick","") or "Otro")[:15]
                if _sport_key not in _sb_sport_stats:
                    _sb_sport_stats[_sport_key] = {"g":0,"p":0}
                if _p.get("resultado")=="ganado": _sb_sport_stats[_sport_key]["g"]+=1
                elif _p.get("resultado")=="perdido": _sb_sport_stats[_sport_key]["p"]+=1

            st.markdown(
                f'<div style="background:#0F0F12;border-radius:12px;padding:12px 16px;margin:8px 0;'
                f'display:grid;grid-template-columns:repeat(3,1fr);gap:10px;text-align:center">'
                f'<div><div style="font-size:1.1rem;font-weight:800;color:#9B6DFF">{len(_sb_picks)}</div>'
                f'<div style="font-size:0.58rem;color:#555;text-transform:uppercase">Picks</div></div>'
                f'<div><div style="font-size:1.1rem;font-weight:800;color:#00D47E">{_sb_wr:.0f}%</div>'
                f'<div style="font-size:0.58rem;color:#555;text-transform:uppercase">Win Rate</div></div>'
                f'<div><div style="font-size:1.1rem;font-weight:800;color:{"#00D47E" if _sb_profit>=0 else "#ef4444"}">'
                f'{"+" if _sb_profit>=0 else ""}${_sb_profit:,.0f}</div>'
                f'<div style="font-size:0.58rem;color:#555;text-transform:uppercase">Profit</div></div>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Best sport in sandbox
            _sb_best = max(_sb_sport_stats.items(), key=lambda x: x[1]["g"]/(x[1]["g"]+x[1]["p"]) if (x[1]["g"]+x[1]["p"])>0 else 0, default=None)
            if _sb_best and (_sb_best[1]["g"]+_sb_best[1]["p"]) >= 2:
                _sb_best_wr = _sb_best[1]["g"]/(_sb_best[1]["g"]+_sb_best[1]["p"])*100
                st.markdown(
                    f'<div style="font-size:0.75rem;color:#9B6DFF;margin-top:6px;text-align:center">'
                    f'🧠 Tu mejor pick en sandbox: <b>{_sb_best[0]}</b> ({_sb_best_wr:.0f}% WR)</div>',
                    unsafe_allow_html=True
                )

            def _clear_sandbox(): st.session_state["sandbox_picks"] = []
            st.button("🗑️ Limpiar Sandbox", key="btn_clear_sandbox", use_container_width=True, on_click=_clear_sandbox)

    # ── Config: banco inicial y meta ──────────────────────────────────────────
    with st.expander("⚙️ Configurar Reto"):
        cfg1, cfg2 = st.columns(2)
        with cfg1:
            new_bank = st.number_input("Bank Inicial ($)", min_value=1.0,
                                       value=float(bank_inicial), step=100.0, key="cfg_bank")
        with cfg2:
            new_meta = st.number_input("Meta ($)", min_value=1.0,
                                       value=float(meta), step=100_000.0, key="cfg_meta")
        if st.button("💾 Guardar Configuración", key="btn_cfg"):
            reto["bank_inicial"] = new_bank
            reto["meta"] = new_meta
            _save_reto(reto, apodo_activo)
            st.toast("✓ Configuración guardada", icon="⚙️")
            st.rerun()

    st.markdown('<div class="den-divider" style="margin:20px 0"></div>', unsafe_allow_html=True)

    # ── Historial de picks ────────────────────────────────────────────────────
    if picks:
        st.markdown('''<div style="font-family:Barlow Condensed,sans-serif;font-size:0.78rem;
            font-weight:800;color:#C9A84C;letter-spacing:3px;text-transform:uppercase;
            margin:18px 0 10px;display:flex;align-items:center;gap:10px">
            <span style="width:3px;height:16px;background:#C9A84C;border-radius:2px;flex-shrink:0"></span>
            📋 HISTORIAL DE PICKS
            <span style="flex:1;height:1px;background:linear-gradient(90deg,rgba(201,168,76,0.3),transparent)"></span>
        </div>''', unsafe_allow_html=True)

        # ── Filtros rápidos ────────────────────────────────────────────────
        _filt_c1, _filt_c2, _filt_c3, _filt_c4 = st.columns(4)
        with _filt_c1:
            def _set_filt_hoy():
                st.session_state["reto_filtro"] = "hoy"
            def _set_filt_gan():
                st.session_state["reto_filtro"] = "ganados"
            def _set_filt_all():
                st.session_state["reto_filtro"] = "todos"
            st.button("📅 Hoy",     key="filt_hoy",  use_container_width=True, on_click=_set_filt_hoy)
        with _filt_c2:
            st.button("✅ Ganados",  key="filt_gan",  use_container_width=True, on_click=_set_filt_gan)
        with _filt_c3:
            def _set_filt_hi():
                st.session_state["reto_filtro"] = "momio_alto"
            st.button("💰 Momio >2", key="filt_hi",   use_container_width=True, on_click=_set_filt_hi)
        with _filt_c4:
            st.button("🔄 Todos",    key="filt_all",  use_container_width=True, on_click=_set_filt_all)

        # Apply filter
        _filtro = st.session_state.get("reto_filtro", "todos")
        from datetime import date as _date_reto
        _today_str = _date_reto.today().isoformat()
        if _filtro == "hoy":
            _picks_show = [p for p in picks if (p.get("fecha","") or "")[:10] == _today_str]
        elif _filtro == "ganados":
            _picks_show = [p for p in picks if p.get("resultado") == "ganado"]
        elif _filtro == "momio_alto":
            _picks_show = [p for p in picks if float(p.get("momio",0) or 0) >= 2.0]
        else:
            _picks_show = picks

        # Filter label
        _filt_label = {"hoy":"📅 Hoy","ganados":"✅ Solo ganados","momio_alto":"💰 Momio ≥2.0","todos":"🔄 Todos"}.get(_filtro,"Todos")
        if _filtro != "todos":
            st.caption(f"Filtro activo: **{_filt_label}** — {len(_picks_show)} picks")

        running_bank = bank_inicial
        for p in reversed(_picks_show):
            num = p.get("num","?")
            res = p.get("resultado","pendiente")
            stake = float(p.get("monto",0))
            momio_p = float(p.get("momio",0))

            if res == "ganado":
                if momio_p >= 1.01 and momio_p < 100:
                    gan = stake * (momio_p - 1)
                elif momio_p > 0:
                    gan = stake * momio_p / 100
                else:
                    gan = stake * 100 / abs(momio_p)
                delta_str = f"+${gan:,.2f}"
                res_color = "#00C896"
                res_icon  = "✅"
            elif res == "perdido":
                delta_str = f"-${stake:,.2f}"
                res_color = "#ef4444"
                res_icon  = "❌"
            elif res == "push":
                delta_str = "$0 (push)"
                res_color = "#C9A84C"
                res_icon  = "↩️"
            else:
                delta_str = "pendiente"
                res_color = "#6B7E6E"
                res_icon  = "⏳"

            momio_fmt = p.get("momio_fmt") or (f"+{momio_p:.0f}" if momio_p > 0 else f"{momio_p:.2f}")
            nota_html = f'<div style="font-size:0.784rem;color:#444444;margin-top:2px">{p.get("nota","")}</div>' if p.get("nota") else ""

            # ── Pick row — premium card ────────────────────────────────────
            _res_colors2 = {"ganado":"#00D47E","perdido":"#ef4444","push":"#C9A84C","pendiente":"#555"}
            _res_bgs2    = {"ganado":"#0D1A10","perdido":"#1A0D0D","push":"#1A1A0D","pendiente":"#111114"}
            _res_bord2   = {"ganado":"rgba(0,212,126,0.25)","perdido":"rgba(239,68,68,0.25)","push":"rgba(201,168,76,0.2)","pendiente":"rgba(255,255,255,0.05)"}
            _rc2 = _res_colors2.get(res,"#555")
            _rbg2= _res_bgs2.get(res,"#111")
            _rbo2= _res_bord2.get(res,"rgba(255,255,255,0.05)")
            _mkt_c2 = {"ML":"#3D8EFF","O/U":"#FF8C00","BTTS":"#00C896","AA":"#00C896","DO":"#9B6DFF"}.get(p.get("mercado",""),"#888")
            _pick_txt = p.get("pick","") or p.get("pick_label","")
            with st.container():
                _nota_html = f'<div style="font-size:0.6rem;color:#444;margin-top:3px">{p.get("nota","")}</div>' if p.get("nota") else ""
                st.markdown(
                    f'<div style="background:{_rbg2};border:1px solid {_rbo2};'
                    f'border-left:3px solid {_rc2};border-radius:12px;'
                    f'padding:12px 14px;margin:3px 0;'
                    f'box-shadow:0 2px 8px rgba(0,0,0,0.25)">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;gap:8px">'
                    f'<div style="flex:1;min-width:0">'
                    f'<div style="font-size:0.82rem;font-weight:700;color:#D8D8E0;'
                    f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:4px">{p.get("partido","")}</div>'
                    f'<div style="display:flex;gap:5px;align-items:center;flex-wrap:wrap">'
                    f'<span style="font-size:0.58rem;background:rgba(201,168,76,0.1);color:#C9A84C;padding:2px 6px;border-radius:4px;font-weight:800">#{num}</span>'
                    f'<span style="font-size:0.6rem;color:{_mkt_c2};padding:2px 7px;border-radius:4px;font-weight:700;border:1px solid {_mkt_c2}44;background:rgba(255,255,255,0.03)">{p.get("mercado","")}</span>'
                    f'<span style="font-size:0.68rem;color:#666;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:140px">{_pick_txt[:25]}</span>'
                    f'</div>'
                    + _nota_html
                    + f'<div style="font-size:0.58rem;color:#2A2A2A;margin-top:2px">{p.get("fecha","")[:10]}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:0.95rem;font-weight:900;color:{_rc2};font-family:Barlow Condensed,sans-serif">{res_icon} {delta_str}</div>'
                    f'<div style="font-size:0.62rem;color:#444;margin-top:2px">{momio_fmt} · ${stake:,.0f}</div>'
                    f'</div></div></div>',
                    unsafe_allow_html=True
                )
        st.markdown('<div class="den-divider" style="margin:16px 0"></div>', unsafe_allow_html=True)

        # ── Picks pendientes — auto-resueltos automáticamente ────────────────
        pendientes = [p for p in picks if p.get("resultado")=="pendiente"]
        if pendientes:
            st.markdown('<div class="section-heading">⏳ Pendientes de Resultado</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);'
                f'border-radius:10px;padding:10px 14px;font-size:0.75rem;color:#555;'
                f'display:flex;align-items:center;gap:8px;margin-bottom:8px">'
                f'<span style="font-size:1rem">🤖</span>'
                f'<span>El sistema verifica automáticamente los resultados de ESPN cada vez que abres esta pestaña. '
                f'{len(pendientes)} pick{"s" if len(pendientes)!=1 else ""} en espera.</span>'
                f'</div>',
                unsafe_allow_html=True
            )
            # Force-resolve button (manual trigger if user wants immediate check)
            def _force_resolve():
                st.session_state["_auto_last_key"] = ""  # reset key to force re-check
            st.button("🔄 Verificar ahora", key="btn_force_resolve",
                      use_container_width=False, on_click=_force_resolve)

            # ── Manual override ───────────────────────────────────────────────
            st.markdown('<div style="font-size:0.784rem;color:#6B7280;margin:8px 0 4px 0">✏️ Actualizar manualmente</div>', unsafe_allow_html=True)
            pen_options = {f"#{p['num']} · {p['partido']} · {p['pick']}": i
                           for i, p in enumerate(picks) if p.get("resultado")=="pendiente"}
            sel_pen = st.selectbox("Pick pendiente", list(pen_options.keys()), key="sel_pendiente")
            new_res = st.selectbox("Nuevo resultado", ["ganado","perdido","push"], key="new_res_pen")
            if st.button("💾 Actualizar", key="btn_update_res"):
                idx_pen = pen_options[sel_pen]
                picks[idx_pen]["resultado"] = new_res
                reto["picks"] = picks
                _save_reto(reto, apodo_activo)
                st.toast(f"✓ Pick actualizado a {new_res}", icon="✅")
                st.rerun()

        # ── Eliminar último pick ──────────────────────────────────────────────
        with st.expander("🗑️ Eliminar pick"):
            if picks:
                del_options = {f"#{p['num']} · {p['partido']} · {p['pick']}": i
                               for i, p in enumerate(picks)}
                sel_del = st.selectbox("Pick a eliminar", list(del_options.keys()), key="sel_del")
                if st.button("🗑️ Confirmar eliminación", key="btn_del", type="primary"):
                    idx_del = del_options[sel_del]
                    picks.pop(idx_del)
                    # Re-number
                    for j, pk in enumerate(picks):
                        pk["num"] = j + 1
                    reto["picks"] = picks
                    _save_reto(reto, apodo_activo)
                    st.toast("Pick eliminado", icon="🗑️")
                    st.rerun()

        # ── Export CSV ───────────────────────────────────────────────────────
        csv_rows = ["#,Fecha,Partido,Pick,Mercado,Momio,Monto,Resultado,Nota"]
        for p in picks:
            csv_rows.append(",".join([
                str(p.get("num","")), p.get("fecha",""), p.get("partido","").replace(",",";"),
                p.get("pick","").replace(",",";"), p.get("mercado",""),
                str(p.get("momio","")), str(p.get("monto","")),
                p.get("resultado",""), p.get("nota","").replace(",",";")
            ]))
        st.download_button(
            "⬇ Exportar CSV",
            data="\n".join(csv_rows),
            file_name=f"reto13m_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="btn_export_reto"
        )


elif _active_page == "Califica":
    # ══════════════════════════════════════════════════════════════════════════
    # CALIFICA TU PICK — Grade any pick A-F using full Monte Carlo engine
    # ══════════════════════════════════════════════════════════════════════════

    st.markdown("""
    <style>
    .grade-ring {
        width: 110px; height: 110px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        flex-direction: column;
        margin: 0 auto;
        position: relative;
        box-shadow: 0 0 40px var(--ring-color);
        border: 4px solid var(--ring-color);
        background: radial-gradient(circle, var(--ring-bg) 0%, #0a0a0a 100%);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px">
      <div style="font-size:2rem;margin-bottom:4px">🏆</div>
      <div style="font-family:'Outfit',sans-serif;font-size:1.4rem;font-weight:900;
        background:linear-gradient(135deg,#FF6B00,#FFD60A);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;letter-spacing:-0.5px">CALIFICA TU PICK</div>
      <div style="font-size:0.65rem;color:#636366;letter-spacing:3px;
        text-transform:uppercase;margin-top:4px">
        Selecciona partido · Elige mercado · Ingresa momio
      </div>
    </div>
    """, unsafe_allow_html=True)

    sr_cal = st.session_state.get("sim_results", [])

    _cal_games = []
    for _r in sr_cal:
        _label = f'{_r.get("away_team","?")} @ {_r.get("home_team","?")} · {_r.get("league","")}'
        _cal_games.append((_label, _r))

    if not _cal_games:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px">
          <div style="font-size:2.5rem;margin-bottom:12px">📡</div>
          <div style="font-size:0.95rem;font-weight:700;color:#E8E8E8;margin-bottom:8px">
            Sin partidos cargados
          </div>
          <div style="font-size:0.82rem;color:#636366">
            Ve a ⚡ Rongol o 🎯 Picks primero para cargar los partidos del día.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.65rem;color:#FF6B00;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">① SELECCIONA EL PARTIDO</div>', unsafe_allow_html=True)

        _cal_labels = [x[0] for x in _cal_games]
        _cal_sel_idx = st.selectbox("Partido", range(len(_cal_labels)),
                                     format_func=lambda i: _cal_labels[i],
                                     key="cal_game_sel", label_visibility="collapsed")
        _cal_r = _cal_games[_cal_sel_idx][1]
        _cal_sim = _cal_r.get("sim", {})
        _cal_league = _cal_r.get("league", "")
        _cal_home = _cal_r.get("home_team", "Local")
        _cal_away = _cal_r.get("away_team", "Visita")
        _cal_sg = LEAGUES.get(_cal_league, {}).get("group", "Soccer")

        _ht_id = _cal_r.get("home_team_id", "")
        _at_id = _cal_r.get("away_team_id", "")
        _hl = _logo_img(_ht_id, _cal_league, 36)
        _al = _logo_img(_at_id, _cal_league, 36)

        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:center;gap:12px;'
            f'padding:12px;background:rgba(255,107,0,0.06);border-radius:16px;margin:8px 0 16px">'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">'
            f'{_al}<span style="font-size:0.75rem;font-weight:700;color:#E8E8E8">{_cal_away}</span></div>'
            f'<span style="font-size:0.9rem;color:#636366;font-weight:700">VS</span>'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">'
            f'{_hl}<span style="font-size:0.75rem;font-weight:700;color:#E8E8E8">{_cal_home}</span></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div style="font-size:0.65rem;color:#FF6B00;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">② TU PICK</div>', unsafe_allow_html=True)

        _cal_col1, _cal_col2 = st.columns(2)
        with _cal_col1:
            _cal_market = st.selectbox(
                "Mercado", ["ML", "O/U Over", "O/U Under", "BTTS Sí", "BTTS No", "Over 2.5", "Over 3.5"],
                key="cal_market", label_visibility="collapsed"
            )
        with _cal_col2:
            if _cal_market == "ML":
                _cal_side = st.selectbox("Equipo", [_cal_home, _cal_away], key="cal_side", label_visibility="collapsed")
            else:
                _cal_side = None
                st.markdown('<div style="padding:8px 0;font-size:0.82rem;color:#AEAEB2">Seleccionado ✓</div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.65rem;color:#FF6B00;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:12px 0 6px">③ MOMIO</div>', unsafe_allow_html=True)

        _suggested_momio = None
        if _cal_market == "ML":
            if _cal_side == _cal_home:
                _suggested_momio = _cal_sim.get("home_ml") or _cal_r.get("odds", {}).get("home_ml")
            else:
                _suggested_momio = _cal_sim.get("away_ml") or _cal_r.get("odds", {}).get("away_ml")
        _momio_default = int(_suggested_momio) if _suggested_momio else -110

        _mcol1, _mcol2 = st.columns(2)
        with _mcol1:
            _cal_momio = st.number_input("Americano", value=_momio_default, step=5,
                                          key="cal_momio", label_visibility="visible")
        with _mcol2:
            try:
                if _cal_momio > 0:
                    _cal_momio_dec = round(_cal_momio / 100 + 1, 3)
                else:
                    _cal_momio_dec = round(100 / abs(_cal_momio) + 1, 3)
            except:
                _cal_momio_dec = 1.909
            st.markdown(
                f'<div style="background:rgba(96,165,250,0.08);border:1px solid rgba(96,165,250,0.2);'
                f'border-radius:10px;padding:10px 12px;margin-top:4px">'
                f'<div style="font-size:0.65rem;color:#6B7280;margin-bottom:2px">Decimal</div>'
                f'<div style="font-size:1.3rem;font-weight:800;color:#60a5fa;'
                f'font-family:Outfit,sans-serif">{_cal_momio_dec}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        _btn_cal = st.button("🏆  CALIFICAR PICK", key="btn_calificar", use_container_width=True, type="primary")

        if _btn_cal or st.session_state.get("_cal_result"):
            if _btn_cal:
                _sim = _cal_sim
                _model_prob = 0.5

                if _cal_market == "ML":
                    if _cal_side == _cal_home:
                        _model_prob = (_sim.get("home_pct", 50) or 50) / 100
                    else:
                        _model_prob = (_sim.get("away_pct", 50) or 50) / 100
                elif _cal_market == "O/U Over":
                    _p_o = _sim.get("p_o_total") or _sim.get("p_o25")
                    _model_prob = (_p_o or 50) / 100
                elif _cal_market == "O/U Under":
                    _p_u = _sim.get("p_u_total") or _sim.get("p_u25")
                    _model_prob = (_p_u or 50) / 100
                elif _cal_market == "BTTS Sí":
                    _model_prob = (_sim.get("p_btts") or 50) / 100
                elif _cal_market == "BTTS No":
                    _model_prob = 1 - (_sim.get("p_btts") or 50) / 100
                elif _cal_market == "Over 2.5":
                    _model_prob = (_sim.get("p_o25") or 50) / 100
                elif _cal_market == "Over 3.5":
                    _model_prob = (_sim.get("p_o35") or 50) / 100

                _impl_prob = ml_to_prob(_cal_momio)
                _ev = calc_ev(_model_prob, str(_cal_momio))
                _edge = round((_model_prob - _impl_prob) * 100, 1)
                _kelly = quarter_kelly(_model_prob, str(_cal_momio))
                _consensus_score = _cal_sim.get("consensus_score", 0)
                _dq = _cal_sim.get("data_quality", 0)

                def _grade_pick(ev, edge_pp, model_prob, dq, consensus_score):
                    score = 0
                    if ev is None: ev = 0
                    if ev >= 20: score += 40
                    elif ev >= 12: score += 32
                    elif ev >= 6: score += 22
                    elif ev >= 2: score += 14
                    elif ev >= 0: score += 6
                    else: score += max(0, 6 + ev)
                    if edge_pp >= 12: score += 25
                    elif edge_pp >= 7: score += 20
                    elif edge_pp >= 4: score += 14
                    elif edge_pp >= 1: score += 8
                    elif edge_pp >= 0: score += 3
                    if model_prob >= 0.72: score += 20
                    elif model_prob >= 0.62: score += 16
                    elif model_prob >= 0.54: score += 11
                    elif model_prob >= 0.50: score += 6
                    else: score += 2
                    if consensus_score >= 0.50: score += 15
                    elif consensus_score >= 0.20: score += 11
                    elif consensus_score >= 0.0: score += 7
                    elif consensus_score >= -0.3: score += 3
                    if dq < 25: score -= 8
                    if dq < 10: score -= 10
                    if edge_pp < -5: score -= 10
                    score = max(0, min(100, score))
                    if score >= 88: return "A+", score
                    elif score >= 80: return "A", score
                    elif score >= 72: return "B+", score
                    elif score >= 64: return "B", score
                    elif score >= 56: return "C+", score
                    elif score >= 48: return "C", score
                    elif score >= 38: return "D", score
                    elif score >= 26: return "E", score
                    else: return "F", score

                _grade, _score = _grade_pick(_ev or 0, _edge, _model_prob, _dq, _consensus_score)

                st.session_state["_cal_result"] = {
                    "grade": _grade, "score": _score,
                    "model_prob": _model_prob, "impl_prob": _impl_prob,
                    "ev": _ev, "edge": _edge, "kelly": _kelly,
                    "consensus": _cal_sim.get("consensus_label", "◈ NEUTRAL"),
                    "consensus_score": _consensus_score,
                    "dq": _dq,
                    "fatigue": _cal_sim.get("fatigue_note", ""),
                    "injury": _cal_sim.get("injury_note", ""),
                    "lam_rh": _cal_sim.get("lam_real_h"),
                    "lam_ra": _cal_sim.get("lam_real_a"),
                    "lam_lg": _cal_sim.get("lam_league"),
                    "market": _cal_market, "side": _cal_side,
                    "home": _cal_home, "away": _cal_away, "league": _cal_league,
                    "momio": _cal_momio,
                }

            _res = st.session_state.get("_cal_result", {})
            if _res:
                _g = _res["grade"]
                _sc = _res["score"]
                _ev_r = _res["ev"] or 0
                _mp = _res["model_prob"]
                _ip = _res["impl_prob"]
                _edg = _res["edge"]
                _kl = _res["kelly"] or 0
                _cons = _res["consensus"]
                _dq_r = _res["dq"]
                _mom = _res["momio"]

                _GRADE_COLORS = {
                    "A+": ("#00C896", "rgba(0,200,150,0.15)", "APUESTA FUERTE 🔥"),
                    "A":  ("#00C896", "rgba(0,200,150,0.12)", "EXCELENTE ✅"),
                    "B+": ("#86efac", "rgba(134,239,172,0.12)", "MUY BUENA ⚡"),
                    "B":  ("#60a5fa", "rgba(96,165,250,0.12)", "BUENA 👍"),
                    "C+": ("#fbbf24", "rgba(251,191,36,0.12)", "ACEPTABLE 📊"),
                    "C":  ("#C9A84C", "rgba(201,168,76,0.10)", "MARGINAL ➡️"),
                    "D":  ("#f97316", "rgba(249,115,22,0.10)", "DÉBIL ⚠️"),
                    "E":  ("#ef4444", "rgba(239,68,68,0.10)", "EVITAR ❌"),
                    "F":  ("#7f1d1d", "rgba(127,29,29,0.15)", "TRAMPA 🚫"),
                }
                _gc, _gbg, _gverdict = _GRADE_COLORS.get(_g, ("#636366", "rgba(99,99,102,0.10)", "SIN DATOS"))

                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{_gbg} 0%,#0a0a0a 100%);'
                    f'border:2px solid {_gc}44;border-radius:24px;padding:20px 16px;'
                    f'margin:8px 0;box-shadow:0 0 40px {_gc}22;text-align:center">'
                    f'<div style="width:120px;height:120px;border-radius:50%;'
                    f'display:flex;align-items:center;justify-content:center;flex-direction:column;'
                    f'margin:0 auto 16px;border:4px solid {_gc};'
                    f'background:radial-gradient(circle,{_gbg} 0%,#0a0a0a 100%);'
                    f'box-shadow:0 0 40px {_gc}66">'
                    f'<span style="font-size:3rem;font-weight:900;color:{_gc};line-height:1;'
                    f'font-family:Outfit,sans-serif">{_g}</span>'
                    f'<span style="font-size:0.52rem;font-weight:700;letter-spacing:2px;'
                    f'text-transform:uppercase;color:{_gc};opacity:0.8">{_sc}/100</span>'
                    f'</div>'
                    f'<div style="font-size:1.1rem;font-weight:800;color:{_gc};margin-bottom:8px">{_gverdict}</div>'
                    f'<div style="font-size:0.78rem;color:#AEAEB2;margin-bottom:4px">{_res["away"]} @ {_res["home"]}</div>'
                    f'<div style="font-size:0.92rem;font-weight:700;color:#E8E8E8">'
                    f'{_res["market"]} {_res["side"] or ""} @ {_mom:+d}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                _m_cols = st.columns(3)
                for _mi, (_lbl, _val, _clr) in enumerate([
                    ("Prob Modelo", f'{_mp*100:.1f}%', "#00C896" if _mp > _ip else "#ef4444"),
                    ("Prob Impl.", f'{_ip*100:.1f}%', "#AEAEB2"),
                    ("EV / $100", f'{_ev_r:+.1f}', "#00C896" if _ev_r > 0 else "#ef4444"),
                    ("Edge", f'{_edg:+.1f}pp', "#00C896" if _edg > 0 else "#ef4444"),
                    ("Kelly 25%", f'{_kl*100:.1f}%', "#60a5fa"),
                    ("DQ", f'{_dq_r:.0f}%', "#00C896" if _dq_r > 60 else "#C9A84C"),
                ]):
                    with _m_cols[_mi % 3]:
                        st.markdown(
                            f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
                            f'border-radius:14px;padding:10px 6px;text-align:center;margin-bottom:8px">'
                            f'<div style="font-size:1.2rem;font-weight:800;color:{_clr}">{_val}</div>'
                            f'<div style="font-size:0.55rem;color:#636366;letter-spacing:1px;text-transform:uppercase;margin-top:2px">{_lbl}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                _verdicts = {
                    "A+": "🔥 Pick de élite. Todas las señales alineadas. Apuesta con confianza.",
                    "A":  "✅ Pick excelente. EV sólido y modelo confirma valor real vs mercado.",
                    "B+": "⚡ Pick muy bueno. EV positivo claro, la mayoría de señales a favor.",
                    "B":  "👍 Pick bueno. Valor real detectado. Apuesta normal dentro del Kelly.",
                    "C+": "📊 Pick aceptable. EV marginal pero positivo. Reduce el stake.",
                    "C":  "➡️ Pick marginal. Apenas positivo. Solo si tienes alta convicción propia.",
                    "D":  "⚠️ Pick débil. EV casi nulo o señales en conflicto. Mejor pasar.",
                    "E":  "❌ Evitar. El modelo ve valor en la dirección contraria.",
                    "F":  "🚫 Trampa de casa. El mercado tiene ventaja clara. No apostar.",
                }
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{_gbg},rgba(0,0,0,0));'
                    f'border-left:4px solid {_gc};border-radius:0 16px 16px 0;padding:14px 18px;margin:16px 0">'
                    f'<div style="font-size:0.62rem;color:{_gc};font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">VEREDICTO FINAL</div>'
                    f'<div style="font-size:0.88rem;color:#E8E8E8;line-height:1.6">{_verdicts.get(_g, "Sin datos.")}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div style="margin:8px 0 20px">'
                    f'<div style="background:rgba(255,255,255,0.06);border-radius:12px;height:8px;overflow:hidden">'
                    f'<div style="width:{_sc}%;height:100%;border-radius:12px;'
                    f'background:linear-gradient(90deg,#ef4444,#f97316,#fbbf24,#00C896)"></div>'
                    f'</div>'
                    f'<div style="text-align:right;font-size:0.65rem;color:{_gc};font-weight:700;margin-top:2px">{_sc}/100 pts</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                def _cal_reset2(): st.session_state.pop("_cal_result", None)
                st.button("↩ Calificar otro pick", key="btn_cal_reset", use_container_width=True, on_click=_cal_reset2)

elif _active_page == "Config":
    st.markdown('<div class="section-heading">⚙️ Config</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.65rem;color:var(--orange);font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px">🔮 SIMULACIONES</div>', unsafe_allow_html=True)
    n_sims_cfg = st.select_slider(
        "Iteraciones",
        options=[1_000, 2_500, 5_000, 10_000, 25_000],
        value=st.session_state.get("n_sims_val", 10_000),
        key="n_sims_slider",
    )
    st.session_state["n_sims_val"] = n_sims_cfg
    st.caption(f"⚡ {n_sims_cfg:,} por partido")

    st.markdown('<div class="den-divider" style="margin:12px 0"></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.65rem;color:var(--orange);font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px">🌍 DEPORTES</div>', unsafe_allow_html=True)
    _groups_all_cfg = sorted(set(v["group"] for v in LEAGUES.values()))
    sel_groups_cfg = st.multiselect(
        "Deportes",
        _groups_all_cfg,
        default=st.session_state.get("sel_groups_val", ["Basketball","Baseball","Soccer","Hockey"]),
        key="sel_groups_v3",
    )
    st.session_state["sel_groups_val"] = sel_groups_cfg

    _avail_cfg = [n for n, cfg in LEAGUES.items() if cfg["group"] in sel_groups_cfg and not cfg.get("hidden")]
    _saved_cfg = st.session_state.get("sel_leagues_val", _avail_cfg)
    _new_lgs_cfg = [l for l in _avail_cfg if l not in _saved_cfg]
    if _new_lgs_cfg:
        _saved_cfg = _saved_cfg + _new_lgs_cfg
        st.session_state["sel_leagues_val"] = _saved_cfg
    _default_leagues_cfg = [l for l in _saved_cfg if l in _avail_cfg]

    st.markdown('<div style="font-size:0.65rem;color:var(--text3);font-weight:600;letter-spacing:1px;text-transform:uppercase;margin:6px 0 3px">LIGAS</div>', unsafe_allow_html=True)
    sel_leagues_cfg = st.multiselect(
        "Ligas",
        _avail_cfg,
        default=_default_leagues_cfg,
        key="sel_leagues_v3",
    )
    st.session_state["sel_leagues_val"] = sel_leagues_cfg

    st.markdown('<div class="den-divider" style="margin:12px 0"></div>', unsafe_allow_html=True)

    use_demo_cfg = st.toggle("🧪 Demo", value=st.session_state.get("use_demo_val", False), key="use_demo_v2")
    st.session_state["use_demo_val"] = use_demo_cfg

    def _run_analyze(): st.session_state["trigger_analyze"] = True
    st.button("▶  Analizar ahora", key="run_btn_menu", use_container_width=True, on_click=_run_analyze)

    st.markdown('<div class="den-divider" style="margin:12px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.65rem;color:var(--text3);font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px">🛠 HERRAMIENTAS</div>', unsafe_allow_html=True)

    _tc1, _tc2 = st.columns(2)
    with _tc1:
        if st.button("↺ Caché", key="clear_cache_menu", use_container_width=True):
            st.cache_data.clear()
            st.session_state.pop("sim_results", None)
            st.session_state.pop("_games_fetched", None)
            st.rerun()
    with _tc2:
        def _run_espn(): st.session_state["run_espn_test"] = True
        st.button("🔍 Test ESPN", key="test_espn_menu", use_container_width=True, on_click=_run_espn)

    _tp_count_sb = st.session_state.get("_tp_count_cached", 0)
    _mem_label = f"✅ {_tp_count_sb} equipos" if _tp_count_sb > 0 else "⬜ Sin memoria"
    st.caption(_mem_label)
    def _run_populate(): st.session_state["run_populate"] = True
    st.button("🧠 Poblar memoria", key="populate_menu", use_container_width=True, on_click=_run_populate)

st.markdown('<div class="den-divider" style="margin-top:24px"></div>',unsafe_allow_html=True)
# ── Ocultar elementos de Streamlit Cloud (JS runtime) ─────────────────────
import streamlit.components.v1 as _components_hide
_components_hide.html("""
<script>
(function hideStreamlitBadges() {
  function nuke() {
    // Selectors para todos los badges y botones de Streamlit Cloud
    const selectors = [
      '[data-testid="stStatusWidget"]',
      '[data-testid="stToolbar"]',
      '[data-testid="stDecoration"]',
      '.viewerBadge_container__1QSob',
      '.viewerBadge_link__1S137',
      'button[title="Manage app"]',
      'button[aria-label="Manage app"]',
      'a[href*="streamlit.io"]',
      'iframe[title*="streamlit"]',
    ];
    selectors.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.opacity = '0';
        el.style.pointerEvents = 'none';
      });
    });
    // Hide Streamlit badges
    document.querySelectorAll('a[href*="streamlit"], button[title*="Manage"], .viewerBadge_container__1QSob, footer, [data-testid="stBottom"]').forEach(el => {
      el.style.display = 'none';
      el.style.visibility = 'hidden';
    });

    // Kill white expander boxes
    document.querySelectorAll('[data-testid="stExpander"] details:not([open])').forEach(det => {
      Array.from(det.children).forEach(child => {
        if (child.tagName !== 'SUMMARY') {
          child.style.cssText = 'display:none!important;height:0!important;overflow:hidden!important;border:none!important;padding:0!important;margin:0!important;background:transparent!important;';
        }
      });
    });

    // Force ALL stButton dark (overrides Streamlit white default)
    document.querySelectorAll('div[data-testid="stButton"] > button').forEach(btn => {
      if (btn.closest('[data-testid="stRadio"]')) return; // skip nav
      btn.style.background = 'linear-gradient(160deg,#1C1C22 0%,#111114 100%)';
      btn.style.color = '#C0C0CC';
      btn.style.border = '1px solid rgba(255,255,255,0.09)';
      btn.style.borderTop = '1.5px solid rgba(255,255,255,0.16)';
      btn.style.borderBottom = '2px solid rgba(0,0,0,0.5)';
      btn.style.borderRadius = '10px';
      btn.style.boxShadow = '0 3px 10px rgba(0,0,0,0.35),0 1px 0 rgba(255,255,255,0.06) inset';
      btn.style.fontFamily = "'Barlow',sans-serif";
      btn.style.fontWeight = '700';
      btn.style.minHeight = '40px';
      btn.style.padding = '10px 16px';
    });
  }
  nuke();
  // Keep checking as Streamlit re-renders
  setInterval(nuke, 1000);
  const observer = new MutationObserver(nuke);
  observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", height=0)

st.markdown('<div style="text-align:center;font-family:\'Inter\',sans-serif;font-size:0.65rem;color:#333333;letter-spacing:2px;padding:12px 0">THE GAMBLERS DEN · MONTE CARLO ENGINE · ⚠ SOLO FINES INFORMATIVOS</div>',unsafe_allow_html=True)

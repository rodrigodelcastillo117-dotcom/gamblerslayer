"""
THE GAMBLERS DEN
Monte Carlo Sports Betting Analyzer
BTTS · O/U · Parlays · Doble Oportunidad
"""

import streamlit as st
import requests
import random
import math
import time
import os
import json
from datetime import datetime, timezone

st.set_page_config(
    page_title="The Gamblers Den",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cinzel:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --gold:    #C9A84C;
  --gold2:   #F0D080;
  --felt:    #0D2818;
  --felt2:   #0A1F12;
  --felt3:   #071610;
  --dark:    #060C08;
  --card:    #0F1F14;
  --card2:   #122318;
  --border:  #1E3825;
  --red:     #C0392B;
  --green:   #27AE60;
  --cyan:    #1ABC9C;
  --text:    #D4C5A0;
  --muted:   #6B7E6E;
  --white:   #F5EDD8;
}

* { box-sizing: border-box; }

.main, .stApp, .stMainBlockContainer {
  background-color: var(--dark) !important;
  color: var(--text) !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--dark); }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 3px; }

/* ── HEADER ── */
.den-header {
  text-align: center;
  padding: 2rem 0 1rem 0;
  position: relative;
}
.den-logo {
  font-family: 'Cinzel', serif;
  font-size: 3.8rem;
  font-weight: 900;
  color: var(--gold);
  letter-spacing: 8px;
  text-transform: uppercase;
  text-shadow: 0 0 40px rgba(201,168,76,0.5), 0 0 80px rgba(201,168,76,0.2);
  line-height: 1;
  margin: 0;
}
.den-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: var(--muted);
  letter-spacing: 6px;
  text-transform: uppercase;
  margin-top: 6px;
}
.den-divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  margin: 1rem 0;
  opacity: 0.5;
}
.den-corner {
  display: inline-block;
  color: var(--gold);
  opacity: 0.4;
  font-size: 1.2rem;
  margin: 0 12px;
}

/* ── METRIC TILES ── */
.stat-grid { display: flex; gap: 12px; margin: 12px 0; flex-wrap: wrap; }
.stat-tile {
  flex: 1; min-width: 100px;
  background: var(--card);
  border: 1px solid var(--border);
  border-top: 2px solid var(--gold);
  border-radius: 4px;
  padding: 14px 10px;
  text-align: center;
}
.stat-num {
  font-family: 'Cinzel', serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--gold);
  line-height: 1;
}
.stat-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  color: var(--muted);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 4px;
}

/* ── PICK CARD (THE MAIN ATTRACTION) ── */
.pick-card {
  background: linear-gradient(145deg, #0F2A14 0%, #0A1E10 50%, #112615 100%);
  border: 2px solid var(--gold);
  border-radius: 10px;
  padding: 0;
  margin: 14px 0;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(201,168,76,0.15),
    0 0 40px rgba(201,168,76,0.18),
    0 0 80px rgba(201,168,76,0.08),
    inset 0 1px 0 rgba(201,168,76,0.25);
  position: relative;
}
.pick-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, var(--gold) 20%, #FFE87C 50%, var(--gold) 80%, transparent 100%);
  box-shadow: 0 0 12px rgba(240,208,128,0.8);
}
.pick-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,0.4), transparent);
}
.pick-header {
  padding: 16px 20px 10px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 8px;
}
.pick-matchup {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--white);
}
.pick-league-badge {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.68rem;
  color: var(--gold);
  letter-spacing: 2px;
  text-transform: uppercase;
  background: rgba(201,168,76,0.1);
  border: 1px solid rgba(201,168,76,0.3);
  padding: 3px 10px;
  border-radius: 20px;
}
.pick-body { padding: 16px 20px; }

.pick-action {
  font-family: 'Cinzel', serif;
  font-size: 1.9rem;
  font-weight: 900;
  color: #FFE87C;
  text-shadow:
    0 0 20px rgba(255,232,124,0.7),
    0 0 40px rgba(201,168,76,0.4),
    0 2px 4px rgba(0,0,0,0.8);
  letter-spacing: 3px;
  margin: 10px 0 6px 0;
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  padding: 10px 0;
  border-bottom: 1px solid rgba(201,168,76,0.2);
}
.pick-action-arrow {
  color: #FFE87C;
  font-size: 2rem;
  filter: drop-shadow(0 0 8px rgba(255,232,124,0.8));
  animation: pulse-arrow 2s ease-in-out infinite;
}
@keyframes pulse-arrow {
  0%, 100% { opacity: 1; transform: translateX(0); }
  50% { opacity: 0.7; transform: translateX(4px); }
}

.market-chip {
  display: inline-block;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 3px;
  margin-right: 4px;
}
.chip-ml     { background: rgba(26,96,196,0.25); color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
.chip-btts   { background: rgba(39,174,96,0.2);  color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.chip-ou     { background: rgba(201,168,76,0.15); color: var(--gold2); border: 1px solid rgba(201,168,76,0.3); }
.chip-dc     { background: rgba(167,139,250,0.2); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }
.chip-parlay { background: rgba(26,188,156,0.2);  color: #1ABC9C; border: 1px solid rgba(26,188,156,0.3); }
.chip-warn   { background: rgba(192,57,43,0.2);   color: #e74c3c; border: 1px solid rgba(231,76,60,0.3); }

.stats-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin: 12px 0;
  padding: 12px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.stat-item { text-align: center; min-width: 70px; }
.stat-item-val {
  font-family: 'Cinzel', serif;
  font-size: 1.3rem;
  font-weight: 700;
  line-height: 1;
}
.stat-item-lbl {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.6rem;
  color: var(--muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 3px;
}
.val-gold   { color: var(--gold2); }
.val-green  { color: #4ade80; }
.val-cyan   { color: #1ABC9C; }
.val-blue   { color: #60a5fa; }
.val-purple { color: #a78bfa; }
.val-red    { color: #ef4444; }
.val-muted  { color: var(--muted); }

/* confidence badge */
.conf-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 20px;
}
.conf-high   { background: rgba(39,174,96,0.15);  color: #4ade80; border: 1px solid rgba(74,222,128,0.4); }
.conf-medium { background: rgba(201,168,76,0.15); color: var(--gold2); border: 1px solid rgba(201,168,76,0.4); }
.conf-low    { background: rgba(192,57,43,0.15);  color: #ef4444; border: 1px solid rgba(231,76,60,0.4); }

/* pick rationale */
.pick-rationale {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: var(--muted);
  line-height: 1.7;
  margin-top: 10px;
}
.pick-rationale b { color: var(--text); }

/* ── PARLAY CARD ── */
.parlay-card {
  background: linear-gradient(145deg, #061A14 0%, #091F1A 50%, #071815 100%);
  border: 2px solid rgba(26,188,156,0.8);
  border-radius: 10px;
  padding: 0;
  margin: 14px 0;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(26,188,156,0.12),
    0 0 40px rgba(26,188,156,0.20),
    0 0 80px rgba(26,188,156,0.08);
  position: relative;
}
.parlay-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, #1ABC9C, #7FFFD4, #1ABC9C, transparent);
  box-shadow: 0 0 12px rgba(26,188,156,0.9);
}
.parlay-header {
  background: linear-gradient(90deg, rgba(26,188,156,0.15), rgba(26,188,156,0.05));
  border-bottom: 1px solid rgba(26,188,156,0.25);
  padding: 14px 20px;
  font-family: 'Cinzel', serif;
  font-size: 1rem;
  color: #2EE8C0;
  letter-spacing: 3px;
  text-transform: uppercase;
  text-shadow: 0 0 16px rgba(26,188,156,0.6);
}
.parlay-body { padding: 14px 16px; }
.parlay-leg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(26,188,156,0.1);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: var(--text);
}
.parlay-leg:last-child { border-bottom: none; }
.parlay-connector {
  text-align: center;
  color: var(--gold);
  font-size: 0.7rem;
  letter-spacing: 3px;
  padding: 2px 0;
  font-family: 'DM Sans', sans-serif;
}

/* ── GAME LIST CARD ── */
.game-row {
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  border-radius: 4px;
  padding: 12px 16px;
  margin: 6px 0;
  transition: border-color 0.2s;
}
.game-row:hover { border-left-color: var(--gold2); }
.game-row-ev {
  border-left-color: #4ade80;
}
.game-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--white);
}
.game-meta {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 2px;
}

/* ── PROB BARS ── */
.bar-wrap { margin: 4px 0; }
.bar-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
.bar-team { font-family: 'DM Sans',sans-serif; font-size:0.72rem; color:var(--muted); }
.bar-pct  { font-family: 'Cinzel',sans-serif; font-size:0.72rem; font-weight:700; }
.bar-bg   { background: rgba(255,255,255,0.05); border-radius:3px; height:6px; }
.bar-fill { height:6px; border-radius:3px; }

/* ── SECTION HEADING ── */
.section-heading {
  font-family: 'Cinzel', serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--gold);
  letter-spacing: 4px;
  text-transform: uppercase;
  margin: 20px 0 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-heading::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--border), transparent);
}

/* ── WARNING BANNER ── */
.warn-banner {
  background: rgba(201,168,76,0.06);
  border: 1px solid rgba(201,168,76,0.25);
  border-radius: 4px;
  padding: 8px 14px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #C9A84C;
  margin: 8px 0;
}
.demo-banner {
  background: rgba(192,57,43,0.08);
  border: 1px solid rgba(192,57,43,0.3);
  border-radius: 4px;
  padding: 8px 14px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #e74c3c;
  margin: 8px 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--felt3) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectSlider span {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text) !important;
}
.sidebar-logo {
  font-family: 'Cinzel', serif;
  font-size: 1.4rem;
  font-weight: 900;
  color: var(--gold);
  letter-spacing: 4px;
  text-align: center;
  padding: 12px 0 4px;
  text-shadow: 0 0 20px rgba(201,168,76,0.4);
}
.sidebar-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.6rem;
  color: var(--muted);
  letter-spacing: 3px;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 8px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--felt3) !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: 'Cinzel', serif !important;
  font-size: 0.72rem !important;
  letter-spacing: 2px !important;
  color: var(--muted) !important;
  background: transparent !important;
  border: none !important;
  padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 2px solid var(--gold) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: var(--dark) !important;
  padding-top: 16px !important;
}

/* ── BUTTON ── */
.stButton > button {
  background: linear-gradient(135deg, #8B6914 0%, var(--gold) 50%, #8B6914 100%) !important;
  color: var(--dark) !important;
  font-family: 'Cinzel', serif !important;
  font-size: 0.9rem !important;
  font-weight: 700 !important;
  letter-spacing: 3px !important;
  text-transform: uppercase !important;
  border: none !important;
  padding: 14px 32px !important;
  border-radius: 3px !important;
  width: 100% !important;
  cursor: pointer !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 30px rgba(201,168,76,0.5) !important;
}

/* ── NO RESULTS ── */
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: var(--muted);
  font-family: 'DM Sans', sans-serif;
}
.empty-icon { font-size: 3rem; margin-bottom: 12px; }
.empty-title { font-family: 'Cinzel', serif; font-size: 1rem; color: var(--gold); letter-spacing: 2px; margin-bottom: 8px; }

hr { border-color: var(--border) !important; }

/* ══════════════════════════════════════════════════
   MOBILE RESPONSIVE  (≤ 768 px)
   ══════════════════════════════════════════════════ */
@media (max-width: 768px) {

  /* ── Global padding ── */
  .block-container {
    padding-left: 8px !important;
    padding-right: 8px !important;
    padding-top: 8px !important;
    max-width: 100% !important;
  }

  /* ── Hide sidebar toggle, keep content full-width ── */
  [data-testid="stSidebar"] {
    min-width: 80vw !important;
    max-width: 88vw !important;
  }

  /* ── TABS: compact, scrollable, no wrap ── */
  .stTabs [data-baseweb="tab-list"] {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
  .stTabs [data-baseweb="tab"] {
    font-size: 0.55rem !important;
    letter-spacing: 0.5px !important;
    padding: 8px 10px !important;
    white-space: nowrap !important;
  }

  /* ── Pick card: smaller text, no overflow ── */
  .pick-card { padding: 0 0 12px 0 !important; margin: 8px 0 !important; }
  .pick-header { padding: 10px 12px !important; flex-direction: column !important; gap: 6px !important; }
  .pick-matchup { font-size: 0.9rem !important; }
  .pick-body { padding: 10px 12px !important; }
  .pick-action {
    font-size: 1.15rem !important;
    letter-spacing: 1px !important;
    gap: 8px !important;
    padding: 8px 0 !important;
  }
  .pick-action-arrow { font-size: 1.3rem !important; }

  /* ── Stats row: 2 cols on mobile ── */
  .stats-row { gap: 10px !important; }
  .stat-item { min-width: 56px !important; }
  .stat-item-val { font-size: 1rem !important; }

  /* ── Game row ── */
  .game-row { padding: 8px 10px !important; }
  .game-title { font-size: 0.78rem !important; }
  .game-meta  { font-size: 0.62rem !important; }

  /* ── Section heading ── */
  .section-heading { font-size: 0.75rem !important; letter-spacing: 2px !important; }

  /* ── Parlay card ── */
  .parlay-header { font-size: 0.75rem !important; padding: 10px 12px !important; letter-spacing: 1.5px !important; }
  .parlay-body   { padding: 10px 12px !important; }
  .parlay-leg    { font-size: 0.72rem !important; }

  /* ── Prob bars ── */
  .bar-team, .bar-pct { font-size: 0.62rem !important; }

  /* ── Buttons ── */
  .stButton > button {
    font-size: 0.7rem !important;
    padding: 10px 16px !important;
    letter-spacing: 2px !important;
  }

  /* ── Sidebar button ── */
  [data-testid="stSidebar"] .stButton > button {
    font-size: 0.65rem !important;
    padding: 8px 12px !important;
  }

  /* ── Columns used for sport tiles: force equal width, no overflow ── */
  [data-testid="column"] {
    min-width: 0 !important;
    overflow: hidden !important;
  }

  /* ── Expanders ── */
  .streamlit-expanderHeader {
    font-size: 0.75rem !important;
    padding: 8px 10px !important;
  }

  /* ── Empty state ── */
  .empty-state { padding: 28px 12px !important; }
  .empty-icon  { font-size: 2rem !important; }
  .empty-title { font-size: 0.85rem !important; }

  /* ── Warn / demo banners ── */
  .warn-banner, .demo-banner { font-size: 0.7rem !important; padding: 6px 10px !important; }

  /* ── Sidebar logo ── */
  .sidebar-logo { font-size: 1.1rem !important; letter-spacing: 2px !important; }
  .sidebar-sub  { font-size: 0.5rem !important; letter-spacing: 2px !important; }

  /* ── Reduce pick card market chip ── */
  .market-chip { font-size: 0.58rem !important; padding: 2px 7px !important; }

  /* ── Confidence badge ── */
  .conf-badge { font-size: 0.6rem !important; padding: 3px 8px !important; }

  /* ── Pick rationale ── */
  .pick-rationale { font-size: 0.72rem !important; }

  /* ── Live section header sport tiles: shrink on mobile ── */
  div[style*="text-align:center"][style*="border-radius:10px"],
  div[style*="text-align:center"][style*="border-radius:9px"] {
    padding: 6px 2px !important;
  }
}

/* Extra small (≤ 480 px — most phones portrait) */
@media (max-width: 480px) {
  .pick-action { font-size: 0.95rem !important; }
  .stat-item-val { font-size: 0.88rem !important; }
  .pick-matchup { font-size: 0.82rem !important; }
  .stTabs [data-baseweb="tab"] {
    font-size: 0.48rem !important;
    padding: 7px 7px !important;
  }
}
</style>
""", unsafe_allow_html=True)

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
    "Champions League":       {"sport":"soccer", "league":"UEFA.CHAMPIONS",    "group":"Soccer"},
    "Europa League":          {"sport":"soccer", "league":"UEFA.EUROPA",         "group":"Soccer"},
    "Conference League":      {"sport":"soccer", "league":"UEFA.CONFERENCE",     "group":"Soccer"},
    "CONCACAF Champions Cup": {"sport":"soccer", "league":"CONCACAF.CHAMPIONS",  "group":"Soccer"},
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
    "CONCACAF Champions Cup": "🌎",
}

def league_label(name):
    """Return flag + league name."""
    return f"{LEAGUE_FLAG.get(name, '🌐')} {name}"

HOME_BOOST = {
    "NBA":0.035,"MLB":0.025,
    "NFL":0.035,"NCAAF":0.045,"NHL":0.03,"MLS":0.04,"Liga MX":0.045,
    "Premier League":0.038,"La Liga":0.04,"Bundesliga":0.042,"Serie A":0.04,
    "Ligue 1":0.04,"Champions League":0.035,"Europa League":0.035,"Conference League":0.032,"CONCACAF Champions Cup":0.04,
    }
LEAGUE_AVG_GOALS = {
    "NBA":228.0,"MLB":9.0,
    "NFL":46.0,"NCAAF":56.0,"NHL":6.2,
    "MLS":2.96,"Liga MX":2.72,"Premier League":2.81,"La Liga":2.63,
    "Bundesliga":3.24,"Serie A":2.72,"Ligue 1":2.61,
    "Champions League":3.14,"Europa League":2.89,"Conference League":2.71,"CONCACAF Champions Cup":2.85,
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
    "thresholds_json",
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
         "odds":{"spread":"BOS -8.5","over_under":"218.0","home_ml":"-320","away_ml":"+260","home_wp":"76","away_wp":"24"}},
        {"id":"d4","league":"NBA","home_team":"Denver Nuggets","away_team":"Oklahoma City Thunder",
         "home_score":"62","away_score":"58","home_record":"44-16","away_record":"46-14",
         "state":"in","status_detail":"3rd Qtr 4:22","date":"","venue":"Ball Arena",
         "odds":{"spread":"OKC -1.5","over_under":"228.0","home_ml":"+105","away_ml":"-125","home_wp":"44","away_wp":"56"}},
        {"id":"d5","league":"Liga MX","home_team":"Club América","away_team":"Chivas Guadalajara",
         "home_score":"","away_score":"","home_record":"14-4-4","away_record":"10-6-6",
         "state":"pre","status_detail":"Sáb 8:00 PM","date":"","venue":"Estadio Azteca",
         "odds":{"spread":"","over_under":"2.5","home_ml":"-130","away_ml":"+320","home_wp":"55","away_wp":"20"}},
        {"id":"d6","league":"MLB","home_team":"New York Yankees","away_team":"Boston Red Sox",
         "home_score":"","away_score":"","home_record":"18-12","away_record":"15-15",
         "state":"pre","status_detail":"7:05 PM ET","date":"","venue":"Yankee Stadium",
         "odds":{"spread":"","over_under":"8.5","home_ml":"-145","away_ml":"+122","home_wp":"59","away_wp":"41"}},
        {"id":"d7","league":"Bundesliga","home_team":"Bayern Munich","away_team":"Borussia Dortmund",
         "home_score":"","away_score":"","home_record":"20-4-4","away_record":"16-6-6",
         "state":"pre","status_detail":"Sáb 9:30 AM","date":"","venue":"Allianz Arena",
         "odds":{"spread":"","over_under":"3.5","home_ml":"-155","away_ml":"+400","home_wp":"58","away_wp":"18"}},
        {"id":"d8","league":"NHL","home_team":"Florida Panthers","away_team":"Tampa Bay Lightning",
         "home_score":"","away_score":"","home_record":"41-18-6","away_record":"38-22-5",
         "state":"pre","status_detail":"7:00 PM ET","date":"","venue":"Amerant Bank Arena",
         "odds":{"spread":"","over_under":"6.0","home_ml":"-135","away_ml":"+115","home_wp":"55","away_wp":"45"}},
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
}

def get_team_profile(team_id):
    """Retorna perfil de equipo del cache, o None si no existe."""
    if not team_id:
        return None
    return _load_all_team_profiles().get(str(team_id))


@st.cache_data(ttl=1800)  # Cache 30min — form doesn't change mid-day
def fetch_recent_form(sport, league, team_id, n_games=5):
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
    Version sin @st.cache_data. Usa /schedule para historial completo.
    Parsea score de múltiples ubicaciones posibles en la respuesta de ESPN.
    """
    if not team_id or not sport or not league:
        return None
    try:
        url = (f"https://site.api.espn.com/apis/site/v2/sports/"
               f"{sport}/{league}/teams/{team_id}/schedule")
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None
        data   = r.json()
        events = data.get("events", [])
        if not events:
            return None

        games_raw_list = []
        now_iso = datetime.now(timezone.utc).isoformat()[:16]  # "2026-03-12T03:15"

        def _get_score(competitor):
            """Try multiple keys where ESPN might store the score."""
            for key in ("score", "homeScore", "awayScore", "points"):
                v = competitor.get(key)
                if v is not None and v != "":
                    try: return float(v)
                    except: pass
            # Try nested score object
            score_obj = competitor.get("score", {})
            if isinstance(score_obj, dict):
                for key in ("value", "displayValue"):
                    v = score_obj.get(key)
                    if v is not None:
                        try: return float(v)
                        except: pass
            return None

        for ev in events:
            ev_date = ev.get("date", "")
            # Skip clearly future games
            if ev_date[:16] > now_iso:
                continue

            competitions = ev.get("competitions", [])
            if not competitions:
                continue
            comp  = competitions[0]
            comps = comp.get("competitors", [])
            if len(comps) < 2:
                continue

            # Match team by id
            team_comp = next((c for c in comps if str(c.get("id","")) == str(team_id)), None)
            opp_comp  = next((c for c in comps if str(c.get("id","")) != str(team_id)), None)
            if not team_comp or not opp_comp:
                continue

            team_score = _get_score(team_comp)
            opp_score  = _get_score(opp_comp)

            # Skip if no scores found
            if team_score is None or opp_score is None:
                continue

            # Skip 0-0 with no boxscore (unplayed)
            if team_score == 0 and opp_score == 0:
                if not comp.get("boxscoreAvailable", False):
                    continue

            is_home   = team_comp.get("homeAway") == "home"
            opp_name  = opp_comp.get("team", {}).get("displayName", "")
            game_date = ev_date[:10]

            games_raw_list.append({
                "scored":   team_score,
                "conceded": opp_score,
                "home":     is_home,
                "date":     game_date,
                "opp":      opp_name,
            })

            if len(games_raw_list) >= n_games:
                break

        return games_raw_list if games_raw_list else None
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
    }

    if league not in LEAGUE_SLUGS:
        return

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
    # Reutiliza hf/af ya obtenidos arriba — sin doble fetch a ESPN
    import threading

    if home_id and isinstance(hf, dict) and hf.get("games_raw"):
        _h_games_raw = hf["games_raw"]
        _h_name      = game["home_team"]
        def _update_home(_tid=home_id, _name=_h_name, _lg=league, _sg=group, _gr=_h_games_raw):
            update_team_profile(team_id=_tid, team_name=_name,
                                league=_lg, sport_group=_sg, new_games=_gr)
        threading.Thread(target=_update_home, daemon=True).start()
    game["home_profile"] = get_team_profile(home_id) if home_id else None

    if away_id and isinstance(af, dict) and af.get("games_raw"):
        _a_games_raw = af["games_raw"]
        _a_name      = game["away_team"]
        def _update_away(_tid=away_id, _name=_a_name, _lg=league, _sg=group, _gr=_a_games_raw):
            update_team_profile(team_id=_tid, team_name=_name,
                                league=_lg, sport_group=_sg, new_games=_gr)
        threading.Thread(target=_update_away, daemon=True).start()
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


@st.cache_data(ttl=300)
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
        today_mx  = _now_mx.strftime("%Y%m%d")
        tom_utc   = (_now + timedelta(days=1)).strftime("%Y%m%d")
        tom_mx    = (_now_mx + timedelta(days=1)).strftime("%Y%m%d")
        d2_utc    = (_now + timedelta(days=2)).strftime("%Y%m%d")
        base_url  = ESPN_URL.format(sport=sport, league=league)
        urls = [
            base_url,                                        # default (today)
            f"{base_url}?dates={today_mx}&limit=100",       # MX today
            f"{base_url}?dates={today_utc}&limit=100",      # UTC today
            f"{base_url}?dates={tom_utc}&limit=100",        # UTC tomorrow
            f"{base_url}?dates={tom_mx}&limit=100",         # MX tomorrow
            f"{base_url}?dates={d2_utc}&limit=100",         # day after tomorrow
            f"{base_url}?limit=200",                        # no date, high limit
        ]

    all_events = []
    returned_data = {}
    for url in urls:
        if not url: continue
        try:
            r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                data = r.json()
                evts = data.get("events", [])
                if isinstance(evts, list) and evts:
                    # Deduplicate by event id
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


def parse_games(data, league_name):
    """Parse ESPN scoreboard JSON into normalized game dicts."""
    games = []
    from datetime import timedelta as _td
    _now_utc   = datetime.now(timezone.utc)
    _now_mx    = _now_utc - _td(hours=6)  # Mexico City offset
    _valid_dates = set()
    for _d in range(-1, 3):  # yesterday, today, tomorrow, day after
        _valid_dates.add((_now_utc + _td(days=_d)).strftime("%Y-%m-%d"))
        _valid_dates.add((_now_mx  + _td(days=_d)).strftime("%Y-%m-%d"))

    for event in data.get("events", []):
        try:
            # Filter: only show games within window of today (±1 day)
            ev_date = event.get("date","")[:10]
            if ev_date and ev_date not in _valid_dates:
                continue
            comp  = event.get("competitions", [{}])[0]
            comps = comp.get("competitors", [])
            if len(comps) < 2:
                continue
            home = next((c for c in comps if c.get("homeAway") == "home"), comps[0])
            away = next((c for c in comps if c.get("homeAway") == "away"), comps[1])
            status = event.get("status", {})

            odds_info = {}
            ol = comp.get("odds", [])
            if ol:
                o = ol[0]
                odds_info = {
                    "spread":   o.get("details", ""),
                    "over_under": o.get("overUnder", ""),
                    "home_ml":  o.get("homeTeamOdds", {}).get("moneyLine", ""),
                    "away_ml":  o.get("awayTeamOdds", {}).get("moneyLine", ""),
                    "home_wp":  o.get("homeTeamOdds", {}).get("winPercentage", ""),
                    "away_wp":  o.get("awayTeamOdds", {}).get("winPercentage", ""),
                }

            hr = home.get("records", [{}])
            ar = away.get("records", [{}])
            live_stats = _parse_live_stats(comp, home, away)

            # Store team IDs for form lookup
            home_team_id = str(home.get("team", {}).get("id", "") or home.get("id", ""))
            away_team_id = str(away.get("team", {}).get("id", "") or away.get("id", ""))

            games.append({
                "id":           event.get("id", ""),
                "league":       league_name,
                "home_team":    home.get("team", {}).get("displayName", "Home"),
                "away_team":    away.get("team", {}).get("displayName", "Away"),
                "home_score":   home.get("score", ""),
                "away_score":   away.get("score", ""),
                "home_record":  hr[0].get("summary", "") if hr else "",
                "away_record":  ar[0].get("summary", "") if ar else "",
                "state":        status.get("type", {}).get("state", "pre"),
                "status_detail": (status.get("type", {}).get("shortDetail", "") or "").split("\n")[0].strip(),
                "date":         event.get("date", ""),
                "venue":        comp.get("venue", {}).get("fullName", ""),
                "odds":         odds_info,
                "live_stats":   live_stats,
                "home_team_id": home_team_id,
                "away_team_id": away_team_id,
            })
        except:
            continue
    return games


def get_all_games(leagues):
    result=[]; errors=[]
    for name in leagues:
        cfg=LEAGUES.get(name)
        if not cfg:
            errors.append(f"{name}: liga no configurada")
            continue
        try:
            data = fetch_scoreboard(cfg["sport"], cfg["league"], tournament_id=cfg.get("tournament_id"))
            parsed = parse_games(data, name)
            result.extend(parsed)
            if not parsed:
                errors.append(f"{name}: sin partidos en ESPN hoy")
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

    "Soccer": """You are a sharp soccer betting analyst covering global leagues (Liga MX, Premier League, UCL, La Liga, etc.).
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
# MATH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
def ml_to_prob(ml):
    try:
        ml=float(str(ml).replace("+",""))
        return 100/(ml+100) if ml>0 else abs(ml)/(abs(ml)+100)
    except: return 0.5

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
      4. Recent form (last 5 games)       weight 2.5  — recency-weighted win rate
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
            form_w = 2.5 if has_ml_signal else 3.5
            weights.append(form_w)
    elif home_form is not None:
        signals.append((home_form + 0.5) / (home_form + 1.0))
        weights.append(1.5)
    elif away_form is not None:
        signals.append(1.0 - (away_form + 0.5) / (away_form + 1.0))
        weights.append(1.5)

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
    "CONCACAF Champions Cup",
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

    if signal_b_ok and h_scored is not None and a_conceded is not None and h_scored > 0:
        avg_per_team = max(0.5, avg / 2.0)
        h_attack  = h_scored   / avg_per_team
        a_defence = max(def_floor, a_conceded / avg_per_team)
        lam_home_real = max(0.1, avg_per_team * h_attack * a_defence * (1.0 + home_boost_b))

    if signal_b_ok and a_scored is not None and h_conceded is not None and a_scored > 0:
        avg_per_team = max(0.5, avg / 2.0)
        a_attack  = a_scored   / avg_per_team
        h_defence = max(def_floor, h_conceded / avg_per_team)
        lam_away_real = max(0.1, avg_per_team * a_attack * h_defence)

    # ── Build final lambdas ───────────────────────────────────────────
    if has_ou_line:
        # ESPN line → use it for total, split by home_share
        home_share = (hp + 0.52) / (hp + ap + 1.04)
        lam_home   = max(0.1, total * home_share)
        lam_away   = max(0.1, total * (1.0 - home_share))
        # If scoring trend available, blend it in (20% weight — line dominates)
        if lam_home_real is not None:
            lam_home = 0.80 * lam_home + 0.20 * lam_home_real
        if lam_away_real is not None:
            lam_away = 0.80 * lam_away + 0.20 * lam_away_real
        # Store for Signal D + display even when ESPN line present
        if lam_home_real is not None and lam_away_real is not None:
            game["_lam_real_h"] = round(lam_home_real, 3)
            game["_lam_real_a"] = round(lam_away_real, 3)
            game["_lam_league"] = round(avg, 2)

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
    # All computed via joint Poisson(avg/2, avg/2) from LEAGUE_AVG_GOALS
    "MLS":                   (0.205, 0.432, 0.656, 0.795, 0.568, 0.344, 0.597),
    "Liga MX":               (0.245, 0.489, 0.710, 0.755, 0.511, 0.290, 0.553),
    "Premier League":        (0.229, 0.467, 0.690, 0.771, 0.533, 0.310, 0.569),
    "La Liga":               (0.262, 0.511, 0.729, 0.738, 0.489, 0.271, 0.535),
    "Bundesliga":            (0.166, 0.372, 0.594, 0.834, 0.628, 0.406, 0.643),
    "Serie A":               (0.245, 0.489, 0.710, 0.755, 0.511, 0.290, 0.553),
    "Ligue 1":               (0.256, 0.502, 0.723, 0.744, 0.498, 0.277, 0.531),
    "Champions League":      (0.179, 0.393, 0.616, 0.821, 0.607, 0.384, 0.627),
    "Europa League":         (0.220, 0.452, 0.676, 0.780, 0.548, 0.324, 0.584),
    "Conference League":     (0.252, 0.497, 0.718, 0.748, 0.503, 0.282, 0.551),
    "CONCACAF Champions Cup":(0.223, 0.458, 0.681, 0.777, 0.542, 0.319, 0.577),
}
# Minimum deviation from league prior to qualify as a valid O/U or BTTS pick.
# 8% = meaningful signal — below this the model learns nothing new vs league avg.
OU_MIN_EDGE = 0.08
# ═══════════════════════════════════════════════════════════════════════════════
# SOCCER O/U CALIBRATION — post-simulation correction per league
# Source: FBref 2024-25 real frequencies vs Poisson model output
# Format: (Δ_u25, Δ_u35, Δ_btts) as fractions (e.g. +0.06 = +6%)
# Applied AFTER simulation to correct systematic Poisson bias per league.
# Positive Δ = model underestimates → add. Negative → subtract.
# O2.5/O3.5 are always = 1 - U2.5/U3.5 after calibration (enforced).
# ═══════════════════════════════════════════════════════════════════════════════
SOCCER_CALIB = {
    "Premier League":         ( -0.015,  +0.020, -0.015),
    "La Liga":                ( -0.030,   0.000, -0.010),
    "Bundesliga":             ( +0.030,  +0.045, -0.050),
    "Serie A":                ( -0.020,  +0.010, -0.020),
    "Ligue 1":                ( -0.015,  +0.005, -0.025),
    "Liga MX":                ( +0.010,  +0.040, -0.070),
    "Champions League":       ( -0.015,  +0.005, -0.015),
    "Europa League":          ( -0.020,  +0.010, -0.035),
    "Conference League":      ( -0.010,  +0.015, -0.030),
    "CONCACAF Champions Cup": ( +0.060,  +0.080, -0.100),
    "MLS":                    ( +0.030,  +0.055, -0.065),
}

def apply_soccer_calib(league, p_u25, p_u35, p_btts, p_o25, p_o35):
    """
    Apply per-league calibration to O/U and BTTS probabilities.
    Enforces constraints: O + U = 1.0, all probs in [0.01, 0.99].
    Only applied for soccer leagues with known calibration data.
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

    # Enforce O = 1 - U (keeps sum = 1.0)
    p_o25_c = clamp(1.0 - p_u25_c)  if p_u25_c is not None else p_o25
    p_o35_c = clamp(1.0 - p_u35_c)  if p_u35_c is not None else p_o35

    return p_u25_c, p_u35_c, p_btts_c, p_o25_c, p_o35_c


# ═══════════════════════════════════════════════════════════════════════════════
# NHL / NBA / MLB NO-LINE CALIBRATION
# Root cause: when ESPN has no O/U line (ou_val=0), the model compares
# sim_total vs λ_expected (the mean) → produces ~50/50 by construction.
# Real O/U hit rates differ from 50% (source: 2024-25 season data):
#   NHL Under: 52.1% (Hockey-Reference, ~1312 games) → +3.1%
#   NBA Under: 48.8% (TeamRankings,    ~1230 games)  → -1.2%
#   MLB Under: 51.8% (2024-25 season,  ~2430 games)  → +1.8%
# When ESPN provides a real line, the market IS the calibration — don't touch it.
# ═══════════════════════════════════════════════════════════════════════════════
NHL_NO_LINE_UNDER = +0.031
NBA_NO_LINE_UNDER = -0.012
MLB_NO_LINE_UNDER = +0.018

def apply_nonsoccer_calib(sport_grp, is_hockey, p_u_total, p_o_total, ou_val):
    """Apply calibration only when ou_val=0 (no ESPN line). O+U enforced=1.0."""
    if p_u_total is None or p_o_total is None or ou_val != 0.0:
        return p_u_total, p_o_total
    def clamp(x): return max(0.01, min(0.99, x))
    if is_hockey:
        p_u_total = clamp(p_u_total + NHL_NO_LINE_UNDER)
    elif sport_grp == "Basketball":
        p_u_total = clamp(p_u_total + NBA_NO_LINE_UNDER)
    elif sport_grp == "Baseball":
        p_u_total = clamp(p_u_total + MLB_NO_LINE_UNDER)
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
        c_color = "#4ade80"
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

    hw=aw=d=btts=o15=o25=o35=u25=u35=dc_1x=dc_x2=dc_12=o_total=u_total=0
    rng=random.Random()

    for _ in range(n):
        ph=max(0.01,min(0.99,hp+rng.gauss(0,sigma)))
        if use_goals:
            lh=max(0.1,lam_h*(1+rng.gauss(0,0.15*(1-dq))))
            la=max(0.1,lam_a*(1+rng.gauss(0,0.15*(1-dq))))
            gh=poisson_sample(lh,rng); ga=poisson_sample(la,rng); tg=gh+ga
            if is_soccer:
                if gh>ga: hw+=1; dc_1x+=1; dc_12+=1
                elif gh==ga: d+=1; dc_1x+=1; dc_x2+=1
                else: aw+=1; dc_x2+=1; dc_12+=1
                if gh>0 and ga>0: btts+=1
                if tg>1.5: o15+=1
                if tg>2.5: o25+=1
                else: u25+=1        # tg <= 2.5  (Under 2.5)
                if tg>3.5: o35+=1
                else: u35+=1        # tg <= 3.5  (Under 3.5)
            else:
                if is_hockey:
                    # NHL — Poisson is correct (λ ~3 goals/team, small enough)
                    # No draw in regulation resolution for O/U purposes (OT/SO ignored)
                    if gh > ga: hw += 1; dc_1x += 1; dc_12 += 1
                    elif gh < ga: aw += 1; dc_x2 += 1; dc_12 += 1
                    else:  # tie after 60 min — 50/50 OT
                        if rng.random() < 0.5: hw += 1; dc_1x += 1; dc_12 += 1
                        else: aw += 1; dc_x2 += 1; dc_12 += 1
                    if ou_val > 0:
                        if tg > ou_val: o_total += 1
                        else: u_total += 1
                else:
                    # NBA / MLB / NFL — normal distribution (Poisson breaks for large λ)
                    std = max(1.0, (lh + la) * 0.08)
                    sim_h = max(0, lh + rng.gauss(0, std * 0.55))
                    sim_a = max(0, la + rng.gauss(0, std * 0.55))
                    sim_total = sim_h + sim_a
                    if sim_h > sim_a: hw += 1; dc_1x += 1; dc_12 += 1
                    else: aw += 1; dc_x2 += 1; dc_12 += 1
                    if ou_val > 0:
                        if sim_total > ou_val: o_total += 1
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
    # NBA/NHL/MLB: O/U over the actual line (lam_h + lam_a = expected total)
    p_o_total = o_total/n if (use_goals and not is_soccer and (o_total+u_total)>0) else None
    p_u_total = u_total/n if (use_goals and not is_soccer and (o_total+u_total)>0) else None
    p_btts=btts/n if use_goals else None
    p_o15=o15/n if use_goals else None
    p_o25=o25/n if use_goals else None
    p_o35=o35/n if use_goals else None
    p_u25=u25/n if use_goals else None
    p_u35=u35/n if use_goals else None

    # ── Per-league calibration (soccer only) ──────────────────────────────────
    if is_soccer and use_goals:
        p_u25, p_u35, p_btts, p_o25, p_o35 = apply_soccer_calib(
            game["league"], p_u25, p_u35, p_btts, p_o25, p_o35)

    # ── NHL / NBA / MLB calibration ────────────────────────────────────────────
    if not is_soccer and use_goals and p_u_total is not None:
        p_u_total, p_o_total = apply_nonsoccer_calib(
            sport_grp, is_hockey, p_u_total, p_o_total, ou_val)

    p_dc_1x=dc_1x/n; p_dc_x2=dc_x2/n; p_dc_12=dc_12/n

    hml=game["odds"].get("home_ml",""); aml=game["odds"].get("away_ml","")
    ou=game["odds"].get("over_under","")
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

    # ── NBA / NHL / MLB O/U (total points/goals line from ESPN) ──────────────
    if p_o_total is not None and ou:
        try:
            ou_line = float(str(ou))
            ou_label = f"Over {ou_line:.1f}"
            uu_label = f"Under {ou_line:.1f}"
            o_total_ev = calc_ev(p_o_total, OU_ML)
            u_total_ev = calc_ev(p_u_total, OU_ML)
            candidates += [
                ("O/U", ou_label,  p_o_total, o_total_ev, str(OU_ML), quarter_kelly(p_o_total, OU_ML)),
                ("O/U", uu_label,  p_u_total, u_total_ev, str(OU_ML), quarter_kelly(p_u_total, OU_ML)),
            ]
        except:
            pass

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
    _has_ml        = bool(hml and aml)
    _has_scoring   = game.get("home_avg_scored") is not None
    _has_form      = game.get("home_form") is not None or game.get("away_form") is not None
    _has_real_signal = _has_ml or _has_scoring or _has_form

    # ── Clasifica fuente de señal disponible ────────────────────────────────────
    _has_profile   = (game.get("home_profile") and game.get("home_profile",{}).get("n_games",0) >= 5) or                      (game.get("away_profile") and game.get("away_profile",{}).get("n_games",0) >= 5)
    _has_record    = (game.get("home_record","") and game.get("away_record",""))  # season W-L-D

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
            if p_o25 is not None:
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

    # Detect "partido parejo" — requires real ML signal to be meaningful
    # Without ML, hp≈aw≈0.37 always → _parejo always True → always picks U3.5
    _spread = abs(sh - sa) * 100  # percentage spread between teams
    _parejo = use_goals and is_soccer and _spread < 12 and _has_ml

    MARKET_PREF = {"BTTS": 4, "O/U": 3, "ML": 2, "DO": 1}
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
            best_single = {"market":mt,"label":lb,"prob":pr,"ev":ev or 0,"ml":ml,"kelly":k or 0}
        # Done — parejo always uses goal market by prob, no ML/DO override
    else:
        # Normal case: pick by highest EV, with BTTS preferred on ties
        for mtype,label,prob,ev,ml,kelly in candidates_main:
            if prob is None or ev is None:
                continue
            pref = MARKET_PREF.get(mtype, 0)
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

    sim = {
        "home_pct":round(sh*100,1),"away_pct":round(sa*100,1),"draw_pct":round(sd*100,1),
        "data_quality":round(dq*100,0),
        "home_ev":home_ev,"away_ev":away_ev,
        "home_ml":hml,"away_ml":aml,"over_under":ou,
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
        "best_single":best_single,"best_parlay":best_parlay,"pos_legs":pos_legs,
        "p_o_total":round(p_o_total*100,1) if p_o_total is not None else None,
        "p_u_total":round(p_u_total*100,1) if p_u_total is not None else None,
        "ou_line":str(ou) if ou else None,
        "is_soccer":is_soccer,"n_simulations":n,"use_goals":use_goals,
        "low_confidence": game.get("_low_confidence", False),
        "lam_real_h":game.get("_lam_real_h"),"lam_real_a":game.get("_lam_real_a"),
        "lam_league":game.get("_lam_league"),
        "home_back2back":game.get("home_back2back",False),"away_back2back":game.get("away_back2back",False),
        "home_rest_days":game.get("home_rest_days"),"away_rest_days":game.get("away_rest_days"),
        "home_injury_factor":game.get("home_injury_factor",1.0),
        "away_injury_factor":game.get("away_injury_factor",1.0),
        "home_injuries":game.get("home_injuries",[]),
        "away_injuries":game.get("away_injuries",[]),
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
        if leg and leg["ev"] > 0:
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
            target = l1["_r"] if l1["ev"] >= l2["ev"] else l2["_r"]
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
            f'<div style="font-family:\'DM Sans\',sans-serif;font-size:0.8rem;color:#6B7E6E;">'
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
    def _sport_best_ph(r):
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
            return {"mercado":"ML","pick_label":t,"prob_pct":round(p,1)} if ml else None

        if sg == "Soccer":
            cands = []
            _btts_ev = sim.get("btts_ev") or 0
            _btts_pb = sim.get("p_btts") or 0
            if _btts_ev > 0 and _btts_pb > 0:
                cands.append({"mercado":"BTTS","pick_label":"Ambos Anotan","prob_pct":round(_btts_pb,1)})
            _o25_ev = sim.get("o25_ev") or 0
            _o25_pb = sim.get("p_o25") or 0
            if _o25_ev > 0 and _o25_pb > 0:
                cands.append({"mercado":"O/U","pick_label":"Over 2.5","prob_pct":round(_o25_pb,1)})
            _ml = best_ml()
            if _ml: cands.append(_ml)
            return max(cands, key=lambda x: x["prob_pct"]) if cands else None
        elif sg in ("Basketball","Hockey"):
            cands = []
            _ml = best_ml()
            if _ml: cands.append(_ml)
            _ou_line = sim.get("ou_line") or ""
            _p_over  = sim.get("p_o_total") or 0
            if _ou_line and _p_over > 45:
                try: _line = float(_ou_line)
                except: _line = None
                if _line:
                    cands.append({"mercado":"O/U","pick_label":f"Over {_line:.1f}","prob_pct":round(_p_over,1)})
            return max(cands, key=lambda x: x["prob_pct"]) if cands else None
        else:
            return best_ml()

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
def chip(market):
    label_map = {"DO": "DO"}
    display_market = label_map.get(market, market)
    cls={"ML":"chip-ml","BTTS":"chip-btts","O/U":"chip-ou","DO":"chip-dc","PARLAY":"chip-parlay"}.get(market,"chip-ml")
    return f'<span class="market-chip {cls}">{display_market}</span>'

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
    is_live    = r.get("state", "") == "in"
    live_html  = '<span class="market-chip chip-btts">🔴 EN VIVO</span>' if is_live else ""
    rank_html  = ""
    if rank:
        rank_html = '<span style="font-family:Cinzel,serif;color:#6B7E6E;font-size:0.8rem">#' + str(rank) + '</span> '

    score_html = ""
    if is_live and r.get("home_score") and r.get("away_score"):
        score_html = (' <span style="color:#4ade80;font-weight:700">'
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
                c = "#4ade80" if ev_v > 0 else ("#C9A84C" if lbl == "O2.5" else "#6B7E6E")
                star = "⭐ " if is_best else ""
                fw = "font-weight:700;" if is_best else ""
                pills.append('<span style="color:' + c + ';font-size:0.88rem;' + fw + '">' + star + lbl + ' <b>' + str(pct) + '%</b> (EV ' + ev_s + ')</span>')
            else:
                c = "#8ab4a0" if is_best else "#6B7E6E"
                star = "⭐ " if is_best else ""
                fw = "font-weight:700;" if is_best else ""
                pills.append('<span style="color:' + c + ';font-size:0.88rem;' + fw + '">' + star + lbl + ' <b>' + str(pct) + '%</b></span>')
        if pills:
            goals_html = ('<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:6px;'
                          'padding-top:6px;border-top:1px solid rgba(255,255,255,0.05)">'
                          + " &nbsp;|&nbsp; ".join(pills) + "</div>")

    dq_html   = dq_warn(dq)
    chip_html = chip(bs["market"])
    status    = r.get("status_detail", "").replace("<","").replace(">","").replace("/","").strip()

    # Recent form badges
    form_html = ""
    hf = r.get("home_form"); af = r.get("away_form")
    def form_badge(f, team):
        if f is None: return ""
        pct = int(f * 100)
        c = "#4ade80" if pct >= 60 else ("#C9A84C" if pct >= 40 else "#ef4444")
        arrow = "▲" if pct >= 60 else ("▬" if pct >= 40 else "▼")
        return f'<span style="font-size:0.72rem;color:{c};margin-right:8px">{arrow} {team} {pct}% forma</span>'
    if hf is not None or af is not None:
        form_html = ('<div style="margin-top:5px;opacity:0.85">' +
                     form_badge(hf, r.get("home_team","Local")) +
                     form_badge(af, r.get("away_team","Visita")) +
                     '<span style="font-size:0.65rem;color:#3a4a3e">· últimos 5 juegos</span></div>')
    elif r.get("_form_unavailable"):
        form_html = '<div style="margin-top:5px;opacity:0.5;font-size:0.65rem;color:#3a4a3e">📡 Forma reciente no disponible (ESPN sin historial para esta liga)</div>' 

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
            '<div style="font-family:\'DM Sans\',sans-serif;font-size:0.65rem;'
            'color:rgba(201,168,76,0.6);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px">'
            + sport_icon + ' Análisis ' + sport_group + ' · Claude</div>'
            '<div style="font-family:\'DM Sans\',sans-serif;font-size:0.82rem;'
            'color:#b8c8b0;line-height:1.65">' + ai_text + '</div>'
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
                vote_parts.append(f'<span style="font-size:0.68rem;color:#9ca3af">{icon} {sig_name}: {detail}</span>')
            votes_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">' + "".join(vote_parts) + '</div>'

        conflict_html = ""
        if conflict_note:
            conflict_html = (f'<div style="font-size:0.7rem;color:#f97316;margin-top:3px;font-style:italic">'
                             f'⚠ {conflict_note}</div>')
        elif fatigue_note:
            conflict_html = (f'<div style="font-size:0.7rem;color:#60a5fa;margin-top:3px">'
                             f'{fatigue_note}</div>')

        consensus_html = (
            f'<div style="margin-top:8px;padding:8px 12px;background:rgba(0,0,0,0.2);'
            f'border-left:3px solid {c_color};border-radius:0 6px 6px 0">'
            f'<span style="font-size:0.75rem;font-weight:700;color:{c_color};'
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
            f'<div style="font-size:0.70rem;color:{color};margin-bottom:2px">'
            f'{sev_lbl} <span style="color:#9ca3af">[{team_name}]</span> {names_str}</div>'
        )

    if inj_parts:
        injury_html = (
            '<div style="margin-top:7px;padding:7px 12px;background:rgba(239,68,68,0.06);'
            'border-left:3px solid rgba(239,68,68,0.4);border-radius:0 6px 6px 0">'
            '<div style="font-size:0.65rem;color:rgba(239,68,68,0.6);letter-spacing:2px;'
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
        color = "#4ade80" if _rel < 0.05 else ("#f97316" if _rel > 0.15 else "#C9A84C")
        # Sport-specific unit and caveat
        sport_grp_d = LEAGUES.get(r.get("league",""), {}).get("group", "Soccer")
        unit = "pts" if sport_grp_d in ("Basketball","Football") else ("runs" if sport_grp_d == "Baseball" else "goles")
        caveat = " ⚠ sin pitcher" if sport_grp_d == "Baseball" else ""
        scoring_trend_html = (
            f'<div style="margin-top:5px;font-size:0.68rem;color:{color};opacity:0.85">'
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
              + '<span style="color:#6B7E6E;font-size:0.72rem;margin-left:6px">' + status + '</span>'
            '</div>'
            '<div class="pick-action">'
              '<span class="pick-action-arrow">&#9658;</span>'
              ' <span>' + bs["label"] + '</span>'
              ' <span style="font-size:1rem;color:#6B7E6E">' + ml_display + '</span>'
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
                '<div class="stat-item-val" style="font-size:0.9rem">' + conf_html + '</div>'
                '<div class="stat-item-lbl">Confianza</div>'
              '</div>'
            '</div>'
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
                '<span style="font-size:0.7rem;color:#6B7E6E;letter-spacing:1px">' + matchup_part + '</span>'
                '<span style="font-family:\'Cinzel\',sans-serif;font-size:0.92rem;color:#E0F7F0">' + pick_part + '</span>'
                '</div>'
            )
        else:
            leg_display = (
                '<span style="font-family:\'Cinzel\',sans-serif;font-size:0.95rem;'
                'color:#E0F7F0;margin-left:8px;flex:1">' + label + '</span>'
            )
        ev_color = "#4ade80" if ev >= 10 else "#C9A84C"
        legs_html += (
            '<div class="parlay-leg" style="align-items:flex-start">'
            + chip(mtype)
            + leg_display
            + '<div style="text-align:right;min-width:70px">'
              '<div style="color:#2EE8C0;font-family:\'Cinzel\',serif;font-weight:700">' + str(round(prob*100,1)) + '%</div>'
              '<div style="font-size:0.68rem;color:' + ev_color + '">EV +' + str(round(ev,1)) + '</div>'
              '</div>'
            + '</div>'
        )
        if i < len(bp["legs"])-1:
            legs_html += '<div class="parlay-connector" style="color:#1ABC9C;font-size:0.75rem;text-align:center;padding:4px 0;letter-spacing:3px">⊕ COMBINADA ⊕</div>'

    parlay_type_badge = (
        '<span style="font-size:0.65rem;color:#2EE8C0;letter-spacing:2px;'
        'background:rgba(26,188,156,0.1);padding:2px 8px;border-radius:3px;margin-left:8px">'
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
              'border-top:1px solid rgba(26,188,156,0.2)">'
              '<div class="stat-item">'
                '<div class="stat-item-val" style="color:#2EE8C0;font-size:1.4rem">' + str(round(bp["prob"]*100,1)) + '%</div>'
                '<div class="stat-item-lbl">Prob. Combo</div>'
              '</div>'
              '<div class="stat-item">'
                '<div class="stat-item-val val-cyan" style="font-size:1.4rem">+' + str(round(bp["payout"],0))[:-2] + '</div>'
                '<div class="stat-item-lbl">Pago / $100</div>'
              '</div>'
              '<div class="stat-item">'
                '<div class="stat-item-val val-gold" style="font-size:1.4rem">+' + str(round(bp["ev"],1)) + '</div>'
                '<div class="stat-item-lbl">EV / $100</div>'
              '</div>'
              '<div class="stat-item">' + conf + '</div>'
            '</div>'
            + dq_warn_html
          + '</div>'
        '</div>'
    )
# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-logo">THE DEN</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Gamblers · Analytics · Edge</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("**🔮 ORÁCULO**")
    n_sims=st.select_slider("Iteraciones",options=[1_000,2_500,5_000,10_000,25_000],value=10_000,
                            label_visibility="collapsed")
    st.caption(f"⚡ {n_sims:,} iteraciones por partido")
    st.divider()

    st.markdown("**LIGAS**")
    groups=sorted(set(v["group"] for v in LEAGUES.values()))
    sel_groups=st.multiselect("Grupos",groups,default=["Basketball","Baseball","Soccer","Hockey"],
                              label_visibility="collapsed")
    avail=[n for n,cfg in LEAGUES.items() if cfg["group"] in sel_groups]
    sel_leagues=st.multiselect("Ligas",avail,default=avail,label_visibility="collapsed")

    st.markdown("")
    run_sidebar = st.button("▶  ANALIZAR AHORA", use_container_width=True,
                            help="Corre el Oráculo para todos los partidos seleccionados")
    st.divider()

    use_demo=st.toggle("🧪 Modo demo",value=False)
    st.divider()
    st.caption("ESPN API · Monte Carlo · Poisson")
    st.caption("BTTS · O/U · DC · Parlays")
    st.caption("100% Gratis · Sin API externa")
    if st.button("↺  LIMPIAR CACHÉ"):
        st.cache_data.clear(); st.session_state.pop("sim_results",None); st.rerun()

    st.divider()
    st.markdown("**🧠 MEMORIA**")
    _tp_count_sb = st.session_state.get("_tp_count_cached", 0)
    if _tp_count_sb > 0:
        st.caption(f"✅ {_tp_count_sb} equipos en memoria")
    else:
        st.caption("⬜ Sin datos aún")
    if st.button("🧠  POBLAR MEMORIA", use_container_width=True,
                 help="Descarga últimos 10 partidos de TODOS los equipos y guarda en Google Sheets"):
        st.session_state["run_populate"] = True

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="den-header">
  <div class="den-logo">The Gamblers Den</div>
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
    with st.spinner("Consultando ESPN..."):
        games,fetch_errors=get_all_games(sel_leagues)
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
    _n_pos = len([r for r in _sr if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"] > 0])
    # ── AUTO-SAVE picks to pick_history (skip demo mode) ──────────────────
    if not is_demo and _gsheets_available():
        try:
            _ph_new = _ph_build_picks_from_sim(_sr, fuente="RONGOL")
            _ph_saved = _ph_save_picks(_ph_new)
            _ph_load.clear()  # invalidate cache
            if run_sidebar and _ph_saved:
                st.toast(f"📋 {_ph_saved} pick(s) guardados en historial", icon="📋")
        except Exception as _ph_err:
            pass  # never block the main flow
    if run_sidebar:
        st.toast(f"✓ {len(games)*n_sims:,} sims en {_elapsed:.1f}s · {_n_pos} value bets", icon="🔮")
    st.rerun()

# Stats bar
live_g=[g for g in games if g["state"]=="in"]
pre_g=[g for g in games if g["state"]=="pre"]
odds_g=[g for g in games if g["odds"]]
sr=st.session_state.get("sim_results",[])
pos_ev=len([r for r in sr if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0])

st.markdown(f"""<div class="stat-grid">
  <div class="stat-tile"><div class="stat-num">{len(games)}</div><div class="stat-label">Partidos</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#4ade80">{len(live_g)}</div><div class="stat-label">En Vivo</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#60a5fa">{len(pre_g)}</div><div class="stat-label">Próximos</div></div>
  <div class="stat-tile"><div class="stat-num">{len(odds_g)}</div><div class="stat-label">Con Cuotas</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#4ade80">{pos_ev}</div><div class="stat-label">Value Bets</div></div>
  <div class="stat-tile"><div class="stat-num" style="color:#1ABC9C">{len([r for r in sr if r["sim"].get("best_parlay") and r["sim"]["best_parlay"]["ev"]>0])}</div><div class="stat-label">Parlays EV+</div></div>
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
        f'<div style="text-align:center;margin-bottom:8px;font-size:0.72rem;'
        f'color:#4ade80;letter-spacing:1px">'
        f'🧠 Memoria activa: <b>{_tp_count_now}</b> equipos · '
        f'<b>{_tp_total_games}</b> partidos · '
        f'<b>{_tp_leagues}</b> ligas</div>',
        unsafe_allow_html=True
    )
elif _tp_err_now:
    st.markdown(
        f'<div style="text-align:center;margin-bottom:8px;font-size:0.72rem;'
        f'color:#ef4444;letter-spacing:1px">'
        f'🧠 Memoria: error — {_tp_err_now[:80]}</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div style="text-align:center;margin-bottom:8px;font-size:0.72rem;'
        'color:#6B7E6E;letter-spacing:1px">'
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
        border-radius:8px;padding:16px;margin-bottom:16px'>
        <div style='font-family:Cinzel,serif;color:#C9A84C;font-size:1rem;
        font-weight:700;margin-bottom:8px'>🧠 POBLANDO MEMORIA DE EQUIPOS</div>
        <div style='font-size:0.75rem;color:#9ca3af'>
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

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_picks, tab_sim, tab_parlays, tab_all, tab_reto = st.tabs([
    "🃏  RONGOL PICKS",
    f"🎯  PICKS  ({n_sims:,}×)",
    "🎰  PARLAYS DEL DÍA",
    "🔴  EN VIVO",
    "💰  RETO 13M",
])

# ══════════════════════════════════════════════════════════════════════════════
with tab_picks:
    sr=st.session_state.get("sim_results",[])
    if not sr:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">🎲</div>
          <div class="empty-title">Sin simulaciones</div>
          <div>Presiona <b>▶ ANALIZAR AHORA</b> en el sidebar o ve al tab <b>🔮 ORÁCULO</b> para generar los picks del día.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Detectar picks terminados ─────────────────────────────────────────────
        pick_game_ids = {r.get("id","") for r in sr if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0}
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
            st.markdown(f'''<div class="warn-banner" style="border-left:4px solid #4ade80;background:rgba(74,222,128,0.08)">
                ✅ <b>Pick(s) terminados:</b> {finished_names}<br>
                <span style="color:#6B7E6E;font-size:0.8rem">{len(pending_games_picks)} partidos pendientes disponibles.</span>
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
            n_new = len([r for r in new_sr_picks if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0])
            st.toast(f"✓ Nuevos picks generados · {n_new} EV+", icon="🃏")
            st.rerun()

        # ── Mostrar picks ─────────────────────────────────────────────────────────
        sr_cur = st.session_state.get("sim_results", [])
        all_bets=[]
        for r in sr_cur:
            bs=r["sim"].get("best_single")
            if bs and bs["ev"]>0: all_bets.append(r)
        all_bets.sort(key=lambda x: x["sim"]["best_single"]["ev"],reverse=True)

        # Indicador de estado
        n_post_p = len([g for g in games if g["state"]=="post"])
        n_live_p = len([g for g in games if g["state"]=="in"])
        n_pre_p  = len([g for g in games if g["state"]=="pre"])
        st.markdown(
            f'<div style="font-size:0.72rem;color:#6B7E6E;margin-bottom:8px">' +
            (f'<span style="color:#4ade80">⚡ {n_live_p} en vivo</span> · ' if n_live_p else "") +
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

        def _sport_best_pick(r):
            """Return the single best pick for a game, per sport rules."""
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
                if not ml: return None
                return {"market":"ML","label":team,"prob":prob,"ev":ev,"kelly":kelly}

            if sg == "Soccer":
                # Candidates: BTTS and O2.5 only (no Under picks in RONGOL)
                cands = []
                if sim.get("use_goals"):
                    # BTTS: only "Ambos Anotan SÍ" (never NO), only if EV+
                    _btts_ev = sim.get("btts_ev") or 0
                    _btts_pb = sim.get("p_btts") or 0
                    if _btts_ev > 0 and _btts_pb > 0:
                        cands.append({"market":"BTTS","label":"Ambos Anotan","prob":_btts_pb,"ev":_btts_ev,"kelly":0})
                    # O/U: only Over 2.5 (never Under anything), only if EV+
                    _o25_ev = sim.get("o25_ev") or 0
                    _o25_pb = sim.get("p_o25") or 0
                    if _o25_ev > 0 and _o25_pb > 0:
                        cands.append({"market":"O/U","label":"Over 2.5 goles","prob":_o25_pb,"ev":_o25_ev,"kelly":0})
                # Add ML (always, highest win%)
                _ml = best_ml()
                if _ml: cands.append(_ml)
                # Return best by probability
                return max(cands, key=lambda x: x["prob"]) if cands else None

            elif sg in ("Basketball", "Hockey"):
                # ML + O/U Over only (no Under in RONGOL for Hockey/Basketball)
                # Hockey: ESPN line is 5.5 or 6.5 (comes from odds.over_under)
                # Basketball: ESPN line typically 210-240
                # If no line available, MLB-style: use ML only
                cands = []
                _ml = best_ml()
                if _ml: cands.append(_ml)
                _ou_line = sim.get("ou_line") or ""
                _p_over  = sim.get("p_o_total") or 0
                if _ou_line and _p_over > 0:
                    try: _line = float(_ou_line)
                    except: _line = None
                    if _line and _p_over > 45:  # only if model actually favors Over (>45%)
                        _ev_ou = round((_p_over/100*(100/110) - (1-_p_over/100))*100, 1)
                        cands.append({"market":"O/U","label":f"Over {_line:.1f}","prob":_p_over,"ev":_ev_ou,"kelly":0})
                # Always include ML as fallback — ensures Basketball always has a pick
                if not cands and _ml:
                    cands.append(_ml)
                return max(cands, key=lambda x: x["prob"]) if cands else None

            else:  # Baseball, Football, NCAAF
                return best_ml()

        # ── Build 1 pick per sport group ──────────────────────────────────────
        # For each sport: take the game with the HIGHEST probability pick
        _sport_pools = {}  # sg -> list of (r, pick_dict)
        for r in sr_cur:
            g_state = next((g["state"] for g in games if g.get("id") == r.get("id")), "pre")
            if g_state == "post": continue
            bp = _sport_best_pick(r)
            if bp:
                sg = LEAGUES.get(r["league"], {}).get("group", "Soccer")
                _sport_pools.setdefault(sg, []).append({**r, "_pick": bp})

        # Sort each pool by prob desc, take top 1
        _SPORT_ORDER_R = ["Soccer","Basketball","Hockey","Baseball","Football"]
        rongol_picks = []
        for _sg in _SPORT_ORDER_R:
            pool = _sport_pools.get(_sg, [])
            if pool:
                pool.sort(key=lambda x: x["_pick"]["prob"], reverse=True)
                rongol_picks.append(pool[0])

        # Legacy: keep allowed_bets for DO parlay logic below
        allowed_bets = rongol_picks

        # ── STATS PANEL — accuracy from pick_history ─────────────────────────
        with st.expander("📊 Accuracy del Sistema", expanded=False):
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
                    _wr_c  = "#4ade80" if _wr>=55 else ("#C9A84C" if _wr>=45 else "#ef4444")

                    # ── Global stats tiles ────────────────────────────────────
                    st.markdown(
                        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0">'
                        f'<div style="flex:1;min-width:80px;background:rgba(74,222,128,0.10);'
                        f'border:1px solid rgba(74,222,128,0.3);border-radius:8px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.5rem;font-weight:900;color:{_wr_c};font-family:Cinzel,serif">{_wr}%</div>'
                        f'<div style="font-size:0.6rem;color:#6B7E6E;letter-spacing:1px;text-transform:uppercase">Win Rate</div>'
                        f'</div>'
                        f'<div style="flex:1;min-width:70px;background:rgba(74,222,128,0.07);'
                        f'border:1px solid rgba(74,222,128,0.2);border-radius:8px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.3rem;font-weight:800;color:#4ade80">{_n_gan}</div>'
                        f'<div style="font-size:0.6rem;color:#6B7E6E;text-transform:uppercase">✅ Ganados</div>'
                        f'</div>'
                        f'<div style="flex:1;min-width:70px;background:rgba(239,68,68,0.07);'
                        f'border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.3rem;font-weight:800;color:#ef4444">{_n_per}</div>'
                        f'<div style="font-size:0.6rem;color:#6B7E6E;text-transform:uppercase">❌ Perdidos</div>'
                        f'</div>'
                        f'<div style="flex:1;min-width:70px;background:rgba(201,168,76,0.07);'
                        f'border:1px solid rgba(201,168,76,0.2);border-radius:8px;padding:10px;text-align:center">'
                        f'<div style="font-size:1.3rem;font-weight:800;color:#C9A84C">{_n_psh}</div>'
                        f'<div style="font-size:0.6rem;color:#6B7E6E;text-transform:uppercase">🔄 Push</div>'
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

                    _mkt_color = {"ML":"#60a5fa","BTTS":"#4ade80","O/U":"#C9A84C","DO":"#a78bfa"}
                    st.markdown('<div style="font-size:0.65rem;color:#6B7E6E;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 6px 0">Por Mercado</div>', unsafe_allow_html=True)
                    for _m, _mc in sorted(_mkts.items()):
                        _mt = _mc["gan"] + _mc["per"] + _mc["psh"]
                        _mwr = round(_mc["gan"]/_mt*100,1) if _mt else 0
                        _mc_c = _mkt_color.get(_m,"#9ca3af")
                        _bar_w = _mwr
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0">'
                            f'<span style="background:{_mc_c}22;color:{_mc_c};border:1px solid {_mc_c}44;'
                            f'border-radius:3px;padding:1px 7px;font-size:0.62rem;font-weight:800;min-width:48px;text-align:center">{_m}</span>'
                            f'<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:4px;height:6px;overflow:hidden">'
                            f'<div style="width:{_bar_w}%;height:100%;background:{_mc_c};border-radius:4px"></div></div>'
                            f'<span style="font-size:0.7rem;font-weight:700;color:{_mc_c};min-width:38px;text-align:right">{_mwr}%</span>'
                            f'<span style="font-size:0.58rem;color:#6B7E6E;min-width:60px">{_mc["gan"]}G {_mc["per"]}P {_mc["psh"]}X</span>'
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
                    st.markdown('<div style="font-size:0.65rem;color:#6B7E6E;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 6px 0">Por Deporte</div>', unsafe_allow_html=True)
                    for _sg, _sc in sorted(_sgps.items()):
                        _st = _sc["gan"] + _sc["per"] + _sc["psh"]
                        _swr = round(_sc["gan"]/_st*100,1) if _st else 0
                        _sgc = "#4ade80" if _swr>=60 else ("#C9A84C" if _swr>=45 else "#ef4444")
                        _ico = _sg_ico.get(_sg,"🎯")
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0">'
                            f'<span style="font-size:0.75rem;min-width:20px">{_ico}</span>'
                            f'<span style="font-size:0.72rem;color:#E0F7F0;min-width:90px">{_sg}</span>'
                            f'<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:4px;height:6px;overflow:hidden">'
                            f'<div style="width:{_swr}%;height:100%;background:{_sgc};border-radius:4px"></div></div>'
                            f'<span style="font-size:0.7rem;font-weight:700;color:{_sgc};min-width:38px;text-align:right">{_swr}%</span>'
                            f'<span style="font-size:0.58rem;color:#6B7E6E;min-width:60px">{_sc["gan"]}G {_sc["per"]}P {_sc["psh"]}X</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("Aún no hay picks resueltos. Pulsa 🔍 Actualizar Resultados para traer los resultados de ESPN.")

        if not rongol_picks:
            st.markdown('<div class="warn-banner">No se encontraron picks. Intenta con más ligas o pulsa ▶ ANALIZAR.</div>', unsafe_allow_html=True)
        else:
            # ── helpers ──────────────────────────────────────────────────────
            _MKT_COLOR = {"ML":"#60a5fa","O/U":"#C9A84C","BTTS":"#4ade80","DO":"#a78bfa"}
            _SPORT_ICON = {"Basketball":"🏀","Soccer":"⚽","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}
            _CONF_LABEL = lambda p: ("🔥 ALTA" if p>=75 else ("⚡ MEDIA" if p>=55 else "🌡 BAJA"))
            _CONF_COLOR = lambda p: ("#4ade80" if p>=75 else ("#C9A84C" if p>=55 else "#ef4444"))

            def _prob_bar_html(prob, color):
                """Thin probability bar."""
                return (
                    f'<div style="margin:6px 0 2px 0;background:rgba(255,255,255,0.06);'
                    f'border-radius:4px;height:5px;overflow:hidden">'
                    f'<div style="width:{prob:.0f}%;height:100%;border-radius:4px;'
                    f'background:linear-gradient(90deg,{color}88,{color});'
                    f'box-shadow:0 0 8px {color}66"></div></div>'
                    f'<div style="font-size:0.58rem;color:{color};text-align:right;'
                    f'margin-top:1px">{prob:.0f}%</div>'
                )

            def _pick_diamante_card(r, tp, rank=0, is_fire=False):
                mc    = _MKT_COLOR.get(tp["market"],"#9ca3af")
                _sg_r = LEAGUES.get(r.get("league",""),{}).get("group","Soccer")
                _ml_i = _SPORT_ICON.get(_sg_r,"⚽")
                _mkt_icon_map = {"ML":_ml_i,"O/U":"📊","BTTS":"🎯","DO":"🔄"}
                icon  = _mkt_icon_map.get(tp["market"],"🎲")
                ev_s  = f'+{tp["ev"]:.1f}' if tp["ev"]>=0 else f'{tp["ev"]:.1f}'
                prob  = tp["prob"]
                conf_lbl = _CONF_LABEL(prob)
                conf_c   = _CONF_COLOR(prob)
                is_diamond = rank == 0

                # gradient border glow for diamond / fire
                if is_fire:
                    outer = (f'background:linear-gradient(135deg,rgba(255,106,0,0.18) 0%,#0d1f1a 55%,{mc}22 100%);'
                             f'border:1px solid rgba(255,106,0,0.6);'
                             f'box-shadow:0 0 28px rgba(255,106,0,0.25),inset 0 1px 0 rgba(255,106,0,0.15);')
                    title_size = "0.95rem"
                    label_size = "1.0rem"
                elif is_diamond:
                    outer = (f'background:linear-gradient(135deg,{mc}44 0%,#0d1f1a 60%,{mc}22 100%);'
                             f'border:1px solid {mc}88;box-shadow:0 0 24px {mc}33,inset 0 1px 0 {mc}22;')
                    title_size = "1.05rem"
                    label_size = "1.1rem"
                else:
                    outer = (f'background:linear-gradient(135deg,{mc}18 0%,#0a1a16 100%);'
                             f'border:1px solid {mc}44;')
                    title_size = "0.88rem"
                    label_size = "0.9rem"

                _low_conf = r.get("sim",{}).get("low_confidence", False)
                _lc_badge = (
                    '<span style="background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b55;'
                    'border-radius:3px;padding:1px 7px;font-size:0.58rem;font-weight:700;'
                    'letter-spacing:1px;margin-right:6px">⚠ SIN CUOTAS</span>' if _low_conf else ""
                )
                _fire_inline = (
                    '<span style="background:rgba(255,106,0,0.2);color:#ff6a00;'
                    'border:1px solid rgba(255,106,0,0.55);border-radius:3px;'
                    'padding:1px 7px;font-size:0.58rem;font-weight:900;'
                    'letter-spacing:1px;margin-right:6px">🔥 FUEGO</span>'
                ) if is_fire else ""
                rank_badge = (
                    f'<span style="background:{mc}22;color:{mc};border:1px solid {mc}55;'
                    f'border-radius:3px;padding:1px 7px;font-size:0.58rem;font-weight:700;'
                    f'letter-spacing:1px;margin-right:8px">#{rank+1}</span>' if not is_diamond and not is_fire else ""
                ) + _fire_inline + _lc_badge
                top_stripe = (
                    f'<div style="height:3px;border-radius:8px 8px 0 0;margin:-14px -14px 10px -14px;'
                    f'background:linear-gradient(90deg,transparent,{"#ff6a00" if is_fire else mc},{"#ff6a00aa" if is_fire else mc+"aa"},transparent);'
                    f'box-shadow:0 0 12px {"rgba(255,106,0,0.6)" if is_fire else mc+"88"}"></div>' if (is_diamond or is_fire) else ""
                )

                return (
                    f'<div style="border-radius:10px;padding:14px;margin:8px 0;{outer}">'
                    + top_stripe +
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap">'
                    f'<div style="min-width:0;flex:1">'
                    f'<div style="font-size:0.62rem;color:#6B7E6E;letter-spacing:1.5px;'
                    f'text-transform:uppercase;margin-bottom:3px">{rank_badge}{league_label(r["league"])}</div>'
                    f'<div style="font-size:{title_size};font-weight:700;color:#E0F7F0;line-height:1.3">'
                    f'{r["away_team"]} <span style="color:#3a4a3e;font-weight:400">vs</span> {r["home_team"]}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:1.15rem;font-weight:900;color:{mc};'
                    f'text-shadow:0 0 12px {mc}88;font-family:Cinzel,serif">EV {ev_s}</div>'
                    f'<div style="font-size:0.6rem;color:{conf_c};font-weight:700">{conf_lbl}</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="margin-top:10px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">'
                    f'<span style="background:{mc}25;color:{mc};border:1px solid {mc}66;'
                    f'border-radius:5px;padding:3px 10px;font-size:0.7rem;font-weight:800;'
                    f'letter-spacing:1px">{icon} {tp["market"]}</span>'
                    f'<span style="font-size:{label_size};font-weight:700;color:#FFE87C;'
                    f'font-family:Cinzel,serif;letter-spacing:0.5px">{tp["label"]}</span>'
                    f'</div>'
                    + _prob_bar_html(prob, mc) +
                    f'</div>'
                )

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

            # Render in rows of 2
            for _row_i in range(0, _n_picks, 2):
                _row_picks = rongol_picks[_row_i:_row_i+2]
                _cols = st.columns(len(_row_picks))
                for _ci, _rp in enumerate(_row_picks):
                    _abs_idx = _row_i + _ci
                    _is_fire = _abs_idx in _fire_indices
                    with _cols[_ci]:
                        _sg_label = _sport_labels.get(LEAGUES.get(_rp["league"],{}).get("group","Soccer"), "")
                        _fire_badge = (
                            '<span style="display:inline-block;background:rgba(255,100,0,0.18);'
                            'color:#ff6a00;border:1px solid rgba(255,106,0,0.5);border-radius:4px;'
                            'padding:1px 7px;font-size:0.6rem;font-weight:900;margin-left:6px;'
                            'vertical-align:middle">🔥 TOP</span>'
                        ) if _is_fire else ""
                        st.markdown(
                            f'<div style="font-size:0.6rem;color:#6B7E6E;letter-spacing:1.5px;'
                            f'text-transform:uppercase;margin-bottom:4px">{_sg_label}{_fire_badge}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(_pick_diamante_card(_rp, _rp["_pick"], rank=_row_i+_ci, is_fire=_is_fire), unsafe_allow_html=True)

            # ── DO PARLAY ─────────────────────────────────────────────────────
            _do_parlays = []
            for r in sr_cur:
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
                _mc_gl = {"BTTS":"#4ade80","O/U":"#C9A84C"}.get(_gl["market"],"#9ca3af")
                _comb_ev = _do["ev"] + _gl["ev"]
                st.markdown(
                    f'<div style="border-radius:10px;padding:14px;margin:8px 0;'
                    f'background:linear-gradient(135deg,rgba(167,139,250,0.12) 0%,#0a1a16 60%,rgba(74,222,128,0.08) 100%);'
                    f'border:1px solid rgba(167,139,250,0.5);'
                    f'box-shadow:0 0 20px rgba(167,139,250,0.15)">'
                    f'<div style="height:2px;border-radius:8px 8px 0 0;margin:-14px -14px 12px -14px;'
                    f'background:linear-gradient(90deg,transparent,#a78bfa,#4ade80,transparent)"></div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">'
                    f'<div>'
                    f'<div style="font-size:0.62rem;color:#6B7E6E;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:3px">'
                    f'🎯 PARLAY · {league_label(_g["league"])}</div>'
                    f'<div style="font-size:0.95rem;font-weight:700;color:#E0F7F0">'
                    f'{_g["away_team"]} vs {_g["home_team"]}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:1.1rem;font-weight:900;color:#a78bfa;font-family:Cinzel,serif">'
                    f'EV +{_comb_ev:.1f}</div>'
                    f'<div style="font-size:0.58rem;color:#6B7E6E">combinado</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="margin-top:10px;display:flex;align-items:center;gap:6px;flex-wrap:wrap">'
                    f'<span style="background:{_mc_do}22;color:{_mc_do};border:1px solid {_mc_do}55;'
                    f'border-radius:5px;padding:3px 9px;font-size:0.68rem;font-weight:800">DO</span>'
                    f'<span style="color:#E0F7F0;font-size:0.82rem">{_do["label"]}</span>'
                    f'<span style="color:#3a4a3e;font-size:1rem;margin:0 2px">✕</span>'
                    f'<span style="background:{_mc_gl}22;color:{_mc_gl};border:1px solid {_mc_gl}55;'
                    f'border-radius:5px;padding:3px 9px;font-size:0.68rem;font-weight:800">{_gl["market"]}</span>'
                    f'<span style="color:#E0F7F0;font-size:0.82rem">{_gl["label"]}</span>'
                    f'</div>'
                    f'<div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap">'
                    f'<span style="font-size:0.62rem;color:{_mc_do}">DO EV +{_do["ev"]:.1f} · {_do.get("prob",0):.0f}%</span>'
                    f'<span style="font-size:0.62rem;color:{_mc_gl}">{_gl["market"]} EV +{_gl["ev"]:.1f} · {_gl["prob"]:.0f}%</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # (PICKS FUEGO removed — 1 per sport shown in grid above)

        # Avoid
        avoid=[r for r in sr_cur if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]<-15]
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
        st.markdown(f'<div style="text-align:center;font-family:\'DM Sans\',sans-serif;font-size:0.72rem;color:#3a4a3e">📅 {today_str} · {total_sims:,} simulaciones · {_src}</div>',unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
with tab_sim:
    # ══════════════════════════════════════════════════════════════════════════
    # PRÓXIMOS PARTIDOS — sport tiles + date/league expanders  (TOP of tab)
    # ══════════════════════════════════════════════════════════════════════════
    from datetime import timedelta as _td_pt
    _now_mx_pt = datetime.now(timezone.utc) - _td_pt(hours=6)
    _meses_pt  = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                  "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    _SPORT_META_P = {
        "Basketball": {"emoji":"🏀","color":"#f97316","accent":"rgba(249,115,22,0.12)"},
        "Soccer":     {"emoji":"⚽","color":"#4ade80","accent":"rgba(74,222,128,0.10)"},
        "Hockey":     {"emoji":"🏒","color":"#60a5fa","accent":"rgba(96,165,250,0.12)"},
        "Baseball":   {"emoji":"⚾","color":"#ef4444","accent":"rgba(239,68,68,0.10)"},
        "Football":   {"emoji":"🏈","color":"#a78bfa","accent":"rgba(167,139,250,0.10)"},
    }
    _SPORTS_ORDER_P = ["Basketball","Soccer","Hockey","Baseball","Football"]

    _today_mx_p = _now_mx_pt.strftime("%Y-%m-%d")
    _tom_mx_p   = (_now_mx_pt + _td_pt(days=1)).strftime("%Y-%m-%d")
    _d2_mx_p    = (_now_mx_pt + _td_pt(days=2)).strftime("%Y-%m-%d")

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
        _time_html = f'<span style="color:#C9A84C;font-size:0.65rem;flex-shrink:0">{_time}</span>' if _time else ""
        _o = g.get("odds",{}) or {}
        _op = []
        if _o.get("over_under"): _op.append(f"O/U {_o['over_under']}")
        if _o.get("home_ml"):    _op.append(f"ML {_o['home_ml']}")
        _oh = f'<div style="color:#C9A84C;font-size:0.6rem;margin-top:2px">{" · ".join(_op)}</div>' if _op else ""
        _ph = ""
        _rp = {_rr.get("id",""): _rr for _rr in st.session_state.get("sim_results",[])}.get(g.get("id",""))
        if _rp:
            _bs = _rp["sim"].get("best_single",{}) or {}
            if _bs and _bs.get("ev",0) > 0:
                _mc2 = {"ML":"#60a5fa","O/U":"#C9A84C","BTTS":"#4ade80","DO":"#a78bfa"}.get(_bs.get("market",""),"#9ca3af")
                _ev2s = f'+{_bs["ev"]:.1f}' if _bs["ev"]>=0 else f'{_bs["ev"]:.1f}'
                _ph = (
                    f'<div style="margin-top:4px;display:flex;align-items:center;gap:4px;flex-wrap:wrap">'
                    f'<span style="background:{_mc2}22;color:{_mc2};border:1px solid {_mc2}55;'
                    f'border-radius:3px;padding:0 4px;font-size:0.56rem;font-weight:700">{_bs.get("market","")}</span>'
                    f'<span style="color:#E0F7F0;font-size:0.65rem;min-width:0;overflow:hidden;'
                    f'text-overflow:ellipsis;white-space:nowrap">{_bs.get("label","")}</span>'
                    f'<span style="color:#4ade80;font-size:0.58rem;margin-left:auto;flex-shrink:0">'
                    f'EV {_ev2s}</span>'
                    f'</div>'
                )
        return (
            f'<div style="padding:7px 8px;margin:3px 0;border-radius:7px;'
            f'background:{sm["accent"]};border-left:2px solid {sm["color"]}66;overflow:hidden">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4px">'
            f'<div style="min-width:0;overflow:hidden;flex:1">'
            f'<div style="font-size:0.72rem;font-weight:700;color:#E0F7F0;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{g["away_team"]}</div>'
            f'<div style="font-size:0.62rem;color:#6B7E6E;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">@ {g["home_team"]}</div>'
            f'</div>'
            f'<div style="flex-shrink:0;padding-left:4px">{_time_html}</div>'
            f'</div>'
            f'{_oh}{_ph}'
            f'</div>'
        )

    # Build tree — pre games only, by sport → date → league
    _tree_p = {}
    for _g in games:
        if _g["state"] in ("post", "in"): continue   # skip finished + live
        _sg_p = LEAGUES.get(_g["league"], {}).get("group", "Soccer")
        _gd   = _mx_date_p(_g)
        if _gd < _today_mx_p or _gd > _d2_mx_p: continue
        _tree_p.setdefault(_sg_p, {}).setdefault(_gd, {}).setdefault(_g["league"], []).append(_g)

    _sports_p = [s for s in _SPORTS_ORDER_P if s in _tree_p]
    _total_p  = sum(len(gs) for sp in _sports_p for dmap in _tree_p[sp].values() for gs in dmap.values())

    st.markdown(f'<div class="section-heading">📅 PRÓXIMOS PARTIDOS</div>', unsafe_allow_html=True)

    if not _sports_p:
        st.markdown('<div class="warn-banner">No hay partidos próximos. Pulsa ▶ ANALIZAR para cargar datos.</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="font-size:0.68rem;color:#6B7E6E;margin-bottom:10px">'
            f'{_total_p} partidos · {len(_sports_p)} deportes · hora CDMX</div>',
            unsafe_allow_html=True
        )
        # Sport tiles — ALL in one row
        _sp_cols_p = st.columns(len(_sports_p))
        for _ci_p, _sp_p in enumerate(_sports_p):
            _smp = _SPORT_META_P[_sp_p]
            _n_p = sum(len(gs) for dmap in _tree_p[_sp_p].values() for gs in dmap.values())
            with _sp_cols_p[_ci_p]:
                st.markdown(
                    f'<div style="text-align:center;padding:8px 3px;border-radius:9px;'
                    f'background:{_smp["accent"]};border:1px solid {_smp["color"]}55;margin-bottom:8px">'
                    f'<div style="font-size:1.5rem;line-height:1">{_smp["emoji"]}</div>'
                    f'<div style="font-size:0.58rem;font-weight:700;color:{_smp["color"]};'
                    f'letter-spacing:0.5px;text-transform:uppercase;margin-top:3px">'
                    f'{_sp_p}</div>'
                    f'<div style="font-size:0.55rem;color:#6B7E6E;margin-top:1px">{_n_p} juegos</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    # ── RE-SIMULAR button (compact, inside games section) ─────────────────
    _col_rs, _ = st.columns([1, 3])
    with _col_rs:
        if st.button(f"🔄 RE-SIMULAR ({n_sims:,}×)", use_container_width=True, key="btn_resim_picks"):
            t0 = time.time()
            sr2 = run_all_simulations(games, n=n_sims)
            elapsed = time.time() - t0
            st.session_state["sim_results"] = sr2
            st.session_state["last_sim_demo"] = is_demo
            n_pos = len([r for r in sr2 if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"] > 0])
            st.toast(f"✓ {len(games)*n_sims:,} sims en {elapsed:.1f}s · {n_pos} value bets", icon="🔮")
            st.rerun()
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
            if _ou_line and (_p_over > 0 or _p_under > 0):
                try: _line = float(_ou_line)
                except: _line = None
                if _line:
                    if _p_over >= _p_under:
                        cands.append({"market":"O/U","label":f"Over {_line:.1f}","prob":_p_over,"ev":0})
                    else:
                        cands.append({"market":"O/U","label":f"Under {_line:.1f}","prob":_p_under,"ev":0})
        return max(cands, key=lambda x: x["prob"])

    def _oracle_card(g, sm):
        """Full oracle card for a game — always shows a pick, no EV+ gate."""
        _r    = _sim_map.get(g.get("id",""))
        _time = _mx_time_p(g)
        _time_s = f' · <span style="color:#C9A84C">{_time}</span>' if _time else ""
        _sd   = (g.get("status_detail") or "").replace("<","").replace(">","").replace("/","").split("\n")[0].strip()
        _low_c  = _r["sim"].get("low_confidence",False) if _r else False
        _lc_tag = '<span style="background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b44;border-radius:3px;padding:1px 5px;font-size:0.55rem;margin-left:4px">⚠ sin cuotas</span>' if _low_c else ""
        _has_ev = bool(_r and _r["sim"].get("best_single") and _r["sim"]["best_single"].get("ev",0)>0)

        _html = (
            f'<div class="game-row{" game-row-ev" if _has_ev else ""}" style="border-left:3px solid {sm["color"]}88;margin:4px 0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:4px">'
            f'<div>'
            f'<div class="game-title">{g["away_team"]} @ {g["home_team"]}</div>'
            f'<div class="game-meta">{league_label(g["league"])} · {_sd}{_time_s}{_lc_tag}</div>'
            f'</div>'
        )

        if not _r:
            _html += '<div style="color:#3a4a3e;font-size:0.68rem;align-self:center">Sin simular</div></div></div>'
            return _html

        sim = _r["sim"]
        dq  = sim["data_quality"]
        dqc = "#4ade80" if dq>=70 else "#C9A84C" if dq>=40 else "#ef4444"

        # ── Pick badge — always one pick, no EV+ required ────────────────────
        bp  = _oracle_pick(_r)
        _bc = {"ML":"#60a5fa","O/U":"#C9A84C","BTTS":"#4ade80"}.get(bp["market"],"#9ca3af")
        _ev = bp.get("ev",0) or 0
        _ev_str = f"+{_ev:.1f}" if _ev >= 0 else f"{_ev:.1f}"
        _ev_c   = "#4ade80" if _ev>=10 else ("#C9A84C" if _ev>=0 else "#ef4444")
        badge = (
            f'<span style="background:{_bc}22;color:{_bc};border:1px solid {_bc}55;'
            f'border-radius:3px;padding:1px 6px;font-size:0.62rem;font-weight:800;margin-right:5px">{bp["market"]}</span>'
            f'<span style="font-weight:700;font-size:0.8rem;color:#FFE87C">{bp["label"]}</span>'
            f'<span style="color:{_ev_c};font-size:0.68rem;margin-left:6px">EV {_ev_str}</span>'
            f'<span style="color:#6B7E6E;font-size:0.62rem;margin-left:4px">· {bp["prob"]:.0f}%</span>'
        )

        _html += (
            f'<div style="text-align:right;font-size:0.65rem;color:#6B7E6E;flex-shrink:0">'
            f'ML {sim["away_ml"] or "—"}/{sim["home_ml"] or "—"}'
            f'<br><span style="color:{dqc}">DQ {dq:.0f}%</span></div>'
            f'</div>'
            f'<div style="margin-top:4px">{badge}</div>'
        )

        # Win probability bars
        _html += f'<div style="margin-top:6px">{bar(sim["away_pct"],"#60a5fa",g["away_team"])}' 
        if sim["is_soccer"]: _html += bar(sim["draw_pct"],"#a78bfa","Empate")
        _html += bar(sim["home_pct"],"#f97316",g["home_team"]) + "</div>"

        # Goals / totals footer
        if sim.get("use_goals") and sim.get("p_btts") is not None:
            btc = "#4ade80" if (sim.get("btts_ev") or 0)>0 else "#6B7E6E"
            o2c = "#C9A84C" if (sim.get("o25_ev") or 0)>0 else "#6B7E6E"
            o3c = "#C9A84C" if (sim.get("o35_ev") or 0)>0 else "#6B7E6E"
            dq_src = "ML+Récords" if dq>=50 else ("Récords" if dq>=25 else ("Prior" if dq>0 else "Sin datos"))
            _html += (
                f'<div style="font-size:0.65rem;margin-top:4px;display:flex;gap:10px;flex-wrap:wrap">'
                f'<span style="color:{btc}">⚽ BTTS {sim["p_btts"]}%</span>'
                f'<span style="color:{o2c}">O2.5 {sim["p_o25"]}%</span>'
                f'<span style="color:{o3c}">O3.5 {sim.get("p_o35","—")}%</span>'
                f'<span style="color:#3a4a3e;margin-left:auto">{dq_src}</span>'
                f'</div>'
            )
        elif sim.get("ou_line") and sim.get("p_o_total") is not None:
            _otc = "#C9A84C" if (sim.get("p_o_total") or 0)>=50 else "#6B7E6E"
            _utc = "#C9A84C" if (sim.get("p_u_total") or 0)>=50 else "#6B7E6E"
            _html += (
                f'<div style="font-size:0.65rem;margin-top:4px;display:flex;gap:10px;flex-wrap:wrap">'
                f'<span style="color:#6B7E6E">Total {sim["ou_line"]}</span>'
                f'<span style="color:{_otc}">Over {sim.get("p_o_total","—")}%</span>'
                f'<span style="color:{_utc}">Under {sim.get("p_u_total","—")}%</span>'
                f'</div>'
            )

        _html += '</div>'
        return _html

    # Expanders — one per sport, games with oracle inside
    for _sp_p in _sports_p:
        _smp   = _SPORT_META_P[_sp_p]
        _dks_p = sorted(_tree_p[_sp_p].keys())
        _n_p   = sum(len(gs) for dmap in _tree_p[_sp_p].values() for gs in dmap.values())
        # Count EV+ picks in this sport
        _ev_count = sum(
            1 for dmap in _tree_p[_sp_p].values()
            for gs in dmap.values() for g in gs
            if _sim_map.get(g.get("id",""),{}).get("sim",{}).get("best_single",{}) and
               _sim_map.get(g.get("id",""),{})["sim"]["best_single"]["ev"] > 0
        )
        _ev_badge = f" 🔥{_ev_count}" if _ev_count else ""
        with st.expander(
            f'{_smp["emoji"]} {_sp_p} — {_n_p} partidos{_ev_badge}',
            expanded=(_today_mx_p in _tree_p[_sp_p])
        ):
            for _dk_p in _dks_p:
                # Date header
                st.markdown(
                    f'<div style="font-size:0.62rem;font-weight:700;color:#C9A84C;'
                    f'letter-spacing:2px;text-transform:uppercase;padding:4px 0 6px 0;'
                    f'border-bottom:1px solid rgba(201,168,76,0.2);margin-bottom:6px">'
                    f'{_fmt_date_p(_dk_p)}</div>',
                    unsafe_allow_html=True
                )
                for _lg_p, _lg_games_p in sorted(_tree_p[_sp_p][_dk_p].items()):
                    # League header
                    st.markdown(
                        f'<div style="font-size:0.58rem;color:{_smp["color"]};font-weight:700;'
                        f'letter-spacing:1.5px;text-transform:uppercase;margin:8px 0 4px 0">'
                        f'{league_label(_lg_p)} · {len(_lg_games_p)}</div>',
                        unsafe_allow_html=True
                    )
                    # Each game as full oracle card (1 per row — full width for detail)
                    for _gg_p in _lg_games_p:
                        st.markdown(_oracle_card(_gg_p, _smp), unsafe_allow_html=True)
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

    # CSV export (collapsed)
    _sr_all = st.session_state.get("sim_results", [])
    if _sr_all:
        with st.expander("⬇ Exportar CSV", expanded=False):
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
with tab_parlays:
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
            if bp and bp["ev"] > 0:
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
            st.markdown(f'''<div class="warn-banner" style="border-left:4px solid #4ade80;background:rgba(74,222,128,0.08)">
                ✅ <b>Partido(s) del parlay terminaron:</b> {finished_names}<br>
                <span style="color:#6B7E6E;font-size:0.8rem">{len(pending_games)} partidos pendientes disponibles para nuevo parlay.</span>
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
            n_new_parlays = len([r for r in new_sr if r["sim"].get("best_parlay") and r["sim"]["best_parlay"]["ev"]>0])
            st.toast(f"✓ Parlay actualizado · {n_new_parlays} combinadas EV+", icon="🎰")
            st.rerun()

        # ── Mostrar parlays (siempre el más reciente en session_state) ────────────
        sr_current = st.session_state.get("sim_results", [])
        parlays = [r for r in sr_current if r["sim"].get("best_parlay") and r["sim"]["best_parlay"]["ev"]>0]
        parlays.sort(key=lambda x: x["sim"]["best_parlay"]["ev"], reverse=True)

        # ── Helpers para armar el parlay de 2 patas de un mismo partido ──────
        _MKT_C = {"ML":"#60a5fa","O/U":"#C9A84C","BTTS":"#4ade80","DO":"#a78bfa"}
        _SG_ICON = {"Soccer":"⚽","Basketball":"🏀","Hockey":"🏒","Baseball":"⚾","Football":"🏈"}
        _SG_COLOR = {"Soccer":"#4ade80","Basketball":"#f97316","Hockey":"#60a5fa",
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
                    try: _line = float(_ou_line)
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

        for r in sr_current:
            g_state = next((g["state"] for g in games if g.get("id")==r.get("id")), "pre")
            if g_state == "post": continue
            for gp in _build_game_parlays(r):
                _sport_game_pools.setdefault(gp["sg"], []).append(gp)
                if gp["combo_type"] == "AA + O2.5":
                    _soccer_btts_o25.append(gp)

        # Best 1 per sport (highest combined prob among all combo types)
        _day_parlays = []
        for _sg in _SPORT_ORDER_PAR:
            pool = _sport_game_pools.get(_sg, [])
            if pool:
                pool.sort(key=lambda x: x["comb_prob"], reverse=True)
                _day_parlays.append(pool[0])

        # Best AA+O2.5 soccer combo (featured separately)
        _best_btts_o25 = (
            max(_soccer_btts_o25, key=lambda x: x["comb_prob"])
            if _soccer_btts_o25 else None
        )

        if _day_parlays:
            n_post  = len([g for g in games if g["state"]=="post"])
            n_live  = len([g for g in games if g["state"]=="in"])
            n_pre   = len([g for g in games if g["state"]=="pre"])
            status_color = "#4ade80" if n_live > 0 else "#60a5fa"
            st.markdown(
                f'<div style="font-size:0.72rem;color:#6B7E6E;margin-bottom:12px">' +
                (f'<span style="color:{status_color}">⚡ {n_live} en vivo</span> · ' if n_live else "") +
                f'{n_pre} próximos · {n_post} terminados</div>',
                unsafe_allow_html=True
            )

            st.markdown('<div class="section-heading">🎰 PARLAYS DEL DÍA · 1 POR DEPORTE</div>', unsafe_allow_html=True)

            # ── Helper: render a generic 2-leg parlay card ────────────────────
            def _render_parlay_card(dp, featured=False):
                """Render any 2-leg parlay dict (leg1+leg2, generic labels)."""
                _sg   = dp["sg"]
                _g    = dp["game"]
                _l1   = dp["leg1"]
                _l2   = dp["leg2"]
                _ct   = dp.get("combo_type","")
                _mc1  = _MKT_C.get(_l1["market"],"#60a5fa")
                _mc2  = _MKT_C.get(_l2["market"],"#C9A84C")
                _sgc  = "#4ade80" if featured else _SG_COLOR.get(_sg,"#4ade80")
                _sgi  = _SG_ICON.get(_sg,"🎯")
                _lg   = league_label(_g["league"])
                _matchup = f'{_g["away_team"]} @ {_g["home_team"]}'
                _border_extra = "box-shadow:0 0 30px rgba(74,222,128,0.22);" if featured else ""
                _feat_stripe  = (
                    f'background:linear-gradient(90deg,transparent,#4ade80,#C9A84C,transparent)'
                ) if featured else f'background:linear-gradient(90deg,transparent,{_sgc},transparent)'
                _feat_label = (
                    '<span style="background:rgba(74,222,128,0.18);color:#4ade80;'
                    'border:1px solid rgba(74,222,128,0.5);border-radius:3px;'
                    'padding:1px 7px;font-size:0.58rem;font-weight:900;margin-left:6px">'
                    '⚽ GOLES COMBO</span>'
                ) if featured else ""

                return (
                    f'<div style="border-radius:10px;padding:14px 16px;margin:8px 0;'
                    f'background:linear-gradient(135deg,{_sgc}14 0%,#0a1a16 60%,{_sgc}08 100%);'
                    f'border:1px solid {_sgc}{"66" if featured else "44"};{_border_extra}">'
                    f'<div style="height:2px;border-radius:8px 8px 0 0;margin:-14px -16px 12px -16px;{_feat_stripe}"></div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap">'
                    f'<div>'
                    f'<div style="font-size:0.58rem;color:#6B7E6E;letter-spacing:2px;text-transform:uppercase;margin-bottom:3px">'
                    f'{_sgi} {_sg} · {_lg}{_feat_label}</div>'
                    f'<div style="font-size:0.88rem;font-weight:700;color:#E0F7F0">{_matchup}</div>'
                    f'<div style="font-size:0.65rem;color:#6B7E6E;margin-top:2px">{_ct}</div>'
                    f'</div>'
                    f'<div style="text-align:right;flex-shrink:0">'
                    f'<div style="font-size:1.1rem;font-weight:900;color:{_sgc};font-family:Cinzel,serif">{dp["comb_prob_pct"]}%</div>'
                    f'<div style="font-size:0.55rem;color:#6B7E6E">prob. combinada</div>'
                    f'</div>'
                    f'</div>'
                    f'<div style="margin-top:10px;display:flex;flex-direction:column;gap:7px">'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="background:{_mc1}22;color:{_mc1};border:1px solid {_mc1}55;'
                    f'border-radius:4px;padding:2px 9px;font-size:0.66rem;font-weight:800;flex-shrink:0">{_l1["market"]}</span>'
                    f'<span style="font-size:0.88rem;color:#E0F7F0;font-weight:600">{_l1["label"]}</span>'
                    f'<span style="margin-left:auto;font-size:0.62rem;color:{_mc1};font-weight:700">{_l1["prob"]:.0f}%</span>'
                    f'</div>'
                    f'<div style="font-size:0.62rem;color:#3a4a3e;text-align:center;letter-spacing:3px">✕ COMBO ✕</div>'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="background:{_mc2}22;color:{_mc2};border:1px solid {_mc2}55;'
                    f'border-radius:4px;padding:2px 9px;font-size:0.66rem;font-weight:800;flex-shrink:0">{_l2["market"]}</span>'
                    f'<span style="font-size:0.88rem;color:#E0F7F0;font-weight:600">{_l2["label"]}</span>'
                    f'<span style="margin-left:auto;font-size:0.62rem;color:{_mc2};font-weight:700">{_l2["prob"]:.0f}%</span>'
                    f'</div>'
                    f'</div>'
                    f'<div style="display:flex;align-items:center;gap:16px;margin-top:10px;padding-top:8px;'
                    f'border-top:1px solid {_sgc}22;flex-wrap:wrap">'
                    f'<span style="font-size:0.62rem;color:#2EE8C0">Pago est. +${dp["payout"]:.0f}/100</span>'
                    f'<span style="margin-left:auto;background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);'
                    f'border-radius:4px;padding:2px 8px;font-size:0.6rem;color:#ef4444">⚠️ STAKE BAJO</span>'
                    f'</div>'
                    f'</div>'
                )

            # ── FEATURED: AA + O2.5 soccer combo ─────────────────────────────
            if _best_btts_o25:
                st.markdown(
                    '<div style="font-size:0.68rem;color:#4ade80;letter-spacing:2px;'
                    'text-transform:uppercase;margin:4px 0 2px 0">'
                    '⚽ COMBO GOLES DESTACADO · Ambos Anotan + Over 2.5</div>',
                    unsafe_allow_html=True
                )
                st.markdown(_render_parlay_card(_best_btts_o25, featured=True), unsafe_allow_html=True)
                st.markdown('<div class="den-divider" style="margin:10px 0"></div>', unsafe_allow_html=True)

            # ── 1 per sport ───────────────────────────────────────────────────
            for _dp in _day_parlays:
                st.markdown(_render_parlay_card(_dp), unsafe_allow_html=True)

            st.markdown(
                '<div class="warn-banner" style="margin-top:12px">'
                '⚠ Cuotas de BTTS/O/U asumidas a −110/−115. Verifica en tu casa. '
                'Parlays = alta varianza — usa máx 1-2% del bankroll por parlay.</div>',
                unsafe_allow_html=True
            )
        elif pending_games:
            all_parlays_raw = [r for r in sr if r["sim"].get("best_parlay")]
            if all_parlays_raw:
                best_raw = max(all_parlays_raw, key=lambda r: r["sim"]["best_parlay"].get("ev",-999))
                bp = best_raw["sim"]["best_parlay"]
                ev_str = f"{bp.get('ev',0):+.1f}"
                st.warning(f"\u26a0 No hay parlays con EV positivo hoy. El mejor disponible tiene EV {ev_str} \u2014 apuesta con precauci\u00f3n.")
                st.markdown(render_parlay_card(best_raw), unsafe_allow_html=True)
            else:
                st.info("No hay suficientes partidos para armar parlays hoy. Selecciona m\u00e1s ligas o espera m\u00e1s juegos.")
        else:
            st.markdown('<div class="warn-banner">Todos los partidos del día han terminado. No hay partidos pendientes para nuevos parlays.</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
with tab_all:
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

        for g in live_games:
            sim         = run_monte_carlo(g, n=5_000)
            dq          = sim["data_quality"]
            sport_group = LEAGUES.get(g["league"], {}).get("group", "Soccer")
            minute      = parse_live_minute(g.get("status_detail", ""))

            try:
                hs = int(g.get("home_score") or 0)
                as_ = int(g.get("away_score") or 0)
            except:
                hs, as_ = 0, 0
            score_str   = f"{as_} – {hs}" if (g.get("home_score") or g.get("away_score")) else "–"
            min_str     = f"min {minute}" if minute else g.get("status_detail","")

            # Get contextual pick
            if sport_group == "Soccer":
                result = live_pick_soccer(g, sim, minute)
            else:
                result = live_pick_other(g, sim)

            if not result:
                continue

            picks     = result["picks"]
            headline  = result.get("headline","")
            # Best pick = highest probability among suggestions
            best      = max(picks, key=lambda p: p["prob"])

            prob_color  = "#4ade80" if best["prob"] >= 70 else "#C9A84C" if best["prob"] >= 55 else "#f97316"
            border_col  = "rgba(255,60,60,0.7)"

            # Build HTML
            picks_html = ""
            for i, pk in enumerate(picks):
                pc = "#4ade80" if pk["prob"] >= 70 else "#C9A84C" if pk["prob"] >= 55 else "#f97316"
                picks_html += (
                    f'<div style="display:flex;align-items:center;gap:10px;'
                    f'padding:8px 12px;margin-bottom:6px;'
                    f'background:rgba(255,232,124,{0.08 if i==0 else 0.03});'
                    f'border-radius:6px;border-left:3px solid {"#FFE87C" if i==0 else "#3a4a3e"}">'
                    f'<span style="color:#FFE87C;font-size:{1.3 if i==0 else 1.0}rem">&#9658;</span>'
                    f'<div style="flex:1">'
                    f'<span style="font-family:Cinzel,serif;font-size:{1.15 if i==0 else 0.95}rem;'
                    f'font-weight:{"900" if i==0 else "600"};color:#FFE87C;letter-spacing:1.5px">'
                    f'{pk["label"]}</span>'
                    f'<div style="font-size:0.75rem;color:#8a9e8a;margin-top:3px;line-height:1.4">'
                    f'{pk["rationale"]}</div>'
                    f'</div>'
                    f'<div style="text-align:center;min-width:48px">'
                    f'<div style="font-family:Cinzel,serif;font-size:1.1rem;color:{pc};font-weight:700">'
                    f'{pk["prob"]:.0f}%</div>'
                    f'<div style="font-size:0.55rem;color:#6B7E6E;letter-spacing:1px">PROB</div>'
                    f'</div></div>'
                )

            stats_html = (
                f'<div style="display:flex;gap:16px;flex-wrap:wrap;padding:8px 0;'
                f'border-top:1px solid rgba(255,255,255,0.06);margin-top:8px">'
                f'<div style="text-align:center"><div style="font-family:Cinzel,serif;font-size:1rem;color:#60a5fa;font-weight:700">'
                f'{sim["away_pct"]:.0f}%</div><div style="font-size:0.55rem;color:#6B7E6E;letter-spacing:1px">'
                f'{g["away_team"][:11]}</div></div>'
                + (f'<div style="text-align:center"><div style="font-family:Cinzel,serif;font-size:1rem;color:#a78bfa;font-weight:700">'
                   f'{sim["draw_pct"]:.0f}%</div><div style="font-size:0.55rem;color:#6B7E6E;letter-spacing:1px">Empate</div></div>'
                   if sim["is_soccer"] else '')
                + f'<div style="text-align:center"><div style="font-family:Cinzel,serif;font-size:1rem;color:#f97316;font-weight:700">'
                f'{sim["home_pct"]:.0f}%</div><div style="font-size:0.55rem;color:#6B7E6E;letter-spacing:1px">'
                f'{g["home_team"][:11]}</div></div>'
                + (f'<div style="text-align:center"><div style="font-family:Cinzel,serif;font-size:1rem;color:#4ade80;font-weight:700">'
                   f'{sim["p_btts"]}%</div><div style="font-size:0.55rem;color:#6B7E6E;letter-spacing:1px">BTTS%</div></div>'
                   if sim.get("p_btts") and sport_group == "Soccer" else '')
                + (f'<div style="text-align:center"><div style="font-family:Cinzel,serif;font-size:1rem;color:#C9A84C;font-weight:700">'
                   f'{sim["p_o25"]}%</div><div style="font-size:0.55rem;color:#6B7E6E;letter-spacing:1px">O2.5%</div></div>'
                   if sim.get("p_o25") and sport_group == "Soccer" else '')
                + f'<div style="margin-left:auto;text-align:right"><div style="font-size:0.65rem;color:#3a4a3e">DQ {dq:.0f}%</div>'
                f'<div style="font-size:0.65rem;color:#3a4a3e">5,000 sims</div></div>'
                f'</div>'
            )

            # xG validation panel — only for Soccer when there's an O/U pick
            xg_html = ""
            if sport_group == "Soccer":
                ou_pick = next((p for p in picks if p["market"] == "O/U" and "Over" in p["label"]), None)
                if ou_pick:
                    total_g = hs + as_
                    ou_line_val = total_g + 1.5
                    xgv = xg_live_validator(g, ou_line_val, ou_pick["prob"], minute)
                    adj   = xgv["adjusted_prob"]
                    conf  = xgv["confidence"]
                    delta = adj - ou_pick["prob"]
                    adj_c = "#4ade80" if adj >= 70 else "#C9A84C" if adj >= 55 else "#f97316"
                    conf_c = {"alta":"#4ade80","media":"#C9A84C","baja":"#f97316"}.get(conf,"#6B7E6E")
                    delta_str = (f"▲ +{delta:.0f}pp" if delta >= 1 else (f"▼ {delta:.0f}pp" if delta <= -1 else "= sin cambio"))
                    delta_c = "#4ade80" if delta >= 1 else ("#ef4444" if delta <= -1 else "#6B7E6E")
                    sigs_html = "".join(
                        f'<div style="font-size:0.73rem;color:#9ab09a;padding:2px 0">{s}</div>'
                        for s in xgv["signals"]
                    ) if xgv["signals"] else '<div style="font-size:0.73rem;color:#6B7E6E">Sin señales adicionales</div>'
                    # Update pick prob display if we have real stats
                    if xgv["has_stats"]:
                        ou_pick["prob"] = adj  # mutate so pick card shows adjusted value
                    xg_html = (
                        f'<div style="margin-top:10px;padding:10px 12px;'
                        f'background:rgba(96,165,250,0.05);border:1px solid rgba(96,165,250,0.2);'
                        f'border-radius:8px">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
                        f'<span style="font-size:0.62rem;color:rgba(96,165,250,0.7);letter-spacing:2px;'
                        f'text-transform:uppercase;font-weight:600">📡 Validación xG en Vivo</span>'
                        f'<div style="display:flex;gap:8px;align-items:center">'
                        f'<span style="font-family:Cinzel,serif;font-size:1.0rem;color:{adj_c};font-weight:700">{adj:.0f}%</span>'
                        f'<span style="font-size:0.7rem;color:{delta_c};font-weight:600">{delta_str}</span>'
                        f'<span style="font-size:0.62rem;color:{conf_c};background:rgba(0,0,0,0.3);'
                        f'border-radius:10px;padding:1px 7px">confianza {conf}</span>'
                        f'</div></div>'
                        + sigs_html
                        + f'</div>'
                    )

            live_html = (
                '<div style="background:linear-gradient(135deg,#0A1E0F,#071A10);'
                f'border:2px solid {border_col};border-radius:10px;padding:0;'
                'margin:10px 0;overflow:hidden;box-shadow:0 0 30px rgba(255,60,60,0.10);">'
                '<div style="height:3px;background:linear-gradient(90deg,transparent,#ff3c3c,#ff6b6b,#ff3c3c,transparent);'
                'box-shadow:0 0 10px rgba(255,60,60,0.7)"></div>'
                '<div style="padding:14px 18px">'
                '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:10px">'
                '<div>'
                f'<span style="font-family:\'Playfair Display\',serif;font-size:1.05rem;font-weight:700;color:#fff">'
                f'{g["away_team"]} @ {g["home_team"]}</span>'
                f' <span style="color:#4ade80;font-weight:700;font-size:1.1rem;margin-left:6px">{score_str}</span>'
                f'<div style="font-size:0.72rem;color:#8a9e8a;margin-top:3px">{headline}</div>'
                '</div>'
                '<div style="display:flex;gap:5px;align-items:center;flex-wrap:wrap">'
                '<span style="background:rgba(255,60,60,0.2);color:#ff6b6b;border:1px solid rgba(255,60,60,0.4);'
                'border-radius:20px;padding:2px 9px;font-size:0.65rem;letter-spacing:1.5px;font-weight:600">🔴 EN VIVO</span>'
                f'<span style="background:rgba(201,168,76,0.1);color:#C9A84C;border:1px solid rgba(201,168,76,0.3);'
                f'border-radius:20px;padding:2px 9px;font-size:0.65rem">{league_label(g["league"])}</span>'
                + (f'<span style="background:rgba(231,76,60,0.15);color:#e74c3c;border:1px solid rgba(231,76,60,0.3);'
                   f'border-radius:20px;padding:2px 7px;font-size:0.62rem">⚠ SIN CUOTAS</span>' if dq == 0 else '')
                + '</div></div>'
                + picks_html
                + xg_html
                + stats_html
                + '</div></div>'
            )
            st.markdown(live_html, unsafe_allow_html=True)

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
def _normalize_team(name):
    """Lowercase, strip accents, remove common suffixes for fuzzy matching."""
    import unicodedata
    name = name.lower().strip()
    name = ''.join(c for c in unicodedata.normalize('NFD', name)
                   if unicodedata.category(c) != 'Mn')
    for suffix in [" fc", " cf", " sc", " ac", " bc", " afc", " utd", " united"]:
        name = name.replace(suffix, "")
    return name.strip()

def _team_match(pick_team, game_home, game_away, threshold=0.70):
    """Return ('home'|'away'|None) if pick_team matches one of the game teams."""
    pt = _normalize_team(pick_team)
    ht = _normalize_team(game_home)
    at = _normalize_team(game_away)
    # Exact substring match first
    if pt in ht or ht in pt: return "home"
    if pt in at or at in pt: return "away"
    # Token overlap
    pt_tok = set(pt.split())
    ht_tok = set(ht.split())
    at_tok = set(at.split())
    def overlap(a, b):
        if not a or not b: return 0
        return len(a & b) / max(len(a), len(b))
    h_sc = overlap(pt_tok, ht_tok)
    a_sc = overlap(pt_tok, at_tok)
    if h_sc >= threshold and h_sc > a_sc: return "home"
    if a_sc >= threshold: return "away"
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

    mercado  = (pick.get("mercado") or "ML").upper()
    pick_lbl = pick.get("pick","").strip()
    sg       = LEAGUES.get(game.get("league",""), {}).get("group","Soccer")

    # ── ML ────────────────────────────────────────────────────────────────────
    if mercado == "ML":
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

    return None

@st.cache_data(ttl=300)
def _fetch_finished_games():
    """Fetch recently finished games across all leagues for auto-resolve."""
    finished = []
    for league_name, cfg in LEAGUES.items():
        try:
            data = fetch_scoreboard(cfg["sport"], cfg["league"],
                                    tournament_id=cfg.get("tournament_id"))
            for g in parse_games(data, league_name):
                if g.get("state") == "post" and g.get("home_score") and g.get("away_score"):
                    finished.append(g)
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

def _list_reto_users():
    """List all users from Google Sheets tabs or local files."""
    if _gsheets_available():
        try:
            gc = _get_gsheet_client()
            sid = st.secrets["gsheets"]["spreadsheet_id"]
            sh = gc.open_by_key(sid)
            return sorted([ws.title for ws in sh.worksheets()])
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

with tab_reto:

    # ── Login por apodo ───────────────────────────────────────────────────────
    st.markdown('''<div style="
        text-align:center;
        font-family:'Cinzel',serif;
        font-size:1.6rem;
        font-weight:700;
        color:#C9A84C;
        letter-spacing:4px;
        padding:16px 0 4px;
        text-shadow: 0 0 20px rgba(201,168,76,0.4)
    ">💰 RETO 13 MILLONES</div>
    <div style="text-align:center;font-family:'DM Sans',sans-serif;font-size:0.8rem;
        color:#6B7E6E;letter-spacing:2px;margin-bottom:20px">
        DE $2,000 A $13,000,000 · UNA APUESTA A LA VEZ
    </div>''', unsafe_allow_html=True)

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
        st.stop()

    # ── Usuario activo ────────────────────────────────────────────────────────
    apodo_activo = st.session_state["reto_apodo"]

    col_usr1, col_usr2 = st.columns([4,1])
    with col_usr1:
        st.markdown(
            f'<div style="font-family:\'Cinzel\',serif;font-size:0.9rem;color:#C9A84C;'
            f'letter-spacing:2px;margin-bottom:12px">👤 {apodo_activo.upper()}</div>',
            unsafe_allow_html=True
        )
    with col_usr2:
        if st.button("↩ Salir", key="btn_logout_reto", use_container_width=True):
            st.session_state["reto_apodo"] = ""
            st.rerun()

    reto = _load_reto(apodo_activo)
    picks = reto.get("picks", [])
    bank_inicial = reto.get("bank_inicial", 2000.0)
    meta = reto.get("meta", 13_000_000.0)

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

    # ── KPIs ──────────────────────────────────────────────────────────────────
    n_gan = sum(1 for p in picks if p.get("resultado")=="ganado")
    n_per = sum(1 for p in picks if p.get("resultado")=="perdido")
    n_pen = sum(1 for p in picks if p.get("resultado")=="pendiente")
    win_rate = (n_gan / (n_gan + n_per) * 100) if (n_gan + n_per) > 0 else 0

    st.markdown(f'''<div class="stat-grid" style="margin-bottom:16px">
      <div class="stat-tile">
        <div class="stat-num" style="color:#C9A84C">${bank_actual:,.0f}</div>
        <div class="stat-label">Bank Actual</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num" style="color:#4ade80">{multiplicador:.1f}×</div>
        <div class="stat-label">Multiplicador</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num" style="color:#60a5fa">{len(picks)}</div>
        <div class="stat-label">Total Picks</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num" style="color:#4ade80">{win_rate:.0f}%</div>
        <div class="stat-label">Win Rate</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num" style="color:#4ade80">{n_gan}</div>
        <div class="stat-label">Ganados</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num" style="color:#ef4444">{n_per}</div>
        <div class="stat-label">Perdidos</div>
      </div>
    </div>''', unsafe_allow_html=True)

    # ── Barra de progreso hacia meta ──────────────────────────────────────────
    falta = max(meta - bank_actual, 0)
    st.markdown(f'''
    <div style="margin:8px 0 20px">
      <div style="display:flex;justify-content:space-between;
          font-family:'DM Sans',sans-serif;font-size:0.72rem;color:#6B7E6E;margin-bottom:6px">
        <span>${bank_inicial:,.0f} inicio</span>
        <span style="color:#C9A84C;font-weight:700">{progreso_pct:.4f}% completado</span>
        <span>Meta: ${meta:,.0f}</span>
      </div>
      <div style="background:#0a1a0f;border-radius:4px;height:10px;overflow:hidden;
          border:1px solid rgba(201,168,76,0.2)">
        <div style="height:100%;width:{min(progreso_pct,100):.4f}%;
            background:linear-gradient(90deg,#C9A84C,#FFE87C);
            border-radius:4px;transition:width 0.5s ease"></div>
      </div>
      <div style="text-align:center;font-family:'DM Sans',sans-serif;
          font-size:0.72rem;color:#6B7E6E;margin-top:6px">
        Faltan <b style="color:#C9A84C">${falta:,.0f}</b> para la meta
      </div>
    </div>
    ''', unsafe_allow_html=True)

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
            colors.append("#4ade80" if series_bank[i] >= series_bank[i-1] else "#ef4444")

        chart_data = _json.dumps({
            "labels": series_labels,
            "values": series_bank,
            "colors": colors,
            "bank_inicial": bank_inicial,
            "meta": meta,
        })

        st.components.v1.html(f'''
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
        <div style="background:#060C08;padding:16px;border-radius:8px;
            border:1px solid rgba(201,168,76,0.2)">
          <canvas id="retoChart" height="280"></canvas>
        </div>
        <script>
        const d = {chart_data};
        const labels = d.labels;
        const values = d.values;
        const colors = d.colors;

        // Build per-segment colors for the line
        const pointColors = ["#C9A84C", ...colors.map(c => c)];
        const pointRadius = values.map((v,i) => i === values.length-1 ? 7 : 4);

        // Gradient fill
        const ctx = document.getElementById("retoChart").getContext("2d");
        const grad = ctx.createLinearGradient(0, 0, 0, 280);
        grad.addColorStop(0, "rgba(201,168,76,0.25)");
        grad.addColorStop(1, "rgba(201,168,76,0.01)");

        // Segment colors on the line itself
        const segmentColors = colors;

        new Chart(ctx, {{
          type: "line",
          data: {{
            labels: labels,
            datasets: [{{
              label: "Bankroll",
              data: values,
              borderColor: function(ctx) {{ return "#C9A84C"; }},
              segment: {{
                borderColor: ctx => {{
                  const i = ctx.p0DataIndex;
                  return i < segmentColors.length ? segmentColors[i] : "#C9A84C";
                }}
              }},
              backgroundColor: grad,
              borderWidth: 2.5,
              pointBackgroundColor: pointColors,
              pointRadius: pointRadius,
              pointHoverRadius: 8,
              fill: true,
              tension: 0.35,
            }}]
          }},
          options: {{
            responsive: true,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                backgroundColor: "#0D2818",
                borderColor: "#C9A84C",
                borderWidth: 1,
                titleColor: "#C9A84C",
                bodyColor: "#b8c8b0",
                callbacks: {{
                  label: ctx => " $" + ctx.parsed.y.toLocaleString("es-MX", {{minimumFractionDigits:2}})
                }}
              }}
            }},
            scales: {{
              x: {{
                ticks: {{ color: "#3a4a3e", font: {{ size: 10 }}, maxRotation: 45 }},
                grid: {{ color: "rgba(255,255,255,0.03)" }}
              }},
              y: {{
                ticks: {{
                  color: "#6B7E6E",
                  font: {{ size: 10 }},
                  callback: v => "$" + v.toLocaleString("es-MX")
                }},
                grid: {{ color: "rgba(255,255,255,0.05)" }},
                beginAtZero: false
              }}
            }}
          }}
        }});
        </script>
        ''', height=320, scrolling=False)

    elif not picks:
        st.markdown('''<div class="empty-state">
          <div class="empty-icon">💰</div>
          <div class="empty-title">Sin picks aún</div>
          <div>Registra tu primer pick abajo para comenzar el reto.</div>
        </div>''', unsafe_allow_html=True)

    st.markdown('<div class="den-divider" style="margin:20px 0"></div>', unsafe_allow_html=True)

    # ── Formulario: agregar pick ──────────────────────────────────────────────
    # Gold labels for all form elements in this tab
    st.markdown("""
    <style>
    /* Gold labels for RETO 13M form */
    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] p,
    div[data-testid="stTextInput"] p,
    div[data-testid="stNumberInput"] p,
    div[data-testid="stSelectbox"] p {
        color: #C9A84C !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    /* Radio option text */
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
        color: #E0C97F !important;
        font-size: 0.88rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-heading">➕ Registrar Pick</div>', unsafe_allow_html=True)

    with st.container():
        fc1, fc2 = st.columns(2)
        with fc1:
            reto_partido  = st.text_input("Partido / Evento", placeholder="ej: Real Madrid vs Bayern",
                                          key="reto_partido")
            reto_pick     = st.text_input("Pick", placeholder="ej: Real Madrid ML / Over 2.5 / BTTS Sí",
                                          key="reto_pick")
            reto_mercado  = st.selectbox("Mercado", ["ML","O/U","BTTS","DO","Spread","Otro"],
                                         key="reto_mercado")
        with fc2:
            # Tipo de momio: americano o decimal
            reto_tipo_momio = st.radio(
                "Formato de momio",
                ["🇺🇸 Americano", "🌍 Decimal"],
                horizontal=True,
                key="reto_tipo_momio"
            )
            if reto_tipo_momio == "🇺🇸 Americano":
                reto_momio_raw = st.number_input(
                    "Momio americano", value=-110, step=5,
                    key="reto_momio_am",
                    help="Positivo: +150 | Negativo: -110"
                )
                # Convert to decimal internally for uniform storage
                if reto_momio_raw > 0:
                    reto_momio_dec = reto_momio_raw / 100 + 1
                else:
                    reto_momio_dec = 100 / abs(reto_momio_raw) + 1
                momio_display = f"+{reto_momio_raw}" if reto_momio_raw > 0 else str(reto_momio_raw)
            else:
                reto_momio_dec = st.number_input(
                    "Momio decimal", value=1.91, step=0.01,
                    min_value=1.01, format="%.2f",
                    key="reto_momio_dec",
                    help="ej: 1.91 = -110 americano | 2.50 = +150 americano"
                )
                momio_display = f"{reto_momio_dec:.2f}"

            reto_monto    = st.number_input("Monto apostado ($)", min_value=1.0,
                                            value=float(min(bank_actual * 0.05, bank_actual)) if bank_actual > 0 else 100.0,
                                            step=10.0, key="reto_monto")
            reto_resultado = st.selectbox("Resultado", ["pendiente","ganado","perdido","push"],
                                          key="reto_resultado")
        reto_nota = st.text_input("Nota (opcional)", placeholder="ej: Liga MX · Jornada 12 · pick del oráculo",
                                  key="reto_nota")

        # Calcular ganancia estimada (decimal odds: ganancia = stake * (dec - 1))
        ganancia_est = reto_monto * (reto_momio_dec - 1)
        st.caption(
            f"💵 Ganancia estimada si gana: **${ganancia_est:,.2f}** "
            f"· Momio: **{momio_display}** "
            f"· Nuevo bank si gana: **${bank_actual + ganancia_est:,.2f}**"
        )

        col_add, col_cfg = st.columns([2,1])
        with col_add:
            if st.button("✅ Agregar Pick", use_container_width=True, key="btn_add_pick"):
                if reto_partido and reto_pick:
                    nuevo = {
                        "num":       len(picks) + 1,
                        "fecha":     datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                        "partido":   reto_partido,
                        "pick":      reto_pick,
                        "mercado":   reto_mercado,
                        "momio":     round(reto_momio_dec, 4),   # always stored as decimal
                        "momio_fmt": momio_display,               # display string original
                        "monto":     reto_monto,
                        "resultado": reto_resultado,
                        "nota":      reto_nota,
                    }
                    picks.append(nuevo)
                    reto["picks"] = picks
                    if _save_reto(reto, apodo_activo):
                        st.toast(f"✅ Pick #{nuevo['num']} registrado", icon="💰")
                        st.rerun()
                    else:
                        st.error("Error guardando. Verifica permisos de escritura.")
                else:
                    st.warning("Completa Partido y Pick antes de agregar.")

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
        st.markdown('<div class="section-heading">📋 Historial de Picks</div>', unsafe_allow_html=True)

        running_bank = bank_inicial
        for p in reversed(picks):
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
                res_color = "#4ade80"
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
            nota_html = f'<div style="font-size:0.7rem;color:#3a4a3e;margin-top:2px">{p.get("nota","")}</div>' if p.get("nota") else ""

            # ── Render pick row con Streamlit nativo ──────────────────────
            with st.container():
                h_left, h_right = st.columns([3, 1])
                with h_left:
                    mercado_chip = {"ML":"🎯","O/U":"📊","BTTS":"⚽","DO":"🔄","Spread":"📐","Otro":"🎲"}.get(p.get("mercado","ML"),"🎯")
                    st.markdown(
                        f'<span style="color:#C9A84C;font-family:\'Cinzel\',serif;font-size:0.78rem">#{num}</span>'
                        f' <span style="color:#E0F7F0;font-weight:600">{p.get("partido","")}</span>'
                        f' <span style="background:rgba(201,168,76,0.15);color:#C9A84C;'
                        f'border-radius:3px;padding:1px 6px;font-size:0.7rem;margin-left:4px">'
                        f'{mercado_chip} {p.get("mercado","ML")}</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div style="font-size:0.85rem;color:#b8c8b0;margin:2px 0">▶ {p.get("pick","")}</div>',
                        unsafe_allow_html=True
                    )
                    if p.get("nota"):
                        st.caption(p["nota"])
                    st.caption(p.get("fecha",""))
                with h_right:
                    st.markdown(
                        f'<div style="text-align:right">'
                        f'<div style="font-size:1rem;font-weight:700;color:{res_color}">{res_icon} {res.upper()}</div>'
                        f'<div style="font-size:0.85rem;color:{res_color};font-weight:600">{delta_str}</div>'
                        f'<div style="font-size:0.72rem;color:#6B7E6E">${stake:,.0f} @ {momio_fmt}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.05);margin:8px 0">', unsafe_allow_html=True)

        st.markdown('<div class="den-divider" style="margin:16px 0"></div>', unsafe_allow_html=True)

        # ── AUTO-RESOLVE: detecta resultados ESPN automáticamente ──────────────
        pendientes = [p for p in picks if p.get("resultado")=="pendiente"]
        if pendientes:
            st.markdown('<div class="section-heading" style="font-size:0.9rem">⏳ Picks Pendientes</div>', unsafe_allow_html=True)

            col_auto, col_manual = st.columns([1,1])
            with col_auto:
                if st.button("🔍 Auto-Resolver con ESPN", use_container_width=True, key="btn_auto_resolve",
                             help="Busca los resultados de tus picks pendientes en ESPN automáticamente"):
                    with st.spinner("Consultando ESPN..."):
                        finished_games = _fetch_finished_games()
                    resolved = 0
                    not_found = []
                    details = []
                    for i, p in enumerate(picks):
                        if p.get("resultado") != "pendiente":
                            continue
                        # Parse partido field "Team A vs Team B" or "Team A @ Team B"
                        partido_txt = p.get("partido","")
                        sep = " vs " if " vs " in partido_txt.lower() else (" @ " if " @ " in partido_txt else None)
                        if sep:
                            parts = partido_txt.split(sep, 1)
                            t1, t2 = parts[0].strip(), parts[1].strip()
                        else:
                            t1, t2 = partido_txt.strip(), ""

                        best_match = None
                        best_result = None
                        for g in finished_games:
                            # Match either team from the pick against the game
                            m1 = _team_match(t1, g["home_team"], g["away_team"])
                            m2 = _team_match(t2, g["home_team"], g["away_team"]) if t2 else None
                            if m1 or m2:
                                res = _evaluate_pick(p, g)
                                if res:
                                    best_match = g
                                    best_result = res
                                    break

                        if best_result:
                            picks[i]["resultado"] = best_result
                            resolved += 1
                            icon = "✅" if best_result=="ganado" else ("❌" if best_result=="perdido" else "🔄")
                            details.append(f"{icon} #{p['num']} {partido_txt} → **{best_result.upper()}**")
                        else:
                            not_found.append(f"#{p['num']} {partido_txt}")

                    if resolved > 0:
                        reto["picks"] = picks
                        _save_reto(reto, apodo_activo)
                        for d in details:
                            st.markdown(d)
                        st.toast(f"✓ {resolved} pick(s) resueltos automáticamente", icon="🔍")
                        st.rerun()
                    else:
                        st.info("No se encontraron resultados aún. Los partidos pueden no haber terminado o los nombres no coinciden.")
                    if not_found:
                        with st.expander(f"⚠ {len(not_found)} sin resolver"):
                            for nf in not_found:
                                st.caption(nf)

            # ── Manual override ───────────────────────────────────────────────
            st.markdown('<div style="font-size:0.7rem;color:#6B7E6E;margin:8px 0 4px 0">✏️ Actualizar manualmente</div>', unsafe_allow_html=True)
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

st.markdown('<div class="den-divider" style="margin-top:24px"></div>',unsafe_allow_html=True)
st.markdown('<div style="text-align:center;font-family:\'Cinzel\',serif;font-size:0.6rem;color:#2a3a2e;letter-spacing:3px;padding:12px 0">THE GAMBLERS DEN · MONTE CARLO ENGINE · ⚠ SOLO FINES INFORMATIVOS</div>',unsafe_allow_html=True)

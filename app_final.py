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
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════
LEAGUES = {
    "NBA":              {"sport":"basketball","league":"nba",                    "group":"Basketball"},
    "WNBA":             {"sport":"basketball","league":"wnba",                   "group":"Basketball"},
    "NCAAB":            {"sport":"basketball","league":"mens-college-basketball","group":"Basketball"},
    "MLB":              {"sport":"baseball",  "league":"mlb",                    "group":"Baseball"},
    "NCAA Baseball":    {"sport":"baseball",  "league":"college-baseball",       "group":"Baseball"},
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
    "Liga de Expansión":      {"sport":"soccer", "league":"mex.2",               "group":"Soccer"},
    "ATP":              {"sport":"tennis",    "league":"atp",                    "group":"Tennis"},
    "WTA":              {"sport":"tennis",    "league":"wta",                    "group":"Tennis"},
    "Indian Wells ATP": {"sport":"tennis",    "league":"atp",                    "group":"Tennis", "tournament_id":"411"},
    "Indian Wells WTA": {"sport":"tennis",    "league":"wta",                    "group":"Tennis", "tournament_id":"411"},
}
HOME_BOOST = {
    "NBA":0.035,"WNBA":0.03,"NCAAB":0.05,"MLB":0.025,"NCAA Baseball":0.02,
    "NFL":0.035,"NCAAF":0.045,"NHL":0.03,"MLS":0.04,"Liga MX":0.045,
    "Premier League":0.038,"La Liga":0.04,"Bundesliga":0.042,"Serie A":0.04,
    "Ligue 1":0.04,"Champions League":0.035,"Europa League":0.035,"Conference League":0.032,"CONCACAF Champions Cup":0.04,
    "Liga de Expansión":0.05,"ATP":0.01,"WTA":0.01,
    "Indian Wells ATP":0.0,"Indian Wells WTA":0.0,
}
LEAGUE_AVG_GOALS = {
    "NBA":114.0,"WNBA":83.0,"NCAAB":72.0,"MLB":4.5,"NCAA Baseball":5.5,
    "NFL":23.0,"NCAAF":28.0,"NHL":3.1,
    "MLS":2.8,"Liga MX":2.6,"Premier League":2.7,"La Liga":2.6,
    "Bundesliga":3.1,"Serie A":2.6,"Ligue 1":2.7,
    "Champions League":2.9,"Europa League":2.7,"Conference League":2.6,"CONCACAF Champions Cup":2.7,"Liga de Expansión":2.5,
    "ATP":None,"WTA":None,
    "Indian Wells ATP":None,"Indian Wells WTA":None,
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
        {"id":"d9","league":"Indian Wells ATP","home_team":"Carlos Alcaraz","away_team":"Casper Ruud",
         "home_score":"","away_score":"","home_record":"","away_record":"",
         "state":"pre","status_detail":"R16 · Stadium 1 · 5:00 PM","date":"","venue":"BNP Paribas Open",
         "odds":{"spread":"","over_under":"","home_ml":"-280","away_ml":"+220","home_wp":"72","away_wp":"28"}},
        {"id":"d10","league":"Indian Wells ATP","home_team":"Novak Djokovic","away_team":"Jack Draper",
         "home_score":"","away_score":"","home_record":"","away_record":"",
         "state":"pre","status_detail":"R16 · Stadium 1 · 9:00 PM","date":"","venue":"BNP Paribas Open",
         "odds":{"spread":"","over_under":"","home_ml":"-145","away_ml":"+120","home_wp":"55","away_wp":"45"}},
        {"id":"d11","league":"Indian Wells WTA","home_team":"Jessica Pegula","away_team":"Belinda Bencic",
         "home_score":"5","away_score":"4","home_record":"","away_record":"",
         "state":"in","status_detail":"1er Set · En vivo","date":"","venue":"BNP Paribas Open",
         "odds":{"spread":"","over_under":"","home_ml":"-130","away_ml":"+108","home_wp":"55","away_wp":"45"}},
        {"id":"d12","league":"Indian Wells WTA","home_team":"Elena Rybakina","away_team":"Sonay Kartal",
         "home_score":"","away_score":"","home_record":"","away_record":"",
         "state":"pre","status_detail":"R16 · Stadium 2 · 7:30 PM","date":"","venue":"BNP Paribas Open",
         "odds":{"spread":"","over_under":"","home_ml":"-400","away_ml":"+300","home_wp":"78","away_wp":"22"}},
    ]

@st.cache_data(ttl=300)
def fetch_scoreboard(sport, league, tournament_id=None):
    """
    Fetch ESPN scoreboard.
    Tennis requires ?dates=YYYYMMDD to get today's matches.
    Also tries tournament-specific endpoints.
    """
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    base  = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"

    if sport == "tennis":
        urls = [
            f"{base}?dates={today}&limit=100",          # today's matches (primary)
            f"{base}?tournamentId={tournament_id}&dates={today}" if tournament_id else None,
            f"{base}?tournamentId={tournament_id}&limit=100"     if tournament_id else None,
            f"{base}?limit=100",                         # no date filter fallback
        ]
    elif tournament_id:
        urls = [
            f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/tournament/{tournament_id}/scoreboard",
            f"{base}?tournamentId={tournament_id}",
            ESPN_URL.format(sport=sport, league=league),
        ]
    else:
        urls = [ESPN_URL.format(sport=sport, league=league)]

    for url in urls:
        if not url: continue
        try:
            r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                data = r.json()
                if data.get("events") or data.get("leagues"):
                    return data
        except: continue
    return {}


def _tennis_player_name(c):
    """Extract player name from a tennis competitor block — tries all known locations."""
    for path in [
        lambda x: x.get("athlete", {}).get("displayName", ""),
        lambda x: x.get("athlete", {}).get("fullName", ""),
        lambda x: x.get("team", {}).get("displayName", ""),
        lambda x: x.get("team", {}).get("name", ""),
        lambda x: x.get("displayName", ""),
    ]:
        try:
            v = path(c)
            if v: return v
        except: pass
    return "Player"

def _parse_tennis_event(event, league_name):
    """Parse a single tennis event dict into our game format."""
    # competitions[0] or direct match block
    comp  = event.get("competitions", [event])[0]
    comps = comp.get("competitors", [])
    if len(comps) < 2:
        return None
    p1, p2 = comps[0], comps[1]
    status = event.get("status", {})
    state  = status.get("type", {}).get("state", "pre")
    detail = status.get("type", {}).get("shortDetail", "") or status.get("type", {}).get("description", "")

    # Score — tennis uses set scores, grab total sets won or current score string
    def tennis_score(c):
        sc = c.get("score", "")
        if sc: return str(sc)
        # linescores = sets
        ls = c.get("linescores", [])
        if ls: return "-".join(str(s.get("value","")) for s in ls)
        return ""

    # Odds
    odds_info = {"spread":"","over_under":"","home_ml":"","away_ml":"","home_wp":"","away_wp":""}
    for odds_src in [comp.get("odds",[]), event.get("odds",[])]:
        if odds_src:
            o = odds_src[0]
            # Try multiple field names ESPN uses for tennis moneylines
            ml1 = (o.get("homeTeamOdds",{}).get("moneyLine","") or
                   o.get("team1Odds",{}).get("moneyLine","") or
                   o.get("competitor1Odds",{}).get("moneyLine",""))
            ml2 = (o.get("awayTeamOdds",{}).get("moneyLine","") or
                   o.get("team2Odds",{}).get("moneyLine","") or
                   o.get("competitor2Odds",{}).get("moneyLine",""))
            wp1 = (o.get("homeTeamOdds",{}).get("winPercentage","") or
                   o.get("team1Odds",{}).get("winPercentage",""))
            wp2 = (o.get("awayTeamOdds",{}).get("winPercentage","") or
                   o.get("team2Odds",{}).get("winPercentage",""))
            if ml1 or ml2:
                odds_info.update({"home_ml":ml1,"away_ml":ml2,"home_wp":wp1,"away_wp":wp2})
            break

    # Tournament name as venue
    tournament = (event.get("tournament",{}).get("displayName","") or
                  event.get("league",{}).get("name","") or
                  comp.get("venue",{}).get("fullName","") or
                  league_name)

    return {
        "id":            event.get("id",""),
        "league":        league_name,
        "home_team":     _tennis_player_name(p1),
        "away_team":     _tennis_player_name(p2),
        "home_score":    tennis_score(p1),
        "away_score":    tennis_score(p2),
        "home_record":   "",
        "away_record":   "",
        "state":         state,
        "status_detail": detail,
        "date":          event.get("date",""),
        "venue":         tournament,
        "odds":          odds_info,
    }

def parse_tennis(data, league_name):
    """
    ESPN tennis JSON has several possible structures:
      A) data["events"] — flat list (standard, used during major tournaments)
      B) data["leagues"][i]["events"] — grouped by league/tour
      C) data["events"] empty but data["leagues"] has nested tournament brackets
    We try all paths and deduplicate by event id.
    """
    games = []
    seen  = set()

    def add(event):
        g = _parse_tennis_event(event, league_name)
        if g and g["id"] not in seen and g["home_team"] != "Player":
            seen.add(g["id"])
            games.append(g)

    # Path A: flat events list
    for event in data.get("events", []):
        try: add(event)
        except: pass

    # Path B: leagues → events
    for league in data.get("leagues", []):
        for event in league.get("events", []):
            try: add(event)
            except: pass

    # Path C: leagues → seasons → types → weeks → events (college/challenger)
    for league in data.get("leagues", []):
        for season in league.get("season", {}).get("types", []):
            for week in season.get("weeks", []):
                for event in week.get("events", []):
                    try: add(event)
                    except: pass

    return games

def _parse_live_stats(comp, home, away):
    """Extract live match stats from ESPN. Returns dict or None."""
    stats = {}
    def get_stat(competitor, *keys):
        s = competitor.get("statistics", {})
        if isinstance(s, list):
            for item in s:
                n = (item.get("name") or item.get("abbreviation") or "").lower()
                for k in keys:
                    if k.lower() in n:
                        try: return float(item.get("value", item.get("displayValue", 0)) or 0)
                        except: pass
        elif isinstance(s, dict):
            for k in keys:
                if k in s:
                    try: return float(s[k] or 0)
                    except: pass
        return None
    for key, hkeys in [
        ("shots",           ["shots","totalShots","Shots"]),
        ("shots_on_target", ["shotsOnTarget","onTarget","ShotsOnGoal"]),
        ("possession",      ["possession","possessionPct","Possession"]),
        ("corners",         ["corners","cornerKicks","Corners"]),
        ("attacks",         ["dangerousAttacks","attacks","Attacks"]),
        ("yellow_cards",    ["yellowCards","Yellow"]),
    ]:
        hv = get_stat(home, *hkeys)
        av = get_stat(away, *hkeys)
        if hv is not None or av is not None:
            stats[key] = {"home": hv or 0, "away": av or 0}
    return stats if stats else None


def parse_games(data, league_name):
    games = []
    for event in data.get("events",[]):
        try:
            comp=event.get("competitions",[{}])[0]; comps=comp.get("competitors",[])
            if len(comps)<2: continue
            home=next((c for c in comps if c.get("homeAway")=="home"),comps[0])
            away=next((c for c in comps if c.get("homeAway")=="away"),comps[1])
            status=event.get("status",{})
            odds_info={}
            ol=comp.get("odds",[])
            if ol:
                o=ol[0]
                odds_info={"spread":o.get("details",""),"over_under":o.get("overUnder",""),
                           "home_ml":o.get("homeTeamOdds",{}).get("moneyLine",""),
                           "away_ml":o.get("awayTeamOdds",{}).get("moneyLine",""),
                           "home_wp":o.get("homeTeamOdds",{}).get("winPercentage",""),
                           "away_wp":o.get("awayTeamOdds",{}).get("winPercentage","")}
            hr=home.get("records",[{}]); ar=away.get("records",[{}])
            live_stats = _parse_live_stats(comp, home, away)
            games.append({"id":event.get("id",""),"league":league_name,
                "home_team":home.get("team",{}).get("displayName","Home"),
                "away_team":away.get("team",{}).get("displayName","Away"),
                "home_score":home.get("score",""),"away_score":away.get("score",""),
                "home_record":hr[0].get("summary","") if hr else "",
                "away_record":ar[0].get("summary","") if ar else "",
                "state":status.get("type",{}).get("state","pre"),
                "status_detail":status.get("type",{}).get("shortDetail",""),
                "date":event.get("date",""),
                "venue":comp.get("venue",{}).get("fullName",""),
                "odds":odds_info,
                "live_stats": live_stats})
        except: continue
    return games

@st.cache_data(ttl=300)
def fetch_tsdb_tennis():
    """
    TheSportsDB fallback for tennis — no API key needed (uses public key '3').
    Returns list of normalized game dicts compatible with the rest of the app.
    Endpoint: /api/v1/json/3/eventsday.php?d=YYYY-MM-DD&s=Tennis
    Fields used: strHomeTeam, strAwayTeam, intHomeScore, intAwayScore,
                 strStatus, strTime, strLeague, idEvent
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url   = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Tennis"
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        events = r.json().get("events") or []
    except:
        return []

    games = []
    for ev in events:
        try:
            league_raw = ev.get("strLeague", "")
            # Map TSDB league names → our league names
            if "WTA" in league_raw or "Women" in league_raw.lower():
                league_name = "Indian Wells WTA" if "Indian Wells" in league_raw or "BNP" in league_raw else "WTA"
            else:
                league_name = "Indian Wells ATP" if "Indian Wells" in league_raw or "BNP" in league_raw else "ATP"

            status_raw = (ev.get("strStatus") or "").lower()
            if status_raw in ("finished", "ft", "aet", "pen"):
                state = "post"
            elif status_raw in ("live", "in progress", "1st set", "2nd set", "3rd set", "4th set", "5th set"):
                state = "in"
            else:
                state = "pre"

            hs = ev.get("intHomeScore") or ""
            as_ = ev.get("intAwayScore") or ""
            detail = ev.get("strStatus") or ev.get("strTime") or ""
            round_info = ev.get("strRound") or ev.get("intRound") or ""
            if round_info:
                detail = f"R{round_info} · {detail}" if detail else f"R{round_info}"

            games.append({
                "id":            ev.get("idEvent", ""),
                "league":        league_name,
                "home_team":     ev.get("strHomeTeam", "Player 1"),
                "away_team":     ev.get("strAwayTeam", "Player 2"),
                "home_score":    str(hs) if hs != "" else "",
                "away_score":    str(as_) if as_ != "" else "",
                "home_record":   "",
                "away_record":   "",
                "state":         state,
                "status_detail": detail,
                "date":          ev.get("dateEvent", ""),
                "venue":         ev.get("strVenue") or ev.get("strCountry") or "",
                "odds":          {},
                "live_stats":    None,
                "source":        "tsdb",
            })
        except:
            continue
    return games


SOCCER_KEYWORDS = {
    "fc", "cf", "sc", "ac", "as", "rc", "sd", "cd", "ud", "real", "atletico",
    "united", "city", "wanderers", "victory", "rovers", "athletic", "sporting",
    "dynamo", "dynamo", "olympic", "olimpia", "deportivo", "county", "rangers",
    "hotspur", "rovers", "albion", "wednesday", "palace", "villa", "forest",
    "wednesday", "county", "wanderers", "rovers", "celtic", "arsenal", "chelsea",
}

def _is_tennis_match(home, away):
    """Return True if both names look like tennis players (not soccer clubs)."""
    def looks_like_player(name):
        parts = name.lower().split()
        # Reject if any word is a known club keyword
        if any(p in SOCCER_KEYWORDS for p in parts):
            return False
        # Reject names longer than 4 words (team names tend to be long)
        if len(parts) > 4:
            return False
        return True
    return looks_like_player(home) and looks_like_player(away)


def get_all_games(leagues):
    result=[]; errors=[]
    tennis_leagues = [n for n in leagues if LEAGUES[n]["group"] == "Tennis"]
    other_leagues  = [n for n in leagues if LEAGUES[n]["group"] != "Tennis"]

    # ── Non-tennis leagues via ESPN ───────────────────────────────────────────
    for name in other_leagues:
        cfg=LEAGUES[name]
        try:
            data = fetch_scoreboard(cfg["sport"], cfg["league"], tournament_id=cfg.get("tournament_id"))
            result.extend(parse_games(data, name))
        except Exception as e: errors.append(f"{name}: {e}")

    # ── Tennis: ESPN first ────────────────────────────────────────────────────
    tennis_espn = []
    for name in tennis_leagues:
        cfg=LEAGUES[name]
        try:
            tid  = cfg.get("tournament_id")
            data = fetch_scoreboard(cfg["sport"], cfg["league"], tournament_id=tid)
            # NEVER fall back to parse_games for tennis — it would parse soccer
            parsed = parse_tennis(data, name)
            # Extra guard: filter out any non-tennis names that slipped through
            parsed = [g for g in parsed if _is_tennis_match(g["home_team"], g["away_team"])]
            tennis_espn.extend(parsed)
        except Exception as e:
            errors.append(f"{name} (ESPN): {e}")

    # ── TheSportsDB fallback — ALWAYS try if ESPN gave us nothing ─────────────
    if not tennis_espn and tennis_leagues:
        try:
            tsdb_games = fetch_tsdb_tennis()
            configured = set(tennis_leagues)
            for g in tsdb_games:
                if not _is_tennis_match(g["home_team"], g["away_team"]):
                    continue
                if g["league"] in configured:
                    tennis_espn.append(g)
                elif "ATP" in g["league"] and any("ATP" in n for n in configured):
                    g["league"] = next(n for n in configured if "ATP" in n)
                    tennis_espn.append(g)
                elif "WTA" in g["league"] and any("WTA" in n for n in configured):
                    g["league"] = next(n for n in configured if "WTA" in n)
                    tennis_espn.append(g)
            # If still nothing matched by league, accept all validated TSDB games
            if tsdb_games and not tennis_espn:
                tennis_espn = [g for g in tsdb_games if _is_tennis_match(g["home_team"], g["away_team"])]
        except Exception as e:
            errors.append(f"TheSportsDB tennis fallback: {e}")

    result.extend(tennis_espn)
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

    "Tennis": """You are a professional tennis betting analyst covering ATP and WTA tours.
You specialize in: surface matchups (clay/grass/hard court specialists), head-to-head patterns,
current form (last 10 matches), serve dominance (ace rate, 1st serve %), return game quality,
tournament round fatigue, and ranking-implied win probabilities vs market odds.
Key edge areas: H2H dominance overriding ranking, surface specialists, tired favorites deep in tournaments.
Respond in 2-3 sharp sentences. Lead with the most decisive factor (surface? H2H? form?). Be direct.""",

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
            note = f"Under 2.5 a {prob_pct:.0f}% — ambos equipos muestran bajo volumen ofensivo. Partido de menos de 3 goles favorecido por el modelo."
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

    # ── Tennis ────────────────────────────────────────────────────────────────
    elif sport_group == "Tennis":
        if spread > 40:
            note = f"{fav} domina con {fav_p:.0f}% — diferencia de ranking importante. En tenis, favoritos tan marcados suelen ganar en sets directos."
        elif spread < 10:
            note = f"Partido muy parejo ({home_pct:.0f}% / {away_pct:.0f}%). En tenis H2H y superficie son determinantes — el EV de +{ev:.1f} sugiere ineficiencia de línea."
        elif pick_is_dog:
            note = f"{dog} como underdog a {dog_p:.0f}% — upsets en tenis son comunes (30%+ de prob.). Moneyline de underdog puede tener valor real si la superficie favorece su juego."
        elif dq < 30:
            note = f"Sin momios ESPN para tenis (DQ {dq:.0f}%). Modelo basado en probabilidades estimadas. Confirma en Bet365 o Pinnacle antes de apostar."
        else:
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
    "NBA": 0.595, "WNBA": 0.570, "NCAAB": 0.620,
    "MLB": 0.540, "NCAA Baseball": 0.540,
    "NFL": 0.570, "NCAAF": 0.610,
    "NHL": 0.550,
    "MLS": 0.480, "Liga MX": 0.485,
    "Premier League": 0.460, "La Liga": 0.470, "Bundesliga": 0.465,
    "Serie A": 0.455, "Ligue 1": 0.455,
    "Champions League": 0.475, "Europa League": 0.465,
    "Conference League": 0.460, "CONCACAF Champions Cup": 0.480,
    "Liga de Expansión": 0.480,
    "ATP": 0.500, "WTA": 0.500,  # No home court in tennis
    "Indian Wells ATP": 0.500, "Indian Wells WTA": 0.500,
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
      3. Record ratio (W-L-D)             weight 2.0  — season performance
      4. League home rate prior           weight 0.6  — fallback when no data

    DQ (data quality) = how much hard evidence we have, 0-100%.
    When DQ is low, Monte Carlo uncertainty (sigma) is higher.
    """
    signals, weights = [], []
    odds   = game["odds"]
    league = game["league"]
    is_soccer = LEAGUES.get(league, {}).get("group") == "Soccer"
    is_tennis = LEAGUES.get(league, {}).get("group") == "Tennis"

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
        weights.append(1.2)

    # ── Signal 4: League historical home rate (prior / fallback) ─────────────
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

def get_lambda(game):
    """
    Estimate expected goals per team using Poisson model.
    Uses O/U line when available, otherwise falls back to league historical average.
    Home team gets slightly more share (home advantage in scoring).
    """
    league = game["league"]
    avg    = LEAGUE_AVG_GOALS.get(league)
    if avg is None: return None, None  # Tennis / non-goal sport

    ou = game["odds"].get("over_under", "")
    try:
        total = float(str(ou))
        # Sanity check — O/U line sometimes comes in weird formats
        if total <= 0 or total > 300: raise ValueError
    except:
        # No O/U line: use league historical average
        # Slight noise so identical games get different lambdas
        total = avg * 2

    base       = compute_base_prob(game)
    hp         = base["home_prob"]
    ap         = base["away_prob"]
    # Home team scores more on average (home advantage in attack)
    home_share = (hp + 0.52) / (hp + ap + 1.04)
    lam_home   = max(0.1, total * home_share)
    lam_away   = max(0.1, total * (1.0 - home_share))
    return lam_home, lam_away

def run_monte_carlo(game, n=10_000):
    base=compute_base_prob(game)
    hp,dp,dq=base["home_prob"],base["draw_prob"],base["dq"]
    is_soccer=base["is_soccer"]; sigma=(1-dq)*0.15
    lam_h,lam_a=get_lambda(game); use_goals=lam_h is not None
    hw=aw=d=btts=o15=o25=o35=dc_1x=dc_x2=dc_12=0
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
            else:
                if gh>ga: hw+=1; dc_1x+=1; dc_12+=1
                else: aw+=1; dc_x2+=1; dc_12+=1
            if gh>0 and ga>0: btts+=1
            if tg>1.5: o15+=1
            if tg>2.5: o25+=1
            if tg>3.5: o35+=1
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
    p_btts=btts/n if use_goals else None
    p_o15=o15/n if use_goals else None
    p_o25=o25/n if use_goals else None
    p_o35=o35/n if use_goals else None
    p_u25=(n-o25)/n if use_goals else None
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
    dc_1x_ev=calc_ev(p_dc_1x,DC_ML); dc_x2_ev=calc_ev(p_dc_x2,DC_ML); dc_12_ev=calc_ev(p_dc_12,DC_ML)

    candidates=[
        ("ML",game["home_team"]+" ML",sh,home_ev,hml,hk),
        ("ML",game["away_team"]+" ML",sa,away_ev,aml,ak),
    ]

    # BTTS + O/U markets — ONLY for soccer (and hockey uses total goals differently)
    # For basketball/football/baseball the O/U line is points, not goals, skip these markets
    soccer_ou_leagues = {"Soccer"}
    sport_group = LEAGUES.get(game["league"], {}).get("group", "")
    if p_btts is not None and sport_group == "Soccer":
        candidates+=[
            ("BTTS","Ambos Anotan — SÍ",p_btts,btts_ev,str(BTTS_ML),quarter_kelly(p_btts,BTTS_ML)),
            ("BTTS","Ambos Anotan — NO",1-p_btts,no_btts_ev,str(BTTS_ML),quarter_kelly(1-p_btts,BTTS_ML)),
            # O/U: Only O2.5, O3.5, Under 2.5 — O1.5 is NEVER a pick (too trivial)
            ("O/U","Over 2.5",p_o25,o25_ev,str(OU_ML),quarter_kelly(p_o25,OU_ML)),
            ("O/U","Over 3.5",p_o35,o35_ev,str(OU_ML),quarter_kelly(p_o35,OU_ML)),
            ("O/U","Under 2.5",p_u25,u25_ev,str(OU_ML),quarter_kelly(p_u25,OU_ML)),
        ]

    # DC only meaningful for soccer (3-way markets)
    if is_soccer:
        candidates+=[
            ("DC", game["home_team"]+" o Empate (1X)", p_dc_1x, dc_1x_ev, str(DC_ML), quarter_kelly(p_dc_1x,DC_ML)),
            ("DC", game["away_team"]+" o Empate (X2)", p_dc_x2, dc_x2_ev, str(DC_ML), quarter_kelly(p_dc_x2,DC_ML)),
            ("DC", game["home_team"]+" o "+game["away_team"]+" (sin empate)", p_dc_12, dc_12_ev, str(DC_ML), quarter_kelly(p_dc_12,DC_ML)),
        ]

    best_single=None; best_ev_v=-999
    for mtype,label,prob,ev,ml,kelly in candidates:
        if prob is not None and ev is not None and ev>best_ev_v:
            best_ev_v=ev; best_single={"market":mtype,"label":label,"prob":prob,"ev":ev,"ml":ml,"kelly":kelly or 0}

    pos_legs=[(mtype,label,prob,ev,ml) for mtype,label,prob,ev,ml,k in candidates
              if prob is not None and ev is not None and ev>0 and mtype not in ("DC",)]
    pos_legs.sort(key=lambda x:x[3],reverse=True)
    best_parlay=None
    if len(pos_legs)>=2:
        leg1,leg2=pos_legs[0],pos_legs[1]
        parlay_prob=leg1[2]*leg2[2]
        def ml_dec(ml):
            try:
                ml=float(str(ml).replace("+",""))
                return (ml/100+1) if ml>0 else (100/abs(ml)+1)
            except: return 1.909
        payout=(ml_dec(leg1[4])*ml_dec(leg2[4])-1)*100
        parlay_ev=round(parlay_prob*payout-(1-parlay_prob)*100,2)
        best_parlay={"legs":[leg1,leg2],"prob":parlay_prob,"ev":parlay_ev,"payout":round(payout,1)}

    return {
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
        "p_dc_1x":round(p_dc_1x*100,1),"dc_1x_ev":dc_1x_ev,
        "p_dc_x2":round(p_dc_x2*100,1),"dc_x2_ev":dc_x2_ev,
        "p_dc_12":round(p_dc_12*100,1),"dc_12_ev":dc_12_ev,
        "best_single":best_single,"best_parlay":best_parlay,
        "is_soccer":is_soccer,"n_simulations":n,"use_goals":use_goals,
    }

def run_all_simulations(games, n=10_000):
    results=[]; pb=st.progress(0); st_txt=st.empty()
    for i,game in enumerate(games):
        st_txt.markdown(
            f'<div style="font-family:\'DM Sans\',sans-serif;font-size:0.8rem;color:#6B7E6E;">'
            f'⚙ Simulando [{i+1}/{len(games)}] — {game["away_team"]} @ {game["home_team"]}</div>',
            unsafe_allow_html=True)
        results.append({**game,"sim":run_monte_carlo(game,n)})
        pb.progress((i+1)/len(games))
    pb.empty(); st_txt.empty()
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# RENDER HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def chip(market):
    cls={"ML":"chip-ml","BTTS":"chip-btts","O/U":"chip-ou","DC":"chip-dc","PARLAY":"chip-parlay"}.get(market,"chip-ml")
    return f'<span class="market-chip {cls}">{market}</span>'

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

    # Goals pills
    goals_html = ""
    if sim.get("use_goals") and sim.get("p_btts") is not None:
        pills = []
        if sim.get("btts_ev") is not None:
            c = "#4ade80" if (sim["btts_ev"] or 0) > 0 else "#6B7E6E"
            ev_s = ("+" if sim["btts_ev"] >= 0 else "") + str(round(sim["btts_ev"], 1))
            pills.append('<span style="color:' + c + ';font-size:0.75rem">BTTS ' + str(sim["p_btts"]) + '% (EV ' + ev_s + ')</span>')
        if sim.get("p_o25") is not None:
            c = "#C9A84C" if (sim.get("o25_ev") or 0) > 0 else "#6B7E6E"
            ev_s = ("+" if (sim.get("o25_ev") or 0) >= 0 else "") + str(round(sim.get("o25_ev") or 0, 1))
            pills.append('<span style="color:' + c + ';font-size:0.75rem">O2.5 ' + str(sim["p_o25"]) + '% (EV ' + ev_s + ')</span>')
        if sim.get("p_o15") is not None:
            pills.append('<span style="color:#6B7E6E;font-size:0.75rem">O1.5 ' + str(sim["p_o15"]) + '%</span>')
        if sim.get("p_o35") is not None:
            pills.append('<span style="color:#6B7E6E;font-size:0.75rem">O3.5 ' + str(sim["p_o35"]) + '%</span>')
        if pills:
            goals_html = ('<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:6px;'
                          'padding-top:6px;border-top:1px solid rgba(255,255,255,0.05)">'
                          + " &nbsp;|&nbsp; ".join(pills) + "</div>")

    dq_html   = dq_warn(dq)
    chip_html = chip(bs["market"])
    status    = r.get("status_detail", "")

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
        sport_icon = {"Basketball":"🏀","Soccer":"⚽","Football":"🏈","Tennis":"🎾","Hockey":"🏒","Baseball":"⚾"}.get(sport_group,"🎯")
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

    return (
        '<div class="pick-card">'
          '<div class="pick-header">'
            '<div>' + rank_html
              + '<span class="pick-matchup">' + r["away_team"] + ' @ ' + r["home_team"] + score_html + '</span>'
            '</div>'
            '<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">'
              + live_html
              + '<span class="pick-league-badge">' + r["league"] + '</span>'
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
            + goals_html
            + ai_html
          + '</div>'
        '</div>'
    )


def render_parlay_card(r):
    sim=r["sim"]; bp=sim["best_parlay"]
    if not bp or bp["ev"]<=0: return ""
    conf=conf_badge(bp["ev"],sim["data_quality"])
    legs_html=""
    for i,leg in enumerate(bp["legs"]):
        legs_html+=(
            '<div class="parlay-leg">'
            + chip(leg[0])
            + '<span style="font-family:\'Cinzel\',sans-serif;font-size:0.95rem;color:#E0F7F0;margin-left:8px">' + leg[1] + '</span>'
            + '<span style="color:#2EE8C0;margin-left:auto;font-family:\'Cinzel\',serif;font-weight:700">' + str(round(leg[2]*100,1)) + '%</span>'
            + '</div>'
        )
        if i<len(bp["legs"])-1:
            legs_html+='<div class="parlay-connector" style="color:#1ABC9C;font-size:0.75rem;text-align:center;padding:4px 0;letter-spacing:3px">⊕ COMBINADA ⊕</div>'

    dq_warn_html = ('<div class="warn-banner" style="margin-top:8px">'
                    '⚠ DQ 0% — Sin cuotas reales. Verifica precios antes de apostar.</div>'
                    if sim["data_quality"]==0 else "")
    return (
        '<div class="parlay-card">'
          '<div class="parlay-header">'
            '🎰 &nbsp;PARLAY &nbsp;·&nbsp; ' + r["away_team"] + ' @ ' + r["home_team"] + ' &nbsp;·&nbsp; ' + r["league"]
          + '</div>'
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
    sel_groups=st.multiselect("Grupos",groups,default=["Basketball","Baseball","Soccer"],
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

        # Specific message if only tennis was selected
        only_tennis = all(LEAGUES.get(l,{}).get("group")=="Tennis" for l in sel_leagues)
        if only_tennis:
            st.markdown("""<div class="warn-banner">
            🎾 <b>ATP / WTA — Sin partidos disponibles.</b><br>
            ESPN solo publica partidos de tenis durante semanas de torneo activo (ej: Indian Wells, Miami Open, Roland Garros).
            Fuera de esas semanas el scoreboard aparece vacío.<br>
            <b>Solución:</b> Agrega otras ligas (NBA, Soccer) o activa Modo Demo para ver cómo funciona la app.
            </div>""", unsafe_allow_html=True)
        else:
            leagues_str = ", ".join(sel_leagues[:6])
            st.markdown(f'<div class="warn-banner">ESPN no retornó partidos para: <b>{leagues_str}</b>.<br>Puede que no haya juegos programados hoy o que la API esté temporalmente caída. Usa el modo demo o selecciona otras ligas.</div>',unsafe_allow_html=True)
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

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_picks, tab_sim, tab_parlays, tab_all = st.tabs([
    "🃏  RONGOL PICKS",
    f"🔮  ORÁCULO  ({n_sims:,}×)",
    "🎰  PARLAYS",
    "📋  PARTIDOS",
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
        all_bets=[]
        for r in sr:
            bs=r["sim"].get("best_single")
            if bs and bs["ev"]>0: all_bets.append(r)
        all_bets.sort(key=lambda x: x["sim"]["best_single"]["ev"],reverse=True)

        if not all_bets:
            st.markdown('<div class="warn-banner">No se encontraron apuestas con EV positivo hoy. Intenta con más ligas o espera actualización de cuotas.</div>',unsafe_allow_html=True)
        else:
            # TOP PICK
            st.markdown('<div class="section-heading">💎 PICK DIAMANTE</div>', unsafe_allow_html=True)
            st.markdown(render_pick_card(all_bets[0]), unsafe_allow_html=True)

            # REST
            if len(all_bets)>1:
                st.markdown(f'<div class="section-heading">🔥 PICKS FUEGO ({len(all_bets)-1})</div>', unsafe_allow_html=True)
                for i,r in enumerate(all_bets[1:7],2):
                    st.markdown(render_pick_card(r,rank=i), unsafe_allow_html=True)

        # Avoid
        avoid=[r for r in sr if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]<-15]
        avoid.sort(key=lambda x:x["sim"]["best_single"]["ev"])
        if avoid:
            st.markdown('<div class="section-heading">♦ Evitar</div>', unsafe_allow_html=True)
            for r in avoid[:3]:
                bs=r["sim"]["best_single"]
                st.markdown(f'<div class="game-row"><span class="game-title" style="color:#ef4444">✗ {r["away_team"]} @ {r["home_team"]}</span><span class="game-meta">{r["league"]} · EV {bs["ev"]:.1f} · {bs["label"]}</span></div>',unsafe_allow_html=True)

        st.markdown('<div class="den-divider" style="margin:16px 0"></div>',unsafe_allow_html=True)
        today=datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")
        total_sims=len(sr)*sr[0]["sim"]["n_simulations"]
        st.markdown(f'<div style="text-align:center;font-family:\'DM Sans\',sans-serif;font-size:0.72rem;color:#3a4a3e">📅 {today} · {total_sims:,} simulaciones · {"DEMO" if is_demo else "ESPN Live"}</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
with tab_sim:
    st.markdown(f'<div class="section-heading">🔮 Oráculo Monte Carlo — {len(games)} partidos × {n_sims:,}</div>',unsafe_allow_html=True)
    if is_demo:
        st.markdown('<div class="demo-banner">Modo demo activo.</div>',unsafe_allow_html=True)

    col_re1, col_re2 = st.columns([2,1])
    with col_re1:
        if st.button(f"🔄  RE-SIMULAR  ({n_sims:,}×)", use_container_width=True):
            t0=time.time()
            sr2=run_all_simulations(games,n=n_sims)
            elapsed=time.time()-t0
            st.session_state["sim_results"]=sr2
            st.session_state["last_sim_demo"]=is_demo
            st.session_state["_sim_key"]=""  # force re-sim
            n_pos=len([r for r in sr2 if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0])
            st.success(f"✓ {len(games)*n_sims:,} sims en {elapsed:.1f}s · {n_pos} value bets")
            st.rerun()

    sr=st.session_state.get("sim_results",[])
    if sr:
        sort_by=st.selectbox("Ordenar por",["Mejor EV","Mayor prob. local","Mayor prob. visitante","Calidad dato"],label_visibility="collapsed")
        def sk(r):
            s=r["sim"]; bs=s.get("best_single")
            if "EV" in sort_by: return bs["ev"] if bs else -999
            if "local" in sort_by: return s["home_pct"]
            if "visitante" in sort_by: return s["away_pct"]
            return s["data_quality"]
        sorted_r=sorted(sr,key=sk,reverse=True)
        ev_only=st.checkbox("Solo EV positivo",value=False)
        display=[r for r in sorted_r if not ev_only or (r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0)]

        for r in display:
            sim=r["sim"]; bs=sim.get("best_single"); dq=sim["data_quality"]
            has_ev=bs and bs["ev"]>0
            card_cls="game-row game-row-ev" if has_ev else "game-row"
            if has_ev:
                ev_c = "#4ade80" if bs["ev"]>=10 else "#C9A84C"
                badge = (f'<span style="color:#FFE87C;margin-right:4px">&#9658;</span>'
                         f'<span style="font-weight:700;font-size:0.85rem;color:#FFE87C">{bs["label"]}</span>'
                         f'<span style="color:{ev_c};font-size:0.78rem;margin-left:8px">EV +{bs["ev"]:.1f}</span>'
                         f'<span style="color:#6B7E6E;font-size:0.72rem;margin-left:6px">· {round(bs["prob"]*100,1)}% prob · Kelly {round(bs.get("kelly",0)*100,1)}%</span>')
            else:
                badge = '<span style="color:#6B7E6E;font-size:0.78rem">Sin EV positivo</span>'
            dqc="#4ade80" if dq>=70 else "#C9A84C" if dq>=40 else "#ef4444"

            bars_html=bar(sim["away_pct"],"#60a5fa",r["away_team"])
            if sim["is_soccer"]: bars_html+=bar(sim["draw_pct"],"#a78bfa","Empate")
            bars_html+=bar(sim["home_pct"],"#f97316",r["home_team"])

            goals_line=""
            if sim["use_goals"] and sim.get("p_btts") is not None:
                btc="#4ade80" if (sim.get("btts_ev") or 0)>0 else "#6B7E6E"
                o2c="#C9A84C" if (sim.get("o25_ev") or 0)>0 else "#6B7E6E"
                o3c="#C9A84C" if (sim.get("o35_ev") or 0)>0 else "#6B7E6E"
                dq_src = "ML+Récords" if dq>=50 else ("Récords" if dq>=25 else ("Prior" if dq>0 else "Sin datos"))
                goals_line=f'<div style="font-size:0.72rem;margin-top:5px;display:flex;gap:12px;flex-wrap:wrap"><span style="color:{btc}">⚽ BTTS {sim["p_btts"]}%</span><span style="color:{o2c}">📊 O2.5 {sim["p_o25"]}%</span><span style="color:{o3c}">O3.5 {sim.get("p_o35","—")}%</span><span style="color:#3a4a3e;margin-left:auto">fuente: {dq_src}</span></div>'

            st.markdown(f"""<div class="{card_cls}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px">
                <div>
                  <div class="game-title">{r['away_team']} @ {r['home_team']}</div>
                  <div class="game-meta">{r['league']} · {r['status_detail']} · <span style="color:{dqc}">DQ {dq:.0f}%</span></div>
                  <div style="margin-top:4px">{badge}</div>
                </div>
                <div style="text-align:right;font-size:0.72rem;color:#6B7E6E">
                  ML {sim['away_ml'] or '—'} / {sim['home_ml'] or '—'}
                </div>
              </div>
              <div style="margin-top:8px">{bars_html}</div>
              {goals_line}
            </div>""",unsafe_allow_html=True)

        st.markdown('<div class="den-divider" style="margin:16px 0"></div>',unsafe_allow_html=True)
        csv=["Liga,Visitante,Local,Prob Vis%,Prob Local%,Empate%,ML Vis,ML Local,EV Vis,EV Local,BTTS%,EV BTTS,O2.5%,EV O2.5,O3.5%,DC 1X%,DC X2%,Mejor Mercado,Mejor Pick,Mejor EV,DQ%"]
        for r in sorted_r:
            s=r["sim"]; bs=s.get("best_single",{}) or {}
            csv.append(",".join([r['league'],r['away_team'],r['home_team'],
                str(s['away_pct']),str(s['home_pct']),str(s['draw_pct']),
                str(s['away_ml']),str(s['home_ml']),
                str(s['away_ev'] or ""),str(s['home_ev'] or ""),
                str(s['p_btts'] or ""),str(s['btts_ev'] or ""),
                str(s['p_o25'] or ""),str(s['o25_ev'] or ""),str(s['p_o35'] or ""),
                str(s['p_dc_1x']),str(s['p_dc_x2']),
                bs.get('market',""),bs.get('label',""),str(bs.get('ev',"")),str(s['data_quality'])]))
        st.download_button("⬇  Descargar CSV",data="\n".join(csv),
                           file_name=f"gamblers_den_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",mime="text/csv")
    else:
        st.markdown("""<div class="empty-state">
          <div class="empty-icon">♠</div>
          <div class="empty-title">Listo para simular</div>
          <div>Presiona el botón para correr las simulaciones Monte Carlo.</div>
        </div>""",unsafe_allow_html=True)

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
            st.markdown(f'<div class="section-heading">🎰 Parlays del día</div>', unsafe_allow_html=True)
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

        if parlays:
            # Indicador de estado de partidos
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
            for r in parlays:
                st.markdown(render_parlay_card(r), unsafe_allow_html=True)
            st.markdown(
                '<div class="warn-banner">⚠ Cuotas de BTTS/O/U asumidas a −110/−115 estándar. ' +
                'Verifica precio real en tu casa. Parlays son de alta varianza — usa sizing conservador.</div>',
                unsafe_allow_html=True
            )
        elif pending_games:
            st.markdown('<div class="warn-banner">No se encontraron parlays con EV positivo. Prueba con más ligas o espera más partidos.</div>',unsafe_allow_html=True)
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
                picks.append({"label": f"{dom_team} gana o empata (DC)", "prob": round(dc_prob, 1), "market": "DC",
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
        elif sport_group == "Tennis":
            rationale = f"{team} lidera en sets/games. Modelo estima {prob:.0f}% de ganar el match."
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
                f'border-radius:20px;padding:2px 9px;font-size:0.65rem">{g["league"]}</span>'
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

    # ── ALL GAMES LIST ─────────────────────────────────────────────────────────
    cf1,cf2=st.columns(2)
    with cf1: fs=st.multiselect("Estado",["pre","in","post"],default=["pre","in"],
                                format_func=lambda x:{"pre":"Próximo","in":"En Vivo","post":"Final"}[x])
    with cf2: fl=st.multiselect("Liga",list(set(g["league"] for g in games)),
                                default=list(set(g["league"] for g in games)))
    filtered=[g for g in games if g["state"] in fs and g["league"] in fl]
    st.caption(f"{len(filtered)} de {len(games)} partidos {'· DEMO' if is_demo else ''}")

    for g in filtered:
        si={"in":"🔴","pre":"◉","post":"○"}.get(g["state"],"")
        live_cls="color:#4ade80;" if g["state"]=="in" else "color:#6B7E6E;"
        oh=""
        if g["odds"]:
            o=g["odds"]; parts=[]
            if o.get("spread"): parts.append(f"Spread: {o['spread']}")
            if o.get("over_under"): parts.append(f"O/U {o['over_under']}")
            if o.get("home_ml"): parts.append(f"ML {o['home_ml']}/{o.get('away_ml','')}")
            if parts: oh=f'<div style="color:#C9A84C;font-size:0.72rem;margin-top:2px">{" · ".join(parts)}</div>'
        sh=f' <span style="color:#4ade80">{g["away_score"]}–{g["home_score"]}</span>' if g["state"]=="in" and g.get("home_score") else ""
        rh=f'<span style="color:#3a4a3e"> · {g.get("away_record","?")} vs {g.get("home_record","?")}</span>' if (g.get("away_record") or g.get("home_record")) else ""
        st.markdown(f"""<div class="game-row">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div class="game-title">{g['away_team']} @ {g['home_team']}{sh}</div>
            <span style="{live_cls}font-size:0.8rem">{si} {g['status_detail']}</span>
          </div>
          <div class="game-meta">{g['league']}{rh}</div>
          {oh}
        </div>""",unsafe_allow_html=True)

st.markdown('<div class="den-divider" style="margin-top:24px"></div>',unsafe_allow_html=True)
st.markdown('<div style="text-align:center;font-family:\'Cinzel\',serif;font-size:0.6rem;color:#2a3a2e;letter-spacing:3px;padding:12px 0">THE GAMBLERS DEN · MONTE CARLO ENGINE · ⚠ SOLO FINES INFORMATIVOS</div>',unsafe_allow_html=True)

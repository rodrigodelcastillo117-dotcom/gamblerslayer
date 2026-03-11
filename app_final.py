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
  background: linear-gradient(145deg, #0A1E0F 0%, #071610 50%, #0D2010 100%);
  border: 1px solid var(--gold);
  border-radius: 8px;
  padding: 0;
  margin: 12px 0;
  overflow: hidden;
  box-shadow: 0 0 60px rgba(201,168,76,0.08), inset 0 1px 0 rgba(201,168,76,0.15);
  position: relative;
}
.pick-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold), var(--gold2), var(--gold), transparent);
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
  font-size: 1.6rem;
  font-weight: 900;
  color: var(--gold2);
  text-shadow: 0 0 20px rgba(240,208,128,0.4);
  letter-spacing: 2px;
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.pick-action-arrow {
  color: var(--gold);
  font-size: 1.8rem;
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
  background: linear-gradient(145deg, #071510 0%, #0A1E18 100%);
  border: 1px solid rgba(26,188,156,0.5);
  border-radius: 8px;
  padding: 0;
  margin: 10px 0;
  overflow: hidden;
  box-shadow: 0 0 30px rgba(26,188,156,0.06);
}
.parlay-header {
  background: rgba(26,188,156,0.08);
  border-bottom: 1px solid rgba(26,188,156,0.2);
  padding: 10px 16px;
  font-family: 'Cinzel', serif;
  font-size: 0.85rem;
  color: #1ABC9C;
  letter-spacing: 2px;
  text-transform: uppercase;
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
    "Champions League": {"sport":"soccer",    "league":"UEFA.CHAMPIONS",         "group":"Soccer"},
    "Europa League":    {"sport":"soccer",    "league":"UEFA.EUROPA",            "group":"Soccer"},
    "Liga de Expansión":{"sport":"soccer",    "league":"mex.2",                  "group":"Soccer"},
    "ATP":              {"sport":"tennis",    "league":"atp",                    "group":"Tennis"},
    "WTA":              {"sport":"tennis",    "league":"wta",                    "group":"Tennis"},
}
HOME_BOOST = {
    "NBA":0.035,"WNBA":0.03,"NCAAB":0.05,"MLB":0.025,"NCAA Baseball":0.02,
    "NFL":0.035,"NCAAF":0.045,"NHL":0.03,"MLS":0.04,"Liga MX":0.045,
    "Premier League":0.038,"La Liga":0.04,"Bundesliga":0.042,"Serie A":0.04,
    "Ligue 1":0.04,"Champions League":0.035,"Europa League":0.035,
    "Liga de Expansión":0.05,"ATP":0.01,"WTA":0.01,
}
LEAGUE_AVG_GOALS = {
    "NBA":114.0,"WNBA":83.0,"NCAAB":72.0,"MLB":4.5,"NCAA Baseball":5.5,
    "NFL":23.0,"NCAAF":28.0,"NHL":3.1,
    "MLS":2.8,"Liga MX":2.6,"Premier League":2.7,"La Liga":2.6,
    "Bundesliga":3.1,"Serie A":2.6,"Ligue 1":2.7,
    "Champions League":2.9,"Europa League":2.7,"Liga de Expansión":2.5,
    "ATP":None,"WTA":None,
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

@st.cache_data(ttl=300)
def fetch_scoreboard(sport, league):
    try:
        r = requests.get(ESPN_URL.format(sport=sport,league=league), timeout=8,
                         headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200: return r.json()
    except: pass
    return {}

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
                "odds":odds_info})
        except: continue
    return games

def get_all_games(leagues):
    result=[]; errors=[]
    for name in leagues:
        cfg=LEAGUES[name]
        try:
            data=fetch_scoreboard(cfg["sport"],cfg["league"])
            result.extend(parse_games(data,name))
        except Exception as e: errors.append(f"{name}: {e}")
    return result, errors

# ═══════════════════════════════════════════════════════════════════════════════
# MATH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
def ml_to_prob(ml):
    try:
        ml=float(str(ml).replace("+",""))
        return 100/(ml+100) if ml>0 else abs(ml)/(abs(ml)+100)
    except: return 0.5

def win_pct(rec):
    try:
        p=rec.strip().split("-"); w,l=int(p[0]),int(p[1])
        return w/(w+l) if (w+l)>=5 else None
    except: return None

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
    signals,weights=[],[]
    odds=game["odds"]; league=game["league"]
    is_soccer=LEAGUES.get(league,{}).get("group")=="Soccer"
    hwp=odds.get("home_wp",""); awp=odds.get("away_wp","")
    if hwp and awp:
        try:
            hw=float(str(hwp).replace("%",""))/100; aw=float(str(awp).replace("%",""))/100
            if 0<hw<1 and 0<aw<1: signals.append(hw/(hw+aw)); weights.append(3.0)
        except: pass
    hml=odds.get("home_ml",""); aml=odds.get("away_ml","")
    if hml and aml:
        hp=ml_to_prob(hml); ap=ml_to_prob(aml); vig=hp+ap
        if 1.0<vig<1.25: signals.append(hp/vig); weights.append(4.0)
    hrec=win_pct(game.get("home_record","")); arec=win_pct(game.get("away_record",""))
    if hrec is not None and arec is not None:
        t=hrec+arec
        if t>0: signals.append(hrec/t); weights.append(1.5)
    elif hrec is not None: signals.append(hrec); weights.append(0.8)
    elif arec is not None: signals.append(1-arec); weights.append(0.8)
    home_p=sum(s*w for s,w in zip(signals,weights))/sum(weights) if signals else 0.5
    home_p=min(0.95,max(0.05,home_p+HOME_BOOST.get(league,0.03)))
    dq=min(1.0,sum(weights)/8.0)
    if is_soccer:
        bd=max(0.10,min(0.35,0.28-abs(home_p-0.5)*0.3)); rem=1-bd
        return {"home_prob":home_p*rem,"away_prob":(1-home_p)*rem,"draw_prob":bd,"dq":dq,"is_soccer":True}
    return {"home_prob":home_p,"away_prob":1-home_p,"draw_prob":0.0,"dq":dq,"is_soccer":False}

def get_lambda(game):
    league=game["league"]; avg=LEAGUE_AVG_GOALS.get(league)
    if avg is None: return None,None
    ou=game["odds"].get("over_under","")
    try: total=float(str(ou))
    except: total=avg*2
    base=compute_base_prob(game); hp=base["home_prob"]; ap=base["away_prob"]
    home_share=(hp+0.52)/(hp+ap+1.04)
    return total*home_share, total*(1-home_share)

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
    if p_btts is not None:
        candidates+=[
            ("BTTS","Ambos Anotan — SÍ",p_btts,btts_ev,str(BTTS_ML),quarter_kelly(p_btts,BTTS_ML)),
            ("BTTS","Ambos Anotan — NO",1-p_btts,no_btts_ev,str(BTTS_ML),quarter_kelly(1-p_btts,BTTS_ML)),
            ("O/U","Over 1.5",p_o15,o15_ev,str(OU_ML),quarter_kelly(p_o15,OU_ML)),
            ("O/U","Over 2.5",p_o25,o25_ev,str(OU_ML),quarter_kelly(p_o25,OU_ML)),
            ("O/U","Over 3.5",p_o35,o35_ev,str(OU_ML),quarter_kelly(p_o35,OU_ML)),
            ("O/U","Under 2.5",p_u25,u25_ev,str(OU_ML),quarter_kelly(p_u25,OU_ML)),
        ]
    candidates+=[
        ("DC","Doble Oportunidad 1X",p_dc_1x,dc_1x_ev,str(DC_ML),quarter_kelly(p_dc_1x,DC_ML)),
        ("DC","Doble Oportunidad X2",p_dc_x2,dc_x2_ev,str(DC_ML),quarter_kelly(p_dc_x2,DC_ML)),
        ("DC","Doble Oportunidad 12",p_dc_12,dc_12_ev,str(DC_ML),quarter_kelly(p_dc_12,DC_ML)),
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
    if dq==0: return '<span class="market-chip chip-warn">⚠ SIN CUOTAS</span>'
    if dq<40: return '<span class="market-chip chip-warn">⚠ DATA BAJA</span>'
    return ""

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
    """Render a full premium pick card with explicit bet label."""
    sim=r["sim"]; bs=sim["best_single"]; dq=sim["data_quality"]
    if not bs: return ""

    impl=ml_to_prob(bs["ml"])*100 if bs["market"]=="ML" and bs["ml"] else 0
    eg=edge(bs["prob"],bs["ml"]) if bs["market"]=="ML" else 0
    is_live = r.get("state","")=="in"
    live_html='<span class="market-chip chip-btts" style="animation:none">🔴 EN VIVO</span>' if is_live else ""
    rank_html=f'<span style="font-family:\'Cinzel\',serif;color:#6B7E6E;font-size:0.8rem">#{rank}</span> ' if rank else ""

    # Score display
    score_html=""
    if is_live and r.get("home_score") and r.get("away_score"):
        score_html=f' <span style="color:#4ade80;font-weight:700">{r["away_score"]} – {r["home_score"]}</span>'

    # Goals market pills
    goals_html=""
    if sim["use_goals"] and sim.get("p_btts") is not None:
        pills=[]
        if sim.get("btts_ev") is not None:
            c="#4ade80" if (sim["btts_ev"] or 0)>0 else "#6B7E6E"
            pills.append(f'<span style="color:{c};font-size:0.75rem">⚽ BTTS {sim["p_btts"]}% (EV {sim["btts_ev"]:+.1f})</span>')
        if sim.get("p_o25") is not None:
            c="#C9A84C" if (sim["o25_ev"] or 0)>0 else "#6B7E6E"
            pills.append(f'<span style="color:{c};font-size:0.75rem">📊 O2.5 {sim["p_o25"]}% (EV {sim["o25_ev"]:+.1f})</span>')
        if sim.get("p_o15") is not None:
            pills.append(f'<span style="color:#6B7E6E;font-size:0.75rem">📊 O1.5 {sim["p_o15"]}%</span>')
        if sim.get("p_o35") is not None:
            pills.append(f'<span style="color:#6B7E6E;font-size:0.75rem">📊 O3.5 {sim["p_o35"]}%</span>')
        if pills:
            goals_html='<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:6px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.05)">'+"".join(pills)+"</div>"

    return f"""<div class="pick-card">
      <div class="pick-header">
        <div>
          {rank_html}<span class="pick-matchup">{r['away_team']} @ {r['home_team']}{score_html}</span>
        </div>
        <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">
          {live_html}
          <span class="pick-league-badge">{r['league']}</span>
          {dq_warn(dq)}
        </div>
      </div>
      <div class="pick-body">
        <div style="margin-bottom:4px">{chip(bs['market'])}<span style="color:#6B7E6E;font-size:0.72rem;margin-left:6px">{r.get('status_detail','')}</span></div>
        <div class="pick-action">
          <span class="pick-action-arrow">▶</span>
          <span>{bs['label']}</span>
          {"<span style='font-size:1rem;color:#6B7E6E'>@ "+bs['ml']+"</span>" if bs['ml'] else ""}
        </div>
        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-item-val val-green">{bs['prob']*100:.1f}%</div>
            <div class="stat-item-lbl">Prob. Sim.</div>
          </div>
          {"<div class='stat-item'><div class='stat-item-val val-muted'>"+str(round(impl,1))+"%</div><div class='stat-item-lbl'>Impl. Casa</div></div>" if impl>0 else ""}
          {"<div class='stat-item'><div class='stat-item-val val-blue'>+"+str(eg)+"%</div><div class='stat-item-lbl'>Edge</div></div>" if eg>0 else ""}
          <div class="stat-item">
            <div class="stat-item-val val-gold">+{bs['ev']:.1f}</div>
            <div class="stat-item-lbl">EV / $100</div>
          </div>
          <div class="stat-item">
            <div class="stat-item-val val-purple">{bs['kelly']:.1%}</div>
            <div class="stat-item-lbl">Kelly 25%</div>
          </div>
          <div class="stat-item">
            <div class="stat-item-val" style="font-size:0.9rem">{conf_badge(bs['ev'],dq)}</div>
            <div class="stat-item-lbl">Confianza</div>
          </div>
        </div>
        {goals_html}
      </div>
    </div>"""

def render_parlay_card(r):
    sim=r["sim"]; bp=sim["best_parlay"]
    if not bp or bp["ev"]<=0: return ""
    conf=conf_badge(bp["ev"],sim["data_quality"])
    legs_html=""
    for i,leg in enumerate(bp["legs"]):
        legs_html+=f'<div class="parlay-leg">{chip(leg[0])}<span>{leg[1]}</span><span style="color:#4ade80;margin-left:auto">{leg[2]*100:.1f}%</span></div>'
        if i<len(bp["legs"])-1:
            legs_html+='<div class="parlay-connector">+ COMBINADA +</div>'
    return f"""<div class="parlay-card">
      <div class="parlay-header">🎰 PARLAY — {r['away_team']} @ {r['home_team']} · {r['league']}</div>
      <div class="parlay-body">
        {legs_html}
        <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:12px;padding-top:10px;border-top:1px solid rgba(26,188,156,0.15)">
          <div class="stat-item"><div class="stat-item-val val-green">{bp['prob']*100:.1f}%</div><div class="stat-item-lbl">Prob. Combo</div></div>
          <div class="stat-item"><div class="stat-item-val val-cyan">+{bp['payout']:.0f}</div><div class="stat-item-lbl">Pago / $100</div></div>
          <div class="stat-item"><div class="stat-item-val val-gold">+{bp['ev']:.1f}</div><div class="stat-item-lbl">EV / $100</div></div>
          <div class="stat-item">{conf}</div>
        </div>
        {"<div class='warn-banner' style='margin-top:8px'>⚠ DQ 0% — Sin cuotas reales. Verifica precios en tu casa antes de apostar.</div>" if sim["data_quality"]==0 else ""}
      </div>
    </div>"""

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-logo">THE DEN</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Gamblers · Analytics · Edge</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("**SIMULACIÓN**")
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
        st.markdown('<div class="warn-banner">ESPN no retornó partidos. Puede que no haya juegos programados hoy o que la API esté caída. Usa el modo demo para probar la app.</div>',unsafe_allow_html=True)
        st.stop()
    else:
        sel_set=set(sel_leagues)
        games=[g for g in games if g["league"] in sel_set] or games

if st.session_state.get("force_demo"):
    games=get_demo_games(); is_demo=True; st.session_state.pop("force_demo",None)

if is_demo:
    st.markdown('<div class="demo-banner">⚠ MODO DEMO — Datos ilustrativos. Desactiva el toggle en el sidebar para datos reales de ESPN.</div>',unsafe_allow_html=True)

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
    "🎯  PICKS DEL DÍA",
    f"🎲  SIMULACIONES  ({n_sims:,}×)",
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
          <div>Ve al tab <b>SIMULACIONES</b> y presiona el botón para generar los picks del día.</div>
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
            st.markdown('<div class="section-heading">♠ Pick Principal</div>', unsafe_allow_html=True)
            st.markdown(render_pick_card(all_bets[0]), unsafe_allow_html=True)

            # REST
            if len(all_bets)>1:
                st.markdown(f'<div class="section-heading">♣ Value Bets ({len(all_bets)-1})</div>', unsafe_allow_html=True)
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
    st.markdown(f'<div class="section-heading">🎲 Motor Monte Carlo — {len(games)} partidos × {n_sims:,}</div>',unsafe_allow_html=True)
    if is_demo:
        st.markdown('<div class="demo-banner">Modo demo activo.</div>',unsafe_allow_html=True)

    if st.button(f"▶  CORRER  {n_sims:,}  SIMULACIONES"):
        t0=time.time()
        sr2=run_all_simulations(games,n=n_sims)
        elapsed=time.time()-t0
        st.session_state["sim_results"]=sr2
        st.session_state["last_sim_demo"]=is_demo
        n_pos=len([r for r in sr2 if r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0])
        st.success(f"✓ {len(games)*n_sims:,} simulaciones en {elapsed:.1f}s · {n_pos} value bets encontradas")
        st.balloons()
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
            badge=f'{chip(bs["market"])} <span style="color:#4ade80;font-weight:600;font-size:0.8rem">EV +{bs["ev"]:.1f} · {bs["label"]}</span>' if has_ev else '<span style="color:#6B7E6E;font-size:0.78rem">Sin EV positivo</span>'
            dqc="#4ade80" if dq>=70 else "#C9A84C" if dq>=40 else "#ef4444"

            bars_html=bar(sim["away_pct"],"#60a5fa",r["away_team"])
            if sim["is_soccer"]: bars_html+=bar(sim["draw_pct"],"#a78bfa","Empate")
            bars_html+=bar(sim["home_pct"],"#f97316",r["home_team"])

            goals_line=""
            if sim["use_goals"] and sim.get("p_btts") is not None:
                btc="#4ade80" if (sim.get("btts_ev") or 0)>0 else "#6B7E6E"
                o2c="#C9A84C" if (sim.get("o25_ev") or 0)>0 else "#6B7E6E"
                goals_line=f'<div style="font-size:0.72rem;margin-top:5px;display:flex;gap:12px;flex-wrap:wrap"><span style="color:{btc}">⚽ BTTS {sim["p_btts"]}%</span><span style="color:{o2c}">📊 O2.5 {sim["p_o25"]}%</span><span style="color:#6B7E6E">O1.5 {sim["p_o15"]}%</span><span style="color:#6B7E6E">O3.5 {sim["p_o35"]}%</span></div>'

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
          <div>Corre las simulaciones primero.</div>
        </div>""",unsafe_allow_html=True)
    else:
        parlays=[r for r in sr if r["sim"].get("best_parlay") and r["sim"]["best_parlay"]["ev"]>0]
        parlays.sort(key=lambda x:x["sim"]["best_parlay"]["ev"],reverse=True)
        if parlays:
            st.markdown(f'<div class="section-heading">🎰 Combinadas con EV+ ({len(parlays)})</div>',unsafe_allow_html=True)
            for r in parlays:
                st.markdown(render_parlay_card(r),unsafe_allow_html=True)
            st.markdown('<div class="warn-banner">⚠ Cuotas de BTTS/O/U asumidas a −110/−115 estándar. Verifica precio real en tu casa. Parlays son de alta varianza — usa sizing conservador.</div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="warn-banner">No se encontraron parlays con EV positivo en los partidos disponibles.</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
with tab_all:
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

"""
ESPN+ Pick Analyzer — Monte Carlo con Mercados Extendidos
BTTS · O/U 1.5/2.5/3.5 · Doble Oportunidad · Parlays Automáticos
"""

import streamlit as st
import requests
import random
import math
import time
from datetime import datetime, timezone

st.set_page_config(page_title="ESPN+ Pick Analyzer", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');
.main,.stApp{background-color:#0A0A0A;color:#E8E8E8;}
h1,h2,h3{font-family:'Bebas Neue',sans-serif!important;letter-spacing:2px;}
.hero-title{font-family:'Bebas Neue',sans-serif;font-size:3.2rem;color:#D00000;letter-spacing:4px;margin-bottom:0;text-shadow:0 0 30px rgba(208,0,0,0.4);}
.hero-sub{font-size:0.85rem;color:#888;letter-spacing:3px;text-transform:uppercase;}
.game-card{background:linear-gradient(135deg,#111128,#1A1A2E);border:1px solid #2A2A4A;border-left:4px solid #D00000;border-radius:8px;padding:14px;margin:6px 0;}
.sim-card{background:linear-gradient(135deg,#0A1A0A,#0D2010);border:1px solid #1a4a1a;border-left:4px solid #4ade80;border-radius:8px;padding:14px;margin:6px 0;}
.sim-card-gold{background:linear-gradient(135deg,#1A1400,#2D2000);border:2px solid #FFD700;border-radius:12px;padding:20px;margin:10px 0;box-shadow:0 0 30px rgba(255,215,0,0.15);}
.sim-card-red{background:linear-gradient(135deg,#1A0500,#2D0A00);border:1px solid #ef4444;border-left:4px solid #ef4444;border-radius:8px;padding:14px;margin:6px 0;}
.sim-card-mid{background:linear-gradient(135deg,#1A1200,#2D2000);border:1px solid #fbbf24;border-left:4px solid #fbbf24;border-radius:8px;padding:14px;margin:6px 0;}
.sim-card-purple{background:linear-gradient(135deg,#12001A,#200D2D);border:1px solid #a78bfa;border-left:4px solid #a78bfa;border-radius:8px;padding:14px;margin:6px 0;}
.parlay-card{background:linear-gradient(135deg,#001A1A,#002D2D);border:2px solid #22d3ee;border-radius:12px;padding:18px;margin:8px 0;box-shadow:0 0 20px rgba(34,211,238,0.1);}
.report-box{background:#111128;border:1px solid #2A2A4A;border-radius:12px;padding:24px;margin:8px 0;line-height:1.8;}
.section-title{font-family:'Bebas Neue',sans-serif;font-size:1.2rem;color:#D00000;letter-spacing:2px;border-bottom:1px solid #2A2A4A;padding-bottom:4px;margin:16px 0 8px 0;}
.market-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700;margin:2px;}
.tag-ml{background:#1a2a4a;color:#60a5fa;}
.tag-btts{background:#1a3a1a;color:#4ade80;}
.tag-ou{background:#3a2a00;color:#fbbf24;}
.tag-dc{background:#2a1a3a;color:#a78bfa;}
.tag-parlay{background:#001a1a;color:#22d3ee;}
.metric-box{background:#1A1A2E;border:1px solid #2A2A4A;border-radius:8px;padding:14px;text-align:center;}
.metric-num{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#D00000;}
.metric-label{font-size:0.7rem;color:#888;text-transform:uppercase;letter-spacing:2px;}
.prob-bar-bg{background:#1A1A2E;border-radius:4px;height:9px;margin:4px 0;}
.prob-bar-fill{height:9px;border-radius:4px;}
.ev-pos{color:#4ade80;font-weight:700;}
.ev-neg{color:#ef4444;font-weight:700;}
.badge-green{background:#1a4a1a;color:#4ade80;padding:2px 8px;border-radius:20px;font-size:0.72rem;font-weight:700;}
.badge-yellow{background:#3a3000;color:#fbbf24;padding:2px 8px;border-radius:20px;font-size:0.72rem;font-weight:700;}
.badge-red{background:#3a0a0a;color:#ef4444;padding:2px 8px;border-radius:20px;font-size:0.72rem;font-weight:700;}
.demo-banner{background:#1a1a00;border:1px solid #444400;border-radius:8px;padding:10px 16px;margin:8px 0;color:#fbbf24;font-size:0.85rem;}
.status-live{color:#4ade80;font-weight:700;}
.status-pre{color:#60a5fa;}
.stButton>button{background:linear-gradient(135deg,#D00000,#8B0000)!important;color:white!important;font-family:'Bebas Neue',sans-serif!important;font-size:1.05rem!important;letter-spacing:2px!important;border:none!important;padding:12px 32px!important;border-radius:6px!important;width:100%!important;}
hr{border-color:#2A2A4A;}
</style>
""", unsafe_allow_html=True)

# ── Leagues ───────────────────────────────────────────────────────────────────
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
# Goles/puntos promedio esperados por liga (para Poisson)
LEAGUE_AVG_GOALS = {
    "NBA":114.0,"WNBA":83.0,"NCAAB":72.0,
    "MLB":4.5,"NCAA Baseball":5.5,
    "NFL":23.0,"NCAAF":28.0,
    "NHL":3.1,
    "MLS":2.8,"Liga MX":2.6,"Premier League":2.7,"La Liga":2.6,
    "Bundesliga":3.1,"Serie A":2.6,"Ligue 1":2.7,
    "Champions League":2.9,"Europa League":2.7,"Liga de Expansión":2.5,
    "ATP":None,"WTA":None,  # No aplica goles
}
ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"

# ── Demo data ────────────────────────────────────────────────────────────────
def get_demo_games():
    return [
        {"id":"d1","league":"Premier League","home_team":"Arsenal","away_team":"Chelsea",
         "home_score":"","away_score":"","home_record":"20-6-5","away_record":"17-8-6",
         "state":"pre","status_detail":"Dom 12:30 PM","date":"","venue":"Emirates Stadium",
         "odds":{"spread":"","over_under":"2.5","home_ml":"-145","away_ml":"+380","home_wp":"52","away_wp":"23"}},
        {"id":"d2","league":"Champions League","home_team":"Real Madrid","away_team":"Bayern Munich",
         "home_score":"","away_score":"","home_record":"24-5-2","away_record":"22-6-3",
         "state":"pre","status_detail":"Mar 3:00 PM","date":"","venue":"Santiago Bernabéu",
         "odds":{"spread":"","over_under":"3.0","home_ml":"-118","away_ml":"+290","home_wp":"47","away_wp":"28"}},
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
        {"id":"d7","league":"NHL","home_team":"Florida Panthers","away_team":"Tampa Bay Lightning",
         "home_score":"","away_score":"","home_record":"41-18-6","away_record":"38-22-5",
         "state":"pre","status_detail":"7:00 PM ET","date":"","venue":"Amerant Bank Arena",
         "odds":{"spread":"","over_under":"6.0","home_ml":"-135","away_ml":"+115","home_wp":"55","away_wp":"45"}},
        {"id":"d8","league":"Bundesliga","home_team":"Bayern Munich","away_team":"Borussia Dortmund",
         "home_score":"","away_score":"","home_record":"20-4-4","away_record":"16-6-6",
         "state":"pre","status_detail":"Sáb 9:30 AM","date":"","venue":"Allianz Arena",
         "odds":{"spread":"","over_under":"3.5","home_ml":"-155","away_ml":"+400","home_wp":"58","away_wp":"18"}},
    ]

# ── ESPN Fetch ────────────────────────────────────────────────────────────────
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

# ── Math helpers ──────────────────────────────────────────────────────────────
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
    """Fast Poisson sampler via Knuth algorithm."""
    if lam <= 0: return 0
    L = math.exp(-lam); k = 0; p = 1.0
    while p > L:
        k += 1; p *= rng.random()
    return k - 1

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
    """Estimate expected goals/points per team using O/U line."""
    league=game["league"]
    avg=LEAGUE_AVG_GOALS.get(league)
    if avg is None: return None, None
    ou=game["odds"].get("over_under","")
    try: total=float(str(ou))
    except: total=avg*2
    base=compute_base_prob(game)
    hp=base["home_prob"]; ap=base["away_prob"]
    # Distribute total proportionally to win probability, with small home boost
    home_share = (hp + 0.52) / (hp + ap + 1.04)
    lam_home = total * home_share
    lam_away = total * (1 - home_share)
    return lam_home, lam_away

# ── Monte Carlo with Extended Markets ─────────────────────────────────────────
def run_monte_carlo(game, n=10_000):
    base=compute_base_prob(game)
    hp,dp,dq=base["home_prob"],base["draw_prob"],base["dq"]
    is_soccer=base["is_soccer"]
    sigma=(1-dq)*0.15
    lam_h, lam_a = get_lambda(game)
    use_goals = lam_h is not None

    # Result counters
    hw=aw=d=0
    # Goals markets
    btts=0; o15=0; o25=0; o35=0; u15=0; u25=0; u35=0
    # Double chance
    dc_1x=0; dc_x2=0; dc_12=0

    rng=random.Random()

    for _ in range(n):
        ph=max(0.01,min(0.99,hp+rng.gauss(0,sigma)))

        if use_goals:
            # Simulate actual score via Poisson
            lh=max(0.1, lam_h*(1+rng.gauss(0,0.15*(1-dq))))
            la=max(0.1, lam_a*(1+rng.gauss(0,0.15*(1-dq))))
            gh=poisson_sample(lh,rng); ga=poisson_sample(la,rng)
            total_g=gh+ga

            if is_soccer:
                if gh>ga: hw+=1; dc_1x+=1; dc_12+=1
                elif gh==ga: d+=1; dc_1x+=1; dc_x2+=1
                else: aw+=1; dc_x2+=1; dc_12+=1
            else:
                if gh>ga: hw+=1; dc_1x+=1; dc_12+=1
                else: aw+=1; dc_x2+=1; dc_12+=1

            if gh>0 and ga>0: btts+=1
            if total_g>1.5: o15+=1
            else: u15+=1
            if total_g>2.5: o25+=1
            else: u25+=1
            if total_g>3.5: o35+=1
            else: u35+=1
        else:
            # No score simulation (tennis/etc) — use probability only
            if is_soccer:
                pd=max(0.01,min(0.50,dp+rng.gauss(0,sigma*0.5)))
                phn=ph*(1-pd); pan=(1-ph)*(1-pd); t=phn+pan+pd
                phn/=t; pan/=t; pd/=t
                r=rng.random()
                if r<phn: hw+=1; dc_1x+=1; dc_12+=1
                elif r<phn+pd: d+=1; dc_1x+=1; dc_x2+=1
                else: aw+=1; dc_x2+=1; dc_12+=1
            else:
                if rng.random()<ph: hw+=1; dc_1x+=1; dc_12+=1
                else: aw+=1; dc_x2+=1; dc_12+=1

    # ── Probabilities ──────────────────────────────────────────────────────
    sh=hw/n; sa=aw/n; sd=d/n
    p_btts=btts/n if use_goals else None
    p_o15=o15/n if use_goals else None
    p_o25=o25/n if use_goals else None
    p_o35=o35/n if use_goals else None
    p_u25=(n-o25)/n if use_goals else None
    p_dc_1x=dc_1x/n; p_dc_x2=dc_x2/n; p_dc_12=dc_12/n

    # ── Moneyline EV ──────────────────────────────────────────────────────
    hml=game["odds"].get("home_ml",""); aml=game["odds"].get("away_ml","")
    ou=game["odds"].get("over_under","")
    home_ev=calc_ev(sh,hml) if hml else None
    away_ev=calc_ev(sa,aml) if aml else None
    hk=quarter_kelly(sh,hml) if hml else None
    ak=quarter_kelly(sa,aml) if aml else None

    # ── Goals markets EV (assume standard juice -110 unless line known) ───
    BTTS_ML = -115   # typical BTTS yes price
    NO_BTTS_ML = -105
    OU_ML = -110

    btts_ev   = calc_ev(p_btts, BTTS_ML) if p_btts is not None else None
    no_btts_ev= calc_ev(1-p_btts, NO_BTTS_ML) if p_btts is not None else None
    o15_ev    = calc_ev(p_o15, OU_ML) if p_o15 is not None else None
    o25_ev    = calc_ev(p_o25, OU_ML) if p_o25 is not None else None
    o35_ev    = calc_ev(p_o35, OU_ML) if p_o35 is not None else None
    u25_ev    = calc_ev(p_u25, OU_ML) if p_u25 is not None else None

    # Doble oportunidad (typical -200 for DC)
    DC_ML = -200
    dc_1x_ev = calc_ev(p_dc_1x, DC_ML)
    dc_x2_ev = calc_ev(p_dc_x2, DC_ML)
    dc_12_ev  = calc_ev(p_dc_12, DC_ML)

    # ── Best single bet across ALL markets ───────────────────────────────
    candidates = [
        ("ML", game["home_team"]+" ML", sh, home_ev, hml, hk),
        ("ML", game["away_team"]+" ML", sa, away_ev, aml, ak),
    ]
    if p_btts is not None:
        candidates += [
            ("BTTS", "Ambos Anotan SÍ", p_btts, btts_ev, str(BTTS_ML), quarter_kelly(p_btts,BTTS_ML)),
            ("BTTS", "Ambos Anotan NO", 1-p_btts if p_btts else None, no_btts_ev, str(NO_BTTS_ML), quarter_kelly(1-p_btts,NO_BTTS_ML) if p_btts else None),
            ("O/U",  f"Over 1.5", p_o15, o15_ev, str(OU_ML), quarter_kelly(p_o15,OU_ML)),
            ("O/U",  f"Over 2.5", p_o25, o25_ev, str(OU_ML), quarter_kelly(p_o25,OU_ML)),
            ("O/U",  f"Over 3.5", p_o35, o35_ev, str(OU_ML), quarter_kelly(p_o35,OU_ML)),
            ("O/U",  f"Under 2.5", p_u25, u25_ev, str(OU_ML), quarter_kelly(p_u25,OU_ML)),
        ]
    candidates += [
        ("DC", "Doble Oportunidad 1X", p_dc_1x, dc_1x_ev, str(DC_ML), quarter_kelly(p_dc_1x,DC_ML)),
        ("DC", "Doble Oportunidad X2", p_dc_x2, dc_x2_ev, str(DC_ML), quarter_kelly(p_dc_x2,DC_ML)),
        ("DC", "Doble Oportunidad 12", p_dc_12, dc_12_ev, str(DC_ML), quarter_kelly(p_dc_12,DC_ML)),
    ]

    best_single=None; best_ev_val=-999
    for mtype, label, prob, ev, ml, kelly in candidates:
        if prob is not None and ev is not None and ev > best_ev_val:
            best_ev_val=ev
            best_single={"market":mtype,"label":label,"prob":prob,"ev":ev,"ml":ml,"kelly":kelly or 0}

    # ── Best parlay: top 2 positive-EV legs from this game ────────────────
    pos_legs=[(mtype,label,prob,ev,ml) for mtype,label,prob,ev,ml,k in candidates
              if prob is not None and ev is not None and ev>0 and mtype!="DC"]
    pos_legs.sort(key=lambda x: x[3], reverse=True)
    best_parlay=None
    if len(pos_legs)>=2 and p_btts is not None:
        leg1,leg2=pos_legs[0],pos_legs[1]
        # Combined probability (assume independence — conservative)
        parlay_prob=leg1[2]*leg2[2]
        # Standard parlay payout: multiply decimal odds
        def ml_to_decimal(ml):
            try:
                ml=float(str(ml).replace("+",""))
                return (ml/100+1) if ml>0 else (100/abs(ml)+1)
            except: return 1.909
        dec1=ml_to_decimal(leg1[4]); dec2=ml_to_decimal(leg2[4])
        parlay_payout=(dec1*dec2-1)*100  # profit per $100
        parlay_ev=round(parlay_prob*parlay_payout-(1-parlay_prob)*100,2)
        best_parlay={"legs":[leg1,leg2],"prob":parlay_prob,
                     "ev":parlay_ev,"payout":round(parlay_payout,1)}

    return {
        "home_pct":round(sh*100,1),"away_pct":round(sa*100,1),"draw_pct":round(sd*100,1),
        "data_quality":round(dq*100,0),
        "home_ev":home_ev,"away_ev":away_ev,
        "home_ml":hml,"away_ml":aml,"over_under":ou,
        "home_kelly":hk,"away_kelly":ak,
        # Goals markets
        "p_btts":round(p_btts*100,1) if p_btts is not None else None,
        "btts_ev":btts_ev,"no_btts_ev":no_btts_ev,
        "p_o15":round(p_o15*100,1) if p_o15 is not None else None,"o15_ev":o15_ev,
        "p_o25":round(p_o25*100,1) if p_o25 is not None else None,"o25_ev":o25_ev,
        "p_o35":round(p_o35*100,1) if p_o35 is not None else None,"o35_ev":o35_ev,
        "p_u25":round(p_u25*100,1) if p_u25 is not None else None,"u25_ev":u25_ev,
        # Double chance
        "p_dc_1x":round(p_dc_1x*100,1),"dc_1x_ev":dc_1x_ev,
        "p_dc_x2":round(p_dc_x2*100,1),"dc_x2_ev":dc_x2_ev,
        "p_dc_12":round(p_dc_12*100,1),"dc_12_ev":dc_12_ev,
        # Best picks
        "best_single":best_single,"best_parlay":best_parlay,
        "is_soccer":is_soccer,"n_simulations":n,
        "use_goals":use_goals,
    }

def run_all_simulations(games, n=10_000):
    results=[]; pb=st.progress(0); st_txt=st.empty()
    for i,game in enumerate(games):
        st_txt.markdown(f"**⚙️ [{i+1}/{len(games)}]** `{game['away_team']} @ {game['home_team']}` — {game['league']}")
        results.append({**game,"sim":run_monte_carlo(game,n)})
        pb.progress((i+1)/len(games))
    pb.empty(); st_txt.empty()
    return results

# ── Report ────────────────────────────────────────────────────────────────────
def confidence_label(ev, dq):
    if ev>=10 and dq>=60: return "ALTA","badge-green","🟢"
    if ev>=5  and dq>=40: return "MEDIA","badge-yellow","🟡"
    return "BAJA","badge-red","🔴"

def edge_pct(prob_sim, ml):
    try: return round((prob_sim-ml_to_prob(float(str(ml).replace("+",""))))*100,1)
    except: return 0.0

def market_tag(mtype):
    tags={"ML":"tag-ml ML","BTTS":"tag-btts BTTS","O/U":"tag-ou O/U","DC":"tag-dc DC","PARLAY":"tag-parlay PARLAY"}
    cls,lbl=tags.get(mtype,"tag-ml ML").split(" ",1)
    return f'<span class="market-tag {cls}">{lbl}</span>'

def generate_report(sim_results, is_demo=False):
    today=datetime.now(timezone.utc).strftime("%A %d %b %Y, %H:%M UTC")

    # Collect all best singles
    all_singles=[]
    for r in sim_results:
        sim=r["sim"]; bs=sim.get("best_single")
        if bs and bs["ev"]>0:
            eg=edge_pct(bs["prob"],bs["ml"]) if bs["market"]=="ML" else 0
            all_singles.append({**r,"bs":bs,"edge":eg})
    all_singles.sort(key=lambda x: x["bs"]["ev"],reverse=True)

    # Collect all parlays
    all_parlays=[]
    for r in sim_results:
        sim=r["sim"]; bp=sim.get("best_parlay")
        if bp and bp["ev"]>0:
            all_parlays.append({**r,"bp":bp})
    all_parlays.sort(key=lambda x: x["bp"]["ev"],reverse=True)

    lines=['<div class="report-box">']
    if is_demo:
        lines.append('<div class="demo-banner">⚠️ <b>MODO DEMO</b> — Datos ilustrativos. Activa ligas reales en el sidebar.</div>')
    lines.append(f'<div style="color:#555;font-size:0.8rem;margin-bottom:16px">📅 {today} · {len(sim_results)} partidos · {sim_results[0]["sim"]["n_simulations"]:,} iters/partido</div>')

    # ── PICK PRINCIPAL ────────────────────────────────────────────────────
    if all_singles:
        top=all_singles[0]; bs=top["bs"]; sim=top["sim"]
        conf,badge_cls,emoji=confidence_label(bs["ev"],sim["data_quality"])
        impl=ml_to_prob(bs["ml"])*100 if bs["ml"] and bs["market"]=="ML" else 0
        lines.append('<div class="section-title">🥇 PICK PRINCIPAL</div>')
        lines.append(f"""<div class="sim-card-gold" style="margin:0">
          <div style="font-size:1.05rem;font-weight:700;color:#fff">{top['away_team']} @ {top['home_team']}</div>
          <div style="color:#888;font-size:0.8rem;margin-bottom:8px">{top['league']} · {top['status_detail']}</div>
          <div style="margin-bottom:10px">{market_tag(bs['market'])}
            <span style="font-size:1.2rem;color:#FFD700;font-weight:700;margin-left:8px">► {bs['label']}</span>
          </div>
          <div style="display:flex;gap:18px;flex-wrap:wrap;margin-bottom:10px">
            <div><div style="color:#888;font-size:0.68rem">PROB. SIMULADA</div><div style="font-size:1.3rem;font-weight:700;color:#4ade80">{bs['prob']*100:.1f}%</div></div>
            {"<div><div style='color:#888;font-size:0.68rem'>PROB. IMPLÍCITA</div><div style='font-size:1.3rem;font-weight:700;color:#aaa'>"+str(round(impl,1))+"%</div></div>" if impl else ""}
            {"<div><div style='color:#888;font-size:0.68rem'>EDGE</div><div style='font-size:1.3rem;font-weight:700;color:#60a5fa'>+"+str(top['edge'])+"%</div></div>" if top['edge'] else ""}
            <div><div style="color:#888;font-size:0.68rem">EV / $100</div><div style="font-size:1.3rem;font-weight:700;color:#FFD700">+{bs['ev']:.1f}</div></div>
            <div><div style="color:#888;font-size:0.68rem">KELLY 25%</div><div style="font-size:1.3rem;font-weight:700;color:#a78bfa">{bs['kelly']:.1%}</div></div>
            <div><div style="color:#888;font-size:0.68rem">CONFIANZA</div><div style="margin-top:4px"><span class="{badge_cls}">{emoji} {conf}</span></div></div>
          </div>
        </div>""")

        # ── VALUE BETS ADICIONALES ────────────────────────────────────────
        if len(all_singles)>1:
            lines.append(f'<div class="section-title">🥈 TODAS LAS VALUE BETS ({len(all_singles)-1} adicionales)</div>')
            for r in all_singles[1:8]:
                bs2=r["bs"]; sim2=r["sim"]
                conf2,badge2,em2=confidence_label(bs2["ev"],sim2["data_quality"])
                lines.append(f"""<div class="sim-card">
                  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;align-items:center">
                    <div>
                      <div style="font-weight:700;font-size:0.9rem">{r['away_team']} @ {r['home_team']}</div>
                      <div style="color:#555;font-size:0.75rem">{r['league']}</div>
                      <div style="margin-top:3px">{market_tag(bs2['market'])}
                        <span style="color:#4ade80;font-weight:700"> {bs2['label']}</span>
                      </div>
                    </div>
                    <div style="text-align:right">
                      <span class="{badge2}">{em2} {conf2}</span><br>
                      <span style="color:#FFD700;font-weight:700">EV +{bs2['ev']:.1f}</span><br>
                      <span style="color:#aaa;font-size:0.75rem">{bs2['prob']*100:.1f}% prob · Kelly {bs2['kelly']:.1%}</span>
                    </div>
                  </div>
                </div>""")

    # ── MEJORES PARLAYS ───────────────────────────────────────────────────
    if all_parlays:
        lines.append(f'<div class="section-title">🎰 MEJORES COMBINADAS / PARLAYS ({len(all_parlays)})</div>')
        for r in all_parlays[:4]:
            bp=r["bp"]; legs=bp["legs"]
            conf_p,badge_p,em_p=confidence_label(bp["ev"],r["sim"]["data_quality"])
            leg_html="".join(
                f'<div style="padding:4px 0;border-bottom:1px solid #1a3a3a;font-size:0.82rem">'
                f'{market_tag(lg[0])} <span style="color:#E8E8E8">{lg[1]}</span> '
                f'<span style="color:#4ade80">{lg[2]*100:.1f}%</span></div>'
                for lg in legs
            )
            lines.append(f"""<div class="parlay-card">
              <div style="font-weight:700;color:#22d3ee;margin-bottom:6px">🎰 PARLAY: {r['away_team']} @ {r['home_team']} — {r['league']}</div>
              {leg_html}
              <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
                <div><div style="color:#888;font-size:0.68rem">PROB. COMBINADA</div><div style="font-size:1.1rem;font-weight:700;color:#4ade80">{bp['prob']*100:.1f}%</div></div>
                <div><div style="color:#888;font-size:0.68rem">PAGO / $100</div><div style="font-size:1.1rem;font-weight:700;color:#22d3ee">+{bp['payout']:.0f}</div></div>
                <div><div style="color:#888;font-size:0.68rem">EV / $100</div><div style="font-size:1.1rem;font-weight:700;color:#FFD700">{"+" if bp['ev']>0 else ""}{bp['ev']:.1f}</div></div>
                <div style="margin-top:4px"><span class="{badge_p}">{em_p} {conf_p}</span></div>
              </div>
            </div>""")

    # ── RESUMEN ───────────────────────────────────────────────────────────
    if not all_singles:
        lines.append('<div class="section-title">⚠️ SIN VALUE BETS</div>')
        lines.append('<p style="color:#888">No se encontraron apuestas con EV positivo. Amplía las ligas seleccionadas.</p>')

    total_sims=len(sim_results)*sim_results[0]["sim"]["n_simulations"]
    n_goals=[r for r in sim_results if r["sim"]["use_goals"]]
    lines.append('<div class="section-title">📈 RESUMEN</div>')
    lines.append(f"""<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px">
      <div style="background:#1a4a1a;padding:8px 14px;border-radius:6px;text-align:center"><div style="font-size:1.3rem;font-weight:700;color:#4ade80">{len(all_singles)}</div><div style="color:#888;font-size:0.7rem">BETS EV+</div></div>
      <div style="background:#001a1a;padding:8px 14px;border-radius:6px;text-align:center"><div style="font-size:1.3rem;font-weight:700;color:#22d3ee">{len(all_parlays)}</div><div style="color:#888;font-size:0.7rem">PARLAYS EV+</div></div>
      <div style="background:#1A1A2E;padding:8px 14px;border-radius:6px;text-align:center"><div style="font-size:1.3rem;font-weight:700;color:#a78bfa">{len(n_goals)}</div><div style="color:#888;font-size:0.7rem">CON GOLES SIM</div></div>
      <div style="background:#1A1A2E;padding:8px 14px;border-radius:6px;text-align:center"><div style="font-size:1.3rem;font-weight:700;color:#60a5fa">{total_sims:,}</div><div style="color:#888;font-size:0.7rem">TOTAL SIMS</div></div>
    </div>
    <div style="color:#555;font-size:0.72rem;margin-top:6px">⚠️ EV de BTTS/O/U calculado asumiendo cuota estándar (-110/-115). Verifica cuota real en tu casa. Solo fines informativos.</div>""")
    lines.append("</div>")
    return "\n".join(lines)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title">ESPN+</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Monte Carlo · Mercados Extendidos</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🎲 Simulación")
    n_sims=st.select_slider("Iteraciones",options=[1_000,2_500,5_000,10_000,25_000],value=10_000)
    st.caption(f"⚡ {n_sims:,} sims/partido")
    st.divider()
    st.markdown("### 🏆 Ligas")
    groups=sorted(set(v["group"] for v in LEAGUES.values()))
    sel_groups=st.multiselect("Grupos",groups,default=["Basketball","Baseball","Soccer"])
    avail=[n for n,cfg in LEAGUES.items() if cfg["group"] in sel_groups]
    sel_leagues=st.multiselect("Ligas",avail,default=avail)
    st.divider()
    use_demo=st.toggle("🧪 Forzar datos demo",value=False)
    st.divider()
    st.caption("📡 ESPN API · caché 5 min")
    st.caption("🎯 ML · BTTS · O/U · DC · Parlays")
    st.caption("💰 100% Gratis")
    if st.button("🔄 Limpiar caché"):
        st.cache_data.clear(); st.session_state.pop("sim_results",None); st.success("✅")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🎯 Monte Carlo Pick Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">ML · BTTS · Over/Under · Doble Oportunidad · Parlays · 100% Gratis</p>', unsafe_allow_html=True)
st.divider()

if not sel_leagues: st.warning("⚠️ Selecciona al menos una liga."); st.stop()

is_demo=False
if use_demo:
    games=get_demo_games(); is_demo=True
    st.info("🧪 Usando datos demo.")
else:
    with st.spinner("📡 Cargando datos de ESPN..."):
        games,fetch_errors=get_all_games(sel_leagues)
    if not games:
        st.warning("⚠️ ESPN no retornó partidos.")
        col_a,col_b=st.columns(2)
        with col_a:
            if st.button("🔄 Reintentar"): st.cache_data.clear(); st.rerun()
        with col_b:
            if st.button("🧪 Usar demo"): st.session_state["force_demo"]=True; st.rerun()
        st.stop()
    else:
        sel_set=set(sel_leagues)
        games=[g for g in games if g["league"] in sel_set] or games

if st.session_state.get("force_demo"):
    games=get_demo_games(); is_demo=True; st.session_state.pop("force_demo",None)

live_g=[g for g in games if g["state"]=="in"]
pre_g=[g for g in games if g["state"]=="pre"]
odds_g=[g for g in games if g["odds"]]

c1,c2,c3,c4=st.columns(4)
for col,num,label,color in [(c1,len(games),"Partidos","#D00000"),(c2,len(live_g),"En Vivo","#4ade80"),(c3,len(pre_g),"Próximos","#60a5fa"),(c4,len(odds_g),"Con Cuotas","#FFD700")]:
    col.markdown(f'<div class="metric-box"><div class="metric-num" style="color:{color}">{num}</div><div class="metric-label">{label}</div></div>',unsafe_allow_html=True)

st.divider()
tab_report,tab_sim,tab_all=st.tabs(["🎯 Reporte de Picks","🎲 Simulaciones","📋 Partidos"])

# ── TAB REPORT ────────────────────────────────────────────────────────────────
with tab_report:
    sr=st.session_state.get("sim_results",[])
    if not sr:
        st.info("👈 Ve al tab **🎲 Simulaciones** y presiona el botón.")
        st.markdown("""
**Mercados que analiza esta versión:**

| Mercado | Descripción |
|---------|-------------|
| <span class="market-tag tag-ml">ML</span> | Moneyline — ganador del partido | 
| <span class="market-tag tag-btts">BTTS</span> | Ambos Anotan Sí/No |
| <span class="market-tag tag-ou">O/U</span> | Over/Under 1.5, 2.5, 3.5 goles |
| <span class="market-tag tag-dc">DC</span> | Doble Oportunidad 1X / X2 / 12 |
| <span class="market-tag tag-parlay">PARLAY</span> | Combinada automática de los 2 mejores legs |

BTTS y O/U usan simulación de goles por distribución **Poisson** calibrada al O/U line de ESPN.
        """, unsafe_allow_html=True)
    else:
        report_html=generate_report(sr,is_demo=st.session_state.get("last_sim_demo",False))
        st.markdown(report_html,unsafe_allow_html=True)

# ── TAB SIMULATIONS ───────────────────────────────────────────────────────────
with tab_sim:
    st.markdown(f"### {len(games)} partidos × {n_sims:,} iteraciones = **{len(games)*n_sims:,} simulaciones**")
    if is_demo: st.markdown('<div class="demo-banner">🧪 Modo DEMO activo.</div>',unsafe_allow_html=True)

    if st.button(f"🚀 CORRER {n_sims:,} SIMULACIONES",key="run_sim"):
        t0=time.time()
        sr2=run_all_simulations(games,n=n_sims)
        elapsed=time.time()-t0
        st.session_state["sim_results"]=sr2
        st.session_state["last_sim_demo"]=is_demo
        st.success(f"✅ {len(games)*n_sims:,} simulaciones en {elapsed:.1f}s — ve al tab **🎯 Reporte de Picks**")
        st.balloons()

    sr=st.session_state.get("sim_results",[])
    if sr:
        sort_by=st.selectbox("Ordenar por",["Mejor EV (cualquier mercado)","Mayor prob. local","Mayor prob. visitante","Calidad dato"])
        def sk(r):
            s=r["sim"]; bs=s.get("best_single")
            if "EV" in sort_by: return bs["ev"] if bs else -999
            if "local" in sort_by: return s["home_pct"]
            if "visitante" in sort_by: return s["away_pct"]
            return s["data_quality"]
        sorted_r=sorted(sr,key=sk,reverse=True)
        ev_filter=st.checkbox("Solo EV positivo",value=False)
        display=[r for r in sorted_r if not ev_filter or (r["sim"].get("best_single") and r["sim"]["best_single"]["ev"]>0)]

        for r in display:
            sim=r["sim"]; bs=sim.get("best_single"); dq=sim["data_quality"]
            card="sim-card" if (bs and bs["ev"]>5) else "sim-card-red" if not(bs and bs["ev"]>0) else "game-card"
            def bar(pct,color,label):
                return f'<div style="margin:3px 0"><div style="display:flex;justify-content:space-between"><span style="font-size:0.75rem;color:#aaa">{label}</span><span style="font-size:0.75rem;font-weight:700;color:{color}">{pct:.1f}%</span></div><div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{min(pct,100):.1f}%;background:{color}"></div></div></div>'

            bars=bar(sim["away_pct"],"#60a5fa",r["away_team"])
            if sim["is_soccer"]: bars+=bar(sim["draw_pct"],"#a78bfa","Empate")
            bars+=bar(sim["home_pct"],"#f97316",r["home_team"])

            best_badge=f'{market_tag(bs["market"])} <span class="badge-green">EV +{bs["ev"]:.1f}</span>' if (bs and bs["ev"]>0) else ""
            dqc="#4ade80" if dq>=70 else "#fbbf24" if dq>=40 else "#ef4444"

            # Goals markets summary
            goals_html=""
            if sim["use_goals"] and sim.get("p_btts") is not None:
                btts_color="#4ade80" if (sim.get("btts_ev") or 0)>0 else "#ef4444"
                o25_color="#4ade80" if (sim.get("o25_ev") or 0)>0 else "#ef4444"
                goals_html=f"""<div style="margin-top:6px;font-size:0.78rem;display:flex;gap:12px;flex-wrap:wrap">
                  <span>⚽ BTTS: <b style="color:{btts_color}">{sim['p_btts']}%</b> (EV {sim.get('btts_ev',0) or 0:+.1f})</span>
                  <span>📊 O2.5: <b style="color:{o25_color}">{sim['p_o25']}%</b> (EV {sim.get('o25_ev',0) or 0:+.1f})</span>
                  <span>📊 O1.5: <b>{sim['p_o15']}%</b></span>
                  <span>📊 O3.5: <b>{sim['p_o35']}%</b></span>
                </div>"""

            # Best parlay badge
            parlay_html=""
            bp=sim.get("best_parlay")
            if bp and bp["ev"]>0:
                parlay_html=f'<br><span class="market-tag tag-parlay">PARLAY EV +{bp["ev"]:.1f} · pago +{bp["payout"]:.0f}</span>'

            st.markdown(f"""<div class="{card}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap">
                <div>
                  <strong>{r['away_team']} @ {r['home_team']}</strong>
                  <br><small style="color:#555">{r['league']} · {r['status_detail']} · <span style="color:{dqc}">DQ {dq:.0f}%</span></small>
                  {("<br>"+best_badge) if best_badge else ""}
                  {parlay_html}
                </div>
                <div style="text-align:right;font-size:0.78rem;color:#888">
                  ML {sim['away_ml'] or 'N/A'} / {sim['home_ml'] or 'N/A'}
                </div>
              </div>
              <div style="margin-top:8px">{bars}</div>
              {goals_html}
            </div>""",unsafe_allow_html=True)

        # CSV
        st.divider()
        csv=["Liga,Visitante,Local,Prob Vis%,Prob Local%,Empate%,ML Vis,ML Local,EV Vis,EV Local,BTTS%,EV BTTS,O2.5%,EV O2.5,O3.5%,DC 1X%,DC X2%,DC 12%,Mejor Mercado,Mejor Label,Mejor EV,DQ%"]
        for r in sorted_r:
            s=r["sim"]; bs=s.get("best_single",{}) or {}
            csv.append(",".join([
                r['league'],r['away_team'],r['home_team'],
                str(s['away_pct']),str(s['home_pct']),str(s['draw_pct']),
                str(s['away_ml']),str(s['home_ml']),
                str(s['away_ev'] or ""),str(s['home_ev'] or ""),
                str(s['p_btts'] or ""),str(s['btts_ev'] or ""),
                str(s['p_o25'] or ""),str(s['o25_ev'] or ""),
                str(s['p_o35'] or ""),
                str(s['p_dc_1x']),str(s['p_dc_x2']),str(s['p_dc_12']),
                bs.get('market',""),bs.get('label',""),str(bs.get('ev',"")),
                str(s['data_quality'])
            ]))
        st.download_button("💾 Descargar CSV completo",data="\n".join(csv),
                           file_name=f"mc_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",mime="text/csv")

# ── TAB ALL GAMES ─────────────────────────────────────────────────────────────
with tab_all:
    cf1,cf2=st.columns(2)
    with cf1: fs=st.multiselect("Estado",["pre","in","post"],default=["pre","in"],format_func=lambda x:{"pre":"🔵 Próximo","in":"🔴 En Vivo","post":"⚫ Final"}[x])
    with cf2: fl=st.multiselect("Liga",list(set(g["league"] for g in games)),default=list(set(g["league"] for g in games)))
    filtered=[g for g in games if g["state"] in fs and g["league"] in fl]
    st.caption(f"Mostrando {len(filtered)} de {len(games)} partidos {'(DEMO)' if is_demo else ''}")
    for g in filtered:
        sc={"in":"status-live","pre":"status-pre","post":"status-post"}.get(g["state"],"")
        si={"in":"🔴","pre":"🔵","post":"⚫"}.get(g["state"],"")
        oh=""
        if g["odds"]:
            o=g["odds"]; parts=[]
            if o.get("spread"): parts.append(f"<b>Spread:</b> {o['spread']}")
            if o.get("over_under"): parts.append(f"<b>O/U:</b> {o['over_under']}")
            if o.get("home_ml"): parts.append(f"<b>ML Casa:</b> {o['home_ml']}")
            if o.get("away_ml"): parts.append(f"<b>ML Vis:</b> {o['away_ml']}")
            if parts: oh="<br><small style='color:#FFD700'>"+" · ".join(parts)+"</small>"
        sh=f" <span style='color:#4ade80;font-weight:700'>{g['away_score']}-{g['home_score']}</span>" if g["state"]=="in" and g["home_score"] else ""
        rh=f"<br><small style='color:#555'>{g.get('away_record','?')} vs {g.get('home_record','?')}</small>" if (g.get("away_record") or g.get("home_record")) else ""
        st.markdown(f"""<div class="game-card">
          <div style="display:flex;justify-content:space-between">
            <strong>{g['away_team']} @ {g['home_team']}{sh}</strong>
            <span class="{sc}">{si} {g['status_detail']}</span>
          </div>
          <small style="color:#555">{g['league']}</small>{rh}{oh}
        </div>""",unsafe_allow_html=True)

st.divider()
st.markdown('<div style="text-align:center;color:#444;font-size:0.72rem">ESPN+ Monte Carlo · ML · BTTS · O/U · DC · Parlays · 100% Gratis · ⚠️ Solo fines informativos</div>',unsafe_allow_html=True)

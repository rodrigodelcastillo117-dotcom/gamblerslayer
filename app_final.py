"""
ESPN+ Pick Analyzer — Motor Monte Carlo (10,000 sims) · 100% Gratis · Sin API de pago
"""

import streamlit as st
import requests
import random
import time
from datetime import datetime, timezone

st.set_page_config(page_title="ESPN+ Pick Analyzer", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');
.main, .stApp { background-color: #0A0A0A; color: #E8E8E8; }
h1,h2,h3 { font-family:'Bebas Neue',sans-serif !important; letter-spacing:2px; }
.hero-title { font-family:'Bebas Neue',sans-serif; font-size:3.5rem; color:#D00000; letter-spacing:4px; margin-bottom:0; text-shadow:0 0 30px rgba(208,0,0,0.4); }
.hero-sub { font-size:0.9rem; color:#888; letter-spacing:3px; text-transform:uppercase; }
.game-card { background:linear-gradient(135deg,#111128,#1A1A2E); border:1px solid #2A2A4A; border-left:4px solid #D00000; border-radius:8px; padding:16px; margin:8px 0; }
.sim-card  { background:linear-gradient(135deg,#0A1A0A,#0D2010); border:1px solid #1a4a1a; border-left:4px solid #4ade80; border-radius:8px; padding:16px; margin:8px 0; }
.sim-card-gold { background:linear-gradient(135deg,#1A1400,#2D2000); border:2px solid #FFD700; border-radius:12px; padding:20px; margin:10px 0; box-shadow:0 0 30px rgba(255,215,0,0.15); }
.sim-card-red  { background:linear-gradient(135deg,#1A0500,#2D0A00); border:1px solid #ef4444; border-left:4px solid #ef4444; border-radius:8px; padding:16px; margin:8px 0; }
.sim-card-mid  { background:linear-gradient(135deg,#1A1200,#2D2000); border:1px solid #fbbf24; border-left:4px solid #fbbf24; border-radius:8px; padding:16px; margin:8px 0; }
.pick-box { background:linear-gradient(135deg,#1A0A00,#2D1500); border:2px solid #FFD700; border-radius:12px; padding:24px; margin:16px 0; box-shadow:0 0 40px rgba(255,215,0,0.15); }
.pick-title { font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#FFD700; letter-spacing:3px; }
.report-box { background:#111128; border:1px solid #2A2A4A; border-radius:12px; padding:24px; margin:8px 0; line-height:1.8; }
.section-title { font-family:'Bebas Neue',sans-serif; font-size:1.3rem; color:#D00000; letter-spacing:2px; border-bottom:1px solid #2A2A4A; padding-bottom:4px; margin:16px 0 8px 0; }
.metric-box { background:#1A1A2E; border:1px solid #2A2A4A; border-radius:8px; padding:16px; text-align:center; }
.metric-num { font-family:'Bebas Neue',sans-serif; font-size:2.2rem; color:#D00000; }
.metric-label { font-size:0.75rem; color:#888; text-transform:uppercase; letter-spacing:2px; }
.prob-bar-bg   { background:#1A1A2E; border-radius:4px; height:10px; margin:4px 0; }
.prob-bar-fill { height:10px; border-radius:4px; }
.ev-pos { color:#4ade80; font-weight:700; }
.ev-neg { color:#ef4444; font-weight:700; }
.badge-green  { background:#1a4a1a; color:#4ade80; padding:2px 10px; border-radius:20px; font-size:0.8rem; font-weight:700; }
.badge-yellow { background:#3a3000; color:#fbbf24; padding:2px 10px; border-radius:20px; font-size:0.8rem; font-weight:700; }
.badge-red    { background:#3a0a0a; color:#ef4444; padding:2px 10px; border-radius:20px; font-size:0.8rem; font-weight:700; }
.status-live { color:#4ade80; font-weight:700; }
.status-pre  { color:#60a5fa; }
.status-post { color:#888; }
.stButton>button { background:linear-gradient(135deg,#D00000,#8B0000) !important; color:white !important; font-family:'Bebas Neue',sans-serif !important; font-size:1.1rem !important; letter-spacing:2px !important; border:none !important; padding:12px 32px !important; border-radius:6px !important; width:100% !important; }
hr { border-color:#2A2A4A; }
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
ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"
HOME_BOOST = {"NBA":0.035,"WNBA":0.03,"NCAAB":0.05,"MLB":0.025,"NCAA Baseball":0.02,
              "NFL":0.035,"NCAAF":0.045,"NHL":0.03,"MLS":0.04,"Liga MX":0.045,
              "Premier League":0.038,"La Liga":0.04,"Bundesliga":0.042,"Serie A":0.04,
              "Ligue 1":0.04,"Champions League":0.035,"Europa League":0.035,
              "Liga de Expansión":0.05,"ATP":0.01,"WTA":0.01}

# ── ESPN Fetch ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_scoreboard(sport, league):
    try:
        r = requests.get(ESPN_URL.format(sport=sport,league=league), timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200: return r.json()
    except: pass
    return {}

def parse_games(data, league_name):
    games = []
    for event in data.get("events",[]):
        try:
            comp  = event.get("competitions",[{}])[0]
            comps = comp.get("competitors",[])
            if len(comps) < 2: continue
            home = next((c for c in comps if c.get("homeAway")=="home"), comps[0])
            away = next((c for c in comps if c.get("homeAway")=="away"), comps[1])
            status = event.get("status",{})
            odds_info = {}
            odds_list = comp.get("odds",[])
            if odds_list:
                o = odds_list[0]
                odds_info = {
                    "spread":    o.get("details",""),
                    "over_under":o.get("overUnder",""),
                    "home_ml":   o.get("homeTeamOdds",{}).get("moneyLine",""),
                    "away_ml":   o.get("awayTeamOdds",{}).get("moneyLine",""),
                    "home_wp":   o.get("homeTeamOdds",{}).get("winPercentage",""),
                    "away_wp":   o.get("awayTeamOdds",{}).get("winPercentage",""),
                }
            hr = home.get("records",[{}]); ar = away.get("records",[{}])
            games.append({
                "id":          event.get("id",""),
                "league":      league_name,
                "home_team":   home.get("team",{}).get("displayName","Home"),
                "away_team":   away.get("team",{}).get("displayName","Away"),
                "home_score":  home.get("score",""),
                "away_score":  away.get("score",""),
                "home_record": hr[0].get("summary","") if hr else "",
                "away_record": ar[0].get("summary","") if ar else "",
                "state":       status.get("type",{}).get("state","pre"),
                "status_detail":status.get("type",{}).get("shortDetail",""),
                "date":        event.get("date",""),
                "venue":       comp.get("venue",{}).get("fullName",""),
                "odds":        odds_info,
            })
        except: continue
    return games

def get_all_games(leagues):
    result = []
    for name in leagues:
        cfg = LEAGUES[name]
        result.extend(parse_games(fetch_scoreboard(cfg["sport"],cfg["league"]), name))
    return result

# ── Math helpers ──────────────────────────────────────────────────────────────
def ml_to_prob(ml):
    try:
        ml = float(str(ml).replace("+",""))
        return 100/(ml+100) if ml>0 else abs(ml)/(abs(ml)+100)
    except: return 0.5

def win_pct(rec):
    try:
        p = rec.strip().split("-"); w,l = int(p[0]),int(p[1])
        return w/(w+l) if (w+l)>=5 else None
    except: return None

def calc_ev(prob, ml):
    try:
        ml = float(str(ml).replace("+",""))
        payout = ml if ml>0 else 10000/abs(ml)
        return round(prob*payout - (1-prob)*100, 2)
    except: return None

def quarter_kelly(prob, ml):
    try:
        ml = float(str(ml).replace("+",""))
        b = ml/100 if ml>0 else 100/abs(ml)
        k = (b*prob-(1-prob))/b
        return max(0.0, round(k*0.25, 4))
    except: return None

def compute_base_prob(game):
    signals, weights = [], []
    odds = game["odds"]; league = game["league"]
    is_soccer = LEAGUES.get(league,{}).get("group")=="Soccer"
    hwp = odds.get("home_wp",""); awp = odds.get("away_wp","")
    if hwp and awp:
        try:
            hw = float(str(hwp).replace("%",""))/100
            aw = float(str(awp).replace("%",""))/100
            if 0<hw<1 and 0<aw<1: signals.append(hw/(hw+aw)); weights.append(3.0)
        except: pass
    hml = odds.get("home_ml",""); aml = odds.get("away_ml","")
    if hml and aml:
        hp=ml_to_prob(hml); ap=ml_to_prob(aml); vig=hp+ap
        if 1.0<vig<1.25: signals.append(hp/vig); weights.append(4.0)
    hrec=win_pct(game.get("home_record","")); arec=win_pct(game.get("away_record",""))
    if hrec is not None and arec is not None:
        t=hrec+arec
        if t>0: signals.append(hrec/t); weights.append(1.5)
    elif hrec is not None: signals.append(hrec); weights.append(0.8)
    elif arec is not None: signals.append(1-arec); weights.append(0.8)
    home_p = sum(s*w for s,w in zip(signals,weights))/sum(weights) if signals else 0.5
    home_p = min(0.95, max(0.05, home_p + HOME_BOOST.get(league,0.03)))
    dq = min(1.0, sum(weights)/8.0)
    if is_soccer:
        bd = max(0.10, min(0.35, 0.28-abs(home_p-0.5)*0.3))
        rem=1-bd; ha=home_p*rem; aa=(1-home_p)*rem
        return {"home_prob":ha,"away_prob":aa,"draw_prob":bd,"dq":dq,"is_soccer":True}
    return {"home_prob":home_p,"away_prob":1-home_p,"draw_prob":0.0,"dq":dq,"is_soccer":False}

# ── Monte Carlo ───────────────────────────────────────────────────────────────
def run_monte_carlo(game, n=10_000):
    base = compute_base_prob(game)
    hp,ap,dp,dq = base["home_prob"],base["away_prob"],base["draw_prob"],base["dq"]
    is_soccer = base["is_soccer"]
    sigma = (1-dq)*0.15
    hw=aw=d=0; rng=random.Random()
    for _ in range(n):
        ph = max(0.01,min(0.99, hp+rng.gauss(0,sigma)))
        if is_soccer:
            pd = max(0.01,min(0.50, dp+rng.gauss(0,sigma*0.5)))
            phn=ph*(1-pd); pan=(1-ph)*(1-pd); t=phn+pan+pd
            phn/=t; pan/=t; pd/=t
            r=rng.random()
            if r<phn: hw+=1
            elif r<phn+pd: d+=1
            else: aw+=1
        else:
            if rng.random()<ph: hw+=1
            else: aw+=1
    sh=hw/n; sa=aw/n; sd=d/n
    hml=game["odds"].get("home_ml",""); aml=game["odds"].get("away_ml","")
    ou=game["odds"].get("over_under","")
    home_ev=calc_ev(sh,hml) if hml else None
    away_ev=calc_ev(sa,aml) if aml else None
    over_prob = min(0.70, max(0.30, 0.50+rng.gauss(0,0.04*(1-dq))))
    over_ev=calc_ev(over_prob,-110) if ou else None
    hk=quarter_kelly(sh,hml) if hml else None
    ak=quarter_kelly(sa,aml) if aml else None
    best_bet=None; best_ev=-999
    for side,team,prob,ev,ml,kelly in [
        ("home",game["home_team"],sh,home_ev,hml,hk),
        ("away",game["away_team"],sa,away_ev,aml,ak),
    ]:
        if ev is not None and ev>best_ev: best_ev=ev; best_bet={"side":side,"team":team,"prob":prob,"ev":ev,"ml":ml,"kelly":kelly}
    return {
        "home_pct":round(sh*100,1),"away_pct":round(sa*100,1),"draw_pct":round(sd*100,1),
        "data_quality":round(dq*100,0),
        "home_ev":home_ev,"away_ev":away_ev,"over_ev":over_ev,
        "home_ml":hml,"away_ml":aml,"over_under":ou,
        "home_kelly":hk,"away_kelly":ak,
        "best_bet":best_bet,"is_soccer":is_soccer,"n_simulations":n,
    }

def run_all_simulations(games, n=10_000):
    results=[]; pb=st.progress(0); st_txt=st.empty()
    for i,game in enumerate(games):
        st_txt.markdown(f"**⚙️ [{i+1}/{len(games)}]** {game['away_team']} @ {game['home_team']} — {game['league']}")
        results.append({**game,"sim":run_monte_carlo(game,n)})
        pb.progress((i+1)/len(games))
    pb.empty(); st_txt.empty()
    return results

# ── Auto Pick Report Generator ────────────────────────────────────────────────
def confidence_label(ev, dq):
    if ev >= 10 and dq >= 60: return "ALTA", "badge-green", "🟢"
    if ev >= 5  and dq >= 40: return "MEDIA","badge-yellow","🟡"
    return "BAJA","badge-red","🔴"

def edge_pct(prob_sim, ml):
    """How much our simulated prob beats the implied prob."""
    try:
        implied = ml_to_prob(float(str(ml).replace("+","")))
        return round((prob_sim - implied)*100, 1)
    except: return 0.0

def generate_report(sim_results):
    """Build a structured pick report from Monte Carlo results — no AI needed."""
    today = datetime.now(timezone.utc).strftime("%A %d %b %Y, %H:%M UTC")

    # Filter positive EV bets
    value_bets = []
    for r in sim_results:
        sim = r["sim"]; bb = sim.get("best_bet")
        if bb and bb["ev"] > 0:
            eg = edge_pct(bb["prob"], bb["ml"])
            value_bets.append({**r, "bb":bb, "edge":eg})

    value_bets.sort(key=lambda x: x["bb"]["ev"], reverse=True)

    # Also find best O/U
    best_ou = sorted(
        [r for r in sim_results if r["sim"].get("over_ev") and r["sim"]["over_ev"] > 3],
        key=lambda x: x["sim"]["over_ev"], reverse=True
    )

    lines = []
    lines.append(f'<div class="report-box">')
    lines.append(f'<div style="color:#555;font-size:0.8rem;margin-bottom:16px">📅 {today} · {len(sim_results)} partidos simulados · {sim_results[0]["sim"]["n_simulations"]:,} iteraciones/partido</div>')

    # ── BEST PICK ─────────────────────────────────────────────────────────
    if value_bets:
        top = value_bets[0]; bb = top["bb"]; sim = top["sim"]
        conf, badge_cls, emoji = confidence_label(bb["ev"], sim["data_quality"])
        implied_p = ml_to_prob(bb["ml"]) * 100 if bb["ml"] else 0
        lines.append(f'<div class="section-title">🥇 PICK PRINCIPAL</div>')
        lines.append(f"""
        <div class="sim-card-gold" style="margin:0">
          <div style="font-size:1.1rem;font-weight:700;color:#fff">{top['away_team']} @ {top['home_team']}</div>
          <div style="color:#888;font-size:0.8rem;margin-bottom:12px">{top['league']} · {top['status_detail']}</div>
          <div style="font-size:1.3rem;color:#FFD700;font-weight:700;margin-bottom:12px">► {bb['team']} ML {bb['ml']}</div>
          <div style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:12px">
            <div><div style="color:#888;font-size:0.7rem">PROB. SIMULADA</div><div style="font-size:1.4rem;font-weight:700;color:#4ade80">{bb['prob']*100:.1f}%</div></div>
            <div><div style="color:#888;font-size:0.7rem">PROB. IMPLÍCITA</div><div style="font-size:1.4rem;font-weight:700;color:#aaa">{implied_p:.1f}%</div></div>
            <div><div style="color:#888;font-size:0.7rem">EDGE</div><div style="font-size:1.4rem;font-weight:700;color:#60a5fa">+{top['edge']:.1f}%</div></div>
            <div><div style="color:#888;font-size:0.7rem">EV / $100</div><div style="font-size:1.4rem;font-weight:700;color:#FFD700">+{bb['ev']:.1f}</div></div>
            <div><div style="color:#888;font-size:0.7rem">KELLY 25%</div><div style="font-size:1.4rem;font-weight:700;color:#a78bfa">{bb['kelly']:.1%}</div></div>
            <div><div style="color:#888;font-size:0.7rem">CONFIANZA</div><div style="margin-top:4px"><span class="{badge_cls}">{emoji} {conf}</span></div></div>
          </div>
          <div style="font-size:0.85rem;color:#aaa;line-height:1.7">
            <b style="color:#E8E8E8">¿Por qué este pick?</b><br>
            • La simulación asigna <b style="color:#4ade80">{bb['prob']*100:.1f}%</b> de probabilidad de ganar vs. el <b style="color:#aaa">{implied_p:.1f}%</b> implícito en la cuota (<b>+{top['edge']:.1f}% de edge</b>)<br>
            • Con {sim['n_simulations']:,} iteraciones Monte Carlo, el Expected Value es de <b style="color:#FFD700">+${bb['ev']:.1f} por cada $100</b> apostados<br>
            • Kelly Criterion recomienda apostar el <b style="color:#a78bfa">{bb['kelly']:.1%}</b> del bankroll (fracción 25% conservadora)<br>
            • Calidad del dato: <b style="color:{"#4ade80" if sim["data_quality"]>=60 else "#fbbf24"}">{sim['data_quality']:.0f}%</b> {"— alta confianza en los inputs" if sim["data_quality"]>=60 else "— moderada (cuotas o récords incompletos)"}
          </div>
        </div>
        """)

        # ── VALUE BETS ADICIONALES ────────────────────────────────────────
        if len(value_bets) > 1:
            lines.append(f'<div class="section-title">🥈 VALUE BETS ADICIONALES ({len(value_bets)-1})</div>')
            for r in value_bets[1:6]:
                bb2 = r["bb"]; sim2 = r["sim"]
                conf2,badge2,em2 = confidence_label(bb2["ev"],sim2["data_quality"])
                impl2 = ml_to_prob(bb2["ml"])*100 if bb2["ml"] else 0
                lines.append(f"""
                <div class="sim-card">
                  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;align-items:flex-start">
                    <div>
                      <div style="font-weight:700">{r['away_team']} @ {r['home_team']}</div>
                      <div style="color:#555;font-size:0.8rem">{r['league']}</div>
                      <div style="color:#4ade80;font-weight:700;margin-top:4px">► {bb2['team']} ML {bb2['ml']}</div>
                    </div>
                    <div style="text-align:right">
                      <span class="{badge2}">{em2} {conf2}</span><br>
                      <span style="color:#FFD700;font-weight:700">EV +{bb2['ev']:.1f}</span>
                      <span style="color:#888;font-size:0.8rem"> / Edge +{r['edge']:.1f}%</span><br>
                      <span style="color:#aaa;font-size:0.8rem">{bb2['prob']*100:.1f}% sim vs {impl2:.1f}% impl · Kelly {bb2['kelly']:.1%}</span>
                    </div>
                  </div>
                </div>""")

        # ── BEST O/U ──────────────────────────────────────────────────────
        if best_ou:
            lines.append(f'<div class="section-title">📊 MEJOR OVER/UNDER</div>')
            br = best_ou[0]; bs = br["sim"]
            lines.append(f"""
            <div class="sim-card-mid">
              <div style="font-weight:700">{br['away_team']} @ {br['home_team']}</div>
              <div style="color:#555;font-size:0.8rem">{br['league']}</div>
              <div style="color:#fbbf24;font-weight:700;margin-top:4px">► OVER {bs['over_under']} (−110)</div>
              <div style="color:#aaa;font-size:0.85rem;margin-top:4px">EV estimado: <b style="color:#fbbf24">+{bs['over_ev']:.1f}</b> | DQ: {bs['data_quality']:.0f}%</div>
            </div>""")

    else:
        lines.append(f'<div class="section-title">⚠️ SIN VALUE BETS HOY</div>')
        lines.append(f'<p style="color:#888">La simulación no encontró apuestas con Expected Value positivo en los partidos disponibles. Considera ampliar las ligas seleccionadas o esperar a que las cuotas se actualicen.</p>')

    # ── EV NEGATIVO (evitar) ──────────────────────────────────────────────
    avoid = [r for r in sim_results if r["sim"].get("best_bet") and r["sim"]["best_bet"]["ev"] < -10]
    avoid.sort(key=lambda x: x["sim"]["best_bet"]["ev"])
    if avoid:
        lines.append(f'<div class="section-title">🚫 EVITAR — EV MUY NEGATIVO</div>')
        for r in avoid[:3]:
            bb3=r["sim"]["best_bet"]
            lines.append(f'<div style="color:#ef4444;font-size:0.85rem;padding:6px 0;border-bottom:1px solid #2a2a4a">✗ {r["away_team"]} @ {r["home_team"]} · {r["league"]} — EV {bb3["ev"]:.1f}</div>')

    # ── RESUMEN ───────────────────────────────────────────────────────────
    pos = len(value_bets)
    neg = len([r for r in sim_results if r["sim"].get("best_bet") and r["sim"]["best_bet"]["ev"] < 0])
    no_odds = len([r for r in sim_results if not r["sim"]["home_ml"]])
    lines.append(f'<div class="section-title">📈 RESUMEN DE SESIÓN</div>')
    lines.append(f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:8px">
      <div style="background:#1a4a1a;padding:8px 16px;border-radius:6px;text-align:center"><div style="font-size:1.4rem;font-weight:700;color:#4ade80">{pos}</div><div style="color:#888;font-size:0.75rem">VALUE BETS EV+</div></div>
      <div style="background:#3a0a0a;padding:8px 16px;border-radius:6px;text-align:center"><div style="font-size:1.4rem;font-weight:700;color:#ef4444">{neg}</div><div style="color:#888;font-size:0.75rem">EV NEGATIVO</div></div>
      <div style="background:#1A1A2E;padding:8px 16px;border-radius:6px;text-align:center"><div style="font-size:1.4rem;font-weight:700;color:#888">{no_odds}</div><div style="color:#888;font-size:0.75rem">SIN CUOTAS</div></div>
      <div style="background:#1A1A2E;padding:8px 16px;border-radius:6px;text-align:center"><div style="font-size:1.4rem;font-weight:700;color:#60a5fa">{len(sim_results):,}×{sim_results[0]["sim"]["n_simulations"]:,}</div><div style="color:#888;font-size:0.75rem">SIMULACIONES TOTAL</div></div>
    </div>
    <div style="color:#555;font-size:0.75rem;margin-top:8px">⚠️ Solo fines informativos. EV calculado contra cuotas ESPN BET. Apuesta con responsabilidad.</div>
    """)
    lines.append("</div>")
    return "\n".join(lines)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title">ESPN+</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Monte Carlo · 100% Gratis</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🎲 Simulación")
    n_sims = st.select_slider("Iteraciones Monte Carlo", options=[1_000,2_500,5_000,10_000,25_000], value=10_000)
    st.caption(f"⚡ ~{n_sims/1000:.0f}K sims/partido · ~{len([1])*n_sims/1_000_000:.2f}M total")
    st.divider()
    st.markdown("### 🏆 Ligas")
    groups = sorted(set(v["group"] for v in LEAGUES.values()))
    sel_groups = st.multiselect("Grupos", groups, default=["Basketball","Baseball","Soccer"])
    avail = [n for n,cfg in LEAGUES.items() if cfg["group"] in sel_groups]
    sel_leagues = st.multiselect("Ligas", avail, default=avail)
    st.divider()
    st.caption("📡 ESPN API pública · caché 5 min")
    st.caption("🎲 Monte Carlo + Beta dist.")
    st.caption("💰 Sin costo — sin API externa")
    if st.button("🔄 Limpiar caché"):
        st.cache_data.clear(); st.success("Caché limpiado")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🎯 Monte Carlo Pick Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">ESPN+ Data · 10,000 Simulations · Expected Value Engine · 100% Gratis</p>', unsafe_allow_html=True)
st.divider()

if not sel_leagues: st.warning("⚠️ Selecciona al menos una liga."); st.stop()

with st.spinner("📡 Cargando datos de ESPN..."):
    games = get_all_games(sel_leagues)
if not games: st.error("No se encontraron partidos."); st.stop()

live_g=[g for g in games if g["state"]=="in"]
pre_g =[g for g in games if g["state"]=="pre"]
odds_g=[g for g in games if g["odds"]]

c1,c2,c3,c4 = st.columns(4)
for col,num,label,color in [(c1,len(games),"Total Partidos","#D00000"),(c2,len(live_g),"En Vivo","#4ade80"),(c3,len(pre_g),"Próximos","#60a5fa"),(c4,len(odds_g),"Con Cuotas","#FFD700")]:
    col.markdown(f'<div class="metric-box"><div class="metric-num" style="color:{color}">{num}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

st.divider()
tab_report, tab_sim, tab_all = st.tabs(["🎯 Reporte de Picks", f"🎲 Simulaciones ({n_sims:,}x)", "📋 Partidos"])

# ── TAB REPORT ────────────────────────────────────────────────────────────────
with tab_report:
    sr = st.session_state.get("sim_results",[])
    if not sr:
        st.info("👈 Ve al tab **Simulaciones** y corre las simulaciones primero.")
        st.markdown("""
**¿Cómo funciona sin AI?**

El motor Monte Carlo calcula automáticamente:

- **Expected Value (EV)** — cuánto ganarías por $100 a largo plazo según la simulación vs. la cuota de la casa
- **Edge %** — diferencia entre probabilidad simulada e implícita de la cuota (vig-removed)
- **Kelly Criterion (25%)** — tamaño óptimo de apuesta como % del bankroll
- **Confianza** — basada en EV + calidad del dato disponible (cuotas, récords, ESPN win %)

El reporte se genera instantáneamente, sin ninguna API externa.
        """)
    else:
        if st.button("🔄 REGENERAR REPORTE", key="regen"):
            pass  # will re-render below
        report_html = generate_report(sr)
        st.markdown(report_html, unsafe_allow_html=True)

        # Text download
        pos_ev = [r for r in sr if r["sim"].get("best_bet") and r["sim"]["best_bet"]["ev"]>0]
        txt = [f"ESPN+ Monte Carlo Pick Analyzer — {datetime.now().strftime('%Y-%m-%d %H:%M')}", f"{len(sr)} partidos · {sr[0]['sim']['n_simulations']:,} sims/partido", "="*60]
        for r in pos_ev:
            bb=r["sim"]["best_bet"]; impl=ml_to_prob(bb["ml"])*100 if bb["ml"] else 0
            txt.append(f"\n[{r['league']}] {r['away_team']} @ {r['home_team']}")
            txt.append(f"  PICK: {bb['team']} ML {bb['ml']}")
            txt.append(f"  Prob simulada: {bb['prob']*100:.1f}% vs implícita: {impl:.1f}%")
            txt.append(f"  EV: +{bb['ev']:.1f} / $100 | Kelly: {bb['kelly']:.1%} | DQ: {r['sim']['data_quality']:.0f}%")
        st.download_button("💾 Descargar reporte TXT", data="\n".join(txt), file_name=f"picks_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain")

# ── TAB SIMULATIONS ───────────────────────────────────────────────────────────
with tab_sim:
    st.markdown(f"### {len(games)} partidos × {n_sims:,} iteraciones = **{len(games)*n_sims:,} simulaciones**")
    if st.button(f"🚀 CORRER {n_sims:,} SIMULACIONES", key="run_sim"):
        t0=time.time()
        sr2=run_all_simulations(games, n=n_sims)
        elapsed=time.time()-t0
        st.session_state["sim_results"]=sr2
        st.session_state["sim_time"]=datetime.now().strftime("%H:%M:%S")
        st.success(f"✅ {len(games)*n_sims:,} simulaciones en {elapsed:.1f}s · Ve al tab **Reporte de Picks**")

    sr = st.session_state.get("sim_results",[])
    if sr:
        sort_by = st.selectbox("Ordenar por",["Mejor EV","Mayor prob. local","Mayor prob. visitante","Calidad dato"])
        def sk(r):
            s=r["sim"]; bb=s.get("best_bet")
            if sort_by=="Mejor EV": return bb["ev"] if bb else -999
            if sort_by=="Mayor prob. local": return s["home_pct"]
            if sort_by=="Mayor prob. visitante": return s["away_pct"]
            return s["data_quality"]
        sorted_r=sorted(sr,key=sk,reverse=True)
        ev_filter=st.checkbox("Solo EV positivo",value=False)
        display=[r for r in sorted_r if not ev_filter or (r["sim"].get("best_bet") and r["sim"]["best_bet"]["ev"]>0)]

        for r in display:
            sim=r["sim"]; bb=sim.get("best_bet"); dq=sim["data_quality"]
            card="sim-card" if (bb and bb["ev"]>5) else "sim-card-red" if not(bb and bb["ev"]>0) else "game-card"
            def bar(pct,color,label): return f'<div style="margin:4px 0"><div style="display:flex;justify-content:space-between"><span style="font-size:0.8rem;color:#aaa">{label}</span><span style="font-size:0.8rem;font-weight:700;color:{color}">{pct:.1f}%</span></div><div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{min(pct,100):.1f}%;background:{color}"></div></div></div>'
            bars=bar(sim["away_pct"],"#60a5fa",r["away_team"])
            if sim["is_soccer"]: bars+=bar(sim["draw_pct"],"#a78bfa","Empate")
            bars+=bar(sim["home_pct"],"#f97316",r["home_team"])
            he=f'<span class="{"ev-pos" if sim["home_ev"] and sim["home_ev"]>0 else "ev-neg"}">{sim["home_ev"]:+.1f}</span>' if sim["home_ev"] is not None else "<span style='color:#555'>N/A</span>"
            ae=f'<span class="{"ev-pos" if sim["away_ev"] and sim["away_ev"]>0 else "ev-neg"}">{sim["away_ev"]:+.1f}</span>' if sim["away_ev"] is not None else "<span style='color:#555'>N/A</span>"
            badge=f'<span class="badge-green" style="margin-left:8px">EV +{bb["ev"]:.1f}</span>' if (bb and bb["ev"]>0) else ""
            dqc="#4ade80" if dq>=70 else "#fbbf24" if dq>=40 else "#ef4444"
            ou_html=f'<br><small style="color:#888">O/U {sim["over_under"]} → Over EV: <span style="color:{"#4ade80" if sim["over_ev"]>0 else "#ef4444"}">{sim["over_ev"]:+.1f}</span></small>' if sim.get("over_ev") is not None and sim.get("over_under") else ""
            st.markdown(f"""<div class="{card}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap">
                <div><strong>{r['away_team']} @ {r['home_team']}</strong>{badge}<br>
                <small style="color:#555">{r['league']} · {r['status_detail']} · <span style="color:{dqc}">DQ {dq:.0f}%</span></small></div>
                <div style="text-align:right;font-size:0.8rem">ML {sim['away_ml'] or 'N/A'} / {sim['home_ml'] or 'N/A'}<br>EV: {ae} / {he}</div>
              </div>
              <div style="margin-top:10px">{bars}</div>{ou_html}
            </div>""", unsafe_allow_html=True)

        # CSV
        st.divider()
        csv=["Liga,Visitante,Local,Prob Vis%,Prob Local%,Prob Empate%,ML Vis,ML Local,EV Vis,EV Local,Kelly Vis,Kelly Local,O/U,EV Over,DQ%,N Sims"]
        for r in sorted_r:
            s=r["sim"]
            csv.append(f"{r['league']},{r['away_team']},{r['home_team']},{s['away_pct']},{s['home_pct']},{s['draw_pct']},{s['away_ml']},{s['home_ml']},{s['away_ev'] or ''},{s['home_ev'] or ''},{s['away_kelly'] or ''},{s['home_kelly'] or ''},{s['over_under'] or ''},{s['over_ev'] or ''},{s['data_quality']},{s['n_simulations']}")
        st.download_button("💾 Descargar CSV", data="\n".join(csv), file_name=f"mc_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

# ── TAB ALL GAMES ─────────────────────────────────────────────────────────────
with tab_all:
    cf1,cf2=st.columns(2)
    with cf1: fs=st.multiselect("Estado",["pre","in","post"],default=["pre","in"],format_func=lambda x:{"pre":"🔵 Próximo","in":"🔴 En Vivo","post":"⚫ Final"}[x])
    with cf2: fl=st.multiselect("Liga",list(set(g["league"] for g in games)),default=list(set(g["league"] for g in games)))
    filtered=[g for g in games if g["state"] in fs and g["league"] in fl]
    st.caption(f"Mostrando {len(filtered)} de {len(games)} partidos")
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
        rh=f"<br><small style='color:#555'>{g['away_record'] or '?'} vs {g['home_record'] or '?'}</small>" if (g["away_record"] or g["home_record"]) else ""
        st.markdown(f"""<div class="game-card">
          <div style="display:flex;justify-content:space-between">
            <strong>{g['away_team']} @ {g['home_team']}{sh}</strong>
            <span class="{sc}">{si} {g['status_detail']}</span>
          </div>
          <small style="color:#555">{g['league']}</small>{rh}{oh}
        </div>""", unsafe_allow_html=True)

st.divider()
st.markdown('<div style="text-align:center;color:#444;font-size:0.75rem">ESPN+ Monte Carlo · 100% Gratis · Sin API externa · ⚠️ Solo fines informativos</div>', unsafe_allow_html=True)

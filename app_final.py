"""
THE GAMBLERS LAYER — FINAL
100% ESPN · Bot Telegram integrado · Sin BD local
"""
import streamlit as st
import requests, numpy as np, math, threading
from datetime import datetime, timedelta
import pytz

st.set_page_config(page_title="THE GAMBLERS LAYER 💎", page_icon="💎",
                   layout="wide", initial_sidebar_state="collapsed")

CDMX = pytz.timezone("America/Mexico_City")
ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer"
H    = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36","Accept":"application/json"}

# ── Bot Telegram ──────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()
# Streamlit Cloud usa st.secrets, local usa .env
try:
    BOT_TOKEN = st.secrets["BOT_TOKEN"]
    CHAT_ID   = st.secrets["CHAT_ID"]
except:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    CHAT_ID   = os.getenv("CHAT_ID", "")

LIGAS = {
    "eng.1":"Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿","eng.2":"Championship 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "esp.1":"La Liga 🇪🇸","esp.2":"Segunda 🇪🇸",
    "ger.1":"Bundesliga 🇩🇪","ger.2":"2. Bundesliga 🇩🇪",
    "ita.1":"Serie A 🇮🇹","fra.1":"Ligue 1 🇫🇷",
    "ned.1":"Eredivisie 🇳🇱","por.1":"Primeira Liga 🇵🇹",
    "mex.1":"Liga MX 🇲🇽","mex.2":"Expansión MX 🇲🇽",
    "usa.1":"MLS 🇺🇸","bra.1":"Brasileirão 🇧🇷",
    "arg.1":"Liga Argentina 🇦🇷","col.1":"Liga BetPlay 🇨🇴",
    "chi.1":"Primera División 🇨🇱","sau.1":"Saudi Pro League 🇸🇦",
    "tur.1":"Süper Lig 🇹🇷","sco.1":"Premiership 🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "uefa.champions":"Champions League 🏆","uefa.europa":"Europa League 🏆",
    "uefa.europa.conf":"Conference League 🏆",
    "den.1":"Superliga 🇩🇰","nor.1":"Eliteserien 🇳🇴",
    "bel.1":"Pro League 🇧🇪",
    "gre.1":"Super League 🇬🇷",
}

# ══════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Rajdhani:wght@700;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;color:#EEEEFF!important;background:#07071a!important}
.stApp{background:#07071a!important}
p,span,div,label,li,td,th,small,strong,em,b,h1,h2,h3,h4,
.stMarkdown *,[data-testid="stMarkdownContainer"] *,[data-testid="stText"] *,
.element-container *,.stRadio *{color:#EEEEFF!important}
.stButton>button{background:linear-gradient(135deg,#7c00ff,#00ccff)!important;color:#FFF!important;
  border:none!important;border-radius:12px!important;font-weight:700!important;
  padding:11px 24px!important;box-shadow:0 4px 20px #7c00ff44!important}
.stButton>button:hover{opacity:.85!important;transform:translateY(-2px)!important}
.stTabs [data-baseweb="tab"]{color:#666!important;font-weight:700!important;font-size:.9rem!important;padding:10px 14px!important}
.stTabs [aria-selected="true"]{color:#FFD700!important;border-bottom:3px solid #FFD700!important}
.streamlit-expanderHeader{background:#0d0d2e!important;border:1px solid #252555!important;
  border-radius:12px!important;padding:14px 20px!important;font-weight:700!important;color:#EEEEFF!important}
.streamlit-expanderContent{background:#0a0a26!important;border:1px solid #252555!important;
  border-top:none!important;border-radius:0 0 12px 12px!important}
.acard{background:#0d0d2e;border:1px solid #252555;border-radius:16px;padding:20px 24px;margin:10px 0}
.shdr{font-size:.8rem;font-weight:700;color:#FFD700!important;text-transform:uppercase;
  letter-spacing:.14em;margin:20px 0 10px;display:flex;align-items:center;gap:8px}
.shdr::after{content:'';flex:1;height:1px;background:#252555}
.mbox{background:#0d0d2e;border:1px solid #252555;border-radius:12px;padding:16px 12px;text-align:center}
.mval{font-size:1.8rem;font-weight:900;line-height:1.1}
.mlbl{font-size:.72rem;color:#666!important;margin-top:4px;text-transform:uppercase;letter-spacing:.06em}
.bw{background:#00ff8825;border:1px solid #00ff88;border-radius:6px;padding:3px 10px;font-size:.85rem;font-weight:700;color:#00ff88!important;margin:2px;display:inline-block}
.bd{background:#FFD70025;border:1px solid #FFD700;border-radius:6px;padding:3px 10px;font-size:.85rem;font-weight:700;color:#FFD700!important;margin:2px;display:inline-block}
.bl{background:#ff444425;border:1px solid #ff4444;border-radius:6px;padding:3px 10px;font-size:.85rem;font-weight:700;color:#ff4444!important;margin:2px;display:inline-block}
.diamond-hero{background:linear-gradient(135deg,#120030,#001a40,#1a1000);border:2px solid #FFD700;
  border-radius:22px;padding:30px 36px;margin:10px 0;position:relative;overflow:hidden}
.diamond-hero::before{content:'💎';position:absolute;right:24px;top:16px;font-size:5rem;opacity:.1}
.parlay-hero{background:linear-gradient(135deg,#001a2e,#001a10);border:2px solid #00ccff;border-radius:22px;padding:28px 32px;margin:10px 0}
.trilay-card{background:linear-gradient(135deg,#1a0030,#000e2e);border:2px solid #aa00ff;border-radius:18px;padding:20px 24px;margin:10px 0}
.pato-card{background:linear-gradient(135deg,#001a0e,#0a1a00);border:2px solid #39d353;border-radius:18px;padding:18px 22px;margin:8px 0;transition:.2s}
.pato-card:hover{border-color:#7fff00;transform:translateY(-2px)}
.pato-hero{background:linear-gradient(135deg,#001008,#050f00);border:2px solid #39d353;border-radius:22px;padding:26px 32px;margin-bottom:20px}
.mrow{background:#0d0d2e;border:1px solid #252555;border-radius:12px;padding:14px 18px;margin:5px 0}
.mrow:hover{background:#12123a;border-color:#7c00ff55}
.bot-card{background:linear-gradient(135deg,#001a2e,#0d0030);border:2px solid #229ED9;border-radius:18px;padding:20px 24px;margin:10px 0}
.pbar{height:8px;border-radius:4px;background:#1a1a40;overflow:hidden;margin-top:4px}
.hist-w{background:#00ff8815;border:1px solid #00ff8844;border-radius:10px;padding:10px 14px;margin:4px 0}
.hist-l{background:#ff444415;border:1px solid #ff444444;border-radius:10px;padding:10px 14px;margin:4px 0}
.hist-p{background:#FFD70015;border:1px solid #FFD70044;border-radius:10px;padding:10px 14px;margin:4px 0}
.conf-pill{border-radius:20px;padding:4px 12px;font-size:.78rem;font-weight:700;display:inline-block;margin:2px}
.stand-row{display:grid;grid-template-columns:28px 1fr 36px 36px 36px 36px 50px;gap:6px;
  align-items:center;padding:8px 4px;border-bottom:1px solid #151530;font-size:.85rem}
/* ── MOBILE ── */
@media(max-width:768px){
  .diamond-hero{padding:18px 16px!important}
  .diamond-hero::before{font-size:3rem!important;opacity:.06!important}
  .mval{font-size:1.4rem!important}
  .mlbl{font-size:.65rem!important}
  .mbox{padding:10px 6px!important}
  .acard{padding:14px 12px!important}
  .parlay-hero{padding:16px 14px!important}
  .trilay-card{padding:14px 12px!important}
  .pato-card{padding:12px 10px!important}
  .shdr{font-size:.72rem!important;letter-spacing:.08em!important}
  .stTabs [data-baseweb="tab"]{padding:8px 8px!important;font-size:.78rem!important}
  [data-testid="column"]{min-width:0!important}
  .stand-row{grid-template-columns:22px 1fr 28px 28px 28px 28px 42px!important;font-size:.75rem!important}
}
</style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ESPN HELPERS
# ══════════════════════════════════════════════════════════
def eg(url, params=None):
    try:
        r = requests.get(url, headers=H, params=params, timeout=12)
        return r.json() if r.status_code == 200 else {}
    except: return {}

def parse_score(s):
    if isinstance(s, dict): return int(float(s.get("value", 0) or 0))
    try: return int(float(s or 0))
    except: return 0

@st.cache_data(ttl=300, show_spinner=False)
def get_cartelera():
    now   = datetime.now(CDMX)
    # Pedimos hoy + 5 días en UTC para no perder partidos por diferencia horaria
    dates = [(now + timedelta(days=i)).strftime("%Y%m%d") for i in range(0, 6)]
    hoy   = now.strftime("%Y-%m-%d")  # desde hoy CDMX
    matches, seen = [], set()
    for slug in LIGAS:
        for ds in dates:
            data = eg(f"{ESPN}/{slug}/scoreboard", {"dates": ds, "limit": 100})
            for ev in data.get("events", []):
                eid = ev.get("id", "")
                if eid in seen: continue
                seen.add(eid)
                try:
                    comp  = ev["competitions"][0]
                    comps = comp["competitors"]
                    hc    = next(c for c in comps if c["homeAway"] == "home")
                    ac    = next(c for c in comps if c["homeAway"] == "away")
                    utc   = datetime.strptime(ev["date"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.UTC)
                    hora  = utc.astimezone(CDMX).strftime("%H:%M")
                    fecha = utc.astimezone(CDMX).strftime("%Y-%m-%d")
                    state = ev["status"]["type"]["state"]
                    # Solo partidos de hoy en adelante en hora CDMX
                    if fecha < hoy: continue
                    # Solo hasta lunes 9 Mar
                    if fecha > (now + timedelta(days=4)).strftime("%Y-%m-%d"): continue
                    odd_h = odd_a = odd_d = 0.0
                    try:
                        odds = comp.get("odds", [])
                        if odds:
                            o = odds[0]
                            def am2dec(v):
                                try:
                                    v = int(v)
                                    return round((v/100)+1, 2) if v > 0 else round((100/abs(v))+1, 2)
                                except: return 0.0
                            odd_h = am2dec(o.get("homeTeamOdds", {}).get("moneyLine", 0))
                            odd_a = am2dec(o.get("awayTeamOdds", {}).get("moneyLine", 0))
                            odd_d = am2dec(o.get("drawOdds", {}).get("moneyLine", 0))
                    except: pass
                    def get_record(c):
                        try: return c["records"][0]["summary"]
                        except: return "0-0-0"
                    matches.append({
                        "id":       eid,
                        "home":     hc["team"]["displayName"],
                        "away":     ac["team"]["displayName"],
                        "home_id":  str(hc["team"]["id"]),
                        "away_id":  str(ac["team"]["id"]),
                        "home_rec": get_record(hc),
                        "away_rec": get_record(ac),
                        "league":   LIGAS[slug],
                        "slug":     slug,
                        "hora":     hora,
                        "fecha":    fecha,
                        "state":    state,
                        "odd_h":    odd_h,
                        "odd_a":    odd_a,
                        "odd_d":    odd_d,
                        "score_h":  parse_score(hc.get("score", 0)),
                        "score_a":  parse_score(ac.get("score", 0)),
                    })
                except: continue
    return matches

@st.cache_data(ttl=1800, show_spinner=False)
def get_form(team_id, slug):
    """Últimos 10 partidos de un equipo desde ESPN schedule."""
    team_id = str(team_id)
    data    = eg(f"{ESPN}/{slug}/teams/{team_id}/schedule")
    events  = data.get("events", [])
    matches = []
    for ev in events:
        try:
            comp  = ev["competitions"][0]
            comps = comp["competitors"]
            state = ev.get("status", {}).get("type", {}).get("state", "")
            if state != "post": continue
            hc  = next(c for c in comps if c["homeAway"] == "home")
            ac  = next(c for c in comps if c["homeAway"] == "away")
            # ── es_home: el team_id aparece en home o away ──
            is_home = str(hc["team"]["id"]) == team_id
            my      = hc if is_home else ac
            opp     = ac if is_home else hc
            gf      = parse_score(my.get("score", 0))
            gc      = parse_score(opp.get("score", 0))
            result  = "W" if gf > gc else ("D" if gf == gc else "L")
            matches.append({
                "date":     ev.get("date", "")[:10],
                "result":   result,
                "gf":       gf,
                "gc":       gc,
                "opponent": opp["team"]["displayName"],
                "is_home":  is_home,
                "league":   ev.get("name", ""),
            })
        except: continue
    matches.sort(key=lambda x: x["date"], reverse=True)
    return matches[:10]

@st.cache_data(ttl=1800, show_spinner=False)
def get_h2h(home_id, away_id, slug, home_name, away_name):
    home_id = str(home_id); away_id = str(away_id)
    data    = eg(f"{ESPN}/{slug}/teams/{home_id}/schedule")
    h2h     = []
    for ev in data.get("events", []):
        try:
            comp  = ev["competitions"][0]
            comps = comp["competitors"]
            if ev.get("status", {}).get("type", {}).get("state") != "post": continue
            ids   = {str(c["team"]["id"]) for c in comps}
            if away_id not in ids: continue
            hc = next(c for c in comps if c["homeAway"] == "home")
            ac = next(c for c in comps if c["homeAway"] == "away")
            gh = parse_score(hc.get("score", 0))
            ga = parse_score(ac.get("score", 0))
            hn = hc["team"]["displayName"]; an = ac["team"]["displayName"]
            win = home_name if gh > ga else (away_name if ga > gh else "Draw")
            h2h.append({"home":hn,"away":an,"gh":gh,"ga":ga,
                        "winner":win,"date":ev.get("date","")[:10],"total":gh+ga})
        except: continue
    h2h.sort(key=lambda x: x["date"], reverse=True)
    return h2h[:10]

@st.cache_data(ttl=3600, show_spinner=False)
def get_standings(slug):
    """Tabla de posiciones desde ESPN."""
    data = eg(f"{ESPN}/{slug}/standings")
    rows = []
    try:
        for group in data.get("standings", {}).get("entries", []):
            t = group.get("team", {})
            stats = {s["name"]: s.get("displayValue","?") for s in group.get("stats",[])}
            rows.append({
                "pos":   stats.get("rank", group.get("rank","?")),
                "team":  t.get("displayName","?"),
                "tid":   str(t.get("id","")),
                "pj":    stats.get("gamesPlayed","?"),
                "pts":   stats.get("points","?"),
                "gf":    stats.get("pointsFor","?"),
                "gc":    stats.get("pointsAgainst","?"),
                "dif":   stats.get("pointDifferential","?"),
                "forma": stats.get("streak",""),
            })
    except: pass
    return rows

# ══════════════════════════════════════════════════════════
# HISTORIAL DE PICKS (session state)
# ══════════════════════════════════════════════════════════
def init_history():
    if "pick_history" not in st.session_state:
        st.session_state["pick_history"] = []

def add_pick(match, pick_label, prob, odd):
    init_history()
    st.session_state["pick_history"].append({
        "date":   datetime.now(CDMX).strftime("%d/%m %H:%M"),
        "home":   match["home"],
        "away":   match["away"],
        "league": match["league"],
        "pick":   pick_label,
        "prob":   prob,
        "odd":    odd,
        "result": "⏳",  # pendiente
    })

def render_history():
    init_history()
    h = st.session_state["pick_history"]
    if not h:
        st.markdown("<div style='color:#555;padding:16px'>No has guardado picks aún. Abre un partido y haz click en '💾 Guardar Pick'.</div>", unsafe_allow_html=True)
        return
    wins   = sum(1 for x in h if x["result"]=="✅")
    losses = sum(1 for x in h if x["result"]=="❌")
    pend   = sum(1 for x in h if x["result"]=="⏳")
    total  = wins+losses
    pct    = round(wins/total*100) if total>0 else 0
    # Stats header
    st.markdown(
        f"<div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px'>"
        f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ff88'>{wins}</div><div class='mlbl'>Ganados ✅</div></div>"
        f"<div class='mbox' style='flex:1'><div class='mval' style='color:#ff4444'>{losses}</div><div class='mlbl'>Perdidos ❌</div></div>"
        f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{pend}</div><div class='mlbl'>Pendientes ⏳</div></div>"
        f"<div class='mbox' style='flex:1'><div class='mval' style='color:#7c00ff'>{pct}%</div><div class='mlbl'>% Acierto</div></div>"
        f"</div>", unsafe_allow_html=True)
    for i, p in enumerate(reversed(h)):
        css = "hist-w" if p["result"]=="✅" else ("hist-l" if p["result"]=="❌" else "hist-p")
        ri  = len(h)-1-i
        c1, c2, c3 = st.columns([4,2,2])
        with c1:
            st.markdown(
                f"<div class='{css}'>"
                f"<div style='font-weight:700;font-size:.9rem'>{p['pick']}</div>"
                f"<div style='color:#555;font-size:.78rem'>{p['home']} vs {p['away']} · {p['league']}</div>"
                f"<div style='color:#555;font-size:.75rem'>{p['date']} · {p['prob']*100:.0f}% · @{p['odd'] if p['odd']>1 else 'N/A'}</div>"
                f"</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='padding-top:10px;font-size:1.5rem;text-align:center'>{p['result']}</div>", unsafe_allow_html=True)
        with c3:
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("✅", key=f"hw_{ri}", help="Ganó"):
                    st.session_state["pick_history"][ri]["result"] = "✅"; st.rerun()
            with cc2:
                if st.button("❌", key=f"hl_{ri}", help="Perdió"):
                    st.session_state["pick_history"][ri]["result"] = "❌"; st.rerun()
    if st.button("🗑️ Limpiar historial", key="clear_hist"):
        st.session_state["pick_history"] = []; st.rerun()


def avg(lst): return sum(lst)/len(lst) if lst else 0.0

def xg_from_record(record_str, is_home):
    """xG desde récord W-D-L cuando no hay historial de partidos."""
    try:
        w, d, l = map(int, record_str.split("-"))
        n = w + d + l
        if n > 0: return max(0.35, 0.7 + (w/n)*1.6 + (0.15 if is_home else 0))
    except: pass
    return 1.3 if is_home else 1.0

def mc50k(hxg, axg, N=50_000):
    rng = np.random.default_rng(42)
    hg  = rng.poisson(max(0.3, hxg), N)
    ag  = rng.poisson(max(0.3, axg), N)
    return {
        "ph":   float((hg>ag).mean()),  "pd":  float((hg==ag).mean()),
        "pa":   float((ag>hg).mean()),  "o15": float(((hg+ag)>1).mean()),
        "o25":  float(((hg+ag)>2).mean()), "o35": float(((hg+ag)>3).mean()),
        "btts": float(((hg>0)&(ag>0)).mean()),
        "cs_h": float((ag==0).mean()),  "cs_a": float((hg==0).mean()),
        "hxg":  round(hxg,2),           "axg":  round(axg,2),
    }

def poisson_u45(lh, la):
    p = 0.0
    for gh in range(6):
        for ga in range(6):
            if gh+ga > 4: continue
            p += (math.exp(-lh)*lh**gh/math.factorial(gh))*(math.exp(-la)*la**ga/math.factorial(ga))
    return min(p, 1.0)

def h2h_stats(h2h, hn, an):
    if not h2h: return {}
    tot  = len(h2h)
    hw   = sum(1 for x in h2h if x["winner"]==hn)
    aw   = sum(1 for x in h2h if x["winner"]==an)
    dw   = tot-hw-aw
    avg_g= sum(x["total"] for x in h2h)/tot
    o25  = sum(1 for x in h2h if x["total"]>2)
    btts = sum(1 for x in h2h if x["gh"]>0 and x["ga"]>0)
    l5   = h2h[:5]
    return {"tot":tot,"hw":hw,"aw":aw,"dw":dw,
            "hp":round(hw/tot*100),"dp":round(dw/tot*100),"ap":round(aw/tot*100),
            "avg_g":round(avg_g,2),"o25p":round(o25/tot*100),"bttsp":round(btts/tot*100),
            "l5h":sum(1 for x in l5 if x["winner"]==hn),
            "l5d":sum(1 for x in l5 if x["winner"]=="Draw"),
            "l5a":sum(1 for x in l5 if x["winner"]==an)}

def diamond_engine(mc, h2h_s, hform, aform):
    ph, pd, pa = mc["ph"], mc["pd"], mc["pa"]
    if h2h_s.get("tot",0) >= 3:
        ph = 0.75*ph + 0.25*(h2h_s["hp"]/100)
        pd = 0.75*pd + 0.25*(h2h_s["dp"]/100)
        pa = 0.75*pa + 0.25*(h2h_s["ap"]/100)
    def pts(f): return sum(3 if r["result"]=="W" else(1 if r["result"]=="D" else 0) for r in f[:5])
    hp5 = pts(hform); ap5 = pts(aform); tot = max(hp5+ap5,1)
    ph  = 0.82*ph + 0.18*(hp5/tot)
    pa  = 0.82*pa + 0.18*(ap5/tot)
    s   = ph+pd+pa
    if s > 0: ph/=s; pd/=s; pa/=s
    top = max(ph,pd,pa)
    if top >= 0.55:   conf,cc = "💎 DIAMANTE","#FFD700"
    elif top >= 0.46: conf,cc = "🔥 ALTA","#00ff88"
    elif top >= 0.37: conf,cc = "⚡ MEDIA","#00aaff"
    else:             conf,cc = "⚠️ BAJA","#ff9500"
    return {"ph":ph,"pd":pd,"pa":pa,"conf":conf,"cc":cc,"top":top}

def smart_parlay(mc, dp, hn, an):
    T=0.58
    leg1=[]
    if dp["ph"]>=T: leg1.append({"l":f"🏠 {hn[:13]} gana","p":dp["ph"]})
    if dp["pa"]>=T: leg1.append({"l":f"✈️ {an[:13]} gana","p":dp["pa"]})
    if not leg1:
        if dp["ph"]+dp["pd"]>=T: leg1.append({"l":f"🏠 {hn[:11]} o Empate","p":dp["ph"]+dp["pd"]})
        if dp["pa"]+dp["pd"]>=T: leg1.append({"l":f"✈️ {an[:11]} o Empate","p":dp["pa"]+dp["pd"]})
    leg1.sort(key=lambda x:-x["p"])
    leg2=[]
    if mc["o25"]>=T:  leg2.append({"l":"⚽ Over 2.5","p":mc["o25"]})
    if mc["btts"]>=T: leg2.append({"l":"⚡ Ambos Anotan","p":mc["btts"]})
    if mc["o35"]>=T:  leg2.append({"l":"⚽ Over 3.5","p":mc["o35"]})
    if not leg2:      leg2.append({"l":"⚽ Over 1.5","p":mc["o15"]})
    leg2.sort(key=lambda x:-x["p"])
    out=[]
    for l1 in leg1[:2]:
        for l2 in leg2[:2]:
            cp=l1["p"]*l2["p"]
            out.append({"l1":l1["l"],"p1":l1["p"],"l2":l2["l"],"p2":l2["p"],
                        "cp":cp,"odds":round(1/cp,2) if cp>0 else 99})
    if not out:
        for l2 in leg2[:2]:
            out.append({"l1":"","p1":0,"l2":l2["l"],"p2":l2["p"],
                        "cp":l2["p"],"odds":round(1/l2["p"],2)})
    out.sort(key=lambda x:-x["cp"])
    return out[:3]

def badges(form):
    return "".join(
        f"<span class='{'bw' if r['result']=='W' else ('bd' if r['result']=='D' else 'bl')}'>{r['result']}</span>"
        for r in form[:10]
    ) if form else "<span style='color:#555'>Sin datos</span>"

def days_since(form):
    if not form: return 99
    try: return (datetime.now()-datetime.strptime(form[0]["date"],"%Y-%m-%d")).days
    except: return 99

def cmprow(label, hv, av, fmt="{:.2f}", suf=""):
    hv=hv or 0; av=av or 0
    hc="#00ff88" if hv>=av else "#ff4444"; ac="#00ff88" if av>=hv else "#ff4444"
    hw=min(int(hv/(max(hv,av,0.01))*100),100); aw=min(int(av/(max(hv,av,0.01))*100),100)
    return (f"<div style='display:grid;grid-template-columns:1fr 200px 1fr;gap:8px;"
            f"align-items:center;padding:10px 0;border-bottom:1px solid #151530'>"
            f"<div style='text-align:right'><span style='color:{hc};font-weight:700;font-size:1.05rem'>"
            f"{fmt.format(hv)}{suf}</span>"
            f"<div class='pbar'><div style='width:{hw}%;height:100%;background:{hc};border-radius:4px'></div></div></div>"
            f"<div style='text-align:center;color:#555;font-size:.82rem'>{label}</div>"
            f"<div><span style='color:{ac};font-weight:700;font-size:1.05rem'>{fmt.format(av)}{suf}</span>"
            f"<div class='pbar'><div style='width:{aw}%;height:100%;background:{ac};border-radius:4px'></div></div></div>"
            f"</div>")

# ══════════════════════════════════════════════════════════
# TELEGRAM
# ══════════════════════════════════════════════════════════
def tg_send(msg):
    if BOT_TOKEN == "Pega_Aqui_Tu_Token_De_BotFather": return False
    try:
        r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          json={"chat_id":CHAT_ID,"text":msg,"parse_mode":"Markdown"},timeout=10)
        return r.ok
    except: return False

def escanear_y_enviar(matches):
    """Escanea todos los partidos y manda picks con edge > 8% a Telegram."""
    picks = []
    for m in matches:
        if m["state"] != "pre": continue
        hf  = get_form(m["home_id"], m["slug"])
        af  = get_form(m["away_id"], m["slug"])
        hxg = max(0.35, avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
        axg = max(0.35, avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
        mc  = mc50k(hxg, axg)
        h2h = get_h2h(m["home_id"],m["away_id"],m["slug"],m["home"],m["away"])
        h2s = h2h_stats(h2h, m["home"], m["away"])
        dp  = diamond_engine(mc, h2s, hf, af)
        odd_h = m["odd_h"]
        if odd_h > 1:
            edge = dp["ph"] - (1/odd_h)
            if edge >= 0.08 and dp["ph"] >= 0.45:
                b = odd_h - 1; p = dp["ph"]
                kelly = max(0, (b*p-(1-p))/b*100)
                picks.append({**m,"dp":dp,"mc":mc,"edge":edge,"kelly":kelly})

    if not picks:
        tg_send("🛡️ *Escáner Diario:* No hay picks con Edge > 8% hoy. Mantén el dinero en la bolsa.")
        return 0

    msg  = "🦅 *THE GAMBLERS LAYER | ESCÁNER DIARIO* 🦅\n"
    msg += f"_{datetime.now(CDMX).strftime('%d/%m/%Y')} — {len(picks)} picks_\n\n"
    for p in sorted(picks, key=lambda x:-x["edge"]):
        msg += f"🚨 *SHARP ALERT:* {p['league']}\n"
        msg += f"⚽ {p['home']} vs {p['away']}\n"
        msg += f"🕒 {p['hora']} CDMX\n"
        msg += f"👉 *Local gana @{p['odd_h']}*\n"
        msg += f"📊 Prob: {p['dp']['ph']*100:.1f}%  •  Edge: *{p['edge']*100:.1f}%*\n"
        msg += f"💰 Kelly: {p['kelly']:.1f}% bankroll\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "\n_Que la varianza esté a nuestro favor._ 🎲"
    tg_send(msg)
    return len(picks)

# ══════════════════════════════════════════════════════════
# TRILAY / PATO
# ══════════════════════════════════════════════════════════
@st.cache_data(ttl=600, show_spinner=False)
def compute_trilay(matches):
    cands=[]
    for m in matches[:40]:
        hf  = get_form(m["home_id"],m["slug"])
        af  = get_form(m["away_id"],m["slug"])
        hxg = max(0.35,avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
        axg = max(0.35,avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
        mc  = mc50k(hxg,axg)
        bp  = max(mc["btts"],mc["o25"])
        bm  = "AA (BTTS)" if mc["btts"]>=mc["o25"] else "Over 2.5"
        cands.append({**m,"mc":mc,"best_p":bp,"best_m":bm,"hxg":hxg,"axg":axg})
    cands.sort(key=lambda x:-x["best_p"])
    return cands[:3]

@st.cache_data(ttl=600, show_spinner=False)
def compute_pato(matches):
    cands=[]
    for m in matches[:80]:
        hf  = get_form(m["home_id"],m["slug"])
        af  = get_form(m["away_id"],m["slug"])
        hxg = max(0.2,avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
        axg = max(0.2,avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
        u45 = poisson_u45(hxg,axg)*100
        h_gc= avg([r["gc"] for r in hf]) if hf else 1.2
        a_gc= avg([r["gc"] for r in af]) if af else 1.2
        cands.append({**m,"hxg":round(hxg,2),"axg":round(axg,2),"u45":round(u45,1),
                      "total_avg":round(hxg+axg,2),"h_gc":round(h_gc,2),"a_gc":round(a_gc,2)})
    cands.sort(key=lambda x:-x["u45"])
    return cands

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
for k,v in [("view","cartelera"),("sel",None)]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;padding:24px 0 8px'>
  <div style='font-family:Rajdhani,sans-serif;font-size:2.8rem;font-weight:900;
    background:linear-gradient(135deg,#7c00ff,#00ccff,#FFD700);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:.06em'>
    THE GAMBLERS LAYER
  </div>
  <div style='color:#333!important;font-size:.8rem;letter-spacing:.15em;margin-top:4px'>
    PICKS · PARLAY · TRILAY · PATO · TELEGRAM BOT
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# CARGAR PARTIDOS
# ══════════════════════════════════════════════════════════
with st.spinner("Cargando cartelera..."):
    all_matches = get_cartelera()

if not all_matches:
    st.warning("No hay partidos disponibles.")
    st.stop()

liga_opts = ["Todas"] + sorted(set(m["league"] for m in all_matches))
liga_sel  = st.selectbox("Liga", liga_opts, label_visibility="collapsed")
matches   = all_matches if liga_sel=="Todas" else [m for m in all_matches if m["league"]==liga_sel]

# ══════════════════════════════════════════════════════════
# CARTELERA
# ══════════════════════════════════════════════════════════
if st.session_state["view"] == "cartelera":

    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial"])

    # ─── TAB CARTELERA ───────────────────────────────────
    with tab1:
        fc1, fc2 = st.columns([3,1])
        with fc1:
            conf_fil = st.selectbox("Filtro", ["Todos","💎 Solo Diamante","🔥 Alta o más","⚡ Media o más"],
                                    label_visibility="collapsed", key="conf_filter")
        with fc2:
            st.markdown(f"<div style='color:#555;font-size:.82rem;padding:10px 0;text-align:right'>{len(matches)} partidos</div>",unsafe_allow_html=True)

        from collections import defaultdict
        fecha_liga = defaultdict(lambda: defaultdict(list))
        now_str = datetime.now(CDMX)
        def fecha_label(f):
            try:
                d = datetime.strptime(f, "%Y-%m-%d")
                dias  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                meses = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                return f"📅 {dias[d.weekday()]} {d.day} {meses[d.month]}"
            except: return f"📅 {f}"
        for m in matches:
            fecha_liga[m["fecha"]][m["league"]].append(m)
        for fecha in sorted(fecha_liga.keys()):
            st.markdown(f"<div style='font-size:1rem;font-weight:900;color:#FFD700;margin:20px 0 10px;"
                        f"padding:8px 0;border-bottom:2px solid #252555'>{fecha_label(fecha)}</div>",unsafe_allow_html=True)
            for liga in sorted(fecha_liga[fecha].keys()):
                liga_matches = []
                for m in fecha_liga[fecha][liga]:
                    if conf_fil != "Todos" and m["state"] == "pre":
                        hf  = get_form(m["home_id"], m["slug"])
                        af  = get_form(m["away_id"], m["slug"])
                        hxg = max(0.35, avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
                        axg = max(0.35, avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
                        dp_ = diamond_engine(mc50k(hxg,axg), {}, hf, af)
                        conf = dp_["conf"]
                        if conf_fil == "💎 Solo Diamante" and "DIAMANTE" not in conf: continue
                        if conf_fil == "🔥 Alta o más" and conf not in ["💎 DIAMANTE","🔥 ALTA"]: continue
                        if conf_fil == "⚡ Media o más" and "BAJA" in conf: continue
                        m = {**m, "_conf": conf}
                    liga_matches.append(m)
                if not liga_matches: continue
                st.markdown(f"<div class='shdr'>{liga}</div>", unsafe_allow_html=True)
                for m in liga_matches:
                    live = m["state"] == "in"
                    sc   = f"{m['score_h']}-{m['score_a']}" if live else m["hora"]
                    conf_tag = f" · {m.get('_conf','')}" if m.get("_conf") else ""
                    lbl = f"{'🔴 ' if live else ''}{m['home']}  vs  {m['away']}   ·   {sc}{conf_tag}"
                    if st.button(lbl, key=f"b_{m['id']}", use_container_width=True):
                        st.session_state["sel"]  = m
                        st.session_state["view"] = "analisis"
                        st.rerun()

    # ─── TAB TRILAY ──────────────────────────────────────
    with tab2:
        st.markdown("<div class='shdr'>🎰 TRILAY — Top 3 para BTTS / Over 2.5</div>",unsafe_allow_html=True)
        with st.spinner("Calculando..."):
            trilay = compute_trilay(matches)
        if trilay:
            pc = 1.0
            for t in trilay: pc *= t["best_p"]
            st.markdown(
                f"<div class='trilay-card'>"
                f"<div style='font-size:.8rem;color:#aa00ff;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>✦ TRILAY DEL DÍA</div>"
                f"<div style='display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px'>"
                f"<div class='mbox' style='flex:1'><div class='mval' style='color:#aa00ff'>{pc*100:.1f}%</div><div class='mlbl'>Prob. Combinada</div></div>"
                f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{1/pc:.2f}x</div><div class='mlbl'>Cuota estimada</div></div>"
                f"</div>",unsafe_allow_html=True)
            for i,t in enumerate(trilay,1):
                st.markdown(
                    f"<div style='padding:10px 0;border-bottom:1px solid #1a1a40'>"
                    f"<div style='font-weight:700'>{i}. {t['home']} vs {t['away']}</div>"
                    f"<div style='color:#555;font-size:.82rem'>{t['league']} · {t['hora']}</div>"
                    f"<div style='margin-top:6px'><span style='color:#aa00ff;font-weight:700'>👉 {t['best_m']}</span>"
                    f"<span style='color:#666;margin-left:12px'>{t['best_p']*100:.1f}% · xG {t['hxg']:.1f}-{t['axg']:.1f}</span>"
                    f"</div></div>",unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)

    # ─── TAB PATO ────────────────────────────────────────
    with tab3:
        st.markdown("<div class='shdr'>🦆 PATO — Mejores Under 4.5</div>",unsafe_allow_html=True)
        with st.spinner("Calculando..."):
            pato = compute_pato(matches)
        umbral = st.slider("Umbral mínimo U4.5 %",60,95,75,5,key="pslider")
        fil    = [p for p in pato if p["u45"]>=umbral]
        if not fil:
            st.info(f"No hay partidos con U4.5 ≥ {umbral}%")
        else:
            st.markdown(
                f"<div class='pato-hero'>"
                f"<div style='font-size:.8rem;color:#39d353;font-weight:700;letter-spacing:.1em;margin-bottom:8px'>🦆 PATO DEL DÍA</div>"
                f"<div style='font-size:1.1rem;font-weight:700'>{fil[0]['home']} vs {fil[0]['away']}</div>"
                f"<div style='font-size:.85rem;color:#555;margin:4px 0'>{fil[0]['league']}</div>"
                f"<div style='margin-top:10px'><span style='background:#39d35322;border:1.5px solid #39d353;"
                f"border-radius:20px;padding:6px 16px;font-size:1.1rem;font-weight:900;color:#39d353!important'>"
                f"U4.5: {fil[0]['u45']:.1f}%</span></div></div>",unsafe_allow_html=True)
            for p in fil:
                uc = "#39d353" if p["u45"]>=85 else ("#00ff88" if p["u45"]>=75 else "#FFD700")
                st.markdown(
                    f"<div class='pato-card'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<div><div style='font-weight:700'>{p['home']} vs {p['away']}</div>"
                    f"<div style='color:#555;font-size:.82rem'>{p['league']} · {p['hora']}</div>"
                    f"<div style='margin-top:6px;font-size:.82rem'>xG: {p['hxg']}–{p['axg']} · GC prom: {p['h_gc']}–{p['a_gc']}</div></div>"
                    f"<div style='text-align:right'><div style='color:{uc};font-size:1.6rem;font-weight:900'>{p['u45']:.1f}%</div>"
                    f"<div style='font-size:.75rem;color:#555'>U4.5</div></div></div></div>",unsafe_allow_html=True)

    # ─── TAB PICKS ───────────────────────────────────────
    with tab4:
        st.markdown("<div class='shdr'>🎯 Mejores Picks del Día</div>",unsafe_allow_html=True)
        with st.spinner("Calculando picks..."):
            picks=[]
            for m in matches[:50]:
                if m["state"]!="pre": continue
                hf  = get_form(m["home_id"],m["slug"])
                af  = get_form(m["away_id"],m["slug"])
                hxg = max(0.35,avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
                axg = max(0.35,avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
                mc  = mc50k(hxg,axg)
                h2h = get_h2h(m["home_id"],m["away_id"],m["slug"],m["home"],m["away"])
                h2s = h2h_stats(h2h,m["home"],m["away"])
                dp  = diamond_engine(mc,h2s,hf,af)
                # Mejor pick del partido
                opts=[]
                if m["odd_h"]>1: opts.append(("🏠 "+m["home"][:15]+" gana",dp["ph"],m["odd_h"],dp["ph"]-(1/m["odd_h"])))
                if m["odd_a"]>1: opts.append(("✈️ "+m["away"][:15]+" gana",dp["pa"],m["odd_a"],dp["pa"]-(1/m["odd_a"])))
                opts.append(("⚽ Over 2.5",mc["o25"],0,mc["o25"]-0.50))
                opts.append(("⚡ Ambos Anotan",mc["btts"],0,mc["btts"]-0.50))
                opts.sort(key=lambda x:-x[3])
                best=opts[0]
                if best[3]>0.03:
                    picks.append({**m,"pick":best[0],"prob":best[1],"odd":best[2],"edge":best[3],"conf":dp["conf"]})
        picks.sort(key=lambda x:-x["prob"])
        if not picks:
            st.info("No se encontraron picks con valor hoy.")
        for p in picks[:15]:
            os_=f"@{p['odd']}" if p["odd"]>1 else ""
            st.markdown(
                f"<div class='mrow' style='display:flex;justify-content:space-between;align-items:center'>"
                f"<div><div style='font-weight:700'>{p['home']} vs {p['away']}</div>"
                f"<div style='color:#555;font-size:.82rem'>{p['league']} · {p['hora']}</div>"
                f"<div style='margin-top:4px;color:#00ccff;font-weight:700'>{p['pick']} {os_}</div></div>"
                f"<div style='text-align:right'>"
                f"<div style='font-size:1.4rem;font-weight:900;color:#FFD700'>{p['prob']*100:.1f}%</div>"
                f"<div style='font-size:.75rem;color:#555'>{p['conf']}</div></div></div>",
                unsafe_allow_html=True)

    # ─── TAB BOT TELEGRAM ────────────────────────────────
    with tab5:
        bot_ok = bool(BOT_TOKEN and CHAT_ID)
        st.markdown(
            f"<div class='bot-card'>"
            f"<div style='font-size:.8rem;color:#229ED9;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>🤖 BOT TELEGRAM</div>"
            f"<div style='font-size:1.1rem;font-weight:700;margin-bottom:6px'>The Gamblers Layer Bot</div>"
            f"<div style='color:#555;font-size:.85rem'>Estado: {'✅ Configurado' if bot_ok else '⚠️ Sin configurar — edita BOT_TOKEN y CHAT_ID en el código'}</div>"
            f"</div>",unsafe_allow_html=True)
        if bot_ok:
            col1,col2 = st.columns(2)
            with col1:
                if st.button("📡 Enviar Escáner Ahora", use_container_width=True):
                    with st.spinner("Escaneando y enviando..."):
                        n = escanear_y_enviar(all_matches)
                    st.success(f"✅ Enviado. {n} picks encontrados.")
            with col2:
                if st.button("🧪 Test — Enviar Mensaje de Prueba", use_container_width=True):
                    ok = tg_send("🦅 *The Gamblers Layer* — Test de conexión exitoso ✅")
                    st.success("✅ Mensaje enviado.") if ok else st.error("❌ Error. Verifica token y chat_id.")

            st.markdown("<div class='shdr'>Envío Automático</div>",unsafe_allow_html=True)
            st.info("El bot ya está programado en PythonAnywhere para correr todos los días a las 13:00 UTC. "
                    "Usa el botón de arriba para un escaneo manual en cualquier momento.")

            st.markdown("<div class='shdr'>Últimos picks enviados</div>",unsafe_allow_html=True)
            with st.spinner("Calculando picks para preview..."):
                preview=[]
                for m in all_matches[:30]:
                    if m["state"]!="pre": continue
                    hf  = get_form(m["home_id"],m["slug"])
                    af  = get_form(m["away_id"],m["slug"])
                    hxg = max(0.35,avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
                    axg = max(0.35,avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
                    mc  = mc50k(hxg,axg)
                    h2s = h2h_stats(get_h2h(m["home_id"],m["away_id"],m["slug"],m["home"],m["away"]),m["home"],m["away"])
                    dp  = diamond_engine(mc,h2s,hf,af)
                    if m["odd_h"]>1:
                        edge=dp["ph"]-(1/m["odd_h"])
                        if edge>=0.08 and dp["ph"]>=0.45:
                            preview.append({**m,"dp":dp,"edge":edge})
                preview.sort(key=lambda x:-x["edge"])
            if not preview:
                st.markdown("<div style='color:#555;padding:10px'>No hay picks con edge>8% en la cartelera actual.</div>",unsafe_allow_html=True)
            for p in preview[:5]:
                st.markdown(
                    f"<div class='mrow' style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<div><div style='font-weight:700'>🚨 {p['home']} vs {p['away']}</div>"
                    f"<div style='color:#555;font-size:.82rem'>{p['league']} · {p['hora']}</div>"
                    f"<div style='margin-top:4px;color:#00ccff'>Local gana @{p['odd_h']} · Edge: {p['edge']*100:.1f}%</div></div>"
                    f"<div style='text-align:right'><div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{p['dp']['ph']*100:.1f}%</div>"
                    f"<div style='font-size:.75rem;color:#555'>{p['dp']['conf']}</div></div></div>",
                    unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#0d0d2e;border-radius:12px;padding:20px;margin-top:10px;color:#666'>
            <b>Cómo configurar el bot:</b><br><br>
            1. Abre el archivo <code>app_final.py</code><br>
            2. Cambia <code>BOT_TOKEN</code> por el token que te dio BotFather<br>
            3. Cambia <code>CHAT_ID</code> por tu chat ID<br>
            4. Reinicia la app
            </div>""",unsafe_allow_html=True)

    # ─── TAB HISTORIAL ───────────────────────────────────
    with tab6:
        st.markdown("<div class='shdr'>📋 Historial de Picks</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:#555;font-size:.82rem;margin-bottom:12px'>Abre un partido → click en 💾 Guardar Pick → marca ✅ o ❌ cuando termine</div>", unsafe_allow_html=True)
        render_history()

# ══════════════════════════════════════════════════════════
# ANÁLISIS
# ══════════════════════════════════════════════════════════
else:
    g = st.session_state["sel"]
    if st.button("← Volver"):
        st.session_state["view"]="cartelera"; st.session_state["sel"]=None; st.rerun()

    st.markdown(
        f"<div style='text-align:center;padding:16px 0 4px'>"
        f"<div style='font-size:.8rem;color:#555;letter-spacing:.1em'>{g['league']}</div>"
        f"<div style='font-size:2rem;font-weight:900;margin:6px 0'>{g['home']} <span style='color:#333'>vs</span> {g['away']}</div>"
        f"<div style='color:#555;font-size:.9rem'>🕒 {g['hora']} CDMX</div></div>",unsafe_allow_html=True)

    prog = st.progress(0,"📊 Cargando datos ESPN...")
    hform = get_form(g["home_id"],g["slug"]); prog.progress(30,f"📊 {g['away']}...")
    aform = get_form(g["away_id"],g["slug"]); prog.progress(60,"⚔️ H2H...")
    h2h   = get_h2h(g["home_id"],g["away_id"],g["slug"],g["home"],g["away"]); prog.progress(85,"⚡ Monte Carlo...")
    h2s   = h2h_stats(h2h,g["home"],g["away"])
    hxg   = max(0.35,avg([r["gf"] for r in hform])) if hform else xg_from_record(g["home_rec"],True)
    axg   = max(0.35,avg([r["gf"] for r in aform])) if aform else xg_from_record(g["away_rec"],False)
    mc    = mc50k(hxg,axg); dp = diamond_engine(mc,h2s,hform,aform)
    pls   = smart_parlay(mc,dp,g["home"],g["away"])
    prog.progress(100,"✅ Listo"); prog.empty()

    # fuente
    src_h = f"✅ ESPN ({len(hform)}P)" if hform else f"📊 Récord {g['home_rec']}"
    src_a = f"✅ ESPN ({len(aform)}P)" if aform else f"📊 Récord {g['away_rec']}"
    st.markdown(
        f"<div style='font-size:.8rem;background:#0a0a1e;border-radius:8px;padding:8px 14px;"
        f"border:1px solid #1a1a40;margin:4px 0 14px;display:flex;gap:20px;flex-wrap:wrap'>"
        f"<span style='color:#444;font-weight:700'>Fuente:</span>"
        f"<span style='color:#00ff88'>{g['home'][:14]}: {src_h}</span>"
        f"<span style='color:#00ff88'>{g['away'][:14]}: {src_a}</span></div>",unsafe_allow_html=True)

    # ── JUGADA DIAMANTE ──
    picks_s = sorted([
        (f"🏠 {g['home'][:16]} gana",dp["ph"]),
        ("⚖️ Empate",dp["pd"]),
        (f"✈️ {g['away'][:16]} gana",dp["pa"]),
    ],key=lambda x:-x[1])
    main=picks_s[0]
    st.markdown(
        f"<div class='diamond-hero'>"
        f"<div style='font-size:.82rem;font-weight:700;color:#FFD700;letter-spacing:.14em;margin-bottom:14px'>✦ JUGADA DIAMANTE — {dp['conf']}</div>"
        f"<div style='font-size:3rem;font-weight:900;line-height:1;margin-bottom:10px'>{main[0]}</div>"
        f"<div style='font-size:1.4rem;font-weight:700;color:#FFD700;margin-bottom:24px'>{main[1]*100:.1f}% de probabilidad</div>"
        f"<div style='display:flex;gap:12px;flex-wrap:wrap'>"
        +"".join(f"<div class='mbox' style='flex:1;min-width:90px'><div class='mval' style='color:{'#7c00ff' if i==0 else '#555'}'>{v*100:.1f}%</div><div class='mlbl'>{l[:18]}</div></div>" for i,(l,v) in enumerate(picks_s))
        +f"<div class='mbox' style='flex:1;min-width:90px'><div class='mval' style='color:#ff9500'>{mc['btts']*100:.0f}%</div><div class='mlbl'>⚡ Ambos Anotan</div></div>"
        +f"<div class='mbox' style='flex:1;min-width:90px'><div class='mval' style='color:#00ccff'>{mc['o25']*100:.0f}%</div><div class='mlbl'>⚽ Over 2.5</div></div>"
        +f"</div><div style='font-size:.78rem;color:#444;margin-top:14px'>xG: {hxg:.1f} vs {axg:.1f} · MC 50K + H2H + Forma</div></div>",
        unsafe_allow_html=True)

    # ── GUARDAR PICK ──
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        if st.button(f"💾 Guardar: {main[0][:20]}", use_container_width=True, key="save_main"):
            add_pick(g, main[0], main[1], g.get("odd_h",0) if "gana" in main[0] and "🏠" in main[0] else g.get("odd_a",0))
            st.success("✅ Pick guardado en Historial")
    with sc2:
        if st.button(f"💾 Guardar: Over 2.5", use_container_width=True, key="save_o25"):
            add_pick(g, "⚽ Over 2.5", mc["o25"], 0)
            st.success("✅ Pick guardado")
    with sc3:
        if st.button(f"💾 Guardar: Ambos Anotan", use_container_width=True, key="save_btts"):
            add_pick(g, "⚡ Ambos Anotan", mc["btts"], 0)
            st.success("✅ Pick guardado")

    # ── TABLA DE POSICIONES ──
    st.markdown("<div class='shdr'>📊 Tabla de Posiciones</div>", unsafe_allow_html=True)
    with st.spinner("Cargando tabla..."):
        standings = get_standings(g["slug"])
    if standings:
        # Highlight home and away team
        st.markdown(
            f"<div class='acard' style='padding:12px 16px'>"
            f"<div class='stand-row' style='color:#555;font-size:.72rem;font-weight:700;border-bottom:2px solid #252555'>"
            f"<span>#</span><span>Equipo</span><span>PJ</span><span>Pts</span>"
            f"<span>GF</span><span>GC</span><span>Dif</span></div>",
            unsafe_allow_html=True)
        for row in standings[:20]:
            is_h = g["home_id"] == row["tid"]
            is_a = g["away_id"] == row["tid"]
            bg   = "background:#7c00ff22;border-left:3px solid #7c00ff;" if is_h else \
                   ("background:#ff444422;border-left:3px solid #ff4444;" if is_a else "")
            name_color = "#7c00ff" if is_h else ("#ff4444" if is_a else "#EEEEFF")
            st.markdown(
                f"<div class='stand-row' style='{bg}'>"
                f"<span style='color:#555'>{row['pos']}</span>"
                f"<span style='color:{name_color};font-weight:{'700' if is_h or is_a else '400'}'>{row['team'][:16]}</span>"
                f"<span style='color:#555'>{row['pj']}</span>"
                f"<span style='color:#FFD700;font-weight:700'>{row['pts']}</span>"
                f"<span style='color:#00ff88'>{row['gf']}</span>"
                f"<span style='color:#ff4444'>{row['gc']}</span>"
                f"<span style='color:#aaa'>{row['dif']}</span>"
                f"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#555;font-size:.85rem'>Tabla no disponible para esta liga.</div>", unsafe_allow_html=True)

    # ── MERCADOS ──
    st.markdown("<div class='shdr'>📊 Todos los Mercados</div>",unsafe_allow_html=True)
    cols=st.columns(6)
    for col,(label,val) in zip(cols,[("Over 1.5",mc["o15"]),("Over 2.5",mc["o25"]),
        ("Over 3.5",mc["o35"]),("Ambos Anotan",mc["btts"]),("CS Local",mc["cs_h"]),("CS Visit.",mc["cs_a"])]):
        with col:
            color="#00ff88" if val>=0.58 else ("#FFD700" if val>=0.45 else "#666")
            st.markdown(f"<div class='mbox'><div class='mval' style='color:{color}'>{val*100:.0f}%</div><div class='mlbl'>{label}</div></div>",unsafe_allow_html=True)

    # ── SMART PARLAY ──
    if pls:
        st.markdown("<div class='shdr'>🎰 Smart Parlay</div>",unsafe_allow_html=True)
        best=pls[0]; legs=[x for x in [best.get("l1"),best.get("l2")] if x]
        st.markdown(
            f"<div class='parlay-hero'>"
            f"<div style='font-size:.8rem;color:#00ccff;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>✦ PARLAY RECOMENDADO</div>"
            +"".join(f"<div style='font-size:1.1rem;font-weight:700;margin:4px 0'>✓ {l}</div>" for l in legs)
            +f"<div style='display:flex;gap:12px;margin-top:16px;flex-wrap:wrap'>"
            +"".join(f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ccff'>{p*100:.1f}%</div><div class='mlbl'>{l}</div></div>" for l,p in [(best.get("l1",""),best.get("p1",0)),(best.get("l2",""),best.get("p2",0))])
            +f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{best['cp']*100:.1f}%</div><div class='mlbl'>Combinada</div></div>"
            +f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{best['odds']}x</div><div class='mlbl'>Cuota</div></div>"
            +f"</div></div>",unsafe_allow_html=True)

    # ── STATS ──
    st.markdown("<div class='shdr'>📈 Estadísticas Comparativas</div>",unsafe_allow_html=True)
    h_gf=avg([r["gf"] for r in hform]) if hform else 0
    a_gf=avg([r["gf"] for r in aform]) if aform else 0
    h_gc=avg([r["gc"] for r in hform]) if hform else 0
    a_gc=avg([r["gc"] for r in aform]) if aform else 0
    h_o25=len([r for r in hform if r["gf"]+r["gc"]>2])/max(len(hform),1)*100
    a_o25=len([r for r in aform if r["gf"]+r["gc"]>2])/max(len(aform),1)*100
    h_bt=len([r for r in hform if r["gf"]>0 and r["gc"]>0])/max(len(hform),1)*100
    a_bt=len([r for r in aform if r["gf"]>0 and r["gc"]>0])/max(len(aform),1)*100
    rows=(f"<div style='display:grid;grid-template-columns:1fr 200px 1fr;gap:4px;"
          f"padding:8px 0;border-bottom:1px solid #151530;font-size:.82rem;font-weight:700;color:#555'>"
          f"<div style='text-align:right'>{g['home'][:14]}</div>"
          f"<div style='text-align:center'>Estadística</div>"
          f"<div>{g['away'][:14]}</div></div>")
    rows+=cmprow("Goles anotados/partido",h_gf,a_gf)
    rows+=cmprow("Goles recibidos/partido",h_gc,a_gc)
    rows+=cmprow("xG estimado",hxg,axg,"{:.1f}")
    rows+=cmprow("% Over 2.5 (últimos 10)",h_o25,a_o25,"{:.0f}","%")
    rows+=cmprow("% Ambos Anotan (últimos 10)",h_bt,a_bt,"{:.0f}","%")
    st.markdown(f"<div class='acard'>{rows}</div>",unsafe_allow_html=True)

    # ── FORMA ──
    st.markdown("<div class='shdr'>📈 Forma reciente</div>",unsafe_allow_html=True)
    fc1,fc2=st.columns(2)
    for col,tname,form,color,rec in [(fc1,g["home"],hform,"#7c00ff",g["home_rec"]),(fc2,g["away"],aform,"#ff4444",g["away_rec"])]:
        with col:
            w=sum(1 for r in form if r["result"]=="W")
            d=sum(1 for r in form if r["result"]=="D")
            l=sum(1 for r in form if r["result"]=="L")
            gf=sum(r["gf"] for r in form); gc=sum(r["gc"] for r in form)
            if form:
                st.markdown(
                    f"<div class='acard'>"
                    f"<div style='font-weight:700;font-size:1.05rem;color:{color};margin-bottom:10px'>{tname}</div>"
                    f"<div style='margin-bottom:12px'>{badges(form)}</div>"
                    f"<div style='display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px'>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ff88'>{w}</div><div class='mlbl'>V</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{d}</div><div class='mlbl'>E</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#ff4444'>{l}</div><div class='mlbl'>D</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ccff'>{gf}</div><div class='mlbl'>GF</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#ff9500'>{gc}</div><div class='mlbl'>GC</div></div>"
                    f"</div>"
                    f"<div style='font-size:.82rem;color:#555'>Récord temporada: {rec} · Último: hace {days_since(form)}d</div>"
                    f"</div>",unsafe_allow_html=True)
            else:
                # Sin historial ESPN — mostrar solo récord de temporada
                try:
                    rw,rd,rl = map(int, rec.split("-"))
                    rn = rw+rd+rl
                    rwp = round(rw/rn*100) if rn>0 else 0
                except: rw=rd=rl=rn=rwp=0
                st.markdown(
                    f"<div class='acard'>"
                    f"<div style='font-weight:700;font-size:1.05rem;color:{color};margin-bottom:10px'>{tname}</div>"
                    f"<div style='margin-bottom:12px'><span style='color:#555;font-size:.85rem'>Sin historial detallado en ESPN</span></div>"
                    f"<div style='display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px'>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ff88'>{rw}</div><div class='mlbl'>V</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{rd}</div><div class='mlbl'>E</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#ff4444'>{rl}</div><div class='mlbl'>D</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ccff'>{rn}</div><div class='mlbl'>PJ</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#7c00ff'>{rwp}%</div><div class='mlbl'>% V</div></div>"
                    f"</div>"
                    f"<div style='font-size:.82rem;color:#555'>Récord temporada: {rec}</div>"
                    f"</div>",unsafe_allow_html=True)
            with st.expander(f"📋 {tname[:20]} — partidos detallados"):
                if not form:
                    st.markdown("<div style='color:#555;padding:10px'>Sin historial ESPN para esta liga.</div>",unsafe_allow_html=True)
                for r in form:
                    rc="#00ff88" if r["result"]=="W" else ("#FFD700" if r["result"]=="D" else "#ff4444")
                    loc="🏠" if r["is_home"] else "✈️"
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;font-size:.88rem;"
                        f"padding:6px 4px;border-bottom:1px solid #151530'>"
                        f"<span style='color:#555;width:90px'>{r['date']}</span>"
                        f"<span>{loc} {r['opponent'][:18]}</span>"
                        f"<span style='color:{rc};font-weight:700'>{r['gf']}-{r['gc']} ({r['result']})</span></div>",
                        unsafe_allow_html=True)

    # ── H2H ──
    st.markdown("<div class='shdr'>⚔️ Head to Head</div>",unsafe_allow_html=True)
    if h2h:
        ha,hb=st.columns([3,2])
        with ha:
            st.markdown("<div class='acard'>",unsafe_allow_html=True)
            for x in h2h[:8]:
                wc="#00ff88" if x["winner"]==g["home"] else ("#ff4444" if x["winner"]==g["away"] else "#FFD700")
                bg="#00ff8810" if x["winner"]==g["home"] else ("#ff444410" if x["winner"]==g["away"] else "#FFD70010")
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:8px 12px;border-radius:6px;margin:3px 0;background:{bg}'>"
                    f"<span style='color:#555'>{x['date'][:7]}</span>"
                    f"<span>{x['home'][:12]}</span>"
                    f"<span style='font-weight:900;color:{wc};min-width:40px;text-align:center'>{x['gh']}-{x['ga']}</span>"
                    f"<span>{x['away'][:12]}</span></div>",unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)
        with hb:
            if h2s:
                st.markdown(
                    f"<div class='acard'>"
                    f"<div style='font-weight:700;margin-bottom:12px'>Últimos {h2s['tot']} encuentros</div>"
                    f"<div style='display:flex;gap:8px;margin-bottom:12px'>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ff88'>{h2s['hw']}</div><div class='mlbl'>{g['home'][:8]}</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{h2s['dw']}</div><div class='mlbl'>Empate</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#ff4444'>{h2s['aw']}</div><div class='mlbl'>{g['away'][:8]}</div></div>"
                    f"</div>"
                    f"<div style='font-size:.85rem;color:#555'>Prom. goles: {h2s['avg_g']}</div>"
                    f"<div style='font-size:.85rem;color:#555'>Over 2.5: {h2s['o25p']}%</div>"
                    f"<div style='font-size:.85rem;color:#555'>BTTS: {h2s['bttsp']}%</div>"
                    f"</div>",unsafe_allow_html=True)
    else:
        st.info("No se encontraron encuentros anteriores en ESPN para esta liga.")

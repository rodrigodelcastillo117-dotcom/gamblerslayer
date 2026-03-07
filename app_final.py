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
    BOT_TOKEN         = st.secrets["BOT_TOKEN"]
    CHAT_ID           = st.secrets["CHAT_ID"]
    ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")
    TENNIS_API_KEY    = st.secrets.get("TENNIS_API_KEY", "04f347bda8bf9af33d836085b958ed98cb885b4d94e1a1bb848732d5813a2cfc")
except:
    BOT_TOKEN         = os.getenv("BOT_TOKEN", "")
    CHAT_ID           = os.getenv("CHAT_ID", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    TENNIS_API_KEY    = os.getenv("TENNIS_API_KEY", "04f347bda8bf9af33d836085b958ed98cb885b4d94e1a1bb848732d5813a2cfc")

LIGAS = {
    "eng.1":"Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿","eng.2":"Championship 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "eng.fa":"FA Cup 🏆🏴󠁧󠁢󠁥󠁮󠁧󠁿",
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
/* ── INLINE CODE tags — dark always ── */
code{background:#1a1a40!important;color:#00ccff!important;border-radius:5px!important;
  padding:2px 7px!important;font-size:.85em!important;border:1px solid #252555!important}
/* ── ST TEXT INPUT — dark background ── */
[data-testid="stTextInput"] > div > div > input{
  background:#0d0d2e!important;color:#EEEEFF!important;
  border:1px solid #252555!important;border-radius:10px!important}
[data-testid="stTextInput"] > div > div > input::placeholder{color:#555!important}
[data-testid="stTextInput"] > div > div > input:focus{border-color:#7c00ff!important;
  box-shadow:0 0 0 2px #7c00ff33!important}
[data-testid="stTextInput"] label{color:#aaa!important;font-size:.82rem!important}
/* ── NUMBER INPUT — dark ── */
[data-testid="stNumberInput"] input{background:#0d0d2e!important;color:#EEEEFF!important;
  border:1px solid #252555!important;border-radius:10px!important}
/* ── PASSWORD INPUT ── */
[data-testid="stTextInput"] [data-testid="InputInstructions"]{color:#555!important}
/* loader lives in iframe component — no CSS needed here */
/* ── SELECTBOX — texto visible siempre ── */
[data-testid="stSelectbox"] > div > div{
  background:#0d0d2e!important;border:1px solid #252555!important;
  border-radius:10px!important;color:#EEEEFF!important}
[data-testid="stSelectbox"] > div > div > div{color:#EEEEFF!important}
[data-testid="stSelectbox"] svg{fill:#EEEEFF!important}
/* Dropdown abierto */
[data-baseweb="popover"] [role="option"]{
  background:#0d0d2e!important;color:#EEEEFF!important}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"]{
  background:#1a1a50!important;color:#FFD700!important}
[data-baseweb="select"] [data-testid="stMarkdownContainer"] *{color:#EEEEFF!important}
/* Selectbox input text */
div[data-baseweb="select"] > div{
  background:#0d0d2e!important;border-color:#252555!important;color:#EEEEFF!important}
div[data-baseweb="select"] > div > div{color:#EEEEFF!important;font-weight:600!important}
div[data-baseweb="select"] input{color:#EEEEFF!important}
/* ── EXPANDERS — texto siempre blanco ── */
[data-testid="stExpander"]{border:1px solid #252555!important;border-radius:12px!important;background:#0d0d2e!important}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] details summary{
  color:#EEEEFF!important;background:#0d0d2e!important;font-weight:700!important}
[data-testid="stExpander"] summary:hover,
[data-testid="stExpander"] summary:hover *{color:#FFD700!important}
[data-testid="stExpander"] > details > summary{
  background:#0d0d2e!important;border-radius:12px!important;padding:12px 16px!important;color:#EEEEFF!important}
/* Force all text inside expander header white */
details > summary > div,
details > summary > div *,
details > summary span,
details > summary p{color:#EEEEFF!important}
/* ── DATE / FECHA label en expanders ── */
.streamlit-expanderHeader *{color:#EEEEFF!important}
.streamlit-expanderHeader:hover,
.streamlit-expanderHeader:hover *{color:#FFD700!important;background:#12123a!important}
/* ── MOBILE ── */
@media(max-width:768px){
  /* Header */
  div[style*="2.8rem"]{font-size:1.9rem!important}
  div[style*="letter-spacing:.15em"]{font-size:.65rem!important;letter-spacing:.08em!important}
  /* Cards */
  .diamond-hero{padding:14px 12px!important}
  .diamond-hero::before{font-size:2.5rem!important;opacity:.05!important;right:10px!important;top:10px!important}
  .parlay-hero{padding:14px 12px!important}
  .trilay-card{padding:12px 10px!important}
  .pato-card{padding:10px 8px!important}
  .pato-hero{padding:14px 12px!important}
  .acard{padding:12px 10px!important}
  .mrow{padding:10px 12px!important}
  .bot-card{padding:14px 12px!important}
  /* Metric boxes */
  .mval{font-size:1.2rem!important}
  .mlbl{font-size:.6rem!important}
  .mbox{padding:8px 4px!important}
  /* Headers */
  .shdr{font-size:.68rem!important;letter-spacing:.06em!important}
  /* Tabs — scroll horizontal */
  .stTabs [data-baseweb="tab-list"]{overflow-x:auto!important;flex-wrap:nowrap!important;
    -webkit-overflow-scrolling:touch!important;gap:0!important;
    scrollbar-width:none!important}
  .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar{display:none!important}
  .stTabs [data-baseweb="tab"]{padding:8px 10px!important;font-size:.72rem!important;
    white-space:nowrap!important;min-width:auto!important;flex-shrink:0!important}
  /* Columns no overflow */
  [data-testid="column"]{min-width:0!important;overflow:hidden!important}
  /* Sport selector buttons */
  .stButton>button{padding:8px 6px!important;font-size:.8rem!important}
  /* Standings */
  .stand-row{grid-template-columns:18px 1fr 26px 26px 26px 26px 38px!important;font-size:.7rem!important;padding:6px 2px!important}
  /* Expanders */
  .streamlit-expanderHeader{padding:10px 14px!important;font-size:.85rem!important}
  /* Text overflow */
  .mrow div[style*="font-weight:700"]{font-size:.88rem!important;
    white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;max-width:58vw!important}
  /* Full width containers */
  section[data-testid="stMain"] .block-container{padding:0.5rem 0.6rem 2rem!important}
}
</style>""", unsafe_allow_html=True)

# ── Loading animation — inyectada via components para que el JS se ejecute ──
# st.markdown bloquea <script>; st.components.v1.html() vive en iframe
# Solución: meter el overlay en el DOM padre via postMessage + JS en iframe
import streamlit.components.v1 as _components
_components.html("""<!DOCTYPE html>
<html><head><style>
  body{margin:0;padding:0;background:transparent;overflow:hidden}
</style></head>
<body>
<script>
(function(){
  // Este iframe se ejecuta dentro de Streamlit.
  // Inyectamos el overlay y su lógica en el documento PADRE.
  var css = [
    '.gl-overlay{position:fixed;top:0;left:0;width:100%;height:100%;',
    'background:rgba(5,5,20,.82);backdrop-filter:blur(6px);z-index:99999;',
    'display:flex;flex-direction:column;align-items:center;justify-content:center;',
    'opacity:0;pointer-events:none;transition:opacity .25s}',
    '.gl-overlay.show{opacity:1;pointer-events:all}',
    '.gl-track{display:flex;gap:18px;align-items:center;margin-bottom:18px}',
    '.gl-ball{font-size:2.4rem;animation:glB 1.1s ease-in-out infinite}',
    '.gl-ball:nth-child(1){animation-delay:0s}',
    '.gl-ball:nth-child(2){animation-delay:.18s}',
    '.gl-ball:nth-child(3){animation-delay:.36s}',
    '.gl-ball:nth-child(4){animation-delay:.54s}',
    '.gl-ball:nth-child(5){animation-delay:.72s}',
    '@keyframes glB{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}',
    '.gl-txt{color:#FFD700;font-size:1rem;font-weight:700;letter-spacing:.12em;',
    'animation:glP 1.4s ease-in-out infinite}',
    '@keyframes glP{0%,100%{opacity:1}50%{opacity:.4}}'
  ].join('');

  var p = window.parent;
  if(!p || p === window) return;
  var pd = p.document;

  // Inject CSS
  if(!pd.getElementById('gl-style')){
    var s = pd.createElement('style');
    s.id = 'gl-style'; s.textContent = css;
    pd.head.appendChild(s);
  }

  // Inject overlay div
  var overlay = pd.getElementById('gl-overlay');
  if(!overlay){
    overlay = pd.createElement('div');
    overlay.id = 'gl-overlay';
    overlay.className = 'gl-overlay';
    overlay.innerHTML = '<div class="gl-track">'
      + '<span class="gl-ball">⚽</span>'
      + '<span class="gl-ball">🎾</span>'
      + '<span class="gl-ball">🪙</span>'
      + '<span class="gl-ball">🏀</span>'
      + '<span class="gl-ball">🎰</span>'
      + '</div><div class="gl-txt">Cargando picks...</div>';
    pd.body.appendChild(overlay);
  }

  var showing = false;
  var hideTimer = null;

  function show(){
    if(!showing){ showing=true; overlay.classList.add('show'); }
    clearTimeout(hideTimer);
    hideTimer = setTimeout(hide, 9000); // failsafe
  }
  function hide(){
    if(showing){ showing=false; overlay.classList.remove('show'); }
    clearTimeout(hideTimer);
  }

  // Click en cualquier botón del padre = show loader
  pd.addEventListener('click', function(e){
    var btn = e.target.closest('button');
    if(!btn || btn.closest('#gl-overlay')) return;
    show();
  }, true);

  // MutationObserver en padre: cuando el DOM deja de cambiar 700ms = hide
  var domTimer = null;
  var obs = new MutationObserver(function(muts){
    var sig = muts.some(function(m){
      return m.target.id !== 'gl-overlay' && !m.target.closest('#gl-overlay') && m.addedNodes.length > 0;
    });
    if(!sig) return;
    clearTimeout(domTimer);
    domTimer = setTimeout(hide, 700);
  });

  function boot(){
    var root = pd.querySelector('[data-testid="stAppViewContainer"]') || pd.body;
    obs.observe(root, {childList:true, subtree:true});
  }

  pd.readyState === 'loading'
    ? pd.addEventListener('DOMContentLoaded', boot)
    : setTimeout(boot, 300);
})();
</script>
</body></html>""", height=0, scrolling=False)

NBA_ESPN = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
TEN_ESPN = "https://site.api.espn.com/apis/site/v2/sports/tennis"

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
# ODDS API — The Odds API (gratis 500 req/mes)
# ══════════════════════════════════════════════════════════
try:
    ODDS_API_KEY = st.secrets.get("ODDS_API_KEY", "")
except:
    ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")
BOOKMAKERS   = ["bet365","pinnacle","unibet","williamhill"]

@st.cache_data(ttl=300, show_spinner=False)
def get_real_odds(home_name, away_name, league_slug):
    """
    Intenta obtener cuotas reales de The Odds API.
    Si no hay key o falla, devuelve dict vacío.
    """
    _key = st.session_state.get("runtime_odds_key", ODDS_API_KEY)
    if not _key:
        return {}
    # Mapeo de slugs ESPN → sport_key de Odds API
    slug_map = {
        "eng.1":"soccer_epl","esp.1":"soccer_spain_la_liga",
        "ger.1":"soccer_germany_bundesliga","ita.1":"soccer_italy_serie_a",
        "fra.1":"soccer_france_ligue_one","ned.1":"soccer_netherlands_eredivisie",
        "por.1":"soccer_portugal_primeira_liga","mex.1":"soccer_mexico_ligamx",
        "usa.1":"soccer_usa_mls","arg.1":"soccer_argentina_primera_division",
        "bra.1":"soccer_brazil_campeonato","tur.1":"soccer_turkey_super_league",
        "bel.1":"soccer_belgium_first_div","sco.1":"soccer_scotland_premiership",
        "uefa.champions":"soccer_uefa_champs_league","uefa.europa":"soccer_uefa_europa_league",
    }
    sport = slug_map.get(league_slug)
    if not sport: return {}
    try:
        url  = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        resp = requests.get(url, params={
            "apiKey": st.session_state.get("runtime_odds_key", ODDS_API_KEY), "regions":"eu",
            "markets":"h2h","oddsFormat":"decimal","bookmakers": ",".join(BOOKMAKERS)
        }, timeout=8)
        if resp.status_code != 200: return {}
        for game in resp.json():
            h = game.get("home_team","").lower()
            a = game.get("away_team","").lower()
            if home_name[:6].lower() in h or away_name[:6].lower() in a:
                out = {}
                for bk in game.get("bookmakers",[]):
                    name = bk["key"]
                    for mkt in bk.get("markets",[]):
                        if mkt["key"] == "h2h":
                            outs = {o["name"].lower():o["price"] for o in mkt["outcomes"]}
                            out[name] = {
                                "h": outs.get(h, 0),
                                "d": outs.get("draw", 0),
                                "a": outs.get(a, 0),
                            }
                return out
    except: pass
    return {}


# ══════════════════════════════════════════════════════════
# SHARP MONEY INTELLIGENCE SYSTEM
# Detecta: línea de movimiento · steam moves · reverse line movement
# Fuentes: The Odds API (multi-book) + Betfair Exchange + heurísticas
# ══════════════════════════════════════════════════════════

_LINE_HISTORY_FILE = "/tmp/tgl_lines.json"
try:
    with open(_LINE_HISTORY_FILE) as _lf: _line_history = __import__("json").load(_lf)
except: _line_history = {}

def _save_line_history():
    try:
        with open(_LINE_HISTORY_FILE,"w") as _lf: __import__("json").dump(_line_history,_lf)
    except: pass

def track_line_movement(game_id, home, away, bk_odds):
    """
    Guarda snapshot de cuotas por partido.
    Detecta movimiento comparando con snapshot anterior.
    """
    now = datetime.now(CDMX).isoformat()
    key = f"{home[:8]}_{away[:8]}"
    if key not in _line_history:
        _line_history[key] = {"snapshots":[], "game_id": game_id}
    snap = {"ts": now, "odds": bk_odds}
    hist = _line_history[key]["snapshots"]
    # Solo guardar si hay cambio real vs último snapshot
    if not hist or snap["odds"] != hist[-1]["odds"]:
        hist.append(snap)
        if len(hist) > 20: _line_history[key]["snapshots"] = hist[-20:]
        _save_line_history()
    return _line_history[key]["snapshots"]

def analyze_line_movement(home, away, current_odds, model_ph):
    """
    Análisis completo de movimiento de línea y señales sharp.
    
    Detecta:
    1. Steam move — movimiento brusco sin noticias (sharps entraron)
    2. Reverse line movement — dinero mayoritario en A, pero línea mueve a B
    3. Pinnacle vs mercado — divergencia entre Pinnacle y casas de retail
    4. Fade the public — cuándo el público está muy cargado en un lado
    5. Closing line value — nuestro modelo vs Pinnacle (el oráculo)
    """
    key = f"{home[:8]}_{away[:8]}"
    hist = _line_history.get(key, {}).get("snapshots", [])
    
    signals = []
    score = 0  # -100 (contrario) a +100 (muy favorable)
    
    # ── 1. PINNACLE COMO ORÁCULO ──
    pin_odds = current_odds.get("pinnacle", {})
    pin_h = pin_odds.get("h", 0)
    if pin_h > 1:
        pin_prob = 1/pin_h
        # Quitar margen Pinnacle (~2.5%)
        pin_total = (1/pin_odds.get("h",1.5) + 1/pin_odds.get("d",4) + 1/pin_odds.get("a",5))
        pin_prob_clean = (1/pin_h) / pin_total if pin_total > 0 else pin_prob
        clv = model_ph - pin_prob_clean  # Closing Line Value
        if clv > 0.06:
            signals.append({"icon":"🎯","label":"CLV Alto","desc":f"Modelo supera Pinnacle limpio en +{clv*100:.1f}%","color":"#00ff88","weight":35})
            score += 35
        elif clv > 0.03:
            signals.append({"icon":"✅","label":"CLV Positivo","desc":f"+{clv*100:.1f}% sobre Pinnacle","color":"#FFD700","weight":20})
            score += 20
        elif clv < -0.04:
            signals.append({"icon":"⚠️","label":"Pinnacle en contra","desc":f"Pinnacle {abs(clv)*100:.1f}% más bajo que nuestro modelo","color":"#ff4444","weight":-25})
            score -= 25
    
    # ── 2. DIVERGENCIA MULTI-BOOK ──
    book_probs_h = []
    for bk, odds in current_odds.items():
        oh = odds.get("h", 0)
        if oh > 1: book_probs_h.append(1/oh)
    if len(book_probs_h) >= 3:
        avg_prob = sum(book_probs_h)/len(book_probs_h)
        std_prob = float(__import__("numpy").std(book_probs_h))
        if std_prob > 0.04:
            signals.append({"icon":"⚡","label":"Divergencia entre casas","desc":f"Desacuerdo entre {len(book_probs_h)} libros (σ={std_prob*100:.1f}%) — alguien sabe algo","color":"#ff9500","weight":15})
            score += 10
        # Soft book vs sharp book gap
        soft_books = ["bet365","williamhill","unibet","bwin","betway"]
        sharp_books = ["pinnacle","betcris","betonlineag"]
        soft_p  = [1/current_odds[b]["h"] for b in soft_books if b in current_odds and current_odds[b].get("h",0)>1]
        sharp_p = [1/current_odds[b]["h"] for b in sharp_books if b in current_odds and current_odds[b].get("h",0)>1]
        if soft_p and sharp_p:
            gap = sum(sharp_p)/len(sharp_p) - sum(soft_p)/len(soft_p)
            if gap > 0.03:
                signals.append({"icon":"🦅","label":"Sharp vs Public gap","desc":f"Sharps tienen {gap*100:.1f}% MÁS en local que el público","color":"#00ccff","weight":25})
                score += 25
            elif gap < -0.03:
                signals.append({"icon":"🐟","label":"Trampa pública","desc":f"Casas soft {abs(gap)*100:.1f}% más altas — dinero público en favorito","color":"#ff4444","weight":-20})
                score -= 20

    # ── 3. STEAM MOVE DETECTION (histórico de líneas) ──
    if len(hist) >= 2:
        first = hist[0]["odds"]
        last  = hist[-1]["odds"]
        # Movimiento total de Pinnacle
        p_open = first.get("pinnacle",{}).get("h",0)
        p_now  = last.get("pinnacle",{}).get("h",0)
        if p_open>1 and p_now>1:
            move = (1/p_now - 1/p_open)  # en probabilidad
            if abs(move) > 0.04:
                direction = "local" if move>0 else "visitante"
                signals.append({"icon":"💨","label":f"Steam Move detectado","desc":f"Línea movió {abs(move)*100:.1f}% hacia {direction} desde apertura","color":"#aa00ff","weight":20 if (move>0 and model_ph>0.5) else -15})
                score += 20 if (move>0 and model_ph>0.5) else -15
        
        # Reverse line movement — lo más valioso
        if len(hist) >= 3:
            # Si la prob implícita del favorito SUBIÓ pero la cuota del favorito TAMBIÉN subió
            # (deberían moverse inversamente si el público apoya al favorito)
            mid = hist[len(hist)//2]["odds"]
            p_mid_h  = mid.get("pinnacle",{}).get("h",0)
            p_last_h = last.get("pinnacle",{}).get("h",0)
            p_mid_b  = mid.get("bet365",{}).get("h",0)
            p_last_b = last.get("bet365",{}).get("h",0)
            if p_mid_h>1 and p_last_h>1 and p_mid_b>1 and p_last_b>1:
                # Pinnacle sube cuota local (menos prob) pero Bet365 baja cuota (más prob)
                pin_move  = p_last_h - p_mid_h   # positivo = cuota subió = menos probable
                b365_move = p_last_b - p_mid_b   # positivo = cuota subió = menos probable
                if pin_move < -0.05 and b365_move > 0.05:
                    signals.append({"icon":"🔄","label":"REVERSE LINE MOVEMENT","desc":"Sharps en local, público en visitante. Señal más valiosa del mercado.","color":"#00ff88","weight":40})
                    score += 40
                elif pin_move > 0.05 and b365_move < -0.05:
                    signals.append({"icon":"🔄","label":"RLM — Cuidado","desc":"Sharps en visitante, público en local. Posible fade.","color":"#ff9500","weight":-30})
                    score -= 30

    # ── 4. PÚBLICO CARGADO (heurística por cuota) ──
    b365_h = current_odds.get("bet365",{}).get("h",0)
    pin_h2  = current_odds.get("pinnacle",{}).get("h",0)
    if b365_h>1 and pin_h2>1:
        b365_prob = 1/b365_h; pin_prob2 = 1/pin_h2
        # Bet365 tiene cuota más baja (más favorable al local) que Pinnacle
        # → Bet365 acepta el público, Pinnacle calibra con sharps
        gap2 = b365_prob - pin_prob2
        if gap2 > 0.04:
            signals.append({"icon":"👥","label":"Público cargado en local","desc":f"Bet365 {gap2*100:.1f}% más bajo que Pinnacle — mercado público","color":"#ff9500","weight":-15})
            score -= 10
        elif gap2 < -0.03:
            signals.append({"icon":"💎","label":"Valor sin público","desc":"Pinnacle más favorable que casas retail — underdog con valor","color":"#00ff88","weight":15})
            score += 15


    # ── VEREDICTO FINAL ──
    score = max(-100, min(100, score))
    if score >= 40:    verdict = "🦅 SHARP MONEY FAVOR"     ; vc = "#00ff88"
    elif score >= 20:  verdict = "✅ SEÑAL POSITIVA"        ; vc = "#00ccff"
    elif score >= -10: verdict = "⚖️ NEUTRAL"               ; vc = "#FFD700"
    elif score >= -30: verdict = "⚠️ DINERO CONTRARIO"      ; vc = "#ff9500"
    else:              verdict = "🚫 EVITAR — TRAMPA PÚBLICA"; vc = "#ff4444"

    return {
        "signals": signals,
        "score": score,
        "verdict": verdict,
        "verdict_color": vc,
        "clv": clv if pin_h > 1 else None,
        "has_data": len(signals) > 0,
    }


_betfair_session = {"token": None, "expires": 0}

def _betfair_login():
    """Login a Betfair y obtener session token. Cachea 6 horas."""
    now = time.time()
    if _betfair_session["token"] and now < _betfair_session["expires"]:
        return _betfair_session["token"]
    try:
        resp = requests.post(
            "https://identitysso-cert.betfair.com/api/certlogin",
            timeout=10
        )
        data = resp.json()
        if data.get("loginStatus") == "SUCCESS":
            _betfair_session["token"] = data["sessionToken"]
            _betfair_session["expires"] = now + 21600  # 6 horas
            return _betfair_session["token"]
    except: pass
    # Fallback: login sin cert (funciona para datos de solo lectura)
    try:
        resp = requests.post(
            "https://identitysso.betfair.com/api/login",
            timeout=10
        )
        data = resp.json()
        if data.get("status") == "SUCCESS":
            _betfair_session["token"] = data.get("token","")
            _betfair_session["expires"] = now + 21600
            return _betfair_session["token"]
    except: pass
    return None

def _betfair_call(method, params, session_token):
    """Llamada JSON-RPC a Betfair Exchange API."""
    try:
        resp = requests.post(
            "https://api.betfair.com/exchange/betting/json-rpc/v1",
            headers={
                "X-Authentication": session_token,
                "Content-Type": "application/json"
            },
            json={"jsonrpc":"2.0","method":f"SportsAPING/v1.0/{method}","params":params,"id":1},
            timeout=10
        )
        result = resp.json()
        return result.get("result", [])
    except: return []

@st.cache_data(ttl=300, show_spinner=False)

# ── SportsBookReview scraper — % público gratis (reemplaza Action Network) ──
@st.cache_data(ttl=600, show_spinner=False)
def get_sbr_public_betting(home, away, sport="soccer"):
    """
    SportsBookReview.com — % de apuestas públicas gratis.
    Más confiable que Action Network para datos no-USA.
    Datos disponibles principalmente para fútbol major y NBA.
    """
    try:
        sport_map = {"soccer":"soccer","nba":"nba","nfl":"nfl"}
        sp = sport_map.get(sport, "soccer")
        url = f"https://www.sportsbookreview.com/betting-odds/{sp}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml"
        }
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code != 200: return {}
        html = resp.text
        # Buscar el nombre del partido en el HTML
        hn = home.lower()[:8]; an = away.lower()[:8]
        idx = -1
        for term in [hn, an]:
            i = html.lower().find(term)
            if i > 0: idx = i; break
        if idx < 0: return {}
        # Extraer % de picks en zona cercana al partido
        import re
        zone = html[max(0,idx-500):idx+1500]
        pcts = re.findall(r'"picksPct"\\s*:\\s*(\\d+(?:\\.\\d+)?)', zone)
        if len(pcts) >= 2:
            return {
                "home_pct": float(pcts[0]),
                "away_pct": float(pcts[1]),
                "source": "SBR"
            }
        # Fallback: buscar patrones numéricos de %
        pcts2 = re.findall(r'(\\d{1,2})%\\s*(?:of\\s*bets|picks)', zone, re.IGNORECASE)
        if pcts2:
            return {"home_pct": float(pcts2[0]), "away_pct": 100-float(pcts2[0]), "source": "SBR"}
    except: pass
    return {}

# ── Action Network — datos NBA/NFL (endpoint no documentado) ──
@st.cache_data(ttl=600, show_spinner=False)
@st.cache_data(ttl=180, show_spinner=False)
def get_action_network_nba(home, away):
    """
    Action Network NBA — PRO + fallback público.
    Devuelve: % bets + % money en spread, ML y O/U + línea apertura/cierre.
    """
    try:
        _token = ""
        try: _token = st.secrets.get("ACTION_NETWORK_TOKEN", "")
        except: _token = os.getenv("ACTION_NETWORK_TOKEN", "")
        
        date = datetime.now(CDMX).strftime("%Y%m%d")
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Referer":    "https://www.actionnetwork.com/",
            "Accept":     "application/json",
        }
        if _token:
            headers["Authorization"] = f"Bearer {_token}"
        
        # PRO endpoint primero, fallback a v1
        for url, params in [
            ("https://api.actionnetwork.com/web/v2/games/nba",
             {"date": date, "bookIds": "15,30,76,123"}),
            ("https://api.actionnetwork.com/web/v1/games/nba",
             {"date": date}),
            ("https://api.actionnetwork.com/web/v1/games",
             {"sport": "nba", "date": date}),
        ]:
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=8)
                if resp.status_code == 200: break
            except: continue
        else:
            return {}
        
        games = resp.json().get("games", [])
        hn = home.lower()[:7]; an = away.lower()[:7]
        
        for g in games:
            teams = g.get("teams", [{}]*2)
            names = [t.get("full_name","").lower() for t in teams]
            abbrs = [t.get("abbr","").lower() for t in teams]
            if not (any(hn in n or n[:7] in hn for n in names+abbrs) or
                    any(an in n or n[:7] in an for n in names+abbrs)):
                continue
            
            # ── % Bets y Money ──
            ml  = g.get("ml_bets",{})  or g.get("moneyline_bets",{}) or {}
            ou  = g.get("ou_bets",{})  or g.get("total_bets",{})     or {}
            spd = g.get("spread_bets",{}) or {}
            
            # Línea apertura vs cierre
            open_total = curr_total = open_ml = curr_ml = 0
            for bk in g.get("books",[]):
                if bk.get("book_id") in [15, 30, 123]:
                    p = bk.get("periods",{}).get("0",{})
                    open_total = p.get("total",{}).get("open",0) or 0
                    curr_total = p.get("total",{}).get("current",0) or 0
                    open_ml    = p.get("money_line",{}).get("open_home",0) or 0
                    curr_ml    = p.get("money_line",{}).get("current_home",0) or 0
                    break
            
            return {
                # ML
                "ml_home_bets_pct":    ml.get("home_bets_pct",0) or ml.get("home_bets",0),
                "ml_home_money_pct":   ml.get("home_money_pct",0) or ml.get("home_money",0),
                "ml_away_bets_pct":    ml.get("away_bets_pct",0) or ml.get("away_bets",0),
                "ml_away_money_pct":   ml.get("away_money_pct",0) or ml.get("away_money",0),
                # O/U
                "over_bets_pct":       ou.get("over_bets_pct",0) or ou.get("over_bets",0),
                "over_money_pct":      ou.get("over_money_pct",0) or ou.get("over_money",0),
                "under_bets_pct":      ou.get("under_bets_pct",0) or ou.get("under_bets",0),
                "under_money_pct":     ou.get("under_money_pct",0) or ou.get("under_money",0),
                # Spread
                "spread_home_bets_pct":  spd.get("home_bets_pct",0),
                "spread_home_money_pct": spd.get("home_money_pct",0),
                # Línea
                "open_total": open_total, "curr_total": curr_total,
                "open_ml_h":  open_ml,   "curr_ml_h":  curr_ml,
                # Meta
                "steam_move":    g.get("steam_move", False),
                "reverse_move":  g.get("reverse_line_movement", False),
                "consensus_pick":g.get("consensus",{}).get("pick",""),
                "injuries":      [i.get("player","")+" "+i.get("status","")
                                  for i in g.get("injuries",[])[:4]],
                "source":        "ActionNetwork PRO" if _token else "ActionNetwork",
            }
    except: pass
    return {}

@st.cache_data(ttl=300, show_spinner=False)
def get_action_network_pro(home, away, sport="soccer", date_str=None):
    """
    Action Network PRO — endpoint autenticado.
    Con cuenta PRO accedes a: % bets, % dinero, sharp %, línea apertura vs cierre,
    steam moves, consensus picks, injury reports con impacto.
    """
    try:
        _an_key = ""
        try: _an_key = st.secrets.get("ACTION_NETWORK_TOKEN", "")
        except: _an_key = os.getenv("ACTION_NETWORK_TOKEN","")
        
        sport_map = {
            "soccer": "soccer", "nba":"nba", "tennis":"tennis",
            "nfl":"nfl", "mlb":"mlb", "nhl":"nhl"
        }
        sp = sport_map.get(sport, "soccer")
        date = date_str or datetime.now(CDMX).strftime("%Y%m%d")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Referer": "https://www.actionnetwork.com/",
            "Accept": "application/json",
            "x-api-key": _an_key,
        }
        
        # PRO endpoint con datos de dinero
        url = f"https://api.actionnetwork.com/web/v2/games/{sp}"
        resp = requests.get(url, headers=headers,
                            params={"date": date, "bookIds":"15,30,76,123"},
                            timeout=10)
        
        if resp.status_code != 200:
            # Fallback endpoint público
            url2 = f"https://api.actionnetwork.com/web/v1/games/{sp}"
            resp = requests.get(url2, headers=headers,
                                params={"date": date}, timeout=8)
        if resp.status_code != 200: return {}
        
        games = resp.json().get("games", [])
        hn = home.lower()[:7]; an = away.lower()[:7]
        
        for g in games:
            teams = g.get("teams", [{}]*2)
            names = [t.get("full_name","").lower() for t in teams]
            abbrs = [t.get("abbr","").lower() for t in teams]
            all_names = names + abbrs
            match = (any(hn in n or n[:7] in hn for n in all_names) or
                     any(an in n or n[:7] in an for n in all_names))
            if not match: continue
            
            # Extraer datos de dinero
            result = {
                "source": "ActionNetwork PRO",
                "game_id": g.get("id"),
                "status": g.get("status",""),
            }
            
            # Money % por mercado
            for mkt_key, mkt_name in [("spread","spread"),("ml","ml"),("total","total")]:
                mkt = g.get(f"{mkt_key}_consensus") or g.get(f"consensus_{mkt_key}") or {}
                if mkt:
                    result[f"{mkt_name}_home_bets_pct"]  = mkt.get("home_bets",0) or mkt.get("away_bets",0)
                    result[f"{mkt_name}_home_money_pct"] = mkt.get("home_money",0) or mkt.get("money_home",0)
                    result[f"{mkt_name}_over_bets_pct"]  = mkt.get("over_bets",0)
                    result[f"{mkt_name}_over_money_pct"] = mkt.get("over_money",0)
            
            # Opening line vs current
            for bk in g.get("books",[]):
                if bk.get("book_id") in [15,30,123]:  # Pinnacle, Circa, Caesars
                    periods = bk.get("periods",{}).get("0",{})
                    result["open_spread"] = periods.get("spread",{}).get("open")
                    result["curr_spread"] = periods.get("spread",{}).get("current") 
                    result["open_total"]  = periods.get("total",{}).get("open")
                    result["curr_total"]  = periods.get("total",{}).get("current")
                    result["open_ml_h"]   = periods.get("money_line",{}).get("open_home")
                    result["curr_ml_h"]   = periods.get("money_line",{}).get("current_home")
                    break
            
            # Sharp % si está disponible (PRO)
            result["sharp_pct_home"]  = g.get("sharp_pct_home", 0)
            result["sharp_pct_away"]  = g.get("sharp_pct_away", 0)
            result["injuries"]        = [i.get("player","") + " " + i.get("status","") 
                                         for i in g.get("injuries",[])[:4]]
            result["consensus_pick"]  = g.get("consensus",{}).get("pick","")
            result["steam_move"]      = g.get("steam_move", False)
            result["reverse_move"]    = g.get("reverse_line_movement", False)
            
            return result
    except Exception as _e:
        pass
    return {}



# ══════════════════════════════════════════════════════════
# DETECTOR DE AMAÑO / MANIPULACIÓN DE PARTIDO
# "El mercado de apuestas mueve más dinero que el PIB de muchos países.
#  Donde hay tanto dinero, hay incentivos para manipular."
#
# Variables estudiadas en literatura académica:
# — Forrest & McHale (2019): patrones de cuota anómalos pre-partido
# — Hill (2010): ligas de riesgo alto identificadas en escándalos
# — Borghesi & Dare (2009): late line movement como señal de info privilegiada
# — Sportradar Fraud Detection System: metodología pública resumida
# ══════════════════════════════════════════════════════════

# Ligas con historial documentado de casos de amaño (fuente: FIFA TMS, Europol)
_HIGH_RISK_LEAGUES = {
    # ── MUY ALTO RIESGO ──
    "tur.1":  {"risk":90,"name":"Süper Lig","cases":"Fenerbahçe 2011, múltiples investigaciones UEFA"},
    "mex.1":  {"risk":85,"name":"Liga MX","cases":"Investigaciones CONADE, partidos sin sentido en descenso"},
    "bra.1":  {"risk":80,"name":"Brasileirão","cases":"Operação Jogo Sujo 2017, árbitros corruptos"},
    "arg.1":  {"risk":82,"name":"Liga Profesional","cases":"Múltiples casos AFA, presión del público en árbitros"},
    "chi.1":  {"risk":88,"name":"Primera División Chile","cases":"Caso ANFP 2015"},
    "col.1":  {"risk":83,"name":"Liga BetPlay","cases":"Historia de influencia del narcotráfico"},
    "ven.1":  {"risk":87,"name":"Liga FUTVE","cases":"Casos FIFA 2015"},
    "ecu.1":  {"risk":84,"name":"LigaPro","cases":"Investigaciones 2019"},
    "per.1":  {"risk":82,"name":"Liga 1","cases":"Casos árbitros 2018-2022"},
    "cor.k1": {"risk":75,"name":"K League 1","cases":"Escándalo masivo 2011 (130+ personas)"},
    "chn.1":  {"risk":88,"name":"CSL","cases":"Operación Whirlwind 2009, 30+ funcionarios"},
    "ita.2":  {"risk":72,"name":"Serie B","cases":"Calcioscommesse, Calciopoli investigación"},
    "spa.2":  {"risk":68,"name":"Segunda División","cases":"LaLiga corrupción árbitros 2014-2019"},
    # ── RIESGO MODERADO-ALTO ──
    "por.1":  {"risk":60,"name":"Primeira Liga","cases":"Caso Apito Dourado 2004"},
    "gre.1":  {"risk":65,"name":"Super League","cases":"Tribunal amaños 2019"},
    "pol.1":  {"risk":70,"name":"Ekstraklasa","cases":"Múltiples suspensiones FIFA 2005-2012"},
    "rou.1":  {"risk":65,"name":"Liga 1","cases":"Investigaciones FFR"},
    "tur.2":  {"risk":80,"name":"TFF 1.Lig","cases":"Derivado Fenerbahçe"},
    "mex.2":  {"risk":80,"name":"Liga de Expansión","cases":"Menor supervisión"},
    # ── RIESGO BAJO (ligas con mayor supervisión) ──
    "eng.1":  {"risk":15,"name":"Premier League","cases":"Controles estrictos FA + UKGC"},
    "ger.1":  {"risk":12,"name":"Bundesliga","cases":"BfV supervisión + DFL integridad"},
    "esp.1":  {"risk":20,"name":"LaLiga","cases":"RFEF controles mejorados post-2014"},
    "fra.1":  {"risk":18,"name":"Ligue 1","cases":"ANJ supervisión activa"},
    "ned.1":  {"risk":14,"name":"Eredivisie","cases":"Knvb + Sportradar"},
    "por.1":  {"risk":55,"name":"Primeira Liga","cases":"Mejoras post-2004"},
    "uefa.champions": {"risk":10,"name":"Champions League","cases":"UEFA supervisión máxima"},
}

# Señales de amaño en tenis documentadas por Tennis Integrity Unit
_TENNIS_RISK_SIGNALS = {
    "challenger": 70,  # Challengers tienen menos supervisión que ATP
    "itf":        85,  # Torneos ITF — menos controles, más casos documentados
    "atp250":     35,
    "atp500":     20,
    "atp1000":    12,
    "grand_slam": 8,
    "wta100":     30,
    "wta250":     55,
}

# NBA: Caso Tim Donaghy + patrones de arbitraje
_NBA_FIX_PATTERNS = {
    "playoff_game_7":     75,  # Incentivo económico máximo para extender series
    "playoff_game_6":     55,  # Segundo juego más lucrativo
    "tanking_team":       60,  # Equipos que pueden beneficiarse de perder
    "superstar_foul_out": 45,  # Partidos donde estrella foulería early = sospechoso
    "referee_flagged":    80,  # Árbitros con historial de anomalías (Donaghy metodología)
}

def analyze_fix_probability(sport, home, away, mc, dp, real_odds,
                             league_slug="", an_data=None, sbr_data=None,
                             line_snapshots=None, extra_context=None):
    """
    Detector de amaño multivariable.
    Score 0-100: 0 = partido limpio, 100 = señales de manipulación muy fuertes.
    
    Variables:
    1.  Liga de alto riesgo (historial documentado)
    2.  Movimiento de línea atípico / steam move tardío
    3.  Reverse line movement extremo sin justificación
    4.  Divergencia Pinnacle vs mercado blando > umbral crítico
    5.  % dinero vs % apuestas invertido (dinero oculto en un lado)
    6.  Cuotas anómalas vs modelo propio (probabilidad implícita imposible)
    7.  Partido sin incentivo (ya clasificado, ya descendido, muerto de tabla)
    8.  Cuota que baja a último momento sin noticias públicas
    9.  Equipo con viaje largo + rival descansado (favorece resultado dado)
    10. Árbitro con historial de partidos de alta varianza
    11. Patrón de resultado predecible que beneficia narrativa de audiencia
    12. Over/Under con movimiento exagerado (señal clásica de amaño de goles)
    13. Asian Handicap línea que no cierra bien (mercados asiáticos = sharps fijos)
    14. Horario inusual o estadio neutro (menos presión de público local)
    15. Jugadores clave con comportamiento atípico en cuotas individuales
    """
    signals   = []
    score     = 0
    
    # ── 1. LIGA DE RIESGO ──
    if sport == "soccer":
        league_data = _HIGH_RISK_LEAGUES.get(league_slug, {})
        league_risk = league_data.get("risk", 30)
        if league_risk >= 80:
            signals.append({
                "cat": "⚠️ Liga", "icon": "🌍",
                "label": f"Liga de ALTO RIESGO ({league_risk}/100)",
                "desc": f"{league_data.get('name',league_slug)}: {league_data.get('cases','Historial documentado')}",
                "color": "#ff4444", "weight": league_risk * 0.3
            })
            score += league_risk * 0.3
        elif league_risk >= 60:
            signals.append({
                "cat": "⚠️ Liga", "icon": "🟡",
                "label": f"Liga de riesgo moderado ({league_risk}/100)",
                "desc": league_data.get("cases","Casos previos documentados"),
                "color": "#ff9500", "weight": league_risk * 0.2
            })
            score += league_risk * 0.2
        elif league_risk <= 20:
            signals.append({
                "cat": "✅ Liga", "icon": "🛡️",
                "label": f"Liga de bajo riesgo ({league_risk}/100)",
                "desc": f"{league_data.get('name','')} — supervisión estricta",
                "color": "#00ff88", "weight": -10
            })
            score -= 10

    # ── 2. ANOMALÍA DE CUOTA MODELO ──
    if real_odds:
        pin = real_odds.get("pinnacle",{})
        pin_h = pin.get("h",0); pin_d = pin.get("d",0); pin_a = pin.get("a",0)
        if pin_h>1 and pin_d>1 and pin_a>1:
            # Probabilidades implícitas Pinnacle (sin margen)
            total_impl = 1/pin_h + 1/pin_d + 1/pin_a
            pin_ph = (1/pin_h)/total_impl
            pin_pa = (1/pin_a)/total_impl
            # Comparar con modelo
            model_ph = dp.get("ph", mc.get("ph",0.33))
            model_pa = dp.get("pa", mc.get("pa",0.33))
            gap_h = abs(model_ph - pin_ph)
            gap_a = abs(model_pa - pin_pa)
            max_gap = max(gap_h, gap_a)
            if max_gap > 0.20:
                signals.append({
                    "cat": "📊 Cuota", "icon": "🚨",
                    "label": f"Cuota imposible — gap {max_gap*100:.1f}%",
                    "desc": f"Pinnacle implica {pin_ph*100:.1f}% local vs nuestro modelo {model_ph*100:.1f}%. Diferencia > 20% es anómala.",
                    "color": "#ff4444", "weight": 25
                })
                score += 25
            elif max_gap > 0.12:
                signals.append({
                    "cat": "📊 Cuota", "icon": "⚡",
                    "label": f"Divergencia cuota-modelo notable ({max_gap*100:.1f}%)",
                    "desc": "Gap superior al umbral normal. Puede indicar información privilegiada en el mercado.",
                    "color": "#ff9500", "weight": 12
                })
                score += 12

    # ── 3. MOVIMIENTO DE LÍNEA TARDÍO ──
    if line_snapshots and len(line_snapshots) >= 3:
        snaps = line_snapshots
        # ¿El mayor movimiento ocurrió en las últimas 2 snapshots?
        pin_odds_list = [s["odds"].get("pinnacle",{}).get("h",0) for s in snaps]
        valid = [(i,o) for i,o in enumerate(pin_odds_list) if o>1]
        if len(valid) >= 3:
            early_move = abs(valid[len(valid)//2][1] - valid[0][1])
            late_move  = abs(valid[-1][1] - valid[len(valid)//2][1])
            if late_move > early_move * 2.5 and late_move > 0.08:
                signals.append({
                    "cat": "📈 Línea", "icon": "💨",
                    "label": "Steam move tardío detectado",
                    "desc": f"La línea se movió {late_move:.2f} en los últimos períodos vs {early_move:.2f} al principio. Dinero de última hora con información.",
                    "color": "#ff9500", "weight": 18
                })
                score += 18
            # ¿Movimiento pre-partido sin noticias? (criterio Sportradar)
            total_move = abs(valid[-1][1] - valid[0][1]) if valid else 0
            if total_move > 0.20:
                signals.append({
                    "cat": "📈 Línea", "icon": "🔴",
                    "label": f"Movimiento total extremo ({total_move:.2f})",
                    "desc": "Línea movió más de 0.20 puntos desde apertura. Sportradar reporta esto como señal de alerta primaria.",
                    "color": "#ff4444", "weight": 20
                })
                score += 20

    # ── 4. DINERO VS APUESTAS INVERTIDO (señal de apuesta coordinada) ──
    if an_data:
        bets_h  = an_data.get("ml_home_bets_pct",0) or an_data.get("spread_home_bets_pct",0)
        money_h = an_data.get("ml_home_money_pct",0) or an_data.get("spread_home_money_pct",0)
        if bets_h > 0 and money_h > 0:
            inversion = abs(bets_h - money_h)
            if inversion > 35 and money_h > bets_h:
                signals.append({
                    "cat": "💰 Dinero", "icon": "🎯",
                    "label": f"Inversión dinero/apuestas: {inversion:.0f}% gap",
                    "desc": f"{bets_h:.0f}% apuestas en local pero {money_h:.0f}% del DINERO. Apuestas grandes coordinadas en un lado.",
                    "color": "#ff4444", "weight": 22
                })
                score += 22
            elif inversion > 25:
                signals.append({
                    "cat": "💰 Dinero", "icon": "⚡",
                    "label": f"Discrepancia bets/money ({inversion:.0f}%)",
                    "desc": "Patrón típico de dinero sharp coordinado — no es comportamiento orgánico del público.",
                    "color": "#ff9500", "weight": 12
                })
                score += 12
        
        # Over/Under con movimiento exagerado — señal clásica de amaño de goles
        over_bets  = an_data.get("total_over_bets_pct",0)
        over_money = an_data.get("total_over_money_pct",0)
        if over_bets > 75 and over_money > 80:
            signals.append({
                "cat": "⚽ Goals", "icon": "🎭",
                "label": f"Over cargado ({over_bets:.0f}% bets, {over_money:.0f}% money)",
                "desc": "El mercado de totales está extremadamente cargado al Over. Señal de amaño de goles en ligas de riesgo.",
                "color": "#ff9500", "weight": 15
            })
            score += 15

    # ── 5. PÚBLICO MUY CARGADO (herramienta de los fijadores) ──
    if sbr_data:
        h_pct = sbr_data.get("home_pct",50)
        # El favorito público extremo es una herramienta: si el partido está amañado
        # a favor del underdog, los fijadores se benefician del lado contrario al público
        if h_pct > 80:
            signals.append({
                "cat": "👥 Público", "icon": "👥",
                "label": f"Público extremo en local ({h_pct:.0f}%)",
                "desc": "Favorito masivo del público. Los fijadores históricamente explotan estos partidos para apostar al underdog con cuotas infladas.",
                "color": "#ff9500", "weight": 10
            })
            score += 10
        elif h_pct < 20:
            signals.append({
                "cat": "👥 Público", "icon": "👥",
                "label": f"Público extremo en visitante ({100-h_pct:.0f}%)",
                "desc": "El público masivamente contra el local. Patrón de riesgo si la liga tiene historial.",
                "color": "#ff9500", "weight": 8
            })
            score += 8

    # ── 6. PARTIDO SIN INCENTIVO DEPORTIVO ──
    if extra_context:
        if extra_context.get("home_already_qualified") or extra_context.get("away_already_qualified"):
            signals.append({
                "cat": "🏆 Contexto", "icon": "😴",
                "label": "Equipo sin nada en juego",
                "desc": "Un equipo ya clasificado/descendido tiene menor motivación. Históricamente estos partidos tienen más anomalías.",
                "color": "#ff9500", "weight": 15
            })
            score += 15
        if extra_context.get("season_finale"):
            signals.append({
                "cat": "🏆 Contexto", "icon": "📅",
                "label": "Última jornada de temporada",
                "desc": "Las últimas jornadas históricamente concentran más casos de amaño por temas de descenso/clasificación.",
                "color": "#ff9500", "weight": 12
            })
            score += 12

    # ── 7. SPORT-SPECIFIC ──
    if sport == "tennis":
        # Tenis: más fácil amañar que equipos (solo un jugador necesario)
        # "Tanking" un set o partido entero — mercado asiático lo detecta primero
        if real_odds:
            # Buscar cuota inusualmente baja para el ranking
            for bk_odds in real_odds.values():
                if isinstance(bk_odds, dict):
                    p1_odd = bk_odds.get("p1",0) or bk_odds.get("h",0)
                    p2_odd = bk_odds.get("p2",0) or bk_odds.get("a",0)
                    if p1_odd>1 and p2_odd>1:
                        ratio = max(p1_odd,p2_odd)/min(p1_odd,p2_odd)
                        if ratio > 8:  # Favorito con cuota menor a 1.15 es sospechoso en tenis
                            signals.append({
                                "cat": "🎾 Tenis", "icon": "🎾",
                                "label": f"Cuota extrema en tenis ({min(p1_odd,p2_odd):.2f})",
                                "desc": "Favoritos con cuota < 1.15 en tenis tienen mayor riesgo de no-tanking (la cuota en sí incentiva al underdog a amañar).",
                                "color": "#ff9500", "weight": 20
                            })
                            score += 20
                            break
        # Torneos de bajo nivel siempre en alerta
        signals.append({
            "cat": "🎾 Tenis", "icon": "🎾",
            "label": "Deporte de alto riesgo de amaño individual",
            "desc": "Tenis: basta 1 jugador. Tennis Integrity Unit investigó 174 jugadores 2023. Mercado asiático en tiempo real detecta anomalías antes que cualquier sistema.",
            "color": "#ff9500", "weight": 12
        })
        score += 12

    if sport == "nba":
        # NBA: árbitros tienen poder enorme. Caso Donaghy documentado.
        signals.append({
            "cat": "🏀 NBA", "icon": "🏀",
            "label": "NBA: factor arbitraje endémico",
            "desc": "Tim Donaghy (2007) demostró que árbitros pueden controlar resultados. La NBA no ha implementado supervisión externa independiente desde entonces.",
            "color": "#ff9500", "weight": 8
        })
        score += 8
        # Playoff = más incentivo económico
        if extra_context and extra_context.get("is_playoff"):
            signals.append({
                "cat": "🏀 NBA", "icon": "🏆",
                "label": "Playoffs — incentivo económico máximo",
                "desc": "Alargar series de playoffs genera ~$25M extra por juego en ingresos de TV/arena. Patrón histórico de series largas.",
                "color": "#ff9500", "weight": 15
            })
            score += 15

    # ── 8. CUOTA OVER/UNDER — señal de amaño de marcador ──
    if real_odds and sport == "soccer":
        pin = real_odds.get("pinnacle",{})
        # Si el Over/Under tiene movimiento sin razón estadística
        mc_o25 = mc.get("o25",0.5) if mc else 0.5
        # Buscar total line en AN data
        if an_data:
            curr_total = an_data.get("curr_total",0)
            open_total = an_data.get("open_total",0)
            if curr_total and open_total and abs(curr_total-open_total) > 0.25:
                signals.append({
                    "cat": "⚽ O/U", "icon": "🎯",
                    "label": f"Línea total movió {abs(curr_total-open_total):.2f} goles",
                    "desc": "Movimiento en Over/Under sin cambio en pronóstico de goles es señal clásica de amaño de marcador.",
                    "color": "#ff4444", "weight": 18
                })
                score += 18

    # ── 9. SEÑAL DE ACTION NETWORK STEAM/REVERSE ──
    if an_data:
        if an_data.get("steam_move"):
            signals.append({
                "cat": "💨 Steam", "icon": "💨",
                "label": "Steam Move confirmado por Action Network",
                "desc": "Action Network detectó entrada coordinada de dinero en poco tiempo. Puede ser sharps legítimos o información privilegiada.",
                "color": "#aa00ff", "weight": 15
            })
            score += 15
        if an_data.get("reverse_move"):
            signals.append({
                "cat": "🔄 RLM", "icon": "🔄",
                "label": "Reverse Line Movement confirmado (AN)",
                "desc": "Dinero mayoritario en un lado pero línea mueve al otro. Señal de dinero con ventaja de información.",
                "color": "#00ccff", "weight": 20
            })
            score += 20

    # ── SCORE FINAL ──
    score = min(100, max(0, score))
    
    # Veredicto + disclaimer
    if score >= 75:
        verdict = "🚨 SEÑALES MUY FUERTES — MÁXIMA SOSPECHA"
        vc = "#ff4444"
        advice = "Evitar apostar. Si se apuesta, asumir que el resultado puede estar predeterminado."
    elif score >= 55:
        verdict = "⚠️ SEÑALES MODERADAS — ALTA SOSPECHA"
        vc = "#ff9500"
        advice = "Reducir stake al mínimo. No usar en parlays. Monitorear movimientos de última hora."
    elif score >= 35:
        verdict = "🟡 SEÑALES LEVES — PRECAUCIÓN"
        vc = "#FFD700"
        advice = "Partido con factores de riesgo. Apostar solo con edge muy claro (>8%)."
    elif score >= 15:
        verdict = "🟢 BAJO RIESGO — SEÑALES NORMALES"
        vc = "#00ccff"
        advice = "Sin anomalías detectadas. Factores de riesgo estándar."
    else:
        verdict = "✅ PARTIDO LIMPIO"
        vc = "#00ff88"
        advice = "Todas las señales dentro de rangos normales."

    return {
        "signals": signals,
        "score": score,
        "verdict": verdict,
        "verdict_color": vc,
        "advice": advice,
        "sport": sport,
    }


def render_fix_detector(sport, home, away, mc, dp, real_odds, game,
                        an_data=None, sbr_data=None, line_snapshots=None):
    """
    Renderiza el detector de amaño en la UI.
    Incluye disclaimer legal claro.
    """
    st.markdown("<div class='shdr'>🔍 DETECTOR DE ANOMALÍAS DE MERCADO</div>", unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown(
        "<div style='background:#1a0a00;border:1px solid #ff440033;border-radius:10px;"
        "padding:10px 16px;margin:4px 0 10px;font-size:.72rem;color:#ff9500'>"
        "⚖️ <b>AVISO:</b> Este análisis detecta anomalías estadísticas en mercados de apuestas. "
        "No acusa a ningún equipo, jugador o árbitro específico. Las señales son indicadores de "
        "comportamiento inusual del mercado, no prueba de manipulación. Basado en metodología "
        "académica pública (Forrest, Hill, Sportradar FDS)."
        "</div>", unsafe_allow_html=True)
    
    league_slug = game.get("slug","")
    extra = {
        "is_playoff": game.get("state","") == "post" or "playoff" in str(game.get("league","")).lower(),
    }
    
    analysis = analyze_fix_probability(
        sport=sport, home=home, away=away,
        mc=mc, dp=dp, real_odds=real_odds,
        league_slug=league_slug,
        an_data=an_data, sbr_data=sbr_data,
        line_snapshots=line_snapshots,
        extra_context=extra
    )
    
    sc = analysis["score"]
    vc = analysis["verdict_color"]
    
    # ── Score visual ──
    # Medidor estilo termómetro
    bar_pct = sc  # 0-100
    bar_color = vc
    
    # Color gradient based on score
    if sc < 20: grd = "linear-gradient(90deg,#00ff88,#00ccff)"
    elif sc < 40: grd = "linear-gradient(90deg,#00ccff,#FFD700)"
    elif sc < 60: grd = "linear-gradient(90deg,#FFD700,#ff9500)"
    else: grd = "linear-gradient(90deg,#ff9500,#ff4444)"
    
    st.markdown(
        f"<div style='background:#0d0d2e;border:2px solid {vc}44;border-radius:16px;padding:20px 22px;margin:8px 0'>"
        f"<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px'>"
        f"<div>"
        f"<div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.12em;margin-bottom:4px'>ÍNDICE DE ANOMALÍA DE MERCADO</div>"
        f"<div style='font-size:1rem;font-weight:900;color:{vc}'>{analysis['verdict']}</div>"
        f"</div>"
        f"<div style='text-align:center'>"
        f"<div style='font-size:2.4rem;font-weight:900;color:{vc};line-height:1'>{sc:.0f}</div>"
        f"<div style='font-size:.65rem;color:#555'>/100</div>"
        f"</div>"
        f"</div>"
        # Progress bar
        f"<div style='background:#1a1a40;border-radius:6px;height:12px;overflow:hidden;margin:10px 0'>"
        f"<div style='width:{bar_pct}%;height:100%;background:{grd};border-radius:6px;transition:.4s'></div>"
        f"</div>"
        f"<div style='display:flex;justify-content:space-between;font-size:.65rem;color:#444;margin-bottom:12px'>"
        f"<span>0 — Limpio</span><span>25 — Bajo</span><span>50 — Medio</span><span>75 — Alto</span><span>100 — Crítico</span>"
        f"</div>"
        # Advice
        f"<div style='background:#12122a;border-radius:8px;padding:10px 14px;font-size:.8rem;color:#aaa'>"
        f"💡 <b style='color:#EEEEFF'>Recomendación:</b> {analysis['advice']}"
        f"</div>"
        f"</div>", unsafe_allow_html=True)
    
    # ── Señales ──
    if analysis["signals"]:
        # Agrupar por categoría
        by_cat = {}
        for sig in analysis["signals"]:
            cat = sig["cat"]
            if cat not in by_cat: by_cat[cat] = []
            by_cat[cat].append(sig)
        
        for cat, sigs in by_cat.items():
            with st.expander(f"{cat} — {len(sigs)} señal{'es' if len(sigs)>1 else ''}", expanded=sc>=40):
                for sig in sigs:
                    st.markdown(
                        f"<div style='background:#07071a;border-left:3px solid {sig['color']};"
                        f"border-radius:0 8px 8px 0;padding:10px 14px;margin:4px 0;"
                        f"display:flex;gap:10px;align-items:flex-start'>"
                        f"<div style='font-size:1.1rem;min-width:24px'>{sig['icon']}</div>"
                        f"<div><div style='font-weight:700;font-size:.83rem;color:{sig['color']}'>{sig['label']}</div>"
                        f"<div style='font-size:.75rem;color:#888;margin-top:3px;line-height:1.5'>{sig['desc']}</div>"
                        f"</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='color:#555;font-size:.83rem;padding:10px;text-align:center'>"
            "✅ Sin señales anómalas detectadas en este partido.</div>", unsafe_allow_html=True)
    
    # ── IA Investigadora ──
    render_ai_investigation(
        sport=sport, home=home, away=away,
        league_slug=league_slug,
        league_name=_HIGH_RISK_LEAGUES.get(league_slug,{}).get("name", league_slug or sport),
        dp=dp, mc=mc, real_odds=real_odds,
        fix_score=sc
    )
    # ── Fuentes bibliográficas ──
    with st.expander("📚 Metodología y fuentes académicas"):
        st.markdown(
            "<div style='font-size:.75rem;color:#555;line-height:1.8'>"
            "• <b style='color:#aaa'>Forrest & McHale (2019)</b> — Identificación de patrones de cuota anómalos pre-partido<br>"
            "• <b style='color:#aaa'>Hill (2010)</b> — Football match manipulation and the wider criminological context<br>"
            "• <b style='color:#aaa'>Borghesi & Dare (2009)</b> — Late line movement como señal de información privilegiada<br>"
            "• <b style='color:#aaa'>Wolfers (2006)</b> — Point shaving en baloncesto universitario (metodología)<br>"
            "• <b style='color:#aaa'>Sportradar FDS</b> — Fraud Detection System, metodología pública resumida<br>"
            "• <b style='color:#aaa'>Europol (2013)</b> — 425 partidos sospechosos en 15 países, 680 personas involucradas<br>"
            "• <b style='color:#aaa'>Tennis Integrity Unit (2023)</b> — 174 jugadores investigados, mercado asiático como señal principal<br>"
            "• <b style='color:#aaa'>Caso Donaghy (2007)</b> — NBA, árbitro Tim Donaghy, metodología de detección posterior"
            "</div>", unsafe_allow_html=True)


@st.cache_data(ttl=1800, show_spinner=False)
def ai_investigate_match(sport, home, away, league_slug, league_name,
                          model_ph, model_pd, model_pa,
                          real_odds_summary, fix_score):
    """
    Claude investiga el partido específico:
    1. Historial de amaños/escándalos documentados en la liga
    2. Antecedentes de los equipos en partidos sospechosos
    3. Contexto del partido (posición tabla, motivación)
    4. Estimación de sharp money cuando no hay datos directos
    5. Veredicto final con nivel de confianza
    """
    if not ANTHROPIC_API_KEY: return {}
    
    prompt = f"""Eres un analista de integridad deportiva y mercados de apuestas. 
Investiga este partido y responde SOLO en JSON válido sin texto adicional ni backticks.

PARTIDO: {home} vs {away}
LIGA: {league_name} ({league_slug})
DEPORTE: {sport}
MODELO: Local {model_ph*100:.1f}% / Empate {model_pd*100:.1f}% / Visita {model_pa*100:.1f}%
CUOTAS DISPONIBLES: {real_odds_summary}
SCORE ANOMALÍA PREVIO: {fix_score}/100

INVESTIGA Y RESPONDE EN JSON:
{{
  "league_integrity": {{
    "risk_score": <0-100>,
    "known_cases": "<casos documentados de amaño en esta liga, escándalos FIFA/UEFA/Europol>",
    "supervision_level": "<alta/media/baja>",
    "last_scandal": "<año y descripción del último escándalo conocido>"
  }},
  "team_flags": {{
    "home_flags": "<cualquier historial sospechoso del equipo local, deudas, problemas financieros, presión de resultados>",
    "away_flags": "<igual para visitante>",
    "rivalry_context": "<contexto de la rivalidad y si hay presiones externas>"
  }},
  "match_context": {{
    "sporting_incentive": "<ambos necesitan ganar/uno sin nada en juego/partido muerto>",
    "fixture_risk": "<es final de temporada, playoff, partido de descenso?>",
    "referee_concern": "<árbitros de esta liga tienen historial de anomalías?>"
  }},
  "sharp_money_estimate": {{
    "estimated_public_pct_home": <0-100>,
    "estimated_sharp_pct_home": <0-100>,
    "estimated_line_direction": "<hacia local/hacia visitante/sin movimiento>",
    "confidence": "<alta/media/baja>",
    "reasoning": "<por qué estimas este movimiento de sharp money basado en cuotas disponibles y contexto>"
  }},
  "manipulation_probability": {{
    "score": <0-100>,
    "primary_risk": "<principal factor de riesgo>",
    "verdict": "<LIMPIO/BAJO RIESGO/PRECAUCIÓN/ALTO RIESGO/CRÍTICO>",
    "recommendation": "<qué hacer con este partido desde perspectiva de apuestas>"
  }},
  "market_intelligence": {{
    "asian_handicap_signal": "<qué implican las cuotas asiáticas si puedes inferirlo>",
    "closing_line_prediction": "<hacia dónde esperas que cierre la línea>",
    "best_market": "<qué mercado tiene más valor en este partido: 1X2/Over-Under/AH>"
  }}
}}

Sé directo y específico. Si no tienes datos concretos, usa tu conocimiento de la liga y el contexto.
Para sharp_money_estimate: usa las cuotas disponibles para inferir dónde está el dinero inteligente."""

    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1200,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=20
        )
        if r.status_code != 200: return {}
        raw = r.json()["content"][0]["text"].strip()
        raw = raw.replace("```json","").replace("```","").strip()
        import json as _j
        return _j.loads(raw)
    except Exception as _e:
        return {}


def render_ai_investigation(sport, home, away, league_slug, league_name,
                             dp, mc, real_odds, fix_score):
    """
    Renderiza la investigación IA del partido.
    Muestra: integridad de liga · flags de equipos · sharp money estimado · veredicto IA
    """
    st.markdown("<div class='shdr'>🤖 IA INVESTIGADORA — ANÁLISIS PROFUNDO</div>",
                unsafe_allow_html=True)
    
    # Construir resumen de cuotas para el prompt
    odds_summary = "Sin cuotas disponibles"
    if real_odds:
        parts = []
        for bk, odds in list(real_odds.items())[:4]:
            if isinstance(odds, dict) and odds.get("h",0) > 1:
                parts.append(f"{bk}: {odds.get('h',0):.2f}/{odds.get('d',0):.2f}/{odds.get('a',0):.2f}")
        if parts: odds_summary = " | ".join(parts)
    
    model_ph = dp.get("ph", mc.get("ph", 0.33)) if dp else mc.get("ph", 0.33)
    model_pd = dp.get("pd", mc.get("pd", 0.33)) if dp else mc.get("pd", 0.33)
    model_pa = dp.get("pa", mc.get("pa", 0.33)) if dp else mc.get("pa", 0.33)
    
    with st.spinner("🔍 IA investigando partido, liga e historial..."):
        inv = ai_investigate_match(
            sport, home, away, league_slug, league_name,
            model_ph, model_pd, model_pa,
            odds_summary, fix_score
        )
    
    if not inv:
        st.markdown(
            "<div style='background:#0d0d2e;border:1px solid #252555;border-radius:12px;"
            "padding:14px 18px;color:#555;font-size:.85rem'>"
            "⚠️ IA no disponible. Verifica ANTHROPIC_API_KEY en Streamlit secrets."
            "</div>", unsafe_allow_html=True)
        return
    
    # ── VEREDICTO IA ──
    manip = inv.get("manipulation_probability", {})
    ai_score = manip.get("score", 0)
    ai_verdict = manip.get("verdict", "N/D")
    ai_rec = manip.get("recommendation", "")
    ai_risk = manip.get("primary_risk", "")
    
    vc_map = {
        "LIMPIO": "#00ff88", "BAJO RIESGO": "#00ccff",
        "PRECAUCIÓN": "#FFD700", "ALTO RIESGO": "#ff9500", "CRÍTICO": "#ff4444"
    }
    vc = vc_map.get(ai_verdict, "#aaa")
    
    if ai_score < 20: grd = "linear-gradient(90deg,#00ff88,#00ccff)"
    elif ai_score < 40: grd = "linear-gradient(90deg,#00ccff,#FFD700)"
    elif ai_score < 60: grd = "linear-gradient(90deg,#FFD700,#ff9500)"
    else: grd = "linear-gradient(90deg,#ff9500,#ff4444)"
    
    st.markdown(
        f"<div style='background:#0d0d2e;border:2px solid {vc}55;border-radius:16px;"
        f"padding:18px 22px;margin:8px 0'>"
        f"<div style='font-size:.65rem;color:#555;font-weight:700;letter-spacing:.14em;margin-bottom:6px'>"
        f"🤖 INTELIGENCIA ARTIFICIAL — VEREDICTO</div>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'>"
        f"<div style='font-size:1.1rem;font-weight:900;color:{vc}'>{ai_verdict}</div>"
        f"<div style='font-size:2rem;font-weight:900;color:{vc}'>{ai_score}</div>"
        f"</div>"
        f"<div style='background:#1a1a40;border-radius:6px;height:8px;overflow:hidden;margin-bottom:12px'>"
        f"<div style='width:{min(ai_score,100)}%;height:8px;background:{grd};border-radius:6px'></div>"
        f"</div>"
        f"<div style='font-size:.78rem;color:#aaa;margin-bottom:6px'>"
        f"⚠️ <b style='color:#ff9500'>Riesgo principal:</b> {ai_risk}</div>"
        f"<div style='background:#12122a;border-radius:8px;padding:10px 14px;font-size:.8rem;color:#aaa'>"
        f"💡 {ai_rec}</div>"
        f"</div>", unsafe_allow_html=True)
    
    # ── INTEGRIDAD DE LIGA ──
    lig = inv.get("league_integrity", {})
    if lig:
        lig_score = lig.get("risk_score", 0)
        lig_c = "#ff4444" if lig_score>=70 else ("#ff9500" if lig_score>=45 else "#00ff88")
        with st.expander(f"🌍 Integridad de Liga — Riesgo {lig_score}/100", expanded=lig_score>=45):
            st.markdown(
                f"<div style='font-size:.8rem;line-height:1.8;color:#aaa'>"
                f"<div style='margin-bottom:8px'>"
                f"<b style='color:{lig_c}'>Score de riesgo: {lig_score}/100</b> · "
                f"Supervisión: <b style='color:#EEEEFF'>{lig.get('supervision_level','N/D').upper()}</b></div>"
                f"<div style='margin-bottom:6px'>📋 <b style='color:#EEEEFF'>Casos conocidos:</b> "
                f"{lig.get('known_cases','Sin datos')}</div>"
                f"<div>🗓️ <b style='color:#EEEEFF'>Último escándalo:</b> "
                f"{lig.get('last_scandal','No documentado')}</div>"
                f"</div>", unsafe_allow_html=True)
    
    # ── FLAGS DE EQUIPOS ──
    teams = inv.get("team_flags", {})
    if teams:
        home_flag = teams.get("home_flags","")
        away_flag = teams.get("away_flags","")
        rivalry   = teams.get("rivalry_context","")
        if any([home_flag, away_flag, rivalry]):
            with st.expander("🚩 Flags de Equipos"):
                for label, val, icon in [
                    (home, home_flag, "🏠"),
                    (away, away_flag, "✈️"),
                    ("Contexto del partido", rivalry, "⚽")
                ]:
                    if val and val.lower() not in ["n/a","ninguno","sin datos","none",""]:
                        st.markdown(
                            f"<div style='background:#07071a;border-left:3px solid #ff950055;"
                            f"border-radius:0 8px 8px 0;padding:10px 14px;margin:4px 0;"
                            f"font-size:.8rem;color:#aaa'>"
                            f"<b style='color:#ff9500'>{icon} {label}:</b> {val}</div>",
                            unsafe_allow_html=True)
    
    # ── CONTEXTO DEL PARTIDO ──
    ctx = inv.get("match_context", {})
    if ctx:
        incentive = ctx.get("sporting_incentive","")
        fixture   = ctx.get("fixture_risk","")
        ref       = ctx.get("referee_concern","")
        if incentive or fixture:
            with st.expander("🏆 Contexto Deportivo"):
                for label, val, icon in [
                    ("Incentivo deportivo", incentive, "🎯"),
                    ("Contexto del fixture", fixture, "📅"),
                    ("Árbitros", ref, "🟨")
                ]:
                    if val:
                        st.markdown(
                            f"<div style='font-size:.8rem;color:#aaa;padding:6px 0;"
                            f"border-bottom:1px solid #1a1a40'>"
                            f"<b style='color:#EEEEFF'>{icon} {label}:</b> {val}</div>",
                            unsafe_allow_html=True)
    
    # ── SHARP MONEY ESTIMADO IA ──
    sharp = inv.get("sharp_money_estimate", {})
    if sharp:
        est_pub  = sharp.get("estimated_public_pct_home", 0)
        est_shrp = sharp.get("estimated_sharp_pct_home", 0)
        line_dir = sharp.get("estimated_line_direction", "")
        conf     = sharp.get("confidence", "")
        reason   = sharp.get("reasoning", "")
        conf_c   = "#00ff88" if conf=="alta" else ("#FFD700" if conf=="media" else "#aaa")
        
        st.markdown(
            f"<div style='background:#0d0d2e;border:1px solid #aa00ff44;border-radius:14px;"
            f"padding:16px 20px;margin:8px 0'>"
            f"<div style='font-size:.7rem;color:#aa00ff;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>"
            f"🦅 SHARP MONEY ESTIMADO POR IA</div>"
            f"<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px'>"
            # Público estimado
            f"<div style='background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
            f"<div style='font-size:.65rem;color:#555;margin-bottom:4px'>👥 PÚBLICO LOCAL</div>"
            f"<div style='font-size:1.6rem;font-weight:900;color:#aaa'>{est_pub:.0f}%</div></div>"
            # Sharp estimado
            f"<div style='background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
            f"<div style='font-size:.65rem;color:#555;margin-bottom:4px'>🦅 SHARP LOCAL</div>"
            f"<div style='font-size:1.6rem;font-weight:900;color:#aa00ff'>{est_shrp:.0f}%</div></div>"
            # Confianza
            f"<div style='background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
            f"<div style='font-size:.65rem;color:#555;margin-bottom:4px'>📊 CONFIANZA</div>"
            f"<div style='font-size:1.1rem;font-weight:900;color:{conf_c}'>{conf.upper()}</div></div>"
            f"</div>"
            # Dirección de línea
            + (f"<div style='background:#12122a;border-radius:8px;padding:8px 12px;"
               f"margin-bottom:10px;font-size:.78rem;color:#00ccff'>"
               f"📈 Línea esperada: <b>{line_dir}</b></div>" if line_dir else "")
            # Razonamiento
            + (f"<div style='font-size:.78rem;color:#888;line-height:1.6'>"
               f"💭 {reason}</div>" if reason else "")
            + f"<div style='margin-top:8px;font-size:.65rem;color:#444'>"
            f"⚠️ Estimación IA — no datos reales. Confianza: {conf}</div>"
            f"</div>", unsafe_allow_html=True)
    
    # ── MARKET INTELLIGENCE ──
    mkt = inv.get("market_intelligence", {})
    if mkt:
        ah     = mkt.get("asian_handicap_signal","")
        cl_pred= mkt.get("closing_line_prediction","")
        best_m = mkt.get("best_market","")
        if any([ah, cl_pred, best_m]):
            with st.expander("📈 Inteligencia de Mercado"):
                for label, val, icon in [
                    ("Señal Asian Handicap", ah, "🀄"),
                    ("Predicción cierre de línea", cl_pred, "🎯"),
                    ("Mercado con más valor", best_m, "💰")
                ]:
                    if val:
                        st.markdown(
                            f"<div style='font-size:.82rem;color:#aaa;padding:8px 0;"
                            f"border-bottom:1px solid #1a1a40'>"
                            f"<b style='color:#00ccff'>{icon} {label}:</b> {val}</div>",
                            unsafe_allow_html=True)

def render_sharp_money(home, away, dp, mc, real_odds, game):
    """
    Sección completa de Sharp Money Intelligence en el partido.
    Muestra: señales detectadas · score · veredicto · CLV · line movement
    """
    st.markdown("<div class='shdr'>🦅 SHARP MONEY INTELLIGENCE</div>", unsafe_allow_html=True)
    
    if not real_odds:
        st.markdown(
            "<div style='background:#0d0d2e;border:1px solid #252555;border-radius:12px;"
            "padding:14px 18px;color:#555;font-size:.85rem'>"
            "🔌 Conecta <b style='color:#EEEEFF'>The Odds API</b> para activar el Sharp Money detector. "
            "Detectará: Steam moves · Reverse line movement · CLV · Divergencia sharp vs público."
            "</div>", unsafe_allow_html=True)
        return

    # Track la línea actual
    game_id = game.get("id","")
    snapshots = track_line_movement(game_id, home, away, real_odds)

    # ── Enriquecer real_odds con datos live de Betfair + SBR ──
    league_slug = game.get("slug","")
    sbr_data = get_sbr_public_betting(home, away, "soccer")

    # Análisis completo
    analysis = analyze_line_movement(home, away, real_odds, dp["ph"])
    
    # ── Score bar ──
    sc = analysis["score"]
    bar_w = min(100, abs(sc))
    bar_color = analysis["verdict_color"]
    bar_dir = "left" if sc < 0 else "right"
    
    st.markdown(
        f"<div style='background:#0d0d2e;border:1px solid #252555;border-radius:16px;padding:20px 22px;margin:8px 0'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px'>"
        f"<div style='font-size:1rem;font-weight:900;color:{bar_color}'>{analysis['verdict']}</div>"
        f"<div style='font-size:1.6rem;font-weight:900;color:{bar_color}'>{'+' if sc>0 else ''}{sc}</div>"
        f"</div>"
        f"<div style='background:#1a1a40;border-radius:6px;height:10px;overflow:hidden;margin-bottom:14px;position:relative'>"
        f"<div style='position:absolute;left:50%;top:0;bottom:0;width:1px;background:#252555'></div>"
        f"<div style='position:absolute;{'right:50%' if sc<0 else 'left:50%'};top:0;bottom:0;"
        f"width:{bar_w/2}%;background:{bar_color};opacity:.8'></div>"
        f"</div>"
        f"<div style='display:flex;justify-content:space-between;font-size:.68rem;color:#555'>"
        f"<span>🚫 Trampa pública</span><span>⚖️ Neutral</span><span>🦅 Sharp money</span></div>"
        f"</div>", unsafe_allow_html=True)

    # ── Señales detectadas ──
    if analysis["signals"]:
        for sig in analysis["signals"]:
            st.markdown(
                f"<div style='background:#07071a;border:1px solid {sig['color']}33;"
                f"border-left:3px solid {sig['color']};border-radius:10px;"
                f"padding:10px 16px;margin:5px 0;display:flex;gap:12px;align-items:flex-start'>"
                f"<div style='font-size:1.2rem'>{sig['icon']}</div>"
                f"<div><div style='font-weight:700;font-size:.85rem;color:{sig['color']}'>{sig['label']}</div>"
                f"<div style='font-size:.78rem;color:#aaa;margin-top:2px'>{sig['desc']}</div></div>"
                f"</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='color:#555;font-size:.83rem;padding:10px'>⏳ Acumulando datos de línea... "
            "Las señales aparecerán conforme el mercado se mueva.</div>", unsafe_allow_html=True)

    # ── SBR % público ──
    if sbr_data:
        h_pct = sbr_data.get("home_pct", 0)
        a_pct = sbr_data.get("away_pct", 0)
        if h_pct or a_pct:
            hc = "#00ff88" if h_pct > 55 else ("#ff4444" if h_pct < 35 else "#FFD700")
            st.markdown(
                f"<div style='background:#0d0d2e;border:1px solid #252555;border-radius:10px;"
                f"padding:12px 16px;margin:6px 0'>"
                f"<div style='font-size:.7rem;color:#555;font-weight:700;margin-bottom:8px'>👥 % APUESTAS PÚBLICAS (SportsBookReview)</div>"
                f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>"
                f"<div style='text-align:center'><div style='font-size:1.4rem;font-weight:900;color:{hc}'>{h_pct:.0f}%</div>"
                f"<div style='font-size:.72rem;color:#aaa'>{home[:14]}</div></div>"
                f"<div style='text-align:center'><div style='font-size:1.4rem;font-weight:900;color:#aaa'>{a_pct:.0f}%</div>"
                f"<div style='font-size:.72rem;color:#aaa'>{away[:14]}</div></div></div>"
                f"<div style='margin-top:8px;font-size:.7rem;color:#555'>"
                f"{'⚠️ Público muy cargado en local — fade the public' if h_pct>70 else ('⚠️ Público muy cargado en visitante — fade the public' if h_pct<30 else '⚖️ Apuestas divididas')}</div>"
                f"</div>", unsafe_allow_html=True)


def render_odds_comparison(home, away, dp, mc, real_odds):
    """Tabla de valor esperado comparando modelo vs casas."""
    st.markdown("<div class='shdr'>💰 Valor Esperado vs Casas de Apuestas</div>", unsafe_allow_html=True)
    
    if not real_odds:
        # Sin Odds API — mostrar mensaje con links visibles y dark input
        st.markdown(
            "<div style='background:#0d0d2e;border:1px solid #7c00ff44;border-radius:14px;"
            "padding:16px 20px'>"
            "<div style='font-size:.78rem;color:#7c00ff;font-weight:700;letter-spacing:.1em;"
            "margin-bottom:10px'>💰 CONECTA ODDS EN TIEMPO REAL</div>"
            "<div style='font-size:.88rem;color:#aaa;line-height:1.6'>"
            "Conecta <b style='color:#EEEEFF'>The Odds API</b> para comparar vs "
            "<b style='color:#FFD700'>Bet365</b>, <b style='color:#FFD700'>Pinnacle</b> y más.<br>"
            "<span style='color:#555'>Plan gratis: 500 requests/mes — más que suficiente.</span>"
            "</div>"
            "<div style='margin-top:12px;display:flex;gap:10px;flex-wrap:wrap'>"
            "<a href='https://the-odds-api.com' target='_blank' "
            "style='background:linear-gradient(135deg,#7c00ff,#00ccff);color:#fff!important;"
            "padding:8px 18px;border-radius:10px;font-weight:700;font-size:.85rem;"
            "text-decoration:none'>🔗 Registrarse gratis</a>"
            "</div></div>"
            , unsafe_allow_html=True)
        # Input para pegar key — dark styled
        _new_key = st.text_input(
            "🔑 Pega tu API Key aquí",
            value=ODDS_API_KEY,
            placeholder="ej: a1b2c3d4e5f6...",
            type="password",
            key="odds_key_input",
            help="Cópiala de the-odds-api.com → Dashboard"
        )
        if _new_key and _new_key != ODDS_API_KEY:
            st.session_state["runtime_odds_key"] = _new_key
            st.success("✅ Key guardada en sesión. Abre un partido para ver odds en vivo.")
            st.rerun()
        return

    probs = {"Local gana": dp["ph"], "Empate": dp["pd"], "Visita gana": dp["pa"]}
    bk_names = {"bet365":"Bet365","pinnacle":"Pinnacle","unibet":"Unibet","williamhill":"William Hill"}
    
    header = (f"<div style='background:#0d0d2e;border:1px solid #252555;border-radius:14px;overflow:hidden'>"
              f"<div style='display:grid;grid-template-columns:120px repeat({len(real_odds)+2},1fr);"
              f"gap:0;padding:10px 14px;background:#12123a;font-size:.75rem;font-weight:700;color:#555'>"
              f"<span>Resultado</span><span>Modelo</span>")
    for bk in real_odds: header += f"<span>{bk_names.get(bk,bk[:8])}</span>"
    header += "<span>Mejor Edge</span></div>"
    st.markdown(header, unsafe_allow_html=True)

    for label, prob in probs.items():
        key = "h" if "Local" in label else ("d" if "Empate" in label else "a")
        best_edge = 0; best_bk = ""
        row = (f"<div style='display:grid;grid-template-columns:120px repeat({len(real_odds)+2},1fr);"
               f"gap:0;padding:10px 14px;border-top:1px solid #151530;align-items:center'>")
        row += f"<span style='font-weight:700;font-size:.85rem'>{label}</span>"
        row += f"<span style='color:#7c00ff;font-weight:700'>{prob*100:.1f}%</span>"
        for bk, odds in real_odds.items():
            odd = odds.get(key, 0)
            if odd > 1:
                impl  = 1/odd
                edge  = prob - impl
                color = "#00ff88" if edge > 0.05 else ("#FFD700" if edge > 0 else "#ff4444")
                row  += f"<span style='color:{color};font-weight:700'>{odd:.2f}<br><span style='font-size:.72rem'>{'▲' if edge>0 else '▼'}{abs(edge)*100:.1f}%</span></span>"
                if edge > best_edge: best_edge=edge; best_bk=bk_names.get(bk,bk)
            else:
                row += "<span style='color:#333'>—</span>"
        if best_edge > 0.05:
            row += f"<span style='color:#00ff88;font-weight:900'>+{best_edge*100:.1f}%<br><span style='font-size:.72rem'>{best_bk}</span></span>"
        elif best_edge > 0:
            row += f"<span style='color:#FFD700;font-weight:700'>+{best_edge*100:.1f}%</span>"
        else:
            row += "<span style='color:#555'>Sin valor</span>"
        row += "</div>"
        st.markdown(row, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# FORM CHART — gráfica SVG de racha
# ══════════════════════════════════════════════════════════
def render_form_chart(form, team_name, color):
    """Gráfica SVG de tendencia de los últimos 10 partidos."""
    if not form or len(form) < 2:
        return
    # Puntos: W=3, D=1, L=0
    pts = [3 if r["result"]=="W" else (1 if r["result"]=="D" else 0) for r in reversed(form)]
    # Media móvil de 3
    ma = []
    for i in range(len(pts)):
        w = pts[max(0,i-2):i+1]
        ma.append(sum(w)/len(w))

    W, H = 300, 80
    pad  = 10
    n    = len(pts)
    xs   = [pad + i*(W-2*pad)/(n-1) for i in range(n)]
    # normalizar a 0-3
    ys   = [H - pad - (v/3)*(H-2*pad) for v in ma]

    # Path
    path = f"M {xs[0]:.1f},{ys[0]:.1f} " + " ".join(f"L {xs[i]:.1f},{ys[i]:.1f}" for i in range(1,n))
    # Dots
    dots = ""
    for i,(x,y,p) in enumerate(zip(xs,ys,pts)):
        dc = "#00ff88" if p==3 else ("#FFD700" if p==1 else "#ff4444")
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{dc}" stroke="#07071a" stroke-width="1.5"/>'

    # Trend arrow
    trend     = ma[-1] - ma[0]
    trend_txt = f"{'↑' if trend>0.3 else ('↓' if trend<-0.3 else '→')} {'Mejorando' if trend>0.3 else ('Bajando' if trend<-0.3 else 'Estable')}"
    trend_col = "#00ff88" if trend>0.3 else ("#ff4444" if trend<-0.3 else "#FFD700")

    svg = f"""<div style='margin:8px 0'>
    <div style='font-size:.75rem;color:#555;margin-bottom:4px'>Tendencia últimos {n} partidos</div>
    <svg width="100%" viewBox="0 0 {W} {H}" style="background:#0a0a20;border-radius:8px;border:1px solid #1a1a40">
      <defs><linearGradient id="grad{team_name[:3]}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="{color}" stop-opacity="0.1"/>
        <stop offset="100%" stop-color="{color}" stop-opacity="0.4"/>
      </linearGradient></defs>
      <path d="{path}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>
      {dots}
    </svg>
    <div style='font-size:.78rem;color:{trend_col};font-weight:700;margin-top:4px'>{trend_txt}</div>
    </div>"""
    st.markdown(svg, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# AUTO TRACKER — revisa resultados de picks guardados
# ══════════════════════════════════════════════════════════
def auto_track_picks():
    """Revisa picks pendientes y actualiza resultado automáticamente."""
    init_history()
    h = st.session_state["pick_history"]
    updated = 0
    for i, pick in enumerate(h):
        if pick["result"] != "⏳": continue
        try:
            # Buscar el partido en ESPN por fecha
            pick_date = datetime.strptime(pick["date"].split()[0], "%d/%m")
            pick_date = pick_date.replace(year=datetime.now().year)
            ds   = pick_date.strftime("%Y%m%d")
            slug = next((s for s,n in LIGAS.items() if n.split()[0] in pick["league"]), None)
            if not slug: continue
            data = eg(f"{ESPN}/{slug}/scoreboard", {"dates": ds, "limit": 100})
            for ev in data.get("events", []):
                comp  = ev["competitions"][0]
                comps = comp["competitors"]
                state = ev.get("status",{}).get("type",{}).get("state","")
                if state != "post": continue
                hc = next((c for c in comps if c["homeAway"]=="home"), None)
                ac = next((c for c in comps if c["homeAway"]=="away"), None)
                if not hc or not ac: continue
                hn = hc["team"]["displayName"]; an = ac["team"]["displayName"]
                if pick["home"][:8].lower() not in hn.lower(): continue
                gh = parse_score(hc.get("score",0)); ga = parse_score(ac.get("score",0))
                # Determinar resultado
                pick_txt = pick["pick"].lower()
                if "local" in pick_txt or "home" in pick_txt or pick["home"][:6].lower() in pick_txt:
                    won = gh > ga
                elif "visita" in pick_txt or "away" in pick_txt or pick["away"][:6].lower() in pick_txt:
                    won = ga > gh
                elif "over 2.5" in pick_txt:
                    won = (gh+ga) > 2
                elif "ambos" in pick_txt or "btts" in pick_txt:
                    won = gh > 0 and ga > 0
                elif "empate" in pick_txt:
                    won = gh == ga
                else:
                    continue
                st.session_state["pick_history"][i]["result"] = "✅" if won else "❌"
                st.session_state["pick_history"][i]["score"]  = f"{gh}-{ga}"
                updated += 1
                break
        except: continue
    return updated

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


# ══════════════════════════════════════════════════════════
# MEMORIA PERSISTENTE — Einstein Brain
# ══════════════════════════════════════════════════════════
import json as _json_mem, collections as _col

MEMORY_FILE = "/tmp/gamblers_brain.json"

def _load_brain():
    try:
        with open(MEMORY_FILE,"r") as f: return _json_mem.load(f)
    except: return {"picks":[],"stats":{},"patterns":{},"version":2}

def _save_brain(b):
    try:
        with open(MEMORY_FILE,"w") as f: _json_mem.dump(b,f,ensure_ascii=False,indent=2)
    except: pass

def init_califica_memory():
    if "brain" not in st.session_state:
        st.session_state["brain"] = _load_brain()

def _update_patterns(brain):
    picks=[p for p in brain["picks"] if p.get("resultado") in ["✅","❌"]]
    if len(picks)<2: brain["patterns"]={}; return
    mkt_s=_col.defaultdict(lambda:{"w":0,"l":0})
    spt_s=_col.defaultdict(lambda:{"w":0,"l":0})
    cq_s={"bajo":{"w":0,"l":0},"medio":{"w":0,"l":0},"alto":{"w":0,"l":0},"muy_alto":{"w":0,"l":0}}
    ed_s={"neg":{"w":0,"l":0},"0_5":{"w":0,"l":0},"5_10":{"w":0,"l":0},"mas10":{"w":0,"l":0}}
    for p in picks:
        k="w" if p.get("correcto") else "l"
        mkt_s[str(p.get("mercado","?")).split()[0].lower()[:12]][k]+=1
        spt_s[str(p.get("deporte","?"))][k]+=1
        c=float(p.get("cuota",0))
        cq_s["bajo" if c<1.5 else ("medio" if c<2.2 else ("alto" if c<3.5 else "muy_alto"))][k]+=1
        e=float(p.get("edge_pct",0))
        ed_s["neg" if e<0 else ("0_5" if e<5 else ("5_10" if e<10 else "mas10"))][k]+=1
    def pct(d): return round(d["w"]/(d["w"]+d["l"])*100,1) if (d["w"]+d["l"])>0 else None
    brain["patterns"]={
        "mercados":{k:{"pct":pct(v),"n":v["w"]+v["l"]} for k,v in mkt_s.items() if v["w"]+v["l"]>=2},
        "deportes":{k:{"pct":pct(v),"n":v["w"]+v["l"]} for k,v in spt_s.items() if v["w"]+v["l"]>=2},
        "cuotas":{k:{"pct":pct(v),"n":v["w"]+v["l"]} for k,v in cq_s.items()},
        "edges":{k:{"pct":pct(v),"n":v["w"]+v["l"]} for k,v in ed_s.items()},
    }
    tot=len(picks); w=sum(1 for p in picks if p.get("correcto"))
    brain["stats"]={"total":tot,"wins":w,"losses":tot-w,
        "roi":round(sum((float(p.get("cuota",1))-1) if p.get("correcto") else -1 for p in picks)/tot*100,1) if tot>0 else 0}

def add_califica_result(mercado,cuota,resultado,correcto,deporte="",equipos="",edge_pct=0,prob_real=0,prob_implicita=0,puntuacion=0):
    init_califica_memory()
    brain=st.session_state["brain"]
    brain["picks"].append({"fecha":datetime.now(CDMX).strftime("%Y-%m-%d %H:%M"),
        "deporte":deporte,"equipos":equipos,"mercado":mercado,"cuota":float(cuota) if cuota else 0,
        "resultado":resultado,"correcto":correcto,"edge_pct":float(edge_pct),
        "prob_real":float(prob_real),"prob_implicita":float(prob_implicita),"puntuacion":int(puntuacion)})
    brain["picks"]=brain["picks"][-500:]
    _update_patterns(brain); _save_brain(brain); st.session_state["brain"]=brain

def get_memory_context():
    init_califica_memory()
    brain=st.session_state["brain"]
    stats=brain.get("stats",{}); patterns=brain.get("patterns",{})
    n=stats.get("total",0)
    if n==0: return ""
    w=stats.get("wins",0); roi=stats.get("roi",0)
    ctx=f"CEREBRO ESTADÍSTICO ({n} picks registrados, {w} correctos, ROI={roi:+.1f}%). "
    mkts=patterns.get("mercados",{})
    best=sorted([(k,v) for k,v in mkts.items() if v["n"]>=2 and v["pct"] is not None],key=lambda x:-x[1]["pct"])[:3]
    worst=sorted([(k,v) for k,v in mkts.items() if v["n"]>=2 and v["pct"] is not None],key=lambda x:x[1]["pct"])[:3]
    if best: ctx+=f"Mercados CON MÁS ACIERTO: {', '.join([f'{k}({v['pct']}%,n={v['n']})' for k,v in best])}. "
    if worst: ctx+=f"Mercados CON MÁS FALLOS: {', '.join([f'{k}({v['pct']}%,n={v['n']})' for k,v in worst])}. "
    edges=patterns.get("edges",{})
    for rng,label in [("mas10","edge>10%"),("5_10","edge 5-10%"),("0_5","edge 0-5%"),("neg","edge negativo")]:
        if edges.get(rng,{}).get("n",0)>=2:
            ctx+=f"{label}: {edges[rng]['pct']}% acierto en {edges[rng]['n']} picks. "
    sports=patterns.get("deportes",{})
    for s,v in sports.items():
        if v.get("n",0)>=2: ctx+=f"{s}: {v['pct']}% acierto ({v['n']} picks). "
    return ctx


# ══════════════════════════════════════════════════════════
# RESULTADOS DB — Base de datos interna de partidos
# Se actualiza cada 2 horas automáticamente
# ══════════════════════════════════════════════════════════
RESULTS_FILE   = "/tmp/gamblers_results.json"
LAST_UPDATE_F  = "/tmp/gamblers_last_update.txt"

def _load_results_db():
    try:
        with open(RESULTS_FILE,"r") as f: return _json_mem.load(f)
    except: return {"partidos":[],"ultima_actualizacion":"","version":1}

def _save_results_db(db):
    try:
        with open(RESULTS_FILE,"w") as f: _json_mem.dump(db,f,ensure_ascii=False,indent=2)
    except: pass

def _needs_update():
    """Returns True if last update was >2 hours ago or never."""
    try:
        with open(LAST_UPDATE_F,"r") as f: last = f.read().strip()
        last_dt = datetime.fromisoformat(last).replace(tzinfo=pytz.UTC)
        return (datetime.now(pytz.UTC) - last_dt).total_seconds() > 7200
    except: return True

def _mark_updated():
    try:
        with open(LAST_UPDATE_F,"w") as f: f.write(datetime.now(pytz.UTC).isoformat())
    except: pass

def _needs_daily_reset():
    """Returns True if it's past 2am CDMX and we haven't reset today."""
    now = datetime.now(CDMX)
    reset_key = f"/tmp/gamblers_reset_{now.strftime('%Y%m%d')}.txt"
    if now.hour >= 2 and not os.path.exists(reset_key):
        try:
            open(reset_key,"w").close()
            return True
        except: return False
    return False

def fetch_soccer_results(days_back=10):
    """Fetch last N days of soccer results from ESPN."""
    partidos = []
    now = datetime.now(CDMX)
    for day_offset in range(days_back, -1, -1):
        d = now - timedelta(days=day_offset)
        ds = d.strftime("%Y%m%d")
        for slug in list(LIGAS.keys())[:12]:  # Top 12 ligas
            try:
                data = eg(f"{ESPN}/{slug}/scoreboard", {"dates": ds, "limit": 50})
                for ev in data.get("events",[]):
                    try:
                        comp  = ev["competitions"][0]
                        state = ev.get("status",{}).get("type",{}).get("state","")
                        comps = comp["competitors"]
                        hc = next(c for c in comps if c["homeAway"]=="home")
                        ac = next(c for c in comps if c["homeAway"]=="away")
                        utc  = datetime.strptime(ev["date"],"%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.UTC)
                        fecha = utc.astimezone(CDMX).strftime("%Y-%m-%d")
                        partidos.append({
                            "id":ev.get("id",""), "deporte":"futbol",
                            "liga":LIGAS[slug], "slug":slug,
                            "home":hc["team"]["displayName"],
                            "away":ac["team"]["displayName"],
                            "home_id":str(hc["team"]["id"]),
                            "away_id":str(ac["team"]["id"]),
                            "score_h":parse_score(hc.get("score",0)) if state=="post" else -1,
                            "score_a":parse_score(ac.get("score",0)) if state=="post" else -1,
                            "fecha":fecha, "state":state,
                        })
                    except: continue
            except: continue
    return partidos

def fetch_nba_results(days_back=10):
    """Fetch last N days of NBA results."""
    partidos = []
    now = datetime.now(CDMX)
    for day_offset in range(days_back, -1, -1):
        d = now - timedelta(days=day_offset)
        ds = d.strftime("%Y%m%d")
        try:
            data = eg(f"{NBA_ESPN}/scoreboard", {"dates": ds, "limit": 30})
            for ev in data.get("events",[]):
                try:
                    comp  = ev["competitions"][0]
                    state = ev.get("status",{}).get("type",{}).get("state","")
                    comps = comp["competitors"]
                    hc = next(c for c in comps if c["homeAway"]=="home")
                    ac = next(c for c in comps if c["homeAway"]=="away")
                    utc   = datetime.strptime(ev["date"],"%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.UTC)
                    fecha = utc.astimezone(CDMX).strftime("%Y-%m-%d")
                    ou_line = 0.0
                    try:
                        odds = comp.get("odds",[])
                        if odds: ou_line = float(odds[0].get("overUnder",0) or 0)
                    except: pass
                    partidos.append({
                        "id":ev.get("id",""), "deporte":"nba",
                        "liga":"NBA 🏀", "slug":"nba",
                        "home":hc["team"]["displayName"],
                        "away":ac["team"]["displayName"],
                        "home_id":str(hc["team"]["id"]),
                        "away_id":str(ac["team"]["id"]),
                        "score_h":parse_score(hc.get("score",0)) if state=="post" else -1,
                        "score_a":parse_score(ac.get("score",0)) if state=="post" else -1,
                        "ou_line":ou_line,
                        "fecha":fecha, "state":state,
                    })
                except: continue
        except: continue
    return partidos

def update_results_db(force=False):
    """Main update function — fetches results and merges into DB."""
    if not force and not _needs_update():
        return False
    db = _load_results_db()
    existing_ids = {p["id"] for p in db["partidos"]}
    # Fetch new data
    new_soccer = fetch_soccer_results(10)
    new_nba    = fetch_nba_results(10)
    all_new    = new_soccer + new_nba
    # Merge: update existing, add new
    existing_map = {p["id"]: i for i,p in enumerate(db["partidos"])}
    for p in all_new:
        if p["id"] in existing_map:
            # Update score/state if now finished
            idx = existing_map[p["id"]]
            if p["state"] == "post":
                db["partidos"][idx]["state"]   = "post"
                db["partidos"][idx]["score_h"] = p["score_h"]
                db["partidos"][idx]["score_a"] = p["score_a"]
        else:
            db["partidos"].append(p)
    # Keep only last 10 days
    cutoff = (datetime.now(CDMX) - timedelta(days=10)).strftime("%Y-%m-%d")
    db["partidos"] = [p for p in db["partidos"] if p.get("fecha","") >= cutoff]
    db["ultima_actualizacion"] = datetime.now(CDMX).strftime("%Y-%m-%d %H:%M")
    _save_results_db(db)
    # Daily brain sync — learn from completed picks at 2am
    if _needs_daily_reset():
        _sync_brain_with_results(db)
    _mark_updated()
    return True

def _sync_brain_with_results(db):
    """At 2am daily: auto-update any pending Einstein picks that now have real results."""
    brain = _load_brain()
    picks = brain.get("picks",[])
    results_map = {}
    for p in db["partidos"]:
        if p["state"] == "post" and p["score_h"] >= 0:
            key = f"{p['home'][:8].lower()}_{p['away'][:8].lower()}_{p['fecha']}"
            results_map[key] = {"score_h":p["score_h"],"score_a":p["score_a"]}
    updated = 0
    for pk in picks:
        if pk.get("resultado") != "⏳": continue
        eq = str(pk.get("equipos",""))
        parts = eq.split(" vs ") if " vs " in eq else eq.split(" @ ")
        if len(parts) < 2: continue
        h,a = parts[0][:8].lower(), parts[1][:8].lower()
        # Try to match date from fecha field
        fecha = str(pk.get("fecha",pk.get("date",""))).split()[0][:10]
        key = f"{h}_{a}_{fecha}"
        if key in results_map:
            r = results_map[key]
            mkt = str(pk.get("mercado","")).lower()
            sh,sa = r["score_h"],r["score_a"]
            won = None
            if "over 2.5" in mkt: won = (sh+sa) > 2
            elif "under 2.5" in mkt: won = (sh+sa) <= 2
            elif "over 3.5" in mkt: won = (sh+sa) > 3
            elif "under 3.5" in mkt: won = (sh+sa) <= 3
            elif "btts" in mkt or "ambos" in mkt: won = sh>0 and sa>0
            elif h in mkt: won = sh > sa
            elif a in mkt: won = sa > sh
            if won is not None:
                pk["resultado"] = "✅" if won else "❌"
                pk["correcto"]  = won
                pk["score_real"] = f"{sh}-{sa}"
                updated += 1
    if updated > 0:
        _update_patterns(brain)
        _save_brain(brain)
    return updated

def init_results_db():
    if "results_db" not in st.session_state:
        st.session_state["results_db"] = _load_results_db()
    if "results_last_check" not in st.session_state:
        st.session_state["results_last_check"] = 0

def get_results_db():
    init_results_db()
    now_ts = datetime.now(pytz.UTC).timestamp()
    # Check every 10 min in UI (actual update throttled to 2h server-side)
    if now_ts - st.session_state["results_last_check"] > 600:
        updated = update_results_db()
        if updated:
            st.session_state["results_db"] = _load_results_db()
        st.session_state["results_last_check"] = now_ts
    return st.session_state["results_db"]

# ══════════════════════════════════════════════════════════
# VILLAR BOT — Limpieza automática y auditoría de resultados
# ══════════════════════════════════════════════════════════

def _villar_check_pick(pick, score_h, score_a, sport):
    """
    Villar evalúa si el pick que dio el sistema ganó o perdió.
    Retorna: "✅ GANÓ", "❌ PERDIÓ", "↩️ EMPUJÓ", "❓ No verificable"
    """
    lbl = pick.get("pick","").lower()
    sh, sa = score_h, score_a
    if sh < 0 or sa < 0: return "❓", "#555"

    if sport == "futbol":
        won_h = sh > sa; won_a = sa > sh; draw = sh == sa
        total = sh + sa
        if any(x in lbl for x in ["gana","local","home","🏠"]):
            team = pick.get("home","")
            if team and team.lower() in lbl:
                return ("✅ GANÓ","#00ff88") if won_h else ("❌ PERDIÓ","#ff4444")
            return ("✅ GANÓ","#00ff88") if won_h else ("❌ PERDIÓ","#ff4444")
        elif any(x in lbl for x in ["visitante","away","✈️"]):
            return ("✅ GANÓ","#00ff88") if won_a else ("❌ PERDIÓ","#ff4444")
        elif "empate" in lbl or "draw" in lbl:
            return ("✅ GANÓ","#00ff88") if draw else ("❌ PERDIÓ","#ff4444")
        elif "dc:" in lbl or "doble chance" in lbl or "o emp" in lbl:
            if "🔵" in lbl or "local" in lbl: return ("✅ GANÓ","#00ff88") if (won_h or draw) else ("❌ PERDIÓ","#ff4444")
            if "🟣" in lbl or "visita" in lbl: return ("✅ GANÓ","#00ff88") if (won_a or draw) else ("❌ PERDIÓ","#ff4444")
            if "🔴" in lbl: return ("✅ GANÓ","#00ff88") if (won_h or won_a) else ("↩️ EMPUJÓ","#FFD700")
        elif "over 2.5" in lbl: return ("✅ GANÓ","#00ff88") if total>2 else ("❌ PERDIÓ","#ff4444")
        elif "over 3.5" in lbl: return ("✅ GANÓ","#00ff88") if total>3 else ("❌ PERDIÓ","#ff4444")
        elif "over 1.5" in lbl: return ("✅ GANÓ","#00ff88") if total>1 else ("❌ PERDIÓ","#ff4444")
        elif "ambos" in lbl or "btts" in lbl or "aa" in lbl: return ("✅ GANÓ","#00ff88") if (sh>0 and sa>0) else ("❌ PERDIÓ","#ff4444")
    elif sport == "nba":
        if "over" in lbl:
            try:
                line = float(''.join(c for c in lbl if c.isdigit() or c=='.'))
                return ("✅ GANÓ","#00ff88") if (sh+sa)>line else ("❌ PERDIÓ","#ff4444")
            except: pass
        elif "under" in lbl:
            try:
                line = float(''.join(c for c in lbl if c.isdigit() or c=='.'))
                return ("✅ GANÓ","#00ff88") if (sh+sa)<line else ("❌ PERDIÓ","#ff4444")
            except: pass
        won_h = sh > sa; won_a = sa > sh
        if any(x in lbl for x in ["local","home","🏠"]): return ("✅ GANÓ","#00ff88") if won_h else ("❌ PERDIÓ","#ff4444")
        if any(x in lbl for x in ["visita","away","✈️"]): return ("✅ GANÓ","#00ff88") if won_a else ("❌ PERDIÓ","#ff4444")
    elif sport == "tenis":
        won_p1 = sh > sa
        p1n = pick.get("p1","").lower()
        p2n = pick.get("p2","").lower()
        if p1n and p1n[:6] in lbl: return ("✅ GANÓ","#00ff88") if won_p1 else ("❌ PERDIÓ","#ff4444")
        if p2n and p2n[:6] in lbl: return ("✅ GANÓ","#00ff88") if not won_p1 else ("❌ PERDIÓ","#ff4444")
    return ("❓","#555")

def _villar_precache_tomorrow():
    """
    Villar corre el análisis Einstein de los partidos de mañana en background.
    Se guarda en disco para que mañana sea instantáneo.
    """
    import hashlib, json as _j, os as _os
    tomorrow = (datetime.now(CDMX)+timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        ten = get_tennis_cartelera()
        pre = [m for m in ten if m.get("fecha")==tomorrow and m.get("state")=="pre"]
        _smap = {"Indian Wells":"hard","Miami":"hard","Roland Garros":"clay",
                 "Wimbledon":"grass","US Open":"hard","Australian Open":"hard",
                 "Monte Carlo":"clay","Madrid":"clay","Barcelona":"clay"}
        cached = 0
        for m in pre[:6]:
            torneo  = m.get("torneo","")
            surface = next((v for k,v in _smap.items() if k.lower() in torneo.lower()), "hard")
            key = hashlib.md5(f"{m['p1']}|{m['p2']}|{surface}|{torneo}".encode()).hexdigest()[:16]
            cp  = f"/tmp/tenis_ai_{key}_{tomorrow}.json"
            if not _os.path.exists(cp):
                result = tennis_expert_analysis(m["p1"],m["p2"],m["rank1"],m["rank2"],
                                                 m["odd_1"],m["odd_2"],surface,torneo)
                if result:
                    with open(cp,'w') as f: _j.dump(result,f)
                    cached += 1
        return cached
    except: return 0

def render_resultados_tab():
    """VILLAR BOT — Resultados, limpieza automática y auditoría de picks."""
    from collections import defaultdict

    # ── VILLAR HEADER ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a001a,#001a0a);border:1px solid #00ff8855;
    border-radius:16px;padding:16px 20px;margin-bottom:16px;display:flex;align-items:center;gap:14px'>
    <div style='font-size:2.2rem'>🤖</div>
    <div>
      <div style='font-size:1.1rem;font-weight:900;color:#00ff88;letter-spacing:.04em'>VILLAR</div>
      <div style='font-size:.78rem;color:#555'>Bot de limpieza · Auditoría de picks · Resultados en tiempo real</div>
    </div>
    </div>""", unsafe_allow_html=True)

    # ── ACCIONES VILLAR ──
    v1, v2, v3 = st.columns(3)
    with v1:
        if st.button("🧹 Limpiar cartelera", use_container_width=True, key="villar_clean",
                     help="Mueve partidos terminados a Resultados"):
            with st.spinner("🤖 Villar revisando scores en línea..."):
                update_results_db(force=True)
                st.session_state["results_db"] = _load_results_db()
            st.success("✅ Villar limpió la cartelera")
            st.rerun()
    with v2:
        if st.button("⚡ Pre-cachear mañana", use_container_width=True, key="villar_precache",
                     help="Einstein analiza los partidos de mañana ahora, para que sean instantáneos"):
            with st.spinner("🧠 Einstein pre-analizando partidos de mañana..."):
                n = _villar_precache_tomorrow()
            st.success(f"✅ {n} partidos de tenis pre-analizados para mañana")
    with v3:
        if st.button("🔄 Actualizar todo", use_container_width=True, key="villar_refresh"):
            with st.spinner("🤖 Villar actualizando scores..."):
                update_results_db(force=True)
                st.session_state["results_db"] = _load_results_db()
                st.session_state["results_last_check"] = datetime.now(pytz.UTC).timestamp()
            st.success("✅ Actualizado"); st.rerun()

    db = get_results_db()
    partidos = db.get("partidos",[])
    ultima = db.get("ultima_actualizacion","Nunca")
    st.caption(f"🕐 Última actualización: {ultima}")

    if not partidos:
        st.info("🤖 Villar no tiene datos aún. Haz clic en 'Limpiar cartelera' para cargar resultados.")
        return

    # ── PICKS GUARDADOS para auditoría ──
    brain = st.session_state.get("brain",{})
    saved_picks = brain.get("picks",[]) if brain else []

    # ── TABS POR DEPORTE ──
    rt1, rt2, rt3 = st.tabs(["⚽ Fútbol", "🏀 NBA", "🎾 Tenis"])

    for tab_obj, sport_key, sport_label, sport_emoji in [
        (rt1,"futbol","Fútbol","⚽"),
        (rt2,"nba","NBA","🏀"),
        (rt3,"tenis","Tenis","🎾"),
    ]:
        with tab_obj:
            sport_p     = [p for p in partidos if p.get("deporte")==sport_key]
            finalizados = sorted([p for p in sport_p if p.get("state")=="post"],
                                  key=lambda x:x.get("fecha",""), reverse=True)
            en_juego    = [p for p in sport_p if p.get("state")=="in"]

            # ── KPIs ──
            picks_sport = [pk for pk in saved_picks if pk.get("deporte",sport_emoji)==sport_emoji]
            ganados = sum(1 for pk in picks_sport if pk.get("result")=="✅")
            perdidos= sum(1 for pk in picks_sport if pk.get("result")=="❌")
            st.markdown(
                f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:14px'>"
                f"<div class='mbox'><div class='mval' style='color:#00ff88'>{len(finalizados)}</div><div class='mlbl'>Terminados</div></div>"
                f"<div class='mbox'><div class='mval' style='color:#ff9500'>{len(en_juego)}</div><div class='mlbl'>En Vivo</div></div>"
                f"<div class='mbox'><div class='mval' style='color:#00ff88'>{ganados}</div><div class='mlbl'>Picks ✅</div></div>"
                f"<div class='mbox'><div class='mval' style='color:#ff4444'>{perdidos}</div><div class='mlbl'>Picks ❌</div></div>"
                f"</div>", unsafe_allow_html=True)

            # ── EN VIVO ──
            if en_juego:
                st.markdown("<div style='font-size:.72rem;font-weight:700;color:#ff9500;text-transform:uppercase;letter-spacing:.1em;margin:8px 0 6px'>🔴 EN VIVO AHORA</div>", unsafe_allow_html=True)
                for p in en_juego:
                    sh=p.get("score_h",-1); sa=p.get("score_a",-1)
                    sc = f"{sh}–{sa}" if sh>=0 else "🔴"
                    home_name = p.get("home",p.get("p1","?"))
                    away_name = p.get("away",p.get("p2","?"))
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;align-items:center;"
                        f"padding:8px 14px;background:#1a0800;border-radius:10px;margin:3px 0;"
                        f"border-left:3px solid #ff9500'>"
                        f"<div style='font-size:.85rem'><b>{home_name}</b> <span style='color:#555'>vs</span> <b>{away_name}</b>"
                        f"<div style='font-size:.7rem;color:#555'>{p.get('liga',p.get('tour',''))} · {p.get('hora','')}</div></div>"
                        f"<div style='font-size:1.4rem;font-weight:900;color:#ff9500'>{sc}</div>"
                        f"</div>", unsafe_allow_html=True)

            # ── FINALIZADOS — por fecha con auditoría Villar ──
            if not finalizados:
                st.info(f"🤖 Villar: No hay partidos {sport_label} finalizados registrados. Haz clic en 'Limpiar cartelera'.")
                continue

            por_fecha = defaultdict(list)
            for p in finalizados: por_fecha[p.get("fecha","?")].append(p)

            dias_  = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
            meses_ = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
            def _fl(f):
                try:
                    d=datetime.strptime(f,"%Y-%m-%d")
                    return f"📅 {dias_[d.weekday()]} {d.day} {meses_[d.month]}"
                except: return f"📅 {f}"

            for fecha in sorted(por_fecha.keys(), reverse=True):
                dia_ps = por_fecha[fecha]
                is_today = fecha == datetime.now(CDMX).strftime("%Y-%m-%d")
                with st.expander(f"{_fl(fecha)}  ·  {len(dia_ps)} partidos {'· HOY' if is_today else ''}",
                                  expanded=is_today or fecha==sorted(por_fecha.keys(),reverse=True)[0]):

                    # Group by liga/tour
                    por_liga = defaultdict(list)
                    for p in dia_ps: por_liga[p.get("liga",p.get("tour","Sin liga"))].append(p)

                    for liga, lps in sorted(por_liga.items()):
                        st.markdown(f"<div style='font-size:.7rem;font-weight:700;color:#FFD700;"
                                    f"text-transform:uppercase;letter-spacing:.1em;margin:10px 0 5px'>"
                                    f"{sport_emoji} {liga}</div>", unsafe_allow_html=True)

                        for p in lps:
                            sh = p.get("score_h",-1); sa = p.get("score_a",-1)
                            if sh < 0: continue  # No score yet

                            home_n = p.get("home",p.get("p1","?"))
                            away_n = p.get("away",p.get("p2","?"))

                            # Resultado del partido
                            if sport_key == "futbol":
                                won_h=sh>sa; won_a=sa>sh; draw=sh==sa
                                hc="#00ff88" if won_h else ("#FFD700" if draw else "#aaa")
                                ac="#00ff88" if won_a else ("#FFD700" if draw else "#aaa")
                            elif sport_key == "nba":
                                won_h=sh>sa; won_a=sa>sh
                                hc="#00ff88" if won_h else "#aaa"
                                ac="#00ff88" if won_a else "#aaa"
                                draw=False
                            else:  # tenis
                                won_h=sh>sa; won_a=sa>sh
                                hc="#00ff88" if won_h else "#aaa"
                                ac="#00ff88" if won_a else "#aaa"
                                draw=False

                            # Villar: ¿hubo pick guardado en este partido?
                            match_picks = [pk for pk in saved_picks
                                          if (pk.get("home","").lower()==home_n.lower() or
                                              pk.get("p1","").lower()==home_n.lower())]
                            pick_html = ""
                            for pk in match_picks:
                                verd, vcol = _villar_check_pick(pk, sh, sa, sport_key)
                                pick_html += (
                                    f"<div style='margin-top:6px;padding:5px 10px;border-radius:7px;"
                                    f"background:{vcol}18;border:1px solid {vcol}44'>"
                                    f"<span style='font-size:.68rem;color:{vcol};font-weight:700'>🤖 VILLAR: {verd}</span>"
                                    f"<span style='font-size:.68rem;color:#555;margin-left:8px'>Pick: {pk.get('pick','')}</span>"
                                    f"</div>"
                                )

                            st.markdown(
                                f"<div style='background:#0a0a1e;border-radius:10px;padding:10px 12px;"
                                f"margin:4px 0;border:1px solid #1a1a40'>"
                                f"<div style='display:grid;grid-template-columns:1fr 80px 1fr;gap:6px;align-items:center'>"
                                f"<div style='text-align:right'>"
                                f"<span style='color:{hc};font-weight:{'900' if won_h else '400'};font-size:.88rem'>{home_n}</span></div>"
                                f"<div style='text-align:center;background:#07071a;border-radius:8px;padding:4px 6px'>"
                                f"<span style='font-size:1.1rem;font-weight:900;color:{hc}'>{sh}</span>"
                                f"<span style='color:#333;font-size:.9rem'> – </span>"
                                f"<span style='font-size:1.1rem;font-weight:900;color:{ac}'>{sa}</span></div>"
                                f"<div style='text-align:left'>"
                                f"<span style='color:{ac};font-weight:{'900' if won_a else '400'};font-size:.88rem'>{away_n}</span></div>"
                                f"</div>"
                                f"{pick_html}"
                                f"</div>", unsafe_allow_html=True)


def avg(lst): return sum(lst)/len(lst) if lst else 0.0


# ══════════════════════════════════════════════════════════
# EL PAPA DE EINSTEIN — Meta-IA Auditora
# Audita, critica y valida el análisis de Einstein.
# Usa Opus 4 (el modelo más potente) para máxima precisión.
# ══════════════════════════════════════════════════════════

def papa_einstein_audit(einstein_data, imagen_b64, media_type, mem_ctx=""):
    """
    El Papa de Einstein — meta-IA que audita el análisis de Einstein.
    
    Proceso:
    1. Recibe el JSON completo de Einstein + la imagen original
    2. Verifica CADA número calculado por Einstein
    3. Detecta errores, sesgos, omisiones críticas
    4. Recalcula edge, EV, Kelly de forma independiente
    5. Da su propio veredicto — puede SUBIR o BAJAR la calificación
    6. Score de confianza en Einstein: 0-100
    """
    if not ANTHROPIC_API_KEY: return {}
    
    einstein_json = __import__("json").dumps(einstein_data, ensure_ascii=False, indent=2)
    
    PAPA_PROMPT = f"""Eres EL PAPA DE EINSTEIN — la meta-IA más crítica, rigurosa e implacable del mundo en análisis de apuestas deportivas.
Tu única misión: AUDITAR y VALIDAR el análisis de Einstein sobre esta apuesta.
Eres el control de calidad supremo. No tienes misericordia con errores. Solo el 100% correcto pasa tu filtro.

ANÁLISIS DE EINSTEIN QUE DEBES AUDITAR:
{einstein_json}

PROCESO DE AUDITORÍA OBLIGATORIO:

1. VERIFICA LA IMAGEN tú mismo — identifica el partido, mercado, cuota y estado.
   ¿Einstein identificó correctamente todos los datos? ¿Hay errores de lectura?

2. RECALCULA INDEPENDIENTEMENTE:
   - Probabilidad implícita = 1/cuota. ¿Einstein la calculó bien?
   - Edge = prob_real - prob_implicita. ¿Es matemáticamente correcto?
   - EV = (prob_real × (cuota-1)) - ((1-prob_real) × 1). ¿Correcto?
   - Kelly = max(0, min(5%, ((cuota-1)×p - (1-p))/(cuota-1)×100)). ¿Correcto?

3. EVALÚA LA PROBABILIDAD REAL:
   - ¿Es razonable la prob_real que Einstein asignó?
   - ¿Consideró suficientes variables ocultas?
   - ¿Hay variables CRÍTICAS que Einstein omitió completamente?
   - ¿Tiene sesgo favorable o desfavorable injustificado?

4. VERIFICA LA CALIFICACIÓN:
   - Escala: A+ (95-100), A (88-94), A- (82-87), B+ (76-81), B (70-75), B- (64-69), C+ (55-63), C (45-54), C- (35-44), D (20-34), F (0-19)
   - ¿La calificación corresponde al EV y edge calculados?
   - ¿El veredicto es consistente con la puntuación?
   - ¿Einstein fue demasiado generoso o demasiado conservador?

5. VERIFICA EL ESTADO DEL PARTIDO:
   - ¿El partido ya terminó y Einstein no lo detectó? (Error crítico = F automático)
   - ¿La cuota parece de partido en vivo vs pre-partido?

6. SEÑAL SHARP:
   - ¿La evaluación del sharp signal es válida?
   - ¿Hay inconsistencias entre la señal sharp y la calificación?

7. ALTERNATIVA DE MERCADO:
   - ¿La alternativa propuesta por Einstein es realmente mejor?
   - ¿Hay una mejor alternativa que Einstein no vio?

{f"8. HISTORIAL DEL APOSTADOR: {mem_ctx} — ¿El pick es consistente con los patrones de éxito del usuario?" if mem_ctx else ""}

RESPONDE SOLO EN JSON SIN MARKDOWN NI TEXTO EXTRA:
{{
  "lectura_imagen": {{
    "partido_correcto": true/false,
    "mercado_correcto": true/false,
    "cuota_correcta": true/false,
    "estado_correcto": true/false,
    "errores_lectura": "<errores detectados o 'ninguno'>"
  }},
  "matematicas": {{
    "prob_implicita_correcta": true/false,
    "prob_implicita_papa": <float>,
    "edge_correcto": true/false,
    "edge_papa": <float>,
    "ev_correcto": true/false,
    "ev_papa": <float>,
    "kelly_correcto": true/false,
    "kelly_papa": <float>,
    "errores_matematicos": "<descripción o 'ninguno'>"
  }},
  "probabilidad_real": {{
    "es_razonable": true/false,
    "prob_real_papa": <float>,
    "sesgo_detectado": "<sobreestimado/subestimado/correcto>",
    "variables_omitidas": "<variables críticas que Einstein no consideró>",
    "variables_mal_ponderadas": "<variables que Einstein ponderó mal>"
  }},
  "calificacion": {{
    "calificacion_einstein_correcta": true/false,
    "calificacion_papa": "<A+/A/A-/B+/B/B-/C+/C/C-/D/F>",
    "puntuacion_papa": <0-100>,
    "veredicto_papa": "<Excelente|Sólida|Marginal|Riesgosa|Evitar|Inválida>",
    "apostar_papa": true/false,
    "justificacion_cambio": "<por qué cambias o confirmas la calificación>"
  }},
  "sharp_signal": {{
    "evaluacion_correcta": true/false,
    "sharp_signal_papa": "<favorable|neutral|contrario|desconocido>",
    "razon": "<análisis de la señal sharp>"
  }},
  "alternativa": {{
    "alternativa_einstein_valida": true/false,
    "mejor_alternativa_papa": "<mercado alternativo o 'la de Einstein es correcta'>",
    "razon_alternativa": "<por qué>"
  }},
  "confianza_en_einstein": <0-100>,
  "resumen_auditoria": "<2-3 oraciones: qué hizo bien Einstein, qué falló, veredicto final>",
  "kelly_recomendado_papa": <float>,
  "advertencia_critica": "<advertencia importante o 'ninguna'>",
  "sello": "<APROBADO CON HONORES|APROBADO|APROBADO CON OBSERVACIONES|RECHAZADO|RECHAZADO - ERROR CRÍTICO>"
}}

Sé brutalmente honesto. Si Einstein se equivocó, dilo claramente.
Si Einstein acertó, confírmalo con evidencia. El apostador necesita la verdad, no halagos."""

    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-opus-4-5",
                "max_tokens": 2000,
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": imagen_b64
                        }},
                        {"type": "text", "text": PAPA_PROMPT}
                    ]
                }]
            },
            timeout=60
        )
        if r.status_code != 200: return {}
        raw = r.json()["content"][0]["text"].strip()
        raw = raw.replace("```json","").replace("```","").strip()
        import json as _j
        return _j.loads(raw)
    except Exception as _e:
        return {}


def render_papa_einstein(einstein_data, audit, score_einstein):
    """
    Renderiza el veredicto del Papa de Einstein.
    Diseño supremo — por encima de Einstein visualmente.
    """
    if not audit:
        st.markdown(
            "<div style='background:#0d0d2e;border:1px solid #252555;border-radius:12px;"
            "padding:14px 18px;color:#555;font-size:.85rem'>"
            "⚠️ El Papa no pudo auditar. Verifica conexión API."
            "</div>", unsafe_allow_html=True)
        return

    sello      = audit.get("sello","N/D")
    confianza  = audit.get("confianza_en_einstein", 0)
    resumen    = audit.get("resumen_auditoria","")
    advertencia= audit.get("advertencia_critica","")
    calif      = audit.get("calificacion",{})
    mat        = audit.get("matematicas",{})
    prob_r     = audit.get("probabilidad_real",{})
    sharp_a    = audit.get("sharp_signal",{})
    alt_a      = audit.get("alternativa",{})
    lectura    = audit.get("lectura_imagen",{})
    
    calif_papa  = calif.get("calificacion_papa","?")
    pts_papa    = calif.get("puntuacion_papa", 0)
    vered_papa  = calif.get("veredicto_papa","")
    apostar_papa= calif.get("apostar_papa", False)
    justif      = calif.get("justificacion_cambio","")
    kelly_papa  = audit.get("kelly_recomendado_papa", 0)

    # Sello colors
    sello_data = {
        "APROBADO CON HONORES":        ("#00ff88", "✦", "linear-gradient(135deg,#001a0a,#002a12)"),
        "APROBADO":                    ("#00ccff", "✓", "linear-gradient(135deg,#001020,#002040)"),
        "APROBADO CON OBSERVACIONES":  ("#FFD700", "!", "linear-gradient(135deg,#1a1400,#2a2000)"),
        "RECHAZADO":                   ("#ff9500", "✗", "linear-gradient(135deg,#1a0800,#2a1000)"),
        "RECHAZADO - ERROR CRÍTICO":   ("#ff4444", "✗✗","linear-gradient(135deg,#1a0000,#2a0000)"),
    }
    sc, si, sg = sello_data.get(sello, ("#aaa","?","linear-gradient(135deg,#0d0d2e,#1a1a40)"))
    
    # Confianza color
    cc = "#00ff88" if confianza>=75 else ("#FFD700" if confianza>=50 else "#ff4444")
    
    # ── SELLO PRINCIPAL ──
    st.markdown(
        f"<div style='background:{sg};border:2px solid {sc};border-radius:20px;"
        f"padding:22px 24px;margin:12px 0;position:relative;overflow:hidden'>"
        # Watermark
        f"<div style='position:absolute;right:-10px;top:-10px;font-size:6rem;"
        f"opacity:.04;color:{sc};font-weight:900;line-height:1'>{si}</div>"
        # Header
        f"<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px'>"
        f"<div>"
        f"<div style='font-size:.65rem;color:#555;font-weight:700;letter-spacing:.2em;margin-bottom:4px'>"
        f"✝ EL PAPA DE EINSTEIN — AUDITORÍA SUPREMA</div>"
        f"<div style='font-size:1.2rem;font-weight:900;color:{sc}'>{sello}</div>"
        f"</div>"
        f"<div style='text-align:center'>"
        f"<div style='font-size:.6rem;color:#555;margin-bottom:2px'>CONFIANZA EN EINSTEIN</div>"
        f"<div style='font-size:2rem;font-weight:900;color:{cc}'>{confianza}</div>"
        f"<div style='font-size:.6rem;color:#555'>/100</div>"
        f"</div>"
        f"</div>"
        # Confianza bar
        f"<div style='background:#1a1a40;border-radius:4px;height:6px;overflow:hidden;margin-bottom:14px'>"
        f"<div style='width:{confianza}%;height:6px;"
        f"background:{'#00ff88' if confianza>=75 else ('#FFD700' if confianza>=50 else '#ff4444')}"
        f";border-radius:4px'></div></div>"
        # Resumen
        f"<div style='font-size:.85rem;color:#ccc;line-height:1.7;margin-bottom:12px'>"
        f"📋 {resumen}</div>"
        # Advertencia
        + (f"<div style='background:#2a0000;border:1px solid #ff444455;border-radius:8px;"
           f"padding:8px 14px;font-size:.78rem;color:#ff4444;margin-top:8px'>"
           f"⚠️ <b>ADVERTENCIA CRÍTICA:</b> {advertencia}</div>"
           if advertencia and advertencia.lower() not in ["ninguna","none","n/a",""] else "")
        + f"</div>", unsafe_allow_html=True)

    # ── CALIFICACIÓN DEL PAPA vs EINSTEIN ──
    letra_e = einstein_data.get("calificacion_letra","?")
    pts_e   = einstein_data.get("puntuacion",0)
    changed = calif_papa != letra_e
    change_color = "#00ff88" if pts_papa > pts_e else ("#ff4444" if pts_papa < pts_e else "#FFD700")
    
    grade_colors = {
        "A+":"#00ff88","A":"#00cc66","A-":"#00aa44",
        "B+":"#FFD700","B":"#ccaa00","B-":"#aa8800",
        "C+":"#ff9500","C":"#cc7000","C-":"#aa5500",
        "D":"#ff4444","F":"#cc0000"
    }
    gce = grade_colors.get(letra_e,"#aaa")
    gcp = grade_colors.get(calif_papa,"#aaa")
    
    calific_html = (
        "<div style='background:#0d0d2e;border:1px solid #252555;border-radius:14px;"
        "padding:16px 20px;margin:8px 0'>"
        "<div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>"
        "📊 CALIFICACIÓN: EINSTEIN vs PAPA</div>"
        f"<div style='display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center'>"
        f"<div style='background:#07071a;border-radius:12px;padding:14px;text-align:center'>"
        f"<div style='font-size:.65rem;color:#555;margin-bottom:6px'>🧠 EINSTEIN</div>"
        f"<div style='font-size:3rem;font-weight:900;color:{gce};line-height:1'>{letra_e}</div>"
        f"<div style='font-size:.75rem;color:#555;margin-top:4px'>{pts_e}/100</div>"
        f"</div>"
        f"<div style='font-size:1.5rem;text-align:center;color:{change_color}'>"
        f"{'→' if not changed else ('↑' if pts_papa>pts_e else '↓')}</div>"
        f"<div style='background:#07071a;border:2px solid {gcp}44;border-radius:12px;padding:14px;text-align:center'>"
        f"<div style='font-size:.65rem;color:#555;margin-bottom:6px'>✝ EL PAPA</div>"
        f"<div style='font-size:3rem;font-weight:900;color:{gcp};line-height:1'>{calif_papa}</div>"
        f"<div style='font-size:.75rem;color:#555;margin-top:4px'>{pts_papa}/100</div>"
        f"</div>"
        f"</div>"
        + (f"<div style='margin-top:12px;padding:10px 14px;background:#12122a;border-radius:8px;"
           f"font-size:.8rem;color:#aaa;line-height:1.6'>"
           f"<b style='color:{change_color}'>{'🔄 CAMBIO JUSTIFICADO' if changed else '✅ CALIFICACIÓN CONFIRMADA'}:</b> "
           f"{justif}</div>" if justif else "")
        + f"<div style='margin-top:12px;display:flex;gap:10px'>"
        f"<div style='flex:1;background:{'#002a00' if apostar_papa else '#1a0000'};"
        f"border:1px solid {'#00ff8855' if apostar_papa else '#ff444455'};"
        f"border-radius:10px;padding:10px;text-align:center'>"
        f"<div style='font-size:1.1rem;font-weight:900;color:{'#00ff88' if apostar_papa else '#ff4444'}'>"
        f"{'✅ EL PAPA APRUEBA APOSTAR' if apostar_papa else '❌ EL PAPA DICE NO APOSTAR'}</div>"
        f"<div style='font-size:.72rem;color:#555;margin-top:3px'>Kelly Papa: {kelly_papa:.1f}% bankroll</div>"
        f"</div></div>"
        f"</div>"
    )
    st.markdown(calific_html, unsafe_allow_html=True)

    # ── AUDITORÍA MATEMÁTICA ──
    if mat:
        errores_mat = mat.get("errores_matematicos","ninguno")
        tiene_errores = mat.get("edge_correcto") == False or mat.get("ev_correcto") == False or mat.get("kelly_correcto") == False
        
        with st.expander(f"🔢 Auditoría Matemática {'⚠️ ERRORES DETECTADOS' if tiene_errores else '✅ Cálculos correctos'}",
                          expanded=tiene_errores):
            cols = [
                ("Prob. Implícita", mat.get("prob_implicita_correcta"), 
                 f"Papa: {mat.get('prob_implicita_papa',0)*100:.2f}%",
                 f"Einstein: {einstein_data.get('prob_implicita_pct',0):.2f}%"),
                ("Edge", mat.get("edge_correcto"),
                 f"Papa: {mat.get('edge_papa',0)*100:.2f}%",
                 f"Einstein: {einstein_data.get('edge_pct',0):.2f}%"),
                ("EV", mat.get("ev_correcto"),
                 f"Papa: {mat.get('ev_papa',0):.4f}",
                 f"Einstein: {einstein_data.get('ev_por_unidad',0):.4f}"),
                ("Kelly", mat.get("kelly_correcto"),
                 f"Papa: {mat.get('kelly_papa',0):.2f}%",
                 f"Einstein: {einstein_data.get('kelly_pct',0):.2f}%"),
            ]
            for label, correcto, papa_val, ein_val in cols:
                c = "#00ff88" if correcto else "#ff4444"
                icon = "✅" if correcto else "❌"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:6px 10px;border-bottom:1px solid #1a1a40;font-size:.82rem'>"
                    f"<span style='color:#aaa'>{icon} {label}</span>"
                    f"<span style='color:#555'>{ein_val}</span>"
                    f"<span style='color:{c};font-weight:700'>{papa_val}</span>"
                    f"</div>", unsafe_allow_html=True)
            if errores_mat and errores_mat.lower() not in ["ninguno","none",""]:
                st.markdown(
                    f"<div style='background:#1a0a00;border-radius:8px;padding:10px;margin-top:8px;"
                    f"font-size:.78rem;color:#ff9500'>⚠️ {errores_mat}</div>",
                    unsafe_allow_html=True)

    # ── LECTURA DE IMAGEN ──
    lectura_ok = all([
        lectura.get("partido_correcto"),
        lectura.get("mercado_correcto"),
        lectura.get("cuota_correcta"),
    ])
    if not lectura_ok:
        errs_lec = lectura.get("errores_lectura","")
        if errs_lec and errs_lec.lower() not in ["ninguno","none",""]:
            st.markdown(
                f"<div style='background:#1a0000;border:1px solid #ff444455;border-radius:10px;"
                f"padding:12px 16px;margin:6px 0;font-size:.82rem;color:#ff4444'>"
                f"🔍 <b>ERROR DE LECTURA:</b> {errs_lec}</div>", unsafe_allow_html=True)

    # ── PROBABILIDAD REAL ──
    pb = audit.get("probabilidad_real",{})
    sesgo = pb.get("sesgo_detectado","")
    omitidas = pb.get("variables_omitidas","")
    mal_pond = pb.get("variables_mal_ponderadas","")
    
    if sesgo != "correcto" or omitidas or mal_pond:
        with st.expander("🎯 Probabilidad Real — Observaciones del Papa"):
            pb_papa = pb.get("prob_real_papa",0)
            pb_ein  = einstein_data.get("prob_real_pct",0)
            diff = pb_papa - pb_ein
            diff_c = "#00ff88" if abs(diff) < 2 else ("#ff9500" if abs(diff) < 5 else "#ff4444")
            st.markdown(
                f"<div style='display:flex;gap:12px;margin-bottom:10px'>"
                f"<div style='flex:1;background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
                f"<div style='font-size:.65rem;color:#555'>🧠 Einstein dice</div>"
                f"<div style='font-size:1.4rem;font-weight:900;color:#aaa'>{pb_ein:.1f}%</div></div>"
                f"<div style='flex:1;background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
                f"<div style='font-size:.65rem;color:#555'>✝ Papa dice</div>"
                f"<div style='font-size:1.4rem;font-weight:900;color:{diff_c}'>{pb_papa:.1f}%</div></div>"
                f"<div style='flex:1;background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
                f"<div style='font-size:.65rem;color:#555'>Diferencia</div>"
                f"<div style='font-size:1.4rem;font-weight:900;color:{diff_c}'>{diff:+.1f}%</div></div>"
                f"</div>", unsafe_allow_html=True)
            if sesgo:
                sc2 = "#ff4444" if sesgo != "correcto" else "#00ff88"
                st.markdown(f"<div style='font-size:.8rem;color:{sc2};margin-bottom:6px'>📊 Sesgo: <b>{sesgo.upper()}</b></div>", unsafe_allow_html=True)
            if omitidas and omitidas.lower() not in ["ninguna","none",""]:
                st.markdown(f"<div style='font-size:.8rem;color:#ff9500;margin-bottom:4px'>⚠️ <b>Variables omitidas por Einstein:</b> {omitidas}</div>", unsafe_allow_html=True)
            if mal_pond and mal_pond.lower() not in ["ninguna","none",""]:
                st.markdown(f"<div style='font-size:.8rem;color:#FFD700'>📉 <b>Mal ponderadas:</b> {mal_pond}</div>", unsafe_allow_html=True)

    # ── SHARP SIGNAL ──
    sharp_ok = sharp_a.get("evaluacion_correcta", True)
    if not sharp_ok:
        sp = sharp_a.get("sharp_signal_papa","")
        sp_r = sharp_a.get("razon","")
        sp_c = {"favorable":"#00ff88","neutral":"#FFD700","contrario":"#ff4444","desconocido":"#555"}.get(sp,"#aaa")
        st.markdown(
            f"<div style='background:#0d0d2e;border:1px solid {sp_c}44;border-left:3px solid {sp_c};"
            f"border-radius:0 10px 10px 0;padding:10px 16px;margin:6px 0;font-size:.82rem'>"
            f"🦅 <b style='color:{sp_c}'>Sharp Signal corregido: {sp.upper()}</b><br>"
            f"<span style='color:#888'>{sp_r}</span></div>", unsafe_allow_html=True)

    # ── ALTERNATIVA ──
    mejor_alt = alt_a.get("mejor_alternativa_papa","")
    if mejor_alt and "einstein es correcta" not in mejor_alt.lower():
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#001a10,#002a12);"
            f"border:2px solid #00ff8855;border-radius:14px;padding:14px 18px;margin:8px 0'>"
            f"<div style='font-size:.7rem;color:#00ff88;font-weight:700;letter-spacing:.1em;margin-bottom:6px'>"
            f"✝ ALTERNATIVA DEL PAPA — MEJOR QUE EINSTEIN</div>"
            f"<div style='font-size:.95rem;font-weight:700;color:#fff'>{mejor_alt}</div>"
            f"<div style='font-size:.8rem;color:#aaa;margin-top:4px'>{alt_a.get('razon_alternativa','')}</div>"
            f"</div>", unsafe_allow_html=True)

def render_einstein_califica(key_sfx="fut"):
    """Unified Einstein-level pick grader — shared across all sports."""
    init_califica_memory()
    mem_ctx = get_memory_context()
    brain = st.session_state.get("brain", {})
    bstats = brain.get("stats", {})
    bpicks = brain.get("picks", [])
    bpatt  = brain.get("patterns", {})

    # ── Brain KPIs ──
    if bstats.get("total", 0) > 0:
        _t = bstats["total"]; _w = bstats["wins"]; _roi = bstats.get("roi", 0)
        _acierto = round(_w/_t*100) if _t > 0 else 0
        st.markdown(
            f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:14px'>"
            f"<div class='mbox'><div class='mval' style='color:#00ccff;font-size:1.1rem'>{_t}</div><div class='mlbl'>Picks</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#00ff88;font-size:1.1rem'>{_w}</div><div class='mlbl'>Aciertos</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#FFD700;font-size:1.1rem'>{_acierto}%</div><div class='mlbl'>Hit rate</div></div>"
            f"<div class='mbox'><div class='mval' style='color:{'#00ff88' if _roi>=0 else '#ff4444'};font-size:1.1rem'>{_roi:+.1f}%</div><div class='mlbl'>ROI</div></div>"
            f"</div>", unsafe_allow_html=True)

    src_opt = st.radio("Fuente", ["📁 Galería / Archivo", "📷 Tomar foto ahora"],
                       horizontal=True, label_visibility="collapsed", key=f"src_{key_sfx}")
    uploaded = None
    if src_opt == "📁 Galería / Archivo":
        uploaded = st.file_uploader("Screenshot", type=["png","jpg","jpeg","webp"],
                                    label_visibility="collapsed", key=f"up_{key_sfx}")
    else:
        cam = st.camera_input("Cámara", label_visibility="collapsed", key=f"cam_{key_sfx}")
        if cam: uploaded = cam

    if uploaded:
        import base64 as _b64e, json as _jce
        img_bytes  = uploaded.read()
        b64        = _b64e.b64encode(img_bytes).decode()
        media_type = getattr(uploaded, "type", None) or "image/jpeg"

        # Compact image preview
        st.markdown(
            f"<div style='text-align:center;margin-bottom:14px'>"
            f"<img src='data:{media_type};base64,{b64}' "
            f"style='max-height:260px;max-width:100%;border-radius:14px;border:1.5px solid #252555'/>"
            f"</div>", unsafe_allow_html=True)

        with st.spinner("🧠 EINSTEIN analizando — variables visibles + ocultas + 50,000 simulaciones..."):
            try:
                EINSTEIN = (
                    "Eres EINSTEIN BETS, la IA más avanzada del mundo en análisis de apuestas deportivas. "
                    "Tu misión: analizar esta apuesta con rigor matemático absoluto, como un quant de Wall Street aplicado al deporte. "
                    "Hoy es " + datetime.now(CDMX).strftime("%A %d de %B de %Y, %H:%M hora CDMX") + ".\n\n"

                    "══ GLOSARIO DE TÉRMINOS LOCALES (CRÍTICO — memoriza esto) ══\n"
                    "PA = 'PAGO ANTICIPADO' — NO es Primer Apuesta. "
                    "  · En FÚTBOL: el equipo gana por 2+ goles en CUALQUIER momento del partido (incluso si al final empata o pierde). "
                    "  · En NBA: el equipo lleva 17+ puntos de ventaja en CUALQUIER momento del partido. "
                    "  · Es un mercado de cashout anticipado MUY popular en México/LATAM. Cuotas bajas son normales (1.10-1.50) porque el evento es más probable que el resultado final. "
                    "  · Para calcular edge en PA: la prob real de que UN equipo líder gane por 2+ goles es ~40-65% dependiendo del favorito. NO uses la prob de resultado final.\n"
                    "Parlay/Combinada/Múltiple = apuesta que combina 2+ selecciones. La cuota es el producto de todas las cuotas individuales. "
                    "  · Analiza CADA selección del parlay por separado y calcula el edge combinado.\n"
                    "Hándicap Asiático (AH) = mercado sin empate, con línea de ventaja.\n"
                    "1X2 = mercado clásico local/empate/visitante.\n\n"

                    "══ ESTADO DEL PARTIDO — REGLA CRÍTICA ══\n"
                    "SOLO marca estado_partido='finalizado' si ves un marcador FINAL explícito (FT, Final, Terminado, 90') en la imagen. "
                    "Si ves una hora futura (ej: '13:30', '20:00', 'Mañana') = 'pendiente'. "
                    "Si ves un marcador parcial con tiempo en curso = 'en_juego'. "
                    "NUNCA asumas que un partido pasó solo porque la hora ya ocurrió en tu zona horaria — el usuario está en México (CDMX, UTC-6).\n\n"

                    "══ PROCESO OBLIGATORIO ══\n"
                    "PASO 1 — IDENTIFICACIÓN PRECISA:\n"
                    "  · Deporte, equipos/jugadores, liga/torneo, fecha/hora visible, cuota exacta.\n"
                    "  · Mercado: identifica si es 1X2, Over/Under, Hándicap, PA (Pago Anticipado), Parlay, Goles, etc.\n"
                    "  · Si es PARLAY: lista cada selección, cuota individual estimada, y la cuota combinada.\n"
                    "  · Estado: pendiente/en_juego/finalizado según regla arriba.\n\n"

                    "PASO 2 — VARIABLES VISIBLES:\n"
                    "  · TENIS: Ranking ATP/WTA, superficie, H2H conocido, forma reciente.\n"
                    "  · FÚTBOL: Posición tabla, goles a favor/contra, local/visitante, importancia.\n"
                    "  · NBA: Win%, pts por partido, diferencial ofensivo/defensivo, lesiones conocidas.\n\n"

                    "PASO 3 — VARIABLES OCULTAS (las que marcan la diferencia real):\n"
                    "  · TENIS: Fatiga acumulada esta semana, velocidad de pista vs estilo, altitud, temperatura, presión de favoritismo, historial en esa ronda, lesiones crónicas, sets jugados últimos 3 partidos, necesidad de puntos ranking.\n"
                    "  · FÚTBOL: xG real vs goles (suerte vs mérito), cansancio doble competición, árbitro y tarjetas/partido, clima ciudad, set-pieces efficiency, deuda táctica del entrenador.\n"
                    "  · NBA: Pace differential, back-to-back, travel miles, rendimiento 4Q clutch, tendencia árbitro en fouls, rotaciones sin estrella.\n"
                    "  · PA específico: velocidad de inicio del equipo favorecido, su historial de ventajas >=2 goles en primeros 60', si el rival tiende a cerrar partidos.\n\n"

                    "PASO 4 — MODELO PROBABILÍSTICO:\n"
                    "  · Poisson para fútbol/NBA, Elo para tenis.\n"
                    "  · Para PA fútbol: prob_real = P(equipo X tenga +2 goles de ventaja en algún momento) ≈ 40-65%.\n"
                    "  · Para PA NBA: prob_real = P(equipo X tenga +17 pts en algún momento) ≈ 35-70%.\n"
                    "  · Para Parlay: prob_real = producto de probabilidades individuales.\n"
                    "  · prob_implicita = 1/cuota_total. edge = prob_real - prob_implicita.\n\n"

                    "PASO 5 — 50,000 SIMULACIONES MONTE CARLO:\n"
                    "  · Simula con las variables anteriores. IC al 95%. EV = (prob_real × (cuota-1)) - ((1-prob_real) × 1).\n\n"

                    "PASO 6 — SEÑAL SHARP:\n"
                    "  · ¿Cuota movida por sharp money? ¿Discrepancia entre casas? ¿Trampa pública?\n\n"

                    "PASO 7 — REVISIÓN CRÍTICA:\n"
                    "  · ¿Partido finalizado? → veredicto=Inválida.\n"
                    "  · ¿Es PA con cuota razonable para el favorito? → no penalices por cuota baja.\n"
                    "  · ¿Parlay con picks de valor real? → evalúa el valor combinado honestamente.\n\n"

                    "PASO 8 — KELLY: kelly% = max(0, min(5, ((cuota-1)×prob_real - (1-prob_real))/(cuota-1)×100)).\n"
                    + (f"PASO 9 — HISTORIAL DEL USUARIO: {mem_ctx}\n" if mem_ctx else "")
                    + "\n══ CALIFICACIÓN REALISTA (calibrada para el mercado real) ══\n"
                    "Sé justo y calibrado. Un pick con edge positivo real MERECE una buena nota.\n"
                    "A+(95-100): EV>+0.08, edge>8%, variables ocultas muy favorables, señal sharp clara\n"
                    "A (88-94): EV>+0.05, edge 5-8%, análisis sólido, pick de valor real\n"
                    "A-(82-87): EV>+0.02, edge 2-5%, pick razonable con fundamento\n"
                    "B+(76-81): EV>0, edge marginal positivo, pick aceptable\n"
                    "B (70-75): EV≈0, cuota justa, sin ventaja clara — apostar solo si hay otra razón\n"
                    "B-(64-69): EV ligeramente negativo — precaución\n"
                    "C+(55-63): EV negativo pequeño — mejor buscar otra opción\n"
                    "C (45-54): EV negativo significativo — evitar\n"
                    "C-(35-44): EV muy negativo — no tiene sentido\n"
                    "D (20-34): Pick sin fundamento estadístico\n"
                    "F (0-19): Partido terminado, mercado cerrado, o pick completamente absurdo\n\n"
                    "RESPONDE SOLO EN JSON SIN MARKDOWN:\n"
                    "{\"deporte\": \"\", \"equipos\": \"\", \"mercado\": \"\", \"cuota\": 0.0, "
                    "\"es_parlay\": false, \"selecciones_parlay\": [], "
                    "\"es_pago_anticipado\": false, "
                    "\"estado_partido\": \"pendiente|en_juego|finalizado\", "
                    "\"prob_real_pct\": 0.0, \"prob_implicita_pct\": 0.0, \"edge_pct\": 0.0, "
                    "\"ev_por_unidad\": 0.0, \"ic_95\": \"\", "
                    "\"variables_ocultas_clave\": \"\", "
                    "\"calificacion_letra\": \"\", \"puntuacion\": 0, "
                    "\"veredicto\": \"Excelente|Sólida|Marginal|Riesgosa|Evitar|Inválida\", "
                    "\"razon_principal\": \"\", \"riesgos_ocultos\": \"\", "
                    "\"sharp_signal\": \"favorable|neutral|contrario|desconocido\", "
                    "\"alternativa_mercado\": \"\", \"alternativa_razon\": \"\", "
                    "\"kelly_pct\": 0.0, \"apostar\": false}"
                )
                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type":"application/json","x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01"},
                    json={"model":"claude-sonnet-4-20250514","max_tokens":1800,
                          "messages":[{"role":"user","content":[
                              {"type":"image","source":{"type":"base64","media_type":media_type,"data":b64}},
                              {"type":"text","text":EINSTEIN}
                          ]}]},
                    timeout=45
                )
                raw  = resp.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
                data = _jce.loads(raw)

                letra   = str(data.get("calificacion_letra","?"))
                pts     = int(data.get("puntuacion", 0))
                edge    = float(data.get("edge_pct", 0))
                kelly   = float(data.get("kelly_pct", 0))
                ev      = float(data.get("ev_por_unidad", 0))
                vered   = str(data.get("veredicto",""))
                estado  = str(data.get("estado_partido","pendiente"))
                apostar = bool(data.get("apostar", False))
                vars_oc = str(data.get("variables_ocultas_clave",""))
                sharp   = str(data.get("sharp_signal","desconocido"))
                ic95    = str(data.get("ic_95",""))
                p_real  = float(data.get("prob_real_pct", 0))
                p_impl  = float(data.get("prob_implicita_pct", 0))
                es_pa      = bool(data.get("es_pago_anticipado", False))
                es_parlay  = bool(data.get("es_parlay", False))
                sels_parlay= data.get("selecciones_parlay", [])
                cmap = {"A+":"#00ff88","A":"#00ff88","A-":"#00dd77","B+":"#7fff00",
                        "B":"#FFD700","B-":"#ffc200","C+":"#ff9500","C":"#ff7700",
                        "C-":"#ff6600","D":"#ff4444","F":"#cc0000"}
                color  = cmap.get(letra,"#777")
                ecol   = "#00ff88" if edge > 0 else "#ff4444"
                evcol  = "#00ff88" if ev > 0 else "#ff4444"
                scol   = {"favorable":"#00ff88","neutral":"#FFD700","contrario":"#ff4444"}.get(sharp,"#aaa")

                # ── PA / PARLAY BADGES ──
                if es_pa:
                    st.markdown(
                        "<div style='background:#001a40;border:2px solid #00ccff66;"
                        "border-radius:12px;padding:10px 16px;margin:8px 0;"
                        "font-size:.85rem;color:#00ccff'>"
                        "💰 <b>PAGO ANTICIPADO (PA)</b> — "
                        "⚽ Fútbol: gana por +2 goles en cualquier momento del partido · "
                        "🏀 NBA: +17 puntos de ventaja en cualquier momento. "
                        "Cuota baja (1.10-1.50) es completamente normal para este mercado.</div>",
                        unsafe_allow_html=True)
                if es_parlay and sels_parlay:
                    sel_html = "".join(
                        f"<div style='padding:4px 0;border-bottom:1px solid #1a1a40;font-size:.8rem;color:#aaa'>▸ {s}</div>"
                        for s in sels_parlay[:6] if s)
                    st.markdown(
                        f"<div style='background:#0a0018;border:2px solid #aa00ff66;"
                        "border-radius:12px;padding:10px 16px;margin:8px 0'>"
                        "<div style='font-size:.75rem;color:#aa00ff;font-weight:700;margin-bottom:6px'>"
                        f"🎰 PARLAY / COMBINADA — {len(sels_parlay)} selecciones</div>"
                        f"{sel_html}</div>",
                        unsafe_allow_html=True)
                # Partido terminado
                if "finalizado" in estado.lower() or "inválida" in vered.lower() or "invalida" in vered.lower():
                    st.markdown("<div style='background:#2a0000;border:2px solid #ff4444;border-radius:14px;padding:14px;margin-bottom:12px;text-align:center;font-weight:700;color:#ff4444;font-size:1rem'>⛔ PARTIDO YA FINALIZADO — Pick inválido para apostar</div>", unsafe_allow_html=True)

                # ── MAIN GRADE ──
                apostar_html = (
                    f"<div style='margin-top:10px;display:inline-block;background:{'#003300' if apostar else '#300000'};"
                    f"border:1.5px solid {'#00ff88' if apostar else '#ff4444'};border-radius:20px;"
                    f"padding:5px 20px;font-size:.9rem;font-weight:700;color:{'#00ff88' if apostar else '#ff4444'}'>"
                    f"{'✅ APOSTAR' if apostar else '🚫 NO APOSTAR'}</div>"
                )
                st.markdown(
                    f"<div style='background:linear-gradient(135deg,#080820,#100820);border:2.5px solid {color};"
                    f"border-radius:22px;padding:26px;text-align:center;margin-bottom:14px'>"
                    f"<div style='font-size:.65rem;color:#444;letter-spacing:.18em;margin-bottom:8px'>🧠 EINSTEIN BETS · ANÁLISIS PROFUNDO · 50K SIMULACIONES</div>"
                    f"<div style='font-size:5rem;font-weight:900;color:{color};line-height:1'>{letra}</div>"
                    f"<div style='font-size:1.15rem;font-weight:700;color:{color};margin-top:4px'>{pts}/100</div>"
                    f"<div style='font-size:.95rem;color:#aaa;margin-top:8px'>{vered}</div>"
                    f"{apostar_html}"
                    f"</div>", unsafe_allow_html=True)

                # ── METRICS ──
                st.markdown(
                    f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-bottom:10px'>"
                    f"<div class='mbox'><div class='mval' style='color:#00ccff;font-size:1.05rem'>{p_real:.1f}%</div><div class='mlbl'>Prob real</div></div>"
                    f"<div class='mbox'><div class='mval' style='color:#777;font-size:1.05rem'>{p_impl:.1f}%</div><div class='mlbl'>Prob cuota</div></div>"
                    f"<div class='mbox'><div class='mval' style='color:{ecol};font-size:1.05rem'>{'+' if edge>0 else ''}{edge:.1f}%</div><div class='mlbl'>Edge</div></div>"
                    f"<div class='mbox'><div class='mval' style='color:{evcol};font-size:1.05rem'>{'+' if ev>0 else ''}{ev:.3f}</div><div class='mlbl'>EV/unidad</div></div>"
                    f"</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:14px'>"
                    f"<div class='mbox'><div class='mval' style='color:#FFD700;font-size:1.05rem'>{kelly:.1f}%</div><div class='mlbl'>Kelly %</div></div>"
                    f"<div class='mbox'><div class='mval' style='color:{scol};font-size:.8rem;margin-top:6px'>{sharp.upper()}</div><div class='mlbl'>Sharp signal</div></div>"
                    f"<div class='mbox'><div style='font-size:.75rem;color:#aaa;padding:4px'>{ic95 or 'N/D'}</div><div class='mlbl'>IC 95%</div></div>"
                    f"</div>", unsafe_allow_html=True)

                # ── ANALYSIS CARD ──
                st.markdown(
                    f"<div class='acard'>"
                    f"<div style='font-size:.7rem;color:#FFD700;font-weight:700;text-transform:uppercase;letter-spacing:.12em;margin-bottom:10px'>📋 Análisis Einstein</div>"
                    f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px'>"
                    f"<div><span style='color:#555;font-size:.8rem'>Partido</span><br><b>{data.get('equipos','?')}</b></div>"
                    f"<div><span style='color:#555;font-size:.8rem'>Mercado</span><br><b>{data.get('mercado','?')}</b></div>"
                    f"<div><span style='color:#555;font-size:.8rem'>Cuota</span><br><b>{data.get('cuota','N/A')}</b></div>"
                    f"<div><span style='color:#555;font-size:.8rem'>Estado</span><br>{estado}</div>"
                    f"</div>"
                    f"<div style='padding-top:10px;border-top:1px solid #1a1a40'>"
                    f"<div style='color:#00ccff;font-size:.75rem;font-weight:700;margin-bottom:4px'>💡 RAZÓN PRINCIPAL</div>"
                    f"<div style='color:#ddd;font-size:.88rem;line-height:1.5'>{data.get('razon_principal','')}</div>"
                    f"</div>"
                    f"<div style='margin-top:10px;padding-top:8px;border-top:1px solid #1a1a40'>"
                    f"<div style='color:#aa00ff;font-size:.75rem;font-weight:700;margin-bottom:4px'>🔭 VARIABLES OCULTAS DETECTADAS</div>"
                    f"<div style='color:#bbb;font-size:.85rem;font-style:italic;line-height:1.5'>{vars_oc}</div>"
                    f"</div>"
                    f"<div style='margin-top:8px;color:#ff6600;font-size:.8rem'>⚠️ {data.get('riesgos_ocultos','')}</div>"
                    f"</div>", unsafe_allow_html=True)

                # ── ALTERNATIVE ──
                if data.get("alternativa_mercado"):
                    st.markdown(
                        f"<div style='background:linear-gradient(135deg,#001a10,#0a1a00);"
                        f"border:2px solid #00ff88;border-radius:14px;padding:16px;margin-top:10px'>"
                        f"<div style='font-size:.7rem;font-weight:700;color:#00ff88;letter-spacing:.12em;margin-bottom:8px'>✨ ALTERNATIVA INTELIGENTE</div>"
                        f"<div style='font-size:1rem;font-weight:700;color:#fff'>🎯 {data.get('alternativa_mercado','')}</div>"
                        f"<div style='font-size:.82rem;color:#aaa;margin-top:5px'>{data.get('alternativa_razon','')}</div>"
                        f"</div>", unsafe_allow_html=True)

                # ── EL PAPA DE EINSTEIN ──
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='background:linear-gradient(135deg,#0a0005,#050015);"
                    "border:2px solid #7c00ff44;border-radius:18px;padding:18px 22px;margin:12px 0'>"
                    "<div style='font-size:.65rem;color:#7c00ff;font-weight:700;letter-spacing:.2em;margin-bottom:4px'>"
                    "NIVEL SUPREMO</div>"
                    "<div style='font-size:1rem;font-weight:900;color:#EEEEFF;margin-bottom:4px'>"
                    "✝ EL PAPA DE EINSTEIN</div>"
                    "<div style='font-size:.78rem;color:#555'>Meta-IA auditora — verifica, recalcula y valida cada número de Einstein.</div>"
                    "</div>", unsafe_allow_html=True)
                with st.spinner("✝ El Papa auditando el análisis de Einstein..."):
                    papa_audit = papa_einstein_audit(data, b64, media_type, mem_ctx)
                render_papa_einstein(data, papa_audit, pts)

                # ── SAVE TO BRAIN ──
                st.markdown("<div class='shdr' style='margin-top:16px'>📥 Registrar resultado real</div>", unsafe_allow_html=True)
                st.markdown("<div style='color:#555;font-size:.8rem;margin-bottom:8px'>El cerebro aprende de cada resultado que registras.</div>", unsafe_allow_html=True)
                _mk=data.get("mercado","?"); _cq=data.get("cuota",0)
                _dp=data.get("deporte",""); _eq=data.get("equipos","")
                rc1, rc2, rc3 = st.columns(3)
                with rc1:
                    if st.button("✅ Acerté", key=f"rw_{key_sfx}_{pts}_{int(edge*10)}", use_container_width=True):
                        add_califica_result(_mk,_cq,"✅",True,_dp,_eq,edge,p_real,p_impl,pts)
                        st.success("🧠 Cerebro actualizado — acierto +1"); st.rerun()
                with rc2:
                    if st.button("❌ Fallé", key=f"rl_{key_sfx}_{pts}_{int(edge*10)}", use_container_width=True):
                        add_califica_result(_mk,_cq,"❌",False,_dp,_eq,edge,p_real,p_impl,pts)
                        st.error("🧠 Cerebro actualizado — fallo registrado"); st.rerun()
                with rc3:
                    if st.button("⏳ Pendiente", key=f"rp_{key_sfx}_{pts}_{int(edge*10)}", use_container_width=True):
                        add_califica_result(_mk,_cq,"⏳",False,_dp,_eq,edge,p_real,p_impl,pts)
                        st.info("Registrado — recuerda volver a registrar el resultado")

            except Exception as _ex:
                st.error(f"Error Einstein: {_ex}")

    # ── BRAIN LOG ──
    if bpicks:
        with st.expander(f"📊 Historial del cerebro ({len(bpicks)} picks)"):
            edges_p = bpatt.get("edges", {})
            if edges_p:
                edge_html = ""
                for rng,lbl in [("mas10","Edge >10%"),("5_10","Edge 5-10%"),("0_5","Edge 0-5%"),("neg","Edge negativo")]:
                    d=edges_p.get(rng,{}); n=d.get("n",0); p=d.get("pct")
                    if n>=2 and p is not None:
                        c="#00ff88" if p>=55 else ("#FFD700" if p>=45 else "#ff4444")
                        edge_html+=f"<div style='display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #1a1a40'><span style='color:#aaa;font-size:.8rem'>{lbl}</span><span style='color:{c};font-weight:700;font-size:.82rem'>{p}% acierto ({n})</span></div>"
                if edge_html:
                    st.markdown(f"<div class='acard' style='margin-bottom:10px;padding:12px 16px'><div style='font-size:.7rem;color:#FFD700;font-weight:700;margin-bottom:6px'>📈 RENDIMIENTO POR RANGO DE EDGE</div>{edge_html}</div>", unsafe_allow_html=True)
            for x in reversed(bpicks[-15:]):
                ic="✅" if x.get("correcto") else ("❌" if x.get("resultado")=="❌" else "⏳")
                ec_="#00ff88" if float(x.get("edge_pct",0))>0 else "#ff4444"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:6px 0;border-bottom:1px solid #1a1a40;font-size:.8rem'>"
                    f"<div><span style='color:#555'>{str(x.get('fecha',''))[:10]}</span> · "
                    f"<b>{str(x.get('mercado','?'))[:20]}</b> <span style='color:#aaa'>@{x.get('cuota',0)}</span><br>"
                    f"<span style='color:{ec_}'>{'+' if float(x.get('edge_pct',0))>0 else ''}{x.get('edge_pct',0):.1f}% edge</span>"
                    f"<span style='color:#555;margin-left:8px'>{x.get('deporte','')}</span></div>"
                    f"<div style='font-size:1.3rem'>{ic}</div></div>", unsafe_allow_html=True)
            if st.button("🗑️ Resetear cerebro", key=f"reset_{key_sfx}"):
                st.session_state["brain"] = {"picks":[],"stats":{},"patterns":{},"version":2}
                _save_brain(st.session_state["brain"]); st.rerun()


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

# ══════════════════════════════════════════════════════════
# MODELOS AVANZADOS — Dixon-Coles · Poisson Bivariado · Elo · Weibull+Markov
# Refs: Dixon&Coles 1997 · Karlis&Ntzoufras 2003 · Klaassen&Magnus 2001
# ══════════════════════════════════════════════════════════

def _dc_tau(gh, ga, lh, la, rho):
    """Factor de corrección Dixon-Coles para resultados bajos."""
    if gh==0 and ga==0: return max(1e-6, 1 - lh*la*rho)
    if gh==1 and ga==0: return 1 + la*rho
    if gh==0 and ga==1: return 1 + lh*rho
    if gh==1 and ga==1: return 1 - rho
    return 1.0

def dc_probabilities(hxg, axg, rho=-0.13):
    """Dixon-Coles 1997 — corrige sobreestimación Poisson en 0-0, 1-0, 0-1, 1-1."""
    lh, la = max(0.15, hxg), max(0.15, axg)
    matrix = {}; total = 0.0
    for gh in range(8):
        for ga in range(8):
            p = max(0.0,
                math.exp(-lh)*lh**gh/math.factorial(gh) *
                math.exp(-la)*la**ga/math.factorial(ga) *
                _dc_tau(gh, ga, lh, la, rho))
            matrix[(gh,ga)] = p; total += p
    if total > 0: matrix = {k: v/total for k,v in matrix.items()}
    ph   = sum(p for (gh,ga),p in matrix.items() if gh>ga)
    pd   = sum(p for (gh,ga),p in matrix.items() if gh==ga)
    pa   = sum(p for (gh,ga),p in matrix.items() if ga>gh)
    o25  = sum(p for (gh,ga),p in matrix.items() if gh+ga>2)
    o35  = sum(p for (gh,ga),p in matrix.items() if gh+ga>3)
    btts = sum(p for (gh,ga),p in matrix.items() if gh>0 and ga>0)
    cs_h = sum(p for (gh,ga),p in matrix.items() if ga==0)
    cs_a = sum(p for (gh,ga),p in matrix.items() if gh==0)
    top  = sorted(matrix.items(), key=lambda x: -x[1])[:6]
    return {"ph":ph,"pd":pd,"pa":pa,"o25":o25,"o35":o35,"btts":btts,
            "cs_h":cs_h,"cs_a":cs_a,"o15":sum(p for (gh,ga),p in matrix.items() if gh+ga>1),
            "top_scores":[(f"{gh}-{ga}", round(p*100,1)) for (gh,ga),p in top]}

def bivariate_poisson(hxg, axg, cov=0.10):
    """Karlis & Ntzoufras 2003 — modela correlación real entre goles locales y visitantes."""
    lam1=max(0.01,hxg-cov); lam2=max(0.01,axg-cov); lam3=max(0.01,cov)
    matrix = {}; total = 0.0
    for gh in range(8):
        for ga in range(8):
            p = sum(
                math.exp(-lam1)*lam1**(gh-k)/math.factorial(gh-k) *
                math.exp(-lam2)*lam2**(ga-k)/math.factorial(ga-k) *
                math.exp(-lam3)*lam3**k/math.factorial(k)
                for k in range(min(gh,ga)+1))
            matrix[(gh,ga)] = max(0.0, p); total += p
    if total > 0: matrix = {k: v/total for k,v in matrix.items()}
    return {
        "ph": sum(p for (gh,ga),p in matrix.items() if gh>ga),
        "pd": sum(p for (gh,ga),p in matrix.items() if gh==ga),
        "pa": sum(p for (gh,ga),p in matrix.items() if ga>gh),
        "o25":sum(p for (gh,ga),p in matrix.items() if gh+ga>2),
        "o35":sum(p for (gh,ga),p in matrix.items() if gh+ga>3),
        "btts":sum(p for (gh,ga),p in matrix.items() if gh>0 and ga>0),
    }

# ── Elo dinámico con pesos exponenciales ──
try:
    import json as _json_elo
    with open("/tmp/tgl_elo.json") as _ef: _elo_db = _json_elo.load(_ef)
except: _elo_db = {}

def _get_elo(tid): return float(_elo_db.get(str(tid), 1500.0))

def _elo_from_form(team_id, form):
    """Elo implícito desde forma reciente — pesos exponenciales."""
    base = _get_elo(team_id)
    if not form: return base
    w = [2**(-i) for i in range(len(form[:10]))]
    tw = sum(w)
    score = sum(wi*(1.0 if r.get("result")=="W" else (0.5 if r.get("result")=="D" else 0.0))
                for r,wi in zip(form[:10],w))
    return base + (score/tw - 0.5) * 180   # ±90 puntos de ajuste

def elo_win_prob(home_id, away_id, hform=None, aform=None, home_adv=50):
    """P(local gana) con Elo dinámico + ventaja de campo."""
    ra = _elo_from_form(home_id, hform) + home_adv
    rb = _elo_from_form(away_id, aform)
    return 1 / (1 + 10**((rb - ra)/400))

# ── Weibull + Markov para tenis (Klaassen & Magnus 2001) ──
def _weibull_srv_prob(rank_srv, rank_ret, surface="hard"):
    base = {"hard":0.630,"clay":0.600,"grass":0.662,"carpet":0.645}.get(surface.lower(),0.630)
    return max(0.35, min(0.78, base - (rank_srv - rank_ret)*0.00015))

def _markov_game(p):
    """P(ganar juego) dado p(ganar punto) — fórmula cerrada exacta."""
    q = 1 - p
    pg = sum(math.comb(a+3,3)*p**4*q**a for a in range(3))
    pg += math.comb(6,3)*(p*q)**3 * (p**2/(p**2+q**2))
    return max(0.01, min(0.99, pg))

def weibull_match_prob(rank1, rank2, odd_1=0, odd_2=0, surface="hard", best_of=3):
    """Probabilidad de partido: Weibull (punto) → Markov (juego → set → partido)."""
    ps1 = (_markov_game(_weibull_srv_prob(rank1, rank2, surface)) +
           (1 - _markov_game(_weibull_srv_prob(rank2, rank1, surface)))) / 2
    ps1 = max(0.01, min(0.99, ps1))
    need = 2 if best_of==3 else 3
    p1m = sum(math.comb(s-1,need-1)*ps1**need*(1-ps1)**(s-need) for s in range(need,best_of+1))
    p1m = max(0.01, min(0.99, p1m))
    if odd_1>1 and odd_2>1:
        t = 1/odd_1+1/odd_2
        p1m = 0.60*p1m + 0.40*(1/odd_1)/t   # 60% Weibull, 40% mercado limpio
    return {"p1":round(p1m,4),"p2":round(1-p1m,4)}

# ── ENSEMBLE: combina todos con pesos óptimos ──

# ══════════════════════════════════════════════════════════════════════
# PRE-MATCH INTELLIGENCE BOT
# Raspa noticias, bajas, lesiones, sanciones, clima antes del partido.
# Ajusta automáticamente las probabilidades de los modelos.
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# 🤖 BADRINO — Pre-Match Intelligence Bot
#    Busca en internet: alineaciones, lesiones, sanciones, rumores.
#    Fútbol: alineaciones 60-90 min antes del partido.
#    NBA: injury report 30 min antes.
#    Tenis: rumores, lesiones, superficie, forma reciente.
#    Ajusta automáticamente todas las probabilidades del modelo.
# ══════════════════════════════════════════════════════════════════════════════

def _badrino_minutes_to_kickoff(hora_str):
    """Calcula minutos hasta el partido. hora_str = 'HH:MM' CDMX."""
    try:
        now  = datetime.now(CDMX)
        h, m = map(int, hora_str.replace("h","").split(":"))
        kick = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if kick < now: kick += timedelta(days=1)
        return int((kick - now).total_seconds() / 60)
    except:
        return 999


@st.cache_data(ttl=600, show_spinner=False)
def badrino_web_search(sport, home, away, league_name, hora_partido="",
                        rank1=0, rank2=0, ou_line=0, hxg=0, axg=0,
                        model_ph=0.33, model_pd=0.25, model_pa=0.33):
    """
    🤖 BADRINO — core function.
    Usa web_search tool de Anthropic para buscar en internet
    alineaciones, lesiones, rumores y ajustar el modelo.
    TTL = 10 min (alineaciones cambian cerca del partido).
    """
    if not ANTHROPIC_API_KEY:
        return {"error": "Sin API key", "badrino_ok": False}

    mins = _badrino_minutes_to_kickoff(hora_partido) if hora_partido else 999
    fecha_hoy = datetime.now(CDMX).strftime("%d %B %Y")
    fecha_corta = datetime.now(CDMX).strftime("%d/%m/%Y")

    # ── Construir queries específicas por deporte ──
    if sport == "soccer":
        queries = [
            f"{home} vs {away} alineacion titular hoy {fecha_hoy}",
            f"{home} vs {away} bajas lesiones sancionados {fecha_corta}",
            f"{home} lesionados bajas confirmadas {datetime.now(CDMX).strftime('%B %Y')}",
            f"{away} lesionados bajas confirmadas {datetime.now(CDMX).strftime('%B %Y')}",
        ]
        timing_note = (
            f"⚽ El partido es en ~{mins} minutos. "
            + ("BUSCA ALINEACION CONFIRMADA — ya debería estar publicada." if mins <= 90
               else "Las alineaciones salen 60-90 min antes del partido.")
        )
    elif sport == "nba":
        queries = [
            f"{home} vs {away} NBA injury report today {fecha_hoy}",
            f"{home} NBA out questionable tonight {datetime.now(CDMX).strftime('%B %Y')}",
            f"{away} NBA out questionable tonight {datetime.now(CDMX).strftime('%B %Y')}",
        ]
        timing_note = (
            f"🏀 El partido es en ~{mins} minutos. "
            + ("INJURY REPORT FINAL disponible — busca quién está OUT." if mins <= 90
               else "El injury report final sale 30 min antes del partido.")
        )
    else:  # tennis
        queries = [
            f"{home} vs {away} tenis lesion retiro {datetime.now(CDMX).strftime('%B %Y')}",
            f"{home} tenis lesion forma reciente {datetime.now(CDMX).strftime('%B %Y')}",
            f"{away} tenis lesion forma reciente {datetime.now(CDMX).strftime('%B %Y')}",
            f"{home} vs {away} {league_name} preview prediction",
        ]
        timing_note = f"🎾 Partido en ~{mins} minutos. Busca lesiones, retiros o rumores recientes."

    # ── Construir contexto del modelo ──
    if sport == "soccer":
        model_ctx = f"xG local={hxg:.2f} xG visit={axg:.2f} | Prob modelo: {home} {model_ph*100:.1f}% / Emp {model_pd*100:.1f}% / {away} {model_pa*100:.1f}%"
    elif sport == "nba":
        model_ctx = f"O/U line={ou_line} | Prob modelo: {home} {model_ph*100:.1f}% / {away} {model_pa*100:.1f}%"
    else:
        model_ctx = f"Ranking {home}=#{rank1 if rank1<900 else '?'} Ranking {away}=#{rank2 if rank2<900 else '?'} | Prob modelo: {home} {model_ph*100:.1f}% / {away} {model_pa*100:.1f}%"

    # ── Prompt para BADRINO con web_search ──
    system_prompt = f"""Eres BADRINO, el bot de inteligencia pre-partido más avanzado del mundo.
Tu trabajo: usar web_search para buscar información REAL y ACTUAL sobre el partido, 
luego analizar el impacto y ajustar las probabilidades del modelo estadístico.

DEPORTE: {sport.upper()}
PARTIDO: {home} vs {away}
LIGA: {league_name}
FECHA: {fecha_hoy}
CONTEXTO MODELO: {model_ctx}
{timing_note}

PROCESO OBLIGATORIO:
1. Busca en internet con web_search las queries más útiles para este partido.
2. Para FÚTBOL busca: alineación titular de ambos equipos (XI), bajas, lesiones, sanciones.
3. Para NBA busca: injury report oficial, quién está OUT/Questionable/Doubtful.
4. Para TENIS busca: lesiones recientes, retiros, forma en superficie, viajes largos.
5. Analiza el impacto de todo lo encontrado en las probabilidades.

REGLAS DE AJUSTE:
- Portero titular OUT: +0.06 a +0.09 prob rival
- Goleador principal OUT: -0.3 a -0.5 xG del equipo, -0.08 prob gana
- 2-3 bajas defensivas clave: +0.3 a +0.5 xG rival
- Estrella NBA OUT (All-Star o top scorer): -8 a -12 pts al total, +0.10 prob rival
- Jugador NBA Questionable: -4 a -6 pts, incertidumbre
- Tenista con lesión activa en rodilla/tobillo en superficie rápida: -0.10 a -0.15 prob
- Rotación esperada (tercer partido en 7 días): -0.06 a -0.10 prob del equipo cansado
- Back-to-back NBA: -6 a -10 pts al total

RESPONDE SOLO EN JSON (sin markdown, sin texto fuera del JSON):
{{
  "bajas_home": ["jugador — razón/status"],
  "bajas_away": ["jugador — razón/status"],
  "sanciones_home": ["jugador — tarjetas/suspensión"],
  "sanciones_away": ["jugador — tarjetas/suspensión"],
  "dudas_home": ["jugador — duda/questionable"],
  "dudas_away": ["jugador — duda/questionable"],
  "alineacion_home": ["XI confirmado o 'No disponible aún'"],
  "alineacion_away": ["XI confirmado o 'No disponible aún'"],
  "alineacion_disponible": false,
  "noticias_clave": ["noticia 1", "noticia 2", "noticia 3"],
  "clima_impacto": "descripción o Sin impacto significativo",
  "motivacion_home": "motivación y contexto de {home}",
  "motivacion_away": "motivación y contexto de {away}",
  "rumores_lesion_home": "rumores o lesiones de {home} — solo tenis/NBA",
  "rumores_lesion_away": "rumores o lesiones de {away} — solo tenis/NBA",
  "ajuste_ph": 0.0,
  "ajuste_pd": 0.0,
  "ajuste_pa": 0.0,
  "ajuste_xg_home": 0.0,
  "ajuste_xg_away": 0.0,
  "ajuste_total_pts": 0.0,
  "impacto_ou": "sube/baja/neutro — explicación",
  "impacto_nivel": "ALTO/MEDIO/BAJO/NULO",
  "equipo_mas_afectado": "{home}/{away}/ambos/ninguno",
  "recomendacion_tactica": "qué mercado se beneficia de esta info",
  "confianza_datos": "alta/media/baja",
  "fuentes_usadas": ["url o nombre de fuente 1", "fuente 2"],
  "resumen": "2-3 líneas de lo más importante para apostar en este partido"
}}"""

    user_msg = f"Analiza {home} vs {away} ({league_name}, {fecha_hoy}). Busca en internet y dame el JSON completo."

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 3000,
                "system": system_prompt,
                "tools": [{"type": "web_search_20250305", "name": "web_search"}],
                "messages": [{"role": "user", "content": user_msg}]
            },
            timeout=60   # web search tarda más
        )
        if resp.status_code != 200:
            return {"error": f"API {resp.status_code}", "badrino_ok": False}

        # ── Procesar respuesta (puede tener tool_use + text) ──
        content_blocks = resp.json().get("content", [])
        final_text = ""
        for block in content_blocks:
            if block.get("type") == "text":
                final_text += block.get("text", "")

        if not final_text:
            return {"error": "Sin respuesta de texto", "badrino_ok": False}

        raw = final_text.strip()
        raw = raw.replace("```json","").replace("```","").strip()
        # Extraer JSON si hay texto rodeándolo
        if "{" in raw:
            raw = raw[raw.find("{"):raw.rfind("}")+1]

        import json as _jb
        result = _jb.loads(raw)
        result["badrino_ok"] = True
        result["mins_to_kickoff"] = mins
        return result

    except Exception as e:
        return {"error": str(e), "badrino_ok": False}


def apply_prematch_adjustments(model_result, ai_analysis, sport="soccer"):
    """Aplica los ajustes Badrino al modelo estadístico."""
    if not ai_analysis or not ai_analysis.get("badrino_ok"): 
        return model_result, False

    adj_ph  = float(ai_analysis.get("ajuste_ph", 0))
    adj_pd  = float(ai_analysis.get("ajuste_pd", 0))
    adj_pa  = float(ai_analysis.get("ajuste_pa", 0))
    adj_xgh = float(ai_analysis.get("ajuste_xg_home", 0))
    adj_xga = float(ai_analysis.get("ajuste_xg_away", 0))
    adj_pts = float(ai_analysis.get("ajuste_total_pts", 0))

    if max(abs(adj_ph),abs(adj_pd),abs(adj_pa),abs(adj_xgh),abs(adj_xga),abs(adj_pts)) < 0.01:
        return model_result, False

    adjusted = dict(model_result)
    if sport == "soccer":
        ph = max(0.01, adjusted.get("ph",0.33) + adj_ph)
        pd = max(0.01, adjusted.get("pd",0.25) + adj_pd)
        pa = max(0.01, adjusted.get("pa",0.33) + adj_pa)
        s  = ph+pd+pa
        adjusted["ph"]=ph/s; adjusted["pd"]=pd/s; adjusted["pa"]=pa/s
        if adj_xgh or adj_xga:
            adjusted["hxg"] = max(0.1, adjusted.get("hxg",1.3)+adj_xgh)
            adjusted["axg"] = max(0.1, adjusted.get("axg",1.0)+adj_xga)
    elif sport == "nba":
        if adj_pts:
            adjusted["proj"] = max(150, adjusted.get("proj",220)+adj_pts)
        if adj_ph or adj_pa:
            ph = max(0.05, adjusted.get("ph",0.5)+adj_ph)
            pa = max(0.05, adjusted.get("pa",0.5)+adj_pa)
            s  = ph+pa; adjusted["ph"]=ph/s; adjusted["pa"]=pa/s
    elif sport == "tennis":
        ph = max(0.05, adjusted.get("p1",0.5)+adj_ph)
        pa = max(0.05, adjusted.get("p2",0.5)+adj_pa)
        s  = ph+pa; adjusted["p1"]=ph/s; adjusted["p2"]=pa/s

    adjusted["_prematch_adjusted"]=True
    adjusted["_adj_ph"]=adj_ph; adjusted["_adj_pa"]=adj_pa
    return adjusted, True


def render_prematch_bot(sport, home, away, league_slug, league_name,
                         model_result, hxg=0, axg=0, ou_line=0,
                         rank1=0, rank2=0, hora_partido=""):
    """🤖 BADRINO — UI renderer."""

    model_ph = model_result.get("ph", model_result.get("p1",0.5))
    model_pd = model_result.get("pd", 0)
    model_pa = model_result.get("pa", model_result.get("p2",0.5))
    mins     = _badrino_minutes_to_kickoff(hora_partido) if hora_partido else 999

    # ── Header Badrino ──
    timing_color = "#ff4444" if mins<=30 else ("#ff9500" if mins<=90 else "#00ccff")
    timing_txt   = (
        f"⚡ {mins} min — ALINEACIONES DISPONIBLES" if sport=="soccer" and mins<=90
        else f"⚡ {mins} min — INJURY REPORT FINAL" if sport=="nba" and mins<=60
        else f"⚡ {mins} min para el partido"
    ) if mins < 999 else "📡 Análisis bajo demanda"

    st.markdown(
        f"<div style='background:linear-gradient(135deg,#05051f,#0a0a30);"
        f"border:2px solid #aa00ff44;border-radius:16px;padding:14px 18px;margin:8px 0'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center'>"
        f"<div>"
        f"<div style='font-size:.65rem;color:#aa00ff;font-weight:700;letter-spacing:.2em'>🤖 BADRINO</div>"
        f"<div style='font-size:.88rem;font-weight:700;color:#EEEEFF'>Pre-Match Intelligence Bot</div>"
        f"<div style='font-size:.72rem;color:#555;margin-top:2px'>"
        f"Web search · Alineaciones · Lesiones · Rumores · Ajuste automático</div>"
        f"</div>"
        f"<div style='text-align:right'>"
        f"<div style='font-size:.72rem;color:{timing_color};font-weight:700'>{timing_txt}</div>"
        f"</div></div></div>",
        unsafe_allow_html=True)

    cache_key = f"badrino_{sport}_{home[:8]}_{away[:8]}"
    col1, col2 = st.columns([3,1])
    with col2:
        run = st.button("🔍 Activar Badrino", key=f"badrino_btn_{cache_key}",
                        use_container_width=True)
    with col1:
        if mins <= 90 and sport == "soccer":
            st.markdown(f"<div style='font-size:.75rem;color:{timing_color};padding-top:8px'>⚽ Busca alineación confirmada en internet ahora</div>", unsafe_allow_html=True)
        elif mins <= 60 and sport == "nba":
            st.markdown(f"<div style='font-size:.75rem;color:{timing_color};padding-top:8px'>🏀 Busca injury report final en internet</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:.75rem;color:#555;padding-top:8px'>Busca en internet bajas, lesiones, rumores y ajusta el modelo</div>", unsafe_allow_html=True)

    if run or st.session_state.get(cache_key+"_done"):
        if run: st.session_state[cache_key+"_done"] = True

        with st.spinner("🌐 Badrino buscando en internet..."):
            bd = badrino_web_search(
                sport=sport, home=home, away=away,
                league_name=league_name, hora_partido=hora_partido,
                rank1=rank1, rank2=rank2, ou_line=ou_line,
                hxg=hxg, axg=axg,
                model_ph=model_ph, model_pd=model_pd, model_pa=model_pa
            )

        if not bd.get("badrino_ok"):
            st.warning(f"⚠️ Badrino no pudo completar la búsqueda: {bd.get('error','')}")
            return model_result, False

        # ── IMPACT HEADER ──
        nivel   = bd.get("impacto_nivel","NULO")
        afect   = bd.get("equipo_mas_afectado","ninguno")
        conf    = bd.get("confianza_datos","baja")
        resumen = bd.get("resumen","")
        mins_k  = bd.get("mins_to_kickoff", 999)
        nivel_c = {"ALTO":"#ff4444","MEDIO":"#ff9500","BAJO":"#FFD700","NULO":"#00ff88"}.get(nivel,"#aaa")
        conf_c  = {"alta":"#00ff88","media":"#FFD700","baja":"#ff9500"}.get(conf,"#aaa")

        st.markdown(
            f"<div style='background:#0d0d2e;border:2px solid {nivel_c}44;"
            f"border-radius:16px;padding:16px 20px;margin:8px 0'>"
            f"<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px'>"
            f"<div><div style='font-size:.65rem;color:#555;font-weight:700;letter-spacing:.12em;margin-bottom:3px'>"
            f"🤖 BADRINO — REPORTE PRE-PARTIDO</div>"
            f"<div style='font-size:1rem;font-weight:900;color:{nivel_c}'>⚡ IMPACTO {nivel}</div></div>"
            f"<div style='text-align:right'>"
            f"<div style='font-size:.65rem;color:#555'>Más afectado</div>"
            f"<div style='font-weight:700;color:#EEEEFF;font-size:.85rem'>{afect}</div>"
            f"<div style='font-size:.65rem;color:{conf_c};margin-top:2px'>Confianza: {conf}</div>"
            f"</div></div>"
            f"<div style='font-size:.82rem;color:#aaa;line-height:1.6;border-top:1px solid #1a1a40;padding-top:8px'>"
            f"{resumen}</div></div>", unsafe_allow_html=True)

        # ── ALINEACIONES (solo fútbol) ──
        if sport == "soccer":
            alin_h = bd.get("alineacion_home",[])
            alin_a = bd.get("alineacion_away",[])
            alin_ok = bd.get("alineacion_disponible", False) or (
                alin_h and alin_h[0].lower() not in ["no disponible aún","no disponible","n/a",""])

            st.markdown(
                f"<div style='font-size:.7rem;color:#00ccff;font-weight:700;"
                f"letter-spacing:.1em;margin:10px 0 6px'>⚽ ALINEACIONES</div>",
                unsafe_allow_html=True)

            if alin_ok and (alin_h or alin_a):
                c1, c2 = st.columns(2)
                def render_xi(team, xi, col):
                    with col:
                        st.markdown(
                            f"<div style='background:#07071a;border-radius:10px;padding:10px 12px'>"
                            f"<div style='font-size:.7rem;color:#00ff88;font-weight:700;margin-bottom:6px'>"
                            f"🟢 XI TITULAR — {team[:18].upper()}</div>"
                            + "".join(
                                f"<div style='font-size:.8rem;color:#ccc;padding:3px 0;"
                                f"border-bottom:1px solid #111'>{p}</div>"
                                for p in (xi[:11] if xi else ["No disponible aún"]))
                            + "</div>", unsafe_allow_html=True)
                render_xi(home, alin_h, c1)
                render_xi(away, alin_a, c2)
            else:
                mins_left = mins_k if mins_k < 999 else "?"
                st.markdown(
                    f"<div style='background:#07071a;border-radius:10px;padding:10px 14px;"
                    f"color:#555;font-size:.8rem;text-align:center'>"
                    f"⏳ Alineaciones no publicadas aún — salen ~60-90 min antes del partido"
                    f"{'  (' + str(mins_left) + ' min restantes)' if mins_left != '?' else ''}"
                    f"</div>", unsafe_allow_html=True)

        # ── BAJAS, SANCIONES Y DUDAS ──
        def render_plist(title, players, color, icon):
            if not players: return ""
            items = "".join(
                f"<div style='padding:4px 0;border-bottom:1px solid #111;"
                f"font-size:.79rem;color:#aaa'>{icon} {p}</div>"
                for p in players[:7] if p)
            return (
                f"<div style='background:#07071a;border-left:3px solid {color};"
                f"border-radius:0 10px 10px 0;padding:9px 13px;margin:4px 0'>"
                f"<div style='font-size:.68rem;color:{color};font-weight:700;margin-bottom:5px'>{title}</div>"
                f"{items}</div>")

        hb = bd.get("bajas_home",[]); ab = bd.get("bajas_away",[])
        hs = bd.get("sanciones_home",[]); as_ = bd.get("sanciones_away",[])
        hd = bd.get("dudas_home",[]); ad = bd.get("dudas_away",[])

        has_players = any([hb,ab,hs,as_,hd,ad])
        if has_players:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div style='font-size:.75rem;color:#EEEEFF;font-weight:700;margin:8px 0 3px'>🏠 {home[:22]}</div>", unsafe_allow_html=True)
                for html in [
                    render_plist("🚑 BAJAS CONFIRMADAS", hb, "#ff4444","❌"),
                    render_plist("🟨 SANCIONES", hs, "#ff9500","🟨"),
                    render_plist("⚠️ DUDAS", hd, "#FFD700","⚠️"),
                ]:
                    if html: st.markdown(html, unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='font-size:.75rem;color:#EEEEFF;font-weight:700;margin:8px 0 3px'>✈️ {away[:22]}</div>", unsafe_allow_html=True)
                for html in [
                    render_plist("🚑 BAJAS CONFIRMADAS", ab, "#ff4444","❌"),
                    render_plist("🟨 SANCIONES", as_, "#ff9500","🟨"),
                    render_plist("⚠️ DUDAS", ad, "#FFD700","⚠️"),
                ]:
                    if html: st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#555;font-size:.8rem;padding:8px;text-align:center'>✅ Sin bajas confirmadas detectadas</div>", unsafe_allow_html=True)

        # ── RUMORES LESIONES (Tenis / NBA) ──
        rum_h = bd.get("rumores_lesion_home","")
        rum_a = bd.get("rumores_lesion_away","")
        if (rum_h or rum_a) and sport in ("tennis","nba"):
            st.markdown("<div style='font-size:.7rem;color:#aa00ff;font-weight:700;letter-spacing:.1em;margin:10px 0 5px'>🔊 RUMORES E INTEL</div>", unsafe_allow_html=True)
            if rum_h and rum_h.lower() not in ["","ninguno","n/a","none"]:
                st.markdown(f"<div style='background:#07071a;border-left:3px solid #aa00ff;border-radius:0 8px 8px 0;padding:7px 12px;margin:3px 0;font-size:.8rem;color:#aaa'>🏠 <b>{home[:18]}:</b> {rum_h}</div>", unsafe_allow_html=True)
            if rum_a and rum_a.lower() not in ["","ninguno","n/a","none"]:
                st.markdown(f"<div style='background:#07071a;border-left:3px solid #aa00ff;border-radius:0 8px 8px 0;padding:7px 12px;margin:3px 0;font-size:.8rem;color:#aaa'>✈️ <b>{away[:18]}:</b> {rum_a}</div>", unsafe_allow_html=True)

        # ── NOTICIAS CLAVE ──
        noticias = bd.get("noticias_clave",[])
        if noticias:
            st.markdown("<div style='font-size:.7rem;color:#00ccff;font-weight:700;letter-spacing:.1em;margin:10px 0 5px'>📰 NOTICIAS CLAVE</div>", unsafe_allow_html=True)
            for n in noticias[:4]:
                if n and n.lower() not in ["ninguna","n/a","none",""]:
                    st.markdown(f"<div style='background:#07071a;border-left:3px solid #00ccff33;border-radius:0 8px 8px 0;padding:6px 12px;margin:3px 0;font-size:.79rem;color:#aaa'>📌 {n}</div>", unsafe_allow_html=True)

        # ── CLIMA E IMPACTO O/U ──
        clima  = bd.get("clima_impacto","")
        ou_imp = bd.get("impacto_ou","")
        if (clima and "sin impacto" not in clima.lower()) or ou_imp:
            st.markdown(
                f"<div style='background:#07071a;border:1px solid #252555;border-radius:10px;"
                f"padding:10px 14px;margin:6px 0;font-size:.79rem;color:#aaa'>"
                + (f"🌦️ <b style='color:#00ccff'>Clima:</b> {clima}<br>" if clima and "sin impacto" not in clima.lower() else "")
                + (f"📊 <b style='color:#FFD700'>Over/Under:</b> {ou_imp}" if ou_imp else "")
                + "</div>", unsafe_allow_html=True)

        # ── MOTIVACIÓN ──
        mot_h = bd.get("motivacion_home",""); mot_a = bd.get("motivacion_away","")
        if mot_h or mot_a:
            with st.expander("🎯 Motivación y Contexto"):
                if mot_h: st.markdown(f"<div style='font-size:.8rem;color:#aaa;padding:6px 0;border-bottom:1px solid #1a1a40'><b style='color:#00ff88'>🏠 {home}:</b> {mot_h}</div>", unsafe_allow_html=True)
                if mot_a: st.markdown(f"<div style='font-size:.8rem;color:#aaa;padding:6px 0'><b style='color:#aa00ff'>✈️ {away}:</b> {mot_a}</div>", unsafe_allow_html=True)

        # ── FUENTES ──
        fuentes = bd.get("fuentes_usadas",[])
        if fuentes:
            with st.expander("🔗 Fuentes consultadas por Badrino"):
                for f_ in fuentes[:6]:
                    if f_: st.markdown(f"<div style='font-size:.75rem;color:#555;padding:2px 0'>🔗 {f_}</div>", unsafe_allow_html=True)

        # ── AJUSTE AL MODELO ──
        adj_ph  = float(bd.get("ajuste_ph",0))
        adj_pd  = float(bd.get("ajuste_pd",0))
        adj_pa  = float(bd.get("ajuste_pa",0))
        adj_xgh = float(bd.get("ajuste_xg_home",0))
        adj_xga = float(bd.get("ajuste_xg_away",0))
        adj_pts = float(bd.get("ajuste_total_pts",0))
        has_adj = max(abs(adj_ph),abs(adj_pd),abs(adj_pa),abs(adj_xgh),abs(adj_xga),abs(adj_pts)) >= 0.01

        if has_adj:
            rec = bd.get("recomendacion_tactica","")
            boxes = ""

            def adj_box(label, orig, delta, fmt="{:.1f}%", scale=100):
                if abs(delta) < 0.008: return ""
                new_v = orig+delta
                dc = "#00ff88" if delta>0 else "#ff4444"
                arr = "▲" if delta>0 else "▼"
                return (
                    f"<div style='background:#07071a;border-radius:10px;padding:10px;text-align:center'>"
                    f"<div style='font-size:.65rem;color:#555;margin-bottom:3px'>{label}</div>"
                    f"<div style='font-size:.75rem;color:#555'>{fmt.format(orig*scale)}</div>"
                    f"<div style='font-size:.95rem;font-weight:900;color:{dc}'>{arr} {fmt.format(new_v*scale)}</div>"
                    f"<div style='font-size:.65rem;color:{dc}'>{('+' if delta>0 else '')}{fmt.format(delta*scale)}</div></div>")

            if sport=="soccer":
                boxes += adj_box(f"🏠 {home[:11]}", model_ph, adj_ph)
                boxes += adj_box(f"✈️ {away[:11]}", model_pa, adj_pa)
                if adj_xgh: boxes += adj_box("⚽ xG Local", hxg, adj_xgh, "{:.2f} xG", 1)
                if adj_xga: boxes += adj_box("⚽ xG Visita", axg, adj_xga, "{:.2f} xG", 1)
            elif sport=="nba":
                if adj_pts: boxes += adj_box("🏀 Total pts", ou_line, adj_pts, "{:.1f} pts", 1)
                if adj_ph: boxes += adj_box(f"🏠 {home[:11]}", model_ph, adj_ph)
                if adj_pa: boxes += adj_box(f"✈️ {away[:11]}", model_pa, adj_pa)
            elif sport=="tennis":
                boxes += adj_box(f"🎾 {home[:13]}", model_ph, adj_ph)
                boxes += adj_box(f"🎾 {away[:13]}", model_pa, adj_pa)

            if boxes:
                st.markdown(
                    "<div style='background:linear-gradient(135deg,#050518,#0a0a28);"
                    "border:2px solid #aa00ff44;border-radius:14px;padding:14px 18px;margin:10px 0'>"
                    "<div style='font-size:.68rem;color:#aa00ff;font-weight:700;letter-spacing:.12em;margin-bottom:10px'>"
                    "⚡ BADRINO — AJUSTE AUTOMÁTICO AL MODELO</div>"
                    f"<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px'>"
                    f"{boxes}</div>"
                    + (f"<div style='margin-top:10px;background:#12122a;border-radius:8px;padding:8px 14px;"
                       f"font-size:.82rem;color:#00ff88'>💡 <b>Badrino recomienda:</b> {rec}</div>" if rec else "")
                    + "</div>", unsafe_allow_html=True)

        # Aplicar ajustes al modelo y devolver
        adjusted_model, was_adjusted = apply_prematch_adjustments(model_result, bd, sport)
        return adjusted_model, was_adjusted

    return model_result, False


def ensemble_football(hxg, axg, h2h_s=None, hform=None, aform=None, home_id=None, away_id=None):
    """
    Dixon-Coles 45% + Poisson Bivariado 30% + Elo 15% + H2H 10%.
    Desviación estándar entre modelos = señal de consenso / confianza.
    """
    dc  = dc_probabilities(hxg, axg)
    bvp = bivariate_poisson(hxg, axg)
    elo_ph = elo_win_prob(home_id or "h", away_id or "a", hform, aform)
    h2h_ph = (h2h_s["hp"]/100 if h2h_s and h2h_s.get("tot",0)>=5 else dc["ph"])
    h2h_pd = (h2h_s["dp"]/100 if h2h_s and h2h_s.get("tot",0)>=5 else dc["pd"])
    ph = 0.45*dc["ph"] + 0.30*bvp["ph"] + 0.15*elo_ph + 0.10*h2h_ph
    pd = 0.45*dc["pd"] + 0.30*bvp["pd"] + 0.25*h2h_pd
    pa = max(0.01, 1-ph-pd)
    s  = ph+pd+pa; ph/=s; pd/=s; pa/=s
    std = float(np.std([dc["ph"], bvp["ph"], elo_ph, h2h_ph]))
    consensus = "🟢 ALTO" if std<0.04 else ("🟡 MEDIO" if std<0.08 else "🔴 BAJO")
    return {
        "ph":ph,"pd":pd,"pa":pa,
        "o15":dc["o15"],"o25":0.5*dc["o25"]+0.5*bvp["o25"],
        "o35":0.5*dc["o35"]+0.5*bvp["o35"],
        "btts":0.5*dc["btts"]+0.5*bvp["btts"],
        "cs_h":dc["cs_h"],"cs_a":dc["cs_a"],
        "hxg":round(hxg,2),"axg":round(axg,2),
        "top_scores":dc["top_scores"],
        "consensus":consensus,
        "dc_ph":round(dc["ph"]*100,1),"bvp_ph":round(bvp["ph"]*100,1),
        "elo_ph":round(elo_ph*100,1),"h2h_ph":round(h2h_ph*100,1),
        "model":"Ensemble DC+BVP+Elo+H2H",
    }


def veredicto_academico(mc, dp, odd_h, odd_a, odd_d, home, away, best_market=None, best_prob=None, best_odd=None):
    """
    Veredicto académico único que integra TODOS los modelos:
    Dixon-Coles 45% + Poisson BV 30% + Elo Dinámico 15% + H2H 10%
    Evalúa el mercado con mayor probabilidad (no solo 1X2).

    Semáforo:
    🟢 APOSTAR       — señal fuerte (score ≥ 7)
    🟡 BANK MEDIO    — señal moderada (score 4-6)
    🔴 NO APOSTAR    — sin valor estadístico (score < 4)
    """
    import statistics, math

    ph = dp["ph"]; pd = dp["pd"]; pa = dp["pa"]

    # ── Identificar el mercado a evaluar ──
    if best_market and best_prob:
        mkt_lbl  = best_market
        mkt_prob = best_prob
        mkt_odd  = best_odd or 0
        # Si es Over 2.5 / AA / Doble Chance, usar su prob directamente
        is_totals  = any(x in best_market for x in ["Over","Ambos","AA","DC","o Emp","o "])
        fav_name   = best_market  if is_totals else (home if ph>=pa else away)
    else:
        fav_is_home = ph >= pa
        fav_name = home if fav_is_home else away
        mkt_prob = max(ph, pa)
        mkt_odd  = odd_h if fav_is_home else odd_a
        is_totals = False

    # ── Probabilidades de cada modelo apuntando al mismo favorito ──
    fav_is_home = ph >= pa
    dc_v  = mc.get("dc_ph",  ph*100)/100 if fav_is_home else max(0.01, 1 - mc.get("dc_ph",ph*100)/100  - 0.26)
    bvp_v = mc.get("bvp_ph", ph*100)/100 if fav_is_home else max(0.01, 1 - mc.get("bvp_ph",ph*100)/100 - 0.26)
    elo_v = mc.get("elo_ph", ph*100)/100 if fav_is_home else max(0.01, 1 - mc.get("elo_ph",ph*100)/100 - 0.26)
    h2h_v = mc.get("h2h_ph", ph*100)/100 if fav_is_home else max(0.01, 1 - mc.get("h2h_ph",ph*100)/100 - 0.26)
    modelos = [dc_v, bvp_v, elo_v, h2h_v]

    # ── Métricas clave ──
    std         = statistics.stdev(modelos) if len(modelos) >= 2 else 0.10
    pct_acuerdo = sum(1 for m in modelos if m >= 0.50) / 4
    ev          = mkt_prob - (1/mkt_odd) if mkt_odd > 1 else 0
    xg_fav      = mc.get("hxg", 1.2) if fav_is_home else mc.get("axg", 1.0)
    ensemble_ph = ph  # promedio ponderado final

    # ── SISTEMA DE PUNTUACIÓN (máx ~11 pts) ──
    score = 0
    factores = []  # (texto, color)

    # 1. CONSENSO entre modelos
    if pct_acuerdo == 1.0:
        score += 3
        factores.append((f"✅ Los 4 modelos coinciden en el mismo favorito ({fav_name[:14]})", "#00ff88"))
    elif pct_acuerdo >= 0.75:
        score += 2
        factores.append(("✅ 3 de 4 modelos apuntan al mismo resultado", "#00ff88"))
    elif pct_acuerdo >= 0.50:
        score += 1
        factores.append(("⚠️ Solo 2 modelos alineados — señal mixta", "#FFD700"))
    else:
        score -= 2
        factores.append(("🚫 Modelos divididos — no hay consenso estadístico", "#ff4444"))

    # 2. DISPERSIÓN entre modelos
    if std < 0.04:
        score += 2
        factores.append((f"✅ Modelos muy coherentes entre sí (σ={std*100:.1f}%) — señal robusta", "#00ff88"))
    elif std < 0.08:
        score += 1
        factores.append((f"⚠️ Ligera divergencia entre modelos (σ={std*100:.1f}%)", "#FFD700"))
    else:
        score -= 1
        factores.append((f"🚫 Alta dispersión entre modelos (σ={std*100:.1f}%) — incertidumbre", "#ff4444"))

    # 3. VALOR ESPERADO (EV)
    if ev > 0.08:
        score += 3
        factores.append((f"✅ Edge sólido vs cuota: +{ev*100:.1f}% — valor real de apuesta", "#00ff88"))
    elif ev > 0.03:
        score += 2
        factores.append((f"✅ Edge positivo: +{ev*100:.1f}% sobre el momio de mercado", "#00ff88"))
    elif ev > 0:
        score += 1
        factores.append((f"⚠️ Edge marginal: +{ev*100:.1f}% — cuota casi en el límite", "#FFD700"))
    elif mkt_odd == 0:
        factores.append(("⚠️ Sin cuota disponible — no se puede calcular valor de apuesta", "#FFD700"))
    else:
        score -= 2
        factores.append((f"🚫 Sin valor en cuota: EV={ev*100:.1f}% — el mercado ya descontó esta prob.", "#ff4444"))

    # 4. PROBABILIDAD DEL MERCADO
    if mkt_prob > 0.70:
        score += 2
        factores.append((f"✅ Probabilidad alta: {mkt_prob*100:.0f}% según modelos estadísticos", "#00ff88"))
    elif mkt_prob > 0.60:
        score += 1
        factores.append((f"✅ Probabilidad favorable: {mkt_prob*100:.0f}% — ventaja clara", "#00ff88"))
    elif mkt_prob > 0.52:
        factores.append((f"⚠️ Probabilidad ajustada: {mkt_prob*100:.0f}% — ventaja estrecha", "#FFD700"))
    else:
        score -= 1
        factores.append((f"🚫 Sin favorito claro: {mkt_prob*100:.0f}% vs {(1-mkt_prob)*100:.0f}% — partido parejo", "#ff4444"))

    # 5. xG ofensivo
    if not is_totals:
        if xg_fav > 1.8:
            score += 1
            factores.append((f"✅ xG ofensivo alto: {xg_fav:.2f} goles esperados — ataque en forma", "#00ff88"))
        elif xg_fav < 0.80:
            score -= 1
            factores.append((f"🚫 xG bajo: {xg_fav:.2f} — ataque poco efectivo últimamente", "#ff4444"))
    else:
        o25 = mc.get("o25", 0.5); btts = mc.get("btts", 0.5)
        hxg = mc.get("hxg", 1.2); axg = mc.get("axg", 1.0)
        total_xg = hxg + axg
        if total_xg > 2.6:
            score += 1
            factores.append((f"✅ xG total partido: {total_xg:.2f} — juego abierto, goles esperados", "#00ff88"))
        elif total_xg < 1.8:
            score -= 1
            factores.append((f"🚫 xG total bajo ({total_xg:.2f}) — partido cerrado, pocos goles", "#ff4444"))

    # ── VEREDICTO FINAL ──
    MAX_SCORE = 11
    score_pct = max(0, min(score, MAX_SCORE))

    if score >= 7:
        nivel      = "APOSTAR"
        emoji_big  = "🟢"
        color_bg   = "linear-gradient(135deg,#001a00,#002800)"
        color_brd  = "#00ff88"
        color_txt  = "#00ff88"
        desc       = "Señal estadística fuerte. Los modelos convergen, existe valor real en la cuota y la probabilidad justifica la apuesta."
        kelly_rec  = "Kelly completo — 1 a 3% del banco"
        kelly_col  = "#00ff88"
    elif score >= 4:
        nivel      = "BANK MEDIO"
        emoji_big  = "🟡"
        color_bg   = "linear-gradient(135deg,#1a1200,#2a1e00)"
        color_brd  = "#FFD700"
        color_txt  = "#FFD700"
        desc       = "Señal moderada. Hay elementos estadísticos a favor pero también incertidumbre. Apuesta pequeña o espera mejores condiciones de cuota."
        kelly_rec  = "Mitad de Kelly — 0.5 a 1.5% del banco"
        kelly_col  = "#FFD700"
    else:
        nivel      = "NO APOSTAR"
        emoji_big  = "🔴"
        color_bg   = "linear-gradient(135deg,#1a0000,#2a0000)"
        color_brd  = "#ff4444"
        color_txt  = "#ff4444"
        desc       = "Los modelos no convergen o la cuota no ofrece ventaja matemática. Apostar aquí sería jugar sin ventaja estadística."
        kelly_rec  = "Abstenerse — 0% del banco"
        kelly_col  = "#ff4444"

    # ── Barra de score visual ──
    bar_pct   = int(score_pct / MAX_SCORE * 100)
    bar_color = "#00ff88" if score >= 7 else ("#FFD700" if score >= 4 else "#ff4444")

    # ── Tabla de modelos ──
    model_rows = ""
    model_data = [
        ("Dixon-Coles",    dc_v,  "#00ccff", "45%", "Ajuste correlación goles (Coles & Jones 1996)"),
        ("Poisson BV",     bvp_v, "#aa00ff", "30%", "Distribución conjunta de marcadores"),
        ("Elo Dinámico",   elo_v, "#00ff88", "15%", "Rating adaptado fútbol (Hvattum & Arntzen 2010)"),
        ("H2H Histórico",  h2h_v, "#FFD700", "10%", "Resultados directos ponderados por recencia"),
    ]
    for mname, mval, mcol, peso, ref in model_data:
        bar_w   = int(mval * 100)
        mcolor  = "#00ff88" if mval >= 0.60 else ("#FFD700" if mval >= 0.50 else "#ff4444")
        arrow   = "▲" if mval >= 0.50 else "▼"
        model_rows += (
            f"<tr style='border-bottom:1px solid #0d0d2e'>"
            f"<td style='padding:7px 10px'>"
            f"  <span style='color:{mcol};font-weight:700;font-size:.78rem'>{mname}</span>"
            f"  <span style='color:#333;font-size:.65rem;margin-left:4px'>({peso})</span>"
            f"</td>"
            f"<td style='padding:7px 10px;text-align:center'>"
            f"  <span style='color:{mcolor};font-weight:900;font-size:.95rem'>{mval*100:.1f}%</span>"
            f"  <span style='color:{mcolor};font-size:.68rem'> {arrow}</span>"
            f"</td>"
            f"<td style='padding:7px 10px'>"
            f"  <div style='height:4px;background:#0d0d2e;border-radius:4px;overflow:hidden'>"
            f"    <div style='width:{bar_w}%;height:100%;background:{mcolor};border-radius:4px'></div>"
            f"  </div>"
            f"</td>"
            f"<td style='padding:7px 10px;color:#333;font-size:.65rem'>{ref}</td>"
            f"</tr>"
        )

    # ── Factores detectados ──
    factores_html = "".join(
        f"<div style='color:{col};font-size:.78rem;padding:3px 0;line-height:1.4'>{txt}</div>"
        for txt, col in factores
    )

    prom_modelos = sum(modelos) / len(modelos)

    html = f"""
<div style='background:{color_bg};border:2px solid {color_brd};border-radius:16px;padding:20px 18px;margin:20px 0'>

  <!-- SEMÁFORO GRANDE -->
  <div style='display:flex;align-items:center;gap:14px;margin-bottom:16px'>
    <div style='font-size:3rem;line-height:1'>{emoji_big}</div>
    <div style='flex:1'>
      <div style='font-size:.68rem;color:#444;letter-spacing:.14em;font-weight:700;margin-bottom:2px'>
        VEREDICTO ACADÉMICO — ENSEMBLE DE 4 MODELOS
      </div>
      <div style='font-size:2rem;font-weight:900;color:{color_txt};line-height:1.1'>{nivel}</div>
      <div style='font-size:.75rem;color:#666;margin-top:2px'>{mkt_lbl}</div>
    </div>
    <div style='text-align:right;flex-shrink:0'>
      <div style='font-size:.62rem;color:#444;margin-bottom:2px'>SCORE ESTADÍSTICO</div>
      <div style='font-size:1.4rem;font-weight:900;color:{color_txt}'>{score_pct}<span style='font-size:.85rem;color:#444'>/{MAX_SCORE}</span></div>
    </div>
  </div>

  <!-- BARRA PROGRESO -->
  <div style='background:#0d0d2e;border-radius:8px;height:8px;margin-bottom:14px;overflow:hidden'>
    <div style='width:{bar_pct}%;height:100%;background:{bar_color};border-radius:8px;
                transition:width .5s ease'></div>
  </div>

  <!-- DESCRIPCIÓN -->
  <div style='font-size:.82rem;color:#aaa;background:#07071a;border-radius:8px;padding:10px 14px;
              border-left:4px solid {color_brd};margin-bottom:16px;line-height:1.65'>
    {desc}
  </div>

  <!-- TABLA MODELOS -->
  <div style='font-size:.65rem;color:#444;font-weight:700;letter-spacing:.1em;margin-bottom:6px'>
    📐 ANÁLISIS POR MODELO — PROB. FAVORITO: {prom_modelos*100:.1f}% PROMEDIO
  </div>
  <div style='background:#07071a;border-radius:10px;overflow:hidden;margin-bottom:14px'>
    <table style='width:100%;border-collapse:collapse'>
      <thead>
        <tr style='border-bottom:1px solid #151530'>
          <th style='padding:6px 10px;text-align:left;color:#333;font-size:.65rem;font-weight:700'>Modelo</th>
          <th style='padding:6px 10px;text-align:center;color:#333;font-size:.65rem;font-weight:700'>Prob.</th>
          <th style='padding:6px 10px;color:#333;font-size:.65rem;font-weight:700'>Intensidad</th>
          <th style='padding:6px 10px;text-align:left;color:#333;font-size:.65rem;font-weight:700'>Fuente</th>
        </tr>
      </thead>
      <tbody>{model_rows}</tbody>
    </table>
  </div>

  <!-- FACTORES -->
  <div style='font-size:.65rem;color:#444;font-weight:700;letter-spacing:.1em;margin-bottom:8px'>
    🔍 FACTORES QUE DETERMINARON EL VEREDICTO
  </div>
  <div style='background:#07071a;border-radius:8px;padding:10px 14px;margin-bottom:14px'>
    {factores_html}
  </div>

  <!-- KELLY / BANKROLL -->
  <div style='display:flex;justify-content:space-between;align-items:center;
              padding-top:12px;border-top:1px solid #151530'>
    <div>
      <div style='font-size:.65rem;color:#444;font-weight:700;letter-spacing:.1em'>💰 GESTIÓN DE BANKROLL</div>
      <div style='font-size:.82rem;font-weight:700;color:{kelly_col};margin-top:2px'>{kelly_rec}</div>
    </div>
    <div style='text-align:right'>
      <div style='font-size:.65rem;color:#444;font-weight:700;letter-spacing:.1em'>EV vs CUOTA</div>
      <div style='font-size:.88rem;font-weight:700;color:{"#00ff88" if ev>0 else "#ff4444"};margin-top:2px'>
        {"+" if ev>0 else ""}{ev*100:.1f}% {"✅" if ev>0 else "🚫"}
      </div>
    </div>
  </div>
</div>"""
    return html


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

def _best_market_soccer(m, dp, mc):
    """
    Evalúa todos los mercados válidos y devuelve el de MAYOR probabilidad.
    Mercados: 1X2, Doble Chance, Over 2.5, Over 3.5, Ambos Anotan.
    NO incluye O1.5, ML simple sin cuota, Handicap.
    """
    opts = []
    # 1X2
    if m.get("odd_h",0)>1: opts.append(("🏠 "+m["home"][:15]+" gana",    dp["ph"], m["odd_h"], dp["ph"]-(1/m["odd_h"])))
    if m.get("odd_d",0)>1: opts.append(("🤝 Empate",                      dp["pd"], m["odd_d"], dp["pd"]-(1/m["odd_d"])))
    if m.get("odd_a",0)>1: opts.append(("✈️ "+m["away"][:15]+" gana",      dp["pa"], m["odd_a"], dp["pa"]-(1/m["odd_a"])))
    # Doble Chance
    dc_1x = dp["ph"]+dp["pd"]; dc_x2 = dp["pd"]+dp["pa"]; dc_12 = dp["ph"]+dp["pa"]
    opts.append(("🔵 DC: "+m["home"][:12]+" o Emp",    dc_1x, 0, dc_1x-0.65))
    opts.append(("🟣 DC: "+m["away"][:12]+" o Emp",    dc_x2, 0, dc_x2-0.65))
    opts.append(("🔴 DC: "+m["home"][:10]+" o "+m["away"][:10], dc_12, 0, dc_12-0.65))
    # Over / BTTS
    opts.append(("⚽ Over 2.5",             mc["o25"],  0, mc["o25"]-0.52))
    opts.append(("⚽ Over 3.5",             mc["o35"],  0, mc["o35"]-0.45))
    opts.append(("⚡ Ambos Anotan (AA)",    mc["btts"], 0, mc["btts"]-0.52))
    # Ordenar: mayor probabilidad primero (el pick DIAMANTE = max prob con edge+)
    opts.sort(key=lambda x: (-x[1], -x[3]))
    valid = [o for o in opts if o[3] > 0.0 and o[1] >= 0.55]
    return valid[0] if valid else None

def escanear_y_enviar(matches):
    """Escanea todos los partidos y manda picks a Telegram.
    El pick de cada partido es el mercado de MAYOR probabilidad con edge positivo."""
    picks = []
    for m in matches:
        if m["state"] != "pre": continue
        hf  = get_form(m["home_id"], m["slug"])
        af  = get_form(m["away_id"], m["slug"])
        hxg = max(0.35, avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
        axg = max(0.35, avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
        h2h = get_h2h(m["home_id"],m["away_id"],m["slug"],m["home"],m["away"])
        h2s = h2h_stats(h2h, m["home"], m["away"])
        mc  = ensemble_football(hxg, axg, h2s, hf, af, m["home_id"], m["away_id"])
        dp  = diamond_engine(mc, h2s, hf, af)
        best = _best_market_soccer(m, dp, mc)
        if best and best[3] >= 0.05:  # edge mínimo 5%
            p = best[1]; b = (best[2]-1) if best[2]>1 else 1
            kelly = max(0, (b*p-(1-p))/b*100) if b>0 else 0
            picks.append({**m,"dp":dp,"mc":mc,"edge":best[3],"kelly":kelly,
                          "pick_label":best[0],"pick_prob":best[1],"pick_odd":best[2]})

    if not picks:
        tg_send("🛡️ *Escáner Diario:* No hay picks con Edge > 8% hoy. Mantén el dinero en la bolsa.")
        return 0

    msg  = "🦅 *THE GAMBLERS LAYER | ESCÁNER DIARIO* 🦅\n"
    msg += f"_{datetime.now(CDMX).strftime('%d/%m/%Y')} — {len(picks)} picks_\n\n"
    for p in sorted(picks, key=lambda x:-x["pick_prob"]):
        msg += f"🚨 *PICK DIAMANTE:* {p['league']}\n"
        msg += f"⚽ {p['home']} vs {p['away']}\n"
        msg += f"👉 *{p.get('pick_label','?')}* — {p['pick_prob']*100:.1f}%"
        if p.get('pick_odd',0)>1: msg += f" @{p['pick_odd']:.2f}"
        msg += f" | Edge: {p['edge']*100:.1f}%\n"
        msg += f"🕒 {p['hora']} CDMX\n"
        msg += f"👉 *Local gana @{p['odd_h']}*\n"
        msg += f"📊 Prob: {p['dp']['ph']*100:.1f}%  •  Edge: *{p['edge']*100:.1f}%*\n"
        # Sharp signal from Ensemble consensus
        consensus = p["mc"].get("consensus","N/D")
        msg += f"🔬 Consenso modelos: {consensus}\n"
        msg += f"💰 Kelly: {p['kelly']:.1f}% bankroll\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "\n_Que la varianza esté a nuestro favor._ 🎲"
    tg_send(msg)
    return len(picks)

def get_nba_public_pct(home, away):
    """Action Network NBA — % público vs sharp en ML y O/U."""
    data = get_action_network_nba(home, away)
    if not data: return {}
    return data


def render_action_network_nba(home, away, ou_line=0):
    """
    Renderiza datos Action Network PRO para NBA:
    % bets vs % money en ML, O/U, spread + línea apertura/cierre + lesiones.
    """
    data = get_action_network_nba(home, away)
    
    src_color = "#aa00ff" if data.get("source","") == "ActionNetwork PRO" else "#555"
    src_label = data.get("source", "ActionNetwork")
    
    st.markdown(
        f"<div class='shdr'>📊 ACTION NETWORK — % PÚBLICO & DINERO</div>",
        unsafe_allow_html=True)
    
    if not data:
        st.markdown(
            "<div style='background:#0d0d2e;border:1px solid #252555;border-radius:12px;"
            "padding:14px 18px;color:#555;font-size:.85rem'>"
            "📡 Conectando con Action Network... "
            "Agrega <b style='color:#EEEEFF'>ACTION_NETWORK_TOKEN</b> en Streamlit secrets para datos PRO."
            "</div>", unsafe_allow_html=True)
        return
    
    ml_h_b  = data.get("ml_home_bets_pct", 0)
    ml_h_m  = data.get("ml_home_money_pct", 0)
    ml_a_b  = data.get("ml_away_bets_pct", 0) or (100-ml_h_b if ml_h_b else 0)
    ml_a_m  = data.get("ml_away_money_pct", 0) or (100-ml_h_m if ml_h_m else 0)
    ov_b    = data.get("over_bets_pct", 0)
    ov_m    = data.get("over_money_pct", 0)
    un_b    = data.get("under_bets_pct", 0) or (100-ov_b if ov_b else 0)
    un_m    = data.get("under_money_pct", 0) or (100-ov_m if ov_m else 0)
    
    def pct_bar(val, color):
        return (f"<div style='background:#1a1a40;border-radius:4px;height:6px;margin-top:4px'>"
                f"<div style='width:{min(val,100):.0f}%;height:6px;background:{color};border-radius:4px'></div></div>")
    
    def side_color(pct):
        return "#00ff88" if pct >= 60 else ("#ff4444" if pct <= 40 else "#FFD700")
    
    # ── ML ──
    if ml_h_b or ml_h_m:
        st.markdown(
            f"<div style='background:#0d0d2e;border:1px solid #252555;border-radius:14px;"
            f"padding:14px 18px;margin:6px 0'>"
            f"<div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.1em;margin-bottom:10px'>"
            f"🏆 MONEY LINE — {src_label}</div>"
            f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px'>"
            # Local
            f"<div style='background:#07071a;border-radius:10px;padding:10px'>"
            f"<div style='font-size:.72rem;color:#aaa;margin-bottom:6px'>🏠 {home[:14]}</div>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Apuestas</span>"
            f"<span style='font-weight:700;color:{side_color(ml_h_b)}'>{ml_h_b:.0f}%</span></div>"
            f"{pct_bar(ml_h_b, side_color(ml_h_b))}"
            f"<div style='display:flex;justify-content:space-between;margin-top:8px;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Dinero</span>"
            f"<span style='font-weight:700;color:{side_color(ml_h_m)}'>{ml_h_m:.0f}%</span></div>"
            f"{pct_bar(ml_h_m, side_color(ml_h_m))}</div>"
            # Visitante
            f"<div style='background:#07071a;border-radius:10px;padding:10px'>"
            f"<div style='font-size:.72rem;color:#aaa;margin-bottom:6px'>✈️ {away[:14]}</div>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Apuestas</span>"
            f"<span style='font-weight:700;color:{side_color(ml_a_b)}'>{ml_a_b:.0f}%</span></div>"
            f"{pct_bar(ml_a_b, side_color(ml_a_b))}"
            f"<div style='display:flex;justify-content:space-between;margin-top:8px;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Dinero</span>"
            f"<span style='font-weight:700;color:{side_color(ml_a_m)}'>{ml_a_m:.0f}%</span></div>"
            f"{pct_bar(ml_a_m, side_color(ml_a_m))}</div>"
            f"</div>"
            # Sharp signal
            + (f"<div style='margin-top:10px;font-size:.75rem;padding:6px 10px;"
               f"background:#12123a;border-radius:6px;color:#FFD700'>"
               f"⚡ <b>Sharp money en {home[:12] if ml_h_m > ml_h_b + 10 else away[:12]}:</b> "
               f"{'Local' if ml_h_m > ml_h_b + 10 else 'Visitante'} tiene más dinero que apuestas — señal sharp</div>"
               if abs(ml_h_m - ml_h_b) > 10 else "")
            + f"</div>", unsafe_allow_html=True)
    
    # ── O/U ──
    if ov_b or ov_m:
        ov_color  = side_color(ov_b)
        un_color  = side_color(un_b)
        st.markdown(
            f"<div style='background:#0d0d2e;border:1px solid #252555;border-radius:14px;"
            f"padding:14px 18px;margin:6px 0'>"
            f"<div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.1em;margin-bottom:10px'>"
            f"📊 OVER / UNDER {ou_line if ou_line else ''}</div>"
            f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px'>"
            f"<div style='background:#07071a;border-radius:10px;padding:10px'>"
            f"<div style='font-size:.8rem;color:#ff4444;font-weight:700;margin-bottom:6px'>🔥 OVER</div>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Apuestas</span>"
            f"<span style='font-weight:700;color:{ov_color}'>{ov_b:.0f}%</span></div>"
            f"{pct_bar(ov_b, ov_color)}"
            f"<div style='display:flex;justify-content:space-between;margin-top:8px;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Dinero</span>"
            f"<span style='font-weight:700;color:{side_color(ov_m)}'>{ov_m:.0f}%</span></div>"
            f"{pct_bar(ov_m, side_color(ov_m))}</div>"
            f"<div style='background:#07071a;border-radius:10px;padding:10px'>"
            f"<div style='font-size:.8rem;color:#00ccff;font-weight:700;margin-bottom:6px'>❄️ UNDER</div>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Apuestas</span>"
            f"<span style='font-weight:700;color:{un_color}'>{un_b:.0f}%</span></div>"
            f"{pct_bar(un_b, un_color)}"
            f"<div style='display:flex;justify-content:space-between;margin-top:8px;margin-bottom:4px'>"
            f"<span style='font-size:.7rem;color:#555'>% Dinero</span>"
            f"<span style='font-weight:700;color:{side_color(un_m)}'>{un_m:.0f}%</span></div>"
            f"{pct_bar(un_m, side_color(un_m))}</div>"
            f"</div>"
            # Fade signal
            + (f"<div style='margin-top:10px;font-size:.75rem;padding:6px 10px;"
               f"background:#12123a;border-radius:6px;color:#ff9500'>"
               f"👥 <b>Público muy cargado en {'Over' if ov_b>70 else 'Under'}:</b> "
               f"Considera fade the public</div>"
               if ov_b > 70 or ov_b < 30 else "")
            + f"</div>", unsafe_allow_html=True)
    
    # ── Línea apertura vs cierre ──
    open_t = data.get("open_total", 0)
    curr_t = data.get("curr_total", 0)
    open_ml = data.get("open_ml_h", 0)
    curr_ml = data.get("curr_ml_h", 0)
    
    if open_t and curr_t and open_t != curr_t:
        move = curr_t - open_t
        mc2 = "#00ff88" if move > 0 else "#ff4444"
        st.markdown(
            f"<div style='background:#0d0d2e;border:1px solid #252555;border-radius:10px;"
            f"padding:10px 16px;margin:6px 0;display:flex;justify-content:space-between;align-items:center'>"
            f"<div><div style='font-size:.7rem;color:#555;font-weight:700'>📈 MOVIMIENTO DE LÍNEA TOTAL</div>"
            f"<div style='font-size:.78rem;color:#aaa;margin-top:2px'>Apertura → Actual</div></div>"
            f"<div style='text-align:right'>"
            f"<div style='font-size:.85rem;color:#aaa'>{open_t} → <b style='color:{mc2}'>{curr_t}</b></div>"
            f"<div style='font-size:.72rem;color:{mc2}'>{'▲' if move>0 else '▼'} {abs(move):.1f} pts</div>"
            f"</div></div>", unsafe_allow_html=True)
    
    # ── Steam / Reverse ──
    if data.get("steam_move"):
        st.markdown(
            "<div style='background:#2a0050;border:1px solid #aa00ff55;border-radius:10px;"
            "padding:10px 16px;margin:6px 0;font-size:.83rem;color:#aa00ff'>"
            "💨 <b>STEAM MOVE detectado por Action Network</b> — dinero coordinado entrando.</div>",
            unsafe_allow_html=True)
    if data.get("reverse_move"):
        st.markdown(
            "<div style='background:#002a00;border:1px solid #00ff8855;border-radius:10px;"
            "padding:10px 16px;margin:6px 0;font-size:.83rem;color:#00ff88'>"
            "🔄 <b>REVERSE LINE MOVEMENT</b> — dinero contrario a la opinión pública. Señal sharp.</div>",
            unsafe_allow_html=True)
    
    # ── Lesiones ──
    injuries = data.get("injuries", [])
    if injuries:
        inj_html = " · ".join(f"<b style='color:#ff4444'>{i}</b>" for i in injuries if i.strip())
        if inj_html:
            st.markdown(
                f"<div style='background:#1a0a00;border:1px solid #ff440033;border-radius:10px;"
                f"padding:10px 16px;margin:6px 0;font-size:.78rem;color:#ff9500'>"
                f"🏥 <b>Lesiones:</b> {inj_html}</div>", unsafe_allow_html=True)

def escanear_nba_y_enviar(games):
    """Escanea NBA y manda picks O/U con edge > 4% a Telegram."""
    picks = []
    for g in games:
        if g["state"] != "pre": continue
        res = nba_ou_model(g["home_id"], g["away_id"], g["ou_line"])
        best_p  = max(res["p_over"], res["p_under"])
        is_over = res["p_over"] > res["p_under"]
        edge    = best_p - 0.5
        if edge >= 0.04:
            picks.append({**g, "res": res, "best_p": best_p,
                          "pick": f"{'Over' if is_over else 'Under'} {res['line']}",
                          "edge": edge})
    if not picks:
        tg_send("🏀 *NBA Scanner:* Sin picks O/U con valor hoy.")
        return 0
    msg  = "🏀 *THE GAMBLERS LAYER | NBA PICKS* 🏀\n"
    msg += f"_{datetime.now(CDMX).strftime('%d/%m/%Y')} — {len(picks)} picks_\n\n"
    for p in sorted(picks, key=lambda x: -x["edge"]):
        msg += f"🚨 {p['away']} @ {p['home']}\n"
        msg += f"🕒 {p['hora']} CDMX\n"
        msg += f"👉 *{p['pick']}* | Proy: {p['res']['proj']} pts\n"
        msg += f"📊 Prob: {p['best_p']*100:.1f}%  •  Edge: *{p['edge']*100:.1f}%*\n"
        _an = get_action_network_nba(p["home"], p["away"])
        if _an.get("over_bets_pct"): msg += f"📊 AN: Over {_an['over_bets_pct']:.0f}% bets · {_an['over_money_pct']:.0f}% money\n"
        if _an.get("steam_move"): msg += "💨 STEAM MOVE detectado\n"
        if _an.get("reverse_move"): msg += "🔄 REVERSE LINE MOVEMENT\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "\n_Que la varianza esté a nuestro favor._ 🎲"
    tg_send(msg)
    return len(picks)

def escanear_tenis_y_enviar(matches):
    """Escanea ATP/WTA y manda ML picks con prob >= 62% a Telegram."""
    picks = []
    for m in matches:
        if m["state"] != "pre": continue
        tm   = tennis_model(m["rank1"], m["rank2"], m["odd_1"], m["odd_2"])
        best_p = max(tm["p1"], tm["p2"])
        fav    = m["p1"] if tm["p1"] >= tm["p2"] else m["p2"]
        odd    = m["odd_1"] if tm["p1"] >= tm["p2"] else m["odd_2"]
        if best_p >= 0.62:
            picks.append({**m, "tm": tm, "fav": fav, "best_p": best_p, "odd": odd})
    if not picks:
        tg_send("🎾 *Tennis Scanner:* Sin picks ML con valor hoy.")
        return 0
    msg  = "🎾 *THE GAMBLERS LAYER | TENNIS PICKS* 🎾\n"
    msg += f"_{datetime.now(CDMX).strftime('%d/%m/%Y')} — {len(picks)} picks_\n\n"
    for p in sorted(picks, key=lambda x: -x["best_p"]):
        odd_txt = f"@{p['odd']:.2f}" if p["odd"] > 1 else "N/D"
        msg += f"🚨 {p['tour']} — {p['torneo']}\n"
        msg += f"🎾 {p['p1']} vs {p['p2']}\n"
        msg += f"🕒 {p['hora']} CDMX\n"
        msg += f"👉 *{p['fav']} gana* {odd_txt}\n"
        msg += f"📊 Prob: {p['best_p']*100:.1f}%  •  {p['tm']['conf']}\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "\n_Que la varianza esté a nuestro favor._ 🎲"
    tg_send(msg)
    return len(picks)

def render_bot_tab(sport_label, scan_fn, scan_args, preview_fn=None):
    """Renderiza el tab de Bot de Telegram reutilizable para cualquier deporte."""
    bot_ok = bool(BOT_TOKEN and CHAT_ID and BOT_TOKEN != "Pega_Aqui_Tu_Token_De_BotFather")
    icon = {"⚽ Fútbol":"⚽","🏀 NBA":"🏀","🎾 Tenis":"🎾"}.get(sport_label,"🤖")
    st.markdown(
        f"<div class='bot-card'>"
        f"<div style='font-size:.8rem;color:#229ED9;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>🤖 BOT TELEGRAM — {sport_label.upper()}</div>"
        f"<div style='font-size:1.1rem;font-weight:700;margin-bottom:6px'>The Gamblers Layer Bot</div>"
        f"<div style='color:#555;font-size:.85rem'>Estado: {'✅ Configurado' if bot_ok else '⚠️ Sin configurar — agrega BOT_TOKEN y CHAT_ID en Streamlit secrets'}</div>"
        f"</div>", unsafe_allow_html=True)
    if bot_ok:
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"📡 Escanear {sport_label} y Enviar", key=f"scan_{sport_label}", use_container_width=True):
                with st.spinner("Escaneando y enviando..."):
                    n = scan_fn(*scan_args)
                st.success(f"✅ Enviado. {n} picks encontrados.")
        with c2:
            if st.button("🧪 Test — Mensaje de Prueba", key=f"test_{sport_label}", use_container_width=True):
                ok = tg_send(f"{icon} *The Gamblers Layer* — Test {sport_label} exitoso ✅")
                st.success("✅ Mensaje enviado.") if ok else st.error("❌ Error. Verifica token y chat_id.")
        st.markdown("<div class='shdr'>Envío Automático</div>", unsafe_allow_html=True)
        st.info("El bot corre automáticamente todos los días a las 13:00 UTC. Usa el botón de arriba para un escaneo manual.")
        if preview_fn:
            st.markdown("<div class='shdr'>Preview de picks</div>", unsafe_allow_html=True)
            preview_fn()
    else:
        st.markdown("""
        <div style='background:#0d0d2e;border-radius:12px;padding:20px;margin-top:10px;color:#666'>
        <b>Cómo configurar el bot:</b><br><br>
        1. Ve a Streamlit Cloud → Settings → Secrets<br>
        2. Agrega <code>BOT_TOKEN = "tu_token"</code><br>
        3. Agrega <code>CHAT_ID = "tu_chat_id"</code><br>
        4. Guarda y reinicia la app
        </div>""", unsafe_allow_html=True)

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
# NBA DATA
# ══════════════════════════════════════════════════════════
@st.cache_data(ttl=300, show_spinner=False)
def get_nba_cartelera():
    now = datetime.now(CDMX)
    dates = [(now+timedelta(days=i)).strftime("%Y%m%d") for i in range(0,5)]
    hoy = now.strftime("%Y-%m-%d")
    games, seen = [], set()
    for ds in dates:
        data = eg(f"{NBA_ESPN}/scoreboard", {"dates": ds, "limit": 50})
        for ev in data.get("events",[]):
            eid = ev.get("id","")
            if eid in seen: continue
            seen.add(eid)
            try:
                comp  = ev["competitions"][0]
                comps = comp["competitors"]
                hc = next(c for c in comps if c["homeAway"]=="home")
                ac = next(c for c in comps if c["homeAway"]=="away")
                utc   = datetime.strptime(ev["date"],"%Y-%m-%dT%H:%MZ").replace(tzinfo=pytz.UTC)
                hora  = utc.astimezone(CDMX).strftime("%H:%M")
                fecha = utc.astimezone(CDMX).strftime("%Y-%m-%d")
                state = ev["status"]["type"]["state"]
                if fecha < hoy: continue
                if fecha > (now+timedelta(days=4)).strftime("%Y-%m-%d"): continue
                ou_line = 0.0
                try:
                    odds = comp.get("odds",[])
                    if odds: ou_line = float(odds[0].get("overUnder",0) or 0)
                except: pass
                games.append({
                    "id":eid,"home":hc["team"]["displayName"],
                    "away":ac["team"]["displayName"],
                    "home_id":str(hc["team"]["id"]),"away_id":str(ac["team"]["id"]),
                    "hora":hora,"fecha":fecha,"state":state,"ou_line":ou_line,
                    "score_h":parse_score(hc.get("score",0)),
                    "score_a":parse_score(ac.get("score",0)),
                })
            except: continue
    return games

@st.cache_data(ttl=3600, show_spinner=False)
def get_nba_team_avg(team_id):
    data = eg(f"{NBA_ESPN}/teams/{team_id}/statistics")
    try:
        for cat in data.get("results",{}).get("stats",{}).get("categories",[]):
            for s in cat.get("stats",[]):
                if s.get("name")=="pointsPerGame": return float(s.get("value",110))
    except: pass
    return 110.0

def nba_ou_model(home_id, away_id, ou_line):
    h_ppg = get_nba_team_avg(home_id)
    a_ppg = get_nba_team_avg(away_id)
    proj  = h_ppg*1.02 + a_ppg
    line  = ou_line if ou_line > 0 else proj
    rng   = np.random.default_rng(42)
    tots  = rng.normal(h_ppg*1.02,12,50_000) + rng.normal(a_ppg,12,50_000)
    p_over = float((tots>line).mean())
    return {"proj":round(proj,1),"line":round(line,1),
            "p_over":p_over,"p_under":1-p_over,
            "rec":"OVER 🔥" if p_over>0.54 else("UNDER ❄️" if p_over<0.46 else "NEUTRAL ⚖️")}

# ══════════════════════════════════════════════════════════
# TENIS DATA
# ══════════════════════════════════════════════════════════
TENNIS_API = "https://api.api-tennis.com/tennis/"

@st.cache_data(ttl=300, show_spinner=False)
def get_tennis_cartelera():
    now  = datetime.now(CDMX)
    hoy  = now.strftime("%Y-%m-%d")
    fin  = (now + timedelta(days=4)).strftime("%Y-%m-%d")
    matches = []
    try:
        r = requests.get(TENNIS_API, params={
            "method":     "get_fixtures",
            "APIkey":     TENNIS_API_KEY,
            "date_start": hoy,
            "date_stop":  fin,
        }, headers=H, timeout=12)
        data = r.json() if r.status_code == 200 else {}
        for ev in data.get("result", []):
            try:
                fecha = ev.get("event_date","")
                hora  = ev.get("event_time","00:00")
                # Convertir hora a CDMX (API devuelve UTC)
                try:
                    utc_t = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M").replace(tzinfo=pytz.UTC)
                    hora  = utc_t.astimezone(CDMX).strftime("%H:%M")
                    fecha = utc_t.astimezone(CDMX).strftime("%Y-%m-%d")
                except: pass
                if fecha < hoy or fecha > fin: continue
                tour_type = ev.get("event_type_type","").upper()
                if "ATP" in tour_type or "WTA" in tour_type or "GRAND SLAM" in tour_type or "MASTERS" in tour_type:
                    tour = "WTA" if "WTA" in tour_type else "ATP"
                else:
                    continue  # filtrar ITF y challengers
                ev_status = str(ev.get("event_status","")).lower()
                ev_finished = str(ev.get("event_final","0"))
                is_live = ev.get("event_live","0") == "1"
                is_post = (ev_finished == "1" or
                           any(x in ev_status for x in ["finished","ft","final","completed","awarded"]))
                t_state = "post" if is_post else ("in" if is_live else "pre")
                # Score for tennis
                sc1 = str(ev.get("event_first_player_result",""))
                sc2 = str(ev.get("event_second_player_result",""))
                matches.append({
                    "id":    str(ev.get("event_key","")),
                    "p1":    ev.get("event_first_player","?"),
                    "p2":    ev.get("event_second_player","?"),
                    "rank1": 999, "rank2": 999,
                    "tour":  tour,
                    "torneo": ev.get("tournament_name",""),
                    "hora":  hora,
                    "fecha": fecha,
                    "state": t_state,
                    "score_p1": sc1, "score_p2": sc2,
                    "odd_1": 0.0, "odd_2": 0.0,
                })
            except: continue
    except Exception as e:
        pass
    return matches

def tennis_model(rank1, rank2, odd_1=0, odd_2=0, surface="hard"):
    """Weibull+Markov (Klaassen&Magnus 2001) — mejor que Elo puro para tenis."""
    try:
        wm = weibull_match_prob(rank1, rank2, odd_1, odd_2, surface)
        p1, p2 = wm["p1"], wm["p2"]
    except:
        r1=max(1,rank1); r2=max(1,rank2); ls=math.log(r2)+math.log(r1)
        p1_rank=math.log(r2)/ls if ls>0 else 0.5
        p1 = 0.5*p1_rank+0.5*(1/odd_1)/(1/odd_1+1/odd_2) if odd_1>1 and odd_2>1 else p1_rank
        p2 = 1-p1
    edge_1=round(p1-(1/odd_1),3) if odd_1>1 else 0
    edge_2=round(p2-(1/odd_2),3) if odd_2>1 else 0
    conf="💎 DIAMANTE" if max(p1,p2)>0.68 else("🔥 ALTA" if max(p1,p2)>0.58 else "⚡ MEDIA")
    return {"p1":round(p1,3),"p2":round(p2,3),"edge_1":edge_1,"edge_2":edge_2,"conf":conf}


def tennis_expert_analysis(p1_name, p2_name, rank1, rank2, odd_1, odd_2,
                            surface, torneo, model_p1=0.5, model_p2=0.5):
    """Wrapper con caché en disco — llama al análisis real si no hay resultado cacheado."""
    import hashlib, json as _j, os as _os, time as _t
    # Clave basada solo en jugadores + superficie + torneo (no en probs flotantes)
    key = hashlib.md5(f"{p1_name}|{p2_name}|{surface}|{torneo}".encode()).hexdigest()[:16]
    today = __import__('datetime').datetime.now().strftime("%Y-%m-%d")
    cache_path = f"/tmp/tenis_ai_{key}_{today}.json"
    # Intentar leer del disco primero
    if _os.path.exists(cache_path):
        try:
            with open(cache_path) as f: return _j.load(f)
        except: pass
    result = _tennis_expert_analysis_raw(p1_name, p2_name, rank1, rank2,
                                          odd_1, odd_2, surface, torneo, model_p1, model_p2)
    if result:
        try:
            with open(cache_path, 'w') as f: _j.dump(result, f)
        except: pass
    return result

def _tennis_expert_analysis_raw(p1_name, p2_name, rank1, rank2, odd_1, odd_2,
                            surface, torneo, model_p1, model_p2):
    """
    Einstein experto en tenis:
    - Analiza H2H real de ambos jugadores
    - Forma reciente en esta superficie específica
    - Historial en este torneo
    - Lesiones conocidas, fatiga
    - Da probabilidades REALES, no siempre 58/42
    """
    if not ANTHROPIC_API_KEY: return None
    prompt = f"""Eres EINSTEIN TENIS, el analista de tenis más avanzado del mundo.
Analiza en PROFUNDIDAD este partido ATP/WTA y da probabilidades REALES.

PARTIDO: {p1_name} vs {p2_name}
TORNEO: {torneo} — SUPERFICIE: {surface.upper()}
RANKING: {p1_name} #{rank1 if rank1<900 else "?"} vs {p2_name} #{rank2 if rank2<900 else "?"}
MOMIOS: {f"{p1_name} @{odd_1:.2f}" if odd_1>1 else "N/D"} / {f"{p2_name} @{odd_2:.2f}" if odd_2>1 else "N/D"}
MODELO WEIBULL BASE: {p1_name} {model_p1*100:.1f}% / {p2_name} {model_p2*100:.1f}%

ANALIZA EXHAUSTIVAMENTE:
1. H2H histórico entre estos dos jugadores (¿cuántos partidos? ¿quién domina? ¿en qué superficie?)
2. Forma reciente de {p1_name}: últimos 5-10 torneos, W/L, superficie actual, lesiones
3. Forma reciente de {p2_name}: últimos 5-10 torneos, W/L, superficie actual, lesiones  
4. Historial específico en {torneo} de ambos
5. Estadísticas en {surface}: % victorias, profundidad de torneo habitual
6. Variables ocultas: fatiga (cuántos sets esta semana), altura del torneo, temperatura
7. Motivación: ¿quién NECESITA más esta victoria para ranking/clasificación?
8. Estilo de juego: ¿el surface favorece más a uno? (servidor en hierba, defensor en tierra)

REGLAS CRÍTICAS:
- Si hay clara diferencia de nivel: da probabilidades reales (70/30, 75/25, etc.)
- Si es parejo de verdad: 55/45 o 52/48 está bien
- NO des siempre 58/42 — eso es inventar, no analizar
- Si un jugador viene de lesión o jugó mucho: refléjalo en la prob
- Basa el % final en los datos reales que conoces

RESPONDE SOLO JSON:
{{
  "p1_pct": <float 0-100, prob real {p1_name}>,
  "p2_pct": <float 0-100, prob real {p2_name}>,
  "h2h_resumen": "<H2H: X-Y a favor de ?, en qué superficie domina>",
  "forma_p1": "<últimos 5 resultados, lesiones, superficie>",
  "forma_p2": "<últimos 5 resultados, lesiones, superficie>",
  "factor_decisivo": "<qué factor inclina la balanza>",
  "surface_ventaja": "<quién se beneficia más de {surface}>",
  "resumen": "<2-3 líneas: análisis concreto con datos reales>",
  "confianza_analisis": "<alta/media/baja>",
  "edge_p1": <float, edge vs momio>,
  "edge_p2": <float, edge vs momio>
}}"""
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":800,
                  "messages":[{"role":"user","content":prompt}]},timeout=20)
        if r.status_code!=200: return None
        raw = r.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
        if "{" in raw: raw=raw[raw.find("{"):raw.rfind("}")+1]
        import json as _jt; d = _jt.loads(raw)
        p1 = max(5,min(95,float(d.get("p1_pct",model_p1*100))))/100
        p2 = 1-p1
        conf = "💎 DIAMANTE" if max(p1,p2)>0.68 else ("🔥 ALTA" if max(p1,p2)>0.62 else "⚡ MEDIA")
        return {
            "p1": round(p1,3), "p2": round(p2,3), "conf": conf,
            "h2h": d.get("h2h_resumen",""), "forma_p1": d.get("forma_p1",""),
            "forma_p2": d.get("forma_p2",""), "factor": d.get("factor_decisivo",""),
            "surface_adv": d.get("surface_ventaja",""), "resumen": d.get("resumen",""),
            "confianza": d.get("confianza_analisis","media"),
            "edge_p1": float(d.get("edge_p1",0)), "edge_p2": float(d.get("edge_p2",0)),
        }
    except: return None

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
for k,v in [("view","cartelera"),("sel",None)]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;padding:16px 0 6px'>
  <div style='font-family:Rajdhani,sans-serif;font-size:clamp(1.6rem,6vw,2.8rem);font-weight:900;
    background:linear-gradient(135deg,#7c00ff,#00ccff,#FFD700);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:.06em;line-height:1.1'>
    THE GAMBLERS LAYER
  </div>
  <div style='color:#555!important;font-size:clamp(.6rem,.9vw,.8rem);letter-spacing:.12em;margin-top:4px'>
    PICKS · PARLAY · TRILAY · PATO · TELEGRAM BOT
  </div>
</div>""", unsafe_allow_html=True)

# ── Sport selector ──
st.markdown("""
<style>
@media(max-width:480px){
  div[data-testid="stHorizontalBlock"] .stButton>button{font-size:.72rem!important;padding:8px 2px!important}
}
</style>""", unsafe_allow_html=True)
sp1,sp2,sp3 = st.columns(3)
with sp1:
    if st.button("⚽ Fútbol", use_container_width=True,
                 type="primary" if st.session_state.get("sport","futbol")=="futbol" else "secondary"):
        st.session_state["sport"]="futbol"; st.session_state["view"]="cartelera"; st.rerun()
with sp2:
    if st.button("🎾 Tenis", use_container_width=True,
                 type="primary" if st.session_state.get("sport","futbol")=="tenis" else "secondary"):
        st.session_state["sport"]="tenis"; st.session_state["view"]="cartelera"; st.rerun()
with sp3:
    if st.button("🏀 NBA", use_container_width=True,
                 type="primary" if st.session_state.get("sport","futbol")=="nba" else "secondary"):
        st.session_state["sport"]="nba"; st.session_state["view"]="cartelera"; st.rerun()

if "sport" not in st.session_state: st.session_state["sport"]="futbol"
deporte = st.session_state["sport"]

# ══════════════════════════════════════════════════════════
# CARGAR DATA SEGÚN DEPORTE
# ══════════════════════════════════════════════════════════
if deporte == "futbol":
    with st.spinner("Cargando cartelera..."):
        all_matches = get_cartelera()
    if not all_matches:
        st.warning("No hay partidos disponibles.")
        st.stop()
    liga_opts = ["Todas"] + sorted(set(m["league"] for m in all_matches))
    liga_sel  = st.selectbox("Liga", liga_opts, label_visibility="collapsed")
    matches   = all_matches if liga_sel=="Todas" else [m for m in all_matches if m["league"]==liga_sel]

elif deporte == "nba":
    with st.spinner("Cargando NBA..."):
        nba_games = get_nba_cartelera()

elif deporte == "tenis":
    with st.spinner("Cargando Tenis..."):
        ten_matches = get_tennis_cartelera()

# ══════════════════════════════════════════════════════════
# CARTELERA
# ══════════════════════════════════════════════════════════
if st.session_state["view"] == "cartelera":

    # ─── NBA ─────────────────────────────────────────────
    if deporte == "nba":
        tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial","🎓 Califica tu Pick","📊 Resultados"])
        with tab1:
            st.markdown("<div class='shdr'>🏀 NBA — Over / Under · ML</div>", unsafe_allow_html=True)
            if not nba_games:
                st.info("No hay juegos NBA hoy.")
            from collections import defaultdict
            nba_por_fecha = defaultdict(list)
            for g in nba_games: nba_por_fecha[g["fecha"]].append(g)
            def fecha_label_nba(f):
                try:
                    d=datetime.strptime(f,"%Y-%m-%d")
                    dias=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                    meses=["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                    return f"🏀 {dias[d.weekday()]} {d.day} {meses[d.month]}"
                except: return f
            for fi, fecha in enumerate(sorted(nba_por_fecha.keys())):
                gs = nba_por_fecha[fecha]
                with st.expander(f"{fecha_label_nba(fecha)}  ·  {len(gs)} juegos", expanded=(fi==0)):
                    for g in gs:
                        if g["state"] == "post":
                            sh=g.get("score_h",-1); sa=g.get("score_a",-1)
                            sf=f"{sh}-{sa}" if sh>=0 else "FT"
                            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 14px;background:#0a0a1e;border-radius:8px;margin:2px 0;border-left:3px solid #333;opacity:.6'><div style='font-size:.82rem;color:#555'>✅ 🏀 {g['away']} @ {g['home']}</div><div style='font-size:.9rem;font-weight:700;color:#555'>{sf}</div></div>", unsafe_allow_html=True)
                            continue
                        live = g["state"]=="in"
                        sc   = f"{g['score_h']}-{g['score_a']}" if live else g["hora"]
                        ou   = f" · Línea {g['ou_line']}" if g["ou_line"]>0 else ""
                        lbl  = f"{'🔴 ' if live else '🏀 '}{g['away']} @ {g['home']}  ·  {sc}{ou}"
                        if st.button(lbl, key=f"nba_{g['id']}", use_container_width=True):
                            with st.spinner("🤖 IA analizando partido..."):
                                res = nba_ou_model(g["home_id"], g["away_id"], g["ou_line"])
                                ai_prompt = (
                                    f"Eres analista NBA experto. Analiza:\n"
                                    f"{g['away']} (visitante) @ {g['home']} (local)\n"
                                    f"Proyección total: {res['proj']} pts | Línea O/U: {res['line']}\n"
                                    f"Modelo: Over={res['p_over']*100:.1f}% Under={res['p_under']*100:.1f}%\n\n"
                                    f"Responde SOLO en JSON sin texto extra:\n"
                                    f"{{\"over\": 58, \"under\": 42, \"ml_local\": 55, \"ml_visita\": 45, "
                                    f"\"rec_ou\": \"OVER\", \"rec_ml\": \"{g['home']}\", "
                                    f"\"conf\": \"Alta\", \"resumen\": \"2-3 lineas: O/U razon, ML quien gana y por que\"}}\n"
                                    f"over+under=100, ml_local+ml_visita=100. Considera ritmo de juego, defensa, forma reciente."
                                )
                                ai_over = res["p_over"]*100
                                ai_under = res["p_under"]*100
                                ai_ml_h = 55.0; ai_ml_a = 45.0
                                ai_rec_ou = res["rec"]; ai_rec_ml = g["home"]
                                ai_txt = ""; ai_conf = "⚡ MEDIA"
                                try:
                                    ai_r = requests.post("https://api.anthropic.com/v1/messages",
                                        headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"},
                                        json={"model":"claude-sonnet-4-20250514","max_tokens":400,
                                              "messages":[{"role":"user","content":ai_prompt}]},timeout=15)
                                    raw = ai_r.json()["content"][0]["text"].strip()
                                    raw = raw.replace("```json","").replace("```","").strip()
                                    import json as _json
                                    ad = _json.loads(raw)
                                    ai_over   = float(ad.get("over", ai_over))
                                    ai_under  = float(ad.get("under", ai_under))
                                    ai_ml_h   = float(ad.get("ml_local", ai_ml_h))
                                    ai_ml_a   = float(ad.get("ml_visita", ai_ml_a))
                                    ai_rec_ou = ad.get("rec_ou", "OVER")
                                    ai_rec_ml = ad.get("rec_ml", g["home"])
                                    ai_txt    = ad.get("resumen","")
                                    c = ad.get("conf","Media")
                                    ai_conf   = "💎 DIAMANTE" if "alta" in c.lower() and max(ai_over,ai_under)>62 else ("🔥 ALTA" if "alta" in c.lower() else "⚡ MEDIA")
                                except: ai_txt = raw if 'raw' in dir() else ""
                            ou_color  = "#ff4444" if "OVER" in ai_rec_ou.upper() else "#00ccff"
                            ml_color  = "#00ff88"
                            conf_color2 = "#FFD700" if "DIAMANTE" in ai_conf else ("#00ff88" if "ALTA" in ai_conf else "#aaa")
                            st.markdown(
                                f"<div class='acard' style='border-color:{conf_color2}'>"
                                f"<div style='font-size:1.1rem;font-weight:900;color:{conf_color2};margin-bottom:14px'>"
                                f"📊 {ai_rec_ou} · ML: {ai_rec_ml}  <span style='font-size:.75rem;font-weight:400;color:#555'>{ai_conf}</span></div>"
                                f"<div style='font-size:.78rem;color:#555;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em'>Over / Under {res['line']}</div>"
                                f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px'>"
                                f"<div class='mbox' style='flex:1'>"
                                f"<div class='mval' style='color:#ff4444'>{ai_over:.0f}%</div>"
                                f"<div class='mlbl'>🔥 Over {res['line']}</div>"
                                f"<div style='height:5px;background:#1a1a40;border-radius:3px;margin-top:6px'>"
                                f"<div style='height:5px;width:{ai_over:.0f}%;background:#ff4444;border-radius:3px'></div></div></div>"
                                f"<div class='mbox' style='flex:1'>"
                                f"<div class='mval' style='color:#00ccff'>{ai_under:.0f}%</div>"
                                f"<div class='mlbl'>❄️ Under {res['line']}</div>"
                                f"<div style='height:5px;background:#1a1a40;border-radius:3px;margin-top:6px'>"
                                f"<div style='height:5px;width:{ai_under:.0f}%;background:#00ccff;border-radius:3px'></div></div></div>"
                                f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{res['proj']}</div><div class='mlbl'>Proy pts</div></div>"
                                f"</div>"
                                f"<div style='font-size:.78rem;color:#555;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em'>Money Line</div>"
                                f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px'>"
                                f"<div class='mbox' style='flex:1'>"
                                f"<div class='mval' style='color:#00ff88'>{ai_ml_h:.0f}%</div>"
                                f"<div class='mlbl'>🏠 {g['home'][:12]}</div>"
                                f"<div style='height:5px;background:#1a1a40;border-radius:3px;margin-top:6px'>"
                                f"<div style='height:5px;width:{ai_ml_h:.0f}%;background:#00ff88;border-radius:3px'></div></div></div>"
                                f"<div class='mbox' style='flex:1'>"
                                f"<div class='mval' style='color:#aa00ff'>{ai_ml_a:.0f}%</div>"
                                f"<div class='mlbl'>✈️ {g['away'][:12]}</div>"
                                f"<div style='height:5px;background:#1a1a40;border-radius:3px;margin-top:6px'>"
                                f"<div style='height:5px;width:{ai_ml_a:.0f}%;background:#aa00ff;border-radius:3px'></div></div></div>"
                                f"</div>"
                                + (f"<div style='background:#0a0a26;border-radius:10px;padding:12px 14px;"
                                   f"border-left:3px solid {conf_color2};font-size:.88rem;line-height:1.7'>"
                                   f"🤖 <b>Análisis IA:</b><br>{ai_txt.replace(chr(10),'<br>')}</div>" if ai_txt else "")
                                + f"</div>", unsafe_allow_html=True)
        # ── VEREDICTO ACADÉMICO NBA ──
        nba_mc_fake = {
            "dc_ph": ai_ml_h/100, "bvp_ph": ai_ml_h/100,
            "elo_ph": ai_ml_h/100, "h2h_ph": ai_ml_h/100,
            "xg_h": res.get("proj",220)/2 / 100, "xg_a": res.get("proj",220)/2 / 100,
            "o25": ai_over/100, "o35": 0.35, "btts": 0.5,
        }
        nba_dp_fake = {"ph": ai_ml_h/100, "pa": ai_ml_a/100, "pd": 0.0, "conf": ai_conf}
        _nba_best_mkt = f"O/U {g.get('ou_line','')}" if g.get("ou_line") else (g["home"] if ai_ml_h >= ai_ml_a else g["away"])
        _nba_best_prob = (ai_over/100) if g.get("ou_line") else max(ai_ml_h, ai_ml_a)/100
        nba_verdict_html = veredicto_academico(
            nba_mc_fake, nba_dp_fake,
            g.get("odd_h",0), g.get("odd_a",0), 0,
            g["home"], g["away"],
            best_market=_nba_best_mkt,
            best_prob=_nba_best_prob,
            best_odd=0
        )
        st.markdown(nba_verdict_html, unsafe_allow_html=True)

        # ── PRE-MATCH INTELLIGENCE BOT — NBA ──
        _nba_ou = g.get("ou_line",220)
        adj_nba, _was_adj_nba = render_prematch_bot(
            sport="nba", home=g["home"], away=g["away"],
            league_slug="nba", league_name="NBA",
            model_result={"ph":0.5,"pa":0.5,"proj":_nba_ou},
            ou_line=_nba_ou,
            hora_partido=g.get("hora","")
        )
        # ── ACTION NETWORK NBA ──
        render_action_network_nba(g["home"], g["away"], g.get("ou_line",0))
        with tab2:
            st.markdown("<div class='shdr'>🎰 TRILAY — Todos los Deportes</div>", unsafe_allow_html=True)
            st.info("El TRILAY multi-deporte con Fútbol + NBA + Tenis está en ⚽ Fútbol → TRILAY. Aquí verás el mejor pick NBA del día:")
            with st.spinner("Calculando TRILAY NBA..."):
                _nba_cands = []
                for _g in nba_games[:20]:
                    if _g["state"]!="pre": continue
                    _r = nba_ou_model(_g["home_id"],_g["away_id"],_g["ou_line"])
                    _bp = max(_r["p_over"],_r["p_under"])
                    _bm = f"🔥 Over {_r['line']}" if _r["p_over"]>_r["p_under"] else f"❄️ Under {_r['line']}"
                    if _bp >= 0.55:
                        _nba_cands.append({"teams":f"{_g['away']} @ {_g['home']}","liga":"NBA","hora":_g["hora"],"pick":_bm,"prob":_bp,"sport":"🏀"})
                _nba_cands.sort(key=lambda x:-x["prob"])
                _trilay3 = _nba_cands[:3]
            if len(_trilay3) >= 2:
                _comb = 1.0
                for _t in _trilay3: _comb *= _t["prob"]
                _cuota = round(1/_comb, 2) if _comb>0 else 0
                st.markdown(f"<div class='trilay-card'><div style='font-size:.8rem;font-weight:700;color:#aa00ff;letter-spacing:.1em;margin-bottom:12px'>✦ TRILAY NBA DEL DÍA</div><div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px'><div class='mbox' style='flex:1'><div class='mval' style='color:#aa00ff'>{_comb*100:.1f}%</div><div class='mlbl'>Prob. combinada</div></div><div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{_cuota}x</div><div class='mlbl'>Cuota estimada</div></div></div>", unsafe_allow_html=True)
                for _i,_t in enumerate(_trilay3):
                    _cc = "#FFD700" if _t["prob"]>0.65 else ("#00ff88" if _t["prob"]>0.58 else "#aaa")
                    st.markdown(f"<div class='mrow'><span style='color:{_cc};font-weight:700'>{_i+1}. {_t['teams']}</span><br><span style='color:#555;font-size:.78rem'>NBA · {_t['hora']}</span><br><span style='color:#00ccff;font-weight:700'>{_t['pick']}</span> <span style='color:{_cc};font-size:.85rem'>{_t['prob']*100:.1f}%</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No hay suficientes picks NBA para TRILAY hoy.")
        with tab3:
            st.info("PATO es exclusivo de fútbol (Under 4.5 goles).")
        with tab4:
            st.info("Los picks unificados de todos los deportes están en ⚽ Fútbol → 🎯 Picks.")
            st.markdown("<div class='shdr'>🎯 Picks NBA del Día — O/U + ML</div>", unsafe_allow_html=True)
            with st.spinner("🤖 IA calculando picks NBA..."):
                nba_picks = []
                for g in nba_games[:20]:
                    if g["state"]!="pre": continue
                    res = nba_ou_model(g["home_id"],g["away_id"],g["ou_line"])
                    best_p = max(res["p_over"],res["p_under"])
                    best_m = f"🔥 Over {res['line']}" if res["p_over"]>res["p_under"] else f"❄️ Under {res['line']}"
                    if best_p-0.5 > 0.04:
                        conf = "💎 DIAMANTE" if best_p>0.65 else ("🔥 ALTA" if best_p>0.58 else "⚡ MEDIA")
                        nba_picks.append({"home":g["home"],"away":g["away"],"hora":g["hora"],"pick":best_m,"prob":best_p,"conf":conf,"type":"O/U"})
                # Add ML picks via AI for top 6 games
                try:
                    _top_games = [g for g in nba_games[:6] if g["state"]=="pre"]
                    if _top_games and ANTHROPIC_API_KEY:
                        _games_txt = "\n".join([f"{g['away']} @ {g['home']}" for g in _top_games])
                        _ml_r = requests.post("https://api.anthropic.com/v1/messages",
                            headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"},
                            json={"model":"claude-sonnet-4-20250514","max_tokens":600,
                                  "messages":[{"role":"user","content":
                                    "NBA ML picks experto. Para estos partidos da solo los que tengan valor real (prob >= 58%). Responde SOLO en JSON array: [{teams, ml_pick, prob, razon}]. Partidos:\n" + _games_txt}]},timeout=12)
                        import json as _j
                        _ml_raw = _ml_r.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
                        _ml_data = _j.loads(_ml_raw)
                        for _ml in _ml_data:
                            _p = float(_ml.get("prob",0))/100
                            if _p >= 0.58:
                                _conf = "💎 DIAMANTE" if _p>0.65 else ("🔥 ALTA" if _p>0.60 else "⚡ MEDIA")
                                nba_picks.append({"home":_ml["teams"].split(" @ ")[1] if " @ " in _ml["teams"] else _ml["teams"],
                                                  "away":_ml["teams"].split(" @ ")[0] if " @ " in _ml["teams"] else "",
                                                  "hora":"","pick":f"🏆 ML: {_ml['ml_pick']}","prob":_p,
                                                  "conf":_conf,"type":"ML","razon":_ml.get("razon","")})
                except: pass
                nba_picks.sort(key=lambda x:-x["prob"])
            if not nba_picks: st.info("No hay picks NBA con valor hoy.")
            for p in nba_picks:
                cc = "#FFD700" if "DIAMANTE" in p["conf"] else ("#00ff88" if "ALTA" in p["conf"] else "#aaa")
                tipo_badge = f"<span style='background:#ff444422;color:#ff4444;border-radius:4px;padding:2px 6px;font-size:.7rem;margin-left:6px'>{p.get('type','')}</span>"
                razon_txt = f"<div style='color:#555;font-size:.76rem;margin-top:2px'>{p.get('razon','')}</div>" if p.get('razon') else ""
                st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between;align-items:center'><div style='flex:1;min-width:0'><div style='font-weight:700;font-size:.9rem'>{p['away']} @ {p['home']}{tipo_badge}</div><div style='color:#555;font-size:.78rem'>NBA{' · '+p['hora'] if p['hora'] else ''}</div><div style='margin-top:4px;color:#00ccff;font-weight:700'>{p['pick']}</div>{razon_txt}</div><div style='text-align:right;flex-shrink:0'><div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{p['prob']*100:.1f}%</div><div style='font-size:.72rem;color:{cc}'>{p['conf']}</div></div></div>",unsafe_allow_html=True)
        with tab5:
            def _nba_preview():
                with st.spinner("Calculando preview NBA..."):
                    _prev = []
                    for _g in nba_games[:15]:
                        if _g["state"]!="pre": continue
                        _r = nba_ou_model(_g["home_id"],_g["away_id"],_g["ou_line"])
                        _bp = max(_r["p_over"],_r["p_under"])
                        if _bp-0.5 >= 0.04:
                            _pick = f"{'🔥 Over' if _r['p_over']>_r['p_under'] else '❄️ Under'} {_r['line']}"
                            _prev.append({"teams":f"{_g['away']} @ {_g['home']}","hora":_g["hora"],"pick":_pick,"prob":_bp})
                    _prev.sort(key=lambda x:-x["prob"])
                if not _prev:
                    st.markdown("<div style='color:#555;padding:10px'>Sin picks NBA con edge>4% ahora.</div>",unsafe_allow_html=True)
                for _p in _prev[:5]:
                    _cc = "#FFD700" if _p["prob"]>0.65 else "#00ff88"
                    st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-weight:700'>{_p['teams']}</div><div style='color:#555;font-size:.8rem'>NBA · {_p['hora']}</div><div style='color:#00ccff;font-weight:700;margin-top:4px'>{_p['pick']}</div></div><div style='text-align:right'><div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{_p['prob']*100:.1f}%</div></div></div>",unsafe_allow_html=True)
            render_bot_tab("🏀 NBA", escanear_nba_y_enviar, [nba_games], _nba_preview)
        with tab6:
            st.markdown("<div class='shdr'>📋 Historial de Picks</div>", unsafe_allow_html=True)
            init_history()
            render_history()
        with tab7:
            st.markdown("<div class='shdr'>🎓 Califica tu Pick — Einstein 🧠</div>", unsafe_allow_html=True)
            # Detector de anomalías NBA
            _an_nba_pro = get_action_network_pro(
                nba_games[0]["home"] if nba_games else "", 
                nba_games[0]["away"] if nba_games else "", "nba")
            render_fix_detector("nba","","",{},{},{},
                               {"slug":"nba"},an_data=_an_nba_pro)
            render_einstein_califica("nba")
        with tab8:
            render_resultados_tab()

    # ─── TENIS ───────────────────────────────────────────
    elif deporte == "tenis":
        tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial","🎓 Califica tu Pick","📊 Resultados"])
        with tab1:
            st.markdown("<div class='shdr'>🎾 Tenis ATP / WTA</div>", unsafe_allow_html=True)
            if not ten_matches:
                st.info("No hay partidos ATP/WTA disponibles para estas fechas.")
            from collections import defaultdict
            ten_por_fecha = defaultdict(lambda: defaultdict(list))
            for m in ten_matches: ten_por_fecha[m["fecha"]][m["tour"]].append(m)
            def fecha_label_ten(f):
                try:
                    d=datetime.strptime(f,"%Y-%m-%d")
                    dias=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                    meses=["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                    return f"🎾 {dias[d.weekday()]} {d.day} {meses[d.month]}"
                except: return f
            for fi, fecha in enumerate(sorted(ten_por_fecha.keys())):
                total_ms = sum(len(v) for v in ten_por_fecha[fecha].values())
                with st.expander(f"{fecha_label_ten(fecha)}  ·  {total_ms} partidos", expanded=(fi==0)):
                    for tour in ["ATP","WTA"]:
                        ms = ten_por_fecha[fecha].get(tour,[])
                        if not ms: continue
                        st.markdown(f"<div class='shdr'>{tour} 🎾</div>", unsafe_allow_html=True)
                        for m in ms:
                            tm = tennis_model(m["rank1"], m["rank2"], m["odd_1"], m["odd_2"])
                            fav = m["p1"] if tm["p1"]>=tm["p2"] else m["p2"]
                            fav_p = max(tm["p1"],tm["p2"])
                            conf_color = "#FFD700" if "DIAMANTE" in tm["conf"] else ("#00ff88" if "ALTA" in tm["conf"] else "#555")
                            # Finished tennis = show score, don't show as button
                        if m["state"] == "post":
                            st.markdown(
                                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                                f"padding:6px 12px;background:#0a0a1e;border-radius:8px;margin:2px 0;"
                                f"border-left:3px solid #333;opacity:.6'>"
                                f"<div style='font-size:.82rem;color:#555'>✅ {m['p1']} vs {m['p2']}</div>"
                                f"<div style='font-size:.8rem;color:#555'>FT</div>"
                                f"</div>", unsafe_allow_html=True)
                            continue
                        if st.button(f"🎾 {m['p1']} vs {m['p2']}  ·  {m['hora']} CDMX", key=f"ten_{m['id']}", use_container_width=True):
                                with st.spinner("🤖 IA analizando..."):
                                    ai_prompt = (
                                        f"Analista tenis experto. Partido ATP/WTA:\n"
                                        f"Torneo: {m['torneo']}\n"
                                        f"{m['p1']} (rank #{m['rank1'] if m['rank1']<900 else '?'}) vs {m['p2']} (rank #{m['rank2'] if m['rank2']<900 else '?'})\n"
                                        f"Momios: {m['odd_1'] if m['odd_1']>1 else 'N/D'} / {m['odd_2'] if m['odd_2']>1 else 'N/D'}\n\n"
                                        f"Responde SOLO en este JSON, sin texto extra:\n"
                                        f"{{\"p1\": 55, \"p2\": 45, \"fav\": \"{m['p1']}\", "
                                        f"\"conf\": \"Alta\", \"resumen\": \"2-3 lineas: quien gana, por que (ranking/superficie/forma), si hay valor en momios\"}}\n\n"
                                        f"p1+p2 deben sumar 100. Basa los % en ranking, historial en la superficie y forma reciente."
                                    )
                                    ai_p1, ai_p2 = tm["p1"]*100, tm["p2"]*100
                                    ai_fav = fav
                                    ai_txt = ""
                                    ai_conf = tm["conf"]
                                    try:
                                        ai_r = requests.post("https://api.anthropic.com/v1/messages",
                                            headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"},
                                            json={"model":"claude-sonnet-4-20250514","max_tokens":400,
                                                  "messages":[{"role":"user","content":ai_prompt}]},timeout=15)
                                        raw = ai_r.json()["content"][0]["text"].strip()
                                        raw = raw.replace("```json","").replace("```","").strip()
                                        import json as _json
                                        ai_data = _json.loads(raw)
                                        ai_p1   = float(ai_data.get("p1", ai_p1))
                                        ai_p2   = float(ai_data.get("p2", ai_p2))
                                        # normalizar a 100
                                        s = ai_p1 + ai_p2
                                        if s > 0: ai_p1 = ai_p1/s*100; ai_p2 = ai_p2/s*100
                                        ai_fav  = ai_data.get("fav", fav)
                                        ai_txt  = ai_data.get("resumen","")
                                        c = ai_data.get("conf","Media")
                                        ai_conf = "💎 DIAMANTE" if "alta" in c.lower() and ai_p1>65 else ("🔥 ALTA" if "alta" in c.lower() else ("⚡ MEDIA" if "media" in c.lower() else "🔻 BAJA"))
                                    except: ai_txt = raw if 'raw' in dir() else ""
                                # color según confianza IA
                                ai_color = "#FFD700" if "DIAMANTE" in ai_conf else ("#00ff88" if "ALTA" in ai_conf else ("#aaa" if "MEDIA" in ai_conf else "#ff4444"))
                                fav_pct = max(ai_p1, ai_p2)
                                p1_color = "#00ccff" if ai_p1 >= ai_p2 else "#aa00ff"
                                p2_color = "#aa00ff" if ai_p1 >= ai_p2 else "#00ccff"
                                st.markdown(
                                    f"<div class='acard' style='border-color:{ai_color}'>"
                                    f"<div style='font-weight:900;font-size:1.1rem;color:{ai_color};margin-bottom:10px'>"
                                    f"{fav_pct:.0f}% → {ai_fav}  <span style='font-size:.78rem;font-weight:400;color:#555'>{ai_conf}</span></div>"
                                    f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px'>"
                                    f"<div class='mbox' style='flex:1'>"
                                    f"<div class='mval' style='color:{p1_color}'>{ai_p1:.0f}%</div>"
                                    f"<div class='mlbl'>{m['p1'][:14]}</div>"
                                    f"<div style='height:5px;background:#1a1a40;border-radius:3px;margin-top:6px'>"
                                    f"<div style='height:5px;width:{ai_p1:.0f}%;background:{p1_color};border-radius:3px'></div></div>"
                                    f"</div>"
                                    f"<div class='mbox' style='flex:1'>"
                                    f"<div class='mval' style='color:{p2_color}'>{ai_p2:.0f}%</div>"
                                    f"<div class='mlbl'>{m['p2'][:14]}</div>"
                                    f"<div style='height:5px;background:#1a1a40;border-radius:3px;margin-top:6px'>"
                                    f"<div style='height:5px;width:{ai_p2:.0f}%;background:{p2_color};border-radius:3px'></div></div>"
                                    f"</div></div>"
                                    + (f"<div style='background:#0a0a26;border-radius:10px;padding:12px 14px;"
                                       f"border-left:3px solid {ai_color};font-size:.88rem;line-height:1.7'>"
                                       f"🤖 <b>Análisis IA:</b><br>{ai_txt.replace(chr(10),'<br>')}</div>" if ai_txt else "")
                                    + f"</div>", unsafe_allow_html=True)
                                # ── VEREDICTO ACADÉMICO TENIS ──
                                _ten_mc_v = {
                                    "dc_ph": ai_p1/100, "bvp_ph": ai_p1/100,
                                    "elo_ph": ai_p1/100, "h2h_ph": ai_p1/100,
                                    "xg_h": 1.0, "xg_a": 1.0,
                                    "o25":0.5,"o35":0.3,"btts":0.5,
                                }
                                _ten_dp_v = {"ph": ai_p1/100, "pa": ai_p2/100, "pd": 0.0, "conf": ai_conf}
                                _ten_odd1 = m.get("odd_1",0); _ten_odd2 = m.get("odd_2",0)
                                _ten_fav = m["p1"] if ai_p1>=ai_p2 else m["p2"]
                                _ten_fav_prob = max(ai_p1,ai_p2)/100
                                _ten_fav_odd  = _ten_odd1 if ai_p1>=ai_p2 else _ten_odd2
                                st.markdown(veredicto_academico(
                                    _ten_mc_v, _ten_dp_v,
                                    _ten_odd1, _ten_odd2, 0,
                                    m["p1"], m["p2"],
                                    best_market=f"🎾 ML: {_ten_fav}",
                                    best_prob=_ten_fav_prob,
                                    best_odd=_ten_fav_odd
                                ), unsafe_allow_html=True)

                                # ── PRE-MATCH BOT — Tenis ──
                                _ten_model = {"p1": ai_p1/100, "p2": ai_p2/100, "ph": ai_p1/100, "pd": 0, "pa": ai_p2/100}
                                render_prematch_bot(
                                    sport="tennis",
                                    home=m["p1"], away=m["p2"],
                                    league_slug=m.get("tour","tennis"),
                                    league_name=m.get("torneo", m.get("tour","Tenis")),
                                    model_result=_ten_model,
                                    rank1=m.get("rank1",0), rank2=m.get("rank2",0),
                                    hora_partido=m.get("hora","")
                                )
        with tab2:
            st.markdown("<div class='shdr'>🎰 TRILAY — Todos los Deportes</div>", unsafe_allow_html=True)
            st.info("El TRILAY multi-deporte con Fútbol + NBA + Tenis está en ⚽ Fútbol → TRILAY. Aquí verás el mejor pick Tenis del día:")
            with st.spinner("Calculando TRILAY Tenis..."):
                _ten_cands = []
                for _tm_match in ten_matches:
                    if _tm_match["state"]!="pre": continue
                    _tmm = tennis_model(_tm_match["rank1"],_tm_match["rank2"],_tm_match["odd_1"],_tm_match["odd_2"])
                    _bp = max(_tmm["p1"],_tmm["p2"])
                    _fv = _tm_match["p1"] if _tmm["p1"]>=_tmm["p2"] else _tm_match["p2"]
                    if _bp >= 0.58:
                        _ten_cands.append({"teams":f"{_tm_match['p1']} vs {_tm_match['p2']}","tour":_tm_match["tour"],"hora":_tm_match["hora"],"pick":f"🎾 {_fv}","prob":_bp})
                _ten_cands.sort(key=lambda x:-x["prob"])
                _trilay_ten = _ten_cands[:3]
            if len(_trilay_ten) >= 2:
                _comb_t = 1.0
                for _t in _trilay_ten: _comb_t *= _t["prob"]
                _cuota_t = round(1/_comb_t,2) if _comb_t>0 else 0
                st.markdown(f"<div class='trilay-card'><div style='font-size:.8rem;font-weight:700;color:#aa00ff;letter-spacing:.1em;margin-bottom:12px'>✦ TRILAY TENIS DEL DÍA</div><div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px'><div class='mbox' style='flex:1'><div class='mval' style='color:#aa00ff'>{_comb_t*100:.1f}%</div><div class='mlbl'>Prob. combinada</div></div><div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{_cuota_t}x</div><div class='mlbl'>Cuota estimada</div></div></div>",unsafe_allow_html=True)
                for _i,_t in enumerate(_trilay_ten):
                    _cc = "#FFD700" if _t["prob"]>0.65 else ("#00ff88" if _t["prob"]>0.58 else "#aaa")
                    st.markdown(f"<div class='mrow'><span style='color:{_cc};font-weight:700'>{_i+1}. {_t['teams']}</span><br><span style='color:#555;font-size:.78rem'>{_t['tour']} · {_t['hora']}</span><br><span style='color:#00ccff;font-weight:700'>{_t['pick']} gana</span> <span style='color:{_cc};font-size:.85rem'>{_t['prob']*100:.1f}%</span></div>",unsafe_allow_html=True)
                st.markdown("</div>",unsafe_allow_html=True)
            else:
                st.info("No hay suficientes picks de tenis para TRILAY hoy.")
        with tab3:
            st.info("PATO es exclusivo de fútbol.")
        with tab4:
            st.info("Los picks unificados de todos los deportes están en ⚽ Fútbol → 🎯 Picks.")
            st.markdown("<div class='shdr'>🎯 Picks Tenis del Día — ML + Valor</div>", unsafe_allow_html=True)
            # ── PASO 1: Weibull rápido en TODOS los partidos (~0s) ──
            _surface_map = {
                "Indian Wells":"hard","Miami":"hard","Roland Garros":"clay",
                "Wimbledon":"grass","US Open":"hard","Australian Open":"hard",
                "Monte Carlo":"clay","Madrid":"clay","Rome":"clay","Cincinnati":"hard",
                "Toronto":"hard","Montreal":"hard","Paris":"hard","Vienna":"hard",
                "Basel":"hard","Rotterdam":"hard","Dubai":"hard","Doha":"hard",
                "Barcelona":"clay","Hamburg":"clay","Geneva":"clay","Lyon":"clay",
                "Halle":"grass","Queen":"grass","Eastbourne":"grass","Birmingham":"grass",
            }
            candidates = []
            for m in ten_matches:
                if m["state"]!="pre": continue
                torneo  = m.get("torneo","")
                surface = next((v for k,v in _surface_map.items() if k.lower() in torneo.lower()), "hard")
                base_tm = tennis_model(m["rank1"],m["rank2"],m["odd_1"],m["odd_2"],surface)
                best_p  = max(base_tm["p1"], base_tm["p2"])
                candidates.append((best_p, m, surface, torneo, base_tm))
            candidates.sort(key=lambda x:-x[0])
            top6 = candidates[:6]  # Solo top 6 candidatos van a Einstein

            # ── PASO 2: Einstein — usa caché disco si existe, paralelo solo si hay misses ──
            import concurrent.futures
            def _analyze_one(args):
                best_p, m, surface, torneo, base_tm = args
                expert = tennis_expert_analysis(
                    m["p1"],m["p2"],m["rank1"],m["rank2"],
                    m["odd_1"],m["odd_2"],surface,torneo,
                    base_tm["p1"],base_tm["p2"]
                )
                return (m, surface, torneo, base_tm, expert)

            # ── Separar hits de caché vs misses (llamadas API reales) ──
            import hashlib as _hlib, json as _jcache, os as _oscache
            today_str = __import__('datetime').datetime.now().strftime("%Y-%m-%d")
            ten_picks_raw = []

            cached_results, need_api = [], []
            for c in top6:
                _, m, surface, torneo, base_tm = c
                key = _hlib.md5(f"{m['p1']}|{m['p2']}|{surface}|{torneo}".encode()).hexdigest()[:16]
                cp  = f"/tmp/tenis_ai_{key}_{today_str}.json"
                if _oscache.path.exists(cp):
                    try:
                        cached_results.append((m, surface, torneo, base_tm, _jcache.load(open(cp))))
                        continue
                    except: pass
                need_api.append(c)

            # Partidos cacheados = resultado instantáneo
            for m, surface, torneo, base_tm, expert in cached_results:
                p1_f = expert["p1"]; p2_f = expert["p2"]
                fav = m["p1"] if p1_f>=p2_f else m["p2"]
                best_p = max(p1_f, p2_f)
                best_odd = m["odd_1"] if p1_f>=p2_f else m["odd_2"]
                edge_v = (p1_f-(1/m["odd_1"])) if p1_f>=p2_f and m["odd_1"]>1 else                          (p2_f-(1/m["odd_2"])) if m["odd_2"]>1 else 0
                ten_picks_raw.append({
                    "p1":m["p1"],"p2":m["p2"],"hora":m["hora"],"tour":m["tour"],
                    "torneo":torneo,"surface":surface,
                    "pick":f"🎾 {fav}","prob":best_p,"odd":best_odd,
                    "conf":expert["conf"],"edge":edge_v,
                    "resumen":expert.get("resumen",""),"h2h":expert.get("h2h",""),
                    "factor":expert.get("factor",""),
                    "forma_p1":expert.get("forma_p1",""),"forma_p2":expert.get("forma_p2",""),
                    "surf_adv":expert.get("surface_adv",""),
                    "p1_pct":p1_f*100,"p2_pct":p2_f*100,"_from_cache":True,
                })

            # Partidos sin caché = llamada API (paralela, con barra de progreso)
            if need_api:
                n_api = len(need_api)
                prog_ten = st.progress(0, f"🧠 Einstein analizando {n_api} partido(s) nuevos... ({len(cached_results)} del caché)")
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
                    futures = {ex.submit(_analyze_one, c): i for i,c in enumerate(need_api)}
                    done = 0
                    for fut in concurrent.futures.as_completed(futures):
                        done += 1
                        prog_ten.progress(done/n_api, f"🧠 Einstein {done}/{n_api} nuevos · {len(cached_results)} del caché ✓")
                        try:
                            m, surface, torneo, base_tm, expert = fut.result()
                        except: continue
                        if expert:
                            p1_f = expert["p1"]; p2_f = expert["p2"]
                            conf = expert["conf"]
                            resumen=expert.get("resumen",""); h2h_txt=expert.get("h2h","")
                            factor=expert.get("factor",""); forma_p1=expert.get("forma_p1","")
                            forma_p2=expert.get("forma_p2",""); surf_adv=expert.get("surface_adv","")
                        else:
                            p1_f=base_tm["p1"]; p2_f=base_tm["p2"]; conf=base_tm["conf"]
                            resumen=h2h_txt=factor=forma_p1=forma_p2=surf_adv=""
                        fav=m["p1"] if p1_f>=p2_f else m["p2"]
                        best_p=max(p1_f,p2_f)
                        best_odd=m["odd_1"] if p1_f>=p2_f else m["odd_2"]
                        edge_v=(p1_f-(1/m["odd_1"])) if p1_f>=p2_f and m["odd_1"]>1 else                                (p2_f-(1/m["odd_2"])) if m["odd_2"]>1 else 0
                        ten_picks_raw.append({
                            "p1":m["p1"],"p2":m["p2"],"hora":m["hora"],"tour":m["tour"],
                            "torneo":torneo,"surface":surface,
                            "pick":f"🎾 {fav}","prob":best_p,"odd":best_odd,
                            "conf":conf,"edge":edge_v,
                            "resumen":resumen,"h2h":h2h_txt,"factor":factor,
                            "forma_p1":forma_p1,"forma_p2":forma_p2,"surf_adv":surf_adv,
                            "p1_pct":p1_f*100,"p2_pct":p2_f*100,
                        })
                prog_ten.empty()
            elif len(cached_results) > 0:
                st.caption(f"⚡ {len(cached_results)} análisis del caché — instantáneo")

            # TOP 3 por probabilidad más alta
            ten_picks_raw.sort(key=lambda x:-x["prob"])
            ten_picks = ten_picks_raw[:3]

            if not ten_picks:
                st.info("No hay picks de tenis disponibles hoy.")
            else:
                st.markdown(f"<div style='font-size:.72rem;color:#555;margin-bottom:8px'>🎾 Top 3 picks por mayor probabilidad · Einstein analiza H2H, superficie y forma</div>", unsafe_allow_html=True)

            for rank_i, p in enumerate(ten_picks):
                cc = "#FFD700" if "DIAMANTE" in p["conf"] else ("#00ff88" if "ALTA" in p["conf"] else "#aaa")
                rank_badge = ["🥇","🥈","🥉"][rank_i] if rank_i<3 else "🎾"
                os_ = f" @{p['odd']:.2f}" if p["odd"]>1 else ""
                surf_icon = {"hard":"🔵","clay":"🟤","grass":"🟢"}.get(p.get("surface","hard"),"🎾")
                edge_txt = f"<span style='color:#00ff88;font-size:.72rem'> edge +{p['edge']*100:.1f}%</span>" if p.get("edge",0)>0.02 else ""

                st.markdown(
                    f"<div class='mrow' style='margin-bottom:4px'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:flex-start'>"
                    f"<div style='flex:1;min-width:0'>"
                    f"<div style='font-weight:700;font-size:.92rem'>{rank_badge} {p['p1']} vs {p['p2']}</div>"
                    f"<div style='color:#555;font-size:.75rem'>{p['tour']} · {p['torneo']} {surf_icon} · {p['hora']}</div>"
                    f"<div style='margin-top:5px;color:#00ccff;font-weight:700;font-size:.95rem'>👉 {p['pick']}{os_}{edge_txt}</div>"
                    f"</div>"
                    f"<div style='text-align:right;flex-shrink:0;margin-left:12px'>"
                    f"<div style='font-size:1.5rem;font-weight:900;color:{cc}'>{p['prob']*100:.1f}%</div>"
                    f"<div style='font-size:.7rem;color:{cc}'>{p['conf']}</div>"
                    f"<div style='font-size:.68rem;color:#555'>{p['p1'][:10]}: {p['p1_pct']:.1f}% / {p['p2'][:10]}: {p['p2_pct']:.1f}%</div>"
                    f"</div></div>",
                    unsafe_allow_html=True)

                # Análisis Einstein expandido
                if p.get("resumen") or p.get("h2h") or p.get("factor"):
                    with st.expander(f"🧠 Análisis Einstein — {p['p1']} vs {p['p2']}"):
                        if p.get("h2h"):
                            st.markdown(f"<div style='font-size:.8rem;color:#00ccff;padding:4px 0'>⚔️ <b>H2H:</b> {p['h2h']}</div>",unsafe_allow_html=True)
                        cols = st.columns(2)
                        with cols[0]:
                            if p.get("forma_p1"):
                                st.markdown(f"<div style='font-size:.78rem;color:#aaa;background:#07071a;border-radius:8px;padding:8px'><b style='color:#00ff88'>{p['p1'][:16]}</b><br>{p['forma_p1']}</div>",unsafe_allow_html=True)
                        with cols[1]:
                            if p.get("forma_p2"):
                                st.markdown(f"<div style='font-size:.78rem;color:#aaa;background:#07071a;border-radius:8px;padding:8px'><b style='color:#aa00ff'>{p['p2'][:16]}</b><br>{p['forma_p2']}</div>",unsafe_allow_html=True)
                        if p.get("surf_adv"):
                            st.markdown(f"<div style='font-size:.78rem;color:#FFD700;padding:4px 0'>{surf_icon} <b>Superficie:</b> {p['surf_adv']}</div>",unsafe_allow_html=True)
                        if p.get("factor"):
                            st.markdown(f"<div style='font-size:.78rem;color:#ff9500;padding:4px 0'>⚡ <b>Factor decisivo:</b> {p['factor']}</div>",unsafe_allow_html=True)
                        if p.get("resumen"):
                            st.markdown(f"<div style='font-size:.82rem;color:#aaa;background:#07071a;border-radius:8px;padding:10px;margin-top:4px;line-height:1.6'>🧠 {p['resumen']}</div>",unsafe_allow_html=True)
        with tab5:
            def _ten_preview():
                with st.spinner("Calculando preview Tenis..."):
                    _prev = []
                    for _m in ten_matches:
                        if _m["state"]!="pre": continue
                        _tm = tennis_model(_m["rank1"],_m["rank2"],_m["odd_1"],_m["odd_2"])
                        _bp = max(_tm["p1"],_tm["p2"])
                        _fv = _m["p1"] if _tm["p1"]>=_tm["p2"] else _m["p2"]
                        if _bp >= 0.62:
                            _prev.append({"match":f"{_m['p1']} vs {_m['p2']}","tour":_m["tour"],"hora":_m["hora"],"fav":_fv,"prob":_bp})
                    _prev.sort(key=lambda x:-x["prob"])
                if not _prev:
                    st.markdown("<div style='color:#555;padding:10px'>Sin picks de tenis con prob>=62% ahora.</div>",unsafe_allow_html=True)
                for _p in _prev[:5]:
                    _cc = "#FFD700" if _p["prob"]>0.68 else "#00ff88"
                    st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-weight:700'>{_p['match']}</div><div style='color:#555;font-size:.8rem'>{_p['tour']} · {_p['hora']}</div><div style='color:#00ccff;font-weight:700;margin-top:4px'>🎾 {_p['fav']} gana</div></div><div style='text-align:right'><div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{_p['prob']*100:.1f}%</div></div></div>",unsafe_allow_html=True)
            render_bot_tab("🎾 Tenis", escanear_tenis_y_enviar, [ten_matches], _ten_preview)
        with tab6:
            st.markdown("<div class='shdr'>📋 Historial de Picks</div>", unsafe_allow_html=True)
            init_history()
            render_history()
        with tab5:
            def _ten_preview():
                with st.spinner("Calculando preview Tenis..."):
                    _prev = []
                    for _m in ten_matches:
                        if _m["state"]!="pre": continue
                        _tm = tennis_model(_m["rank1"],_m["rank2"],_m["odd_1"],_m["odd_2"])
                        _bp = max(_tm["p1"],_tm["p2"])
                        _fv = _m["p1"] if _tm["p1"]>=_tm["p2"] else _m["p2"]
                        if _bp >= 0.62:
                            _prev.append({"match":f"{_m['p1']} vs {_m['p2']}","tour":_m["tour"],"hora":_m["hora"],"fav":_fv,"prob":_bp})
                    _prev.sort(key=lambda x:-x["prob"])
                if not _prev:
                    st.markdown("<div style='color:#555;padding:10px'>Sin picks de tenis con prob>=62% ahora.</div>",unsafe_allow_html=True)
                for _p in _prev[:5]:
                    _cc = "#FFD700" if _p["prob"]>0.68 else "#00ff88"
                    st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-weight:700'>{_p['match']}</div><div style='color:#555;font-size:.8rem'>{_p['tour']} · {_p['hora']}</div><div style='color:#00ccff;font-weight:700;margin-top:4px'>🎾 {_p['fav']} gana</div></div><div style='text-align:right'><div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{_p['prob']*100:.1f}%</div></div></div>",unsafe_allow_html=True)
        with tab6:
            st.markdown("<div class='shdr'>📋 Historial de Picks</div>", unsafe_allow_html=True)
            init_history()
            render_history()
        with tab7:
            st.markdown("<div class='shdr'>🎓 Califica tu Pick — Einstein 🧠</div>", unsafe_allow_html=True)
            # Detector de anomalías Tenis
            _an_ten_pro = get_action_network_pro("","","tennis")
            render_fix_detector("tennis","Jugador 1","Jugador 2",{},{},{},
                               {"slug":"tennis"},an_data=_an_ten_pro)
            render_einstein_califica("ten")
        with tab8:
            render_resultados_tab()

    # ─── FÚTBOL ──────────────────────────────────────────
    else:
        tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial","🎓 Califica tu Pick","📊 Resultados"])

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
            for fi, fecha in enumerate(sorted(fecha_liga.keys())):
                total_p = sum(len(v) for v in fecha_liga[fecha].values())
                label = f"{fecha_label(fecha)}  ·  {total_p} partidos"
                with st.expander(label, expanded=(fi==0)):
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
                            # Skip finished games — they go to Resultados tab
                            if m["state"] == "post":
                                sh = m.get("score_h",-1); sa = m.get("score_a",-1)
                                score_f = f"{sh}-{sa}" if sh>=0 else "FT"
                                st.markdown(
                                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                                    f"padding:6px 14px;background:#0a0a1e;border-radius:8px;margin:2px 0;"
                                    f"border-left:3px solid #333;opacity:.6'>"
                                    f"<div style='font-size:.82rem;color:#555'>"
                                    f"✅ {m['home']} vs {m['away']}</div>"
                                    f"<div style='font-size:.9rem;font-weight:700;color:#555'>{score_f}</div>"
                                    f"</div>", unsafe_allow_html=True)
                                continue
                            live = m["state"] == "in"
                            sc   = f"🔴 {m['score_h']}-{m['score_a']}" if live else m["hora"]
                            conf_tag = f" · {m.get('_conf','')}" if m.get("_conf") else ""
                            lbl = f"{'🔴 ' if live else ''}{m['home']}  vs  {m['away']}   ·   {sc}{conf_tag}"
                            if st.button(lbl, key=f"b_{m['id']}", use_container_width=True):
                                st.session_state["sel"]  = m
                                st.session_state["view"] = "analisis"
                                st.rerun()
    
        # ─── TAB TRILAY ──────────────────────────────────────
        with tab2:
            st.markdown("<div class='shdr'>🎰 TRILAY — Top 3 de todos los deportes</div>",unsafe_allow_html=True)
            with st.spinner("Calculando TRILAY multi-deporte..."):
                # ── Recolectar TODOS los candidatos ──
                trilay_cands = []
                # Fútbol
                for t in compute_trilay(matches):
                    trilay_cands.append({"deporte":"⚽","label":f"{t['home']} vs {t['away']}",
                        "sub":f"{t['league']} · {t['hora']}","pick":t["best_m"],
                        "prob":t["best_p"],"extra":f"xG {t['hxg']:.1f}-{t['axg']:.1f}"})
                # NBA
                try:
                    for g in get_nba_cartelera()[:20]:
                        if g["state"]!="pre": continue
                        res = nba_ou_model(g["home_id"],g["away_id"],g["ou_line"])
                        bp = max(res["p_over"],res["p_under"])
                        bm = f"Over {res['line']}" if res["p_over"]>res["p_under"] else f"Under {res['line']}"
                        if bp >= 0.55:
                            trilay_cands.append({"deporte":"🏀","label":f"{g['away']} @ {g['home']}",
                                "sub":f"NBA · {g['hora']}","pick":bm,"prob":bp,
                                "extra":f"Proy: {res['proj']} pts"})
                except: pass
                # Tenis
                try:
                    for m in get_tennis_cartelera()[:30]:
                        if m["state"]!="pre": continue
                        tm = tennis_model(m["rank1"],m["rank2"],m["odd_1"],m["odd_2"])
                        bp = max(tm["p1"],tm["p2"])
                        fv = m["p1"] if tm["p1"]>=tm["p2"] else m["p2"]
                        if bp >= 0.58:
                            trilay_cands.append({"deporte":"🎾","label":f"{m['p1']} vs {m['p2']}",
                                "sub":f"{m['tour']} · {m['hora']}","pick":f"{fv} gana",
                                "prob":bp,"extra":tm["conf"]})
                except: pass
                trilay_cands.sort(key=lambda x:-x["prob"])

                # ── Generar 3 combinaciones distintas ──
                def make_trilay_combo(pool, exclude_labels):
                    avail = [c for c in pool if c["label"] not in exclude_labels]
                    if len(avail) < 3: return None
                    return avail[:3]

                used = set()
                combos = []
                for _ in range(3):
                    combo = make_trilay_combo(trilay_cands, used)
                    if not combo: break
                    combos.append(combo)
                    # For next combo, exclude the top pick and rotate
                    used.add(combo[0]["label"])

            def render_trilay_combo(combo, idx):
                pc = 1.0
                for t in combo: pc *= t["prob"]
                sports = len(set(t["deporte"] for t in combo))
                dep_colors = {"🏀":"#ff9500","⚽":"#aa00ff","🎾":"#00ccff"}
                st.markdown(
                    f"<div class='trilay-card' style='margin-bottom:16px'>"
                    f"<div style='font-size:.75rem;color:#aa00ff;font-weight:700;letter-spacing:.1em;margin-bottom:10px'>"
                    f"✦ COMBINACIÓN {idx} {'🔥' if idx==1 else ('⚡' if idx==2 else '💡')}</div>"
                    f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px'>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#aa00ff'>{pc*100:.1f}%</div><div class='mlbl'>Prob combinada</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{1/pc:.2f}x</div><div class='mlbl'>Cuota est.</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ccff'>{sports}</div><div class='mlbl'>Deportes</div></div>"
                    f"</div>", unsafe_allow_html=True)
                for i,t in enumerate(combo,1):
                    dc = dep_colors.get(t["deporte"],"#aaa")
                    st.markdown(
                        f"<div style='padding:10px 0;border-bottom:1px solid #1a1a40'>"
                        f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:2px'>"
                        f"<span style='background:{dc}22;border:1px solid {dc};border-radius:20px;"
                        f"padding:2px 10px;font-size:.72rem;font-weight:700;color:{dc}!important'>{t['deporte']}</span>"
                        f"<span style='font-weight:700;font-size:.9rem'>{i}. {t['label']}</span></div>"
                        f"<div style='color:#555;font-size:.8rem'>{t['sub']}</div>"
                        f"<div style='margin-top:5px'><span style='color:#aa00ff;font-weight:700'>👉 {t['pick']}</span>"
                        f"<span style='color:#666;margin-left:10px;font-size:.82rem'>{t['prob']*100:.1f}% · {t['extra']}</span></div>"
                        f"</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if combos:
                for idx, combo in enumerate(combos, 1):
                    render_trilay_combo(combo, idx)
            else:
                st.info("No hay suficientes picks hoy para el TRILAY. Vuelve más tarde.")

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
            st.markdown("<div class='shdr'>🎯 Mejores Picks del Día — Todos los deportes</div>",unsafe_allow_html=True)
            with st.spinner("Calculando picks multi-deporte..."):
                picks = []
                # ── FÚTBOL ──
                for m in matches[:50]:
                    if m["state"]!="pre": continue
                    try:
                        hf  = get_form(m["home_id"],m["slug"])
                        af  = get_form(m["away_id"],m["slug"])
                        hxg = max(0.35,avg([r["gf"] for r in hf])) if hf else xg_from_record(m["home_rec"],True)
                        axg = max(0.35,avg([r["gf"] for r in af])) if af else xg_from_record(m["away_rec"],False)
                        mc_ = mc50k(hxg,axg)
                        h2h = get_h2h(m["home_id"],m["away_id"],m["slug"],m["home"],m["away"])
                        h2s = h2h_stats(h2h,m["home"],m["away"])
                        dp  = diamond_engine(mc_,h2s,hf,af)
                        # ── Evalúa solo mercados válidos para DIAMANTE ──
                        opts=[]
                        # 1X2 — Ganador
                        if m["odd_h"]>1: opts.append(("🏠 "+m["home"][:15]+" gana", dp["ph"], m["odd_h"], dp["ph"]-(1/m["odd_h"])))
                        if m["odd_d"]>1: opts.append(("🤝 Empate",                  dp["pd"], m["odd_d"], dp["pd"]-(1/m["odd_d"])))
                        if m["odd_a"]>1: opts.append(("✈️ "+m["away"][:15]+" gana",  dp["pa"], m["odd_a"], dp["pa"]-(1/m["odd_a"])))
                        # Doble Chance
                        dc_1x = dp["ph"]+dp["pd"]; dc_x2 = dp["pd"]+dp["pa"]; dc_12 = dp["ph"]+dp["pa"]
                        opts.append(("🔵 DC: "+m["home"][:12]+" o Empate", dc_1x, 0, dc_1x-0.65))
                        opts.append(("🟣 DC: "+m["away"][:12]+" o Empate", dc_x2, 0, dc_x2-0.65))
                        opts.append(("🔴 DC: "+m["home"][:11]+" o "+m["away"][:11], dc_12, 0, dc_12-0.65))
                        # Over 2.5 y Over 3.5
                        opts.append(("⚽ Over 2.5", mc_["o25"], 0, mc_["o25"]-0.52))
                        opts.append(("⚽ Over 3.5", mc_["o35"], 0, mc_["o35"]-0.45))
                        # Ambos Anotan
                        opts.append(("⚡ Ambos Anotan (AA)", mc_["btts"], 0, mc_["btts"]-0.52))
                        # Ordenar por probabilidad — el pick es el de MAYOR prob con edge positivo
                        opts.sort(key=lambda x: (-x[1], -x[3]))
                        # Filtrar solo los que tienen edge positivo
                        valid = [o for o in opts if o[3] > 0.0]
                        best = valid[0] if valid else max(opts, key=lambda x: x[1])
                        if best[1] >= 0.55:  # prob mínima 55% para aparecer como pick
                            picks.append({"deporte":"⚽","home":m["home"],"away":m["away"],
                                         "league":m["league"],"hora":m["hora"],
                                         "pick":best[0],"prob":best[1],"odd":best[2],
                                         "edge":best[3],"conf":dp["conf"]})
                    except: continue
                # ── NBA ──
                try:
                    for g in get_nba_cartelera()[:20]:
                        if g["state"]!="pre": continue
                        res = nba_ou_model(g["home_id"],g["away_id"],g["ou_line"])
                        best_p = res["p_over"] if res["p_over"]>res["p_under"] else res["p_under"]
                        best_m = f"🏀 Over {res['line']}" if res["p_over"]>res["p_under"] else f"❄️ Under {res['line']}"
                        edge = best_p - 0.5
                        if edge > 0.04:
                            picks.append({"deporte":"🏀","home":g["home"],"away":g["away"],
                                         "league":"NBA","hora":g["hora"],
                                         "pick":best_m,"prob":best_p,"odd":0,
                                         "edge":edge,"conf":"💎 DIAMANTE" if best_p>0.65 else "🔥 ALTA"})
                except: pass
                # ── TENIS ──
                try:
                    for m in get_tennis_cartelera()[:30]:
                        if m["state"]!="pre": continue
                        tm = tennis_model(m["rank1"],m["rank2"],m["odd_1"],m["odd_2"])
                        best_p = max(tm["p1"],tm["p2"])
                        fav = m["p1"] if tm["p1"]>=tm["p2"] else m["p2"]
                        best_odd = m["odd_1"] if tm["p1"]>=tm["p2"] else m["odd_2"]
                        edge = tm["edge_1"] if tm["p1"]>=tm["p2"] else tm["edge_2"]
                        if best_p >= 0.58:
                            picks.append({"deporte":"🎾","home":m["p1"],"away":m["p2"],
                                         "league":f"{m['tour']} · {m['torneo']}","hora":m["hora"],
                                         "pick":f"🎾 {fav} gana","prob":best_p,
                                         "odd":best_odd,"edge":edge,"conf":tm["conf"]})
                except: pass

                picks.sort(key=lambda x:-x["prob"])

            if not picks:
                st.info("No se encontraron picks con valor hoy.")
            # Mostrar pick diamante primero
            diamantes = [p for p in picks if "DIAMANTE" in p["conf"]]
            if diamantes:
                d = diamantes[0]
                dep_color = "#ff9500" if d["deporte"]=="🏀" else ("#00ccff" if d["deporte"]=="🎾" else "#7c00ff")
                os_ = f"@{d['odd']}" if d["odd"]>1 else ""
                st.markdown(
                    f"<div class='diamond-hero'>"
                    f"<div style='font-size:.78rem;font-weight:700;color:#FFD700;letter-spacing:.14em;margin-bottom:10px'>"
                    f"✦ PICK DIAMANTE DEL DÍA {d['deporte']}</div>"
                    f"<div style='font-size:1.6rem;font-weight:900'>{d['home']} vs {d['away']}</div>"
                    f"<div style='color:#555;font-size:.85rem;margin:4px 0'>{d['league']} · {d['hora']}</div>"
                    f"<div style='font-size:1.2rem;font-weight:700;color:#FFD700;margin:10px 0'>"
                    f"👉 {d['pick']} {os_}</div>"
                    f"<div style='display:flex;gap:10px;flex-wrap:wrap'>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#7c00ff'>{d['prob']*100:.1f}%</div><div class='mlbl'>Probabilidad</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ff88'>+{d['edge']*100:.1f}%</div><div class='mlbl'>Edge</div></div>"
                    f"</div></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            for p in picks[:15]:
                dep_color = "#ff9500" if p["deporte"]=="🏀" else ("#00ccff" if p["deporte"]=="🎾" else "#7c00ff")
                os_ = f"@{p['odd']}" if p["odd"]>1 else ""
                st.markdown(
                    f"<div class='mrow' style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<div style='flex:1'>"
                    f"<div style='display:flex;align-items:center;gap:6px;margin-bottom:2px'>"
                    f"<span style='background:{dep_color}22;border:1px solid {dep_color};border-radius:12px;"
                    f"padding:1px 8px;font-size:.72rem;font-weight:700;color:{dep_color}!important'>{p['deporte']}</span>"
                    f"<span style='font-weight:700;font-size:.9rem'>{p['home']} vs {p['away']}</span></div>"
                    f"<div style='color:#555;font-size:.78rem'>{p['league']} · {p['hora']}</div>"
                    f"<div style='margin-top:4px;color:#00ccff;font-weight:700;font-size:.85rem'>{p['pick']} {os_}</div></div>"
                    f"<div style='text-align:right;min-width:80px'>"
                    f"<div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{p['prob']*100:.1f}%</div>"
                    f"<div style='font-size:.72rem;color:#555'>{p['conf']}</div></div></div>",
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
            col_a, col_b = st.columns([3,1])
            with col_a:
                st.markdown("<div style='color:#555;font-size:.82rem;margin-bottom:4px'>Abre un partido → click en 💾 Guardar Pick → marca ✅ o ❌ cuando termine</div>", unsafe_allow_html=True)
            with col_b:
                if st.button("🔄 Auto-actualizar", use_container_width=True, help="Revisa ESPN y actualiza resultados automáticamente"):
                    with st.spinner("Revisando resultados..."):
                        n = auto_track_picks()
                    if n > 0:
                        st.success(f"✅ {n} pick(s) actualizados")
                    else:
                        st.info("No hay resultados nuevos aún")
            render_history()
    
        # ─── TAB CALIFICA TU PICK ─────────────────────────────
        with tab7:
            st.markdown("<div class'shdr'>🎓 Califica tu Pick — Einstein 🧠</div>", unsafe_allow_html=True)
            render_einstein_califica("fut")
        with tab8:
            render_resultados_tab()

    
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
    aform = get_form(g["away_id"],g["slug"]); prog.progress(60,"📊 Calculando...")
    h2h   = []
    h2s   = {}
    hxg   = max(0.35,avg([r["gf"] for r in hform])) if hform else xg_from_record(g["home_rec"],True)
    axg   = max(0.35,avg([r["gf"] for r in aform])) if aform else xg_from_record(g["away_rec"],False)
    h2h   = get_h2h(g["home_id"],g["away_id"],g["slug"],g["home"],g["away"])
    h2s   = h2h_stats(h2h, g["home"], g["away"])
    mc    = ensemble_football(hxg, axg, h2s, hform, aform, g["home_id"], g["away_id"])
    dp    = diamond_engine(mc, h2s, hform, aform)
    pls   = smart_parlay(mc, dp, g["home"], g["away"])
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

    # ── JUGADA DIAMANTE — pick = mercado con mayor probabilidad ──
    _all_markets = [
        (f"🏠 {g['home'][:16]} gana",      dp["ph"],  g.get("odd_h",0)),
        ("🤝 Empate",                        dp["pd"],  g.get("odd_d",0)),
        (f"✈️ {g['away'][:16]} gana",        dp["pa"],  g.get("odd_a",0)),
        (f"🔵 DC: {g['home'][:12]} o Emp",   dp["ph"]+dp["pd"], 0),
        (f"🟣 DC: {g['away'][:12]} o Emp",   dp["pd"]+dp["pa"], 0),
        (f"🔴 DC: {g['home'][:10]} o {g['away'][:10]}", dp["ph"]+dp["pa"], 0),
        ("⚽ Over 2.5",                       mc["o25"],  0),
        ("⚽ Over 3.5",                       mc["o35"],  0),
        ("⚡ Ambos Anotan (AA)",              mc["btts"], 0),
    ]
    # El pick DIAMANTE = el mercado con probabilidad más alta
    main_mkt = max(_all_markets, key=lambda x: x[1])
    main_lbl, main_prob, main_odd = main_mkt

    # Badges de todos los mercados ordenados por prob
    _mkt_sorted = sorted(_all_markets, key=lambda x:-x[1])
    top3 = _mkt_sorted[:4]  # mostrar top 4 en la card

    mkt_badges = "".join(
        f"<div class='mbox' style='flex:1;min-width:90px'>"
        f"<div class='mval' style='color:{'#FFD700' if i==0 else ('#7c00ff' if i==1 else '#555')};font-size:{1.1 if i==0 else 0.9}rem'>"
        f"{v*100:.1f}%{'  ✦' if i==0 else ''}</div>"
        f"<div class='mlbl' style='font-size:.65rem'>{l[:20]}</div></div>"
        for i,(l,v,_) in enumerate(top3)
    )

    st.markdown(
        f"<div class='diamond-hero'>"
        f"<div style='font-size:.78rem;font-weight:700;color:#FFD700;letter-spacing:.14em;margin-bottom:10px'>"
        f"✦ JUGADA DIAMANTE — {dp['conf']} · Mayor probabilidad del partido</div>"
        f"<div style='font-size:2.4rem;font-weight:900;line-height:1.1;margin-bottom:8px'>{main_lbl}</div>"
        f"<div style='font-size:1.3rem;font-weight:700;color:#FFD700;margin-bottom:6px'>"
        f"{main_prob*100:.1f}% de probabilidad"
        + (f" · @{main_odd:.2f}" if main_odd>1 else "") + "</div>"
        f"<div style='font-size:.75rem;color:#888;margin-bottom:16px'>"
        f"Evaluados: 1X2 · Doble Chance · Over 2.5 · Over 3.5 · Ambos Anotan</div>"
        f"<div style='display:flex;gap:10px;flex-wrap:wrap'>{mkt_badges}</div>"
        f"<div style='margin-top:12px;padding-top:10px;border-top:1px solid #252550'>"
        f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:6px'>"
        f"<div style='text-align:center'><div style='font-size:.9rem;font-weight:700;color:#00ccff'>{mc.get('dc_ph',0):.1f}%</div><div style='font-size:.6rem;color:#555'>Dixon-Coles</div></div>"
        f"<div style='text-align:center'><div style='font-size:.9rem;font-weight:700;color:#aa00ff'>{mc.get('bvp_ph',0):.1f}%</div><div style='font-size:.6rem;color:#555'>Poisson BV</div></div>"
        f"<div style='text-align:center'><div style='font-size:.9rem;font-weight:700;color:#00ff88'>{mc.get('elo_ph',0):.1f}%</div><div style='font-size:.6rem;color:#555'>Elo Dinámico</div></div>"
        f"<div style='text-align:center'><div style='font-size:.9rem;font-weight:700;color:#FFD700'>{mc.get('h2h_ph',0):.1f}%</div><div style='font-size:.6rem;color:#555'>H2H</div></div>"
        f"</div><div style='font-size:.72rem;color:#555'>Consenso: <b>{mc.get('consensus','')}</b> · xG {hxg:.2f}/{axg:.2f} · Ensemble 4 modelos</div>"
        f"</div></div>",
        unsafe_allow_html=True)

    # ── VEREDICTO ACADÉMICO — semáforo ──
    v_html = veredicto_academico(mc, dp, g.get("odd_h",0), g.get("odd_a",0), g.get("odd_d",0), g["home"], g["away"], best_market=main_lbl, best_prob=main_prob, best_odd=main_odd)
    st.markdown(v_html, unsafe_allow_html=True)

    # ── GUARDAR PICK ──
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        if st.button(f"💾 Guardar Diamante: {main_lbl[:18]}", use_container_width=True, key="save_main"):
            add_pick(g, main_lbl, main_prob, main_odd)
            st.success("✅ Pick guardado en Historial")
    with sc2:
        if st.button(f"💾 Over 2.5 ({mc['o25']*100:.0f}%)", use_container_width=True, key="save_o25"):
            add_pick(g, "⚽ Over 2.5", mc["o25"], 0)
            st.success("✅ Pick guardado")
    with sc3:
        if st.button(f"💾 AA ({mc['btts']*100:.0f}%)", use_container_width=True, key="save_btts"):
            add_pick(g, "⚡ Ambos Anotan", mc["btts"], 0)
            st.success("✅ Pick guardado")

    # ══════════════════════════════════════════════════════════
    # VEREDICTO ACADÉMICO — Semáforo 🟢🟡🔴
    # ══════════════════════════════════════════════════════════
    v_html = veredicto_academico(mc, dp,
        g.get("odd_h",0), g.get("odd_a",0), g.get("odd_d",0),
        g["home"], g["away"],
        best_market=main_lbl, best_prob=main_prob, best_odd=main_odd)
    st.markdown(v_html, unsafe_allow_html=True)

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
                render_form_chart(form, tname, color)
            else:
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

    # ── ODDS COMPARISON ──
    with st.spinner("Buscando cuotas..."):
        real_odds = get_real_odds(g["home"], g["away"], g["slug"])
    render_odds_comparison(g["home"], g["away"], dp, mc, real_odds)
    # ── PRE-MATCH INTELLIGENCE BOT — Fútbol ──
    adj_dp, _was_adj = render_prematch_bot(
        sport="soccer", home=g["home"], away=g["away"],
        league_slug=g.get("slug",""),
        league_name=g.get("league",g.get("slug","Fútbol")),
        model_result=dp,
        hxg=g.get("hxg",1.3), axg=g.get("axg",1.0),
        hora_partido=g.get("hora","")
    )
    if _was_adj: dp = adj_dp  # modelo ajustado con bajas
    render_sharp_money(g["home"], g["away"], dp, mc, real_odds, g)
    # ── Fetch AN PRO data for fix detector ──
    _an_pro   = get_action_network_pro(g["home"], g["away"], "soccer")
    _sbr_fix  = get_sbr_public_betting(g["home"], g["away"], "soccer")
    _snaps    = _line_history.get(f"{g["home"][:8]}_{g["away"][:8]}", {}).get("snapshots",[])
    render_fix_detector("soccer", g["home"], g["away"], mc, dp, real_odds, g,
                        an_data=_an_pro, sbr_data=_sbr_fix, line_snapshots=_snaps)



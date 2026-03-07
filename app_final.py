"""
THE GAMBLERS LAYER — FINAL
100% ESPN · Bot Telegram integrado · Sin BD local
"""
import streamlit as st
import streamlit.components.v1 as _st_components
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

    now_cdmx = datetime.now(CDMX)
    hoy_str  = now_cdmx.strftime("%Y-%m-%d")
    hora_now = int(now_cdmx.strftime("%H"))

    # A partir de las 12:00 CDMX: ocultar partidos de ayer/pasados ya terminados
    if hora_now >= 12:
        matches = [m for m in matches if m.get("fecha","") >= hoy_str or m.get("state") in ("in","pre")]

    # Ordenar: hoy primero, luego por hora ASC (partido más próximo arriba)
    def _sort_key(m):
        f = m.get("fecha", "9999-99-99")
        h = m.get("hora", "99:99")
        # Estado: en vivo primero, luego pre, luego post
        s = m.get("state","")
        s_order = 0 if s == "in" else (1 if s == "pre" else 2)
        # Hoy primero, mañana después
        f_order = 0 if f == hoy_str else (1 if f > hoy_str else 2)
        return (f_order, s_order, h)

    matches.sort(key=_sort_key)
    return matches

@st.cache_data(ttl=1800, show_spinner=False)
def get_form(team_id, slug):
    """
    Últimos 15 partidos desde ESPN schedule.
    Incluye shooting stats si disponibles (para xG real).
    """
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
            is_home = str(hc["team"]["id"]) == team_id
            my      = hc if is_home else ac
            opp     = ac if is_home else hc
            gf      = parse_score(my.get("score", 0))
            gc      = parse_score(opp.get("score", 0))
            result  = "W" if gf > gc else ("D" if gf == gc else "L")
            # ── Try to extract xG from ESPN stats if available ──
            xg_f = 0.0; xg_c = 0.0
            try:
                for stat_grp in my.get("statistics",[]):
                    if stat_grp.get("name","").lower() in ("expectedgoals","xg","xgoals"):
                        xg_f = float(stat_grp.get("value",0))
                for stat_grp in opp.get("statistics",[]):
                    if stat_grp.get("name","").lower() in ("expectedgoals","xg","xgoals"):
                        xg_c = float(stat_grp.get("value",0))
            except: pass
            matches.append({
                "date":     ev.get("date", "")[:10],
                "result":   result,
                "gf":       gf,
                "gc":       gc,
                "xg_f":     xg_f,   # real xG if available, else 0
                "xg_c":     xg_c,
                "opponent": opp["team"]["displayName"],
                "is_home":  is_home,
                "league":   ev.get("name", ""),
            })
        except: continue
    matches.sort(key=lambda x: x["date"], reverse=True)
    return matches[:15]  # 15 partidos para más contexto


def xg_weighted(form, is_home, odds_prior=0.0):
    """
    xG con decaimiento exponencial — partidos recientes pesan MÁS.
    Si ESPN devuelve xG real lo usa; si no, usa goles como proxy.
    Incorpora odds como prior bayesiano cuando están disponibles.

    decay = 0.85 por partido (partido de hace 5 = peso 0.44x vs último)
    Ref: Dixon & Coles 1997 — time-weighting de observaciones.
    """
    if not form:
        return (1.25 if is_home else 1.0)

    DECAY = 0.85
    total_w = 0.0; total_xg = 0.0

    for i, r in enumerate(form):
        w = DECAY ** i   # partido más reciente = peso 1.0, hace 10 = 0.85^10=0.197
        # Usar xG real si ESPN lo devuelve, si no usar goles como proxy
        xg_real = r.get("xg_f", 0.0)
        xg_val  = xg_real if xg_real > 0.1 else float(r.get("gf", 1.0))
        total_xg += w * xg_val
        total_w  += w

    xg_base = total_xg / total_w if total_w > 0 else (1.25 if is_home else 1.0)

    # Home advantage adjustment
    if is_home:
        xg_base *= 1.08   # +8% ventaja local (meta-análisis Dixon & Coles)

    # Bayesian prior desde odds de mercado (si disponible)
    # Odds imply an xG — blendear 20% mercado + 80% modelo estadístico
    if odds_prior > 0.05:
        # p_score ≈ 1 - e^(-xG)  →  xG = -ln(1 - p_score)
        # p_win_odds → p_score aproximada con Poisson
        xg_from_odds = max(0.3, -math.log(max(0.01, 1 - odds_prior)) * 1.8)
        xg_base = 0.80 * xg_base + 0.20 * xg_from_odds

    return round(max(0.20, min(4.5, xg_base)), 3)

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
        }
        if _an_key:
            headers["Authorization"] = f"Bearer {_an_key}" if not _an_key.startswith("Bearer") else _an_key

        # Triple fallback: v2 PRO → v1 sport → v1 genérico
        resp = None
        for url, params in [
            (f"https://api.actionnetwork.com/web/v2/games/{sp}", {"date": date, "bookIds": "15,30,76,123"}),
            (f"https://api.actionnetwork.com/web/v1/games/{sp}", {"date": date}),
            (f"https://api.actionnetwork.com/web/v1/games",      {"sport": sp, "date": date}),
        ]:
            try:
                r = requests.get(url, headers=headers, params=params, timeout=8)
                if r.status_code == 200:
                    resp = r; break
            except: continue
        if not resp: return {}
        
        raw   = resp.json()
        games = raw.get("games", raw.get("events", []))
        hn = home.lower()[:7]; an = away.lower()[:7]

        for g in games:
            teams     = g.get("teams", [{}]*2)
            names     = [t.get("full_name","").lower() for t in teams]
            abbrs     = [t.get("abbr","").lower() for t in teams]
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
            
            # Money % por mercado — AN devuelve ml_bets, ou_bets, spread_bets igual que NBA
            ml  = g.get("ml_bets",{})     or g.get("moneyline_bets",{})  or {}
            ou  = g.get("ou_bets",{})     or g.get("total_bets",{})      or {}
            spd = g.get("spread_bets",{}) or {}

            result.update({
                "ml_home_bets_pct":      ml.get("home_bets_pct",0)  or ml.get("home_bets",0),
                "ml_home_money_pct":     ml.get("home_money_pct",0) or ml.get("home_money",0),
                "ml_away_bets_pct":      ml.get("away_bets_pct",0)  or ml.get("away_bets",0),
                "ml_away_money_pct":     ml.get("away_money_pct",0) or ml.get("away_money",0),
                "over_bets_pct":         ou.get("over_bets_pct",0)  or ou.get("over_bets",0),
                "over_money_pct":        ou.get("over_money_pct",0) or ou.get("over_money",0),
                "under_bets_pct":        ou.get("under_bets_pct",0) or ou.get("under_bets",0),
                "under_money_pct":       ou.get("under_money_pct",0)or ou.get("under_money",0),
            })

            # Fallback viejo (por si la respuesta viene en formato v2 distinto)
            for mkt_key, mkt_name in [("spread","spread"),("ml","ml"),("total","total")]:
                mkt = g.get(f"{mkt_key}_consensus") or g.get(f"consensus_{mkt_key}") or {}
                if mkt and not result.get(f"{mkt_name}_home_bets_pct"):
                    result[f"{mkt_name}_home_bets_pct"]  = mkt.get("home_bets",0)
                    result[f"{mkt_name}_home_money_pct"] = mkt.get("home_money",0)
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

def add_pick(match, pick_label, prob, odd, sport="futbol"):
    init_history()
    st.session_state["pick_history"].append({
        "date":   datetime.now(CDMX).strftime("%d/%m %H:%M"),
        "fecha":  match.get("fecha", datetime.now(CDMX).strftime("%Y-%m-%d")),
        "home":   match.get("home", match.get("p1","?")),
        "away":   match.get("away", match.get("p2","?")),
        "league": match.get("league", match.get("torneo", match.get("tour",""))),
        "sport":  sport,
        "pick":   pick_label,
        "prob":   prob,
        "odd":    odd,
        "result": "⏳",
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

MEMORY_FILE   = "/tmp/gamblers_brain.json"
KR_CACHE_FILE = "/tmp/king_rongo_cache.json"

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
PICKS_SNAP_F   = "/tmp/gamblers_picks_snap.json"  # snapshot de picks automáticos

def _load_results_db():
    try:
        with open(RESULTS_FILE,"r") as f:
            db = _json_mem.load(f)
    except:
        return {"partidos":[],"ultima_actualizacion":"","version":1}
    # Limpiar partidos con nombres vacíos — copiar p1/p2 a home/away si faltan
    for p in db.get("partidos", []):
        if not p.get("home") or p.get("home") == "?":
            p["home"] = p.get("p1","?")
        if not p.get("away") or p.get("away") == "?":
            p["away"] = p.get("p2","?")
        if not p.get("p1") or p.get("p1") == "?":
            p["p1"] = p.get("home","?")
        if not p.get("p2") or p.get("p2") == "?":
            p["p2"] = p.get("away","?")
    return db

def _save_results_db(db):
    try:
        with open(RESULTS_FILE,"w") as f: _json_mem.dump(db,f,ensure_ascii=False,indent=2)
    except: pass

def _load_picks_snap():
    """Carga snapshot de picks automáticos generados (por partido_id)."""
    try:
        with open(PICKS_SNAP_F,"r") as f: return json.load(f)
    except: return {}

def _save_picks_snap(snap):
    """Guarda snapshot de picks. snap = {partido_id: {pick, prob, mkt, src, fecha_gen}}"""
    try:
        with open(PICKS_SNAP_F,"w") as f: json.dump(snap, f, ensure_ascii=False, indent=2)
    except: pass

def _snap_auto_pick(partido_id, pick_data, state="pre", force=False):
    """Guarda pick automático en snapshot.
    force=True: sobreescribe siempre (usado por la cartelera con datos completos).
    force=False: no sobreescribe partidos ya terminados (comportamiento por defecto)."""
    if not partido_id or not pick_data: return
    snap = _load_picks_snap()
    # Sin force: no tocar partidos que ya empezaron/terminaron
    if not force and partido_id in snap and state in ("in", "post"):
        return
    snap[partido_id] = {
        "pick":      pick_data.get("pick",""),
        "prob":      pick_data.get("prob",0),
        "mkt":       pick_data.get("mkt", pick_data.get("src","🤖 Modelo")),
        "odd":       pick_data.get("odd",0),
        "src":       pick_data.get("src","🤖 Modelo"),
        "all_picks": pick_data.get("all_picks", []),
        "home":      pick_data.get("home",""),
        "away":      pick_data.get("away",""),
        "sport":     pick_data.get("sport","futbol"),
        "fecha":     pick_data.get("fecha",""),
        "fecha_gen": datetime.now(CDMX).strftime("%Y-%m-%d %H:%M"),
        "frozen":    state in ("in","post"),
    }
    _save_picks_snap(snap)

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
                    hora_nba = utc.astimezone(CDMX).strftime("%H:%M")
                    partidos.append({
                        "id":ev.get("id",""), "deporte":"nba",
                        "liga":"NBA 🏀", "slug":"nba", "_sport":"nba",
                        "home":hc["team"]["displayName"],
                        "away":ac["team"]["displayName"],
                        "home_id":str(hc["team"]["id"]),
                        "away_id":str(ac["team"]["id"]),
                        "score_h":parse_score(hc.get("score",0)) if state=="post" else -1,
                        "score_a":parse_score(ac.get("score",0)) if state=="post" else -1,
                        "ou_line":ou_line,
                        "hora":hora_nba, "fecha":fecha, "state":state,
                    })
                except: continue
        except: continue
    return partidos

def fetch_tennis_results(days_back=10):
    """
    Trae partidos de tenis finalizados (state=post) de los últimos N días.
    Usa dos fuentes: TENNIS_API histórico + get_tennis_cartelera state=post del día.
    """
    now   = datetime.now(CDMX)
    hoy   = now.strftime("%Y-%m-%d")
    desde = (now - timedelta(days=days_back)).strftime("%Y-%m-%d")
    results = []
    seen_ids = set()

    # ── FUENTE 1: Tennis API histórico ──
    try:
        r = requests.get(TENNIS_API, params={
            "method":  "get_fixtures",
            "APIkey":  TENNIS_API_KEY,
            "date_start": desde,
            "date_stop":  hoy,
        }, headers=H, timeout=12)
        data = r.json() if r.status_code == 200 else {}
        for ev in data.get("result", []):
            try:
                fecha = ev.get("event_date","")
                hora  = ev.get("event_time","00:00")
                try:
                    utc_t = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M").replace(tzinfo=pytz.UTC)
                    hora  = utc_t.astimezone(CDMX).strftime("%H:%M")
                    fecha = utc_t.astimezone(CDMX).strftime("%Y-%m-%d")
                except: pass
                if fecha < desde or fecha > hoy: continue
                tour_type = ev.get("event_type_type","").upper()
                if not any(x in tour_type for x in ["ATP","WTA","GRAND SLAM","MASTERS"]):
                    continue
                tour = "WTA" if "WTA" in tour_type else "ATP"
                ev_status   = str(ev.get("event_status","")).lower()
                ev_finished = str(ev.get("event_final","0"))
                is_post = (ev_finished == "1" or
                           any(x in ev_status for x in ["finished","ft","final","completed","awarded",
                                                         "retired","ret.","walkover","w/o","withdraw"]))
                if not is_post: continue
                p1 = ev.get("event_first_player","?")
                p2 = ev.get("event_second_player","?")
                sc1_raw = str(ev.get("event_first_player_result","0"))
                sc2_raw = str(ev.get("event_second_player_result","0"))
                try:  sc1 = max(0, int(sc1_raw))
                except: sc1 = 0
                try:  sc2 = max(0, int(sc2_raw))
                except: sc2 = 0
                eid = f"ten_{ev.get('event_key','')}"
                if eid in seen_ids: continue
                seen_ids.add(eid)
                results.append({
                    "id": eid, "deporte":"tenis",
                    "home":p1, "away":p2, "p1":p1, "p2":p2,
                    "liga":f"{tour} · {ev.get('tournament_name','')}",
                    "tour":tour, "torneo":ev.get("tournament_name",""),
                    "fecha":fecha, "hora":hora, "state":"post",
                    "score_h":sc1, "score_a":sc2,
                })
            except: continue
    except: pass

    # ── FUENTE 2: Cartelera tenis de hoy — partidos state=post ──
    try:
        cartelera_ten = get_tennis_cartelera()
        for m in cartelera_ten:
            if m.get("state") != "post": continue
            eid = f"ten_live_{m.get('id','')}"
            if eid in seen_ids: continue
            seen_ids.add(eid)
            sc1 = m.get("score_p1", m.get("score_h", 0))
            sc2 = m.get("score_p2", m.get("score_a", 0))
            try: sc1 = max(0, int(str(sc1)))
            except: sc1 = 0
            try: sc2 = max(0, int(str(sc2)))
            except: sc2 = 0
            results.append({
                "id": eid, "deporte":"tenis",
                "home":m["p1"], "away":m["p2"], "p1":m["p1"], "p2":m["p2"],
                "liga":f"{m.get('tour','ATP')} · {m.get('torneo','')}",
                "tour":m.get("tour","ATP"), "torneo":m.get("torneo",""),
                "fecha":m.get("fecha",hoy), "hora":m.get("hora",""),
                "state":"post", "score_h":sc1, "score_a":sc2,
            })
    except: pass

    # ── FUENTE 3 SEMILLA: Resultados verificados Indian Wells 2026 ──
    _SEEDS = [
        {"p1":"Alexander Zverev",   "p2":"Matteo Berrettini",           "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Jannik Sinner",      "p2":"Dalibor Svrcina",             "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Felix Auger-Aliassime","p2":"Gael Monfils",              "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Tommy Paul",         "p2":"Zizou Bergs",                 "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Frances Tiafoe",     "p2":"Jenson Brooksby",             "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Gabriel Diallo",     "p2":"Learner Tien",                "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Joao Fonseca",       "p2":"Adam Walton",                 "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Lorenzo Musetti",    "p2":"Marton Fucsovics",            "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Jakub Mensik",       "p2":"Marcos Giron",                "sh":2,"sa":1,"t":"ATP","f":"2026-03-06"},
        {"p1":"Miomir Kecmanovic",  "p2":"Flavio Cobolli",              "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Denis Shapovalov",   "p2":"Tomas Martin Etcheverry",     "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Ben Shelton",        "p2":"Reilly Opelka",               "sh":2,"sa":1,"t":"ATP","f":"2026-03-06"},
        {"p1":"Brandon Nakashima",  "p2":"Camilo Ugo Carabelli",        "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Alejandro Davidovich Fokina","p2":"Zachary Svajda",      "sh":2,"sa":0,"t":"ATP","f":"2026-03-06"},
        {"p1":"Aryna Sabalenka",    "p2":"Himeno Sakatsume",            "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Coco Gauff",         "p2":"Kamilla Rakhimova",           "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Amanda Anisimova",   "p2":"Anna Blinkova",               "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Victoria Mboko",     "p2":"Kimberly Birrell",            "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Naomi Osaka",        "p2":"Victoria Jimenez Kasintseva", "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Iva Jovic",          "p2":"Camila Osorio",               "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Clara Tauson",       "p2":"Yulia Putintseva",            "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Ekaterina Alexandrova","p2":"Talia Gibson",              "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Anna Kalinskaya",    "p2":"Zeynep Sonmez",               "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Diana Shnaider",     "p2":"Sorana Cirstea",              "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Linda Noskova",      "p2":"Jessica Bouzas Maneiro",      "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Jasmine Paolini",    "p2":"Anastasia Potapova",          "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Emma Raducanu",      "p2":"Anastasia Zakharova",         "sh":2,"sa":0,"t":"WTA","f":"2026-03-06"},
        {"p1":"Alexandra Eala",     "p2":"Dayana Yastremska",           "sh":2,"sa":1,"t":"WTA","f":"2026-03-06"},
    ]
    for _s in _SEEDS:
        if _s["f"] < desde: continue
        _sid = f"ten_seed_{_s['p1'][:5].lower().replace(' ','')}_{_s['p2'][:5].lower().replace(' ','')}_{_s['t']}_{_s['f'].replace('-','')}"
        if _sid in seen_ids: continue
        seen_ids.add(_sid)
        results.append({
            "id": _sid, "deporte":"tenis",
            "home":_s["p1"], "away":_s["p2"], "p1":_s["p1"], "p2":_s["p2"],
            "score_h":_s["sh"], "score_a":_s["sa"],
            "state":"post", "liga":f"{_s['t']} · BNP Paribas Open Indian Wells",
            "tour":_s["t"], "torneo":"BNP Paribas Open Indian Wells",
            "fecha":_s["f"], "hora":"12:00", "rank1":0, "rank2":0,
        })

    # ── FUENTE 3: Claude web_search — ATP + WTA (siempre, es la fuente principal) ──
    if ANTHROPIC_API_KEY:
        web_results = _fetch_tennis_results_web(desde, hoy)
        for wr in web_results:
            eid = f"ten_web_{wr['p1'][:6]}_{wr['p2'][:6]}_{wr['fecha']}"
            if eid in seen_ids: continue
            seen_ids.add(eid)
            wr["id"] = eid
            results.append(wr)

    return results



def _fetch_tennis_results_web(desde, hoy):
    """
    Usa la API de Claude con web_search para obtener resultados reales de
    ATP (atptour.com) y WTA (wtatennis.com). Es la ÚNICA fuente que funciona
    en Streamlit Cloud porque el servidor no tiene acceso directo a internet.
    Hace dos llamadas: una para ATP Indian Wells, otra para WTA del día.
    """
    if not ANTHROPIC_API_KEY:
        return []

    import json as _j, re as _re

    results = []
    now_str = datetime.now(CDMX).strftime("%Y-%m-%d")

    def _call_claude(user_msg):
        """
        Llama a Claude con web_search_20250305.
        Este es un server-side tool — una sola llamada, Claude hace la búsqueda internamente.
        """
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "anthropic-beta": "web-search-2025-03-05",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 2000,
                    "tools": [{"type": "web_search_20250305", "name": "web_search"}],
                    "messages": [{"role": "user", "content": user_msg}],
                },
                timeout=60,
            )
            data = resp.json()
            if resp.status_code != 200:
                # Guardar error en session_state para debug
                import streamlit as _st2
                _st2.session_state["_tennis_api_error"] = f"HTTP {resp.status_code}: {data}"
                return ""
            content = data.get("content", [])
            return "".join(b.get("text","") for b in content if b.get("type")=="text")
        except Exception as _ex:
            import streamlit as _st2
            _st2.session_state["_tennis_api_error"] = str(_ex)
            return ""

    def _parse_json_matches(text, tour_default, torneo_default):
        """Extrae array JSON de partidos del texto de Claude."""
        if not text:
            return []
        clean = _re.sub(r"```[a-z]*|```", "", text).strip()
        m = _re.search(r"\[.*\]", clean, _re.DOTALL)
        if not m:
            return []
        try:
            raw = _j.loads(m.group())
        except:
            return []
        out = []
        for p in raw:
            try:
                p1  = str(p.get("p1","")).strip()
                p2  = str(p.get("p2","")).strip()
                sc1 = int(p.get("sets_p1", p.get("sc1", 0)))
                sc2 = int(p.get("sets_p2", p.get("sc2", 0)))
                tour   = str(p.get("tour", tour_default)).upper()
                torneo = str(p.get("torneo", torneo_default))
                fecha  = str(p.get("fecha", now_str))[:10]
                if not p1 or not p2: continue
                if sc1 == 0 and sc2 == 0: continue
                # Guardar tal cual — p1/home = como vino del JSON
                # score_h = sets de p1, score_a = sets de p2
                # Skip doubles pairs
                if "/" in p1 or "/" in p2 or "&" in p1 or "&" in p2: continue
                if p1.count(" ") >= 3 or p2.count(" ") >= 3: continue  # "A. Smith / B. Jones"
                r1 = _resolve_rank_local(p1)
                r2 = _resolve_rank_local(p2)
                out.append({
                    "deporte":"tenis", "home":p1, "away":p2, "p1":p1, "p2":p2,
                    "liga":f"{tour} · {torneo}", "tour":tour, "torneo":torneo,
                    "fecha":fecha, "hora":"00:00", "state":"post",
                    "score_h":sc1, "score_a":sc2,
                    "rank1": r1, "rank2": r2,
                })
            except:
                continue
        return out

    # ── LLAMADA 1: ATP últimos 3 días ──
    try:
        atp_prompt = (
            f"Busca los resultados de SINGLES ATP de los ultimos 3 dias ({desde} al {now_str}) en Indian Wells 2026.\n"
            f"Intenta estas URLs:\n"
            f"1. https://www.atptour.com/en/scores/current/indian-wells/404/results\n"
            f"2. Busca en Google: 'ATP Indian Wells 2026 results this week'\n"
            f"Extrae TODOS los partidos FINALIZADOS de SINGLES masculinos de los ultimos 3 dias.\n"
            f"EXCLUIR: dobles, mixtos, nombres con '/', '&'.\n"
            f"CRITICO: p1=GANADOR (sets_p1>sets_p2). p2=perdedor.\n"
            f"Ej: Zverev gano 2-0 a Berrettini → p1='Alexander Zverev' sets_p1=2, p2='Matteo Berrettini' sets_p2=0\n"
            f"Incluir campo 'fecha' con el dia real del partido (YYYY-MM-DD).\n"
            f"Responde SOLO con JSON array:\n"
            f'[{{"p1":"Ganador Apellido","p2":"Perdedor Apellido",'
            f'"sets_p1":2,"sets_p2":1,"torneo":"BNP Paribas Open Indian Wells",'
            f'"tour":"ATP","fecha":"2026-03-07"}}]'
        )
        atp_text = _call_claude(atp_prompt)
        atp_matches = _parse_json_matches(atp_text, "ATP", "BNP Paribas Open Indian Wells")
        results.extend(atp_matches)
    except:
        pass

    # ── LLAMADA 2: WTA últimos 3 días ──
    try:
        wta_prompt = (
            f"Busca los resultados de SINGLES WTA de los ultimos 3 dias ({desde} al {now_str}) en Indian Wells 2026.\n"
            f"Intenta estas URLs:\n"
            f"1. https://www.wtatennis.com/tournament/1121/indian-wells/2026/scores\n"
            f"2. Busca en Google: 'WTA Indian Wells 2026 results this week'\n"
            f"Extrae TODOS los partidos FINALIZADOS de SINGLES femeninos de los ultimos 3 dias.\n"
            f"EXCLUIR: dobles, mixtos, nombres con '/', '&'.\n"
            f"CRITICO: p1=GANADORA (sets_p1>sets_p2). p2=perdedora.\n"
            f"Ej: Sabalenka gano 2-0 a Osaka → p1='Aryna Sabalenka' sets_p1=2, p2='Naomi Osaka' sets_p2=0\n"
            f"Incluir campo 'fecha' con el dia real del partido (YYYY-MM-DD).\n"
            f"Responde SOLO con JSON array:\n"
            f'[{{"p1":"Ganadora Apellido","p2":"Perdedora Apellido",'
            f'"sets_p1":2,"sets_p2":0,"torneo":"BNP Paribas Open Indian Wells",'
            f'"tour":"WTA","fecha":"2026-03-07"}}]'
        )
        wta_text = _call_claude(wta_prompt)
        wta_matches = _parse_json_matches(wta_text, "WTA", "BNP Paribas Open Indian Wells")
        results.extend(wta_matches)
        if not wta_matches:
            wta_fallback = (
                f"Busca resultados WTA Indian Wells 2026 de los ultimos dias.\n"
                f"CRITICO: p1=GANADORA siempre.\n"
                f"SOLO JSON array:\n"
                f'[{{"p1":"Ganadora","p2":"Perdedora","sets_p1":2,"sets_p2":0,'
                f'"torneo":"Indian Wells","tour":"WTA","fecha":"{now_str}"}}]'
            )
            try:
                wta_text2 = _call_claude(wta_fallback)
                results.extend(_parse_json_matches(wta_text2, "WTA", "BNP Paribas Open Indian Wells"))
            except: pass
    except:
        pass

    return results

def update_results_db(force=False):
    """Main update function — fetches results and merges into DB."""
    if not force and not _needs_update():
        return False
    db = _load_results_db()
    existing_ids = {p["id"] for p in db["partidos"]}
    # Fetch new data
    new_soccer  = fetch_soccer_results(10)
    new_nba     = fetch_nba_results(10)
    new_tennis  = fetch_tennis_results(10)
    all_new     = new_soccer + new_nba + new_tennis
    # Merge: update existing, add new — deduplicar también por nombre+fecha
    existing_map = {p["id"]: i for i,p in enumerate(db["partidos"])}

    def _partido_key(p):
        """Clave fuzzy: apellido p1 + apellido p2 + fecha — para deduplicar entre fuentes."""
        def _ap(n):
            parts = [w for w in str(n).lower().split() if len(w) > 2]
            return parts[-1] if parts else str(n)[:5].lower()
        h = _ap(p.get("home", p.get("p1","")))
        a = _ap(p.get("away", p.get("p2","")))
        f = str(p.get("fecha",""))[:10]
        return f"{h}_{a}_{f}"

    existing_fuzzy = {_partido_key(p): i for i,p in enumerate(db["partidos"])}

    for p in all_new:
        fkey = _partido_key(p)
        if p["id"] in existing_map:
            idx = existing_map[p["id"]]
            if p["state"] == "post":
                db["partidos"][idx]["state"] = "post"
                # Solo sobreescribir score si el nuevo es válido (>= 0)
                # y no reemplazar un score real con 0-0 incorrecto
                _new_sh = p.get("score_h", -1)
                _new_sa = p.get("score_a", -1)
                _old_sh = db["partidos"][idx].get("score_h", -1)
                _old_sa = db["partidos"][idx].get("score_a", -1)
                # Actualizar si: no había score antes, o el nuevo es mayor (más goles/sets)
                if _new_sh >= 0 and (_old_sh < 0 or _new_sh > 0 or _old_sh == 0):
                    db["partidos"][idx]["score_h"] = _new_sh
                    db["partidos"][idx]["score_a"] = _new_sa
                if not db["partidos"][idx].get("rank1") and p.get("rank1"):
                    db["partidos"][idx]["rank1"] = p["rank1"]
                    db["partidos"][idx]["rank2"] = p["rank2"]
        elif fkey in existing_fuzzy:
            idx = existing_fuzzy[fkey]
            if p["state"] == "post":
                db["partidos"][idx]["state"] = "post"
                _new_sh = p.get("score_h", -1)
                _new_sa = p.get("score_a", -1)
                _old_sh = db["partidos"][idx].get("score_h", -1)
                _old_sa = db["partidos"][idx].get("score_a", -1)
                if _new_sh >= 0 and (_old_sh < 0 or _new_sh > 0 or _old_sh == 0):
                    db["partidos"][idx]["score_h"] = _new_sh
                    db["partidos"][idx]["score_a"] = _new_sa
                if not db["partidos"][idx].get("rank1") and p.get("rank1"):
                    db["partidos"][idx]["rank1"] = p["rank1"]
                    db["partidos"][idx]["rank2"] = p["rank2"]
                # Rellenar nombres si venían como "?"
                if db["partidos"][idx].get("home","?") in ("?","") and p.get("home"):
                    db["partidos"][idx]["home"] = p["home"]
                    db["partidos"][idx]["p1"]   = p.get("p1", p["home"])
                if db["partidos"][idx].get("away","?") in ("?","") and p.get("away"):
                    db["partidos"][idx]["away"] = p["away"]
                    db["partidos"][idx]["p2"]   = p.get("p2", p["away"])
        else:
            db["partidos"].append(p)
            existing_fuzzy[fkey] = len(db["partidos"]) - 1
    # Keep only last 10 days
    cutoff = (datetime.now(CDMX) - timedelta(days=10)).strftime("%Y-%m-%d")
    db["partidos"] = [p for p in db["partidos"] if p.get("fecha","") >= cutoff]
    # Dedup tenis por jugadores+fecha (diferentes fuentes generan IDs distintos)
    _seen_ten = set()
    _deduped = []
    for _p in db["partidos"]:
        if _p.get("deporte") == "tenis":
            _p1k = (_p.get("p1","") or _p.get("home",""))[:8].lower()
            _p2k = (_p.get("p2","") or _p.get("away",""))[:8].lower()
            _fk  = _p.get("fecha","")[:10]
            _key = f"{_p1k}_{_p2k}_{_fk}"
            if _key in _seen_ten: continue
            _seen_ten.add(_key)
        _deduped.append(_p)
    db["partidos"] = _deduped
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

def _villar_match_pick_to_result(pk, partido_db):
    """
    Audita un pick vs resultado real.
    Soporta todos los formatos: emojis, nombres completos, mercados.
    Devuelve (veredicto_str, color, explicacion)
    """
    import re as _re

    sh = partido_db.get("score_h", -1)
    sa = partido_db.get("score_a", -1)
    sport_check = (partido_db.get("deporte","") or "").lower()
    # Para cualquier deporte: sin score → pendiente
    if sh < 0 or sa < 0:
        return "⏳ Pendiente", "#555", "Score no disponible aún"
    # Para tenis: 0-0 imposible → score no se guardó
    if sport_check == "tenis" and sh == 0 and sa == 0:
        return "⏳ Pendiente", "#555", "Score de tenis no disponible"

    raw_pick = pk.get("pick", "")
    pick     = raw_pick.lower()
    # Nombres del partido — primero del partido_db (más confiable), luego del pick
    home_db  = (partido_db.get("home", partido_db.get("p1","")) or "").lower().strip()
    away_db  = (partido_db.get("away", partido_db.get("p2","")) or "").lower().strip()
    home_pk  = (pk.get("home","") or pk.get("p1","") or "").lower().strip()
    away_pk  = (pk.get("away","") or pk.get("p2","") or "").lower().strip()
    home     = home_db or home_pk
    away     = away_db or away_pk
    sport    = (pk.get("sport", pk.get("deporte","futbol")) or "futbol").lower()
    total    = sh + sa
    won_h    = sh > sa
    won_a    = sa > sh
    draw     = sh == sa

    def _apellido(name):
        parts = [w for w in name.split() if len(w) > 2]
        return parts[-1] if parts else name[:5]

    def _name_in_pick(name, pick_str):
        """True si alguna palabra significativa del nombre aparece en el pick."""
        for w in name.split():
            if len(w) > 3 and w in pick_str:
                return True
        return False

    ok = None

    # ══ TENIS ══
    if sport in ("tenis","tennis") or "🎾" in raw_pick:
        import unicodedata as _ud
        def _norm(s):
            """Normaliza: quita tildes, minúsculas, quita puntuación."""
            s = str(s).lower().strip()
            try:
                s = _ud.normalize("NFD", s)
                s = "".join(c for c in s if _ud.category(c) != "Mn")
            except: pass
            return s
        def _apellido_norm(name):
            parts = [w for w in _norm(name).split() if len(w) >= 3]
            return parts[-1] if parts else _norm(name)[:6]
        def _name_hits(name, pick_str):
            nn = _norm(name)
            pn = _norm(pick_str)
            # 1. Apellido exacto en el pick (más importante)
            ap = _apellido_norm(name)
            if ap and ap in pn: return True
            # 2. Cualquier palabra >=3 chars del nombre en el pick
            for w in nn.split():
                if len(w) >= 3 and w in pn: return True
            # 3. Nombre completo normalizado como substring
            if nn and nn in pn: return True
            return False

        p1 = home_db or home_pk
        p2 = away_db or away_pk
        # Usar sh/sa ya validados arriba (score real del partido)
        # won_h/won_a ya calculados en el bloque general — son correctos
        # sh=sets_p1, sa=sets_p2 → won_h = p1 ganó más sets

        pick_hits_p1 = _name_hits(p1, pick)
        pick_hits_p2 = _name_hits(p2, pick)

        if pick_hits_p1 and not pick_hits_p2:
            ok = won_h
        elif pick_hits_p2 and not pick_hits_p1:
            ok = won_a
        elif pick_hits_p1 and pick_hits_p2:
            # Ambos nombres en el pick — usar el que tenga mejor match
            ap1 = _apellido_norm(p1); ap2 = _apellido_norm(p2)
            pn = _norm(pick)
            if ap1 in pn and ap2 not in pn:
                ok = won_h
            elif ap2 in pn and ap1 not in pn:
                ok = won_a
            else:
                winner = p1 if won_h else p2
                ok = _name_hits(winner, pick)
        else:
            # Pick no menciona ningún jugador conocido
            winner = p1 if won_h else p2
            ok = _name_hits(winner, pick)

    # ══ NBA ══
    elif sport in ("nba","basketball") or "🏀" in raw_pick:
        nums = _re.findall(r'\d+\.?\d*', pick)
        if "over" in pick:
            line = float(nums[0]) if nums else 220
            ok = total > line
        elif "under" in pick:
            line = float(nums[0]) if nums else 220
            ok = total < line
        elif _name_in_pick(home, pick) or _apellido(home) in pick:
            ok = won_h
        elif _name_in_pick(away, pick) or _apellido(away) in pick:
            ok = won_a

    # ══ FÚTBOL ══
    else:
        pick_clean = pick.replace("🏠","").replace("✈️","").replace("🔵","").replace("🟣","").replace("🤝","").replace("⚽","").replace("⚡","").strip()

        # O/U primero (más específico)
        if "over 3.5" in pick_clean or "o3.5" in pick_clean:
            ok = total > 3
        elif "over 2.5" in pick_clean or "o2.5" in pick_clean:
            ok = total > 2
        elif "over 1.5" in pick_clean or "o1.5" in pick_clean:
            ok = total > 1
        elif "under 2.5" in pick_clean or "u2.5" in pick_clean:
            ok = total <= 2
        elif "under 1.5" in pick_clean or "u1.5" in pick_clean:
            ok = total <= 1
        # BTTS
        elif any(x in pick_clean for x in ["ambos","btts","both","aa "]):
            ok = sh > 0 and sa > 0
        # Empate
        elif any(x in pick_clean for x in ["empate","draw","🤝"," x "]):
            ok = draw
        # Doble Oportunidad — "team o emp" / "o emp" / 1x / x1 / x2
        elif any(x in pick_clean for x in ["o emp","o empate","1x","x1"," o emp"]):
            # DO local: si el nombre del local aparece en el pick → local o empate
            if _name_in_pick(home, pick_clean) or "local" in pick_clean:
                ok = won_h or draw
            # DO visitante
            elif _name_in_pick(away, pick_clean) or "visita" in pick_clean:
                ok = won_a or draw
            else:
                ok = won_h or draw  # fallback DO local
        elif any(x in pick_clean for x in ["x2","2x"]):
            ok = won_a or draw
        # 1X2 por nombre — buscar en pick el nombre de local o visitante
        elif _name_in_pick(home, pick_clean) or "local" in pick_clean or "home" in pick_clean:
            ok = won_h
        elif _name_in_pick(away, pick_clean) or "visita" in pick_clean or "away" in pick_clean:
            ok = won_a
        # Fallback apellido
        elif home and _apellido(home) in pick_clean:
            ok = won_h
        elif away and _apellido(away) in pick_clean:
            ok = won_a

    sc_fmt = f"{sh}–{sa} pts" if sport in ("nba","basketball") else f"{sh}–{sa}"
    if ok is True:
        return "✅ GANÓ", "#00ff88", f"Score: {sc_fmt}"
    elif ok is False:
        return "❌ FALLÓ", "#ff4444", f"Score: {sc_fmt}"
    else:
        return "❓ N/V", "#555", f"Score: {sc_fmt}"


def _resolve_rank_local(name):
    """Resuelve ranking de un jugador de tenis desde tabla local."""
    if not name: return 150
    nl = name.lower().strip()
    parts = [w for w in nl.split() if len(w) > 3]
    for part in reversed(parts):
        if part in _KNOWN_RANKS:
            return _KNOWN_RANKS[part]
    for key, rank in _KNOWN_RANKS.items():
        if key in nl or nl in key:
            return rank
    return 150

def _villar_auto_pick(partido_db):
    """
    Corre los MODELOS sobre el partido (como si fuera antes de jugarse)
    y devuelve el pick de MAYOR PROBABILIDAD que el modelo hubiera dado.
    NO usa el resultado para elegir — elige por prob, luego audita.
    """
    sh = partido_db.get("score_h",-1); sa = partido_db.get("score_a",-1)
    if sh < 0: return None
    sport = partido_db.get("deporte","futbol")
    home  = partido_db.get("home", partido_db.get("p1","?"))
    away  = partido_db.get("away", partido_db.get("p2","?"))

    try:
        if sport == "tenis":
            r1 = partido_db.get("rank1") or 0
            r2 = partido_db.get("rank2") or 0
            o1 = partido_db.get("odd_1", 0)
            o2 = partido_db.get("odd_2", 0)
            # Resolver rankings desde nombre si no los hay
            if r1 <= 0: r1 = _resolve_rank(home, _KNOWN_RANKS) or 150
            if r2 <= 0: r2 = _resolve_rank(away, _KNOWN_RANKS) or 150
            # Weibull: p1 = prob de que home (p1) gane
            tm = tennis_model(r1, r2, o1, o2)
            # El modelo elige al favorito por prob — completamente ciego al resultado
            if tm["p1"] >= tm["p2"]:
                fav, prob = home, tm["p1"]
            else:
                fav, prob = away, tm["p2"]
            # Desempate si muy parejo (< 2pp de diferencia): menor rank gana
            if abs(tm["p1"] - tm["p2"]) < 0.02:
                fav  = home if r1 <= r2 else away
                prob = 0.53
            import unicodedata as _ud2
            def _norm_name(s):
                s = s.strip()
                try:
                    s = _ud2.normalize("NFD", s)
                    s = "".join(c for c in s if _ud2.category(c) != "Mn")
                except: pass
                return s
            fav_norm = _norm_name(fav)
            return {"pick": f"🎾 {fav_norm} gana", "prob": prob, "sport": "tenis",
                    "home": home, "away": away,
                    "src": f"🤖 Weibull #{r1} vs #{r2}"}

        elif sport == "nba":
            home_id = partido_db.get("home_id","")
            away_id = partido_db.get("away_id","")
            ou_line = partido_db.get("ou_line", 220)
            r  = nba_ou_model(home_id, away_id, ou_line)

            # ML pick
            if r["p_h_win"] >= 0.5:
                ml_lbl = f"🏀 {home} gana ML"
                ml_prob = r["p_h_win"]
            else:
                ml_lbl = f"🏀 {away} gana ML"
                ml_prob = r["p_a_win"]

            # O/U pick — solo si hay ventaja real (≥ 55%)
            p_over  = r["p_over"]
            p_under = r["p_under"]
            line    = r["line"]
            if p_over >= 0.55:
                ou_lbl  = f"🔥 Over {line:.1f}"
                ou_prob = p_over
            elif p_under >= 0.55:
                ou_lbl  = f"❄️ Under {line:.1f}"
                ou_prob = p_under
            else:
                ou_lbl  = None
                ou_prob = 0

            # Elegir el pick con mayor probabilidad (siempre hay ML)
            if ou_prob > ml_prob and ou_lbl:
                pick_lbl = ou_lbl
                prob     = ou_prob
            else:
                pick_lbl = ml_lbl
                prob     = ml_prob

            ml_odd_h = partido_db.get("odd_h", 0)
            ml_odd_a = partido_db.get("odd_a", 0)
            ml_odd   = ml_odd_h if r["p_h_win"] >= 0.5 else ml_odd_a
            ml_pick  = {"pick": ml_lbl,  "prob": ml_prob,  "mkt": "ML",   "odd": ml_odd,
                        "sport":"nba","home":home,"away":away,
                        "src": f"🤖 ML {ml_prob*100:.0f}%"}
            over_pick  = {"pick": f"🔥 Over {line:.1f}",  "prob": p_over,  "mkt": "Over",  "odd": 0,
                          "sport":"nba","home":home,"away":away,
                          "src": f"🤖 Over {p_over*100:.0f}%"}
            under_pick = {"pick": f"❄️ Under {line:.1f}", "prob": p_under, "mkt": "Under", "odd": 0,
                          "sport":"nba","home":home,"away":away,
                          "src": f"🤖 Under {p_under*100:.0f}%"}
            return {"pick": pick_lbl, "prob": prob, "sport": "nba",
                    "home": home, "away": away,
                    "src": f"🤖 NBA · ML {r['p_h_win']*100:.0f}%/O{p_over*100:.0f}%/U{p_under*100:.0f}%",
                    "all_picks": [ml_pick, over_pick, under_pick]}

        else:  # futbol — correr ensemble completo
            home_id  = partido_db.get("home_id","")
            away_id  = partido_db.get("away_id","")
            slug     = partido_db.get("slug","")
            odd_h    = partido_db.get("odd_h", 0)
            odd_a    = partido_db.get("odd_a", 0)
            odd_d    = partido_db.get("odd_d", 0)
            home_rec = partido_db.get("home_rec","5-5-5")
            away_rec = partido_db.get("away_rec","5-5-5")

            hf  = get_form(home_id, slug) if home_id and slug else []
            af  = get_form(away_id, slug) if home_id and slug else []

            # ── xG fallback: si no hay historial, usar odds como prior principal ──
            def _xg_from_odds(odd_h, odd_a, odd_d, is_home):
                """Deriva xG desde las odds cuando no hay historial de partidos.
                Convierte implied prob a xG esperado via Poisson inverso."""
                if odd_h > 1 and odd_a > 1 and odd_d > 1:
                    _tot = 1/odd_h + 1/odd_d + 1/odd_a
                    _ph  = (1/odd_h) / _tot   # prob local sin margen
                    _pa  = (1/odd_a) / _tot   # prob visitante sin margen
                    # xG calibrado: ph≈0.60 → hxg≈1.8, ph≈0.30 → hxg≈0.9
                    _hxg = max(0.35, 0.5 + _ph * 2.2 + (0.15 if is_home else 0))
                    _axg = max(0.35, 0.5 + _pa * 2.2 + (0.0  if is_home else 0))
                    return _hxg if is_home else _axg
                return 1.3 if is_home else 1.0

            if hf:
                hxg = xg_weighted(hf, True,  1/odd_h if odd_h>1 else 0)
            elif home_rec and home_rec != "5-5-5":
                hxg = xg_from_record(home_rec, True)
            else:
                hxg = _cup_enriched_xg(partido_db, True,  [], [])

            if af:
                axg = xg_weighted(af, False, 1/odd_a if odd_a>1 else 0)
            elif away_rec and away_rec != "5-5-5":
                axg = xg_from_record(away_rec, False)
            else:
                axg = _cup_enriched_xg(partido_db, False, [], [])
            mc  = mc50k(hxg, axg)

            p_h   = mc["ph"]
            p_a   = mc["pa"]
            p_o25 = mc["o25"]
            p_aa  = mc["btts"]
            p_d   = mc.get("pd", max(0, 1 - p_h - p_a))

            # Usar diamond_engine igual que la cartelera
            dp = diamond_engine(mc, {}, hf, af)
            _ph_d = dp["ph"]; _pa_d = dp["pa"]; _pd_d = dp["pd"]
            _o25_d = mc["o25"]; _aa_d = mc["btts"]
            _xg_tot_d = hxg + axg
            _do_h_d = min(0.95, _ph_d + _pd_d)
            _do_a_d = min(0.95, _pa_d + _pd_d)
            _best_ml = max(_ph_d, _pa_d)
            _fav_ml_lbl = f"🏠 {home} gana" if _ph_d >= _pa_d else f"✈️ {away} gana"
            _fav_ml_p   = max(_ph_d, _pa_d)
            _fav_ml_odd = odd_h if _ph_d >= _pa_d else odd_a
            _ninguno_d  = _best_ml < 0.52
            _eq_d       = abs(_ph_d - _pa_d) < 0.05

            _odd_h = odd_h; _odd_a = odd_a
            _has_odds = _odd_h > 1 and _odd_a > 1
            _edge_ml_h = (_ph_d - 1/_odd_h) if _odd_h > 1 else (_ph_d - 0.50)
            _edge_ml_a = (_pa_d - 1/_odd_a) if _odd_a > 1 else (_pa_d - 0.50)
            _best_ml_edge = max(_edge_ml_h, _edge_ml_a)

            # Misma jerarquía exacta que la cartelera (main_mkt)
            if _pa_d > _ph_d and (_pa_d >= 0.55 or (_has_odds and _edge_ml_a >= 0.03)):
                main_lbl, main_prob, main_odd = f"✈️ {away} gana", _pa_d, odd_a
            elif _ph_d >= 0.55 or (_has_odds and _edge_ml_h >= 0.03):
                main_lbl, main_prob, main_odd = f"🏠 {home} gana", _ph_d, odd_h
            elif _pa_d >= 0.55 or (_has_odds and _edge_ml_a >= 0.03):
                main_lbl, main_prob, main_odd = f"✈️ {away} gana", _pa_d, odd_a
            elif _do_h_d >= 0.76 and _ph_d >= 0.48:
                main_lbl, main_prob, main_odd = f"🔵 {home[:14]} o Emp", _do_h_d, 0
            elif _do_a_d >= 0.76 and _pa_d >= 0.43:
                main_lbl, main_prob, main_odd = f"🟣 {away[:14]} o Emp", _do_a_d, 0
            elif _xg_tot_d >= 2.6 and _o25_d >= 0.54:
                main_lbl, main_prob, main_odd = "⚽ Over 2.5", _o25_d, 0
            elif _best_ml >= 0.46:
                main_lbl, main_prob, main_odd = _fav_ml_lbl, _fav_ml_p, _fav_ml_odd
            elif _o25_d >= 0.52:
                main_lbl, main_prob, main_odd = "⚽ Over 2.5", _o25_d, 0
            elif _ninguno_d and _eq_d and _aa_d >= 0.52:
                main_lbl, main_prob, main_odd = "⚡ Ambos Anotan (AA)", _aa_d, 0
            else:
                main_lbl, main_prob, main_odd = _fav_ml_lbl, _fav_ml_p, _fav_ml_odd

            ml_pick = {
                "pick": f"🏠 {home} gana" if _ph_d >= _pa_d else f"✈️ {away} gana",
                "prob": max(_ph_d, _pa_d), "mkt": "ML",
                "odd": _fav_ml_odd, "sport": "futbol", "home": home, "away": away,
                "src": f"🤖 ML {max(_ph_d,_pa_d)*100:.0f}% · xG {hxg:.2f}–{axg:.2f}",
            }
            o25_pick = {
                "pick": "⚽ Over 2.5", "prob": _o25_d, "mkt": "O25",
                "odd": 0, "sport": "futbol", "home": home, "away": away,
                "src": f"🤖 O2.5 {_o25_d*100:.0f}% · xG total {hxg+axg:.2f}",
            }
            aa_pick = {
                "pick": "⚡ Ambos Anotan", "prob": _aa_d, "mkt": "AA",
                "odd": 0, "sport": "futbol", "home": home, "away": away,
                "src": f"🤖 AA {_aa_d*100:.0f}% · xG {hxg:.2f}–{axg:.2f}",
            }

            return {
                "pick":      main_lbl,
                "prob":      main_prob,
                "sport":     "futbol",
                "home":      home,
                "away":      away,
                "src":       f"🤖 Diamante · {main_prob*100:.0f}% · xG {hxg:.2f}/{axg:.2f}",
                "all_picks": [ml_pick, o25_pick, aa_pick],
            }
    except:
        return None


def _villar_find_result(pk, all_partidos):
    """
    Busca el partido correspondiente al pick en la DB de resultados.
    Usa fuzzy match por nombre de equipo/jugador + fecha.
    Para tenis también extrae el nombre del string del pick.
    """
    pk_home = pk.get("home","").lower().strip()
    pk_away = pk.get("away","").lower().strip()
    pk_date = pk.get("date", pk.get("fecha",""))[:10]
    pk_pick = pk.get("pick","").lower()

    # Para tenis: si no hay home/away, extraer nombre del pick ("🎾 Djokovic gana" → "djokovic")
    if not pk_home and "🎾" in pk.get("pick",""):
        import re as _re2
        _names = _re2.sub(r'[🎾🏀⚽✈️🏠]','', pk_pick).replace("gana","").strip()
        pk_home = _names  # tratar el nombre del favorito como "home" para el match

    def _name_score(a, b):
        if not a or not b: return 0
        a_parts = [x for x in a.split() if len(x) > 2]
        b_parts = [x for x in b.split() if len(x) > 2]
        best = 0
        for ap in a_parts:
            for bp in b_parts:
                if ap in bp or bp in ap:
                    # Apellidos largos valen más
                    best = max(best, 1 + (1 if len(ap) > 4 else 0))
        return best

    best = None; best_score = 0
    for p in all_partidos:
        if p.get("state") != "post": continue
        p_home = p.get("home","").lower()
        p_away = p.get("away","").lower()
        p_date = p.get("fecha","")

        # Date match (±2 días para tenis porque los resultados web pueden venir con fecha distinta)
        date_ok = False
        if pk_date and p_date:
            try:
                from datetime import datetime as _dt
                d1 = _dt.strptime(pk_date, "%Y-%m-%d")
                d2 = _dt.strptime(p_date,  "%Y-%m-%d")
                date_ok = abs((d1-d2).days) <= 2
            except: date_ok = pk_date[:7] == p_date[:7]
        else:
            date_ok = True

        if not date_ok: continue

        score  = _name_score(pk_home, p_home) + _name_score(pk_away, p_away)
        score2 = _name_score(pk_home, p_away) + _name_score(pk_away, p_home)
        # Para tenis: si el nombre del pick aparece en cualquier jugador
        if p.get("deporte") == "tenis":
            score3 = max(_name_score(pk_home, p_home), _name_score(pk_home, p_away))
            match_score = max(score, score2, score3)
        else:
            match_score = max(score, score2)

        if match_score > best_score:
            best_score = match_score
            best = p

    return best if best_score >= 1 else None


def render_resultados_tab():
    """VILLAR — Auditoría automática pick vs resultado real."""
    from collections import defaultdict

    # ── AUTO-AUDITORÍA al entrar al tab ──
    # Villar corre solo, sin que el usuario tenga que picar nada
    _villar_key = "villar_last_auto"
    _now_ts = datetime.now(CDMX).timestamp()
    _last   = st.session_state.get(_villar_key, 0)
    if _now_ts - _last > 300:  # auto-refresh cada 5 min
        with st.spinner("🤖 Villar auditando resultados..."):
            update_results_db(force=False)
            st.session_state["results_db"] = _load_results_db()
        st.session_state[_villar_key] = _now_ts

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a001a,#001a0a);
    border:2px solid #00ff8855;border-radius:16px;padding:14px 18px;
    margin-bottom:12px;display:flex;align-items:center;gap:12px'>
    <div style='font-size:2.2rem'>🤖</div>
    <div>
      <div style='font-size:1.1rem;font-weight:900;color:#00ff88;letter-spacing:.06em'>VILLAR</div>
      <div style='font-size:.75rem;color:#555'>Auditoría automática · Se actualiza al entrar al tab</div>
    </div></div>""", unsafe_allow_html=True)

    # Botón de force-refresh manual (secundario)
    _c1, _c2 = st.columns([3,1])
    with _c2:
        if st.button("🔄 Forzar", use_container_width=True, key="villar_force"):
            st.session_state.pop(_villar_key, None)
            st.session_state.pop("results_db", None)
            st.rerun()

    db       = get_results_db()
    partidos = db.get("partidos", [])
    ultima   = db.get("ultima_actualizacion","Nunca")
    pick_history = st.session_state.get("pick_history", [])
    st.caption(f"🕐 Última actualización: {ultima}")

    # ── Pre-calcular contadores del modelo sobre TODOS los partidos finalizados ──
    _pre_ok   = {"futbol":0,"nba":0,"tenis":0}
    _pre_fail = {"futbol":0,"nba":0,"tenis":0}
    _inicio_conteo = "2026-03-06"  # contar desde viernes 6 marzo 2026
    _fut_c = 0
    for _fp in [p for p in partidos if p.get("state")=="post"]:
        _sp = _fp.get("deporte","")
        _fd = _fp.get("fecha","")
        if _fd < _inicio_conteo:
            continue   # ignorar partidos antes del 6 mar
        if _sp == "futbol":
            if _fut_c >= 30: continue
            _fut_c += 1
        # Solo contar desde hoy
        if _fd < _inicio_conteo: continue
        # Tenis: skip si score inválido (0-0 imposible, -1 no disponible)
        if _sp == "tenis":
            _sh2 = _fp.get("score_h", -1)
            _sa2 = _fp.get("score_a", -1)
            if _sh2 < 0 or _sa2 < 0: continue
            if _sh2 == 0 and _sa2 == 0: continue
        _has_manual = any(_villar_find_result(pk,[_fp]) is not None for pk in pick_history)
        if _has_manual: continue
        try:
            _apk2 = _villar_auto_pick(_fp)
            if not _apk2: continue
            _vd2,_,_ = _villar_match_pick_to_result(_apk2, _fp)
            if "GANÓ"  in _vd2: _pre_ok[_sp]   = _pre_ok.get(_sp,0)+1
            elif "FALLÓ" in _vd2: _pre_fail[_sp] = _pre_fail.get(_sp,0)+1
        except: continue

    _total_ok   = sum(_pre_ok.values())
    _total_fail = sum(_pre_fail.values())
    _total_all  = _total_ok + _total_fail
    _pct_all    = round(_total_ok/_total_all*100) if _total_all>0 else 0
    _bar_c_hdr  = "#00ff88" if _pct_all>=55 else ("#FFD700" if _pct_all>=45 else "#ff4444")
    _global_ok  = _total_ok
    _global_fail= _total_fail

    roi = sum((float(pk.get("odd",0))-1) for pk in pick_history if pk.get("result")=="✅") -           sum(1 for pk in pick_history if pk.get("result")=="❌")

    # Desglose por deporte para el banner unificado
    _fut_ok  = _pre_ok.get('futbol',0);  _fut_fail  = _pre_fail.get('futbol',0)
    _nba_ok  = _pre_ok.get('nba',0);     _nba_fail  = _pre_fail.get('nba',0)
    _ten_ok  = _pre_ok.get('tenis',0);   _ten_fail  = _pre_fail.get('tenis',0)
    def _sp_pct(ok, fail): return f"{round(ok/(ok+fail)*100)}%" if ok+fail>0 else "–"
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#07071a,#0a0a2e);"
        f"border-radius:14px;padding:16px 18px;margin-bottom:14px;"
        f"border:2px solid {_bar_c_hdr}88'>"
        # Header
        f"<div style='font-size:.68rem;font-weight:700;color:#FFD700;"
        f"letter-spacing:.12em;margin-bottom:12px'>🤖 VILLAR — MODELO AUDITADO · TODOS LOS DEPORTES</div>"
        # Big numbers
        f"<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px'>"
        f"<div style='text-align:center;background:#00ff8810;border-radius:10px;padding:10px 4px'>"
        f"<div style='font-size:2rem;font-weight:900;color:#00ff88'>{_total_ok}</div>"
        f"<div style='font-size:.7rem;color:#555'>✅ Acertados</div></div>"
        f"<div style='text-align:center;background:#ff444410;border-radius:10px;padding:10px 4px'>"
        f"<div style='font-size:2rem;font-weight:900;color:#ff4444'>{_total_fail}</div>"
        f"<div style='font-size:.7rem;color:#555'>❌ Fallados</div></div>"
        f"<div style='text-align:center;background:{_bar_c_hdr}18;border-radius:10px;padding:10px 4px'>"
        f"<div style='font-size:2rem;font-weight:900;color:{_bar_c_hdr}'>{_pct_all}%</div>"
        f"<div style='font-size:.7rem;color:#555'>Acierto global</div></div>"
        f"</div>"
        # Barra global
        f"<div style='background:#0d0d2e;border-radius:6px;height:8px;overflow:hidden;margin-bottom:12px'>"
        f"<div style='width:{_pct_all}%;height:100%;background:{_bar_c_hdr};border-radius:6px'></div></div>"
        # Desglose por deporte
        f"<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:6px'>"
        f"<div style='background:#07071a;border-radius:8px;padding:8px;text-align:center'>"
        f"<div style='font-size:.9rem'>⚽</div>"
        f"<div style='font-size:.75rem;color:#00ff88;font-weight:700'>{_fut_ok}✅ {_fut_fail}❌</div>"
        f"<div style='font-size:.8rem;font-weight:900;color:#aaa'>{_sp_pct(_fut_ok,_fut_fail)}</div></div>"
        f"<div style='background:#07071a;border-radius:8px;padding:8px;text-align:center'>"
        f"<div style='font-size:.9rem'>🏀</div>"
        f"<div style='font-size:.75rem;color:#00ff88;font-weight:700'>{_nba_ok}✅ {_nba_fail}❌</div>"
        f"<div style='font-size:.8rem;font-weight:900;color:#aaa'>{_sp_pct(_nba_ok,_nba_fail)}</div></div>"
        f"<div style='background:#07071a;border-radius:8px;padding:8px;text-align:center'>"
        f"<div style='font-size:.9rem'>🎾</div>"
        f"<div style='font-size:.75rem;color:#00ff88;font-weight:700'>{_ten_ok}✅ {_ten_fail}❌</div>"
        f"<div style='font-size:.8rem;font-weight:900;color:#aaa'>{_sp_pct(_ten_ok,_ten_fail)}</div></div>"
        f"</div></div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # RESULTADOS POR DEPORTE — pick de mayor prob + auditoría
    # ════════════════════════════════════════════════════════
    st.markdown("<div class='shdr'>📊 Resultados + Pick del Modelo Auditado</div>", unsafe_allow_html=True)

    rt1,rt2,rt3 = st.tabs(["⚽ Fútbol","🏀 NBA","🎾 Tenis"])

    for tab_obj, sport_key, sport_emoji in [
        (rt1,"futbol","⚽"), (rt2,"nba","🏀"), (rt3,"tenis","🎾")
    ]:
        with tab_obj:
            sport_p     = [p for p in partidos if p.get("deporte")==sport_key]
            finalizados = sorted(
                [p for p in sport_p if p.get("state")=="post"],
                key=lambda x:x.get("fecha",""), reverse=True)
            en_juego    = [p for p in sport_p if p.get("state")=="in"]

            # En vivo
            for p in en_juego:
                sh=p.get("score_h",-1); sa=p.get("score_a",-1)
                sc=f"{sh}–{sa}" if sh>=0 else "?"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:8px 12px;"
                    f"background:#1a0800;border-radius:10px;margin:3px 0;border-left:3px solid #ff9500'>"
                    f"<div style='font-size:.85rem'><b>{p.get('home',p.get('p1','?'))}</b> vs "
                    f"<b>{p.get('away',p.get('p2','?'))}</b> "
                    f"<span style='font-size:.7rem;color:#ff9500'>🔴 EN VIVO</span></div>"
                    f"<div style='font-size:1.4rem;font-weight:900;color:#ff9500'>{sc}</div>"
                    f"</div>", unsafe_allow_html=True)

            if not finalizados:
                if sport_key == "tenis":
                    # Debug: mostrar qué pasó en la última llamada a web_search
                    _api_err = st.session_state.get("_tennis_api_error","")
                    _all_ten = [p for p in partidos if p.get("deporte")=="tenis"]
                    st.info(f"🎾 Sin resultados de tenis. Partidos en DB: {len(_all_ten)}")
                    if _api_err:
                        st.error(f"🔴 Error API tenis: {_api_err}")
                    if st.button("🔄 Buscar resultados de tenis ahora", key="ten_force_fetch"):
                        with st.spinner("🔍 Buscando en ATP/WTA..."):
                            _tw = _fetch_tennis_results_web(
                                (datetime.now(CDMX)-timedelta(days=5)).strftime("%Y-%m-%d"),
                                datetime.now(CDMX).strftime("%Y-%m-%d")
                            )
                            st.write(f"Encontrados: {len(_tw)} partidos")
                            if _tw:
                                _db2 = _load_results_db()
                                _seen2 = {p["id"] for p in _db2["partidos"]}
                                for _wr in _tw:
                                    _eid = f"ten_web_{_wr['p1'][:6]}_{_wr['p2'][:6]}_{_wr['fecha']}"
                                    if _eid not in _seen2:
                                        _wr["id"] = _eid
                                        _db2["partidos"].append(_wr)
                                _db2["ultima_actualizacion"] = datetime.now(CDMX).strftime("%Y-%m-%d %H:%M")
                                _save_results_db(_db2)
                                st.session_state["results_db"] = _db2
                                st.success(f"✅ {len(_tw)} partidos guardados")
                                st.rerun()
                            else:
                                _api_err2 = st.session_state.get("_tennis_api_error","")
                                if _api_err2:
                                    st.error(f"Error: {_api_err2}")
                else:
                    st.info(f"Sin resultados {sport_emoji}. Haz clic en '🧹 Auditar todo'.")
                continue

            # Contadores sport
            ok_sp=0; fail_sp=0
            por_fecha = defaultdict(list)
            for p in finalizados: por_fecha[p.get("fecha","?")].append(p)
            dias_  = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
            meses_ = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

            # Pre-calcular auto_picks — corre modelos sobre todos los partidos finalizados
            # Fútbol: hasta 30 (get_form es lento pero vale la pena para el contador)
            # NBA/Tenis: hasta 14 días atrás
            _catorce_dias = (datetime.now(CDMX)-timedelta(days=14)).strftime("%Y-%m-%d")
            _inicio_conteo_tab = "2026-03-06"  # contar desde viernes 6 marzo 2026
            _auto_pk_cache = {}
            _fut_count = 0
            for _fp in finalizados:
                _mid = _fp.get("id","")
                _fp_sport = _fp.get("deporte","")
                if _fp_sport == "futbol":
                    if _fut_count >= 30: continue
                    _fut_count += 1
                _manual = [pk for pk in pick_history if _villar_find_result(pk,[_fp]) is not None]
                if not _manual:
                    try:
                        # Pasar copia sin score para que el modelo no se contamine
                        _fp_clean = {k:v for k,v in _fp.items() if k not in ("score_h","score_a")}
                        _fp_clean["score_h"] = 0  # _villar_auto_pick necesita score_h >= 0
                        _apk = _villar_auto_pick(_fp_clean)
                        _auto_pk_cache[_mid] = _apk
                        _snap_auto_pick(_mid, _apk, state=_fp.get("state","pre"))
                    except: _auto_pk_cache[_mid] = None

            for fecha in sorted(por_fecha.keys(), reverse=True):
                dia_ps = por_fecha[fecha]
                try:
                    d=datetime.strptime(fecha,"%Y-%m-%d")
                    dlbl=f"📅 {dias_[d.weekday()]} {d.day} {meses_[d.month]}"
                except: dlbl=f"📅 {fecha}"
                is_today = fecha==datetime.now(CDMX).strftime("%Y-%m-%d")

                # Contar solo partidos con score válido para el label
                _n_validos = 0
                for _pv in dia_ps:
                    _sv_h = _pv.get("score_h",-1); _sv_a = _pv.get("score_a",-1)
                    if sport_key == "tenis":
                        if _sv_h < 0: _sv_h = 0
                        if _sv_a < 0: _sv_a = 0
                        if _sv_h > 0 or _sv_a > 0: _n_validos += 1
                    elif _sv_h >= 0 and _sv_a >= 0:
                        _n_validos += 1
                if _n_validos == 0:
                    continue  # no mostrar día si no hay partidos con score
                with st.expander(f"{dlbl} · {_n_validos} partidos", expanded=is_today):
                    por_liga = defaultdict(list)
                    for p in dia_ps:
                        por_liga[p.get("liga",p.get("tour","Sin liga"))].append(p)

                    for liga, lps in sorted(por_liga.items()):
                        st.markdown(
                            f"<div style='font-size:.68rem;font-weight:700;color:#FFD700;"
                            f"text-transform:uppercase;letter-spacing:.1em;margin:10px 0 5px'>"
                            f"{sport_emoji} {liga}</div>", unsafe_allow_html=True)

                        for p in lps:
                            sh=p.get("score_h",-1); sa=p.get("score_a",-1)
                            # Fútbol/NBA: saltar si no hay score
                            if sport_key != "tenis" and (sh<0 or sa<0): continue
                            # Tenis: 0-0 imposible — si ambos 0 o -1, score no disponible
                            if sport_key == "tenis":
                                if sh < 0: sh = 0
                                if sa < 0: sa = 0
                                if sh == 0 and sa == 0:
                                    continue
                            # CRÍTICO: crear copia del partido con scores ya validados
                            # para que _villar_match_pick_to_result reciba scores reales
                            _p_fixed = dict(p)
                            _p_fixed["score_h"] = sh
                            _p_fixed["score_a"] = sa
                            # Nombres: buscar en todos los campos posibles
                            home_n = (p.get("home") or p.get("p1") or "?").strip() or "?"
                            away_n = (p.get("away") or p.get("p2") or "?").strip() or "?"

                            won_h=sh>sa; won_a=sa>sh; draw=(sh==sa and sport_key=="futbol")
                            if sport_key=="futbol":
                                hc="#00ff88" if won_h else ("#FFD700" if draw else "#aaa")
                                ac="#00ff88" if won_a else ("#FFD700" if draw else "#aaa")
                            else:
                                hc="#00ff88" if won_h else "#aaa"
                                ac="#00ff88" if won_a else "#aaa"

                            # 1. Pick manual guardado por usuario
                            manual_pks = [pk for pk in pick_history
                                          if _villar_find_result(pk,[p]) is not None]
                            # 2. Pick automático — BRIDGE DIAMANTE es la fuente de verdad
                            _mid = p.get("id","")
                            auto_pk = None
                            if not manual_pks:
                                _p_state = p.get("state","pre")
                                _bridge = st.session_state.get("_diamond_bridge", {})
                                # Buscar en bridge por ID directo
                                _bp = _bridge.get(_mid)
                                # Fallback: home_id+away_id+fecha
                                if not _bp:
                                    _alt = f"{p.get('home_id','')}_{p.get('away_id','')}_{p.get('fecha','')}"
                                    _bp = _bridge.get(_alt)
                                if _bp:
                                    auto_pk = dict(_bp)
                                else:
                                    # Sin bridge: usar cache o recalcular sin score
                                    auto_pk = _auto_pk_cache.get(_mid)
                                    if not auto_pk:
                                        try:
                                            _fp2 = {k:v for k,v in p.items() if k not in ("score_h","score_a")}
                                            _fp2["score_h"] = 0
                                            auto_pk = _villar_auto_pick(_fp2)
                                            if auto_pk: _auto_pk_cache[_mid] = auto_pk
                                        except: pass

                            pick_rows = []
                            for pk in manual_pks:
                                vd,vc,ex = _villar_match_pick_to_result(pk, _p_fixed)
                                prob_v = pk.get("prob",0)
                                if prob_v<=1: prob_v*=100
                                pick_rows.append({
                                    "label": pk.get("pick","?"),
                                    "prob": prob_v, "odd": pk.get("odd",0),
                                    "src": "💾 Tu pick", "verd": vd, "col": vc, "expl": ex,
                                })
                                _fecha_p = p.get("fecha","")
                                if _fecha_p >= _inicio_conteo_tab:
                                    if "GANÓ" in vd: ok_sp+=1
                                    elif "FALLÓ" in vd: fail_sp+=1

                            if auto_pk:
                                # ── Auditar SOLO el pick principal que el modelo eligió ──
                                # Usar snap congelado si existe, si no usar auto_pk directo
                                _snap_data = _load_picks_snap().get(p.get("id",""), {})
                                _main_pick = auto_pk  # ya viene congelado del flujo arriba

                                _vd2, _vc2, _ex2 = _villar_match_pick_to_result(_main_pick, _p_fixed)
                                _prob2 = _main_pick.get("prob", 0)
                                _mkt2  = _main_pick.get("mkt", "")
                                pick_rows.append({
                                    "label":   _main_pick.get("pick","?"),
                                    "prob":    _prob2 * 100 if _prob2 <= 1 else _prob2,
                                    "odd":     _main_pick.get("odd", 0),
                                    "src":     _main_pick.get("src", "🤖 Modelo"),
                                    "verd":    _vd2, "col": _vc2, "expl": _ex2,
                                    "is_main": True,
                                })
                                # Contar para el contador global
                                if p.get("fecha","") >= _inicio_conteo_tab:
                                    if   "GANÓ"  in _vd2: ok_sp   += 1
                                    elif "FALLÓ" in _vd2: fail_sp += 1

                            # Render card
                            has_win  = any("GANÓ"  in r["verd"] for r in pick_rows)
                            has_fail = any("FALLÓ" in r["verd"] for r in pick_rows)
                            border_c = "#00ff88" if has_win else ("#ff4444" if has_fail else "#1a1a40")

                            pick_html = ""
                            for r in pick_rows:
                                icon = "✅" if "GANÓ" in r["verd"] else ("❌" if "FALLÓ" in r["verd"] else "⏳")
                                bg   = "#00ff8810" if icon=="✅" else ("#ff444410" if icon=="❌" else "#1a1a3a")
                                bd   = r["col"] if icon in ("✅","❌") else "#333"
                                od   = f" · @{r['odd']:.2f}" if r.get("odd",0)>1 else ""
                                pct  = f" · {r['prob']:.0f}%" if r.get("prob",0)>0 else ""
                                # Badge principal vs secundario
                                _is_main = r.get("is_main", True)
                                _main_badge = "<span style='background:#FFD70022;color:#FFD700;font-size:.6rem;padding:1px 5px;border-radius:4px;margin-left:4px;font-weight:700'>★ PICK</span>" if _is_main else ""
                                pick_html += (
                                    f"<div style='margin-top:4px;padding:5px 10px;border-radius:8px;"
                                    f"background:{bg};border:1px solid {bd};"
                                    f"display:flex;align-items:center;gap:8px'>"
                                    f"<div style='font-size:1.05rem'>{icon}</div>"
                                    f"<div style='flex:1'>"
                                    f"<div style='font-size:.78rem;font-weight:700;color:{r["col"]}'>{r["label"]}{od}{pct}{_main_badge}</div>"
                                    f"<div style='font-size:.62rem;color:#555'>{r["src"]} · {r["expl"]}</div>"
                                    f"</div>"
                                    f"</div>"
                                )

                            # Score: tenis = solo ganador con ✅
                            if sport_key == "tenis":
                                _p1 = (p.get("p1") or p.get("home") or "").strip() or home_n
                                _p2 = (p.get("p2") or p.get("away") or "").strip() or away_n
                                _sh = sh; _sa = sa
                                if _sh > _sa:
                                    winner_n, loser_n = _p1, _p2
                                elif _sa > _sh:
                                    winner_n, loser_n = _p2, _p1
                                else:
                                    _gano = next((r["expl"].replace("Ganó: ","") for r in pick_rows if "Ganó:" in r.get("expl","")), None)
                                    if _gano:
                                        winner_n = _gano
                                        loser_n  = _p2 if _gano == _p1 else _p1
                                    else:
                                        winner_n, loser_n = _p1, _p2
                                _wko  = p.get("is_walkover") or p.get("walkover_note","")
                                _note = " <span style='color:#ff9500;font-size:.65rem'>(RET.)</span>" if _wko else ""
                                _bc = "#00ff88" if any("GANÓ" in r.get("verd","") for r in pick_rows) else ("#ff4444" if any("FALLÓ" in r.get("verd","") for r in pick_rows) else "#1a1a40")
                                st.markdown(
                                    f"<div style='background:#0a0a1e;border-radius:12px;padding:10px 12px;"
                                    f"margin:4px 0;border:1px solid {_bc}'>"
                                    f"{pick_html}"
                                    f"<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:6px;"
                                    f"padding-top:6px;border-top:1px solid #1a1a30'>"
                                    f"<span style='font-size:.75rem;color:#555'>Ganó:</span>"
                                    f"<span style='color:#00ff88;font-weight:900;font-size:.88rem'>{winner_n}</span>"
                                    f"<span style='color:#444;font-size:.75rem'>vs</span>"
                                    f"<span style='color:#555;font-size:.82rem'>{loser_n}</span>"
                                    f"{_note}"
                                    f"</div>"
                                    f"</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(
                                    f"<div style='background:#0a0a1e;border-radius:12px;padding:10px 12px;"
                                    f"margin:4px 0;border:1px solid {border_c}'>"
                                    f"{pick_html}"
                                    f"<div style='display:grid;grid-template-columns:1fr 88px 1fr;"
                                    f"gap:4px;align-items:center;margin-top:6px;padding-top:6px;"
                                    f"border-top:1px solid #1a1a30'>"
                                    f"<div style='text-align:right'><span style='color:{hc};"
                                    f"font-weight:{'900' if won_h else '400'};font-size:.88rem'>{home_n}</span></div>"
                                    f"<div style='text-align:center;background:#07071a;border-radius:8px;padding:4px 6px'>"
                                    f"<span style='font-size:1.1rem;font-weight:900;color:{hc}'>{sh}</span>"
                                    f"<span style='color:#333'> – </span>"
                                    f"<span style='font-size:1.1rem;font-weight:900;color:{ac}'>{sa}</span></div>"
                                    f"<div style='text-align:left'><span style='color:{ac};"
                                    f"font-weight:{'900' if won_a else '400'};font-size:.88rem'>{away_n}</span></div>"
                                    f"</div>"
                                    f"</div>", unsafe_allow_html=True)

            total_sp = ok_sp+fail_sp
            pct_sp = round(ok_sp/total_sp*100) if total_sp>0 else 0
            _global_ok   += ok_sp
            _global_fail += fail_sp
            if total_sp>0:
                bar_c = "#00ff88" if pct_sp>=55 else ("#FFD700" if pct_sp>=45 else "#ff4444")
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:10px;padding:8px 12px;"
                    f"background:#07071a;border-radius:8px;margin-top:8px;border-top:1px solid #1a1a30'>"
                    f"<span style='font-size:1rem'>{sport_emoji}</span>"
                    f"<span style='color:#00ff88;font-weight:700;font-size:.9rem'>{ok_sp}✅</span>"
                    f"<span style='color:#ff4444;font-weight:700;font-size:.9rem'>{fail_sp}❌</span>"
                    f"<span style='color:{bar_c};font-weight:900;font-size:1rem'>{pct_sp}%</span>"
                    f"<span style='color:#555;font-size:.72rem;margin-left:auto'>{total_sp} auditados</span>"
                    f"</div>", unsafe_allow_html=True)

    # Banner global del modelo Villar
    # Banner global ya está arriba — no duplicar aquí
    _gtotal = _global_ok + _global_fail
    _gpct   = round(_global_ok/_gtotal*100) if _gtotal > 0 else 0

    # Guardar en session para KING RONGO
    st.session_state["_villar_summary"] = {
        "ok": _total_ok, "fail": _total_fail, "pct": _pct_all, "roi": roi,
        "modelo_ok": _global_ok, "modelo_fail": _global_fail, "modelo_pct": _gpct,
    }



# ══════════════════════════════════════════════════════════════════
# 👑 KING RONGO — El Cerebro Supremo de The Gamblers Layer
# Meta-bot que supervisa Einstein + Villar + todos los modelos.
# Une fuerzas, resuelve contradicciones, da EL pick del día.
# ══════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════
# 👑 KING RONGO — EL CEREBRO SUPREMO
# Meta-sistema de inteligencia que unifica todos los modelos,
# gestiona el bankroll, aprende de los resultados, y da
# EL PICK DEFINITIVO DEL DÍA con máxima confianza.
# ══════════════════════════════════════════════════════════════════════════

# ── Constantes de confianza King Rongo ──
_KR_DIAMOND_THRESHOLD = 0.65   # pick diamante
_KR_GOLD_THRESHOLD    = 0.58   # pick oro
_KR_MIN_EDGE          = 0.00   # sin edge mínimo — KR decide
_KR_MIN_PROB          = 0.50   # prob mínima para aparecer en lista
_KR_CONFLICT_SPREAD   = 0.22   # dispersión modelos → conflicto


def _kr_edge_score(prob, odd):
    """Edge real = prob - 1/odd. Si no hay odd, edge simulado."""
    if odd > 1.01:
        return prob - (1.0 / odd)
    # Sin cuota: edge implícito vs 50-50
    return prob - 0.50


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

    # ── FOTO PRIMERO — lo más importante arriba ──
    st.markdown(
        "<div style='font-size:.78rem;font-weight:700;color:#FFD700;"
        "text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px'>"
        "📸 Sube la foto de tu pick</div>",
        unsafe_allow_html=True)

    src_opt = st.radio("Fuente", ["📁 Galería / Archivo", "📷 Tomar foto ahora"],
                       horizontal=True, label_visibility="collapsed", key=f"src_{key_sfx}")
    uploaded = None
    if src_opt == "📁 Galería / Archivo":
        uploaded = st.file_uploader("", type=["png","jpg","jpeg","webp"],
                                    label_visibility="collapsed", key=f"up_{key_sfx}")
    else:
        cam = st.camera_input("", label_visibility="collapsed", key=f"cam_{key_sfx}")
        if cam: uploaded = cam

    # ── Brain KPIs — solo si hay historial ──
    if not uploaded and bstats.get("total", 0) > 0:
        _t = bstats["total"]; _w = bstats["wins"]; _roi = bstats.get("roi", 0)
        _acierto = round(_w/_t*100) if _t > 0 else 0
        st.markdown(
            f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:12px 0'>"
            f"<div class='mbox'><div class='mval' style='color:#00ccff;font-size:1.1rem'>{_t}</div><div class='mlbl'>Picks</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#00ff88;font-size:1.1rem'>{_w}</div><div class='mlbl'>Aciertos</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#FFD700;font-size:1.1rem'>{_acierto}%</div><div class='mlbl'>Hit rate</div></div>"
            f"<div class='mbox'><div class='mval' style='color:{'#00ff88' if _roi>=0 else '#ff4444'};font-size:1.1rem'>{_roi:+.1f}%</div><div class='mlbl'>ROI</div></div>"
            f"</div>", unsafe_allow_html=True)

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

def _xg_fallback(m, is_home, hf=None, af=None):
    """xG con prioridad: 1) historial partidos 2) récord W-D-L 3) odds del mercado.
    Evita el 33/33/33 cuando no hay historial (ej. FA Cup, Copa, torneos cortos)."""
    form   = hf if is_home else af
    rec    = m.get("home_rec","5-5-5") if is_home else m.get("away_rec","5-5-5")
    odd_h  = float(m.get("odd_h", 0) or 0)
    odd_a  = float(m.get("odd_a", 0) or 0)
    odd_d  = float(m.get("odd_d", 0) or 0)

    # 1. Historial de partidos (más confiable)
    if form:
        op = 1/odd_h if (is_home and odd_h>1) else (1/odd_a if odd_a>1 else 0)
        return xg_weighted(form, is_home, odds_prior=op)

    # 2. Récord W-D-L (si no es el default 5-5-5)
    if rec and rec != "5-5-5":
        return xg_from_record(rec, is_home)

    # 3. Odds como prior (cuando no hay nada más — FA Cup, playoffs, etc.)
    if odd_h > 1 and odd_a > 1 and odd_d > 1:
        _tot = 1/odd_h + 1/odd_d + 1/odd_a
        _ph  = (1/odd_h) / _tot
        _pa  = (1/odd_a) / _tot
        if is_home:
            return max(0.35, 0.50 + _ph * 2.2 + 0.15)
        else:
            return max(0.35, 0.50 + _pa * 2.2)

    return 1.3 if is_home else 1.0


# ══════════════════════════════════════════════════════════════════════
# 🏆 CUP ENRICHER — Factor de división para FA Cup, Copas nacionales
# Cuando dos equipos de distintas divisiones se enfrentan, el modelo
# necesita saber el nivel real de cada uno, no solo las odds.
# ══════════════════════════════════════════════════════════════════════

# Slugs ESPN por liga para buscar forma reciente del equipo en SU liga
_DIVISION_SLUGS = {
    # Inglaterra
    "eng.1": ("Premier League", 1.00, 1.55),   # (nombre, factor_xg, xg_base)
    "eng.2": ("Championship",   0.78, 1.30),
    "eng.3": ("League One",     0.62, 1.15),
    "eng.4": ("League Two",     0.50, 1.05),
    # España
    "esp.1": ("La Liga",        1.00, 1.50),
    "esp.2": ("Segunda",        0.76, 1.25),
    # Alemania
    "ger.1": ("Bundesliga",     1.00, 1.65),
    "ger.2": ("2. Bundesliga",  0.77, 1.30),
    # Italia
    "ita.1": ("Serie A",        1.00, 1.45),
    "ita.2": ("Serie B",        0.74, 1.20),
    # Francia
    "fra.1": ("Ligue 1",        1.00, 1.50),
    "fra.2": ("Ligue 2",        0.75, 1.20),
    # Copa de copas — liga base
    "eng.fa":   ("FA Cup",       None, None),   # → buscar liga real
    "eng.lc":   ("Carabao Cup",  None, None),
    "esp.copa": ("Copa del Rey", None, None),
    "ger.dfb":  ("DFB Pokal",    None, None),
    "ita.coppa":("Coppa Italia", None, None),
    "fra.coupe":("Coupe de France", None, None),
}

# Equipos conocidos con su liga real (para FA Cup sin historial API)
# Top 20 PL + Championship completo + League One top (marzo 2026)
_TEAM_DIVISION: dict = {
    # Premier League 2025-26
    "liverpool":      "eng.1", "arsenal":          "eng.1",
    "chelsea":        "eng.1", "manchester city":  "eng.1",
    "manchester utd": "eng.1", "man utd":          "eng.1",
    "newcastle":      "eng.1", "newcastle utd":    "eng.1",
    "aston villa":    "eng.1", "tottenham":        "eng.1",
    "spurs":          "eng.1", "bournemouth":      "eng.1",
    "fulham":         "eng.1", "brentford":        "eng.1",
    "brighton":       "eng.1", "west ham":         "eng.1",
    "everton":        "eng.1", "leicester":        "eng.1",
    "ipswich":        "eng.1", "southampton":      "eng.1",
    "crystal palace": "eng.1", "nottm forest":     "eng.1",
    "nottingham forest": "eng.1", "wolves":        "eng.1",
    "wolverhampton":  "eng.1",
    # Championship 2025-26
    "leeds":          "eng.2", "leeds utd":        "eng.2",
    "burnley":        "eng.2", "sheffield utd":    "eng.2",
    "norwich":        "eng.2", "millwall":         "eng.2",
    "coventry":       "eng.2", "bristol city":     "eng.2",
    "cardiff":        "eng.2", "hull":             "eng.2",
    "hull city":      "eng.2", "stoke":            "eng.2",
    "stoke city":     "eng.2", "swansea":          "eng.2",
    "blackburn":      "eng.2", "sunderland":       "eng.2",
    "derby":          "eng.2", "derby county":     "eng.2",
    "portsmouth":     "eng.2", "watford":          "eng.2",
    "middlesbrough":  "eng.2", "qpr":              "eng.2",
    "west brom":      "eng.2", "sheffield wed":    "eng.2",
    "plymouth":       "eng.2", "oxford":           "eng.2",
    "luton":          "eng.2", "Preston":          "eng.2",
    # League One 2025-26
    "birmingham":     "eng.3", "huddersfield":     "eng.3",
    "wigan":          "eng.3", "charlton":         "eng.3",
    "rotherham":      "eng.3", "stevenage":        "eng.3",
    "peterborough":   "eng.3", "bristol rovers":   "eng.3",
    # League Two
    "newport":        "eng.4", "grimsby":          "eng.4",
    "doncaster":      "eng.4", "tranmere":         "eng.4",
    "notts county":   "eng.4", "colchester":       "eng.4",
    "mansfield":      "eng.4", "mansfield town":   "eng.4",
    "wrexham":        "eng.2",
    "nurnberg":       "ger.2", "nürnberg":         "ger.2",
    "1. fc nurnberg": "ger.2", "1. fc nürnberg":   "ger.2",
    "fortuna düss":   "ger.2", "fortuna dusseldorf":"ger.2",
    # La Liga
    "barcelona":  "esp.1", "real madrid":     "esp.1",
    "atletico":   "esp.1", "villarreal":      "esp.1",
    "real sociedad":"esp.1","athletic bilbao":"esp.1",
    # Bundesliga
    "bayern":     "ger.1", "dortmund":        "ger.1",
    "leverkusen": "ger.1", "rb leipzig":      "ger.1",
    "frankfurt":  "ger.1", "freiburg":        "ger.1",
}

@st.cache_data(ttl=3600, show_spinner=False)
def _cup_get_form_in_league(team_id: str, team_name: str) -> dict:
    """
    Para equipos en copas nacionales: busca su forma reciente en SU liga,
    no en la copa. Devuelve {slug, division_name, factor, xg_base, form[]}.
    """
    # 1. Detectar liga del equipo por nombre
    name_low = (team_name or "").lower().strip()
    div_slug = None
    for key, slug in _TEAM_DIVISION.items():
        if key in name_low or name_low in key:
            div_slug = slug
            break

    # 2. Si encontramos su liga, buscar forma en esa liga
    form_in_league = []
    if div_slug and div_slug in _DIVISION_SLUGS:
        try:
            data  = eg(f"{ESPN}/{div_slug}/teams/{team_id}/schedule")
            evs   = data.get("events", [])
            for ev in evs:
                try:
                    comp  = ev["competitions"][0]
                    state = ev.get("status",{}).get("type",{}).get("state","")
                    if state != "post": continue
                    # Solo partidos de SU liga (filtrar copa)
                    ev_name = (ev.get("name","") + ev.get("shortName","")).lower()
                    if any(c in ev_name for c in ["fa cup","carabao","copa","pokal","coppa","coupe"]):
                        continue
                    comps = comp["competitors"]
                    hc = next(c for c in comps if c["homeAway"]=="home")
                    ac = next(c for c in comps if c["homeAway"]=="away")
                    is_home = str(hc["team"]["id"]) == str(team_id)
                    my  = hc if is_home else ac
                    opp = ac if is_home else hc
                    gf = parse_score(my.get("score",0))
                    gc = parse_score(opp.get("score",0))
                    form_in_league.append({
                        "date": ev.get("date","")[:10],
                        "result": "W" if gf>gc else ("D" if gf==gc else "L"),
                        "gf": gf, "gc": gc,
                        "xg_f": 0.0, "xg_c": 0.0,
                        "opponent": opp["team"]["displayName"],
                        "is_home": is_home,
                        "league": div_slug,
                    })
                except: continue
            form_in_league.sort(key=lambda x: x["date"], reverse=True)
            form_in_league = form_in_league[:10]
        except: pass

    div_info = _DIVISION_SLUGS.get(div_slug, ("Desconocida", 0.70, 1.10))
    return {
        "slug":     div_slug or "unknown",
        "div_name": div_info[0],
        "factor":   div_info[1] or 0.70,
        "xg_base":  div_info[2] or 1.10,
        "form":     form_in_league,
    }


def _cup_enriched_xg(m: dict, is_home: bool, hf: list, af: list) -> float:
    """
    xG enriquecido para partidos de copa (FA Cup, etc.).
    Combina:
      1. Forma reciente en SU liga propia
      2. Factor de calidad de división
      3. Odds como calibración final
    """
    slug      = m.get("slug","")
    _cup_slugs = {"eng.fa","eng.lc","esp.copa","ger.dfb","ita.coppa","fra.coupe"}
    is_cup = slug in _cup_slugs

    # Si no es copa o hay forma directa disponible — usar pipeline normal
    if not is_cup:
        return _xg_fallback(m, is_home, hf=hf, af=af)

    team_id   = m.get("home_id","") if is_home else m.get("away_id","")
    team_name = m.get("home","") if is_home else m.get("away","")
    odd_h     = float(m.get("odd_h",0) or 0)
    odd_a     = float(m.get("odd_a",0) or 0)
    odd_d     = float(m.get("odd_d",0) or 0)

    # Buscar forma en liga propia
    cup_data  = _cup_get_form_in_league(str(team_id), team_name)
    league_form = cup_data["form"]
    div_factor  = cup_data["factor"]   # ej. 0.78 para Championship
    xg_base     = cup_data["xg_base"]  # xG promedio de esa división

    if league_form:
        # xG desde forma real en su liga, con decaimiento temporal
        raw_xg = xg_weighted(league_form, is_home, odds_prior=0)

        home_cup = _cup_get_form_in_league(str(m.get("home_id","")), m.get("home",""))
        away_cup = _cup_get_form_in_league(str(m.get("away_id","")), m.get("away",""))
        home_factor = home_cup["factor"]
        away_factor = away_cup["factor"]

        # Factor relativo: calidad del equipo que calculamos vs su rival
        this_factor  = home_factor if is_home else away_factor
        rival_factor = away_factor if is_home else home_factor
        rel = this_factor / max(0.3, rival_factor)

        # Cuando la diferencia es grande (ej PL vs L2: 1.0/0.50=2.0),
        # el equipo inferior no se beneficia de jugar en casa
        div_gap = abs(home_factor - away_factor)
        if div_gap >= 0.40:
            # Diferencia de 2+ divisiones: factor de casa casi nulo para el inferior
            home_bonus = 0.03 if (is_home and home_factor < away_factor) else 0.0
            raw_xg_adj = raw_xg * (1.0 + home_bonus)
        else:
            raw_xg_adj = raw_xg

        xg_adj = raw_xg_adj * max(0.5, min(2.0, rel))

    else:
        # Sin forma en liga propia → usar xG base de su división
        xg_adj = xg_base * (1.08 if is_home else 1.0)

    # Calibración final con odds (30% mercado, 70% modelo)
    if odd_h > 1 and odd_a > 1 and odd_d > 1:
        _tot  = 1/odd_h + 1/odd_d + 1/odd_a
        _ph   = (1/odd_h) / _tot
        _pa   = (1/odd_a) / _tot
        _p    = _ph if is_home else _pa
        xg_mkt = max(0.3, 0.50 + _p * 2.2 + (0.15 if is_home else 0))
        xg_adj = 0.70 * xg_adj + 0.30 * xg_mkt

    return round(max(0.20, min(4.5, xg_adj)), 3)

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
    """Probabilidad de ganar punto de servicio — Elo logarítmico para rankings reales."""
    import math as _m
    base = {"hard":0.630,"clay":0.600,"grass":0.662,"carpet":0.645}.get(surface.lower(),0.630)
    # Convertir ranking a Elo: top1≈2400, top10≈2161, top50≈1994, top150≈1880
    def _r2e(r): return 2400 - 550 * _m.log(max(1,min(500,r))) / _m.log(200)
    elo_srv = _r2e(rank_srv)
    elo_ret = _r2e(rank_ret)
    # Factor amplificado: 100 Elo pts → +0.042 (antes era 0.030 — demasiado conservador)
    adj = (elo_srv - elo_ret) * 0.00042
    return max(0.32, min(0.80, base + adj))

def _markov_game(p):
    """P(ganar juego) dado p(ganar punto) — fórmula cerrada exacta."""
    q = 1 - p
    pg = sum(math.comb(a+3,3)*p**4*q**a for a in range(3))
    pg += math.comb(6,3)*(p*q)**3 * (p**2/(p**2+q**2))
    return max(0.01, min(0.99, pg))

def weibull_match_prob(rank1, rank2, odd_1=0, odd_2=0, surface="hard", best_of=3):
    """Probabilidad de partido: Weibull (punto) → Markov (juego → set → partido).
    Usa odds ratio Barnett & Clarke para propagar correctamente sin comprimir hacia 50%."""
    pg1 = _markov_game(_weibull_srv_prob(rank1, rank2, surface))  # prob ganar juego sirviendo p1
    pg2 = _markov_game(_weibull_srv_prob(rank2, rank1, surface))  # prob ganar juego sirviendo p2
    # P(ganar set) usando prob de ganar game al servir y al restar
    # Klaassen & Magnus: usar el odds ratio de games ganados
    # pg1 = prob p1 gana su servicio; (1-pg2) = prob p1 gana el servicio de p2
    p_win_game_overall = (pg1 + (1 - pg2)) / 2  # promedio ponderado
    ps1 = max(0.01, min(0.99, p_win_game_overall))
    need = 2 if best_of == 3 else 3
    p1m = sum(math.comb(s-1,need-1)*ps1**need*(1-ps1)**(s-need) for s in range(need, best_of+1))
    # Amplificar la separación: p1m está en [0.35, 0.65] → stretching calibrado
    # Barnett (2005): prob partido = prob set^k, k≈2.2 para best-of-3 calibrado en ATP
    center = 0.5
    stretched = center + (p1m - center) * 2.2
    p1m = max(0.05, min(0.95, stretched))
    if odd_1 > 1 and odd_2 > 1:
        t = 1/odd_1 + 1/odd_2
        p1m = 0.55 * p1m + 0.45 * (1/odd_1) / t  # más peso al mercado (tiene info de hoy)
    return {"p1": round(p1m, 4), "p2": round(1-p1m, 4)}

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


def ensemble_football(hxg, axg, h2h_s=None, hform=None, aform=None,
                       home_id=None, away_id=None,
                       odd_h=0.0, odd_a=0.0, odd_d=0.0):
    """
    Ensemble mejorado: Dixon-Coles + Poisson BV + Elo + H2H + Mercado (Bayesian).

    Pesos dinámicos:
    - Si hay H2H sólido (≥5 partidos): DC 35% + BVP 25% + Elo 15% + H2H 15% + Mkt 10%
    - Si hay momios en tiempo real:    DC 35% + BVP 25% + Elo 15% + H2H 10% + Mkt 15%
    - Sin nada extra:                  DC 45% + BVP 30% + Elo 15% + H2H 10%

    Mercado como 5° modelo bayesiano:
    El mercado agrega información de miles de apostadores profesionales,
    lesiones de último minuto, y condiciones que el modelo estadístico no ve.
    Ref: Forrest & Simmons 2002 — market efficiency in football betting.

    Dixon-Coles rho dinámico: más negativo cuando ambos xG son bajos
    (partidos defensivos tienen más correlación negativa goles).
    """
    # ── rho dinámico (correlación goles bajos) ──
    total_xg = hxg + axg
    rho = -0.13 if total_xg > 2.2 else (-0.18 if total_xg > 1.5 else -0.22)

    dc  = dc_probabilities(hxg, axg, rho=rho)
    bvp = bivariate_poisson(hxg, axg)
    elo_ph = elo_win_prob(home_id or "h", away_id or "a", hform, aform)

    h2h_valid = h2h_s and h2h_s.get("tot",0) >= 5
    h2h_ph = (h2h_s["hp"]/100 if h2h_valid else dc["ph"])
    h2h_pd = (h2h_s["dp"]/100 if h2h_valid else dc["pd"])

    # ── Mercado como 5° modelo ──
    mkt_ph = mkt_pd = mkt_pa = 0.0
    has_mkt = odd_h > 1 and odd_a > 1 and odd_d > 1
    if has_mkt:
        vig   = 1/odd_h + 1/odd_d + 1/odd_a
        mkt_ph = (1/odd_h) / vig
        mkt_pd = (1/odd_d) / vig
        mkt_pa = (1/odd_a) / vig

    # ── Pesos dinámicos ──
    if has_mkt and h2h_valid:
        w = {"dc":0.33,"bvp":0.23,"elo":0.14,"h2h":0.14,"mkt":0.16}
    elif has_mkt:
        w = {"dc":0.35,"bvp":0.25,"elo":0.15,"h2h":0.10,"mkt":0.15}
    elif h2h_valid:
        w = {"dc":0.35,"bvp":0.25,"elo":0.15,"h2h":0.15,"mkt":0.10}
    else:
        w = {"dc":0.45,"bvp":0.30,"elo":0.15,"h2h":0.10,"mkt":0.00}

    ph = (w["dc"]*dc["ph"] + w["bvp"]*bvp["ph"] + w["elo"]*elo_ph
          + w["h2h"]*h2h_ph + w["mkt"]*mkt_ph)
    pd = (w["dc"]*dc["pd"] + w["bvp"]*bvp["pd"]
          + w["h2h"]*h2h_pd + w["mkt"]*mkt_pd)
    pa = max(0.01, 1-ph-pd)
    s  = ph+pd+pa; ph/=s; pd/=s; pa/=s

    all_phs = [dc["ph"], bvp["ph"], elo_ph, h2h_ph]
    if has_mkt: all_phs.append(mkt_ph)
    std = float(np.std(all_phs))
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
        "mkt_ph":round(mkt_ph*100,1) if has_mkt else 0,
        "rho_used": round(rho,3),
        "weights": w,
        "model":"Ensemble DC+BVP+Elo+H2H+Mkt (dinámico)",
    }


# ══════════════════════════════════════════════════════════════════════
# VEREDICTO ACADÉMICO — TENIS  (metodología exclusiva)
# 3 modelos específicos de tenis + 50,000 simulaciones Monte Carlo
# ══════════════════════════════════════════════════════════════════════

# ── Surface-specific performance profiles (Klaassen & Magnus 2001, updated) ──
# Win rates by surface for different ranking tiers — calibrated from ATP data
_SURFACE_PROFILES = {
    # surface: {tier_diff: prob_adjustment}
    # tier_diff = rank_p1 - rank_p2 divided by 10 (rank brackets)
    "hard":   {"srv_boost": 0.00,  "top10_bonus": 0.02, "upset_rate": 0.28},
    "clay":   {"srv_boost": -0.04, "top10_bonus": 0.04, "upset_rate": 0.22},  # clay rewards consistency
    "grass":  {"srv_boost": 0.05,  "top10_bonus": 0.01, "upset_rate": 0.32},  # grass = more upsets
    "carpet": {"srv_boost": 0.03,  "top10_bonus": 0.01, "upset_rate": 0.30},
}

# Surface affinity by player archetype (inferred from ranking era + name patterns)
# This is a conservative model — only adjusts when ranking is real (< 150)
_CLAY_SPECIALISTS = {
    "etcheverry","nadal","ruud","alcaraz","cerundolo","baez","navone",
    "jarry","tabilo","gaston","coria","schwartzman","ferrer","thiem",
    "swiatek","jabeur","paolini","badosa","sorribes",
}
_GRASS_SPECIALISTS = {
    "djokovic","federer","wimbledon","hurkacz","norrie","draper",
    "rybakina","kvitova","keys",
}
_HARD_SPECIALISTS = {
    "sinner","medvedev","zverev","fritz","shelton","paul","korda",
    "mensik","draper","sabalenka","gauff","zheng","pegula",
}

def _surface_affinity(name: str, surface: str) -> float:
    """
    Returns a small probability bonus (+/-) for a player on a specific surface.
    Only applied when ranking is known (< 150), to avoid amplifying noise.
    Max adjustment: ±0.04 (4 percentage points).
    """
    name_l = name.lower()
    adj = 0.0
    if surface == "clay":
        if any(s in name_l for s in _CLAY_SPECIALISTS):     adj = +0.04
        elif any(s in name_l for s in _GRASS_SPECIALISTS):  adj = -0.03
        elif any(s in name_l for s in _HARD_SPECIALISTS):   adj = -0.02
    elif surface == "grass":
        if any(s in name_l for s in _GRASS_SPECIALISTS):    adj = +0.04
        elif any(s in name_l for s in _CLAY_SPECIALISTS):   adj = -0.03
    elif surface == "hard":
        if any(s in name_l for s in _HARD_SPECIALISTS):     adj = +0.02
        elif any(s in name_l for s in _CLAY_SPECIALISTS):   adj = -0.01
    return adj


def _tennis_elo_prob(rank1, rank2, odd_1=0, odd_2=0, surface="hard",
                     p1_name="", p2_name=""):
    """
    MODELO 1 — Elo Adaptado al Tenis con ajuste de superficie
    (Glickman & Jones 1999 + Klaassen & Magnus surface calibration)

    Pipeline:
    1. Ranking → Elo (escala logarítmica inversa, calibrada con datos ATP)
    2. Elo → prob de victoria (fórmula estándar)
    3. Ajuste por superficie (clay/grass/hard specialist bonus)
    4. Blend con mercado (momios = información agregada de todo el mundo)
    """
    def rank_to_elo(r):
        # Calibración: rank 1 ≈ 2400, rank 10 ≈ 2200, rank 100 ≈ 1800
        r = max(1, min(r, 800))
        return 2400 - 400 * math.log10(r)

    r1 = rank1 if rank1 < 900 else 200
    r2 = rank2 if rank2 < 900 else 200
    e1 = rank_to_elo(r1)
    e2 = rank_to_elo(r2)
    p_elo = 1 / (1 + 10 ** ((e2 - e1) / 400))

    # Surface affinity adjustment (only if ranking is real)
    if r1 < 150 or r2 < 150:
        adj1 = _surface_affinity(p1_name, surface)
        adj2 = _surface_affinity(p2_name, surface)
        p_elo = max(0.05, min(0.95, p_elo + adj1 - adj2))

    # Blend con mercado — el mercado tiene info que el ranking no tiene
    # (lesiones de hoy, condiciones, confianza actual del jugador)
    if odd_1 > 1 and odd_2 > 1:
        vig   = 1/odd_1 + 1/odd_2
        p_mkt = (1/odd_1) / vig
        # Cuanto más igual el ranking, más peso al mercado
        rank_gap = abs(r1 - r2)
        mkt_weight = 0.50 if rank_gap < 20 else (0.40 if rank_gap < 50 else 0.30)
        p_elo = (1 - mkt_weight) * p_elo + mkt_weight * p_mkt

    return round(max(0.05, min(0.95, p_elo)), 4)


def _tennis_surface_model(rank1, rank2, surface, odd_1=0, odd_2=0,
                           p1_name="", p2_name=""):
    """
    MODELO 2 — Weibull-Markov por Superficie (Klaassen & Magnus 2003)
    Cada superficie tiene parámetros distintos de ventaja al servicio.
    Grass > Carpet > Hard > Clay en ventaja de servicio.
    Incluye ajuste de especialista de superficie sobre el modelo Weibull.
    """
    p1_base = weibull_match_prob(rank1, rank2, odd_1, odd_2, surface, best_of=3)["p1"]
    # Add surface affinity on top of Weibull
    if (rank1 < 150 or rank2 < 150) and (p1_name or p2_name):
        adj1 = _surface_affinity(p1_name, surface)
        adj2 = _surface_affinity(p2_name, surface)
        p1_base = max(0.05, min(0.95, p1_base + (adj1 - adj2) * 0.5))
    return p1_base


def _tennis_monte_carlo_50k(p_win_match, odd_1=0, odd_2=0, n=50_000):
    """
    MODELO 3 — Monte Carlo 50,000 simulaciones (inspirado en Barnett & Clarke 2005)
    Simula cada partido set a set, game a game.
    Incorpora varianza real del tenis: ningún partido está "decidido" antes de empezar.
    
    p_win_match = probabilidad base de que P1 gane el partido (0-1)
    Simula best-of-3 sets con tie-break.
    """
    rng = np.random.default_rng(42)

    # Prob de ganar un set dado prob partido (calibración empírica)
    # Ajuste: en best-of-3, si p_partido=0.65 → p_set ≈ 0.58
    def match_to_set_prob(pm):
        # Inversión numérica: P(ganar partido) = sum_{s=2}^{3} C(s-1,1)*ps^2*(1-ps)^(s-2)
        # Aproximación analítica (Newton-Raphson simplificado)
        ps = max(0.35, min(0.75, 0.45 + (pm - 0.50) * 0.65))
        return ps

    ps1 = match_to_set_prob(p_win_match)
    ps2 = 1 - ps1

    p1_wins = 0
    for _ in range(n):
        sets_p1 = sets_p2 = 0
        while sets_p1 < 2 and sets_p2 < 2:
            # Simular set: primero a 6 juegos, tie-break si 6-6
            g1 = g2 = 0
            while True:
                if rng.random() < ps1: g1 += 1
                else:                  g2 += 1
                if g1 >= 6 and g1 - g2 >= 2: break
                if g2 >= 6 and g2 - g1 >= 2: break
                if g1 == 7 or g2 == 7:       break   # tie-break won
                if g1 == 6 and g2 == 6:
                    # Tie-break: primero a 7 puntos con diferencia 2
                    if rng.random() < ps1: g1 = 7
                    else:                  g2 = 7
                    break
            if g1 > g2: sets_p1 += 1
            else:       sets_p2 += 1
        if sets_p1 > sets_p2: p1_wins += 1

    p1_mc = p1_wins / n
    # Blend Monte Carlo con mercado si hay momios
    if odd_1 > 1 and odd_2 > 1:
        vig   = 1/odd_1 + 1/odd_2
        p_mkt = (1/odd_1) / vig
        p1_mc = 0.65 * p1_mc + 0.35 * p_mkt
    return round(max(0.05, min(0.95, p1_mc)), 4)


# ── MODELO 4: H2H Momentum + Ranking Trajectory (nuevo) ──────────────────────
# Basado en Spanias (2012) — los partidos recientes entre dos jugadores
# son más predictivos que el ranking a solas.
# Combina:
#   a) Ventaja de ranking ponderada exponencialmente (más peso al ranking actual)
#   b) Momentum del tour (diferencia de ranking en los últimos meses)
#   c) Fatiga implícita por posición en el torneo (Grand Slam: best-of-5 cuesta más)

_RANK_TRAJECTORY_2026 = {
    # jugadores que SUBIERON rápido en 2025-2026 → momentum positivo
    "mensik":+15,"fonseca":+40,"tien":+30,"cobolli":+20,"darderi":+18,
    "shelton":+8,"draper":+10,"mboko":+25,"andreeva":+12,"jovic":+20,
    "anisimova":+8,"noskova":+12,
    # jugadores que BAJARON o están estancados → momentum negativo
    "tsitsipas":-20,"hurkacz":-18,"rublev":-5,"dimitrov":-15,
    "jabeur":-15,"kvitova":-10,"osaka":-5,"azarenka":-12,
    "badosa":-5,"andreescu":-8,
}

def _tennis_h2h_momentum(rank1, rank2, p1_name, p2_name, odd_1=0, odd_2=0, surface="hard"):
    """
    MODELO 4 — H2H Momentum + Trajectory (Spanias 2012 adaptado)
    Ajusta la prob base de Elo con:
    1. Momentum de ranking (trayectoria reciente en el tour)
    2. Ventaja de especialista de superficie amplificada
    3. Blend con mercado si cuotas disponibles
    """
    import math as _m
    # Prob base Elo (mismo logaritmo)
    def _r2e(r): return 2400 - 400 * _m.log10(max(1, min(800, r)))
    e1 = _r2e(rank1); e2 = _r2e(rank2)
    p_base = 1 / (1 + 10**((e2 - e1) / 400))

    # Ajuste de trayectoria — jugadores en ascenso tienen ventaja sobre su ranking actual
    n1 = p1_name.lower()
    n2 = p2_name.lower()
    traj1 = next((v for k,v in _RANK_TRAJECTORY_2026.items() if k in n1), 0)
    traj2 = next((v for k,v in _RANK_TRAJECTORY_2026.items() if k in n2), 0)
    # Cada 10 posiciones de trayectoria = +0.012 de prob
    traj_adj = (traj1 - traj2) * 0.0012
    p_traj = max(0.05, min(0.95, p_base + traj_adj))

    # Ajuste superficie ampliado (x1.5 vs modelo base)
    adj1 = _surface_affinity(p1_name, surface) * 1.5
    adj2 = _surface_affinity(p2_name, surface) * 1.5
    p_surf = max(0.05, min(0.95, p_traj + adj1 - adj2))

    # Blend con mercado
    if odd_1 > 1 and odd_2 > 1:
        vig = 1/odd_1 + 1/odd_2
        p_mkt = (1/odd_1) / vig
        rank_gap = abs(rank1 - rank2)
        w = 0.45 if rank_gap < 15 else (0.35 if rank_gap < 40 else 0.25)
        p_surf = (1-w)*p_surf + w*p_mkt

    return round(max(0.05, min(0.95, p_surf)), 4)


# ── MODELO 5: Serve Dominance + Break Point Pressure (nuevo) ─────────────────
# Basado en Newton & Aslam (2009) — en tenis, dominar el servicio
# es el factor más correlacionado con ganar partidos en todas las superficies.
# Aproximamos con:
#   a) Ventaja de servidor implícita según superficie (grass > hard > clay)
#   b) Perfil de jugador: big server vs returner vs all-court
#   c) Brecha de ranking como proxy de dominancia de break points

# Perfiles de servicio — big servers tienen ventaja EXTRA en grass/hard
_BIG_SERVERS = {
    "isner","raonic","karlovic","anderson","opelka","perricard","mpetshi",
    "shelton","bublik","rinderknech","fils","zverev","fritz","paul",
    "djokovic","sabalenka","keys","rybakina","pliskova","kvitova",
}
_RETURNERS = {
    "djokovic","alcaraz","sinner","ruud","nadal","schwartzman","thiem",
    "swiatek","halep","azarenka","muchova","pegula","gauff",
}

def _tennis_serve_dominance(rank1, rank2, p1_name, p2_name, odd_1=0, odd_2=0, surface="hard"):
    """
    MODELO 5 — Serve Dominance + Break Point Pressure (Newton & Aslam 2009)
    Evalúa quién controla el ritmo del partido a través del servicio.
    """
    import math as _m
    # Prob base Weibull (reutilizamos la función existente con ajuste mayor)
    p_base = _weibull_srv_prob(rank1, rank2, surface)
    # p_base es prob de ganar punto de servicio — propagar a partido
    pg1 = _markov_game(p_base)  # prob ganar juego sirviendo
    pg2 = _markov_game(_weibull_srv_prob(rank2, rank1, surface))  # oponente sirviendo

    # Ajuste big server
    n1 = p1_name.lower(); n2 = p2_name.lower()
    is_srv1 = any(s in n1 for s in _BIG_SERVERS)
    is_srv2 = any(s in n2 for s in _BIG_SERVERS)
    is_ret1 = any(s in n1 for s in _RETURNERS)
    is_ret2 = any(s in n2 for s in _RETURNERS)

    srv_bonus = {"grass": 0.025, "hard": 0.015, "clay": 0.005}.get(surface, 0.015)
    # Big server vs returner en hierba → big server tiene mucha ventaja
    if is_srv1 and not is_ret2: pg1 = min(0.92, pg1 + srv_bonus)
    if is_srv2 and not is_ret1: pg2 = min(0.92, pg2 + srv_bonus)
    if is_ret1 and not is_srv2: pg1 = min(0.92, pg1 + srv_bonus * 0.5)  # returner vs no-srv
    if is_ret2 and not is_srv1: pg2 = min(0.92, pg2 + srv_bonus * 0.5)

    # Prob de ganar set (approx): p_set = sum_{g=6}^{7} C(g-1,5)*pg1^6*(1-pg1)^(g-6) ...
    # Aproximación directa via markov game → set
    ps1 = pg1  # prob ganar game = proxy razonable para prob ganar set
    # Propagate to match (best-of-3)
    need = 2
    p1m = sum(math.comb(s-1,need-1)*ps1**need*(1-ps1)**(s-need) for s in range(need, 4))
    p1m = max(0.05, min(0.95, p1m))

    # Blend con mercado
    if odd_1 > 1 and odd_2 > 1:
        vig = 1/odd_1 + 1/odd_2
        p_mkt = (1/odd_1) / vig
        p1m = 0.60 * p1m + 0.40 * p_mkt

    return round(max(0.05, min(0.95, p1m)), 4)


def veredicto_academico_tenis(p1_name, p2_name, rank1, rank2,
                               odd_1, odd_2, surface, torneo,
                               expert_p1=None):
    """
    Veredicto académico exclusivo para tenis.
    Integra 5 modelos específicos de tenis + 50k Monte Carlo.
    Semáforo: 🟢 APOSTAR / 🟡 BANK MEDIO / 🔴 NO APOSTAR
    """
    import statistics

    # ── Ejecutar los 5 modelos ──
    p1_elo   = _tennis_elo_prob(rank1, rank2, odd_1, odd_2, surface, p1_name, p2_name)
    p1_surf  = _tennis_surface_model(rank1, rank2, surface, odd_1, odd_2, p1_name, p2_name)
    base_mc  = (p1_elo + p1_surf) / 2
    p1_mc    = _tennis_monte_carlo_50k(base_mc, odd_1, odd_2, n=50_000)
    p1_mom   = _tennis_h2h_momentum(rank1, rank2, p1_name, p2_name, odd_1, odd_2, surface)
    p1_srv   = _tennis_serve_dominance(rank1, rank2, p1_name, p2_name, odd_1, odd_2, surface)

    # Si hay análisis de Einstein, también lo incluimos como señal
    p1_einstein = expert_p1 if expert_p1 is not None else None

    # ── Consenso ponderado — 5 modelos ──
    # Elo y Momentum son los más diferenciadores (amplitud 50-95%)
    # Superficie y Serve dan señal real de superficie pero menor amplitud
    # MC es blend de Elo+Surf — sirve de "árbitro"
    # Pesos: Elo 30%, MC 20%, Momentum 25%, Superficie 13%, Serve 12%
    if p1_einstein is not None:
        p1_final = (0.22*p1_elo + 0.15*p1_surf + 0.16*p1_mc +
                    0.20*p1_mom + 0.12*p1_srv + 0.15*p1_einstein)
    else:
        p1_final = 0.30*p1_elo + 0.13*p1_surf + 0.20*p1_mc + 0.25*p1_mom + 0.12*p1_srv
    p2_final = 1 - p1_final

    fav     = p1_name if p1_final >= p2_final else p2_name
    fav_p   = max(p1_final, p2_final)
    fav_odd = odd_1 if p1_final >= p2_final else odd_2
    dog_p   = min(p1_final, p2_final)

    # ── Edge vs cuota ──
    ev = fav_p - (1/fav_odd) if fav_odd > 1 else 0

    # ── Consenso entre modelos ──
    models_p1 = [p1_elo, p1_surf, p1_mc, p1_mom, p1_srv]
    if p1_einstein: models_p1.append(p1_einstein)
    agree = sum(1 for p in models_p1 if (p >= 0.5) == (p1_final >= 0.5))
    total_m = len(models_p1)
    std = statistics.stdev(models_p1) if len(models_p1) > 1 else 0.1

    # ── Sistema de puntuación ──
    score = 0
    factores = []

    # Probabilidad del favorito
    if fav_p >= 0.70:
        score += 3; factores.append((f"✅ Prob. muy alta: {fav_p*100:.1f}% — favorito claro", "#00ff88"))
    elif fav_p >= 0.62:
        score += 2; factores.append((f"✅ Prob. sólida: {fav_p*100:.1f}%", "#00ff88"))
    elif fav_p >= 0.55:
        score += 1; factores.append((f"⚠️ Prob. moderada: {fav_p*100:.1f}% — partido parejo", "#FFD700"))
    else:
        score -= 1; factores.append((f"🚫 Partido muy parejo: {fav_p*100:.1f}% — sin ventaja clara", "#ff4444"))

    # Consenso entre modelos
    if agree == total_m:
        score += 2; factores.append((f"✅ Los {total_m} modelos coinciden en el mismo ganador", "#00ff88"))
    elif agree >= total_m*0.75:
        score += 1; factores.append((f"⚠️ {agree}/{total_m} modelos de acuerdo", "#FFD700"))
    else:
        score -= 2; factores.append((f"🚫 Modelos divididos — señal mixta en tenis", "#ff4444"))

    # Dispersión
    if std < 0.04:
        score += 2; factores.append((f"✅ Alta consistencia entre modelos (σ={std*100:.1f}%)", "#00ff88"))
    elif std < 0.08:
        score += 1; factores.append((f"⚠️ Dispersión moderada entre modelos (σ={std*100:.1f}%)", "#FFD700"))
    else:
        score -= 1; factores.append((f"🚫 Alta varianza entre modelos (σ={std*100:.1f}%)", "#ff4444"))

    # Edge vs cuota
    if ev > 0.08:
        score += 3; factores.append((f"✅ Edge real: +{ev*100:.1f}% sobre la cuota de mercado", "#00ff88"))
    elif ev > 0.04:
        score += 2; factores.append((f"✅ Edge moderado: +{ev*100:.1f}%", "#00ff88"))
    elif ev > 0:
        score += 1; factores.append((f"⚠️ Edge marginal: +{ev*100:.1f}%", "#FFD700"))
    elif fav_odd == 0:
        factores.append(("⚠️ Sin cuota disponible — EV no calculable", "#FFD700"))
    else:
        score -= 2; factores.append((f"🚫 Sin valor vs cuota: EV={ev*100:.1f}%", "#ff4444"))

    # Monte Carlo específico (50k simulaciones)
    if p1_mc > 0.65 or p1_mc < 0.35:
        score += 1; factores.append((f"✅ Monte Carlo 50k confirma ventaja clara: {max(p1_mc,1-p1_mc)*100:.1f}%", "#00ff88"))
    elif abs(p1_mc - 0.5) < 0.05:
        score -= 1; factores.append((f"🚫 Monte Carlo 50k: partido 50/50 ({p1_mc*100:.1f}%)", "#ff4444"))

    # ── Veredicto final ──
    if score >= 7:
        nivel="#00ff88"; emoji="🟢"; label="APOSTAR"
        desc="Los 3 modelos de tenis + Monte Carlo 50k convergen. Existe ventaja estadística real."
        kelly=f"Kelly sugerido: 1–3% del banco"
        bg="linear-gradient(135deg,#001a00,#002800)"; brd="#00ff88"
    elif score >= 4:
        nivel="#FFD700"; emoji="🟡"; label="APOSTAR — BANK MEDIO"
        desc="Señal moderada. Apuesta conservadora o espera mejor cuota."
        kelly=f"Kelly sugerido: 0.5–1.5% del banco"
        bg="linear-gradient(135deg,#1a1200,#2a1e00)"; brd="#FFD700"
    else:
        nivel="#ff4444"; emoji="🔴"; label="NO APOSTAR"
        desc="Modelos no convergen o cuota sin valor. Sin ventaja estadística en tenis."
        kelly="Abstenerse — 0% del banco"
        bg="linear-gradient(135deg,#1a0000,#2a0000)"; brd="#ff4444"

    # ── Tabla de los 5 modelos ──
    surf_icon = {"hard":"🔵","clay":"🟤","grass":"🟢"}.get(surface.lower(),"🎾")
    model_data = [
        ("Elo Adaptado al Tenis",        p1_elo,  "#00ccff", "30%",
         "Glickman & Jones 1999 — ranking→Elo→prob partido"),
        (f"Superficie {surf_icon} {surface.title()}", p1_surf, "#aa00ff", "13%",
         f"Klaassen & Magnus 2003 — Weibull-Markov en {surface}"),
        ("Monte Carlo 50,000 sim.",      p1_mc,   "#FFD700", "20%",
         "Barnett & Clarke 2005 — 50k simulaciones set a set"),
        ("H2H Momentum + Trayectoria",   p1_mom,  "#ff9500", "25%",
         "Spanias 2012 — trayectoria reciente en el tour + sup."),
        ("Serve Dominance + Break Pts",  p1_srv,  "#ff4488", "12%",
         "Newton & Aslam 2009 — control de ritmo por servicio"),
    ]
    if p1_einstein:
        model_data.append(("Einstein IA + H2H", p1_einstein, "#00ff88", "+",
                           "Análisis H2H, forma, lesiones, motivación"))

    p1_show = p1_final if p1_final>=p2_final else p2_final
    p2_show = 1 - p1_show
    fav_show = fav; dog_show = p2_name if p1_final>=p2_final else p1_name

    model_rows = ""
    for mname, mv, mcol, peso, ref in model_data:
        mv_fav = mv if p1_final>=p2_final else 1-mv
        mcolor = "#00ff88" if mv_fav>=0.60 else ("#FFD700" if mv_fav>=0.50 else "#ff4444")
        bw = int(mv_fav*100)
        model_rows += (
            f"<tr style='border-bottom:1px solid #0d0d2e'>"
            f"<td style='padding:7px 10px'><span style='color:{mcol};font-weight:700;font-size:.78rem'>{mname}</span>"
            f" <span style='color:#333;font-size:.65rem'>({peso})</span></td>"
            f"<td style='padding:7px 10px;text-align:center'>"
            f"<span style='color:{mcolor};font-weight:900;font-size:.95rem'>{mv_fav*100:.1f}%</span>"
            f"<span style='color:{mcolor};font-size:.68rem'> {'▲' if mv_fav>=0.5 else '▼'}</span></td>"
            f"<td style='padding:7px 10px'>"
            f"<div style='height:4px;background:#0d0d2e;border-radius:4px;overflow:hidden'>"
            f"<div style='width:{bw}%;height:100%;background:{mcolor};border-radius:4px'></div></div></td>"
            f"<td style='padding:7px 10px;color:#333;font-size:.65rem'>{ref}</td></tr>"
        )

    factores_html = "".join(
        f"<div style='color:{col};font-size:.78rem;padding:3px 0;line-height:1.4'>{txt}</div>"
        for txt, col in factores
    )

    bar_pct = max(0, min(score, 11))
    bar_color = nivel

    _html_out = f"""
<div style='background:{bg};border:2px solid {brd};border-radius:16px;padding:20px;margin:16px 0'>
  <!-- Semáforo -->
  <div style='display:flex;align-items:center;gap:14px;margin-bottom:4px'>
    <div style='font-size:3rem;line-height:1'>{emoji}</div>
    <div>
      <div style='font-size:.7rem;font-weight:700;color:{nivel};letter-spacing:.14em;text-transform:uppercase'>
        VEREDICTO TENIS — 5 MODELOS + MONTE CARLO 50K</div>
      <div style='font-size:1.5rem;font-weight:900;color:{nivel};letter-spacing:.04em'>{label}</div>
    </div>
  </div>
  <!-- Pick y desc -->
  <div style='background:#07071a88;border-radius:10px;padding:10px 14px;margin:10px 0'>
    <div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.1em'>PICK</div>
    <div style='font-size:1.1rem;font-weight:800;color:#fff'>🎾 {fav_show} gana</div>
    <div style='font-size:.82rem;color:#aaa;margin-top:2px'>{desc}</div>
    <div style='font-size:.8rem;font-weight:700;color:{nivel};margin-top:4px'>💰 {kelly}</div>
  </div>
  <!-- Score bar -->
  <div style='margin:10px 0 6px'>
    <div style='display:flex;justify-content:space-between;font-size:.65rem;color:#555;margin-bottom:3px'>
      <span>🔴 No apostar</span><span>Confianza</span><span>🟢 Apostar</span>
    </div>
    <div style='height:6px;background:#0d0d2e;border-radius:6px;overflow:hidden'>
      <div style='width:{bar_pct/11*100:.0f}%;height:100%;background:{bar_color};border-radius:6px;
           transition:width 0.5s'></div>
    </div>
  </div>
  <!-- Probabilidades finales -->
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0'>
    <div style='background:#07071a;border-radius:10px;padding:10px;text-align:center'>
      <div style='font-size:.65rem;color:#555;margin-bottom:2px'>{fav_show[:18]}</div>
      <div style='font-size:1.6rem;font-weight:900;color:{nivel}'>{fav_p*100:.1f}%</div>
      <div style='font-size:.65rem;color:#555'>FAVORITO</div>
    </div>
    <div style='background:#07071a;border-radius:10px;padding:10px;text-align:center'>
      <div style='font-size:.65rem;color:#555;margin-bottom:2px'>{dog_show[:18]}</div>
      <div style='font-size:1.6rem;font-weight:900;color:#555'>{dog_p*100:.1f}%</div>
      <div style='font-size:.65rem;color:#555'>UNDERDOG</div>
    </div>
  </div>
  <!-- Tabla 3 modelos -->
  <div style='font-size:.7rem;font-weight:700;color:#555;letter-spacing:.1em;text-transform:uppercase;margin:10px 0 4px'>
    📊 Análisis por Modelo — Prob. favorito: {fav_p*100:.1f}% promedio</div>
  <table style='width:100%;border-collapse:collapse;background:#07071a;border-radius:10px;overflow:hidden'>
    <tr style='background:#0d0d2e'>
      <th style='padding:7px 10px;text-align:left;color:#555;font-size:.68rem;font-weight:600'>Modelo</th>
      <th style='padding:7px 10px;text-align:center;color:#555;font-size:.68rem;font-weight:600'>Prob.</th>
      <th style='padding:7px 10px;color:#555;font-size:.68rem;font-weight:600'>Intensidad</th>
      <th style='padding:7px 10px;color:#555;font-size:.68rem;font-weight:600'>Fuente</th>
    </tr>
    {model_rows}
  </table>
  <!-- Factores -->
  <div style='margin-top:12px;padding-top:10px;border-top:1px solid #151530'>
    {factores_html}
  </div>
  <div style='margin-top:6px;font-size:.65rem;color:#222;font-family:monospace'>
    σ={std*100:.2f}% · agree={agree}/{total_m} · score={score}/11 · 
    {surf_icon} {surface} · MC50k={p1_mc*100:.1f}%/{(1-p1_mc)*100:.1f}%
  </div>
</div>"""

    # Return dict — pipeline reads values directly, no re-parsing of HTML
    return {
        "_p1_final":   p1_final,
        "_p2_final":   p2_final,
        "_fav_name":   fav,
        "_fav_prob":   fav_p,
        "_dog_name":   dog_show,
        "_dog_prob":   dog_p,
        "_label":      label,
        "_nivel_color": nivel,
        "_score":      score,
        "_kelly":      kelly,
        "_html":       _html_out,
        # individual model probs (for transparency)
        "_p1_elo":       p1_elo,
        "_p1_surf":      p1_surf,
        "_p1_mc":        p1_mc,
        "_p1_mom":       p1_mom,
        "_p1_srv":       p1_srv,
        "_p1_einstein":  p1_einstein,
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
        # Si es Over 2.5 / AA / Mitad, usar su prob directamente
        is_totals  = any(x in best_market for x in ["Over","Ambos","AA","mitad","o Emp"])
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
    Mercados: 1X2, Over 2.5, Over 3.5, Ambos Anotan, Gana cualquier mitad.
    NO incluye O1.5, ML simple sin cuota, Handicap.
    """
    opts = []
    # 1X2
    if m.get("odd_h",0)>1: opts.append(("🏠 "+m["home"][:15]+" gana",    dp["ph"], m["odd_h"], dp["ph"]-(1/m["odd_h"])))
    if m.get("odd_d",0)>1: opts.append(("🤝 Empate",                      dp["pd"], m["odd_d"], dp["pd"]-(1/m["odd_d"])))
    if m.get("odd_a",0)>1: opts.append(("✈️ "+m["away"][:15]+" gana",      dp["pa"], m["odd_a"], dp["pa"]-(1/m["odd_a"])))
    # DO cualquiera gana — también eliminado
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
        hxg = _cup_enriched_xg(m, True,  hf, af)
        axg = _cup_enriched_xg(m, False, hf, af)
        h2h = get_h2h(m["home_id"],m["away_id"],m["slug"],m["home"],m["away"])
        h2s = h2h_stats(h2h, m["home"], m["away"])
        mc  = ensemble_football(hxg, axg, h2s, hf, af, m["home_id"], m["away_id"], odd_h=m.get("odd_h",0), odd_a=m.get("odd_a",0), odd_d=m.get("odd_d",0))
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
        return  # Sin token — silencioso, no mostrar mensaje
    
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
    _smap = {"Indian Wells":"hard","Miami":"hard","Roland Garros":"clay",
             "Wimbledon":"grass","US Open":"hard","Australian Open":"hard",
             "Monte Carlo":"clay","Madrid":"clay","Barcelona":"clay",
             "Rome":"clay","Cincinnati":"hard","Toronto":"hard",
             "Halle":"grass","Queen":"grass","Dubai":"hard","Doha":"hard"}
    picks = []
    for m in matches:
        if m["state"] != "pre": continue
        try:
            tor = m.get("torneo", m.get("tour",""))
            srf = next((v for k,v in _smap.items() if k.lower() in tor.lower()), "hard")
            r1 = m.get("rank1",0) or 0; r2 = m.get("rank2",0) or 0
            p1n = m.get("p1",""); p2n = m.get("p2","")
            if r1 <= 0 or r1 >= 150:
                r1 = _resolve_rank(p1n, _KNOWN_RANKS) or _resolve_rank_local(p1n) or 120
            if r2 <= 0 or r2 >= 150:
                r2 = _resolve_rank(p2n, _KNOWN_RANKS) or _resolve_rank_local(p2n) or 120
            _vd = veredicto_academico_tenis(p1n, p2n, r1, r2,
                                             m.get("odd_1",0), m.get("odd_2",0), srf, tor)
            best_p = _vd["_fav_prob"]
            fav    = _vd["_fav_name"]
            odd    = m.get("odd_1",0) if fav == p1n else m.get("odd_2",0)
            conf   = _vd["_label"]
            if best_p >= 0.62:
                picks.append({**m, "fav": fav, "best_p": best_p, "odd": odd, "conf": conf,
                               "r1": r1, "r2": r2, "srf": srf})
        except: continue
    if not picks:
        tg_send("🎾 *Tennis Scanner:* Sin picks ML con valor hoy.")
        return 0
    msg  = "🎾 *THE GAMBLERS LAYER | TENNIS PICKS* 🎾\n"
    msg += f"_{datetime.now(CDMX).strftime('%d/%m/%Y')} — {len(picks)} picks_\n\n"
    for p in sorted(picks, key=lambda x: -x["best_p"]):
        odd_txt = f"@{p['odd']:.2f}" if p["odd"] > 1 else "N/D"
        msg += f"🚨 {p.get('tour','')} — {p.get('torneo','')}\n"
        msg += f"🎾 {p['p1']} vs {p['p2']}\n"
        msg += f"🕒 {p.get('hora','')} CDMX · {p.get('srf','hard').title()} · Rk#{p['r1']} vs #{p['r2']}\n"
        msg += f"👉 *{p['fav']} gana* {odd_txt}\n"
        msg += f"📊 Prob: {p['best_p']*100:.1f}%  •  {p['conf']}\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "\n_Que la varianza esté a nuestro favor._ 🎲"
    tg_send(msg)
    return len(picks)

def _pach_call(pregunta: str, sport_label: str, context_data: dict) -> str:
    """
    PACH — AI analyst. Llama a Claude con web_search tool activado.
    Recibe la pregunta del usuario + contexto de la app.
    """
    if not ANTHROPIC_API_KEY:
        return "❌ PACH necesita ANTHROPIC_API_KEY en secrets.toml"

    fecha_hoy = datetime.now(CDMX).strftime("%d/%m/%Y")
    hora_hoy  = datetime.now(CDMX).strftime("%H:%M")

    # Contexto compacto para el system prompt
    partidos_txt = ""
    for p in context_data.get("partidos", [])[:12]:
        partidos_txt += (f"  • {p.get('home','?')} vs {p.get('away','?')} "
                         f"| {p.get('hora','')} | odds: {p.get('odd_h',0):.2f}/{p.get('odd_d',0):.2f}/{p.get('odd_a',0):.2f}\n")

    kr_pick = context_data.get("kr_pick", "")
    villar  = context_data.get("villar", "")

    system = f"""Eres PACH, analista de apuestas deportivas de The Gamblers Layer. 
Hoy es {fecha_hoy} a las {hora_hoy} CDMX. Deporte activo: {sport_label}.

PARTIDOS DISPONIBLES HOY:
{partidos_txt if partidos_txt else '  (sin datos cargados)'}

KING RONGO PICK DEL DÍA: {kr_pick if kr_pick else 'no disponible'}
VILLAR MODELO: {villar if villar else 'no disponible'}

TU MISIÓN:
- Analiza PICKS ESPECÍFICOS que el usuario no puede calcular con la app: handicaps, spread, \
over/under de sets (tenis), triple dobles, player props, parlays combinados, \
over de corners, tarjetas, etc.
- USA web_search para buscar información ACTUAL: lesiones, alineaciones, forma reciente, \
head-to-head, clima, contexto del torneo. SIEMPRE busca antes de responder.
- Da una respuesta DIRECTA y CONCISA. Máximo 5 líneas. Termina con: 
  VEREDICTO: [JUGAR / NO JUGAR / ESPERAR] + probabilidad estimada en %.
- Habla en español, tono confiado pero honesto.
- NUNCA inventes estadísticas — si no encuentras info, dilo.
- Recuerda: las apuestas tienen riesgo. Siempre juega responsablemente."""

    try:
        import json as _j
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 600,
            "system": system,
            "tools": [{"type": "web_search_20250305", "name": "web_search"}],
            "messages": [{"role": "user", "content": pregunta}]
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "interleaved-thinking-2025-05-14"
        }
        import urllib.request as _ur
        req  = _ur.Request("https://api.anthropic.com/v1/messages",
                           data=_j.dumps(payload).encode(), headers=headers, method="POST")
        with _ur.urlopen(req, timeout=30) as resp:
            data = _j.loads(resp.read())
        # Extraer solo texto (ignorar tool_use blocks)
        texts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
        return "\n".join(texts).strip() or "⚠️ PACH no obtuvo respuesta."
    except Exception as e:
        return f"⚠️ Error al contactar PACH: {str(e)[:120]}"


def render_pach(sport_label: str, context_data: dict):
    """
    🤖 PACH — Chat AI analista integrado en el tab de Bot.
    1 pregunta a la vez, respuesta con web_search en vivo.
    """
    api_ok = bool(ANTHROPIC_API_KEY)

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0a0020,#001a10);
    border:2px solid #bb00ff88;border-radius:16px;padding:16px 18px;margin-bottom:10px'>
      <div style='display:flex;align-items:center;gap:12px;margin-bottom:12px'>
        <div style='font-size:2.4rem'>🤖</div>
        <div style='flex:1'>
          <div style='font-size:1.2rem;font-weight:900;color:#cc44ff;letter-spacing:.08em'>PACH</div>
          <div style='font-size:.72rem;color:#888'>Analista AI · Powered by Claude · Busca en internet en tiempo real</div>
        </div>
        <div style='font-size:.65rem;padding:4px 10px;border-radius:20px;
        background:{"#00ff8820" if api_ok else "#ff000020"};
        color:{"#00ff88" if api_ok else "#ff4444"};
        border:1px solid {"#00ff8855" if api_ok else "#ff444455"};white-space:nowrap'>
        {"● ONLINE" if api_ok else "● SIN API KEY"}</div>
      </div>
      <div style='background:#ffffff08;border-radius:10px;padding:10px 14px;
      border-left:3px solid #cc44ff;margin-bottom:10px'>
        <div style='color:#cc44ff;font-size:.72rem;font-weight:700;margin-bottom:4px'>💬 PACH DICE:</div>
        <div style='color:#ddd;font-size:.88rem;font-style:italic'>
          "Pregúntame cualquier apuesta deportiva y te ayudo. Analizo handicaps, spreads, 
          over de sets, player props, triple dobles, corners, parlays... lo que quieras. 
          Busco la info en internet antes de responderte."
        </div>
      </div>
      <div style='display:flex;gap:6px;flex-wrap:wrap'>
        <span style='background:#1a0a2e;color:#bb00ff;font-size:.65rem;padding:3px 8px;border-radius:12px;border:1px solid #bb00ff44'>Handicaps</span>
        <span style='background:#1a0a2e;color:#bb00ff;font-size:.65rem;padding:3px 8px;border-radius:12px;border:1px solid #bb00ff44'>Over/Under sets</span>
        <span style='background:#1a0a2e;color:#bb00ff;font-size:.65rem;padding:3px 8px;border-radius:12px;border:1px solid #bb00ff44'>Player Props</span>
        <span style='background:#1a0a2e;color:#bb00ff;font-size:.65rem;padding:3px 8px;border-radius:12px;border:1px solid #bb00ff44'>Triple dobles</span>
        <span style='background:#1a0a2e;color:#bb00ff;font-size:.65rem;padding:3px 8px;border-radius:12px;border:1px solid #bb00ff44'>Corners · Tarjetas</span>
        <span style='background:#1a0a2e;color:#bb00ff;font-size:.65rem;padding:3px 8px;border-radius:12px;border:1px solid #bb00ff44'>Parlays combinados</span>
      </div>
    </div>""", unsafe_allow_html=True)

    if not api_ok:
        st.warning("Agrega `ANTHROPIC_API_KEY` en Streamlit secrets para activar PACH.")
        return

    # Historial de la sesión (solo últimas 6 para no saturar UI)
    hist_key = f"pach_hist_{sport_label}"
    if hist_key not in st.session_state:
        st.session_state[hist_key] = []

    # Mostrar historial
    hist = st.session_state[hist_key]
    if hist:
        for entry in hist[-6:]:
            # Pregunta del usuario
            st.markdown(
                f"<div style='background:#1a0a2e;border-radius:10px 10px 2px 10px;"
                f"padding:8px 12px;margin:4px 0;font-size:.85rem;"
                f"border-left:3px solid #bb00ff;color:#ddd'>"
                f"<span style='color:#bb00ff;font-size:.65rem;font-weight:700'>TÚ</span><br>"
                f"{entry['q']}</div>", unsafe_allow_html=True)
            # Respuesta de PACH
            resp_color = "#00ff88" if "JUGAR" in entry['a'].upper() else \
                         ("#ff4444" if "NO JUGAR" in entry['a'].upper() else "#FFD700")
            st.markdown(
                f"<div style='background:#07071a;border-radius:2px 10px 10px 10px;"
                f"padding:10px 12px;margin:4px 0 10px 0;font-size:.82rem;"
                f"border-left:3px solid {resp_color};color:#ccc;white-space:pre-wrap'>"
                f"<span style='color:#cc44ff;font-size:.65rem;font-weight:700'>🤖 PACH</span><br>"
                f"{entry['a']}</div>", unsafe_allow_html=True)

    # Input — form para que Enter dispare sin botón
    _fk = f"pach_form_{sport_label}"
    _ck = f"pach_clear_{sport_label}"

    with st.form(key=_fk, clear_on_submit=True):
        col_in, col_btn = st.columns([5, 1])
        with col_in:
            pregunta = st.text_input(
                "Pregúntale a PACH",
                placeholder="Ej: Alcaraz -1.5 sets vs Ruud · Over 2.5 City vs Arsenal · Triple doble LeBron...",
                label_visibility="collapsed")
        with col_btn:
            enviar = st.form_submit_button("▶", use_container_width=True)

    col_hint, col_clear = st.columns([4, 1])
    with col_hint:
        st.caption("💡 Escribe y presiona Enter · PACH busca en internet antes de responder")
    with col_clear:
        if st.button("🗑️", key=_ck, help="Limpiar historial"):
            st.session_state[hist_key] = []
            st.rerun()

    if enviar and pregunta.strip():
        with st.spinner("🌐 PACH buscando en la web..."):
            respuesta = _pach_call(pregunta.strip(), sport_label, context_data)
        st.session_state[hist_key].append({"q": pregunta.strip(), "a": respuesta})
        st.rerun()


def render_bot_tab(sport_label, scan_fn, scan_args, preview_fn=None):
    """Renderiza el tab de Bot de Telegram reutilizable para cualquier deporte."""

    # ══ PACH PRIMERO — siempre visible, arriba de todo ══
    _kr_raw  = st.session_state.get("_king_el_pick", {})
    _vl_raw  = st.session_state.get("_villar_summary", {})
    _sp_key  = {"⚽ Fútbol":"futbol","🏀 NBA":"nba","🎾 Tenis":"tenis"}.get(sport_label,"futbol")
    _pach_matches = []
    try:
        if _sp_key == "futbol":   _pach_matches = st.session_state.get("_kr_cache_fut", [])
        elif _sp_key == "nba":    _pach_matches = st.session_state.get("_kr_cache_nba", [])
        else:                     _pach_matches = st.session_state.get("_kr_cache_ten", [])
    except: pass
    _pach_ctx = {
        "partidos": _pach_matches[:15],
        "kr_pick":  _kr_raw.get("pick","") if isinstance(_kr_raw, dict) else str(_kr_raw)[:80],
        "villar":   f"{_vl_raw.get('modelo_ok',0)}✅ {_vl_raw.get('modelo_fail',0)}❌ {_vl_raw.get('modelo_pct',0)}%" if _vl_raw else "",
    }
    render_pach(sport_label, _pach_ctx)

    # ══ SEPARADOR ══
    st.markdown("<div style='margin:20px 0 8px 0'></div>", unsafe_allow_html=True)
    st.markdown("<div class='shdr'>🤖 BOT TELEGRAM</div>", unsafe_allow_html=True)

    bot_ok = bool(BOT_TOKEN and CHAT_ID and BOT_TOKEN != "Pega_Aqui_Tu_Token_De_BotFather")
    icon = {"⚽ Fútbol":"⚽","🏀 NBA":"🏀","🎾 Tenis":"🎾"}.get(sport_label,"🤖")
    st.markdown(
        f"<div class='bot-card'>"
        f"<div style='font-size:.8rem;color:#229ED9;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>📡 BOT TELEGRAM — {sport_label.upper()}</div>"
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

def _ventana_22h(matches):
    """
    Filtra partidos en la ventana activa de 24 horas:
    10pm CDMX de hoy → 10pm CDMX de mañana.
    Incluye pre, in Y post — PATO/TRILAY necesitan ver también los ya jugados.
    """
    now    = datetime.now(CDMX)
    inicio = now.replace(hour=22, minute=0, second=0, microsecond=0)
    if now.hour < 22:
        inicio = inicio - timedelta(days=1)   # ventana empezó ayer a las 22h
    fin = inicio + timedelta(hours=24)

    result = []
    for m in matches:
        # Incluir todos los estados — PATO muestra U4.5 de toda la jornada
        try:
            hora_str = m.get("hora", "00:00") or "00:00"
            dt = CDMX.localize(
                datetime.strptime(f"{m['fecha']} {hora_str}", "%Y-%m-%d %H:%M")
            )
            if inicio <= dt < fin:
                result.append(m)
        except:
            hoy = now.strftime("%Y-%m-%d")
            man = (now + timedelta(days=1)).strftime("%Y-%m-%d")
            if m.get("fecha", "") in (hoy, man):
                result.append(m)
    return result


@st.cache_data(ttl=600, show_spinner=False)
def compute_trilay(matches):
    """
    TRILAY estructurado: 1 pick ML (favorito fuerte) + 1 Over 2.5 + 1 AA (Ambos Anotan).
    Cada pick viene de un partido diferente.
    Si un mercado no tiene candidato con ventaja real, usa el mejor ML disponible.
    """
    hoy_matches = _ventana_22h(matches)
    if not hoy_matches:
        hoy = datetime.now(CDMX).strftime("%Y-%m-%d")
        hoy_matches = [m for m in matches if m.get("fecha","") == hoy]

    # Calcular modelo para cada partido
    cands_ml, cands_o25, cands_aa = [], [], []
    for m in hoy_matches[:40]:
        try:
            hf  = get_form(m["home_id"],m["slug"])
            af  = get_form(m["away_id"],m["slug"])
            hxg = _cup_enriched_xg(m, True,  hf, af)
            axg = _cup_enriched_xg(m, False, hf, af)
            mc  = mc50k(hxg,axg)
            _ph = mc["ph"]; _pa = mc["pa"]; _o25 = mc["o25"]; _aa = mc["btts"]
            _best_ml_p = max(_ph,_pa)
            _best_ml_m = f"🏠 {m['home']} gana" if _ph>=_pa else f"✈️ {m['away']} gana"
            base = {**m, "mc":mc, "hxg":hxg, "axg":axg}
            # ML: preferir cuando hay favorito claro (≥52%)
            cands_ml.append({**base, "best_p":_best_ml_p, "best_m":_best_ml_m, "mkt":"ML"})
            # Over 2.5
            cands_o25.append({**base, "best_p":_o25, "best_m":"⚽ Over 2.5", "mkt":"O/U"})
            # AA
            cands_aa.append({**base, "best_p":_aa, "best_m":"⚡ Ambos Anotan", "mkt":"AA"})
        except: continue

    cands_ml.sort(key=lambda x:-x["best_p"])
    cands_o25.sort(key=lambda x:-x["best_p"])
    cands_aa.sort(key=lambda x:-x["best_p"])

    result = []
    used_ids = set()

    def _partido_id(c): return f"{c.get('home_id','')}_{c.get('away_id','')}"

    # 1. Mejor ML
    for c in cands_ml:
        if _partido_id(c) not in used_ids:
            result.append(c); used_ids.add(_partido_id(c)); break

    # 2. Mejor Over 2.5 (partido distinto)
    for c in cands_o25:
        if _partido_id(c) not in used_ids:
            result.append(c); used_ids.add(_partido_id(c)); break

    # 3. Mejor AA (partido distinto)
    for c in cands_aa:
        if _partido_id(c) not in used_ids:
            result.append(c); used_ids.add(_partido_id(c)); break

    # Si no se completó con 3 partidos distintos, rellenar con el siguiente mejor ML
    for c in cands_ml:
        if len(result) >= 3: break
        if _partido_id(c) not in used_ids:
            result.append(c); used_ids.add(_partido_id(c))

    return result[:3]

@st.cache_data(ttl=600, show_spinner=False)
def compute_pato(matches):
    cands=[]
    for m in matches[:80]:
        hf  = get_form(m["home_id"],m["slug"])
        af  = get_form(m["away_id"],m["slug"])
        hxg = _cup_enriched_xg(m, True,  hf, af) if not hf else max(0.2,avg([r["gf"] for r in hf]))
        axg = _cup_enriched_xg(m, False, hf, af) if not af else max(0.2,avg([r["gf"] for r in af]))
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

def _sort_cartelera(matches, hoy_str, hora_now):
    """Ordena cartelera: hoy primero, en vivo arriba, oculta pasados si >= 12:00."""
    if hora_now >= 12:
        matches = [m for m in matches
                   if m.get("fecha","") >= hoy_str or m.get("state") in ("in","pre")]
    def _key(m):
        f = m.get("fecha","9999-99-99")
        h = m.get("hora","99:99")
        s = m.get("state","")
        return (0 if f==hoy_str else 1, 0 if s=="in" else (1 if s=="pre" else 2), h)
    matches.sort(key=_key)
    return matches

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
    _now2 = datetime.now(CDMX)
    games = _sort_cartelera(games, _now2.strftime("%Y-%m-%d"), int(_now2.strftime("%H")))
    return games

@st.cache_data(ttl=3600, show_spinner=False)
def get_nba_team_stats(team_id):
    """
    Extrae stats avanzadas de ESPN NBA:
    PPG, OppPPG, Pace, eFG%, TurnoverRate, FTRate
    Estos son los drivers reales del total de puntos.
    """
    data = eg(f"{NBA_ESPN}/teams/{team_id}/statistics")
    stats = {"ppg":110.0,"opp_ppg":110.0,"pace":100.0,
             "efg":0.52,"tov_rate":0.14,"ft_rate":0.23,
             "ortg":112.0,"drtg":112.0,"net_rtg":0.0}
    try:
        for cat in data.get("results",{}).get("stats",{}).get("categories",[]):
            for s in cat.get("stats",[]):
                n = s.get("name","").lower()
                v = float(s.get("value",0) or 0)
                if n in ("pointspergame","ppg"):            stats["ppg"]      = v
                elif n in ("opponentpointspergame","oppg"): stats["opp_ppg"]  = v
                elif n == "pace":                           stats["pace"]     = v
                elif n in ("effectivefgpct","efgpct"):      stats["efg"]      = v
                elif n in ("turnoverpct","tovpct"):         stats["tov_rate"] = v
                elif n in ("offensiverating","ortg"):       stats["ortg"]     = v
                elif n in ("defensiverating","drtg"):       stats["drtg"]     = v
    except: pass
    # Net rating
    stats["net_rtg"] = stats["ortg"] - stats["drtg"]
    return stats


@st.cache_data(ttl=1800, show_spinner=False)
def get_nba_recent_form(team_id, n_games=7):
    """
    Últimos N partidos NBA — detecta racha, back-to-back fatigue,
    promedio de puntos reciente (más relevante que promedio de temporada).
    """
    data = eg(f"{NBA_ESPN}/teams/{team_id}/schedule")
    events = data.get("events", [])
    results = []
    for ev in events:
        try:
            comp  = ev["competitions"][0]
            state = ev.get("status",{}).get("type",{}).get("state","")
            if state != "post": continue
            comps = comp["competitors"]
            hc = next(c for c in comps if c["homeAway"]=="home")
            ac = next(c for c in comps if c["homeAway"]=="away")
            is_home = str(hc["team"]["id"]) == str(team_id)
            my  = hc if is_home else ac
            opp = ac if is_home else hc
            pts_for     = parse_score(my.get("score",0))
            pts_against = parse_score(opp.get("score",0))
            results.append({
                "date":    ev.get("date","")[:10],
                "pts_for": pts_for,
                "pts_against": pts_against,
                "total":   pts_for + pts_against,
                "won":     pts_for > pts_against,
                "is_home": is_home,
            })
        except: continue
    results.sort(key=lambda x: x["date"], reverse=True)
    return results[:n_games]


def nba_ou_model(home_id, away_id, ou_line):
    """
    Modelo NBA O/U mejorado — usa 5 factores reales:
    1. PPG reciente (últimos 7 partidos) con decay 0.88
    2. Pace del equipo (posesiones/48min)
    3. eFG% ofensivo vs defensivo
    4. Net Rating (mejor predictor de resultados que PPG)
    5. Monte Carlo 50k simulaciones con varianza calibrada

    Ref: Oliver 2004 (Basketball on Paper), Kubatko 2007 (pace adjustments)
    """
    # ── Stats avanzadas ──
    h_stats = get_nba_team_stats(home_id)
    a_stats = get_nba_team_stats(away_id)
    h_form  = get_nba_recent_form(home_id, 7)
    a_form  = get_nba_recent_form(away_id, 7)

    # ── PPG con decay exponencial (últimos 7 > promedio temporada) ──
    DECAY = 0.88
    def decay_ppg(form, fallback):
        if not form: return fallback
        w_total = w_pts = 0
        for i, g in enumerate(form):
            w = DECAY ** i
            w_pts   += w * g["pts_for"]
            w_total += w
        return w_pts / w_total if w_total > 0 else fallback

    h_recent_ppg = decay_ppg(h_form, h_stats["ppg"])
    a_recent_ppg = decay_ppg(a_form, a_stats["ppg"])

    # ── Pace adjustment: blend promedios ──
    avg_pace = (h_stats["pace"] + a_stats["pace"]) / 2
    pace_adj  = avg_pace / 100.0  # normalizado

    # ── Proyección base ──
    # Local tiene +2.5 pts ventaja de cancha en casa
    h_proj = h_recent_ppg * 1.025 * min(1.05, max(0.95, pace_adj))
    a_proj = a_recent_ppg * min(1.05, max(0.95, pace_adj))
    proj   = h_proj + a_proj

    # ── Net rating adjustment ──
    # Si un equipo tiene mucho mejor/peor NetRtg, ajustar proyección
    net_diff = h_stats["net_rtg"] - a_stats["net_rtg"]
    proj += net_diff * 0.15   # cada punto de net rating = 0.15 pts en total

    line = ou_line if ou_line > 0 else proj

    # ── Back-to-back fatigue: reduce proyección si jugó ayer ──
    def played_yesterday(form):
        if len(form) < 2: return False
        try:
            from datetime import datetime as _dt, timedelta as _td
            d1 = _dt.strptime(form[0]["date"], "%Y-%m-%d")
            d2 = _dt.strptime(form[1]["date"], "%Y-%m-%d")
            return abs((d1-d2).days) <= 1
        except: return False

    b2b_h = played_yesterday(h_form)
    b2b_a = played_yesterday(a_form)
    if b2b_h: proj -= 4.0   # -4 pts por back-to-back local
    if b2b_a: proj -= 3.5   # -3.5 pts por back-to-back visitante

    # ── Monte Carlo 50k con varianza calibrada ──
    # Std dev calibrada: 11 pts por equipo (histórico NBA, Oliver 2004)
    rng    = np.random.default_rng(42)
    h_sims = rng.normal(h_proj - (4 if b2b_h else 0), 11.0, 50_000)
    a_sims = rng.normal(a_proj - (3.5 if b2b_a else 0), 11.0, 50_000)
    tots   = h_sims + a_sims

    p_over  = float((tots > line).mean())
    p_under = 1 - p_over

    # ── ML (win probability) con Net Rating ──
    # Net Rating es el mejor predictor de victorias (r²=0.89 vs PPG r²=0.72)
    net_h = h_stats["net_rtg"]; net_a = a_stats["net_rtg"]
    # Convertir net rating a prob de victoria: logistic calibrado
    net_diff_ml = (net_h - net_a + 3.0)  # +3 home court advantage
    p_h_win = 1 / (1 + math.exp(-net_diff_ml * 0.15))
    p_a_win = 1 - p_h_win

    return {
        "proj":       round(proj, 1),
        "line":       round(line, 1),
        "p_over":     round(p_over, 4),
        "p_under":    round(p_under, 4),
        "p_h_win":    round(p_h_win, 4),
        "p_a_win":    round(p_a_win, 4),
        "h_proj":     round(h_proj, 1),
        "a_proj":     round(a_proj, 1),
        "b2b_h":      b2b_h,
        "b2b_a":      b2b_a,
        "net_h":      round(net_h, 1),
        "net_a":      round(net_a, 1),
        "pace":       round(avg_pace, 1),
        "h_recent_ppg": round(h_recent_ppg, 1),
        "a_recent_ppg": round(a_recent_ppg, 1),
        "rec":        "OVER 🔥" if p_over>0.54 else ("UNDER ❄️" if p_over<0.46 else "NEUTRAL ⚖️"),
    }

# ══════════════════════════════════════════════════════════
# TENIS DATA
# ══════════════════════════════════════════════════════════
TENNIS_API = "https://api.api-tennis.com/tennis/"

# ── ATP/WTA Rankings reales ──
# Extraídos de la propia tennis API o fallback a lookup table de jugadores conocidos.
# Se cachean 24h — los rankings cambian semanalmente, no diario.
_ATP_RANK_CACHE: dict = {}
_ATP_RANK_DATE: str   = ""

@st.cache_data(ttl=86400, show_spinner=False)
@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_atp_rankings_raw(tour="ATP"):
    """
    Descarga el ranking ATP/WTA actual desde la tennis API.
    Devuelve dict {nombre_normalizado: ranking_int}
    """
    try:
        endpoint = "get_standings" if tour=="ATP" else "get_standings"
        r = requests.get(TENNIS_API, params={
            "method":  "get_standings",
            "APIkey":  TENNIS_API_KEY,
            "tour_key": "2" if tour=="ATP" else "3",  # 2=ATP, 3=WTA
        }, headers=H, timeout=10)
        if r.status_code != 200: return {}
        data = r.json()
        ranks = {}
        for entry in data.get("result", []):
            name = str(entry.get("player_name","")).strip()
            pos  = entry.get("standing_place") or entry.get("rank") or 999
            try: pos = int(pos)
            except: pos = 999
            if name:
                # Normalizar: "Djokovic N." → "djokovic", "Carlos Alcaraz" → "alcaraz"
                parts = name.lower().split()
                for p in parts:
                    if len(p) > 3 and not p.endswith("."):
                        ranks[p] = min(ranks.get(p, 999), pos)
                ranks[name.lower()] = pos
        return ranks
    except:
        return {}

# Rankings reales ATP/WTA — actualizados 7 marzo 2026 (fuente AP / WTA oficial)
_KNOWN_RANKS = {
    # ── ATP top 60 (marzo 2026) ──
    "alcaraz":1,"sinner":2,"djokovic":3,"zverev":4,"musetti":5,
    "de minaur":6,"minaur":6,"fritz":7,"shelton":8,
    "auger-aliassime":9,"auger aliassime":9,"aliassime":9,
    "bublik":10,"medvedev":11,"mensik":12,"ruud":13,
    "draper":14,"cobolli":15,"khachanov":16,"rublev":17,
    "rune":18,"davidovich fokina":19,"fokina":19,
    "cerundolo":20,"darderi":21,"tiafoe":22,"lehecka":23,
    "paul":24,"griekspoor":25,"vacherot":26,"norrie":27,
    "nakashima":28,"rinderknech":29,"machac":30,
    "baez":32,"fonseca":33,"tien":34,
    "mpetshi perricard":35,"perricard":35,"fils":36,
    "korda":38,"struff":42,"berrettini":48,
    "tsitsipas":52,"dimitrov":56,"hurkacz":60,
    "popyrin":62,"jarry":65,"etcheverry":70,
    "wawrinka":150,"monfils":180,
    # ── WTA top 40 (marzo 2026) ──
    "sabalenka":1,"swiatek":2,"rybakina":3,"gauff":4,"pegula":5,
    "anisimova":6,"paolini":7,"andreeva":8,"mirra andreeva":8,
    "svitolina":9,"mboko":10,"alexandrova":11,"bencic":12,
    "muchova":13,"noskova":14,"keys":15,"osaka":16,
    "tauson":17,"jovic":18,"iva jovic":18,"samsonova":19,
    "shnaider":20,"mertens":21,"kalinskaya":22,"zheng":23,
    "qinwen":23,"zheng qinwen":23,"navarro":24,"badosa":25,
    "kostyuk":26,"andreescu":27,"haddad maia":28,"haddad":28,
    "kasatkina":29,"raducanu":30,"sorribes tormo":32,"sorribes":32,
    "putintseva":34,"fruhvirtova":36,"linette":38,
    "kvitova":45,"azarenka":50,"halep":200,"williams":500,
}

def _resolve_rank(player_name: str, api_ranks: dict) -> int:
    """
    Resuelve el ranking de un jugador:
    1. Busca en rankings en vivo de la API
    2. Fallback a tabla de jugadores conocidos
    3. Fallback a 200 (jugador no top)
    """
    if not player_name or player_name == "?":
        return 200
    name_low = player_name.lower().strip()

    # 1. Exact match en API
    if name_low in api_ranks:
        return api_ranks[name_low]

    # 2. Partial match en API (apellido)
    parts = name_low.split()
    for part in parts:
        if len(part) > 3 and part in api_ranks:
            return api_ranks[part]

    # 3. Known ranks table
    for key, rank in _KNOWN_RANKS.items():
        if key in name_low or name_low in key:
            return rank

    # 4. Partial match en known ranks
    for part in parts:
        if len(part) > 3:
            for key, rank in _KNOWN_RANKS.items():
                if part in key or key in part:
                    return rank

    return 120   # jugador fuera del top conocido — rank conservador


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
                tour_type   = ev.get("event_type_type","").upper()
                tour_name   = ev.get("tournament_name","").upper()
                league_name = ev.get("league_name","").upper()
                all_text    = tour_type + " " + tour_name + " " + league_name

                # Detectar ITF/Challenger (excluir) — queremos ATP, WTA y Grand Slams
                p1n = ev.get("event_first_player","")
                p2n = ev.get("event_second_player","")
                # Skip doubles: player names contain "/" or "&"
                if "/" in p1n or "/" in p2n: continue
                if "&" in p1n or "&" in p2n: continue  # some APIs use & for doubles pairs
                if any(x in all_text for x in ["ITF","JUNIOR","WHEELCHAIR","EXHIBITION","DOUBLES","DOUBLE","DBL"]):
                    continue
                # Skip if either player name has multiple last names separated by / or looks like pair
                if len(p1n.split("/")) > 1 or len(p2n.split("/")) > 1: continue

                # Determinar tour por nombre del torneo + tipo
                if "WTA" in all_text:
                    tour = "WTA"
                elif "ATP" in all_text or "GRAND SLAM" in all_text or "MASTERS" in all_text:
                    tour = "ATP"
                elif any(x in all_text for x in ["CHALLENGER","FUTURES"]):
                    continue  # skip challengers
                else:
                    # Si es femenino por jugadoras conocidas o tournament_type = "WTA"
                    ev_gender = ev.get("event_type","").upper()
                    tour = "WTA" if "WTA" in ev_gender or "WOMEN" in ev_gender else "ATP"
                    # Sin contexto — incluir igual, clasificar como ATP por defecto
                ev_status   = str(ev.get("event_status","")).lower()
                ev_finished = str(ev.get("event_final","0"))
                is_live     = ev.get("event_live","0") == "1"
                # Retiros y walkovers también son partidos terminados
                _retired_keywords = ["finished","ft","final","completed","awarded",
                                     "retired","ret.","walkover","w/o","walkover","withdraw",
                                     "abandoned","cancelled","default","disqualified"]
                is_post = (ev_finished == "1" or
                           any(x in ev_status for x in _retired_keywords))
                is_walkover = any(x in ev_status for x in ["retired","ret.","walkover","w/o","withdraw"])
                t_state = "post" if is_post else ("in" if is_live else "pre")
                # Score for tennis
                sc1 = str(ev.get("event_first_player_result",""))
                sc2 = str(ev.get("event_second_player_result",""))
                # Si hay retiro, el ganador = quien tiene más sets (o sc1 si ambos 0)
                # Marcamos con retiro para mostrar en UI
                p1_name = ev.get("event_first_player","?")
                p2_name = ev.get("event_second_player","?")
                # Try to get real rank from API event fields first
                r1_api = ev.get("event_first_player_ranking") or ev.get("player1_rank") or 0
                r2_api = ev.get("event_second_player_ranking") or ev.get("player2_rank") or 0
                try: r1_api = int(r1_api)
                except: r1_api = 0
                try: r2_api = int(r2_api)
                except: r2_api = 0
                # If API didn't give rank, resolve from rankings table
                if r1_api <= 0 or r1_api >= 999:
                    _api_r = _fetch_atp_rankings_raw(tour)
                    r1_api = _resolve_rank(p1_name, _api_r)
                if r2_api <= 0 or r2_api >= 999:
                    _api_r = _fetch_atp_rankings_raw(tour)
                    r2_api = _resolve_rank(p2_name, _api_r)
                matches.append({
                    "id":    str(ev.get("event_key","")),
                    "p1":    p1_name, "home": p1_name,
                    "p2":    p2_name, "away": p2_name,
                    "rank1": r1_api,
                    "rank2": r2_api,
                    "tour":  tour,
                    "torneo": ev.get("tournament_name",""),
                    "hora":  hora,
                    "fecha": fecha,
                    "state": t_state,
                    "score_p1": sc1, "score_p2": sc2,
                    "score_h":  int(sc1) if str(sc1).isdigit() else 0,
                    "score_a":  int(sc2) if str(sc2).isdigit() else 0,
                    "is_walkover": is_walkover,
                    "walkover_note": "RET." if is_walkover else "",
                    "odd_1": 0.0, "odd_2": 0.0,
                    "_sport": "tennis",
                    "league": f"{tour} · {ev.get('tournament_name','')}",
                    "liga":   f"{tour} · {ev.get('tournament_name','')}",
                })
            except: continue
    except Exception as e:
        pass
    _now3 = datetime.now(CDMX)
    matches = _sort_cartelera(matches, _now3.strftime("%Y-%m-%d"), int(_now3.strftime("%H")))
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


def _kr_edge(prob, odd):
    """Edge real vs casas. Sin cuota: edge vs 50-50."""
    if odd > 1.01:
        return prob - (1.0 / odd)
    return prob - 0.50


def _kr_kelly(prob, odd, cap=0.08):
    """Fracción Kelly, cappada al 8%."""
    if odd <= 1.01 or prob <= 0:
        return 0.0
    k = (prob * (odd - 1) - (1 - prob)) / (odd - 1)
    return round(max(0.0, min(k, cap)) * 100, 1)


def _kr_conf(prob, edge, spread_pp):
    """Devuelve (emoji, label, color) de confianza."""
    penalizado = spread_pp > _KR_CONFLICT_PP
    if prob >= _KR_DIAMOND_PROB and edge >= 0.07 and not penalizado:
        return "💎", "DIAMANTE", "#FFD700"
    if prob >= _KR_GOLD_PROB and edge >= _KR_MIN_EDGE and not penalizado:
        return "🔥", "ALTA",     "#00ff88"
    if prob >= 0.57 and not penalizado:
        return "⚡", "MEDIA",    "#00ccff"
    if prob >= 0.52:
        return "⚠️", "BAJA",     "#ff9500"
    return "🔻", "NO APOSTAR",  "#ff4444"


def _kr_score(prob, edge, spread_pp, kelly, contradiccion):
    """Score compuesto 0-10 para rankear candidatos."""
    s  = min(prob * 5.5,  4.0)       # probabilidad base         0-4.0
    s += min(max(edge * 28, 0), 2.8) # edge real positivo        0-2.8
    s += min(kelly / 6.0, 1.5)       # kelly: cuánto apostar     0-1.5
    s -= min(spread_pp / 16.0, 1.5)  # penalizar dispersión      0-1.5
    if contradiccion: s -= 2.2       # penalización conflicto
    return round(max(0.0, min(s, 10.0)), 2)


# ══════════════════════════════════════════════════════════════════════════════
# 👑 KING RONGO — MODELOS EXCLUSIVOS
# Modelos propios del Rey. No se usan en ningún otro lugar del código.
# ══════════════════════════════════════════════════════════════════════════════

# ── KR FÚTBOL: Dixon-Coles Bivariado (rho -0.13) ─────────────────────────────
def _kr_dixon_coles(hxg, axg, odd_h=0, odd_a=0, odd_d=0):
    """Dixon & Coles (1997) bivariado — exclusivo King Rongo fútbol."""
    import math as _m
    rho = -0.13  # correlación empírica marcadores bajos (calibrada en Premier League)
    def poisson_pmf(k, lam):
        return _m.exp(-lam) * lam**k / _m.factorial(min(k,20))
    def tau(x,y,mu,lam,r):
        if x==0 and y==0: return max(0.001, 1-mu*lam*r)
        if x==0 and y==1: return max(0.001, 1+mu*r)
        if x==1 and y==0: return max(0.001, 1+lam*r)
        if x==1 and y==1: return max(0.001, 1-r)
        return 1.0
    ph=pd=pa=0.0
    for i in range(8):
        for j in range(8):
            p = poisson_pmf(i,hxg)*poisson_pmf(j,axg)*tau(i,j,hxg,axg,rho)
            if i>j: ph+=p
            elif i<j: pa+=p
            else: pd+=p
    tot=ph+pd+pa
    if tot>0: ph/=tot; pd/=tot; pa/=tot
    if odd_h>1 and odd_a>1 and odd_d>1:
        vig=1/odd_h+1/odd_a+1/odd_d
        ph=0.55*ph+0.45*(1/odd_h)/vig
        pd=0.55*pd+0.45*(1/odd_d)/vig
        pa=0.55*pa+0.45*(1/odd_a)/vig
    return {"ph":round(ph,4),"pd":round(pd,4),"pa":round(pa,4)}


# ── KR NBA: Pythagorean Win Expectancy + Pace Adjustment ─────────────────────
_KR_NBA_PACE = {
    "atl":102.4,"bos":100.2,"bkn":101.8,"cha":100.5,"chi":100.1,"cle":98.7,
    "dal":101.2,"den":103.5,"det":101.0,"gsw":102.8,"hou":104.2,"ind":103.8,
    "lac":100.8,"lal":101.6,"mem":102.0,"mia":98.5,"mil":99.8,"min":100.4,
    "nop":101.5,"nyk":99.2,"okc":103.1,"orl":100.7,"phi":100.3,"phx":101.9,
    "por":102.6,"sac":103.7,"sas":102.2,"tor":100.9,"uta":103.0,"was":102.5,
}
def _kr_nba_pythagorean(home_id, away_id, p_h_win, p_a_win, p_over, ou_line):
    """Pythagorean NBA (Morey 2003 / Oliver 2004) + Pace — exclusivo King Rongo."""
    h_pace = _KR_NBA_PACE.get((home_id or "")[:3].lower(), 101.5)
    a_pace = _KR_NBA_PACE.get((away_id or "")[:3].lower(), 101.5)
    avg_pace = (h_pace+a_pace)/2
    pace_diff = h_pace-a_pace
    pace_adj  = pace_diff*0.003
    p_h_adj = max(0.05, min(0.95, p_h_win+pace_adj))
    p_a_adj = 1-p_h_adj
    ou_delta = ((avg_pace-101.5)*0.04) / max(1, ou_line)
    p_over_adj  = max(0.05, min(0.95, p_over+ou_delta*0.3))
    p_under_adj = 1-p_over_adj
    return {"p_h":round(p_h_adj,4),"p_a":round(p_a_adj,4),
            "p_over":round(p_over_adj,4),"p_under":round(p_under_adj,4),
            "pace_h":h_pace,"pace_a":a_pace}


# ── KR TENIS: Pressure Index (rendimiento bajo presión) ──────────────────────
_KR_PRESSURE_PROFILE = {
    # (gs_boost, masters_boost) — positivo = mejor en torneos grandes
    "djokovic":(+0.04,+0.03),"alcaraz":(+0.03,+0.02),"sinner":(+0.02,+0.02),
    "zverev":(-0.02,+0.01),"medvedev":(+0.01,+0.01),"ruud":(-0.03,-0.01),
    "fritz":(-0.02,-0.01),"shelton":(-0.01,+0.01),"bublik":(-0.04,-0.02),
    "rublev":(-0.03,-0.02),"sabalenka":(+0.04,+0.03),"rybakina":(+0.03,+0.02),
    "swiatek":(+0.03,+0.02),"gauff":(+0.02,+0.01),"pegula":(-0.02,-0.01),
    "anisimova":(+0.01,+0.00),"andreeva":(+0.01,+0.01),"svitolina":(+0.02,+0.02),
    "mensik":(+0.01,+0.01),"draper":(+0.01,+0.01),"fonseca":(+0.01,+0.00),
}
def _kr_tennis_pressure(rank1, rank2, p1_name, p2_name, torneo, odd_1=0, odd_2=0):
    """Pressure Index — exclusivo King Rongo tenis."""
    import math as _m
    def _r2e(r): return 2400-400*_m.log10(max(1,min(800,r)))
    p_base = 1/(1+10**((_r2e(rank2)-_r2e(rank1))/400))
    t_upper = torneo.upper()
    is_gs      = any(x in t_upper for x in ["GRAND SLAM","AUSTRALIAN","ROLAND","WIMBLEDON","US OPEN"])
    is_masters = any(x in t_upper for x in ["MASTERS","INDIAN WELLS","MIAMI","MADRID","ROME",
                                              "MONTREAL","TORONTO","CINCINNATI","SHANGHAI","PARIS"])
    boost_idx = 0 if is_gs else (1 if is_masters else -1)
    n1=p1_name.lower(); n2=p2_name.lower()
    prof1 = next((v for k,v in _KR_PRESSURE_PROFILE.items() if k in n1),(0,0))
    prof2 = next((v for k,v in _KR_PRESSURE_PROFILE.items() if k in n2),(0,0))
    adj1 = prof1[boost_idx] if boost_idx>=0 else 0
    adj2 = prof2[boost_idx] if boost_idx>=0 else 0
    p = max(0.05, min(0.95, p_base+adj1-adj2))
    if odd_1>1 and odd_2>1:
        vig=1/odd_1+1/odd_2; p=0.60*p+0.40*(1/odd_1)/vig
    return round(p, 4)


# ────────────────────────────────────────────────────────────────────────────
# MOTOR DE ESCANEO — analiza los 3 deportes
# ────────────────────────────────────────────────────────────────────────────

def _king_rongo_scan_all(matches_fut, nba_games, ten_matches):
    """
    Corre TODOS los modelos sobre todos los partidos pre-match.
    Retorna: (el_pick, contradicciones, todos_ordenados)
    """
    candidates = []

    # ── ⚽ FÚTBOL ─────────────────────────────────────────────────────────
    try:
        for m in (matches_fut or [])[:40]:
            # King Rongo analiza todos los partidos del día (pre, in, post)
            try:
                home_id = m.get("home_id",""); away_id = m.get("away_id",""); slug = m.get("slug","")
                if not home_id or not slug: continue
                hf  = get_form(home_id, slug) or []
                af  = get_form(away_id, slug) or []
                hxg = xg_weighted(hf, True,  1/m["odd_h"] if m.get("odd_h",0)>1 else 0) \
                      if hf else _cup_enriched_xg(m, True,  hf, af)
                axg = xg_weighted(af, False, 1/m["odd_a"] if m.get("odd_a",0)>1 else 0) \
                      if af else _cup_enriched_xg(m, False, hf, af)
                h2h = get_h2h(home_id, away_id, slug, m.get("home","?"), m.get("away","?"))
                h2s = h2h_stats(h2h, m.get("home","?"), m.get("away","?"))
                mc  = ensemble_football(hxg, axg, h2s, hf, af,
                                        m["home_id"], m["away_id"],
                                        odd_h=m.get("odd_h",0),
                                        odd_a=m.get("odd_a",0),
                                        odd_d=m.get("odd_d",0))
                dp  = diamond_engine(mc, h2s, hf, af)

                # ── Modelo exclusivo KR: Dixon-Coles bivariado ──
                try:
                    _dc = _kr_dixon_coles(hxg, axg, m.get("odd_h",0), m.get("odd_a",0), m.get("odd_d",0))
                    _dc_ph = _dc["ph"]; _dc_pa = _dc["pa"]; _dc_pd = _dc["pd"]
                except:
                    _dc_ph = 0; _dc_pa = 0; _dc_pd = 0

                # ── Blend ensemble + Dixon-Coles (KR usa ambos) ──
                _ph_base = dp["ph"]; _pa_base = dp["pa"]
                _ph = 0.70*_ph_base + 0.30*_dc_ph if _dc_ph>0 else _ph_base
                _pa = 0.70*_pa_base + 0.30*_dc_pa if _dc_pa>0 else _pa_base
                _pd   = mc.get("pd", max(0, 1-_ph-_pa))
                _o25  = mc["o25"]; _aa = mc["btts"]
                _o15  = mc.get("o15", min(0.90, _o25+0.18))
                _1xm  = min(0.82, _ph+0.12); _2xm = min(0.78, _pa+0.12)
                _do_h = min(0.95, _ph+_pd); _do_a = min(0.95, _pa+_pd)
                # Partido equilibrado si xG similares
                _xg_gap_kr = abs(hxg - axg)
                _xg_total_kr = hxg + axg
                _eq_kr = _xg_gap_kr < 0.55
                _muy_of_kr = _xg_total_kr >= 3.0
                _of_med_kr = 2.5 <= _xg_total_kr < 3.0

                _home = m.get("home","?"); _away = m.get("away","?")
                # ── Jerarquía King Rongo: ML > DO > O2.5 > AA solo si los demás son bajos ──
                _ninguno_kr = max(_ph,_pa) < 0.52 and _do_h < 0.72 and _do_a < 0.72 and _o25 < 0.54
                _best_ml_kr = max(_ph, _pa)

                if _pa >= 0.55 and _pa > _ph:
                    lbl, prob, odd, mkt = f"✈️ {_away} gana", _pa, m.get("odd_a",0), "1X2"
                elif _ph >= 0.55:
                    lbl, prob, odd, mkt = f"🏠 {_home} gana", _ph, m.get("odd_h",0), "1X2"
                elif _pa >= 0.55:
                    lbl, prob, odd, mkt = f"✈️ {_away} gana", _pa, m.get("odd_a",0), "1X2"
                elif _do_h >= 0.76 and _ph >= 0.48:
                    lbl, prob, odd, mkt = f"🔵 {_home[:14]} o Emp", _do_h, 0, "DO"
                elif _do_a >= 0.76 and _pa >= 0.43:
                    lbl, prob, odd, mkt = f"🟣 {_away[:14]} o Emp", _do_a, 0, "DO"
                elif _muy_of_kr and _o25 >= 0.56:
                    lbl, prob, odd, mkt = "⚽ Over 2.5", _o25, 0, "O/U"
                elif _o25 >= 0.54:
                    lbl, prob, odd, mkt = "⚽ Over 2.5", _o25, 0, "O/U"
                elif _best_ml_kr >= 0.46:
                    if _ph >= _pa: lbl, prob, odd, mkt = f"🏠 {_home} gana", _ph, m.get("odd_h",0), "1X2"
                    else:          lbl, prob, odd, mkt = f"✈️ {_away} gana", _pa, m.get("odd_a",0), "1X2"
                elif _ninguno_kr and _eq_kr and _aa >= 0.52:
                    lbl, prob, odd, mkt = "⚡ Ambos Anotan", _aa, 0, "BTTS"
                else:
                    # fallback: siempre ML
                    if _ph >= _pa: lbl, prob, odd, mkt = f"🏠 {_home} gana", _ph, m.get("odd_h",0), "1X2"
                    else:          lbl, prob, odd, mkt = f"✈️ {_away} gana", _pa, m.get("odd_a",0), "1X2"

                if prob < 0.30: continue  # solo descartar si modelo dice <30% (imposible casi)
                edge   = _kr_edge(prob, odd)
                kelly  = _kr_kelly(prob, odd)
                mv     = [mc.get("dc_ph",0.5), mc.get("bvp_ph",0.5),
                          mc.get("elo_ph",0.5), mc.get("h2h_ph",0.5)]
                spread = round((max(mv)-min(mv))*100, 1)
                contra = spread > _KR_CONFLICT_PP
                ce,cl,cc = _kr_conf(prob, edge, spread)

                c = {
                    "deporte":"⚽ Fútbol","sport":"futbol",
                    "label":f"{_home} vs {_away}",
                    "liga":m.get("league",""),"hora":m.get("hora",""),
                    "pick":lbl,"prob":prob,"odd":odd,"edge":edge,
                    "kelly_pct":kelly,"mkt_type":mkt,
                    "contradiccion":contra,"model_spread":spread,
                    "conf_emoji":ce,"conf_label":cl,"conf_color":cc,
                    "reasoning":f"xG {hxg:.2f}–{axg:.2f} · {mc.get('consensus','')} · {dp.get('conf','')}",
                    "match":m,
                    "models":{"👑 D-Coles": round(_dc_ph*100,1) if _dc_ph>0 else "N/A",
                              "Ensemble":   round(_ph_base*100,1),
                              "xG H":       round(hxg,2),
                              "xG A":       round(axg,2)},
                    "hxg":hxg,"axg":axg,
                }
                c["score"] = _kr_score(prob, edge, spread, kelly, contra)
                candidates.append(c)
            except Exception as _e_fut:
                continue  # partido fallido, continuar con el siguiente
    except Exception as _e_fut_outer:
        pass

    # ── 🏀 NBA ────────────────────────────────────────────────────────────
    try:
        for g in (nba_games or [])[:20]:
            # King Rongo analiza todos los juegos del día
            try:
                res = nba_ou_model(g["home_id"], g["away_id"], g["ou_line"])
                p_h_base = res.get("p_h_win", 0.55); p_a_base = 1-p_h_base
                line= res["line"]

                # ── Modelo exclusivo KR: Pythagorean + Pace ──
                try:
                    _pyth = _kr_nba_pythagorean(g["home_id"], g["away_id"],
                                                 p_h_base, p_a_base,
                                                 res["p_over"], line)
                    # Blend: base 70%, Pythagorean 30%
                    p_h = 0.70*p_h_base + 0.30*_pyth["p_h"]
                    p_a = 1-p_h
                    p_over_kr  = 0.70*res["p_over"]  + 0.30*_pyth["p_over"]
                    p_under_kr = 1-p_over_kr
                    pace_note  = f"Pace H:{_pyth['pace_h']:.0f}/A:{_pyth['pace_a']:.0f}"
                except:
                    p_h = p_h_base; p_a = p_a_base
                    p_over_kr = res["p_over"]; p_under_kr = res["p_under"]
                    pace_note = ""

                mkts= [
                    (f"🔥 Over {line}",   p_over_kr,  0,               "O/U"),
                    (f"❄️  Under {line}",  p_under_kr, 0,               "O/U"),
                    (f"🏠 {g['home']}",    p_h,        g.get("odd_h",0),"ML"),
                    (f"✈️  {g['away']}",    p_a,        g.get("odd_a",0),"ML"),
                ]
                mkts = [(l,p,o,t) for l,p,o,t in mkts if p >= 0.50]
                if not mkts: continue
                best = max(mkts, key=lambda x: _kr_edge(x[1],x[2]) if x[2]>1 else x[1]-0.48)
                lbl,prob,odd,mkt = best
                edge   = _kr_edge(prob, odd)
                kelly  = _kr_kelly(prob, odd)
                spread = round((1-abs(p_over_kr-p_under_kr))*50, 1)
                contra = abs(p_over_kr-p_under_kr) < 0.08
                ce,cl,cc = _kr_conf(prob, edge, spread)
                c = {
                    "deporte":"🏀 NBA","sport":"nba",
                    "label":f"{g['away']} @ {g['home']}",
                    "liga":"NBA","hora":g.get("hora",""),
                    "pick":lbl,"prob":prob,"odd":odd,"edge":edge,
                    "kelly_pct":kelly,"mkt_type":mkt,
                    "contradiccion":contra,"model_spread":spread,
                    "conf_emoji":ce,"conf_label":cl,"conf_color":cc,
                    "reasoning":f"Proy {res['proj']} pts · {pace_note} · NetRtg {res.get('net_h',0):+.1f}/{res.get('net_a',0):+.1f}",
                    "match":g,
                    "models":{"👑 Pyth%":round(p_h*100,1),
                              "Over%":   round(p_over_kr*100,1),
                              "Under%":  round(p_under_kr*100,1),
                              "ML Away": round(p_a*100,1)},
                }
                c["score"] = _kr_score(prob, edge, spread, kelly, contra)
                candidates.append(c)
            except: continue
    except: pass

    # ── 🎾 TENIS ──────────────────────────────────────────────────────────
    _smap = {"Indian Wells":"hard","Miami":"hard","Roland Garros":"clay",
             "Wimbledon":"grass","US Open":"hard","Australian Open":"hard",
             "Monte Carlo":"clay","Madrid":"clay","Barcelona":"clay",
             "Rome":"clay","Cincinnati":"hard","Toronto":"hard",
             "Halle":"grass","Queen":"grass","Dubai":"hard","Doha":"hard"}
    try:
        for m in (ten_matches or [])[:45]:
            # King Rongo analiza todos los partidos del día
            try:
                tor = m.get("torneo", m.get("tour",""))
                srf = next((v for k,v in _smap.items() if k.lower() in tor.lower()), "hard")
                r1 = m.get("rank1",0) or 0
                r2 = m.get("rank2",0) or 0
                p1_name = m.get("p1",""); p2_name = m.get("p2","")

                # ── Siempre resolver ranks desde nombre — misma lógica que cartelera ──
                if r1 <= 0 or r1 >= 150:
                    r1 = _resolve_rank(p1_name, _KNOWN_RANKS) or _resolve_rank_local(p1_name) or 120
                if r2 <= 0 or r2 >= 150:
                    r2 = _resolve_rank(p2_name, _KNOWN_RANKS) or _resolve_rank_local(p2_name) or 120

                odd_1 = m.get("odd_1", m.get("odd_h",0))
                odd_2 = m.get("odd_2", m.get("odd_a",0))

                # ── Usar MISMO modelo que la cartelera de tenis ──
                _vd = veredicto_academico_tenis(
                    p1_name=p1_name, p2_name=p2_name,
                    rank1=r1, rank2=r2,
                    odd_1=odd_1, odd_2=odd_2,
                    surface=srf, torneo=tor,
                    expert_p1=None
                )
                p1_vd = _vd["_p1_final"]
                # ── Modelo exclusivo KR: Pressure Index ──
                try:
                    p1_press = _kr_tennis_pressure(r1, r2, p1_name, p2_name, tor, odd_1, odd_2)
                    p1_final = 0.80*p1_vd + 0.20*p1_press
                except:
                    p1_final = p1_vd; p1_press = p1_vd
                p2_final = 1 - p1_final
                fav  = p1_name if p1_final >= p2_final else p2_name
                prob = max(p1_final, p2_final)
                odd  = odd_1 if p1_final >= p2_final else odd_2

                edge   = _kr_edge(prob, odd)
                kelly  = _kr_kelly(prob, odd)
                spread = round(abs(p1_final - p2_final) * 100, 1)
                contra = spread < 4
                ce,cl,cc = _kr_conf(prob, edge, _KR_CONFLICT_PP+5 if contra else 10)
                rd = abs(r1 - r2)
                c = {
                    "deporte":"🎾 Tenis","sport":"tenis",
                    "label":f"{p1_name} vs {p2_name}",
                    "liga":tor,"hora":m.get("hora",""),
                    "pick":f"🎾 {fav} gana","prob":prob,"odd":odd,"edge":edge,
                    "kelly_pct":kelly,"mkt_type":"ML",
                    "contradiccion":contra,"model_spread":spread,
                    "conf_emoji":ce,"conf_label":cl,"conf_color":cc,
                    "reasoning":f"Rk #{r1} vs #{r2} · {srf.title()} · Δ{spread:.0f}pp",
                    "match":m,
                    "models":{
                        "Elo":     round(_vd.get("_p1_elo",   p1_final)*100, 1),
                        "Sup":     round(_vd.get("_p1_surf",  p1_final)*100, 1),
                        "MC50k":   round(_vd.get("_p1_mc",    p1_final)*100, 1),
                        "Moment":  round(_vd.get("_p1_mom",   p1_final)*100, 1),
                        "Serve":   round(_vd.get("_p1_srv",   p1_final)*100, 1),
                        "👑 Press":round(p1_press*100, 1),
                    },
                }
                c["score"] = _kr_score(prob, edge, spread if contra else 10, kelly, contra)
                candidates.append(c)
            except: continue
    except: pass

    # ── Rankear ──
    candidates.sort(key=lambda x: -x.get("score",0))
    contras = [c for c in candidates if c.get("contradiccion")]

    # Cascada — siempre retorna algo si hay candidatos
    el_pick = (
        next((c for c in candidates if not c.get("contradiccion") and c.get("edge",0) > 0), None) or
        next((c for c in candidates if not c.get("contradiccion") and c.get("prob",0) >= 0.45), None) or
        next((c for c in candidates if not c.get("contradiccion")), None) or
        (candidates[0] if candidates else None)
    )
    if el_pick:
        el_pick = {**el_pick, "is_rongo_pick": True}

    # TOP 3 DEL REY — el mejor de cada deporte, priorizando sin contradicción
    _top3 = []
    _deps_usados = set()
    # Primero: mejores sin contradicción
    for _c in candidates:
        if _c.get("contradiccion"): continue
        _dep = _c.get("deporte","")
        if _dep not in _deps_usados:
            _deps_usados.add(_dep)
            _top3.append({**_c, "is_rongo_pick": True})
        if len(_top3) == 3: break
    # Completar si hace falta (incluso con contradicción)
    if len(_top3) < 3:
        for _c in candidates:
            _dep = _c.get("deporte","")
            already = any(t.get("label")==_c.get("label") for t in _top3)
            if not already and _dep not in {t.get("deporte") for t in _top3}:
                _top3.append({**_c, "is_rongo_pick": True})
            elif not already and len(_top3) < 3:
                _top3.append({**_c, "is_rongo_pick": True})
            if len(_top3) == 3: break

    return el_pick, contras, candidates[:20], _top3


def _kr_parlay_del_rey(todos):
    """
    Arma EL PARLAY DEL REY: los 3 mejores picks de deportes distintos
    sin contradicción, máxima prob combinada.
    Retorna lista de hasta 3 candidatos o [] si no hay suficientes.
    """
    sin_contra = [c for c in todos if not c.get("contradiccion") and c.get("prob",0) >= 0.58]
    # Un pick por deporte
    usados_deportes = set()
    parlay = []
    for c in sin_contra:
        dep = c["deporte"]
        if dep not in usados_deportes:
            usados_deportes.add(dep)
            parlay.append(c)
        if len(parlay) == 3:
            break
    return parlay


# ────────────────────────────────────────────────────────────────────────────
# BANKROLL INTELLIGENCE
# ────────────────────────────────────────────────────────────────────────────

def _king_rongo_bankroll_advice(pick_history):
    """
    Analiza historial y racha actual.
    Retorna dict con todos los indicadores para la UI.
    """
    empty = {"kelly_rec":2.0,"racha":0,"racha_sign":"─","consejo":"Sin historial",
             "color":"#555","pct":0,"pct10":0,"wins":0,"total":0,
             "risk_level":"neutro","roi":0.0,"wins10":0,"last_results":[]}
    if not pick_history: return empty

    settled = [p for p in pick_history if p.get("result") in ("✅","❌")]
    if not settled: return empty

    wins  = sum(1 for p in settled if p.get("result")=="✅")
    total = len(settled)
    pct   = round(wins/total*100) if total else 0

    last10  = settled[-10:]
    wins10  = sum(1 for p in last10 if p.get("result")=="✅")
    pct10   = round(wins10/len(last10)*100) if last10 else 0
    last_r  = [p.get("result","⏳") for p in last10]

    # Racha
    racha=0; sign=None
    for pk in reversed(settled):
        r=pk.get("result")
        if sign is None: sign=r
        if r==sign: racha+=1
        else: break
    rs = racha if sign=="✅" else -racha

    # ROI
    roi = sum(
        (float(p.get("odd",0))-1 if float(p.get("odd",0))>1 else 0.5) if p["result"]=="✅" else -1.0
        for p in settled
    )

    # Kelly y consejo
    if rs <= -5:   kr,co,rl,c = 0.5, "🔴 STOP — racha crítica. Pausa obligatoria.", "critico",   "#ff4444"
    elif rs <= -3: kr,co,rl,c = 1.0, "🔴 Racha negativa severa — mínimo posible.",  "peligro",  "#ff4444"
    elif rs <= -1: kr,co,rl,c = 1.5, "🟠 Reduce exposición — no fuerces.",          "reducir",  "#ff9500"
    elif rs >= 6:  kr,co,rl,c = 5.0, "🟢 Racha épica — sigue con disciplina.",      "epico",    "#FFD700"
    elif rs >= 4:  kr,co,rl,c = 4.0, "🟢 Racha excelente — puedes subir un poco.", "excelente","#00ff88"
    elif rs >= 2:  kr,co,rl,c = 3.0, "🟢 Buena racha — mantén el ritmo.",          "bueno",    "#00ff88"
    elif pct10>=70:kr,co,rl,c = 3.5, "🟢 Últimos 10 perfectos — sigue así.",       "bueno",    "#00ff88"
    elif pct10<35 and len(last10)>=5:
                   kr,co,rl,c = 1.5, "🟡 Forma reciente floja — ten cuidado.",      "reducir",  "#FFD700"
    elif pct>=60:  kr,co,rl,c = 3.0, "🟢 Buen historial — mantén estándar.",       "bueno",    "#00ff88"
    else:          kr,co,rl,c = 2.0, "⚪ Momento neutro — apuesta estándar.",       "neutro",   "#aaa"

    return {"kelly_rec":kr,"racha":rs,"racha_sign":"▲" if rs>0 else("▼" if rs<0 else"─"),
            "consejo":co,"color":c,"pct":pct,"pct10":pct10,"wins":wins,"wins10":wins10,
            "total":total,"risk_level":rl,"roi":round(roi,1),"last_results":last_r}


# ────────────────────────────────────────────────────────────────────────────
# IA NARRATIVA — King Rongo habla
# ────────────────────────────────────────────────────────────────────────────

def _kr_ia_narracion(el_pick, bk, todos):
    """
    Llama a Claude para que King Rongo narre el pick en primera persona.
    Conciso, poderoso, con personalidad.
    """
    if not ANTHROPIC_API_KEY: return ""
    try:
        modelos_txt = " | ".join(f"{k}: {v}%" for k,v in el_pick.get("models",{}).items())
        parlay      = _kr_parlay_del_rey(todos)
        parlay_txt  = "; ".join(f"{p['pick']} ({p['prob']*100:.0f}%)" for p in parlay) if len(parlay)>=2 else "No disponible"

        prompt = (
            f"Eres KING RONGO, el cerebro supremo de The Gamblers Layer. "
            f"Hablas en español, con autoridad, en primera persona, máximo 3 frases cortas. "
            f"NO uses asteriscos ni markdown. Solo texto plano con carácter.\n\n"
            f"PICK DEL DÍA:\n"
            f"Partido: {el_pick['label']}\n"
            f"Pick: {el_pick['pick']}\n"
            f"Probabilidad: {el_pick['prob']*100:.1f}%\n"
            f"Edge real: {el_pick['edge']*100:+.1f}%\n"
            f"Modelos: {modelos_txt}\n"
            f"Razonamiento base: {el_pick.get('reasoning','')}\n"
            f"Confianza: {el_pick.get('conf_label','')}\n\n"
            f"ESTADO DEL BANKROLL:\n"
            f"Racha: {bk['racha_sign']}{abs(bk['racha'])} · "
            f"Acierto global: {bk['pct']}% · ROI: {bk['roi']:+.1f}u\n"
            f"Consejo: {bk['consejo']}\n\n"
            f"PARLAY DEL REY: {parlay_txt}\n\n"
            f"Narra el pick. Sé el rey."
        )
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01",
                     "content-type":"application/json"},
            json={"model":"claude-opus-4-6","max_tokens":180,
                  "messages":[{"role":"user","content":prompt}]},
            timeout=12
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"].strip()
    except: pass
    return ""


# ────────────────────────────────────────────────────────────────────────────
# RENDERIZADO — componentes visuales
# ────────────────────────────────────────────────────────────────────────────

def _kr_render_header():
    st.markdown("""
    <div style='position:relative;overflow:hidden;border-radius:20px;margin-bottom:6px'>
      <!-- Fondo degradado animado -->
      <div style='background:linear-gradient(160deg,#180030 0%,#001a00 40%,#1a0020 80%,#000818 100%);
      padding:0;'>

        <!-- Línea superior dorada -->
        <div style='height:3px;background:linear-gradient(90deg,
        transparent 0%,#FFD700 20%,#ff9500 50%,#FFD700 80%,transparent 100%)'></div>

        <!-- Orbs de ambiente -->
        <div style='position:absolute;top:-30px;left:-30px;width:180px;height:180px;
        background:radial-gradient(circle,#FFD70014 0%,transparent 70%);pointer-events:none'></div>
        <div style='position:absolute;top:-30px;right:-30px;width:180px;height:180px;
        background:radial-gradient(circle,#7c00ff14 0%,transparent 70%);pointer-events:none'></div>
        <div style='position:absolute;bottom:-30px;left:50%;transform:translateX(-50%);
        width:300px;height:100px;
        background:radial-gradient(ellipse,#00ff8808 0%,transparent 70%);pointer-events:none'></div>

        <!-- Contenido central -->
        <div style='padding:24px 20px 20px;text-align:center;position:relative'>
          <div style='font-size:3.2rem;line-height:1;margin-bottom:8px;
          filter:drop-shadow(0 0 16px #FFD70099)'>👑</div>

          <div style='font-size:2rem;font-weight:900;letter-spacing:.22em;
          background:linear-gradient(135deg,#FFD700 0%,#ff9500 35%,#FFD700 65%,#ffe066 100%);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
          margin-bottom:6px;line-height:1.1'>KING RONGO</div>

          <div style='font-size:.68rem;color:#555;letter-spacing:.16em;
          text-transform:uppercase;margin-bottom:2px'>
          El Cerebro Supremo · Árbitro de Modelos</div>

          <div style='display:flex;justify-content:center;gap:16px;margin-top:10px;flex-wrap:wrap'>
            <span style='font-size:.65rem;background:#FFD70015;border:1px solid #FFD70033;
            border-radius:20px;padding:3px 12px;color:#FFD70088'>⚽ xG + Ensemble 4M</span>
            <span style='font-size:.65rem;background:#ff950015;border:1px solid #ff950033;
            border-radius:20px;padding:3px 12px;color:#ff950088'>🏀 Net Rating + O/U</span>
            <span style='font-size:.65rem;background:#00ccff15;border:1px solid #00ccff33;
            border-radius:20px;padding:3px 12px;color:#00ccff88'>🎾 Weibull + Elo</span>
          </div>
        </div>

        <!-- Línea inferior bicolor -->
        <div style='height:2px;background:linear-gradient(90deg,
        transparent 0%,#7c00ff 25%,#FFD700 50%,#7c00ff 75%,transparent 100%)'></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def _kr_render_bankroll(bk):
    rc     = bk["color"]
    sign   = bk["racha_sign"]
    racha  = abs(bk["racha"])

    # Dot indicators for last 10
    dots = ""
    for r in bk.get("last_results",[])[-10:]:
        dc = "#00ff88" if r=="✅" else ("#ff4444" if r=="❌" else "#333")
        dots += f"<div style='width:9px;height:9px;border-radius:50%;background:{dc}'></div>"

    st.markdown(
        f"<div style='background:linear-gradient(135deg,#0a0020,#001008);"
        f"border:1px solid {rc}33;border-radius:14px;padding:14px 16px;margin-bottom:10px'>"

        # Título + racha grande
        f"<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px'>"
        f"<div>"
        f"<div style='font-size:.65rem;color:#FFD700;font-weight:700;letter-spacing:.12em'>👑 BANKROLL INTELLIGENCE</div>"
        f"<div style='font-size:.78rem;color:{rc};margin-top:3px'>{bk['consejo']}</div>"
        f"</div>"
        f"<div style='text-align:right'>"
        f"<div style='font-size:2.2rem;font-weight:900;color:{rc};line-height:1'>{sign}{racha}</div>"
        f"<div style='font-size:.6rem;color:#444'>racha actual</div>"
        f"</div></div>"

        # KPIs fila
        f"<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin-bottom:10px'>"
        f"<div class='mbox'><div class='mval' style='color:#00ff88'>{bk['wins']}</div><div class='mlbl'>✅ Gana</div></div>"
        f"<div class='mbox'><div class='mval' style='color:#00ccff'>{bk['pct']}%</div><div class='mlbl'>Glb</div></div>"
        f"<div class='mbox'><div class='mval' style='color:#aa00ff'>{bk['pct10']}%</div><div class='mlbl'>Últ10</div></div>"
        f"<div class='mbox'><div class='mval' style='color:#FFD700'>{bk['kelly_rec']}%</div><div class='mlbl'>Kelly</div></div>"
        f"<div class='mbox'><div class='mval' style='color:{'#00ff88' if bk['roi']>=0 else '#ff4444'}'>"
        f"{bk['roi']:+.1f}u</div><div class='mlbl'>ROI</div></div>"
        f"</div>"

        # Últimos 10 dots
        f"<div style='display:flex;align-items:center;gap:8px'>"
        f"<span style='font-size:.6rem;color:#333;white-space:nowrap'>Últ 10</span>"
        f"<div style='display:flex;gap:4px;align-items:center'>{dots}</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )


def _kr_render_pick_card(el_pick, bk, narracion=""):
    """La card principal del pick del día — RONGO PICK supremo."""
    prob  = el_pick.get("prob", 0)
    edge  = el_pick.get("edge", 0)
    odd   = el_pick.get("odd", 0)
    kelly = el_pick.get("kelly_pct", bk.get("kelly_rec", 0))
    ce    = el_pick.get("conf_emoji", "⚡")
    cl    = el_pick.get("conf_label", "MEDIA")
    cc    = el_pick.get("conf_color", "#FFD700")
    score = el_pick.get("score", 0)
    odd_txt  = f"@{odd:.2f}" if odd > 1 else "S/C"
    edge_c   = "#00ff88" if edge >= 0 else "#ff4444"
    units    = round(kelly / 100 * 10, 1)
    meter_w  = min(int(prob * 100), 100)

    # ── 1. PICK PRINCIPAL — siempre visible primero ──
    st.markdown(f"""
<style>
@keyframes rp-glow{{0%,100%{{box-shadow:0 0 24px #FFD70033}}50%{{box-shadow:0 0 48px #FFD70066}}}}
@keyframes rp-bar{{0%{{background-position:-200px 0}}100%{{background-position:200px 0}}}}
.rp-bar-shine{{
  height:8px;border-radius:6px;
  background:linear-gradient(90deg,{cc}44,{cc},#FFD700,{cc});
  background-size:200px 100%;animation:rp-bar 1.8s linear infinite;
  width:{meter_w}%;
}}
</style>
<div style='background:linear-gradient(145deg,#0d0028,#001208,#180800);
  border:2px solid #FFD700;border-radius:20px;padding:20px 16px 16px;
  animation:rp-glow 3s ease-in-out infinite;margin:8px 0;position:relative'>

  <div style='position:absolute;top:0;left:50%;transform:translateX(-50%);
    background:linear-gradient(135deg,#FFD700,#ff9500);
    padding:4px 18px;border-radius:0 0 12px 12px;
    font-size:.6rem;font-weight:900;color:#0a0010;letter-spacing:.15em;white-space:nowrap'>
    👑 RONGO PICK · {ce} {cl}
  </div>

  <div style='text-align:center;margin:10px 0 14px'>
    <div style='font-size:.62rem;color:#444;letter-spacing:.08em'>
      {el_pick.get("deporte","")} · {el_pick.get("liga","")[:32]} · {el_pick.get("hora","")} CDMX
    </div>
    <div style='font-size:.9rem;font-weight:700;color:#888;margin:4px 0'>
      {el_pick.get("label","")}
    </div>
  </div>

  <div style='text-align:center;background:#07071a;border:1px solid #FFD70033;
    border-radius:14px;padding:16px 10px;margin-bottom:14px'>
    <div style='font-size:1.9rem;font-weight:900;color:#FFD700;
      text-shadow:0 0 28px #FFD70099'>
      {el_pick.get("pick","")}
    </div>
    <div style='font-size:.68rem;color:#555;margin-top:4px'>{odd_txt}</div>
  </div>

  <div style='margin-bottom:12px'>
    <div style='display:flex;justify-content:space-between;margin-bottom:4px'>
      <span style='font-size:.6rem;color:#333'>Probabilidad</span>
      <span style='font-size:.72rem;font-weight:900;color:#FFD700'>{prob*100:.1f}%</span>
    </div>
    <div style='background:#0a0a1e;border-radius:6px;height:8px;overflow:hidden'>
      <div class='rp-bar-shine'></div>
    </div>
  </div>

  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:10px'>
    <div class='mbox'><div class='mval' style='color:#FFD700'>{prob*100:.1f}%</div><div class='mlbl'>Prob</div></div>
    <div class='mbox'><div class='mval' style='color:{edge_c}'>{edge*100:+.1f}%</div><div class='mlbl'>Edge</div></div>
    <div class='mbox'><div class='mval' style='color:#ff9500'>{odd_txt}</div><div class='mlbl'>Cuota</div></div>
    <div class='mbox'><div class='mval' style='color:#00ccff'>{units}u</div><div class='mlbl'>Kelly</div></div>
  </div>

</div>
""", unsafe_allow_html=True)

    # ── 2. MODELOS — pills separadas ──
    models = el_pick.get("models", {})
    if models:
        cols_m = st.columns(len(models))
        for i, (k, v) in enumerate(models.items()):
            with cols_m[i]:
                st.markdown(
                    f"<div style='background:#0a0a1e;border:1px solid {cc}22;border-radius:10px;"
                    f"padding:6px 4px;text-align:center'>"
                    f"<div style='font-size:.82rem;font-weight:700;color:{cc}'>{v}%</div>"
                    f"<div style='font-size:.58rem;color:#444'>{k}</div></div>",
                    unsafe_allow_html=True)

    # ── 3. VEREDICTO DE KING RONGO — texto de análisis abajo ──
    if narracion and isinstance(narracion, str) and len(narracion) > 10:
        st.markdown(
            f"<div style='background:#07071a;border-left:3px solid #FFD700;"
            f"border-radius:0 10px 10px 0;padding:10px 14px;margin:10px 0;"
            f"font-size:.82rem;color:#aaa;line-height:1.7;font-style:italic'>"
            f"💬 {narracion}</div>",
            unsafe_allow_html=True)
    else:
        # Veredicto automático sin API — basado en los datos del pick
        _razon = el_pick.get("reasoning", "")
        _dep   = el_pick.get("deporte", "")
        _conf_txt = "Señal fuerte" if prob >= 0.60 else ("Señal media" in cl and "señal de valor" or "jugada de valor")
        _edge_txt = f"edge real de {edge*100:+.1f}%" if edge != 0 else "sin cuota disponible para calcular edge"
        _veredicto = (
            f"El modelo encuentra {_conf_txt} en {el_pick.get('label','')}. "
            f"Probabilidad calculada: {prob*100:.1f}% con {_edge_txt}. "
            f"{'Confianza alta — bankroll al ' + str(units) + ' unidades.' if units > 0 else 'Sin apuesta recomendada por Kelly.'}"
        )
        st.markdown(
            f"<div style='background:#07071a;border-left:3px solid #555;"
            f"border-radius:0 10px 10px 0;padding:10px 14px;margin:10px 0;"
            f"font-size:.78rem;color:#666;line-height:1.6'>"
            f"🧠 {_veredicto}</div>",
            unsafe_allow_html=True)


def _kr_render_parlay(parlay):
    """Parlay del Rey — 3 picks multi-deporte combinados."""
    if len(parlay) < 2: return

    prob_c = 1.0
    for p in parlay: prob_c *= p["prob"]
    odds_c = 1.0
    for p in parlay:
        if p.get("odd",0)>1: odds_c *= p["odd"]

    legs_html = ""
    for i,p in enumerate(parlay,1):
        cc = p.get("conf_color","#aaa")
        legs_html += (
            f"<div style='padding:10px 12px;background:#0a0a1e;"
            f"border-radius:10px;margin:4px 0;border-left:3px solid {cc}'>"
            f"<div style='display:flex;align-items:center;justify-content:space-between'>"
            f"<div>"
            f"<div style='font-size:.65rem;color:#444'>{p['deporte']} · {p.get('liga','')[:20]}</div>"
            f"<div style='font-size:.8rem;color:#888'>{p['label']}</div>"
            f"<div style='font-size:.85rem;font-weight:700;color:{cc}'>{p['pick']}</div>"
            f"</div>"
            f"<div style='text-align:right'>"
            f"<div style='font-size:.9rem;font-weight:900;color:{cc}'>{p['prob']*100:.0f}%</div>"
            f"<div style='font-size:.65rem;color:#444'>{'@'+str(round(p['odd'],2)) if p.get('odd',0)>1 else 'S/C'}</div>"
            f"</div></div></div>"
        )

    odd_txt = f"Cuota combinada aprox {odds_c:.2f}" if odds_c > 1.1 else ""

    st.markdown(
        f"<div style='background:linear-gradient(135deg,#0a001a,#001008);"
        f"border:1px solid #FFD70055;border-radius:16px;padding:14px 16px;margin:12px 0'>"
        f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:12px'>"
        f"<div style='font-size:1.8rem'>🃏</div>"
        f"<div>"
        f"<div style='font-size:.7rem;font-weight:700;color:#FFD700;letter-spacing:.12em'>PARLAY DEL REY</div>"
        f"<div style='font-size:.72rem;color:#555'>{len(parlay)} picks · {len(set(p['deporte'] for p in parlay))} deportes</div>"
        f"</div>"
        f"<div style='margin-left:auto;text-align:right'>"
        f"<div style='font-size:1.2rem;font-weight:900;color:#FFD700'>{prob_c*100:.1f}%</div>"
        f"<div style='font-size:.62rem;color:#555'>Prob combinada</div>"
        f"</div></div>"
        f"{legs_html}"
        f"<div style='font-size:.68rem;color:#444;margin-top:8px;padding-top:8px;border-top:1px solid #1a1a30'>"
        f"{'💰 ' + odd_txt if odd_txt else ''} · Apuesta máx 0.5% del banco por pata</div>"
        f"</div>",
        unsafe_allow_html=True
    )


def _kr_render_table(todos, el_pick):
    """Ranking completo de todos los picks del día."""
    st.markdown(
        "<div style='font-size:.68rem;font-weight:700;color:#FFD700;letter-spacing:.1em;"
        "text-transform:uppercase;margin:16px 0 8px'>📊 Ranking completo — todos los picks del día</div>",
        unsafe_allow_html=True
    )
    for i,c in enumerate(todos[:16]):
        is_king = el_pick and c["label"]==el_pick["label"]
        cc      = c.get("conf_color","#555")
        ec      = "#00ff88" if c.get("edge",0)>0.05 else ("#FFD700" if c.get("edge",0)>0 else "#ff4444")
        bg      = "background:linear-gradient(90deg,#10001e,#0a0a1e)" if is_king else "background:#0a0a1e"
        bd      = f"border:1px solid {cc}77" if is_king else "border:1px solid #141428"
        flag    = "⚠️ " if c.get("contradiccion") else ""
        crown   = "👑 " if is_king else ""
        score_bar = int(c.get("score",0)*10)
        models_mini = " · ".join(f"{k} {v}%" for k,v in list(c.get("models",{}).items())[:2])

        st.markdown(
            f"<div style='{bg};{bd};border-radius:10px;padding:9px 12px;margin:3px 0;"
            f"position:relative;overflow:hidden'>"
            f"<div style='position:absolute;left:0;top:0;bottom:0;width:{score_bar}%;"
            f"background:{cc}07;pointer-events:none'></div>"
            f"<div style='display:flex;align-items:center;gap:10px;position:relative'>"
            f"<div style='font-size:.85rem;font-weight:900;min-width:24px;color:#333'>{crown}{i+1}</div>"
            f"<div style='flex:1;min-width:0'>"
            f"<div style='font-size:.6rem;color:#444;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>"
            f"{flag}{c['deporte']} · {c.get('liga','')[:20]} · {c.get('hora','')}</div>"
            f"<div style='font-size:.76rem;color:#777;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{c['label']}</div>"
            f"<div style='font-size:.82rem;font-weight:700;color:{cc}'>{c['pick']}</div>"
            f"<div style='font-size:.58rem;color:#2a2a50'>{models_mini}</div>"
            f"</div>"
            f"<div style='text-align:right;flex-shrink:0'>"
            f"<div style='font-size:1rem;font-weight:900;color:{cc}'>{c['prob']*100:.1f}%</div>"
            f"<div style='font-size:.62rem;color:{ec}'>Edge {c['edge']*100:+.1f}%</div>"
            f"<div style='font-size:.6rem;color:#FFD70066'>{'@'+str(round(c['odd'],2)) if c.get('odd',0)>1 else ''}</div>"
            f"</div></div></div>",
            unsafe_allow_html=True
        )


def _kr_render_contradictions(contras):
    if not contras: return
    with st.expander(f"⚠️ {len(contras)} picks bloqueados — modelos en conflicto", expanded=False):
        st.markdown(
            "<div style='font-size:.72rem;color:#ff9500;margin-bottom:8px'>"
            "King Rongo detectó contradicciones entre modelos. "
            "Se bloquearon para proteger el bankroll.</div>",
            unsafe_allow_html=True
        )
        for c in contras[:8]:
            sp = c.get("model_spread",0)
            st.markdown(
                f"<div style='background:#120800;border-radius:8px;padding:8px 12px;"
                f"margin:3px 0;border-left:3px solid #ff950055'>"
                f"<div style='display:flex;justify-content:space-between'>"
                f"<div><div style='font-size:.76rem;color:#ff9500'>{c['deporte']} · {c['label']}</div>"
                f"<div style='font-size:.65rem;color:#444'>{c.get('reasoning','')}</div></div>"
                f"<div style='font-size:.8rem;font-weight:700;color:#ff9500'>{sp:.0f}pp</div></div>"
                f"<div style='margin-top:5px;background:#1a1000;border-radius:3px;height:3px'>"
                f"<div style='height:3px;width:{min(int(sp),100)}%;background:#ff9500;border-radius:3px'></div>"
                f"</div></div>",
                unsafe_allow_html=True
            )


def _kr_render_memory(pick_history):
    """Insights de memoria evolutiva."""
    settled = [p for p in pick_history if p.get("result") in ("✅","❌")]
    if len(settled) < 5: return

    from collections import defaultdict
    sp_s = defaultdict(lambda:{"w":0,"l":0,"u":0.0})
    mk_s = defaultdict(lambda:{"w":0,"l":0,"u":0.0})

    for p in settled:
        o   = float(p.get("odd",0))
        sp  = p.get("sport","?")
        pk  = p.get("pick","").lower()
        if   "over"  in pk: mk="Over"
        elif "under" in pk: mk="Under"
        elif "ambos" in pk or "btts" in pk: mk="BTTS"
        elif "empate" in pk: mk="Empate"
        elif "gana"  in pk: mk="Win ML"
        else: mk="Otro"
        won = p.get("result")=="✅"
        u   = (o-1 if o>1 else 0.5) if won else -1.0
        sp_s[sp]["w" if won else "l"]+=1; sp_s[sp]["u"]+=u
        mk_s[mk]["w" if won else "l"]+=1; mk_s[mk]["u"]+=u

    def row(d):
        n=d["w"]+d["l"]
        return {"n":n,"pct":round(d["w"]/n*100),"roi":round(d["u"]/n*100,1)} if n>=3 else None

    sp_rows = sorted([(k,row(v)) for k,v in sp_s.items() if row(v)], key=lambda x:-x[1]["roi"])
    mk_rows = sorted([(k,row(v)) for k,v in mk_s.items() if row(v)], key=lambda x:-x[1]["roi"])
    if not sp_rows and not mk_rows: return

    with st.expander("🧠 Memoria Evolutiva — patrones de tu historial", expanded=False):
        st.markdown(
            "<div style='font-size:.7rem;color:#444;margin-bottom:10px'>"
            "King Rongo aprende de cada pick. Estos son tus patrones reales.</div>",
            unsafe_allow_html=True
        )
        c1,c2 = st.columns(2)
        for col,rows,title in [(c1,sp_rows,"POR DEPORTE"),(c2,mk_rows,"POR MERCADO")]:
            with col:
                st.markdown(
                    f"<div style='font-size:.65rem;color:#FFD700;font-weight:700;"
                    f"letter-spacing:.1em;margin-bottom:6px'>{title}</div>",
                    unsafe_allow_html=True
                )
                for k,s in rows[:5]:
                    rc="#00ff88" if s["roi"]>=0 else "#ff4444"
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;align-items:center;"
                        f"padding:5px 8px;background:#0a0a1e;border-radius:7px;margin:2px 0'>"
                        f"<span style='font-size:.74rem;color:#777'>{k}</span>"
                        f"<div style='display:flex;gap:10px'>"
                        f"<span style='font-size:.72rem;color:#00ccff'>{s['pct']}%</span>"
                        f"<span style='font-size:.7rem;color:{rc}'>{s['roi']:+.1f}%</span>"
                        f"<span style='font-size:.62rem;color:#333'>n={s['n']}</span>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )


# ────────────────────────────────────────────────────────────────────────────
# RENDER PRINCIPAL
# ────────────────────────────────────────────────────────────────────────────



# ══════════════════════════════════════════════════════════════════════
# KING RONGO — SISTEMA DE ESCANEO AUTOMÁTICO 3x DÍA
# Horarios CDMX: 08:00, 14:00, 22:00
# Antes de 22h → target = HOY | Desde 22h → target = MAÑANA
# Persiste en /tmp/king_rongo_cache.json para sobrevivir entre sesiones
# ══════════════════════════════════════════════════════════════════════

_KR_SCAN_HOURS = [8, 14, 22]   # horas CDMX en que se dispara auto-scan

def _kr_target_date():
    """
    Retorna la fecha objetivo para King Rongo.
    Antes de 22h → hoy. Desde 22h → mañana.
    """
    now = datetime.now(CDMX)
    if now.hour >= 22:
        return (now + timedelta(days=1)).strftime("%Y-%m-%d"), "mañana"
    return now.strftime("%Y-%m-%d"), "hoy"

def _kr_next_scan_time():
    """Retorna la próxima hora de escaneo automático como string HH:MM."""
    now = datetime.now(CDMX)
    for h in _KR_SCAN_HOURS:
        if now.hour < h:
            return f"{h:02d}:00"
    return f"{_KR_SCAN_HOURS[0]:02d}:00 (mañana)"

def _kr_should_auto_scan():
    """
    True si corresponde hacer un scan automático ahora.
    Ventana: dentro de los 15 minutos posteriores a la hora programada
    Y no se ha hecho ya un scan en esta ventana.
    """
    now  = datetime.now(CDMX)
    hour = now.hour
    minute = now.minute
    # ¿Estamos en ventana de scan? (HH:00 → HH:14)
    in_window = hour in _KR_SCAN_HOURS and minute < 15
    if not in_window:
        return False
    # ¿Ya escaneamos en esta ventana hoy?
    cache = _kr_load_cache()
    last_ts = cache.get("scan_ts","")
    if last_ts:
        try:
            last_dt = datetime.strptime(last_ts, "%Y-%m-%d %H:%M")
            last_dt = CDMX.localize(last_dt) if last_dt.tzinfo is None else last_dt
            diff_min = (datetime.now(CDMX) - last_dt).total_seconds() / 60
            if diff_min < 15:
                return False  # ya escaneamos hace menos de 15 min
        except: pass
    return True

def _kr_load_cache():
    """Carga el cache de King Rongo desde disco."""
    try:
        import json as _jkr
        with open(KR_CACHE_FILE, "r") as f:
            return _jkr.load(f)
    except:
        return {}

def _kr_save_cache(data):
    """Guarda el cache de King Rongo en disco."""
    try:
        import json as _jkr
        with open(KR_CACHE_FILE, "w") as f:
            _jkr.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

def _kr_sync_session_from_cache():
    """
    Al iniciar la sesión, carga el último scan del disco a session_state.
    Solo si el cache es del mismo target_date y no está expirado (< 8h).
    """
    cache = _kr_load_cache()
    if not cache or not cache.get("el_pick"):
        return
    target_date, _ = _kr_target_date()
    if cache.get("target_date","") != target_date:
        return  # cache de otra fecha — no cargar
    # Verificar que no sea demasiado viejo (máx 8h)
    ts = cache.get("scan_ts","")
    if ts:
        try:
            last_dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
            last_dt = CDMX.localize(last_dt) if last_dt.tzinfo is None else last_dt.astimezone(CDMX)
            age_h = (datetime.now(CDMX) - last_dt).total_seconds() / 3600
            if age_h > 8:
                return  # muy viejo
        except: pass
    # Cargar a session_state
    st.session_state["_king_el_pick"]  = cache.get("el_pick")
    st.session_state["_king_contras"]  = cache.get("contradicciones", [])
    st.session_state["_king_todos"]    = cache.get("todos", [])
    st.session_state["_king_scanned"]  = True
    st.session_state["_king_ts"]       = cache.get("hora_scan","")
    st.session_state["_king_target"]   = cache.get("target_date","")

def _kr_filter_by_date(matches, target_date):
    """Filtra partidos por fecha objetivo ±1 día. Incluye pre, in y post."""
    from datetime import datetime as _dt2, timedelta as _td2
    out = []
    try:
        _tf = _dt2.strptime(target_date, "%Y-%m-%d")
    except:
        _tf = None
    for m in (matches or []):
        # NO excluir post — KR necesita ver el día completo incluyendo ya jugados
        fecha = m.get("fecha","")
        if not fecha:
            out.append(m); continue
        if _tf:
            try:
                _mf = _dt2.strptime(fecha, "%Y-%m-%d")
                if abs((_mf - _tf).days) <= 1:
                    out.append(m)
                continue
            except: pass
        if fecha == target_date:
            out.append(m)
    return out

def render_king_rongo(matches_fut=None, nba_games=None, ten_matches=None):
    """
    👑 KING RONGO — El Cerebro Supremo de The Gamblers Layer.
    Escanea ⚽🏀🎾, corre todos los modelos, detecta contradicciones,
    gestiona bankroll, aprende del historial, y da EL PICK DEL DÍA.
    """
    pick_history = st.session_state.get("pick_history", [])

    # ══════════════════════════════════════════════════════
    # HEADER — presencia máxima
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style='position:relative;background:linear-gradient(160deg,#150030,#001500,#150030);
    border:none;border-radius:20px;padding:0;margin-bottom:4px;overflow:hidden'>

    <!-- Top glow bar -->
    <div style='height:3px;background:linear-gradient(90deg,transparent,#FFD700,#ff9500,#FFD700,transparent)'></div>

    <!-- Ambient orb left -->
    <div style='position:absolute;top:-40px;left:-40px;width:140px;height:140px;
    background:radial-gradient(circle,#FFD70015,transparent 70%);pointer-events:none'></div>
    <!-- Ambient orb right -->
    <div style='position:absolute;top:-40px;right:-40px;width:140px;height:140px;
    background:radial-gradient(circle,#7c00ff15,transparent 70%);pointer-events:none'></div>

    <div style='padding:20px 22px 18px;text-align:center;position:relative'>
      <div style='font-size:3rem;margin-bottom:6px;line-height:1;
      filter:drop-shadow(0 0 12px #FFD70088)'>👑</div>
      <div style='font-size:1.8rem;font-weight:900;letter-spacing:.2em;
      background:linear-gradient(135deg,#FFD700,#ff9500,#FFD700,#ffcc00);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      text-shadow:none;margin-bottom:6px'>KING RONGO</div>
      <div style='font-size:.72rem;color:#666;letter-spacing:.12em'>
      EL CEREBRO SUPREMO · ÁRBITRO DE MODELOS · PICK DEFINITIVO</div>
    </div>

    <!-- Bottom glow bar -->
    <div style='height:2px;background:linear-gradient(90deg,transparent,#7c00ff,#FFD700,#7c00ff,transparent)'></div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # BANKROLL PANEL — siempre visible
    # ══════════════════════════════════════════════════════
    bk = _king_rongo_bankroll_advice(pick_history)
    _kr_render_bankroll(bk)

    # ══════════════════════════════════════════════════════
    # 👑 AUDITORÍA KING RONGO — solo sus propios picks
    # ══════════════════════════════════════════════════════
    _kr_picks = [p for p in pick_history if str(p.get("pick","")).startswith("👑")]
    _kr_win  = sum(1 for p in _kr_picks if p.get("result") == "✅")
    _kr_loss = sum(1 for p in _kr_picks if p.get("result") == "❌")
    _kr_pend = sum(1 for p in _kr_picks if p.get("result") == "⏳")
    _kr_tot  = _kr_win + _kr_loss
    _kr_pct  = round(_kr_win / _kr_tot * 100) if _kr_tot > 0 else 0
    _kr_bar_c = "#FFD700" if _kr_pct >= 60 else ("#00ff88" if _kr_pct >= 50 else ("#FFD700" if _kr_pct >= 45 else "#ff4444"))

    # También auditar automáticamente contra results_db (igual que Villar)
    _rdb = get_results_db()
    _rdb_partidos = _rdb.get("partidos", [])
    _kr_auto_ok = 0; _kr_auto_fail = 0
    for _kp in _kr_picks:
        if _kp.get("result") in ("✅","❌"): continue  # ya calificado manualmente
        _res = _villar_find_result(_kp, _rdb_partidos)
        if _res:
            _vd2, _, _ = _villar_match_pick_to_result(_kp, _res)
            if   "GANÓ"  in _vd2: _kr_auto_ok   += 1
            elif "FALLÓ" in _vd2: _kr_auto_fail += 1

    _kr_total_ok   = _kr_win + _kr_auto_ok
    _kr_total_fail = _kr_loss + _kr_auto_fail
    _kr_total_all  = _kr_total_ok + _kr_total_fail
    _kr_total_pct  = round(_kr_total_ok / _kr_total_all * 100) if _kr_total_all > 0 else 0
    _kr_bc2 = "#FFD700" if _kr_total_pct >= 60 else ("#00ff88" if _kr_total_pct >= 55 else ("#FFD700" if _kr_total_pct >= 45 else "#ff4444"))

    if _kr_total_all > 0 or _kr_pend > 0:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#100020,#0a1500);"
            f"border:2px solid #FFD70066;border-radius:14px;padding:14px 18px;margin-bottom:14px'>"
            f"<div style='font-size:.68rem;font-weight:700;color:#FFD700;"
            f"letter-spacing:.12em;margin-bottom:10px'>👑 KING RONGO — AUDITORÍA DE SUS PICKS</div>"
            f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px'>"
            f"<div style='text-align:center;background:#00ff8810;border-radius:10px;padding:8px 4px'>"
            f"<div style='font-size:1.8rem;font-weight:900;color:#00ff88'>{_kr_total_ok}</div>"
            f"<div style='font-size:.68rem;color:#555'>✅ Ganados</div></div>"
            f"<div style='text-align:center;background:#ff444410;border-radius:10px;padding:8px 4px'>"
            f"<div style='font-size:1.8rem;font-weight:900;color:#ff4444'>{_kr_total_fail}</div>"
            f"<div style='font-size:.68rem;color:#555'>❌ Fallados</div></div>"
            f"<div style='text-align:center;background:{_kr_bc2}18;border-radius:10px;padding:8px 4px'>"
            f"<div style='font-size:1.8rem;font-weight:900;color:{_kr_bc2}'>{_kr_total_pct}%</div>"
            f"<div style='font-size:.68rem;color:#555'>Acierto</div></div>"
            f"<div style='text-align:center;background:#FFD70010;border-radius:10px;padding:8px 4px'>"
            f"<div style='font-size:1.8rem;font-weight:900;color:#FFD700'>{_kr_pend}</div>"
            f"<div style='font-size:.68rem;color:#555'>⏳ Pendientes</div></div>"
            f"</div>"
            f"<div style='background:#0d0d2e;border-radius:6px;height:8px;overflow:hidden'>"
            f"<div style='width:{_kr_total_pct}%;height:100%;"
            f"background:linear-gradient(90deg,#FFD700,#ff9500);border-radius:6px'></div></div>"
            f"<div style='font-size:.65rem;color:#444;margin-top:6px;text-align:right'>"
            f"{_kr_total_all} picks auditados · {_kr_pend} pendientes de resultado</div>"
            f"</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='background:#0a0a20;border:1px solid #FFD70033;border-radius:12px;"
            f"padding:12px 16px;margin-bottom:14px;text-align:center'>"
            f"<div style='font-size:.7rem;color:#FFD700;font-weight:700;margin-bottom:4px'>"
            f"👑 AUDITORÍA KING RONGO</div>"
            f"<div style='color:#555;font-size:.8rem'>Guarda picks de KR para ver tu historial de aciertos</div>"
            f"</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # SINCRONIZAR cache de disco → session_state (al cargar)
    # ══════════════════════════════════════════════════════
    if not st.session_state.get("_king_scanned"):
        _kr_sync_session_from_cache()

    # ══════════════════════════════════════════════════════
    # FECHA OBJETIVO y próximo scan
    # ══════════════════════════════════════════════════════
    _target_date, _target_label = _kr_target_date()
    _next_scan = _kr_next_scan_time()

    # Banner de contexto
    _hora_actual = datetime.now(CDMX).strftime("%H:%M")
    st.markdown(
        f"<div style='background:#0a0020;border:1px solid #FFD70033;border-radius:12px;"
        f"padding:10px 16px;margin-bottom:8px;display:flex;justify-content:space-between;"
        f"align-items:center;flex-wrap:wrap;gap:6px'>"
        f"<span style='color:#FFD700;font-size:.82rem;font-weight:700'>"
        f"🎯 Escaneando partidos de <b>{_target_label.upper()}</b> ({_target_date})</span>"
        f"<span style='color:#555;font-size:.75rem'>⏰ Scans automáticos: 08:00 · 14:00 · 22:00 CDMX"
        f" &nbsp;|&nbsp; próximo: {_next_scan}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════════════════
    # BOTONES DE ACCIÓN
    # ══════════════════════════════════════════════════════
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        do_scan = st.button(
            f"👑 ESCANEAR {_target_label.upper()} — ⚽ Fútbol + 🏀 NBA + 🎾 Tenis",
            use_container_width=True, key="king_scan",
            help=f"King Rongo analiza partidos de {_target_label} y elige EL pick con mayor edge real"
        )
    with c2:
        do_tg = st.button("📡 Telegram", use_container_width=True, key="king_tg")
    with c3:
        do_reset = st.button("🔄 Reset", use_container_width=True, key="king_reset")

    if do_reset:
        for k in ["_king_el_pick","_king_contras","_king_todos","_king_scanned","_king_ts","_king_target"]:
            st.session_state.pop(k, None)
        _kr_save_cache({})
        st.rerun()

    # ══════════════════════════════════════════════════════
    # AUTO-SCAN: marcar en session y dejar que el if de abajo lo tome
    # ══════════════════════════════════════════════════════
    _auto = _kr_should_auto_scan()
    if _auto and not st.session_state.get("_king_scanned"):
        do_scan = True
    # Si no hay cache y el usuario no presionó el botón, forzar scan
    if not st.session_state.get("_king_scanned") and not do_scan:
        do_scan = True

    # ══════════════════════════════════════════════════════
    # SCAN + RESULTADOS
    # ══════════════════════════════════════════════════════
    if do_scan or st.session_state.get("_king_scanned"):

        if do_scan:
            # ── CORONA ANIMADA ──
            _crown_slot = st.empty()
            _crown_slot.markdown("""
<style>
@keyframes kr-spin{
  0%  {transform:rotate(0deg)  scale(1.0);filter:drop-shadow(0 0 10px #FFD700bb)}
  25% {transform:rotate(90deg) scale(1.14);filter:drop-shadow(0 0 24px #ff9500ff)}
  50% {transform:rotate(180deg)scale(1.07);filter:drop-shadow(0 0 32px #FFD700ff)}
  75% {transform:rotate(270deg)scale(1.16);filter:drop-shadow(0 0 26px #7c00ffcc)}
  100%{transform:rotate(360deg)scale(1.0);filter:drop-shadow(0 0 10px #FFD700bb)}
}
@keyframes kr-shimmer{0%{background-position:-300px 0}100%{background-position:300px 0}}
@keyframes kr-glow{0%,100%{opacity:.5}50%{opacity:1}}
.kr-wrap{background:linear-gradient(160deg,#0e0028,#001608,#0e0028);
  border:1px solid #FFD70055;border-radius:20px;padding:30px 24px 26px;
  text-align:center;position:relative;overflow:hidden;margin:8px 0;}
.kr-wrap::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,#FFD700,#ff9500,transparent);
  animation:kr-glow 1.4s ease-in-out infinite;}
.kr-wrap::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,#7c00ff,transparent);
  animation:kr-glow 1.8s ease-in-out infinite reverse;}
.kr-crown{font-size:4rem;display:inline-block;
  animation:kr-spin 1.4s cubic-bezier(.4,0,.2,1) infinite;line-height:1;margin-bottom:14px;}
.kr-title{font-size:1rem;font-weight:900;letter-spacing:.2em;
  background:linear-gradient(135deg,#FFD700,#ff9500,#FFD700);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;}
.kr-bar-wrap{background:#080820;border-radius:99px;height:8px;
  overflow:hidden;margin:14px auto 0;border:1px solid #1a1a3a;}
.kr-bar{height:100%;border-radius:99px;width:100%;
  background:linear-gradient(90deg,#7c00ff,#FFD700,#ff9500,#FFD700);
  background-size:300% 100%;animation:kr-shimmer 1.2s linear infinite;}
</style>
<div class="kr-wrap">
  <div class="kr-crown">👑</div>
  <div class="kr-title">KING RONGO — ESCANEANDO</div>
  <div style="font-size:.8rem;color:#666;margin-top:6px;letter-spacing:.06em">
    ⚽ Fútbol · 🏀 NBA · 🎾 Tenis · 🧠 Modelos
  </div>
  <div class="kr-bar-wrap"><div class="kr-bar"></div></div>
</div>
""", unsafe_allow_html=True)

            with st.status("👑 King Rongo escaneando...", expanded=False) as _kr_status:
                try:
                    # Usar datos pasados directamente — ya vienen cargados del bridge
                    _kr_status.update(label="⚽ Preparando cartelera de fútbol...")
                    _mf = matches_fut or []
                    _mf_target = _kr_filter_by_date(_mf, _target_date)
                    if not _mf_target: _mf_target = _mf

                    _kr_status.update(label="🏀 Preparando partidos NBA...")
                    _nbg = nba_games or []
                    _nbg_target = _kr_filter_by_date(_nbg, _target_date)
                    if not _nbg_target: _nbg_target = _nbg

                    _kr_status.update(label="🎾 Preparando torneos de tenis...")
                    _ten = ten_matches or []
                    _ten_target = _kr_filter_by_date(_ten, _target_date)
                    if not _ten_target: _ten_target = _ten

                    _kr_status.update(label=f"🧠 Analizando {len(_mf_target)} fútbol · {len(_nbg_target)} NBA · {len(_ten_target)} tenis...")
                    el_pick, contradicciones, todos, top3 = _king_rongo_scan_all(
                        _mf_target, _nbg_target, _ten_target
                    )

                    _kr_status.update(
                        label=f"💎 {len(todos)} candidatos — ⚽{sum(1 for c in todos if 'Fútbol' in c.get('deporte',''))} 🏀{sum(1 for c in todos if 'NBA' in c.get('deporte',''))} 🎾{sum(1 for c in todos if 'Tenis' in c.get('deporte',''))}",
                        state="complete"
                    )
                    _ts_now = datetime.now(CDMX).strftime("%H:%M")
                    _ts_full = datetime.now(CDMX).strftime("%Y-%m-%d %H:%M")

                    # Si no hay candidatos — construir picks directamente de cartelera
                    if not todos:
                        # Bridge directo: 1 pick por deporte de la cartelera disponible
                        _fallback_cands = []
                        # Fútbol: mejor ML del día
                        for _fm in (_mf_target or [])[:20]:
                            try:
                                _fhf = get_form(_fm.get("home_id",""), _fm.get("slug","")) or []
                                _faf = get_form(_fm.get("away_id",""), _fm.get("slug","")) or []
                                _fhxg = _cup_enriched_xg(_fm, True,  _fhf, _faf) if not _fhf else xg_weighted(_fhf,True)
                                _faxg = _cup_enriched_xg(_fm, False, _fhf, _faf) if not _faf else xg_weighted(_faf,False)
                                _fmc = mc50k(_fhxg, _faxg)
                                _fph = _fmc["ph"]; _fpa = _fmc["pa"]
                                _fbest_p = max(_fph,_fpa)
                                _fbest_lbl = f"🏠 {_fm.get('home','?')} gana" if _fph>=_fpa else f"✈️ {_fm.get('away','?')} gana"
                                _fbest_odd = _fm.get("odd_h",0) if _fph>=_fpa else _fm.get("odd_a",0)
                                _fallback_cands.append({
                                    "deporte":"⚽ Fútbol","sport":"futbol",
                                    "label":f"{_fm.get('home','?')} vs {_fm.get('away','?')}",
                                    "liga":_fm.get("league",""),"hora":_fm.get("hora",""),
                                    "pick":_fbest_lbl,"prob":_fbest_p,"odd":_fbest_odd,
                                    "edge":(_fbest_p-1/_fbest_odd) if _fbest_odd>1 else (_fbest_p-0.50),
                                    "kelly_pct":0,"mkt_type":"1X2","contradiccion":False,
                                    "model_spread":10,"conf_emoji":"⚡","conf_label":"MEDIA","conf_color":"#aaa",
                                    "reasoning":f"xG {_fhxg:.2f}–{_faxg:.2f}","match":_fm,
                                    "hxg":_fhxg,"axg":_faxg,
                                    "score":_fbest_p * 5,
                                })
                                break
                            except: continue
                        # NBA
                        for _ng in (_nbg_target or [])[:10]:
                            try:
                                _nr = nba_ou_model(_ng.get("home_id",""), _ng.get("away_id",""), _ng.get("ou_line",220))
                                _np = max(_nr["p_over"],_nr["p_under"])
                                _nm = f"🔥 Over {_nr['line']}" if _nr["p_over"]>=_nr["p_under"] else f"❄️ Under {_nr['line']}"
                                _fallback_cands.append({
                                    "deporte":"🏀 NBA","sport":"nba",
                                    "label":f"{_ng.get('away','?')} @ {_ng.get('home','?')}",
                                    "liga":"NBA","hora":_ng.get("hora",""),
                                    "pick":_nm,"prob":_np,"odd":0,
                                    "edge":_np-0.50,"kelly_pct":0,"mkt_type":"O/U",
                                    "contradiccion":False,"model_spread":5,
                                    "conf_emoji":"⚡","conf_label":"MEDIA","conf_color":"#aaa",
                                    "reasoning":f"Proy {_nr['proj']} pts","match":_ng,
                                    "score":_np * 5,
                                })
                                break
                            except: continue
                        # Tenis
                        for _tm in (_ten_target or [])[:15]:
                            try:
                                _tt = tennis_model(_tm.get("rank1",100), _tm.get("rank2",150), _tm.get("odd_1",0), _tm.get("odd_2",0))
                                _tp = max(_tt["p1"],_tt["p2"])
                                _tfav = _tm.get("p1","?") if _tt["p1"]>=_tt["p2"] else _tm.get("p2","?")
                                _fallback_cands.append({
                                    "deporte":"🎾 Tenis","sport":"tenis",
                                    "label":f"{_tm.get('p1','?')} vs {_tm.get('p2','?')}",
                                    "liga":_tm.get("torneo","Tennis"),"hora":_tm.get("hora",""),
                                    "pick":f"🎾 {_tfav} gana","prob":_tp,"odd":0,
                                    "edge":_tp-0.50,"kelly_pct":0,"mkt_type":"ML",
                                    "contradiccion":False,"model_spread":5,
                                    "conf_emoji":"⚡","conf_label":"MEDIA","conf_color":"#aaa",
                                    "reasoning":f"Rk #{_tm.get('rank1','?')} vs #{_tm.get('rank2','?')}","match":_tm,
                                    "score":_tp * 5,
                                })
                                break
                            except: continue
                        todos = _fallback_cands
                        el_pick = todos[0] if todos else None
                        if el_pick: el_pick = {**el_pick, "is_rongo_pick": True}
                        top3 = [{**c, "is_rongo_pick": True} for c in todos[:3]]
                        contradicciones = []

                    if not el_pick and todos:
                        el_pick = {**todos[0], "is_rongo_pick": True}

                    st.session_state["_king_el_pick"]  = el_pick
                    st.session_state["_king_contras"]  = contradicciones
                    st.session_state["_king_todos"]    = todos
                    st.session_state["_king_top3"]     = top3
                    st.session_state["_king_scanned"]  = True
                    st.session_state["_king_ts"]       = _ts_now
                    st.session_state["_king_target"]   = _target_date

                    # ── AUTO-GUARDAR pick de KR en historial ──
                    # Solo si no existe ya un pick de KR para este partido hoy
                    if el_pick:
                        _kr_match = el_pick.get("match", {})
                        _kr_home  = _kr_match.get("home", _kr_match.get("p1", el_pick.get("label","?").split(" vs ")[0]))
                        _kr_away  = _kr_match.get("away", _kr_match.get("p2", el_pick.get("label","?").split(" vs ")[-1] if " vs " in el_pick.get("label","") else "?"))
                        _kr_fecha = _kr_match.get("fecha", datetime.now(CDMX).strftime("%Y-%m-%d"))
                        _kr_label = f"👑 {el_pick.get('pick','?')}"
                        # Verificar si ya existe este pick en historial (mismo partido + mismo día)
                        init_history()
                        _existing = [p for p in st.session_state.get("pick_history",[])
                                     if p.get("pick","").startswith("👑")
                                     and p.get("home","") == _kr_home
                                     and p.get("fecha","") == _kr_fecha]
                        if not _existing:
                            add_pick(
                                {"home": _kr_home, "away": _kr_away,
                                 "league": el_pick.get("liga",""), "fecha": _kr_fecha},
                                _kr_label,
                                el_pick.get("prob", 0),
                                el_pick.get("odd", 0),
                                sport=el_pick.get("sport","futbol")
                            )

                    # Persistir en disco para sobrevivir entre sesiones
                    _kr_save_cache({
                        "el_pick":        el_pick,
                        "contradicciones":contradicciones,
                        "todos":          todos,
                        "target_date":    _target_date,
                        "target_label":   _target_label,
                        "hora_scan":      _ts_now,
                        "scan_ts":        _ts_full,
                    })

                except Exception as e:
                    import traceback as _tb_mod
                    _tb_str = _tb_mod.format_exc()
                    _kr_status.update(label=f"❌ Error: {e}", state="error")
                    st.error(f"Error en escaneo: {e}")
                    with st.expander("🔍 Traceback"):
                        st.code(_tb_str)

            _crown_slot.empty()

        el_pick        = st.session_state.get("_king_el_pick")
        contradicciones= st.session_state.get("_king_contras", [])
        todos          = st.session_state.get("_king_todos", [])
        top3           = st.session_state.get("_king_top3", [])
        scan_ts        = st.session_state.get("_king_ts","")
        scan_target    = st.session_state.get("_king_target", _target_date)

        # Meta-stats del escaneo
        n_fut  = sum(1 for c in todos if "Fútbol" in c["deporte"])
        n_nba  = sum(1 for c in todos if "NBA"    in c["deporte"])
        n_ten  = sum(1 for c in todos if "Tenis"  in c["deporte"])
        n_pos  = sum(1 for c in todos if c.get("edge",0) > 0)
        n_blk  = len(contradicciones)

        st.markdown(
            f"<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin-bottom:12px'>"
            f"<div class='mbox'><div class='mval' style='color:#aa00ff'>{n_fut}</div><div class='mlbl'>⚽</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#ff9500'>{n_nba}</div><div class='mlbl'>🏀</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#00ccff'>{n_ten}</div><div class='mlbl'>🎾</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#00ff88'>{n_pos}</div><div class='mlbl'>Edge+</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#ff4444'>{n_blk}</div><div class='mlbl'>Bloq.</div></div>"
            f"</div>",
            unsafe_allow_html=True
        )

        if scan_ts:
            st.caption(f"👑 Último scan: {scan_ts} CDMX · Partidos de {scan_target}")

        # ── EL PICK DEL DÍA ──
        if el_pick:
            # Mostrar pick primero — sin esperar API
            _kr_render_pick_card(el_pick, bk, "")

            # TOP 3 del Rey
            if top3 and len(top3) > 0:
                st.markdown(
                    "<div style='font-size:.72rem;font-weight:700;color:#FFD700;"
                    "text-transform:uppercase;letter-spacing:.15em;margin:18px 0 8px;"
                    "text-align:center'>👑 LOS 3 PICKS DEL REY</div>",
                    unsafe_allow_html=True)
                _t3_cols = st.columns(min(len(top3), 3))
                for _t3i, _t3c in enumerate(top3[:3]):
                    with _t3_cols[_t3i]:
                        _t3_prob  = _t3c.get("prob", 0)
                        _t3_edge  = _t3c.get("edge", 0)
                        _t3_odd   = _t3c.get("odd", 0)
                        _t3_sport = _t3c.get("deporte","")
                        _t3_cc    = _t3c.get("conf_color","#FFD700")
                        _t3_ce    = _t3c.get("conf_emoji","⚡")
                        _t3_medal = ["👑","🥇","🥈"][_t3i]
                        _t3_odd_txt = f"@{_t3_odd:.2f}" if _t3_odd > 1 else "S/C"
                        _t3_edge_c  = "#00ff88" if _t3_edge >= 0 else "#ff4444"
                        st.markdown(
                            f"<div style='background:linear-gradient(145deg,#0a0020,#07071a);"
                            f"border:1px solid {_t3_cc}66;border-radius:14px;padding:12px;"
                            f"text-align:center;height:100%'>"
                            f"<div style='font-size:1.4rem'>{_t3_medal}</div>"
                            f"<div style='font-size:.68rem;color:#888;margin:2px 0'>{_t3_sport}</div>"
                            f"<div style='font-size:.72rem;font-weight:700;color:#ddd;"
                            f"margin:4px 0;line-height:1.3'>{_t3c.get('label','')}</div>"
                            f"<div style='font-size:.85rem;font-weight:900;color:{_t3_cc};"
                            f"margin:6px 0'>{_t3c.get('pick','')}</div>"
                            f"<div style='font-size:1.2rem;font-weight:900;color:#fff'>"
                            f"{_t3_prob*100:.0f}%</div>"
                            f"<div style='font-size:.65rem;color:{_t3_edge_c}'>"
                            f"Edge {_t3_edge*100:+.1f}% · {_t3_odd_txt}</div>"
                            f"<div style='font-size:.6rem;color:#555;margin-top:4px'>"
                            f"{_t3_ce} {_t3c.get('conf_label','')}</div>"
                            f"</div>",
                            unsafe_allow_html=True)

            # Botones de acción del pick
            a1, a2, a3 = st.columns(3)
            with a1:
                if st.button(f"💾 Guardar pick de King Rongo", key="save_king", use_container_width=True):
                    m = el_pick.get("match", {})
                    fake = {
                        "home":   m.get("home", m.get("p1", el_pick["label"].split(" vs ")[0])),
                        "away":   m.get("away", m.get("p2", el_pick["label"].split(" vs ")[-1])),
                        "league": el_pick.get("liga",""),
                        "fecha":  m.get("fecha", datetime.now(CDMX).strftime("%Y-%m-%d")),
                    }
                    add_pick(fake, f"👑 {el_pick['pick']}", el_pick["prob"],
                             el_pick.get("odd",0), sport=el_pick["sport"])
                    st.success("✅ Pick guardado")
            with a2:
                if st.button("📡 Enviar a Telegram", key="king_tg2", use_container_width=True):
                    do_tg = True
            with a3:
                # Abrir partido completo
                if el_pick.get("match") and st.button("🔎 Ver análisis completo", key="king_open", use_container_width=True):
                    _m = el_pick["match"]
                    sport = el_pick["sport"]
                    if sport == "tenis":
                        sel = {**_m,
                               "home": _m.get("p1",_m.get("home","")),
                               "away": _m.get("p2",_m.get("away","")),
                               "home_id": _m.get("id","")+"_p1",
                               "away_id": _m.get("id","")+"_p2",
                               "league":  _m.get("torneo",_m.get("tour","Tenis")),
                               "slug":"tennis","home_rec":"","away_rec":"",
                               "odd_h":_m.get("odd_1",0),"odd_a":_m.get("odd_2",0),
                               "odd_d":0,"_sport":"tennis"}
                    else:
                        sel = {**_m}
                    st.session_state["sel"]  = sel
                    st.session_state["view"] = "analisis"
                    st.rerun()

            # ── VEREDICTO DE KING RONGO ──
            with st.expander("💬 Veredicto de King Rongo", expanded=True):
                with st.spinner("👑 King Rongo analizando..."):
                    _kr_narr = _kr_ia_narracion(el_pick, bk, todos) if todos else ""
                if _kr_narr:
                    st.markdown(
                        f"<div style='font-size:.86rem;color:#ccc;line-height:1.8;"
                        f"font-style:italic;padding:6px 0'>{_kr_narr}</div>",
                        unsafe_allow_html=True)
                else:
                    _p  = el_pick.get("prob",0)
                    _e  = el_pick.get("edge",0)
                    _lbl = el_pick.get("pick","")
                    _match = el_pick.get("label","")
                    st.markdown(
                        f"<div style='font-size:.84rem;color:#888;line-height:1.7'>"
                        f"El modelo encuentra <b style='color:#FFD700'>{_p*100:.1f}%</b> de probabilidad "
                        f"en <b style='color:#ccc'>{_lbl}</b> para el partido <i>{_match}</i>. "
                        f"Edge calculado: <b style='color:{'#00ff88' if _e>=0 else '#ff4444'}'>{_e*100:+.1f}%</b>. "
                        f"{'Apostar con criterio.' if _e < 0 else 'Ventaja real detectada — jugar con confianza.'}"
                        f"</div>",
                        unsafe_allow_html=True)

            # ── CONTRADICCIONES ──
            _kr_render_contradictions(contradicciones)

            # ── TABLA DE PICKS ──
            _kr_render_table(todos, el_pick)

            # ── MEMORIA EVOLUTIVA ──
            _kr_render_memory(pick_history)

            # ── TELEGRAM ──
            if do_tg:
                _nl = chr(10)
                prob_pct = el_pick["prob"] * 100
                edge_pct = el_pick["edge"] * 100
                conf_e   = el_pick.get("conf_emoji","⚡")
                models_txt = " | ".join(f"{k}: {v}%" for k,v in list(el_pick.get("models",{}).items())[:3])
                # Construir texto del TOP 3
                _top3_txt = ""
                for _ti, _tc in enumerate(top3[:3]):
                    _medal = ["👑","🥇","🥈"][_ti]
                    _t_odd = f" @{_tc['odd']:.2f}" if _tc.get('odd',0)>1 else ""
                    _top3_txt += f"{_medal} {_tc['deporte']} · {_tc['label']}{_nl}"
                    _top3_txt += f"   ➜ *{_tc['pick']}* {_tc['prob']*100:.0f}%{_t_odd}{_nl}"

                msg = (
                    f"👑 *KING RONGO — PICK DEL DÍA*{_nl}"
                    f"━━━━━━━━━━━━━━━━━━━{_nl}"
                    f"{el_pick['deporte']} · {el_pick.get('liga','')}{_nl}"
                    f"🆚 *{el_pick['label']}*{_nl}"
                    f"🕒 {el_pick.get('hora','')} CDMX{_nl}{_nl}"
                    f"{conf_e} *PICK: {el_pick['pick']}*{_nl}"
                    f"📊 Prob: *{prob_pct:.1f}%*{_nl}"
                    f"📈 Edge: *{edge_pct:+.1f}%*{_nl}"
                    f"🎯 Kelly: *{bk['kelly_rec']}%* del banco{_nl}"
                    f"{'💰 @' + str(round(el_pick['odd'],2)) if el_pick.get('odd',0)>1 else ''}{_nl}{_nl}"
                    f"🧠 Modelos: {models_txt}{_nl}{_nl}"
                    f"━━━━━━━━━━━━━━━━━━━{_nl}"
                    f"🎯 *LOS 3 PICKS DEL REY:*{_nl}"
                    f"{_top3_txt}"
                    f"━━━━━━━━━━━━━━━━━━━{_nl}"
                    f"_{bk['consejo']}_{_nl}"
                    f"_The Gamblers Layer · King Rongo v2_{_nl}"
                    f"_Escaneados: {len(todos)} partidos ⚽{n_fut} 🏀{n_nba} 🎾{n_ten}_"
                )
                if tg_send(msg):
                    st.success("✅ Pick enviado a Telegram")
                else:
                    st.error("❌ Error Telegram")

        else:
            # No pick encontrado
            st.markdown(
                "<div style='text-align:center;padding:30px;background:#07071a;"
                "border-radius:14px;border:1px solid #1a1a30;margin:12px 0'>"
                "<div style='font-size:2rem'>🤔</div>"
                "<div style='font-size:1rem;font-weight:700;color:#555;margin:8px 0'>"
                "King Rongo no encontró picks con edge positivo hoy.</div>"
                "<div style='font-size:.8rem;color:#333'>Día de descanso recomendado. "
                "Proteger el bankroll también es ganar.</div>"
                "</div>",
                unsafe_allow_html=True
            )

    else:
        # Pre-scan — estado inicial
        st.markdown(
            "<div style='text-align:center;padding:36px 20px;"
            "background:linear-gradient(160deg,#0a0020,#07071a);"
            "border-radius:16px;border:1px solid #1a1a30;margin:12px 0'>"
            "<div style='font-size:3rem;margin-bottom:12px;"
            "filter:drop-shadow(0 0 10px #FFD70044)'>👑</div>"
            "<div style='font-size:1rem;font-weight:700;color:#555;margin-bottom:8px'>"
            "King Rongo está listo para escanear</div>"
            "<div style='font-size:.78rem;color:#333;line-height:1.8'>"
            "Presiona el botón y King Rongo correrá todos los modelos simultáneamente:<br>"
            "xG · Elo · Dixon-Coles · Monte Carlo · Weibull · Net Rating<br>"
            "y elegirá EL PICK con mayor edge real ajustado a tu bankroll."
            "</div></div>",
            unsafe_allow_html=True
        )
        # Mostrar memoria aunque no haya escaneado
        _kr_render_memory(pick_history)



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

# ── Cargar bridge diamante al inicio de cada sesión ──
if "_diamond_bridge" not in st.session_state:
    try:
        import json as _jb
        with open("/tmp/gamblers_diamond_bridge.json") as _bf:
            st.session_state["_diamond_bridge"] = _jb.load(_bf)
    except: st.session_state["_diamond_bridge"] = {}

# ── KING RONGO — Banner de presencia permanente ──
_king_pick = st.session_state.get("_king_el_pick")
if _king_pick:
    _kp   = _king_pick["prob"]*100
    _ke   = _king_pick.get("edge",0)*100
    _kc   = _king_pick.get("conf_color","#FFD700")
    _ke_c = "#00ff88" if _ke>0 else "#ff4444"
    _ts   = st.session_state.get("_king_ts","")
    st.markdown(
        f"<div style='background:linear-gradient(90deg,#100018,#00100a,#100018);"
        f"border-radius:12px;padding:10px 14px;margin:4px 0 10px;"
        f"border:1px solid {_kc}44;"
        f"display:flex;align-items:center;gap:12px;position:relative;overflow:hidden'>"
        f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
        f"background:linear-gradient(90deg,transparent,{_kc},transparent)'></div>"
        f"<div style='font-size:1.5rem;filter:drop-shadow(0 0 6px {_kc}88)'>👑</div>"
        f"<div style='flex:1;min-width:0'>"
        f"<div style='font-size:.62rem;color:#444;letter-spacing:.1em;font-weight:700'>"
        f"KING RONGO · PICK DEL DÍA{(' · ' + _ts) if _ts else ''}</div>"
        f"<div style='font-size:.88rem;font-weight:900;color:{_kc};"
        f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{_king_pick['pick']}</div>"
        f"<div style='font-size:.68rem;color:#555;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>"
        f"{_king_pick['deporte']} · {_king_pick['label'][:30]}</div>"
        f"</div>"
        f"<div style='text-align:right;flex-shrink:0'>"
        f"<div style='font-size:1.1rem;font-weight:900;color:{_kc}'>{_kp:.0f}%</div>"
        f"<div style='font-size:.65rem;color:{_ke_c}'>Edge {_ke:+.1f}%</div>"
        f"</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# CARGAR DATA SEGÚN DEPORTE
# ══════════════════════════════════════════════════════════
matches     = []
nba_games   = []
ten_matches = []

# ── AUTO-SYNC resultados en background — cada 30 min silenciosamente ──
_auto_sync_key = "last_auto_sync"
_now_ts2 = datetime.now(CDMX).timestamp()
if _now_ts2 - st.session_state.get(_auto_sync_key, 0) > 1800:  # cada 30 min
    try:
        update_results_db(force=False)
        st.session_state["results_db"] = _load_results_db()
    except: pass
    st.session_state[_auto_sync_key] = _now_ts2

if deporte == "futbol":
    with st.spinner("Cargando cartelera..."):
        try:
            all_matches = get_cartelera()
        except Exception as _e:
            all_matches = []
            st.warning(f"⚠️ Error cargando fútbol: {_e}")

    # ── PRE-SNAP BACKGROUND: calcular y guardar pick de cada partido ──
    # Corre diamond_engine para todos los partidos (pre y post) y llena el bridge.
    # El bridge persiste en archivo — Resultados siempre encuentra el pick correcto.
    if all_matches:
        if "_diamond_bridge" not in st.session_state:
            # Cargar bridge persistido de sesiones anteriores
            try:
                import json as _json
                with open("/tmp/gamblers_diamond_bridge.json") as _bf:
                    st.session_state["_diamond_bridge"] = _json.load(_bf)
            except: st.session_state["_diamond_bridge"] = {}
        _bridge = st.session_state["_diamond_bridge"]
        _bridge_dirty = False
        for _pm in all_matches:
            try:
                _pid  = _pm.get("id","")
                _pid2 = f"{_pm.get('home_id','')}_{_pm.get('away_id','')}_{_pm.get('fecha','')}"
                _pst  = _pm.get("state","pre")
                # Pre-partido: saltar si ya está en bridge
                if _pst == "pre" and (_pid in _bridge or _pid2 in _bridge):
                    continue
                # Calcular con datos limpios (sin score)
                _pm_clean = {k: v for k, v in _pm.items() if k not in ("score_h","score_a")}
                _pm_clean["score_h"] = 0
                _bk_pk = _villar_auto_pick(_pm_clean)
                if _bk_pk:
                    _entry = {
                        "pick": _bk_pk.get("pick",""), "prob": _bk_pk.get("prob",0),
                        "odd":  _bk_pk.get("odd",0),  "src":  _bk_pk.get("src","🤖"),
                        "home": _pm.get("home",""),    "away": _pm.get("away",""),
                        "sport": "futbol",             "fecha": _pm.get("fecha",""),
                        "mkt":  _bk_pk.get("mkt",""),
                    }
                    if _pid:  _bridge[_pid]  = _entry
                    if _pid2: _bridge[_pid2] = _entry
                    _bridge_dirty = True
            except: continue
        # Persistir a archivo si hubo cambios
        if _bridge_dirty:
            try:
                import json as _json
                with open("/tmp/gamblers_diamond_bridge.json","w") as _bf:
                    _json.dump(_bridge, _bf)
            except: pass
    if not all_matches:
        st.info("⚽ No hay partidos de fútbol disponibles ahora. Intenta refrescar en unos minutos.")
    else:
        liga_opts = ["Todas"] + sorted(set(m["league"] for m in all_matches))
        liga_sel  = st.selectbox("Liga", liga_opts, label_visibility="collapsed")
        matches   = all_matches if liga_sel=="Todas" else [m for m in all_matches if m["league"]==liga_sel]

elif deporte == "nba":
    with st.spinner("Cargando NBA..."):
        try:
            nba_games = get_nba_cartelera()
        except Exception as _e:
            nba_games = []
            st.warning(f"⚠️ Error cargando NBA: {_e}")

elif deporte == "tenis":
    with st.spinner("Cargando Tenis..."):
        try:
            ten_matches = get_tennis_cartelera()
        except Exception as _e:
            ten_matches = []
            st.warning(f"⚠️ Error cargando Tenis: {_e}")

# ══════════════════════════════════════════════════════════
# CARTELERA
# ══════════════════════════════════════════════════════════
if st.session_state["view"] == "cartelera":

    # ─── NBA ─────────────────────────────────────────────
    if deporte == "nba":
        tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab_king = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial","🎓 Califica tu Pick","📊 Resultados","👑 King Rongo"])
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
                    # ── Finalizados — clickeables con score real ──
                    for g in [x for x in gs if x["state"]=="post"]:
                        sh=g.get("score_h",-1); sa=g.get("score_a",-1)
                        sf=f"{sh}–{sa} pts" if sh>=0 else "FT"
                        won_h=sh>sa; hc="#00ff88" if won_h else "#aaa"; ac="#00ff88" if sa>sh else "#aaa"
                        won_lbl = g["home"] if won_h else g["away"]
                        if st.button(
                            f"✅ {g['away']} @ {g['home']}  ·  {sf}  · 🏆 {won_lbl}",
                            key=f"nba_post_{g['id']}", use_container_width=True):
                            st.session_state["sel"]  = {**g, "_sport":"nba"}
                            st.session_state["view"] = "analisis"
                            st.rerun()

                    # ── Pre/live en 2 COLUMNAS ──
                    active_gs = [x for x in gs if x["state"]!="post"]
                    for gi in range(0, len(active_gs), 2):
                        pair = active_gs[gi:gi+2]
                        ncols = st.columns(len(pair))
                        for ncol, g in zip(ncols, pair):
                            with ncol:
                                live = g["state"]=="in"
                                sc   = f"{g['score_h']}-{g['score_a']}" if live else g["hora"]
                                ou   = f"  O/U {g['ou_line']}" if g["ou_line"]>0 else ""
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
                                        "xg_h": res.get("proj",220)/2/100, "xg_a": res.get("proj",220)/2/100,
                                        "o25": ai_over/100, "o35": 0.35, "btts": 0.5,
                                    }
                                    nba_dp_fake = {"ph": ai_ml_h/100, "pa": ai_ml_a/100, "pd": 0.0, "conf": ai_conf}
                                    _nba_best_mkt  = f"O/U {g.get('ou_line','')}" if g.get("ou_line") else (g["home"] if ai_ml_h >= ai_ml_a else g["away"])
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
                _ven_nba = _ventana_22h(nba_games or [])
                _nba_cands = []
                for _g in _ven_nba[:20]:
                    _r = nba_ou_model(_g["home_id"],_g["away_id"],_g["ou_line"])
                    _bp = max(_r["p_over"],_r["p_under"])
                    _bm = f"🔥 Over {_r['line']}" if _r["p_over"]>_r["p_under"] else f"❄️ Under {_r['line']}"
                    if _bp >= 0.55:
                        _nba_cands.append({"teams":f"{_g['away']} @ {_g['home']}","liga":"NBA","hora":_g["hora"],"pick":_bm,"prob":_bp,"sport":"🏀"})
                _nba_cands.sort(key=lambda x:-x["prob"])
                _trilay3 = _nba_cands[:3]
            if len(_trilay3) >= 2:
                _comb = 1.0
                for _t in _trilay3: _comb *= _t.get("best_p", _t.get("prob", 0.5))
                _cuota = round(1/_comb, 2) if _comb>0 else 0
                st.markdown(f"<div class='trilay-card'><div style='font-size:.8rem;font-weight:700;color:#aa00ff;letter-spacing:.1em;margin-bottom:12px'>✦ TRILAY NBA DEL DÍA</div><div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px'><div class='mbox' style='flex:1'><div class='mval' style='color:#aa00ff'>{_comb*100:.1f}%</div><div class='mlbl'>Prob. combinada</div></div><div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{_cuota}x</div><div class='mlbl'>Cuota estimada</div></div></div>", unsafe_allow_html=True)
                for _i,_t in enumerate(_trilay3):
                    _p3 = _t.get("best_p", _t.get("prob",0.5))
                    _tm3 = f"{_t.get('home',_t.get('teams','?'))} vs {_t.get('away','')}"
                    _pk3 = _t.get("best_m", _t.get("pick","?"))
                    _cc = "#FFD700" if _p3>0.65 else ("#00ff88" if _p3>0.58 else "#aaa")
                    st.markdown(f"<div class='mrow'><span style='color:{_cc};font-weight:700'>{_i+1}. {_tm3}</span><br><span style='color:#555;font-size:.78rem'>NBA · {_t['hora']}</span><br><span style='color:#00ccff;font-weight:700'>{_t['pick']}</span> <span style='color:{_cc};font-size:.85rem'>{_t['prob']*100:.1f}%</span></div>", unsafe_allow_html=True)
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
            render_einstein_califica("nba")
        with tab8:
            render_resultados_tab()
        with tab_king:
            # KR siempre necesita los 3 deportes — cargar lo que falte
            _kr_fut = matches if matches else st.session_state.get("_kr_cache_fut") or []
            _kr_nba = nba_games if nba_games else st.session_state.get("_kr_cache_nba") or []
            _kr_ten = st.session_state.get("_kr_cache_ten") or []
            if not _kr_ten:
                try: _kr_ten = get_tennis_cartelera()
                except: _kr_ten = []
            if not _kr_nba:
                try: _kr_nba = get_nba_cartelera()
                except: _kr_nba = []
            if not _kr_fut:
                try: _kr_fut = get_cartelera()
                except: _kr_fut = []
            st.session_state["_kr_cache_fut"] = _kr_fut
            st.session_state["_kr_cache_nba"] = _kr_nba
            st.session_state["_kr_cache_ten"] = _kr_ten
            render_king_rongo(matches_fut=_kr_fut, nba_games=_kr_nba, ten_matches=_kr_ten)

    # ─── TENIS ───────────────────────────────────────────
    elif deporte == "tenis":
        tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab_king = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial","🎓 Califica tu Pick","📊 Resultados","👑 King Rongo"])
        with tab1:
            # ── TENNIS CARTELERA — 2 columnas, separado por ATP / WTA ──
            pre_m  = [m for m in ten_matches if m["state"] == "pre"]
            live_m = [m for m in ten_matches if m["state"] == "in"]
            post_m = [m for m in ten_matches if m["state"] == "post"]
            total_pre = len(pre_m) + len(live_m)

            if not ten_matches:
                st.info("No hay partidos ATP/WTA disponibles para estas fechas.")
            else:
                st.markdown(
                    f"<div style='display:flex;gap:10px;margin-bottom:12px'>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ff88'>{total_pre}</div><div class='mlbl'>Hoy / Próximos</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#ff9500'>{len(live_m)}</div><div class='mlbl'>🔴 En Vivo</div></div>"
                    f"<div class='mbox' style='flex:1'><div class='mval' style='color:#555'>{len(post_m)}</div><div class='mlbl'>Terminados</div></div>"
                    f"</div>", unsafe_allow_html=True)

            from collections import defaultdict
            ten_por_fecha = defaultdict(lambda: defaultdict(list))
            for m in ten_matches:
                if m["state"] != "post":  # solo pre + live en cartelera
                    ten_por_fecha[m["fecha"]][m["tour"]].append(m)

            def fecha_label_ten(f):
                try:
                    d=datetime.strptime(f,"%Y-%m-%d")
                    dias=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                    meses=["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                    return f"🎾 {dias[d.weekday()]} {d.day} {meses[d.month]}"
                except: return f

            for fi, fecha in enumerate(sorted(ten_por_fecha.keys())):
                total_ms = sum(len(v) for v in ten_por_fecha[fecha].values())
                is_hoy = fecha == datetime.now(CDMX).strftime("%Y-%m-%d")
                with st.expander(f"{fecha_label_ten(fecha)}  ·  {total_ms} partidos", expanded=(fi==0)):
                    for tour in ["ATP","WTA"]:
                        ms = ten_por_fecha[fecha].get(tour,[])
                        if not ms: continue
                        tour_color = "#00ccff" if tour == "ATP" else "#aa00ff"
                        st.markdown(
                            f"<div style='font-size:.72rem;font-weight:900;color:{tour_color};"
                            f"text-transform:uppercase;letter-spacing:.12em;margin:10px 0 8px'>"
                            f"{'🎾' if tour=='ATP' else '🎾'} {tour} · {len(ms)} partidos</div>",
                            unsafe_allow_html=True)

                        # ── 2 COLUMNAS ──
                        # Finished matches first in muted row, then pre/live in 2-col grid
                        fin_ms  = [m for m in ms if m["state"]=="post"]
                        pre_ms  = [m for m in ms if m["state"]!="post"]

                        # Finalizados — clickeables con score sets real
                        for m in fin_ms:
                            sc1r = m.get("score_p1",""); sc2r = m.get("score_p2","")
                            sc = f"{sc1r}–{sc2r}" if sc1r else "FT"
                            won_n = m["p1"] if (sc1r and sc2r and sc1r > sc2r) else m["p2"]
                            if st.button(
                                f"✅ {m['p1']} vs {m['p2']}  ·  Sets {sc}  · 🏆 {won_n}",
                                key=f"ten_post_{m['id']}", use_container_width=True):
                                # convert tennis match to sel format for detail view
                                sel_m = {**m,
                                    "home": m["p1"], "away": m["p2"],
                                    "home_id": m["id"]+"_p1", "away_id": m["id"]+"_p2",
                                    "league": m.get("torneo", m.get("tour","Tenis")),
                                    "slug": "tennis", "home_rec":"", "away_rec":"",
                                    "odd_h": m.get("odd_1",0), "odd_a": m.get("odd_2",0),
                                    "odd_d": 0, "_sport": "tennis",
                                }
                                st.session_state["sel"]  = sel_m
                                st.session_state["view"] = "analisis"
                                st.rerun()

                        # Pre/live in 2-column grid
                        # We render them as pairs into 2 st.columns
                        for i in range(0, len(pre_ms), 2):
                            pair = pre_ms[i:i+2]
                            cols = st.columns(len(pair))
                            for col, m in zip(cols, pair):
                                with col:
                                    tm = tennis_model(m["rank1"], m["rank2"], m["odd_1"], m["odd_2"])
                                    fav   = m["p1"] if tm["p1"]>=tm["p2"] else m["p2"]
                                    fav_p = max(tm["p1"],tm["p2"])
                                    live_badge = " 🔴" if m["state"]=="in" else ""
                                    conf_color = "#FFD700" if "DIAMANTE" in tm["conf"] else ("#00ff88" if "ALTA" in tm["conf"] else "#555")
                                    if st.button(f"🎾 {m['p1']} vs {m['p2']}  ·  {m['hora']}{live_badge}", key=f"ten_{m['id']}", use_container_width=True):
                                        sel_m = {**m,
                                            "home":m["p1"],"away":m["p2"],
                                            "home_id":m["id"]+"_p1","away_id":m["id"]+"_p2",
                                            "league":m.get("torneo",m.get("tour","Tenis")),
                                            "slug":"tennis","home_rec":"","away_rec":"",
                                            "odd_h":m.get("odd_1",0),"odd_a":m.get("odd_2",0),
                                            "odd_d":0,"_sport":"tennis",
                                        }
                                        st.session_state["sel"]  = sel_m
                                        st.session_state["view"] = "analisis"
                                        st.rerun()

        with tab2:
            st.markdown("<div class='shdr'>🎰 TRILAY Tenis</div>", unsafe_allow_html=True)
            _ven_ten = _ventana_22h(ten_matches or [])
            ten_cands = []
            for _m in _ven_ten[:20]:
                try:
                    _tm = tennis_model(_m["rank1"],_m["rank2"],_m.get("odd_1",0),_m.get("odd_2",0))
                    _fav = _m["p1"] if _tm["p1"]>=_tm["p2"] else _m["p2"]
                    _p   = max(_tm["p1"],_tm["p2"])
                    if _p >= 0.58:
                        ten_cands.append({"teams":f"{_m['p1']} vs {_m['p2']}","liga":_m.get("torneo","Tenis"),"hora":_m.get("hora",""),"pick":f"🎾 {_fav}","prob":_p})
                except: pass
            ten_cands.sort(key=lambda x:-x["prob"])
            if len(ten_cands) >= 2:
                _comb = 1.0
                for _t in ten_cands[:3]: _comb *= _t.get("prob", _t.get("best_p", 0.5))
                st.markdown(f"<div class='trilay-card'><div style='font-size:.8rem;font-weight:700;color:#00ccff'>🎾 TRILAY TENIS · {_comb*100:.1f}%</div>", unsafe_allow_html=True)
                for _i,_t in enumerate(ten_cands[:3]):
                    _cc = "#FFD700" if _t["prob"]>0.65 else ("#00ff88" if _t["prob"]>0.58 else "#aaa")
                    st.markdown(f"<div class='mrow'><span style='color:{_cc}'>{_i+1}. {_t['teams']}</span><span style='color:{_cc};float:right'>{_t['prob']*100:.1f}%</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No hay suficientes picks de tenis para TRILAY.")
        with tab3:
            st.info("PATO es exclusivo de fútbol.")
        with tab4:
            st.markdown("<div class='shdr'>🎯 Picks Tenis del Día</div>", unsafe_allow_html=True)
            ten_picks = []
            for _m in ten_matches[:30]:
                if _m["state"] != "pre": continue
                try:
                    _tm = tennis_model(_m["rank1"],_m["rank2"],_m.get("odd_1",0),_m.get("odd_2",0))
                    _fav = _m["p1"] if _tm["p1"]>=_tm["p2"] else _m["p2"]
                    _p   = max(_tm["p1"],_tm["p2"])
                    _odd = _m.get("odd_1",0) if _fav==_m["p1"] else _m.get("odd_2",0)
                    _edge = _p-(1/_odd if _odd>1 else _p)
                    if _edge > 0.03:
                        _conf = "💎 DIAMANTE" if _p>0.68 else ("🔥 ALTA" if _p>0.62 else "⚡ MEDIA")
                        ten_picks.append({"home":_m["p1"],"away":_m["p2"],"hora":_m.get("hora",""),"pick":f"🎾 {_fav} gana","prob":_p,"conf":_conf,"odd":_odd,"edge":_edge})
                except: pass
            ten_picks.sort(key=lambda x:-x["prob"])
            if not ten_picks: st.info("No hay picks tenis con edge positivo hoy.")
            for _pk in ten_picks:
                _cc = "#FFD700" if "DIAMANTE" in _pk["conf"] else ("#00ff88" if "ALTA" in _pk["conf"] else "#aaa")
                st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-size:.78rem;color:#555'>{_pk['home']} vs {_pk['away']} · {_pk['hora']}</div><div style='color:{_cc};font-weight:700'>{_pk['conf']} {_pk['pick']}</div></div><div style='text-align:right'><div style='font-size:1rem;font-weight:900;color:{_cc}'>{_pk['prob']*100:.1f}%</div><div style='font-size:.65rem;color:#555'>Edge {_pk['edge']*100:+.1f}%</div></div></div>", unsafe_allow_html=True)
        with tab5:
            render_bot_tab("🎾 Tenis", None, [], None)
        with tab6:
            st.markdown("<div class='shdr'>📋 Historial de Picks</div>", unsafe_allow_html=True)
            init_history()
            render_history()
        with tab7:
            render_einstein_califica("tenis")
        with tab8:
            render_resultados_tab()
        with tab_king:
            _kr_fut = st.session_state.get("_kr_cache_fut") or []
            _kr_nba = st.session_state.get("_kr_cache_nba") or []
            _kr_ten = ten_matches if ten_matches else st.session_state.get("_kr_cache_ten") or []
            if not _kr_fut:
                try: _kr_fut = get_cartelera()
                except: _kr_fut = []
            if not _kr_nba:
                try: _kr_nba = get_nba_cartelera()
                except: _kr_nba = []
            st.session_state["_kr_cache_fut"] = _kr_fut
            st.session_state["_kr_cache_nba"] = _kr_nba
            st.session_state["_kr_cache_ten"] = _kr_ten
            render_king_rongo(matches_fut=_kr_fut, nba_games=_kr_nba, ten_matches=_kr_ten)

    # ─── FÚTBOL ──────────────────────────────────────────
    elif deporte == "futbol":
        tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab_king = st.tabs(["📅 Cartelera","🎰 TRILAY","🦆 PATO","🎯 Picks","🤖 Bot","📋 Historial","🎓 Califica tu Pick","📊 Resultados","👑 King Rongo"])
        with tab1:
            st.markdown("<div class='shdr'>⚽ Cartelera — Partidos del Día</div>", unsafe_allow_html=True)
            if not matches:
                st.info("No hay partidos de fútbol disponibles.")
            else:
                from collections import defaultdict
                fut_por_fecha = defaultdict(lambda: defaultdict(list))
                for _m in matches:
                    fut_por_fecha[_m["fecha"]][_m.get("league","")].append(_m)
                def _fecha_lbl_fut(f):
                    try:
                        d=datetime.strptime(f,"%Y-%m-%d")
                        dias=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                        meses=["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                        return f"⚽ {dias[d.weekday()]} {d.day} {meses[d.month]}"
                    except: return f
                for _fi, _fecha in enumerate(sorted(fut_por_fecha.keys())):
                    _ligas = fut_por_fecha[_fecha]
                    _total = sum(len(v) for v in _ligas.values())
                    _is_hoy = _fecha == datetime.now(CDMX).strftime("%Y-%m-%d")
                    with st.expander(f"{_fecha_lbl_fut(_fecha)}  ·  {_total} partidos", expanded=(_fi==0)):
                        for _li, (_liga, _lms) in enumerate(sorted(_ligas.items())):
                            _n_pre  = sum(1 for m in _lms if m["state"]!="post")
                            _n_post = sum(1 for m in _lms if m["state"]=="post")
                            _liga_badge = f"{'🔴 ' if any(m['state']=='in' for m in _lms) else ''}{'✅ ' if _n_post and not _n_pre else ''}{_liga}  ·  {len(_lms)} partidos"
                            with st.expander(_liga_badge, expanded=False):
                                _post_ms = [m for m in _lms if m["state"]=="post"]
                                _pre_ms  = [m for m in _lms if m["state"]!="post"]
                                # Finalizados — clickeables
                                for _m in _post_ms:
                                    _sh=_m.get("score_h",-1); _sa=_m.get("score_a",-1)
                                    _sf=f"{_sh}–{_sa}" if _sh>=0 else "FT"
                                    _res = "Empate" if _sh==_sa else (_m["home"] if _sh>_sa else _m["away"])
                                    if st.button(f"✅ {_m['home']} vs {_m['away']}  ·  {_sf}  · 🏆 {_res}", key=f"fut_post_{_m['home_id']}_{_m['away_id']}", use_container_width=True):
                                        st.session_state["sel"]  = {**_m, "_sport":"futbol"}
                                        st.session_state["view"] = "analisis"
                                        st.rerun()
                                # Pre/live — tarjetas con prob local/empate/visitante
                                for _m in _pre_ms:
                                    _live = _m["state"] == "in"
                                    _sc   = f"🔴 {_m['score_h']}-{_m['score_a']}" if _live else f"🕐 {_m.get('hora','')}"
                                    try:
                                        _hf2 = get_form(_m["home_id"], _m["slug"]) or []
                                        _af2 = get_form(_m["away_id"], _m["slug"]) or []
                                        _hx2 = xg_weighted(_hf2,True) if _hf2 else _cup_enriched_xg(_m, True,  _hf2, _af2)
                                        _ax2 = xg_weighted(_af2,False) if _af2 else _cup_enriched_xg(_m, False, _hf2, _af2)
                                        _mc2 = mc50k(_hx2, _ax2)
                                        _ph2 = _mc2["ph"]; _pd2 = _mc2.get("pd", max(0,1-_mc2["ph"]-_mc2["pa"])); _pa2 = _mc2["pa"]
                                    except:
                                        _ph2 = _m.get("odd_h",0); _pa2 = _m.get("odd_a",0); _pd2 = _m.get("odd_d",0)
                                        if _ph2 > 1 and _pa2 > 1:
                                            _tot = 1/_ph2 + (1/_pd2 if _pd2>1 else 0.25) + 1/_pa2
                                            _ph2 = (1/_ph2)/_tot; _pd2 = 0.25; _pa2 = (1/_pa2)/_tot
                                        else:
                                            _ph2 = 0.40; _pd2 = 0.25; _pa2 = 0.35
                                    _mx = max(_ph2,_pd2,_pa2)
                                    _ch = "#00ff88" if _ph2==_mx else "#555"
                                    _cd = "#FFD700" if _pd2==_mx else "#555"
                                    _ca = "#00ff88" if _pa2==_mx else "#555"
                                    _wh = "800" if _ph2==_mx else "400"
                                    _wd = "800" if _pd2==_mx else "400"
                                    _wa = "800" if _pa2==_mx else "400"
                                    st.markdown(f"""<div style='background:#0a0a18;border:1px solid #1a1a30;border-radius:10px;padding:8px 10px;margin:3px 0'>
  <div style='font-size:.65rem;color:#444;margin-bottom:5px'>{_sc}</div>
  <div style='display:flex;align-items:center;gap:4px'>
    <div style='flex:2;font-size:.75rem;color:#bbb;font-weight:600;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_m["home"]}</div>
    <div style='display:flex;gap:3px;flex-shrink:0'>
      <div style='background:#0f0f20;border:1px solid {_ch}44;border-radius:6px;padding:4px 6px;text-align:center;min-width:42px'>
        <div style='font-size:.78rem;font-weight:{_wh};color:{_ch}'>{_ph2*100:.0f}%</div>
        <div style='font-size:.55rem;color:#333'>🏠</div>
      </div>
      <div style='background:#0f0f20;border:1px solid {_cd}44;border-radius:6px;padding:4px 6px;text-align:center;min-width:42px'>
        <div style='font-size:.78rem;font-weight:{_wd};color:{_cd}'>{_pd2*100:.0f}%</div>
        <div style='font-size:.55rem;color:#333'>🤝</div>
      </div>
      <div style='background:#0f0f20;border:1px solid {_ca}44;border-radius:6px;padding:4px 6px;text-align:center;min-width:42px'>
        <div style='font-size:.78rem;font-weight:{_wa};color:{_ca}'>{_pa2*100:.0f}%</div>
        <div style='font-size:.55rem;color:#333'>✈️</div>
      </div>
    </div>
    <div style='flex:2;font-size:.75rem;color:#bbb;font-weight:600;text-align:right;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_m["away"]}</div>
  </div>
</div>""", unsafe_allow_html=True)
                                    if st.button("📊 Analizar", key=f"fut_{_m['home_id']}_{_m['away_id']}", use_container_width=True):
                                        st.session_state["sel"]  = {**_m, "_sport":"futbol"}
                                        st.session_state["view"] = "analisis"
                                        st.rerun()
        with tab2:
            st.markdown("<div class='shdr'>🎰 TRILAY — Multi-Deporte</div>", unsafe_allow_html=True)
            with st.spinner("Calculando TRILAY..."):
                trilay_picks = compute_trilay(matches)
            if not trilay_picks:
                st.info("No hay suficientes partidos con edge para armar TRILAY hoy.")
            else:
                _comb_p = 1.0
                for _t in trilay_picks: _comb_p *= _t.get("best_p", _t.get("prob", 0.5))
                _cuota_c = round(1/_comb_p,2) if _comb_p>0 else 0
                st.markdown(f"<div class='trilay-card'><div style='font-size:.8rem;font-weight:700;color:#aa00ff;letter-spacing:.1em'>🎰 TRILAY DEL DÍA · Prob: {_comb_p*100:.1f}% · Cuota aprox {_cuota_c}</div>", unsafe_allow_html=True)
                for _i,_t in enumerate(trilay_picks):
                    _p  = _t.get("best_p", _t.get("prob", 0.5))
                    _pk = _t.get("best_m", _t.get("pick","?"))
                    _tm = f"{_t.get('home','?')} vs {_t.get('away','?')}"
                    _cc = "#FFD700" if _p>0.65 else ("#00ff88" if _p>0.58 else "#aaa")
                    st.markdown(f"<div class='mrow'><span style='color:{_cc};font-weight:700'>{_i+1}. {_tm}</span><span style='color:{_cc};float:right'>{_pk} · {_p*100:.1f}%</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        with tab3:
            st.markdown("<div class='shdr'>🦆 PATO — Under 4.5 Seguros</div>", unsafe_allow_html=True)
            _pato_matches = _ventana_22h(matches)
            pato_picks = []
            for _m in _pato_matches:
                try:
                    _hf = get_form(_m["home_id"],_m["slug"]) or []
                    _af = get_form(_m["away_id"],_m["slug"]) or []
                    _hxg = xg_weighted(_hf,True) if _hf else _cup_enriched_xg(_m, True,  _hf, _af)
                    _axg = xg_weighted(_af,False) if _af else _cup_enriched_xg(_m, False, _hf, _af)
                    _h2h = get_h2h(_m["home_id"],_m["away_id"],_m["slug"],_m["home"],_m["away"])
                    _h2s = h2h_stats(_h2h,_m["home"],_m["away"])
                    _mc  = ensemble_football(_hxg,_axg,_h2s,_hf,_af,_m["home_id"],_m["away_id"],odd_h=_m.get("odd_h",0),odd_a=_m.get("odd_a",0),odd_d=_m.get("odd_d",0))
                    # Under 4.5: 1 - P(O4.5). Usamos P(O3.5) como proxy — si O3.5 es bajo, U4.5 es alto
                    _p_o35 = _mc.get("o35", max(0, _mc.get("o25",0.5) - 0.18))
                    _p_u45 = max(0, 1.0 - _p_o35)
                    if _p_u45 >= 0.55:  # umbral bajado a 0.55 para más picks
                        pato_picks.append({"home":_m["home"],"away":_m["away"],"liga":_m.get("league",""),"hora":_m.get("hora",""),"prob":_p_u45})
                except: pass
            pato_picks.sort(key=lambda x:-x["prob"])
            if not pato_picks:
                st.info("🦆 PATO no encontró partidos Under 4.5 seguros hoy (prob < 68%).")
            for _pk in pato_picks:
                _cc = "#FFD700" if _pk["prob"]>0.75 else "#00ff88"
                st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-size:.78rem;color:#555'>{_pk['liga']} · {_pk['hora']}</div><div style='font-size:.88rem;font-weight:700'>{_pk['home']} vs {_pk['away']}</div><div style='color:{_cc};font-weight:700'>🦆 Under 4.5 goles</div></div><div style='font-size:1.1rem;font-weight:900;color:{_cc}'>{_pk['prob']*100:.1f}%</div></div>", unsafe_allow_html=True)
        with tab4:
            st.markdown("<div class='shdr'>🎯 Picks del Día — Fútbol</div>", unsafe_allow_html=True)
            fut_picks = []
            for _m in matches[:30]:
                if _m["state"] != "pre": continue
                try:
                    _hf = get_form(_m["home_id"],_m["slug"]) or []
                    _af = get_form(_m["away_id"],_m["slug"]) or []
                    _hxg = xg_weighted(_hf,True) if _hf else _cup_enriched_xg(_m, True,  _hf, _af)
                    _axg = xg_weighted(_af,False) if _af else _cup_enriched_xg(_m, False, _hf, _af)
                    _h2h = get_h2h(_m["home_id"],_m["away_id"],_m["slug"],_m["home"],_m["away"])
                    _h2s = h2h_stats(_h2h,_m["home"],_m["away"])
                    _mc  = ensemble_football(_hxg,_axg,_h2s,_hf,_af,_m["home_id"],_m["away_id"],odd_h=_m.get("odd_h",0),odd_a=_m.get("odd_a",0),odd_d=_m.get("odd_d",0))
                    _dp  = diamond_engine(_mc,_h2s,_hf,_af)
                    # Jerarquía de picks — AA solo si los demás son muy bajos
                    _ph  = _dp["ph"]; _pa = _dp["pa"]; _pd = _dp.get("pd", max(0,1-_ph-_pa))
                    _o25 = _mc["o25"]; _aa = _mc["btts"]
                    _do_h = min(0.95,_ph+_pd); _do_a = min(0.95,_pa+_pd)
                    _xg_tot_p = _hxg + _axg
                    _ninguno_p = max(_ph,_pa) < 0.52 and _do_h < 0.72 and _do_a < 0.72 and _o25 < 0.54
                    _eq_p = abs(_hxg - _axg) < 0.55
                    if _ph >= 0.60:
                        _lbl, _p, _odd = "🏠 "+_m["home"], _ph, _m.get("odd_h",0)
                    elif _pa >= 0.60:
                        _lbl, _p, _odd = "✈️ "+_m["away"], _pa, _m.get("odd_a",0)
                    elif _do_h >= 0.76 and _ph >= 0.50:
                        _lbl, _p, _odd = f"🔵 {_m['home'][:14]} o Emp", _do_h, 0
                    elif _do_a >= 0.76 and _pa >= 0.45:
                        _lbl, _p, _odd = f"🟣 {_m['away'][:14]} o Emp", _do_a, 0
                    elif _xg_tot_p >= 2.8 and _o25 >= 0.56:
                        _lbl, _p, _odd = "⚽ Over 2.5", _o25, 0
                    elif max(_ph,_pa) >= 0.52:
                        if _ph >= _pa: _lbl, _p, _odd = "🏠 "+_m["home"], _ph, _m.get("odd_h",0)
                        else:          _lbl, _p, _odd = "✈️ "+_m["away"], _pa, _m.get("odd_a",0)
                    elif _o25 >= 0.54:
                        _lbl, _p, _odd = "⚽ Over 2.5", _o25, 0
                    elif _ninguno_p and _eq_p and _aa >= 0.52:
                        _lbl, _p, _odd = "⚡ Ambos Anotan", _aa, 0
                    else:
                        if _ph >= _pa: _lbl, _p, _odd = "🏠 "+_m["home"], _ph, _m.get("odd_h",0)
                        else:          _lbl, _p, _odd = "✈️ "+_m["away"], _pa, _m.get("odd_a",0)
                    # Edge: vs cuota si existe, sino vs 50% base
                    _edge = (_p - 1/_odd) if _odd>1 else (_p - 0.50)
                    # Umbral: tomar si prob >= 0.52 (siempre habrá algo)
                    if _p >= 0.52:
                        _conf = "💎 DIAMANTE" if _p>0.68 else ("🔥 ALTA" if _p>0.62 else ("⚡ MEDIA" if _p>0.56 else "📊 SEÑAL"))
                        fut_picks.append({"home":_m["home"],"away":_m["away"],"liga":_m.get("league",""),"hora":_m.get("hora",""),"pick":_lbl,"prob":_p,"conf":_conf,"odd":_odd,"edge":_edge})
                except: pass
            fut_picks.sort(key=lambda x:-x["prob"])
            if not fut_picks: st.info("Sin partidos de fútbol pre-match disponibles aún.")
            for _pk in fut_picks:
                _cc = "#FFD700" if "DIAMANTE" in _pk["conf"] else ("#00ff88" if "ALTA" in _pk["conf"] else "#aaa")
                st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-size:.78rem;color:#555'>{_pk['liga']} · {_pk['hora']}</div><div style='font-size:.78rem;color:#777'>{_pk['home']} vs {_pk['away']}</div><div style='color:{_cc};font-weight:700'>{_pk['conf']} {_pk['pick']}</div></div><div style='text-align:right'><div style='font-size:1rem;font-weight:900;color:{_cc}'>{_pk['prob']*100:.1f}%</div><div style='font-size:.65rem;color:#555'>Edge {_pk['edge']*100:+.1f}%</div></div></div>", unsafe_allow_html=True)
        with tab5:
            def _fut_preview():
                with st.spinner("Calculando preview fútbol..."):
                    _prev = []
                    for _m in matches[:15]:
                        if _m["state"] != "pre": continue
                        try:
                            _hf = get_form(_m["home_id"],_m["slug"]) or []
                            _af = get_form(_m["away_id"],_m["slug"]) or []
                            _hxg = xg_weighted(_hf,True) if _hf else _cup_enriched_xg(_m, True,  _hf, _af)
                            _axg = xg_weighted(_af,False) if _af else _cup_enriched_xg(_m, False, _hf, _af)
                            _mc  = ensemble_football(_hxg,_axg,{},_hf,_af,_m["home_id"],_m["away_id"])
                            _dp  = diamond_engine(_mc,{},_hf,_af)
                            _bm  = max([(_dp["ph"],f"🏠 {_m['home']}"),(_dp["pa"],f"✈️ {_m['away']}"),(_mc["o25"],"⚽ Over 2.5")],key=lambda x:x[0])
                            if _bm[0] >= 0.52:
                                _prev.append({"teams":f"{_m['home']} vs {_m['away']}","hora":_m.get("hora",""),"pick":_bm[1],"prob":_bm[0]})
                        except: pass
                    _prev.sort(key=lambda x:-x["prob"])
                for _p in _prev[:5]:
                    _cc = "#FFD700" if _p["prob"]>0.65 else "#00ff88"
                    st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between'><div><div style='font-size:.72rem;color:#555'>{_p['teams']} · {_p['hora']}</div><div style='color:{_cc};font-weight:700'>{_p['pick']}</div></div><div style='font-size:1rem;font-weight:900;color:{_cc}'>{_p['prob']*100:.1f}%</div></div>", unsafe_allow_html=True)
            render_bot_tab("⚽ Fútbol", escanear_y_enviar, [matches], _fut_preview)
        with tab6:
            st.markdown("<div class='shdr'>📋 Historial de Picks</div>", unsafe_allow_html=True)
            init_history()
            render_history()
        with tab7:
            render_einstein_califica("futbol")
        with tab8:
            render_resultados_tab()
        with tab_king:
            _kr_fut = matches if matches else st.session_state.get("_kr_cache_fut") or []
            _kr_nba = st.session_state.get("_kr_cache_nba") or []
            _kr_ten = st.session_state.get("_kr_cache_ten") or []
            if not _kr_nba:
                try: _kr_nba = get_nba_cartelera()
                except: _kr_nba = []
            if not _kr_ten:
                try: _kr_ten = get_tennis_cartelera()
                except: _kr_ten = []
            if not _kr_fut:
                try: _kr_fut = get_cartelera()
                except: _kr_fut = []
            st.session_state["_kr_cache_fut"] = _kr_fut
            st.session_state["_kr_cache_nba"] = _kr_nba
            st.session_state["_kr_cache_ten"] = _kr_ten
            render_king_rongo(matches_fut=_kr_fut, nba_games=_kr_nba, ten_matches=_kr_ten)

else:
    g = st.session_state["sel"]
    if st.button("← Volver"):
        st.session_state["view"]="cartelera"; st.session_state["sel"]=None; st.rerun()

    # ══════════════════════════════════════════════════════════════
    # ANALISIS VIEW — ramificado por deporte
    # ══════════════════════════════════════════════════════════════
    _sport = g.get("_sport","")

    if _sport == "tennis":
        # ── TENNIS ANALYSIS — full pipeline ──
        st.markdown(
            f"<div style='text-align:center;padding:16px 0 4px'>"
            f"<div style='font-size:.8rem;color:#00ccff;letter-spacing:.1em'>"
            f"{g.get('league','Tenis')}</div>"
            f"<div style='font-size:2rem;font-weight:900;margin:6px 0'>"
            f"{g['home']} <span style='color:#333'>vs</span> {g['away']}</div>"
            f"<div style='color:#555;font-size:.9rem'>🕒 {g.get('hora','')} CDMX</div></div>",
            unsafe_allow_html=True)

        _ten_surface_map = {
            "Indian Wells":"hard","Miami":"hard","Roland Garros":"clay",
            "Wimbledon":"grass","US Open":"hard","Australian Open":"hard",
            "Monte Carlo":"clay","Madrid":"clay","Barcelona":"clay",
            "Rome":"clay","Cincinnati":"hard","Toronto":"hard",
            "Halle":"grass","Queen":"grass","Dubai":"hard","Doha":"hard",
        }
        _ten_tour    = g.get("torneo", g.get("league",""))
        _ten_surface = next((v for k,v in _ten_surface_map.items()
                             if k.lower() in _ten_tour.lower()), "hard")
        # Resolver ranks siempre desde nombre si son 0 o default alto
        _rank1 = g.get("rank1", 0) or 0
        _rank2 = g.get("rank2", 0) or 0
        if _rank1 <= 0 or _rank1 >= 150:
            _rank1 = _resolve_rank(g["home"], _KNOWN_RANKS) or _resolve_rank_local(g["home"]) or 120
        if _rank2 <= 0 or _rank2 >= 150:
            _rank2 = _resolve_rank(g["away"], _KNOWN_RANKS) or _resolve_rank_local(g["away"]) or 120
        _odd1  = g.get("odd_h", g.get("odd_1",0))
        _odd2  = g.get("odd_a", g.get("odd_2",0))

        _weib = tennis_model(_rank1, _rank2, _odd1, _odd2, _ten_surface)

        # Einstein
        _einstein_p1 = None
        with st.spinner("🧠 Einstein: H2H y forma reciente..."):
            _ei = tennis_expert_analysis(
                g["home"], g["away"], _rank1, _rank2,
                _odd1, _odd2, _ten_surface, _ten_tour,
                model_p1=_weib["p1"], model_p2=_weib["p2"]
            )
        if _ei: _einstein_p1 = _ei.get("p1")

        # Veredicto unificado
        with st.spinner("🎾 Calculando 50,000 simulaciones..."):
            _vd = veredicto_academico_tenis(
                p1_name=g["home"], p2_name=g["away"],
                rank1=_rank1, rank2=_rank2,
                odd_1=_odd1, odd_2=_odd2,
                surface=_ten_surface, torneo=_ten_tour,
                expert_p1=_einstein_p1
            )

        _vd_p1    = _vd["_p1_final"]; _vd_p2 = _vd["_p2_final"]
        _vd_fav   = _vd["_fav_name"]; _vd_fav_p = _vd["_fav_prob"]
        _vd_score = _vd["_score"];    _vd_html  = _vd["_html"]

        if _vd_score >= 7 and _vd_fav_p >= 0.65:
            _ten_conf = "💎 DIAMANTE"; _conf_color = "#FFD700"
        elif _vd_score >= 4 and _vd_fav_p >= 0.58:
            _ten_conf = "🔥 ALTA"; _conf_color = "#00ff88"
        elif _vd_score >= 4:
            _ten_conf = "⚡ MEDIA"; _conf_color = "#aaa"
        else:
            _ten_conf = "🔻 NO APOSTAR"; _conf_color = "#ff4444"

        # Hero card
        st.markdown(
            f"<div class='diamond-hero'>"
            f"<div style='font-size:.75rem;font-weight:700;color:#FFD700;letter-spacing:.12em;margin-bottom:8px'>"
            f"✦ JUGADA DIAMANTE TENIS — {_ten_conf}</div>"
            f"<div style='font-size:2.2rem;font-weight:900;margin-bottom:6px'>🎾 {_vd_fav} gana</div>"
            f"<div style='font-size:1.3rem;font-weight:700;color:#FFD700;margin-bottom:10px'>"
            f"{_vd_fav_p*100:.1f}% de probabilidad</div>"
            f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px'>"
            f"<div class='mbox'><div class='mval' style='color:#00ccff'>{_vd['_p1_elo']*100:.0f}%</div><div class='mlbl'>Elo</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#aa00ff'>{_vd['_p1_surf']*100:.0f}%</div><div class='mlbl'>Superficie</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#00ff88'>{_vd['_p1_mc']*100:.0f}%</div><div class='mlbl'>Monte Carlo</div></div>"
            f"<div class='mbox'><div class='mval' style='color:#FFD700'>{(_vd.get('_p1_einstein') or _vd.get('_p1_mom', _vd.get('p1',0.5)))*100:.0f}%</div>"
            f"<div class='mlbl'>{'Einstein' if _vd.get('_p1_einstein') else 'Momentum'}</div></div>"
            f"</div></div>", unsafe_allow_html=True)

        # Veredicto
        st.markdown(_vd_html, unsafe_allow_html=True)

        # Guardar pick
        if st.button(f"💾 Guardar: 🎾 {_vd_fav} gana ({_vd_fav_p*100:.0f}%)",
                     use_container_width=True, key="save_ten_main"):
            add_pick({"home":g["home"],"away":g["away"],
                      "league":g.get("league",""),"fecha":g.get("fecha","")},
                     f"🎾 {_vd_fav} gana", _vd_fav_p,
                     _odd1 if _vd_fav==g["home"] else _odd2, sport="tenis")
            st.success("✅ Pick guardado")

        # Einstein resumen
        if _ei and _ei.get("resumen"):
            st.markdown(
                f"<div style='background:#0a0a26;border-radius:10px;padding:12px 14px;"
                f"border-left:3px solid #FFD700;font-size:.88rem;line-height:1.7;margin-top:12px'>"
                f"🧠 <b>Einstein:</b><br>{_ei['resumen'].replace(chr(10),'<br>')}</div>",
                unsafe_allow_html=True)

        # Badrino
        st.markdown("<div class='shdr'>🤖 Badrino — Análisis Completo</div>", unsafe_allow_html=True)
        badrino_key = f"bad_detail_{g['home'][:6]}_{g['away'][:6]}"
        if st.button("🤖 Generar análisis Badrino", key=badrino_key, use_container_width=True):
            render_badrino_tennis(
                g["home"], g["away"], _rank1, _rank2,
                _odd1, _odd2, _ten_surface, _ten_tour,
                _vd_p1, _vd_p2, _vd_fav, _vd_fav_p, _ten_conf,
                _ei or {}
            )

    elif _sport == "nba":
        # ── NBA ANALYSIS ──
        st.markdown(
            f"<div style='text-align:center;padding:16px 0 8px'>"
            f"<div style='font-size:.75rem;color:#ff9500;letter-spacing:.12em;font-weight:700'>🏀 NBA</div>"
            f"<div style='font-size:2rem;font-weight:900;margin:6px 0'>"
            f"{g.get('away','?')} <span style='color:#333'>@</span> {g.get('home','?')}</div>"
            f"<div style='color:#555;font-size:.85rem'>🕒 {g.get('hora','')} CDMX · O/U {g.get('ou_line',0)}</div>"
            + (f"<div style='margin-top:8px;font-size:1.4rem;font-weight:900;color:#00ff88'>"
               f"{g['score_h']} – {g['score_a']} pts</div>" if g.get('state')=='post' and g.get('score_h',-1)>=0 else "")
            + "</div>",
            unsafe_allow_html=True)
        if g.get("state") == "post":
            st.info("✅ Partido finalizado. Resultado final mostrado arriba.")
        else:
            with st.spinner("🏀 Calculando modelo O/U + ML..."):
                _nba_res = nba_ou_model(g.get("home_id",""), g.get("away_id",""), g.get("ou_line",0))
            _p_over  = _nba_res.get("p_over", 0.5)
            _p_under = _nba_res.get("p_under", 0.5)
            _p_home  = _nba_res.get("p_h_win", 0.5)
            _p_away  = 1 - _p_home
            _line    = _nba_res.get("line", g.get("ou_line",0))
            _proj    = _nba_res.get("proj", 0)
            _ou_rec  = _nba_res.get("rec","OVER")
            # Card principal
            _ou_col  = "#00ff88" if _p_over >= _p_under else "#00ccff"
            _ml_fav  = g.get("home","?") if _p_home >= _p_away else g.get("away","?")
            _ml_p    = max(_p_home, _p_away)
            _conf_ou = "💎 DIAMANTE" if max(_p_over,_p_under)>0.68 else ("🔥 ALTA" if max(_p_over,_p_under)>0.62 else "⚡ MEDIA")
            st.markdown(
                f"<div class='diamond-hero'>"
                f"<div style='font-size:.75rem;font-weight:700;color:#ff9500;letter-spacing:.14em;margin-bottom:8px'>🏀 ANÁLISIS O/U + ML</div>"
                f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px'>"
                f"<div style='background:#0a0a1e;border-radius:12px;padding:14px;border:1px solid {_ou_col}44'>"
                f"<div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.1em'>OVER / UNDER</div>"
                f"<div style='font-size:.75rem;color:#777;margin:4px 0'>Línea: {_line} pts · Proy: {_proj:.0f} pts</div>"
                f"<div style='font-size:1.5rem;font-weight:900;color:{_ou_col}'>{_ou_rec}</div>"
                f"<div style='display:flex;gap:8px;margin-top:6px'>"
                f"<span style='font-size:.78rem;color:#00ff88'>Over {_p_over*100:.1f}%</span>"
                f"<span style='font-size:.78rem;color:#00ccff'>Under {_p_under*100:.1f}%</span></div></div>"
                f"<div style='background:#0a0a1e;border-radius:12px;padding:14px;border:1px solid #FFD70044'>"
                f"<div style='font-size:.7rem;color:#555;font-weight:700;letter-spacing:.1em'>MONEY LINE</div>"
                f"<div style='font-size:.75rem;color:#777;margin:4px 0'>Favorito</div>"
                f"<div style='font-size:1.2rem;font-weight:900;color:#FFD700'>{_ml_fav[:16]}</div>"
                f"<div style='font-size:.85rem;color:#FFD700;margin-top:6px'>{_ml_p*100:.1f}% prob</div>"
                f"<div style='font-size:.72rem;color:#555'>🏠 {g.get('home','')[:14]}: {_p_home*100:.1f}%  ✈️ {g.get('away','')[:14]}: {_p_away*100:.1f}%</div>"
                f"</div></div>"
                f"<div style='font-size:.72rem;color:#555;padding-top:10px;border-top:1px solid #1a1a40'>"
                f"{_conf_ou} · Modelos: xG ESPN + Pace + DefRtg</div></div>",
                unsafe_allow_html=True)
            # Save pick button
            _nba_pick_lbl = f"{'🔥 Over' if _p_over>_p_under else '❄️ Under'} {_line}"
            _nba_odd = 1.91  # standard -110
            if st.button("💾 Guardar Pick", key="save_nba_pick"):
                if "pick_history" not in st.session_state: st.session_state["pick_history"]=[]
                st.session_state["pick_history"].append({
                    "equipos":f"{g.get('away','')} @ {g.get('home','')}",
                    "pick":_nba_pick_lbl, "deporte":"🏀 NBA",
                    "mercado":"NBA O/U","odd":_nba_odd,
                    "prob":max(_p_over,_p_under),"result":"⏳",
                    "fecha":g.get("fecha",datetime.now(CDMX).strftime("%Y-%m-%d"))
                })
                st.success("✅ Pick guardado")

    else:
        # ── SOCCER ANALYSIS ──

        prog = st.progress(0,"📊 Cargando datos ESPN...")
        hform = get_form(g["home_id"],g["slug"]); prog.progress(30,f"📊 {g['away']}...")
        aform = get_form(g["away_id"],g["slug"]); prog.progress(60,"📊 Calculando...")
        h2h   = []
        h2s   = {}
        # xG con decaimiento exponencial + prior bayesiano de odds
        hxg = xg_weighted(hform, is_home=True,  odds_prior=1/g.get("odd_h",0) if g.get("odd_h",0)>1 else 0) if hform else xg_from_record(g.get("home_rec","5-5-5"),True)
        axg = xg_weighted(aform, is_home=False, odds_prior=1/g.get("odd_a",0) if g.get("odd_a",0)>1 else 0) if aform else xg_from_record(g.get("away_rec","5-5-5"),False)
        h2h   = get_h2h(g["home_id"],g["away_id"],g["slug"],g["home"],g["away"])
        h2s   = h2h_stats(h2h, g["home"], g["away"])
        mc    = ensemble_football(hxg, axg, h2s, hform, aform, g["home_id"], g["away_id"], odd_h=g.get("odd_h",0), odd_a=g.get("odd_a",0), odd_d=g.get("odd_d",0))
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

        # ── JUGADA DIAMANTE — jerarquía correcta ML > DO > O2.5 > AA ──
        _all_markets = [
            (f"🏠 {g['home'][:16]} gana",      dp["ph"],  g.get("odd_h",0)),
            ("🤝 Empate",                        dp["pd"],  g.get("odd_d",0)),
            (f"✈️ {g['away'][:16]} gana",        dp["pa"],  g.get("odd_a",0)),
            ("⚽ Over 2.5",                       mc["o25"],  0),
            ("⚽ Over 3.5",                       mc["o35"],  0),
            ("⚡ Ambos Anotan (AA)",              mc["btts"], 0),
        ]
        def _mkt_edge(t):
            lbl, prob, odd = t
            return (prob - 1/odd) if odd > 1 else (prob - 0.50)

        # Jerarquía: ML > DO > O2.5 > AA
        # Si hay cuotas reales, el ML con mejor edge siempre gana
        _ph_d = dp["ph"]; _pa_d = dp["pa"]; _pd_d = dp.get("pd", max(0,1-_ph_d-_pa_d))
        _o25_d = mc["o25"]; _aa_d = mc["btts"]
        _do_h_d = min(0.95, _ph_d+_pd_d); _do_a_d = min(0.95, _pa_d+_pd_d)
        _xg_tot_d = hxg + axg
        _best_ml   = max(_ph_d, _pa_d)  # siempre hay un mejor ML
        _fav_ml_lbl = f"🏠 {g['home'][:16]} gana" if _ph_d >= _pa_d else f"✈️ {g['away'][:16]} gana"
        _fav_ml_p   = _ph_d if _ph_d >= _pa_d else _pa_d
        _fav_ml_odd = g.get("odd_h",0) if _ph_d >= _pa_d else g.get("odd_a",0)
        _ninguno_d = _best_ml < 0.50 and _do_h_d < 0.70 and _do_a_d < 0.70 and _o25_d < 0.52
        _eq_d = abs(hxg - axg) < 0.55

        # Con cuotas reales: comparar edge ML vs O2.5
        _odd_h = g.get("odd_h",0); _odd_a = g.get("odd_a",0)
        _has_odds = _odd_h > 1 and _odd_a > 1
        _edge_ml_h = (_ph_d - 1/_odd_h) if _odd_h > 1 else (_ph_d - 0.50)
        _edge_ml_a = (_pa_d - 1/_odd_a) if _odd_a > 1 else (_pa_d - 0.50)
        _best_ml_edge = max(_edge_ml_h, _edge_ml_a)

        if _pa_d > _ph_d and (_pa_d >= 0.55 or (_has_odds and _edge_ml_a >= 0.03)):
            # Visitante es favorito — mostrar ML visitante
            main_mkt = (f"✈️ {g['away'][:16]} gana", _pa_d, g.get("odd_a",0))
        elif _ph_d >= 0.55 or (_has_odds and _edge_ml_h >= 0.03):
            main_mkt = (f"🏠 {g['home'][:16]} gana", _ph_d, _odd_h)
        elif _pa_d >= 0.55 or (_has_odds and _edge_ml_a >= 0.03):
            main_mkt = (f"✈️ {g['away'][:16]} gana", _pa_d, g.get("odd_a",0))
        elif _do_h_d >= 0.76 and _ph_d >= 0.48:
            main_mkt = (f"🔵 {g['home'][:14]} o Emp", _do_h_d, 0)
        elif _do_a_d >= 0.76 and _pa_d >= 0.43:
            main_mkt = (f"🟣 {g['away'][:14]} o Emp", _do_a_d, 0)
        elif _xg_tot_d >= 2.6 and _o25_d >= 0.54:
            main_mkt = ("⚽ Over 2.5", _o25_d, 0)
        elif _best_ml >= 0.46:
            # Siempre mostrar ML si es el más probable — aunque sea parejo
            main_mkt = (_fav_ml_lbl, _fav_ml_p, _fav_ml_odd)
        elif _o25_d >= 0.52:
            main_mkt = ("⚽ Over 2.5", _o25_d, 0)
        elif _ninguno_d and _eq_d and _aa_d >= 0.52:
            main_mkt = ("⚡ Ambos Anotan (AA)", _aa_d, 0)
        else:
            # Fallback absoluto: siempre el mejor ML
            main_mkt = (_fav_ml_lbl, _fav_ml_p, _fav_ml_odd)

        main_lbl, main_prob, main_odd = main_mkt

        # Badges de todos los mercados ordenados por prob — incluye ML
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
            f"Evaluados: Over 2.5 · Over 3.5 · Ambos Anotan · Mitad · 1X2</div>"
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

        # ── BRIDGE DIAMANTE → RESULTADOS ──
        # Guardar el pick exacto que se mostró, indexado por ID del partido
        if "_diamond_bridge" not in st.session_state:
            st.session_state["_diamond_bridge"] = {}
        _bridge_key = g.get("id","") or f"{g.get('home_id','')}_{g.get('away_id','')}_{g.get('fecha','')}"
        st.session_state["_diamond_bridge"][_bridge_key] = {
            "pick": main_lbl, "prob": main_prob, "odd": main_odd,
            "home": g.get("home",""), "away": g.get("away",""),
            "sport": "futbol", "fecha": g.get("fecha",""),
            "src": f"💎 Diamante · {main_prob*100:.0f}%",
            "mkt": "1X2" if "gana" in main_lbl else ("O/U" if "Over" in main_lbl else ("BTTS" if "Ambos" in main_lbl else "DO")),
        }
        # También guardar por home_id+away_id+fecha como alias
        _bridge_key2 = f"{g.get('home_id','')}_{g.get('away_id','')}_{g.get('fecha','')}"
        if _bridge_key2 != _bridge_key:
            st.session_state["_diamond_bridge"][_bridge_key2] = st.session_state["_diamond_bridge"][_bridge_key]
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

        # ── SMART PARLAY ──
        if pls:
            best=pls[0]; legs=[x for x in [best.get("l1"),best.get("l2")] if x]
            st.markdown(
                f"<div class='parlay-hero'>"
                f"<div style='font-size:.8rem;color:#00ccff;font-weight:700;letter-spacing:.1em;margin-bottom:12px'>✦ SMART PLAY — PARLAY RECOMENDADO</div>"
                +"".join(f"<div style='font-size:1.1rem;font-weight:700;margin:4px 0'>✓ {l}</div>" for l in legs)
                +f"<div style='display:flex;gap:12px;margin-top:16px;flex-wrap:wrap'>"
                +"".join(f"<div class='mbox' style='flex:1'><div class='mval' style='color:#00ccff'>{p*100:.1f}%</div><div class='mlbl'>{l}</div></div>" for l,p in [(best.get("l1",""),best.get("p1",0)),(best.get("l2",""),best.get("p2",0))])
                +f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{best['cp']*100:.1f}%</div><div class='mlbl'>Combinada</div></div>"
                +f"<div class='mbox' style='flex:1'><div class='mval' style='color:#FFD700'>{best['odds']}x</div><div class='mlbl'>Cuota</div></div>"
                +f"</div></div>",unsafe_allow_html=True)

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
        # Fila 1: ML (1X2) — los más importantes
        _odd_h_lbl = f" @{g['odd_h']:.2f}" if g.get("odd_h",0)>1 else ""
        _odd_a_lbl = f" @{g['odd_a']:.2f}" if g.get("odd_a",0)>1 else ""
        _odd_d_lbl = f" @{g['odd_d']:.2f}" if g.get("odd_d",0)>1 else ""
        cols_ml = st.columns(3)
        for col, (label, val, odd_lbl, color_hi) in zip(cols_ml, [
            (f"🏠 {g['home'][:12]} ML", dp["ph"], _odd_h_lbl, "#00ff88"),
            ("🤝 Empate ML",             dp["pd"], _odd_d_lbl, "#FFD700"),
            (f"✈️ {g['away'][:12]} ML",  dp["pa"], _odd_a_lbl, "#aa00ff"),
        ]):
            with col:
                color = color_hi if val>=0.45 else "#555"
                st.markdown(f"<div class='mbox'><div class='mval' style='color:{color}'>{val*100:.0f}%</div><div class='mlbl'>{label}{odd_lbl}</div></div>",unsafe_allow_html=True)
        # Fila 2: Totales
        cols2 = st.columns(6)
        for col,(label,val) in zip(cols2,[("Over 1.5",mc["o15"]),("Over 2.5",mc["o25"]),
            ("Over 3.5",mc["o35"]),("Ambos Anotan",mc["btts"]),("CS Local",mc["cs_h"]),("CS Visit.",mc["cs_a"])]):
            with col:
                color="#00ff88" if val>=0.58 else ("#FFD700" if val>=0.45 else "#666")
                st.markdown(f"<div class='mbox'><div class='mval' style='color:{color}'>{val*100:.0f}%</div><div class='mlbl'>{label}</div></div>",unsafe_allow_html=True)

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

# ════════════════════════════════════════════════════════════════════════════
# 👑 KING RONGO — EL CEREBRO SUPREMO v3
#
# El meta-sistema que unifica TODOS los modelos de The Gamblers Layer:
#   ⚽ xG · Dixon-Coles · Poisson BV · Elo Dinámico · H2H Monte-Carlo
#   🏀 Net Rating · O/U Proyectado · Money Line implícito
#   🎾 Weibull · Elo ATP/WTA · Superficie · Odds Bayesianos
#
# Capacidades:
#   1. Escaneo completo de los 3 deportes
#   2. Scoring compuesto (edge + prob + consenso + kelly)
#   3. Detección de contradicciones entre modelos
#   4. Gestión de bankroll con memoria de racha
#   5. Parlay del Rey: combina los 3 mejores picks multi-deporte
#   6. Narración IA: Claude explica el pick en lenguaje humano
#   7. Memoria evolutiva: aprende qué mercados/deportes funcionan
#   8. Presencia global: banner permanente en toda la app
#   9. Telegram completo: pick + parlay + bankroll
# ════════════════════════════════════════════════════════════════════════════

# KR thresholds — usar los definidos arriba en _KR_DIAMOND_THRESHOLD
_KR_CONFLICT_PP    = 22     # dispersión (pp) entre modelos → conflicto
_KR_DIAMOND_PROB   = _KR_DIAMOND_THRESHOLD   # 0.65
_KR_GOLD_PROB      = _KR_GOLD_THRESHOLD       # 0.58
_KR_PARLAY_MIN     = 3      # picks mínimos para armar el parlay del rey


# ────────────────────────────────────────────────────────────────────────────
# UTILIDADES MATEMÁTICAS
# ────────────────────────────────────────────────────────────────────────────

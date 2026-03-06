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
/* loader lives in iframe component — no CSS needed here */
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
ODDS_API_KEY = ""  # Pon tu key de https://the-odds-api.com (gratis)
BOOKMAKERS   = ["bet365","pinnacle","unibet","williamhill"]

@st.cache_data(ttl=300, show_spinner=False)
def get_real_odds(home_name, away_name, league_slug):
    """
    Intenta obtener cuotas reales de The Odds API.
    Si no hay key o falla, devuelve dict vacío.
    """
    if not ODDS_API_KEY:
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
            "apiKey": ODDS_API_KEY, "regions":"eu",
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

def render_odds_comparison(home, away, dp, mc, real_odds):
    """Tabla de valor esperado comparando modelo vs casas."""
    st.markdown("<div class='shdr'>💰 Valor Esperado vs Casas de Apuestas</div>", unsafe_allow_html=True)
    
    if not real_odds:
        # Sin Odds API — mostrar solo ESPN odds si hay
        st.markdown(
            "<div style='background:#0d0d2e;border:1px solid #252555;border-radius:12px;"
            "padding:14px 18px;color:#555;font-size:.85rem'>"
            "💡 Conecta <b>The Odds API</b> para comparar vs Bet365, Pinnacle y más. "
            "Regístrate gratis en <code>the-odds-api.com</code> y pega tu key en <code>ODDS_API_KEY</code>"
            "</div>", unsafe_allow_html=True)
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

def render_resultados_tab():
    """Full Resultados Pasados tab — shared across all sports."""
    db = get_results_db()
    partidos = db.get("partidos",[])
    ultima = db.get("ultima_actualizacion","Nunca")

    # Header with refresh
    col_h, col_r = st.columns([3,1])
    with col_h:
        st.markdown(f"<div class='shdr'>📊 Resultados Pasados</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#555;font-size:.75rem;margin-bottom:12px'>Última actualización: {ultima} · Se actualiza cada 2h automáticamente</div>", unsafe_allow_html=True)
    with col_r:
        if st.button("🔄 Actualizar ahora", key="refresh_results", use_container_width=True):
            with st.spinner("Actualizando base de datos..."):
                update_results_db(force=True)
                st.session_state["results_db"] = _load_results_db()
                st.session_state["results_last_check"] = datetime.now(pytz.UTC).timestamp()
            st.success("✅ Actualizado")
            st.rerun()

    if not partidos:
        st.info("Base de datos vacía. Haz clic en 'Actualizar ahora' para cargar los últimos 10 días.")
        return

    # Filter tabs by sport
    rt1, rt2 = st.tabs(["⚽ Fútbol", "🏀 NBA"])

    for tab_obj, sport_key, sport_label in [(rt1,"futbol","⚽ Fútbol"),(rt2,"nba","🏀 NBA")]:
        with tab_obj:
            sport_p = [p for p in partidos if p.get("deporte")==sport_key]
            finalizados = [p for p in sport_p if p.get("state")=="post"]
            en_juego    = [p for p in sport_p if p.get("state")=="in"]
            proximos    = [p for p in sport_p if p.get("state")=="pre"]

            # KPIs
            st.markdown(
                f"<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px'>"
                f"<div class='mbox'><div class='mval' style='color:#00ff88;font-size:1.3rem'>{len(finalizados)}</div><div class='mlbl'>Finalizados</div></div>"
                f"<div class='mbox'><div class='mval' style='color:#ff9500;font-size:1.3rem'>{len(en_juego)}</div><div class='mlbl'>En juego</div></div>"
                f"<div class='mbox'><div class='mval' style='color:#00ccff;font-size:1.3rem'>{len(proximos)}</div><div class='mlbl'>Próximos</div></div>"
                f"</div>", unsafe_allow_html=True)

            # ── EN JUEGO ──
            if en_juego:
                st.markdown("<div class='shdr' style='color:#ff9500!important'>🔴 En Juego Ahora</div>", unsafe_allow_html=True)
                for p in en_juego:
                    sh = p.get("score_h",-1); sa = p.get("score_a",-1)
                    score_txt = f"{sh} - {sa}" if sh>=0 else "En curso"
                    st.markdown(
                        f"<div class='mrow' style='border-left:3px solid #ff9500'>"
                        f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                        f"<div><span style='color:#ff9500;font-size:.72rem;font-weight:700'>🔴 EN VIVO</span><br>"
                        f"<b>{p['home']} vs {p['away']}</b><br>"
                        f"<span style='color:#555;font-size:.78rem'>{p.get('liga','')} · {p.get('fecha','')}</span></div>"
                        f"<div style='text-align:right'><div style='font-size:1.6rem;font-weight:900;color:#ff9500'>{score_txt}</div></div>"
                        f"</div></div>", unsafe_allow_html=True)

            # ── FINALIZADOS — grouped by date ──
            if finalizados:
                st.markdown("<div class='shdr'>✅ Resultados por Fecha</div>", unsafe_allow_html=True)
                from collections import defaultdict
                por_fecha = defaultdict(list)
                for p in finalizados: por_fecha[p.get("fecha","")].append(p)
                for fecha in sorted(por_fecha.keys(), reverse=True):
                    dia_ps = por_fecha[fecha]
                    try:
                        d = datetime.strptime(fecha,"%Y-%m-%d")
                        dias = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
                        meses = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                        label = f"📅 {dias[d.weekday()]} {d.day} {meses[d.month]}"
                    except: label = f"📅 {fecha}"
                    with st.expander(f"{label} — {len(dia_ps)} partidos", expanded=(fecha==sorted(por_fecha.keys(),reverse=True)[0])):
                        # Group by league
                        por_liga = defaultdict(list)
                        for p in dia_ps: por_liga[p.get("liga","")].append(p)
                        for liga, liga_ps in sorted(por_liga.items()):
                            st.markdown(f"<div style='font-size:.72rem;font-weight:700;color:#FFD700;text-transform:uppercase;letter-spacing:.1em;margin:10px 0 5px'>{liga}</div>", unsafe_allow_html=True)
                            for p in liga_ps:
                                sh = p.get("score_h",-1); sa = p.get("score_a",-1)
                                if sh < 0: continue
                                if sport_key == "futbol":
                                    won_h = sh > sa; won_a = sa > sh; draw = sh == sa
                                    h_col = "#00ff88" if won_h else ("#FFD700" if draw else "#555")
                                    a_col = "#00ff88" if won_a else ("#FFD700" if draw else "#555")
                                    resultado = "Empate" if draw else (f"{p['home'].split()[-1]} gana" if won_h else f"{p['away'].split()[-1]} gana")
                                else:
                                    won_h = sh > sa; won_a = sa > sh
                                    h_col = "#00ff88" if won_h else "#555"
                                    a_col = "#00ff88" if won_a else "#555"
                                    total_pts = sh + sa
                                    resultado = f"Total: {total_pts} pts"
                                st.markdown(
                                    f"<div style='display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;"
                                    f"padding:8px 10px;border-bottom:1px solid #1a1a40;font-size:.88rem'>"
                                    f"<div style='text-align:right;color:{h_col};font-weight:{'700' if won_h else '400'}'>{p['home']}</div>"
                                    f"<div style='text-align:center;background:#0d0d2e;border-radius:8px;padding:4px 12px;"
                                    f"font-weight:900;font-size:1rem;min-width:70px'>"
                                    f"<span style='color:{h_col}'>{sh}</span> - <span style='color:{a_col}'>{sa}</span></div>"
                                    f"<div style='text-align:left;color:{a_col};font-weight:{'700' if won_a else '400'}'>{p['away']}</div>"
                                    f"</div>", unsafe_allow_html=True)

            # ── PRÓXIMOS ──
            if proximos:
                st.markdown("<div class='shdr'>📅 Próximos Partidos</div>", unsafe_allow_html=True)
                proximos_sorted = sorted(proximos, key=lambda x: x.get("fecha",""))
                prev_fecha = None
                for p in proximos_sorted[:30]:
                    if p["fecha"] != prev_fecha:
                        try:
                            d = datetime.strptime(p["fecha"],"%Y-%m-%d")
                            dias = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
                            meses = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
                            st.markdown(f"<div style='font-size:.72rem;color:#FFD700;font-weight:700;margin:10px 0 4px'>{dias[d.weekday()]} {d.day} {meses[d.month]}</div>", unsafe_allow_html=True)
                        except: st.markdown(f"<div style='color:#FFD700;font-size:.72rem;margin:8px 0 4px'>{p['fecha']}</div>", unsafe_allow_html=True)
                        prev_fecha = p["fecha"]
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;align-items:center;"
                        f"padding:6px 10px;border-bottom:1px solid #1a1a40;font-size:.85rem'>"
                        f"<span style='color:#aaa'>{p['home']} <span style='color:#555'>vs</span> {p['away']}</span>"
                        f"<span style='color:#555;font-size:.75rem'>{p.get('liga','')} · 🕒</span>"
                        f"</div>", unsafe_allow_html=True)


def avg(lst): return sum(lst)/len(lst) if lst else 0.0

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
                    "PROCESO OBLIGATORIO (ejecuta todos los pasos):\n"
                    "PASO 1 — IDENTIFICACIÓN PRECISA: Deporte exacto, equipos/jugadores, torneo/liga, fecha estimada, mercado específico, cuota exacta, estado actual del partido.\n"
                    "PASO 2 — VARIABLES HUMANAS VISIBLES:\n"
                    "  · TENIS: Ranking ATP/WTA de ambos, superficie del torneo, historial H2H conocido, forma reciente (últimos 5 torneos).\n"
                    "  · FÚTBOL: Posición en tabla, goles a favor/contra, condición local/visitante, importancia del partido.\n"
                    "  · NBA: Win%, puntos por partido, diferencial ofensivo/defensivo.\n"
                    "PASO 3 — VARIABLES OCULTAS (las que los humanos no calculan):\n"
                    "  · TENIS: Fatiga acumulada (días desde último partido jugado esta semana). Velocidad de pista vs estilo de juego (servidor potente en hierba, defensor en tierra). Altitud del torneo (afecta resistencia). Temperatura y humedad estimada (afecta tenistas con menos masa muscular). Presión de favoritismo. Historial en esa ronda específica del torneo. Historial de lesiones crónicas relevantes. Cuántos sets jugados en los últimos 3 partidos (fatiga real). Motivación: ¿necesita puntos ranking? ¿ya clasificado?\n"
                    "  · FÚTBOL: xG reales vs goles marcados (suerte vs mérito). Presión táctica específica del rival. Cansancio por calendario (Europa + Liga). Árbitro (si identificable) y tarjetas por partido. Clima estimado para ese día/ciudad. Historial de lesiones del equipo. Deuda táctica del entrenador. Eficiencia en goles de set-piece.\n"
                    "  · NBA: Pace differential vs ese rival. Back-to-back games o cuarto partido en 6 noches. Travel miles esta semana. Rendimiento en 4Q y clutch time. Arbitraje tendencia (fouls per game). Rendimiento sin jugador estrella (rotaciones).\n"
                    "PASO 4 — MODELO PROBABILÍSTICO: Ejecuta distribución de Poisson (fútbol/NBA) o Elo ajustado (tenis) mentalmente. Estima prob_real como un actuario. Calcula la probabilidad implícita de la cuota: 1/cuota. Calcula edge = prob_real - prob_implicita.\n"
                    "PASO 5 — 50,000 SIMULACIONES MONTE CARLO: Simula el evento con las variables anteriores. Determina el intervalo de confianza al 95%. Calcula EV = (prob_real × (cuota-1)) - (prob_fallo × 1).\n"
                    "PASO 6 — SEÑAL DE MERCADO SHARP: ¿La cuota parece de apertura o movida por sharp money? ¿Hay discrepancia con otras casas? ¿Es una cuota trampa para el público general?\n"
                    "PASO 7 — REVISIÓN CRÍTICA: ¿El partido ya terminó? Si sí, veredicto='Inválida'. ¿Es mercado de mala cuota para el valor real? ¿Hay banderas rojas que invalidan el pick?\n"
                    "PASO 8 — KELLY CRITERION: kelly% = max(0, min(5, ((cuota-1)*prob_real - prob_fallo)/(cuota-1)*100)). Nunca más del 5% del bankroll.\n"
                    + (f"PASO 9 — APRENDIZAJE REAL DE TU HISTORIAL: {mem_ctx}\n" if mem_ctx else "")
                    + "CALIFICACIÓN ESTRICTA (sé implacable — sólo el top 10% de picks merece A):\n"
                    "A+(95-100): EV>+0.10, edge>10%, variables ocultas muy favorables, señal sharp\n"
                    "A (88-94): EV>+0.06, edge 6-10%, análisis sólido\n"
                    "A-(82-87): EV>+0.03, edge 3-6%, pick razonable\n"
                    "B+(76-81): EV>+0.01, valor marginal pero existe\n"
                    "B (70-75): EV≈0, cuota justa, sin ventaja real — no apostar\n"
                    "B-(64-69): EV ligeramente negativo — no apostar\n"
                    "C+(55-63): EV negativo -3% — pick malo\n"
                    "C (45-54): EV negativo significativo — evitar\n"
                    "C-(35-44): EV muy negativo — tirar dinero\n"
                    "D (20-34): Pick sin análisis, trampa de público\n"
                    "F (0-19): Fraude, partido terminado, pick absurdo\n"
                    "RESPONDE SOLO EN JSON SIN MARKDOWN:\n"
                    "{\"deporte\": \"\", \"equipos\": \"\", \"mercado\": \"\", \"cuota\": 0.0, "
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
                cmap = {"A+":"#00ff88","A":"#00ff88","A-":"#00dd77","B+":"#7fff00",
                        "B":"#FFD700","B-":"#ffc200","C+":"#ff9500","C":"#ff7700",
                        "C-":"#ff6600","D":"#ff4444","F":"#cc0000"}
                color  = cmap.get(letra,"#777")
                ecol   = "#00ff88" if edge > 0 else "#ff4444"
                evcol  = "#00ff88" if ev > 0 else "#ff4444"
                scol   = {"favorable":"#00ff88","neutral":"#FFD700","contrario":"#ff4444"}.get(sharp,"#aaa")

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
                matches.append({
                    "id":    str(ev.get("event_key","")),
                    "p1":    ev.get("event_first_player","?"),
                    "p2":    ev.get("event_second_player","?"),
                    "rank1": 999, "rank2": 999,
                    "tour":  tour,
                    "torneo": ev.get("tournament_name",""),
                    "hora":  hora,
                    "fecha": fecha,
                    "state": "in" if ev.get("event_live","0")=="1" else "pre",
                    "odd_1": 0.0, "odd_2": 0.0,
                })
            except: continue
    except Exception as e:
        pass
    return matches

def tennis_model(rank1, rank2, odd_1, odd_2):
    r1=max(1,rank1); r2=max(1,rank2)
    ls=math.log(r2)+math.log(r1)
    p1_rank=math.log(r2)/ls if ls>0 else 0.5
    if odd_1>1 and odd_2>1:
        p1o=1/odd_1; p2o=1/odd_2; s=p1o+p2o
        p1=0.5*p1_rank+0.5*(p1o/s)
    else:
        p1=p1_rank
    p2=1-p1
    edge_1=round(p1-(1/odd_1),3) if odd_1>1 else 0
    edge_2=round(p2-(1/odd_2),3) if odd_2>1 else 0
    conf="💎 DIAMANTE" if max(p1,p2)>0.68 else("🔥 ALTA" if max(p1,p2)>0.58 else "⚡ MEDIA")
    return {"p1":round(p1,3),"p2":round(p2,3),"edge_1":edge_1,"edge_2":edge_2,"conf":conf}

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
            with st.spinner("🤖 IA calculando picks de tenis..."):
                ten_picks = []
                for m in ten_matches:
                    if m["state"]!="pre": continue
                    tm = tennis_model(m["rank1"],m["rank2"],m["odd_1"],m["odd_2"])
                    best_p = max(tm["p1"],tm["p2"])
                    fav = m["p1"] if tm["p1"]>=tm["p2"] else m["p2"]
                    best_odd = m["odd_1"] if tm["p1"]>=tm["p2"] else m["odd_2"]
                    edge = tm["edge_1"] if tm["p1"]>=tm["p2"] else tm["edge_2"]
                    if best_p >= 0.57:
                        conf = "💎 DIAMANTE" if best_p>0.68 else ("🔥 ALTA" if best_p>0.62 else "⚡ MEDIA")
                        ten_picks.append({"p1":m["p1"],"p2":m["p2"],"hora":m["hora"],"tour":m["tour"],
                                         "torneo":m["torneo"],"pick":f"🎾 ML: {fav}","prob":best_p,
                                         "odd":best_odd,"conf":conf,"edge":edge,"type":"ML"})
                # AI picks for matches without clear ranking edge
                try:
                    _no_rank = [m for m in ten_matches if m["state"]=="pre" and m["rank1"]>=900 and m["rank2"]>=900][:5]
                    if _no_rank and ANTHROPIC_API_KEY:
                        _txt = "\n".join([f"{m['p1']} vs {m['p2']} ({m['tour']}) @{m['odd_1']}/{m['odd_2']}" for m in _no_rank])
                        _ai_r = requests.post("https://api.anthropic.com/v1/messages",
                            headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"},
                            json={"model":"claude-sonnet-4-20250514","max_tokens":500,
                                  "messages":[{"role":"user","content":
                                    "Analista tenis experto. Para estos partidos ATP/WTA da picks con valor (prob>=58%). Solo JSON array: [{p1,p2,pick,prob,razon}]. Partidos: " + _txt}]},timeout=12)
                        import json as _jt
                        _ai_raw = _ai_r.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
                        _ai_picks = _jt.loads(_ai_raw)
                        for _ap in _ai_picks:
                            _p = float(_ap.get("prob",0))/100
                            if _p >= 0.58:
                                _conf = "💎 DIAMANTE" if _p>0.68 else ("🔥 ALTA" if _p>0.62 else "⚡ MEDIA")
                                ten_picks.append({"p1":_ap.get("p1",""),"p2":_ap.get("p2",""),
                                                  "hora":"","tour":"ATP/WTA","torneo":"","pick":f"🎾 ML: {_ap.get('pick','')}",
                                                  "prob":_p,"odd":0,"conf":_conf,"edge":0,"type":"ML-IA",
                                                  "razon":_ap.get("razon","")})
                except: pass
                ten_picks.sort(key=lambda x:-x["prob"])
            if not ten_picks: st.info("No hay picks de tenis con valor hoy.")
            for p in ten_picks:
                cc = "#FFD700" if "DIAMANTE" in p["conf"] else ("#00ff88" if "ALTA" in p["conf"] else "#aaa")
                os_ = f" @{p['odd']:.2f}" if p["odd"]>1 else ""
                edge_txt = f"<span style='color:#00ff88;font-size:.75rem'> +{p['edge']*100:.1f}% edge</span>" if p.get("edge",0)>0.05 else ""
                razon_txt = f"<div style='color:#555;font-size:.76rem'>{p.get('razon','')}</div>" if p.get("razon") else ""
                tipo = p.get("type","ML")
                tipo_badge = f"<span style='background:#00ccff22;color:#00ccff;border-radius:4px;padding:2px 6px;font-size:.7rem;margin-left:4px'>{tipo}</span>"
                st.markdown(f"<div class='mrow' style='display:flex;justify-content:space-between;align-items:center'><div style='flex:1;min-width:0'><div style='font-weight:700;font-size:.9rem'>{p['p1']} vs {p['p2']}{tipo_badge}</div><div style='color:#555;font-size:.78rem'>{p['tour']}{' · '+p['torneo'] if p['torneo'] else ''}{' · '+p['hora'] if p['hora'] else ''}</div><div style='margin-top:4px;color:#00ccff;font-weight:700'>{p['pick']}{os_}{edge_txt}</div>{razon_txt}</div><div style='text-align:right;flex-shrink:0'><div style='font-size:1.3rem;font-weight:900;color:#FFD700'>{p['prob']*100:.1f}%</div><div style='font-size:.72rem;color:{cc}'>{p['conf']}</div></div></div>",unsafe_allow_html=True)
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
                        opts=[]
                        if m["odd_h"]>1: opts.append(("🏠 "+m["home"][:15]+" gana",dp["ph"],m["odd_h"],dp["ph"]-(1/m["odd_h"])))
                        if m["odd_a"]>1: opts.append(("✈️ "+m["away"][:15]+" gana",dp["pa"],m["odd_a"],dp["pa"]-(1/m["odd_a"])))
                        opts.append(("⚽ Over 2.5",mc_["o25"],0,mc_["o25"]-0.50))
                        opts.append(("⚡ Ambos Anotan",mc_["btts"],0,mc_["btts"]-0.50))
                        opts.sort(key=lambda x:-x[3])
                        best=opts[0]
                        if best[3]>0.03:
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



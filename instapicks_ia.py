import os
import ast
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

# ------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ------------------------------------------------------------------
st.set_page_config(
    page_title="InstaPicks·IA — Casa de apuestas con predicción por IA",
        layout="wide",
)

# ------------------------------------------------------------------
# ESTILOS — InstaPicks·IA (tema oscuro con acentos teal)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root{
    --bg:#0B0E13; --panel:#161B23; --panel2:#1D2430; --line:#2A303C;
    --gold:#E3A857; --teal:#2FE0B8; --teal-dim:#1E7566; --muted:#8B93A3; --muted2:#5C6373;
}

.stApp{
    background:
        radial-gradient(circle at 8% 0%, rgba(47,224,184,0.07) 0%, transparent 40%),
        radial-gradient(circle at 100% 20%, rgba(227,168,87,0.05) 0%, transparent 35%),
        var(--bg);
    color:#EDEFF3;
}
h1,h2,h3,h4{ font-family:'Sora', sans-serif; letter-spacing:0.01em; }
p, span, div, label{ font-family:'Inter', sans-serif; }

/* ---------- MARCA ---------- */
.brand-wrap{ display:flex; align-items:center; gap:10px; margin-bottom:2px; }
.brand-mark{
    width:34px; height:34px; border-radius:9px; flex-shrink:0;
    background:linear-gradient(135deg, var(--teal) 0%, #17998A 100%);
    display:flex; align-items:center; justify-content:center;
    font-size:13px; font-weight:800; font-family:'Sora', sans-serif; color:#08110E;
    box-shadow:0 0 18px rgba(47,224,184,0.35); letter-spacing:0.02em;
}
.brand{ font-size:26px; font-weight:800; font-family:'Sora', sans-serif; }
.brand span{
    background:linear-gradient(90deg, var(--teal), #7CF0D8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.brand-tagline{
    font-size:11px; color:var(--muted2); letter-spacing:0.14em; text-transform:uppercase;
    margin-left:44px; margin-top:-4px;
}
.accent-rule{
    height:2px; width:100%; margin:10px 0 16px 0; border-radius:2px;
    background:linear-gradient(90deg, var(--teal) 0%, rgba(47,224,184,0.15) 45%, transparent 80%);
}

/* ---------- DISCLAIMER ---------- */
.disclaimer{
    background:var(--panel2); border:1px solid var(--line); border-left:3px solid var(--teal);
    border-radius:8px; padding:9px 16px; font-size:12px; color:var(--muted);
    text-align:center; margin-bottom:16px;
}
.disclaimer b{ color:var(--teal); }

/* ---------- TARJETAS DE PARTIDO ---------- */
.match-card{
    position:relative; background:var(--panel); border:1px solid var(--line);
    border-radius:12px; padding:14px 18px 14px 20px; margin-bottom:12px;
    box-shadow:0 2px 10px rgba(0,0,0,0.18);
    transition:border-color .15s ease, transform .15s ease, box-shadow .15s ease;
    overflow:hidden;
}
.match-card::before{
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:linear-gradient(180deg, var(--teal), var(--teal-dim));
}
.match-card:hover{
    border-color:#3A4356; transform:translateY(-1px);
    box-shadow:0 6px 18px rgba(47,224,184,0.08);
}
.comp-tag{
    font-size:11px; color:var(--teal); text-transform:uppercase; letter-spacing:0.1em; font-weight:600;
}
.team-line{ font-size:16.5px; font-weight:700; margin:4px 0 2px 0; font-family:'Sora', sans-serif; }
.match-meta{ font-size:12px; color:var(--muted2); margin-bottom:8px; }
.ai-pill{
    display:inline-block; font-family:'IBM Plex Mono', monospace; font-size:11px; color:#0B0E13;
    background:linear-gradient(90deg, var(--teal), #7CF0D8); font-weight:600;
    padding:2px 9px; border-radius:20px; margin-left:8px;
}
.pending-note{ font-size:12px; color:var(--muted2); font-style:italic; }

/* ---------- BOLETO ---------- */
.slip-item{
    background:var(--panel2); border:1px solid var(--line); border-radius:8px;
    padding:9px 12px; margin-bottom:7px; font-size:13px;
    border-left:2px solid var(--gold);
}
.slip-total{
    font-size:15px; font-weight:700; color:var(--gold);
    border-top:1px dashed var(--line); padding-top:10px; margin-top:8px;
}

/* ---------- CAJA DE ANÁLISIS IA ---------- */
.ia-box{
    background:linear-gradient(180deg, var(--panel), var(--panel2));
    border:1px solid var(--line); border-top:2px solid var(--teal);
    border-radius:12px; padding:20px 24px; margin-top:14px;
    box-shadow:0 4px 20px rgba(0,0,0,0.25);
}

/* ---------- BOTONES ---------- */
div.stButton > button{
    background:var(--panel2); border:1px solid var(--line); color:#EDEFF3;
    border-radius:8px; font-family:'IBM Plex Mono', monospace; font-weight:600; width:100%;
    transition:all .15s ease;
}
div.stButton > button:hover{
    border-color:var(--teal); color:var(--teal);
    box-shadow:0 0 0 1px var(--teal), 0 0 14px rgba(47,224,184,0.25);
}
div.stButton > button[kind="primary"]{
    background:linear-gradient(90deg, var(--teal), #17998A);
    color:#08110E; border:none; font-family:'Sora', sans-serif; font-weight:700;
}
div.stButton > button[kind="primary"]:hover{
    box-shadow:0 0 16px rgba(47,224,184,0.45); filter:brightness(1.08);
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"]{
    color:var(--muted); font-weight:600; border-radius:8px 8px 0 0;
}
.stTabs [aria-selected="true"]{
    color:var(--teal) !important; border-bottom:2px solid var(--teal) !important;
}

/* ---------- INPUTS ---------- */
div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input{
    background:var(--panel2) !important; border:1px solid var(--line) !important;
    border-radius:8px !important;
}
div[data-baseweb="select"] > div:focus-within, .stTextInput input:focus{
    border-color:var(--teal) !important; box-shadow:0 0 0 1px var(--teal) !important;
}

/* ---------- POPOVER LOGIN ---------- */
div[data-testid="stPopover"] button{
    border:1px solid var(--teal-dim) !important; color:var(--teal) !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# ESTADO DE SESIÓN
# ------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.balance = 50000.0
    st.session_state.betslip = {}   # {match_id: {"match": str, "pick": str, "odd": float}}

# ------------------------------------------------------------------
# DATOS REALES DE PARTIDOS (al 12 de julio de 2026)
# ------------------------------------------------------------------
COMPETITIONS = {
    "Mundial 2026": {
        "sub": "Semifinales confirmadas — AT&T Stadium / Mercedes-Benz Stadium",
        "liga_nombre": "FIFA World Cup",
        "matches": [
            {
                "id": "wc1", "home": "Francia", "away": "España",
                "meta": "Semifinal · Mar 14 Jul · AT&T Stadium, Dallas · 16:00 (ARG)",
                "odds": {"Francia": 2.50, "Empate": 3.20, "España": 2.70},
                "probs": {"Francia": 37, "Empate": 26, "España": 37},
                "conf": 69,
            },
            {
                "id": "wc2", "home": "Argentina", "away": "Inglaterra",
                "meta": "Semifinal · Mié 15 Jul · Mercedes-Benz Stadium, Atlanta · 16:00 (ARG)",
                "odds": {"Argentina": 2.05, "Empate": 3.30, "Inglaterra": 3.60},
                "probs": {"Argentina": 43, "Empate": 25, "Inglaterra": 32},
                "conf": 72,
            },
            {
                "id": "wc3", "home": "Perdedor Semi 1", "away": "Perdedor Semi 2",
                "meta": "Tercer puesto · Sáb 18 Jul · Hard Rock Stadium, Miami",
                "odds": None,
                "pending": "Cuotas disponibles tras las semifinales",
            },
            {
                "id": "wc4", "home": "Ganador Semi 1", "away": "Ganador Semi 2",
                "meta": "Gran Final · Dom 19 Jul · MetLife Stadium, Nueva Jersey",
                "odds": None,
                "pending": "Cuotas disponibles tras las semifinales",
            },
        ],
    },
    "Premier League": {
        "sub": "Pretemporada 2026/27 — amistosos internacionales de preparación",
        "liga_nombre": "Premier League",
        "matches": [
            {"id": "pl1", "home": "Manchester United", "away": "Wrexham",
             "meta": "Amistoso · Sáb 18 Jul · Helsinki",
             "odds": {"Manchester United": 1.28, "Empate": 5.20, "Wrexham": 9.00},
             "probs": {"Manchester United": 74, "Empate": 17, "Wrexham": 9}, "conf": 70},
            {"id": "pl2", "home": "Liverpool", "away": "Sunderland",
             "meta": "Amistoso · Sáb 25 Jul · Nashville",
             "odds": {"Liverpool": 1.40, "Empate": 4.60, "Sunderland": 7.20},
             "probs": {"Liverpool": 68, "Empate": 20, "Sunderland": 12}, "conf": 65},
            {"id": "pl3", "home": "Aston Villa", "away": "Real Sociedad",
             "meta": "Amistoso · Sáb 25 Jul · Walsall",
             "odds": {"Aston Villa": 2.10, "Empate": 3.30, "Real Sociedad": 3.30},
             "probs": {"Aston Villa": 42, "Empate": 28, "Real Sociedad": 30}, "conf": 55},
            {"id": "pl4", "home": "Chelsea", "away": "Tottenham",
             "meta": "Amistoso · Sáb 1 Ago · Sídney",
             "odds": {"Chelsea": 2.30, "Empate": 3.30, "Tottenham": 2.95},
             "probs": {"Chelsea": 38, "Empate": 27, "Tottenham": 35}, "conf": 52},
            {"id": "pl5", "home": "Manchester City", "away": "Inter de Milán",
             "meta": "Amistoso · Sáb 1 Ago · Hong Kong",
             "odds": {"Manchester City": 1.90, "Empate": 3.60, "Inter de Milán": 3.80},
             "probs": {"Manchester City": 46, "Empate": 25, "Inter de Milán": 29}, "conf": 60},
            {"id": "pl6", "home": "Arsenal", "away": "Real Betis",
             "meta": "Amistoso · Mié 5 Ago · Dublín",
             "odds": {"Arsenal": 1.75, "Empate": 3.70, "Real Betis": 4.20},
             "probs": {"Arsenal": 50, "Empate": 25, "Real Betis": 25}, "conf": 63},
        ],
    },
    "Champions League": {
        "sub": "UEFA 2026/27 — 2ª ronda de clasificación (ida 21/22 jul, vuelta 28/29 jul)",
        "liga_nombre": "UEFA Champions League",
        "matches": [
            {"id": "cl1", "home": "Fenerbahçe", "away": "Górnik Zabrze",
             "meta": "Clasificación · Mar 21 Jul · Estambul",
             "odds": {"Fenerbahçe": 1.35, "Empate": 4.70, "Górnik Zabrze": 7.80},
             "probs": {"Fenerbahçe": 68, "Empate": 20, "Górnik Zabrze": 12}, "conf": 68},
            {"id": "cl2", "home": "Sturm Graz", "away": "Heart of Midlothian",
             "meta": "Clasificación · Mar 21 Jul · Graz",
             "odds": {"Sturm Graz": 1.65, "Empate": 3.90, "Heart of Midlothian": 4.90},
             "probs": {"Sturm Graz": 54, "Empate": 24, "Heart of Midlothian": 22}, "conf": 58},
            {"id": "cl3", "home": "Dinamo Zagreb", "away": "Por definir",
             "meta": "Clasificación · Mié 22 Jul · Zagreb",
             "odds": None,
             "pending": "Rival saldrá del cruce de primera ronda"},
        ],
    },
    "NBA y ATP": {
        "sub": "Pretemporada NBA y gira de verano ATP",
        "liga_nombre": None,  # no es fútbol, no aplica al analista IA
        "matches": [
            {"id": "nba1", "home": "Boston Celtics", "away": "Milwaukee Bucks",
             "meta": "Pretemporada · Vie 17 Jul · 21:00",
             "odds": {"Boston Celtics": 1.55, "Milwaukee Bucks": 2.45},
             "probs": {"Boston Celtics": 64, "Milwaukee Bucks": 36}, "conf": 76},
            {"id": "nba2", "home": "LA Lakers", "away": "Denver Nuggets",
             "meta": "Pretemporada · Vie 17 Jul · 23:30",
             "odds": {"LA Lakers": 2.10, "Denver Nuggets": 1.72},
             "probs": {"LA Lakers": 45, "Denver Nuggets": 55}, "conf": 69},
            {"id": "atp1", "home": "C. Alcaraz", "away": "J. Sinner",
             "meta": "Gira de verano ATP · Lun 20 Jul · 08:00",
             "odds": {"C. Alcaraz": 1.62, "J. Sinner": 2.30},
             "probs": {"C. Alcaraz": 60, "J. Sinner": 40}, "conf": 74},
            {"id": "atp2", "home": "N. Djokovic", "away": "A. Zverev",
             "meta": "Gira de verano ATP · Lun 20 Jul · 10:30",
             "odds": {"N. Djokovic": 1.78, "A. Zverev": 2.05},
             "probs": {"N. Djokovic": 55, "A. Zverev": 45}, "conf": 66},
        ],
    },
}

COLORS = ["#E3A857", "#5C6373", "#33C2A8"]  # local, empate, visita

# ------------------------------------------------------------------
# MÓDULO DE ANÁLISIS IA (adaptado del app.py original, con Groq)
# ------------------------------------------------------------------
MAPA_LIGAS = {
    'WC': 'FIFA World Cup', 'CL': 'UEFA Champions League', 'BL1': 'Bundesliga',
    'DED': 'Eredivisie', 'BSA': 'Campeonato Brasileiro Série A', 'PD': 'Primera Division',
    'FL1': 'Ligue 1', 'ELC': 'Championship', 'PPL': 'Primeira Liga',
    'EC': 'European Championship', 'SA': 'Serie A', 'PL': 'Premier League',
}


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza el dataset crudo: extrae nombres de equipo y traduce el código de liga."""
    def extraer_nombre(val):
        try:
            if isinstance(val, str):
                return ast.literal_eval(val).get('name', val).strip()
            return str(val)
        except Exception:
            return str(val)

    df['home_name'] = df['homeTeam'].apply(extraer_nombre)
    df['away_name'] = df['awayTeam'].apply(extraer_nombre)
    df['liga_nombre'] = df['liga'].map(MAPA_LIGAS).fillna(df['liga'])
    df = df.dropna(subset=['home_name', 'away_name'])
    return df


@st.cache_data
def cargar_dataset_real(path: str = "master_dataset_final.csv"):
    """Intenta cargar el dataset histórico real. Devuelve (df, encontrado: bool)."""
    if not os.path.exists(path):
        return None, False
    try:
        df = pd.read_csv(path)
        return limpiar_datos(df), True
    except Exception:
        return None, False


def construir_dataset_demo():
    """
    Fallback si no existe master_dataset_final.csv: arma un dataset mínimo
    a partir de los partidos reales ya cargados en la casa de apuestas,
    para que el selector de ligas/equipos funcione igual mientras
    se sube el dataset histórico completo.
    """
    filas = []
    for comp in COMPETITIONS.values():
        liga = comp.get("liga_nombre")
        if not liga:
            continue
        for m in comp["matches"]:
            if m["home"].startswith(("Ganador", "Perdedor")) or m["away"] in ("Por definir",):
                continue
            filas.append({"home_name": m["home"], "away_name": m["away"], "liga_nombre": liga})
    return pd.DataFrame(filas)


@st.cache_resource
def obtener_cliente_groq():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or Groq is None:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


def obtener_analisis_ia(client, equipo_a: str, equipo_b: str, liga: str) -> str:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # Modelo muy rápido
        messages=[{"role": "user", "content": f"""
    Actúa como un Senior Sports Data Analyst especializado en apuestas deportivas.

    TOMA NOTA: No hagas un resumen de partidos pasados. Tu trabajo es realizar una PROYECCIÓN PROBABILÍSTICA del próximo encuentro.

    Contexto del encuentro:
    - Partido: {equipo_a} (Local) vs {equipo_b} (Visitante)
    - Competición: {liga}
    Eres un analista profesional de apuestas deportivas especializado en fútbol.

Tu objetivo NO es adivinar resultados, sino encontrar apuestas con valor esperado positivo (EV+).

Nunca analices un partido únicamente por el nombre de los equipos.

Siempre analiza utilizando la siguiente metodología.

==============================
FASE 1
ANÁLISIS GENERAL
==============================

Analiza:

• últimos 30 partidos
• últimos 5 partidos
• calidad de rivales
• rendimiento como local y visitante
• goles anotados
• goles recibidos
• xG
• xGA
• remates
• remates a puerta
• posesión
• precisión de pase
• córners
• faltas
• tarjetas
• saques de banda
• offsides
• recuperación de balón
• pérdidas
• eficacia ofensiva
• eficacia defensiva
• conversión de ocasiones
• goles por remate
• goles por remate a puerta
• balón parado
• penales
• transiciones
• contraataques
• presión alta
• bloque bajo
• ritmo del partido
• entrenador
• sustituciones
• profundidad del banquillo
• lesiones
• suspendidos
• fatiga
• calendario
• clima
• estadio
• importancia del partido
• motivación
• historial H2H

==============================
FASE 2
INDICES
==============================

Construye una tabla.

Forma últimos 5
Forma últimos 30
Ataque
Defensa
xG
Eficacia
Balón parado
Contraataque
Presión
Banquillo
Momento psicológico
Calidad rivales
Disciplina

Califica cada uno de 0 a 100.

Calcula un índice global.

==============================
FASE 3
SIMULACIÓN
==============================

Simula al menos 5000 partidos.

Entrega:

Probabilidad de victoria

Empate

Derrota

Probabilidad de clasificación

Probabilidad de:

Más de 0.5
Más de 1.5
Más de 2.5
Más de 3.5
Ambos anotan

Marcadores más probables.

==============================
FASE 4
RITMO
==============================

Predice

posesión

remates

remates a puerta

córners

faltas

tarjetas

saques de banda

offsides

por cada equipo.

==============================
FASE 5
MERCADOS
==============================

Analiza TODOS los mercados disponibles normalmente en Codere.

Ganador

Empate

Doble oportunidad

Clasifica

Hándicap

Over Under goles

Ambos anotan

Córners

Tarjetas

Faltas

Saques de banda

Remates

Remates a puerta

Remates fuera

Remates bloqueados

Faltas por jugador

Tarjetas por jugador

Remates por jugador

Remates a puerta por jugador

Entradas por jugador

Asistencias

Goleadores

Crear Apuesta

Primer tiempo

Segundo tiempo

Próximo gol

Equipo marca primero

Equipo marca último

Cada mercado debe tener

Confianza

de 0 a 100

y

Valor

Excelente

Bueno

Regular

Malo

==============================
FASE 6
JUGADORES
==============================

Analiza TODOS los jugadores titulares.

Predice

faltas

tarjetas

remates

remates a puerta

entradas

saques de banda

duelos ganados

intercepciones

recuperaciones

pases

centros

disparos bloqueados

regates

goles

asistencias

Para cada jugador indica una confianza.

==============================
FASE 7
VALOR DE LA CUOTA
==============================

Nunca recomiendes una apuesta solo porque sea probable.

Compara siempre

Probabilidad real

vs

Cuota implícita.

Explica si existe valor esperado positivo (EV+).

==============================
FASE 8
TOP PICKS
==============================

Entrega

TOP 10 apuestas.

Cada una con

Confianza

Valor

Riesgo

Análisis corto

Análisis largo

==============================
FASE 9
APUESTA SEGURA
==============================

Entrega

🥇 Pick Premium

🥈 Súper Segura

🥉 Apuesta de Valor

🔥 Combinada

==============================
FASE 10
SEMÁFORO
==============================

🟢 Excelente

🟡 Aceptable

🔴 Evitar

==============================
FASE 11
ANÁLISIS EN VIVO
==============================

Si el partido ya empezó

analiza

posesión

ritmo

xG

dominador

presión

fatiga

cambios

lesiones

tarjetas

faltas

momentum

y adapta todas las apuestas.

==============================
FASE 12
POST PARTIDO
==============================

Cuando termine el partido

compara

tu predicción

contra

lo ocurrido.

Indica

qué acertaste

qué fallaste

por qué

cómo mejorar el modelo.

Nunca inventes estadísticas. Si un dato específico no está disponible, indícalo claramente y basa el análisis en información verificable y tendencias recientes. Diferencia siempre entre hechos, estimaciones y predicciones.

    Si no tienes los datos de las alineaciones de hoy, asume una base estadística basada en el rendimiento de los últimos 5 partidos de cada equipo. Usa un tono analítico, basado en datos, sin ser un bot genérico.
    """}],
    )
    return completion.choices[0].message.content


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
col_brand, col_auth = st.columns([3, 2])
with col_brand:
    st.markdown(
        '<div class="brand-wrap">'
        '<div class="brand-mark">IP</div>'
        '<div class="brand">Insta<span>Picks</span>·IA</div>'
        '</div>'
        '<div class="brand-tagline">Predicciones deportivas con inteligencia artificial</div>',
        unsafe_allow_html=True,
    )

with col_auth:
    if st.session_state.logged_in:
        c1, c2 = st.columns([3, 1])
        c1.markdown(
            f"👤 **{st.session_state.user_name}** · Saldo demo: "
            f"`${st.session_state.balance:,.0f}`"
        )
        if c2.button("Salir"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()
    else:
        with st.popover("Iniciar sesión / Crear cuenta", use_container_width=True):
            tab_login, tab_register = st.tabs(["Iniciar sesión", "Crear cuenta"])

            with tab_login:
                email = st.text_input("Correo electrónico", key="login_email")
                pw = st.text_input("Contraseña", type="password", key="login_pw")
                if st.button("Ingresar", key="login_btn"):
                    if email:
                        st.session_state.logged_in = True
                        st.session_state.user_name = email.split("@")[0].replace(".", " ").title()
                        st.rerun()
                    else:
                        st.warning("Ingresá tu correo para continuar (modo demo).")

            with tab_register:
                name = st.text_input("Nombre completo", key="reg_name")
                email_r = st.text_input("Correo electrónico", key="reg_email")
                pw_r = st.text_input("Contraseña (mín. 8 caracteres)", type="password", key="reg_pw")
                if st.button("Crear cuenta", key="reg_btn"):
                    if name and email_r and len(pw_r) >= 8:
                        st.session_state.logged_in = True
                        st.session_state.user_name = name
                        st.rerun()
                    else:
                        st.warning("Completá nombre, correo y una contraseña de al menos 8 caracteres.")

st.markdown('<div class="accent-rule"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="disclaimer">Proyecto académico — Inteligencia Artificial, Universidad Tecnológica '
    '&nbsp;|&nbsp; <b>No involucra dinero real.</b> Los partidos y fechas son reales, '
    'las cuentas, cuotas y análisis se generan con fines educativos.</div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# LAYOUT PRINCIPAL: partidos (izquierda) + boleto (derecha)
# ------------------------------------------------------------------
col_main, col_slip = st.columns([2.4, 1])

with col_main:
    tab_names = list(COMPETITIONS.keys()) + ["Análisis IA"]
    tabs = st.tabs(tab_names)

    # --- pestañas de competiciones (idénticas a la versión anterior) ---
    for tab, (comp_name, comp_data) in zip(tabs[:-1], COMPETITIONS.items()):
        with tab:
            st.caption(comp_data["sub"])

            for m in comp_data["matches"]:
                st.markdown('<div class="match-card">', unsafe_allow_html=True)

                st.markdown(f'<div class="comp-tag">{m["meta"]}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="team-line">{m["home"]} <span style="color:var(--muted2);">vs</span> '
                    f'{m["away"]}'
                    + (f'<span class="ai-pill">IA {m["conf"]}%</span>' if m.get("conf") else '')
                    + '</div>',
                    unsafe_allow_html=True,
                )

                if m["odds"] is None:
                    st.markdown(f'<div class="pending-note">{m["pending"]}</div>', unsafe_allow_html=True)
                else:
                    probs = m["probs"]
                    bar_html = '<div style="display:flex;height:8px;border-radius:4px;overflow:hidden;margin:6px 0;">'
                    for i, (label, p) in enumerate(probs.items()):
                        bar_html += f'<div style="width:{p}%;background:{COLORS[i % 3]};"></div>'
                    bar_html += '</div>'
                    legend = " · ".join(f"{k} {v}%" for k, v in probs.items())
                    st.markdown(bar_html, unsafe_allow_html=True)
                    st.caption(legend)

                    cols = st.columns(len(m["odds"]))
                    for i, (pick, odd) in enumerate(m["odds"].items()):
                        key = f'{m["id"]}_{pick}'
                        selected = st.session_state.betslip.get(m["id"], {}).get("pick") == pick
                        label = f'{"» " if selected else ""}{pick}\n{odd:.2f}'
                        if cols[i].button(label, key=key):
                            if selected:
                                st.session_state.betslip.pop(m["id"], None)
                            else:
                                st.session_state.betslip[m["id"]] = {
                                    "match": f'{m["home"]} vs {m["away"]}',
                                    "pick": pick,
                                    "odd": odd,
                                }
                            st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    # --- pestaña nueva: Analista IA ---
    with tabs[-1]:
        st.subheader("Analista IA de Partidos")
        st.caption(
            "Elegí liga y equipo local/visitante y el analista IA arma una proyección "
            "probabilística completa: índices de forma, mercados, valor de cuota (EV+) y top picks."
        )

        df_real, csv_encontrado = cargar_dataset_real()
        if csv_encontrado:
            df = df_real
        else:
            df = construir_dataset_demo()
            st.info(
                "No se encontró `master_dataset_final.csv` en la carpeta del proyecto, así que el "
                "selector está usando los partidos reales ya cargados en la casa de apuestas como "
                "dataset de respaldo. Subí tu dataset histórico completo junto a este archivo para "
                "habilitar todas las ligas y equipos."
            )

        ligas_disponibles = sorted(df["liga_nombre"].dropna().unique().tolist())

        # --- selección rápida a partir de los partidos ya cargados ---
        atajos = {"— Elegir manualmente —": None}
        for comp_name, comp_data in COMPETITIONS.items():
            liga_de_comp = comp_data.get("liga_nombre")
            if not liga_de_comp:
                continue
            for m in comp_data["matches"]:
                if m["home"].startswith(("Ganador", "Perdedor")) or m["away"] == "Por definir":
                    continue
                etiqueta = f'{m["home"]} vs {m["away"]} ({comp_name})'
                atajos[etiqueta] = (m["home"], m["away"], liga_de_comp)

        def aplicar_atajo():
            """Se ejecuta al elegir un partido rápido: pisa la selección manual
            (liga y equipo, local y visitante) y marca la consulta para
            disparar el análisis IA apenas se vuelva a dibujar la página."""
            preset = atajos.get(st.session_state.get("atajo_partido"))
            if preset is None:
                return
            home, away, liga = preset
            st.session_state["l_a"] = liga
            st.session_state["l_b"] = liga
            st.session_state["filtro_a"] = ""
            st.session_state["filtro_b"] = ""
            st.session_state["e_a"] = home
            st.session_state["e_b"] = away
            st.session_state["auto_analizar"] = True

        st.selectbox(
            "Partido rápido (opcional)", list(atajos.keys()),
            key="atajo_partido", on_change=aplicar_atajo,
        )

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Local**")
            if st.session_state.get("l_a") not in ligas_disponibles:
                st.session_state["l_a"] = ligas_disponibles[0]
            liga_a = st.selectbox("Liga", ligas_disponibles, key="l_a")

            df_a = df[df["liga_nombre"] == liga_a]
            equipos_a = sorted(set(df_a["home_name"].tolist() + df_a["away_name"].tolist()))
            filtro_a = st.text_input("Buscar equipo local", key="filtro_a", placeholder="Escribí para filtrar...")
            equipos_a_filtrados = [e for e in equipos_a if filtro_a.lower() in e.lower()] or equipos_a

            if st.session_state.get("e_a") not in equipos_a_filtrados:
                st.session_state["e_a"] = equipos_a_filtrados[0]
            equipo_a = st.selectbox("Equipo local", equipos_a_filtrados, key="e_a")

        with col2:
            st.markdown("**Visitante**")
            if st.session_state.get("l_b") not in ligas_disponibles:
                st.session_state["l_b"] = ligas_disponibles[0]
            liga_b = st.selectbox("Liga", ligas_disponibles, key="l_b")

            df_b = df[df["liga_nombre"] == liga_b]
            equipos_b = sorted(set(df_b["home_name"].tolist() + df_b["away_name"].tolist()))
            filtro_b = st.text_input("Buscar equipo visitante", key="filtro_b", placeholder="Escribí para filtrar...")
            equipos_b_filtrados = [e for e in equipos_b if filtro_b.lower() in e.lower()] or equipos_b

            default_b = equipos_b_filtrados[0]
            if st.session_state.get("e_b") not in equipos_b_filtrados:
                st.session_state["e_b"] = (
                    equipos_b_filtrados[1] if len(equipos_b_filtrados) > 1 else default_b
                )
            equipo_b = st.selectbox("Equipo visitante", equipos_b_filtrados, key="e_b")

        st.divider()

        client_groq = obtener_cliente_groq()
        if client_groq is None:
            st.warning(
                "No se encontró `GROQ_API_KEY` en el archivo `.env` (o falta instalar el paquete `groq`). "
                "El resto de la página funciona igual; para habilitar el analista IA agregá tu clave "
                "a un archivo `.env` junto a este script:\n\n`GROQ_API_KEY=tu_clave_aqui`"
            )

        auto_disparado = st.session_state.pop("auto_analizar", False)
        consultar = st.button(
            "Consultar Analista IA", type="primary", disabled=client_groq is None
        )

        if (consultar or auto_disparado) and client_groq is not None:
            with st.spinner("El analista IA está estudiando el partido..."):
                try:
                    analisis = obtener_analisis_ia(client_groq, equipo_a, equipo_b, liga_a)
                    st.markdown(f'<div class="ia-box">{analisis}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error al consultar el analista IA: {e}")

# ------------------------------------------------------------------
# BOLETO DE APUESTAS
# ------------------------------------------------------------------
with col_slip:
    st.subheader("Boleto de apuestas")
    slip = st.session_state.betslip

    if not slip:
        st.info("Elegí una cuota para armar tu boleto.")
    else:
        st.caption(f"{len(slip)} selección(es)")
        total_odd = 1.0
        for mid, s in slip.items():
            st.markdown(
                f'<div class="slip-item">{s["match"]}<br>'
                f'<b>{s["pick"]}</b> — <span style="color:var(--gold);font-family:monospace;">{s["odd"]:.2f}</span></div>',
                unsafe_allow_html=True,
            )
            total_odd *= s["odd"]

        stake = st.number_input("Monto a apostar ($)", min_value=0, value=10000, step=1000)
        payout = stake * total_odd

        st.markdown(
            f'<div class="slip-total">Cuota combinada: {total_odd:.2f}<br>'
            f'Ganancia potencial: ${payout:,.0f}</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        if c1.button("Confirmar apuesta (demo)", type="primary"):
            st.success("Apuesta demo confirmada. No se procesó dinero real.")
            st.session_state.betslip = {}
            st.rerun()
        if c2.button("Vaciar boleto"):
            st.session_state.betslip = {}
            st.rerun()

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown("---")
st.caption(
    "InstaPicks·IA es un prototipo educativo desarrollado para la materia de Inteligencia Artificial "
    "de la Universidad Tecnológica. Los partidos, competiciones y fechas mostrados son reales al "
    "12 de julio de 2026. Las cuentas de usuario, saldos, cuotas y el análisis generado por el "
    "modelo de lenguaje son simulados/educativos: no se procesa dinero real ni se gestionan "
    "apuestas reales. Si algún día usás una casa de apuestas real: jugá con responsabilidad y "
    "fijá límites de tiempo y dinero."
)

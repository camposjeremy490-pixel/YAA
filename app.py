import streamlit as st
import pandas as pd
import ast
import os
import time
from dotenv import load_dotenv
from groq import Groq
import os

# 1. Configuración de seguridad
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") # Esto toma la clave del .env, NO la escribas aquí
client = Groq(api_key=api_key)

# 3. Inicializar el cliente (si la clave es None, dará error para avisarte)
if not api_key:
    st.error("No se encontró la clave de API (GROQ_API_KEY). Verifica tu archivo .env")
    st.stop()

client = Groq(api_key=api_key)


st.set_page_config(page_title="IA Soccer Predictor", layout="wide")


# 3. Diccionario de Ligas
MAPA_LIGAS = {
    'WC': 'FIFA World Cup', 'CL': 'UEFA Champions League', 'BL1': 'Bundesliga',
    'DED': 'Eredivisie', 'BSA': 'Campeonato Brasileiro Série A', 'PD': 'Primera Division',
    'FL1': 'Ligue 1', 'ELC': 'Championship', 'PPL': 'Primeira Liga',
    'EC': 'European Championship', 'SA': 'Serie A', 'PL': 'Premier League'
}

# 4. Función de Limpieza (La vacuna contra errores)
def limpiar_datos(df):
    def extraer_nombre(val):
        try:
            if isinstance(val, str):
                return ast.literal_eval(val).get('name', val).strip()
            return str(val)
        except:
            return str(val)
    
    df['home_name'] = df['homeTeam'].apply(extraer_nombre)
    df['away_name'] = df['awayTeam'].apply(extraer_nombre)
    df['liga_nombre'] = df['liga'].map(MAPA_LIGAS).fillna(df['liga'])
    
    # Eliminamos filas con nombres vacíos para evitar errores
    df = df.dropna(subset=['home_name', 'away_name'])
    return df

@st.cache_data
def cargar_datos():
    df = pd.read_csv("master_dataset_final.csv")
    return limpiar_datos(df)

df = cargar_datos()

def obtener_analisis_ia(equipo_a, equipo_b, liga):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b", # Modelo muy rápido
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

    

# 6. Interfaz de usuario
st.title("⚽ Predictor Inteligente de Fútbol")
ligas_disponibles = sorted(df['liga_nombre'].unique())

col1, col2 = st.columns(2)

with col1:
    st.subheader("Local")
    liga_a = st.selectbox("Liga Local", ligas_disponibles, key="l_a")
    df_a = df[df['liga_nombre'] == liga_a]
    equipos_a = sorted(list(set(df_a['home_name'].unique().tolist() + df_a['away_name'].unique().tolist())))
    equipo_a = st.selectbox("Equipo Local", equipos_a, key="e_a")

with col2:
    st.subheader("Visitante")
    liga_b = st.selectbox("Liga Visitante", ligas_disponibles, key="l_b")
    df_b = df[df['liga_nombre'] == liga_b]
    equipos_b = sorted(list(set(df_b['home_name'].unique().tolist() + df_b['away_name'].unique().tolist())))
    equipo_b = st.selectbox("Equipo Visitante", equipos_b, key="e_b")

if st.button("🚀 Consultar Analista IA"):
    with st.spinner('El analista IA está estudiando el partido...'):
        try:
            analisis = obtener_analisis_ia(equipo_a, equipo_b, liga_a)
            st.markdown("---")
            st.markdown(analisis)
        except Exception as e:
            st.error(f"Error: {e}")
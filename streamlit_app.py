import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Reporte Mixpanel",
    page_icon="📊",
    layout="wide"
)

# BLOQUE DE CSS GLOBAL
st.markdown("""
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #eaefff;
        }
        .stApp {
            background-color: #eaefff;
        }
        h1, h2, h3 {
            font-family: 'DM Sans', sans-serif;
            color: black;
        }
        .header {
            background-color: #0C1461;
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            position: relative;
            margin-top: 50px;
        }
        .header h1 {
            color: white;
        }
        .kpi-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin: 20px 0;
            padding: 0;
            width: 100%;
        }
        .kpi {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid #e0e0e0;
        }
        .kpi:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .kpi h2 {
            color: #0C1461;
            font-size: 2.5em;
            margin: 0;
            font-family: 'DM Sans', sans-serif;
            font-weight: bold;
            line-height: 1.2;
        }
        .kpi p {
            color: #666;
            margin: 10px 0 0 0;
            font-size: 1em;
            font-weight: 500;
            line-height: 1.4;
            text-align: center;
        }
        .stDataFrame, .stTable {
            background: transparent !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .stDataFrame table, .stTable table {
            background: transparent !important;
            border-radius: 10px !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        .stDataFrame th, .stTable th {
            background-color: #5DDBDB !important;
            color: white !important;
            padding: 12px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 1.08em !important;
            border: 1px solid #BDC3C7 !important;
        }
        .stDataFrame td, .stTable td {
            background-color: white !important;
            color: #222 !important;
            padding: 12px !important;
            border: 1px solid #BDC3C7 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1em !important;
        }
        .stDataFrame tr, .stTable tr {
            background: transparent !important;
        }
        .bar-row {
            margin-bottom: 12px;
        }
        .bar-label {
            display: block;
            font-weight: 500;
            margin-bottom: 4px;
        }
        .bar {
            width: 100%;
            background-color: #ddd;
            border-radius: 8px;
            height: 24px;
        }
        .bar-fill {
            background-color: #5DDBDB;
            height: 100%;
            border-radius: 8px;
        }

        /* Botones generales en calipso */
        .stButton > button {
            background-color: #5DDBDB !important;
            color: #0C1461 !important;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            box-shadow: 0 4px 16px rgba(44, 62, 80, 0.15);
            transform: translateY(-2px) scale(1.04);
            color: #0C1461 !important;
            background-color: #5DDBDB !important;
        }

        /* Color base del texto general */
        body, .stApp, .markdown-text-container, .stMarkdown, p {
            color: #111 !important;
        }
        .header h1, .header h2, .header h3 {
            color: white !important;
        }

        /* Solo títulos y párrafos en negro */
        h1, h2, h3, p {
            color: #111 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Función para mostrar encabezado con logo
def encabezado_con_logo(titulo):
    st.markdown(f"""
    <div class='header'>
        <div><h2>{titulo}</h2></div>
    </div>
    """, unsafe_allow_html=True)

# Encabezado
encabezado_con_logo("Reporte de Clics - Mixpanel")

csv_path = "inputs/mixpanel_applicants_merged_20250708_100107.csv"

# Leer solo las columnas necesarias
cols = ["event", "userUuid", "date"]
try:
    df = pd.read_csv(csv_path, usecols=lambda c: c in cols, low_memory=False)
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
    st.stop()

# Estadísticas generales
usuarios_unicos = df["userUuid"].nunique()
total_clics = len(df)
promedio_clics = total_clics / usuarios_unicos if usuarios_unicos > 0 else 0

# Mostrar KPIs con el estilo del otro archivo
st.markdown("""
<div class="kpi-container">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi">
        <h2>{usuarios_unicos:,}</h2>
        <p>Usuarios únicos</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_clics:,}</h2>
        <p>Total de clics (eventos)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi">
        <h2>{promedio_clics:.2f}</h2>
        <p>Promedio de clics por usuario</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Estadísticas por tipo de evento
st.subheader("📊 Estadísticas por Tipo de Evento")

# Calcular estadísticas por evento
eventos_stats = df.groupby('event').agg({
    'userUuid': ['count', 'nunique']
}).round(2)

# Renombrar columnas
eventos_stats.columns = ['Total Clics', 'Usuarios Únicos']
eventos_stats = eventos_stats.reset_index()

# Calcular promedio de clics por usuario para cada evento
eventos_stats['Promedio Clics por Usuario'] = (eventos_stats['Total Clics'] / eventos_stats['Usuarios Únicos']).round(2)

# Ordenar por total de clics (descendente)
eventos_stats = eventos_stats.sort_values('Total Clics', ascending=False)

# Mostrar tabla de estadísticas por evento
st.markdown("### Tabla de Estadísticas por Evento")
st.dataframe(eventos_stats, use_container_width=True)

# Gráfico de barras para los eventos más populares
st.markdown("### 📈 Top 10 Eventos por Total de Clics")

# Tomar los top 10 eventos
top_10_eventos = eventos_stats.head(10)

# Crear gráfico de barras
import plotly.express as px

fig = px.bar(
    top_10_eventos,
    x='event',
    y='Total Clics',
    title='Top 10 Eventos por Total de Clics',
    color='Total Clics',
    color_continuous_scale='Blues'
)

fig.update_layout(
    xaxis_title="Tipo de Evento",
    yaxis_title="Total de Clics",
    plot_bgcolor='#eaefff',
    paper_bgcolor='#eaefff',
    font=dict(family="Inter", size=14, color="#333"),
    title=dict(
        font=dict(size=20, family="DM Sans", color="#0C1461"),
        x=0.5,
        xanchor='center'
    )
)

fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# Gráfico de promedio de clics por usuario
st.markdown("### 📊 Promedio de Clics por Usuario (Top 10)")

fig_promedio = px.bar(
    top_10_eventos,
    x='event',
    y='Promedio Clics por Usuario',
    title='Promedio de Clics por Usuario por Evento',
    color='Promedio Clics por Usuario',
    color_continuous_scale='Greens'
)

fig_promedio.update_layout(
    xaxis_title="Tipo de Evento",
    yaxis_title="Promedio de Clics por Usuario",
    plot_bgcolor='#eaefff',
    paper_bgcolor='#eaefff',
    font=dict(family="Inter", size=14, color="#333"),
    title=dict(
        font=dict(size=20, family="DM Sans", color="#0C1461"),
        x=0.5,
        xanchor='center'
    )
)

fig_promedio.update_xaxes(tickangle=45)
st.plotly_chart(fig_promedio, use_container_width=True)

# Mostrar tabla de eventos recientes
st.subheader("📋 Primeros 100 eventos")
df_sample = df.head(100)
st.dataframe(df_sample)

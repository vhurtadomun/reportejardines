import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Reporte Usuarios - Jardines",
    page_icon="👥",
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
encabezado_con_logo("Reporte de Usuarios - Jardines")

# Cargar datos de usuarios por fuente
user_files = {
    "MongoDB": "inputs/mongo_user_summary.csv",
    "PostgreSQL": "inputs/postgres_user_summary.csv", 
    "Mixpanel": "inputs/mixpanel_user_summary.csv"
}

dfs = {}
for source, file_path in user_files.items():
    try:
        df = pd.read_csv(file_path)
        df['data_source'] = source
        dfs[source] = df
        st.success(f"✅ {source}: {len(df)} usuarios cargados")
    except Exception as e:
        st.error(f"❌ Error cargando {source}: {str(e)}")

if not dfs:
    st.error("❌ No se pudieron cargar los archivos de usuarios")
    st.stop()

# Combinar todos los DataFrames
all_users = pd.concat(dfs.values(), ignore_index=True)

# 👥 ESTADÍSTICAS A NIVEL DE USUARIOS
st.markdown("## 👥 Estadísticas a Nivel de Usuarios")

# 1. KPIs principales
total_usuarios = len(all_users)
usuarios_por_fuente = all_users['data_source'].value_counts()
promedio_eventos = all_users['total_events'].mean()
promedio_eventos_unicos = all_users['unique_event_count'].mean()

# Mostrar KPIs básicos
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_usuarios:,}</h2>
        <p>Total de Usuarios</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi">
        <h2>{promedio_eventos:.1f}</h2>
        <p>Promedio Eventos/Usuario</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi">
        <h2>{promedio_eventos_unicos:.1f}</h2>
        <p>Promedio Eventos Únicos/Usuario</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi">
        <h2>{len(all_users['user'].unique()):,}</h2>
        <p>Usuarios Únicos</p>
    </div>
    """, unsafe_allow_html=True)

# 2. Distribución de usuarios por fuente de datos
st.markdown("### 📊 Distribución de Usuarios por Fuente de Datos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Usuarios por Fuente de Datos")
    source_stats = all_users['data_source'].value_counts().reset_index()
    source_stats.columns = ['Fuente de Datos', 'Total de Usuarios']
    st.dataframe(source_stats, use_container_width=True)

with col2:
    # Gráfico de fuentes de datos
    fig_source = px.pie(
        source_stats, 
        values='Total de Usuarios', 
        names='Fuente de Datos',
        title='Distribución de Usuarios por Fuente de Datos'
    )
    fig_source.update_layout(
        plot_bgcolor='#eaefff',
        paper_bgcolor='#eaefff',
        font=dict(family="Inter", size=14, color="#333"),
        title=dict(
            font=dict(size=20, family="DM Sans", color="#0C1461"),
            x=0.5,
            xanchor='center'
        )
    )
    st.plotly_chart(fig_source, use_container_width=True)

# 3. Análisis de actividad de usuarios
st.markdown("### 📈 Análisis de Actividad de Usuarios")

# Top 10 usuarios más activos
st.markdown("#### Top 10 Usuarios Más Activos")
top_active_users = all_users.nlargest(10, 'total_events')[['user', 'email', 'data_source', 'total_events', 'unique_event_count']]
st.dataframe(top_active_users, use_container_width=True)

# Gráfico de distribución de eventos por usuario
fig_events_dist = px.histogram(
    all_users,
    x='total_events',
    nbins=20,
    title='Distribución de Total de Eventos por Usuario',
    labels={'total_events': 'Total de Eventos', 'count': 'Número de Usuarios'}
)
fig_events_dist.update_layout(
    plot_bgcolor='#eaefff',
    paper_bgcolor='#eaefff',
    font=dict(family="Inter", size=14, color="#333"),
    title=dict(
        font=dict(size=20, family="DM Sans", color="#0C1461"),
        x=0.5,
        xanchor='center'
    )
)
st.plotly_chart(fig_events_dist, use_container_width=True)

# 4. Comparación entre fuentes de datos
st.markdown("### 🔄 Comparación entre Fuentes de Datos")

# Estadísticas por fuente
source_comparison = all_users.groupby('data_source').agg({
    'total_events': ['mean', 'median', 'max'],
    'unique_event_count': ['mean', 'median', 'max'],
    'user': 'count'
}).round(2)

source_comparison.columns = ['Promedio Eventos', 'Mediana Eventos', 'Máx Eventos', 
                           'Promedio Eventos Únicos', 'Mediana Eventos Únicos', 'Máx Eventos Únicos', 'Total Usuarios']
source_comparison = source_comparison.reset_index()

st.markdown("#### Estadísticas Comparativas por Fuente")
st.dataframe(source_comparison, use_container_width=True)

# Gráfico de comparación
fig_comparison = px.bar(
    source_comparison,
    x='data_source',
    y=['Promedio Eventos', 'Promedio Eventos Únicos'],
    title='Comparación de Promedio de Eventos por Fuente',
    barmode='group'
)
fig_comparison.update_layout(
    plot_bgcolor='#eaefff',
    paper_bgcolor='#eaefff',
    font=dict(family="Inter", size=14, color="#333"),
    title=dict(
        font=dict(size=20, family="DM Sans", color="#0C1461"),
        x=0.5,
        xanchor='center'
    )
)
st.plotly_chart(fig_comparison, use_container_width=True)

# 5. Análisis temporal de actividad
st.markdown("### ⏰ Análisis Temporal de Actividad")

# Convertir fechas
all_users['first_activity'] = pd.to_datetime(all_users['first_activity'])
all_users['last_activity'] = pd.to_datetime(all_users['last_activity'])

# Calcular duración de sesión
all_users['session_duration'] = (all_users['last_activity'] - all_users['first_activity']).dt.total_seconds() / 3600  # en horas

# Top 10 sesiones más largas
st.markdown("#### Top 10 Sesiones Más Largas (horas)")
top_sessions = all_users.nlargest(10, 'session_duration')[['user', 'email', 'data_source', 'session_duration', 'total_events']]
top_sessions['session_duration'] = top_sessions['session_duration'].round(2)
st.dataframe(top_sessions, use_container_width=True)

# Gráfico de duración de sesiones
fig_sessions = px.histogram(
    all_users[all_users['session_duration'] > 0],
    x='session_duration',
    nbins=20,
    title='Distribución de Duración de Sesiones (horas)',
    labels={'session_duration': 'Duración (horas)', 'count': 'Número de Usuarios'}
)
fig_sessions.update_layout(
    plot_bgcolor='#eaefff',
    paper_bgcolor='#eaefff',
    font=dict(family="Inter", size=14, color="#333"),
    title=dict(
        font=dict(size=20, family="DM Sans", color="#0C1461"),
        x=0.5,
        xanchor='center'
    )
)
st.plotly_chart(fig_sessions, use_container_width=True)

# 6. Resumen de datos
st.markdown("### 📋 Resumen de Datos")
st.markdown(f"""
- **Total de usuarios analizados**: {total_usuarios:,}
- **Usuarios únicos**: {len(all_users['user'].unique()):,}
- **Promedio de eventos por usuario**: {promedio_eventos:.1f}
- **Promedio de eventos únicos por usuario**: {promedio_eventos_unicos:.1f}
- **Usuario más activo**: {all_users.loc[all_users['total_events'].idxmax(), 'email']} ({all_users['total_events'].max()} eventos)
- **Sesión más larga**: {all_users['session_duration'].max():.2f} horas
""")

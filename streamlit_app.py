import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Completo - Jardines",
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
encabezado_con_logo("Dashboard Completo - Jardines")

# Función para cargar datos
def load_data():
    data = {}
    
    # Archivos de resumen de usuarios
    user_summary_files = {
        "MongoDB": "inputs/mongo_user_summary.csv",
        "PostgreSQL": "inputs/postgres_user_summary.csv", 
        "Mixpanel": "inputs/mixpanel_user_summary.csv"
    }
    
    # Archivos de eventos por usuario
    user_event_files = {
        "MongoDB": "inputs/mongo_user_event_summary.csv",
        "PostgreSQL": "inputs/postgres_user_event_summary.csv", 
        "Mixpanel": "inputs/mixpanel_user_event_summary.csv"
    }
    
    # Archivos de actividad diaria
    daily_activity_files = {
        "MongoDB": "inputs/mongo_daily_activity_summary.csv",
        "PostgreSQL": "inputs/postgres_daily_activity_summary.csv", 
        "Mixpanel": "inputs/mixpanel_ daily_activity_summary.csv"
    }
    
    # Archivos de resumen de eventos
    event_summary_files = {
        "MongoDB": "inputs/mongo_event_summary.csv",
        "PostgreSQL": "inputs/postgres_event_summary.csv", 
        "Mixpanel": "inputs/mixpanel_event_summary.csv"
    }
    
    # Archivos filtrados por aplicantes
    applicant_files = {
        "MongoDB": "inputs/mongo_filtered_by_applicants.csv",
        "PostgreSQL": "inputs/postgres_filtered_by_applicants.csv", 
        "Mixpanel": "inputs/mixpanel_filtered_by_applicants.csv"
    }
    
    # Cargar todos los archivos
    for source, file_path in user_summary_files.items():
        try:
            df = pd.read_csv(file_path)
            df['data_source'] = source
            data[f"{source}_user_summary"] = df
        except Exception as e:
            st.error(f"❌ Error cargando {source} user_summary: {str(e)}")
    
    for source, file_path in user_event_files.items():
        try:
            df = pd.read_csv(file_path)
            df['data_source'] = source
            data[f"{source}_user_events"] = df
        except Exception as e:
            st.error(f"❌ Error cargando {source} user_events: {str(e)}")
    
    for source, file_path in daily_activity_files.items():
        try:
            df = pd.read_csv(file_path)
            df['data_source'] = source
            data[f"{source}_daily"] = df
        except Exception as e:
            st.error(f"❌ Error cargando {source} daily_activity: {str(e)}")
    
    for source, file_path in event_summary_files.items():
        try:
            df = pd.read_csv(file_path)
            df['data_source'] = source
            data[f"{source}_events"] = df
        except Exception as e:
            st.error(f"❌ Error cargando {source} event_summary: {str(e)}")
    
    for source, file_path in applicant_files.items():
        try:
            df = pd.read_csv(file_path)
            df['data_source'] = source
            data[f"{source}_applicants"] = df
        except Exception as e:
            st.error(f"❌ Error cargando {source} applicants: {str(e)}")
    
    return data

# Cargar datos
data = load_data()

if not data:
    st.error("❌ No se pudieron cargar los archivos")
    st.stop()

# Función para encontrar el evento más frecuente por usuario
def get_top_event_per_user(df, user_col='user', email_col='email'):
    """Encuentra el evento más frecuente para cada usuario"""
    event_columns = [col for col in df.columns if col not in [user_col, email_col, 'applicant_id', 'data_source']]
    
    if not event_columns:
        return pd.DataFrame()
    
    results = []
    for _, row in df.iterrows():
        user = row[user_col]
        email = row[email_col]
        data_source = row.get('data_source', 'Unknown')
        
        # Encontrar el evento con mayor valor
        event_counts = {col: row[col] for col in event_columns if pd.notna(row[col]) and row[col] > 0}
        
        if event_counts:
            top_event = max(event_counts.items(), key=lambda x: x[1])
            results.append({
                'user': user,
                'email': email,
                'data_source': data_source,
                'top_event': top_event[0],
                'event_count': top_event[1],
                'total_events': sum(event_counts.values())
            })
    
    return pd.DataFrame(results)

# 1. ANÁLISIS DE EVENTOS POR USUARIO
st.markdown("## 🎯 Análisis de Eventos por Usuario")

# Solo usar datos de Mixpanel para la tabla principal
mixpanel_user_events = None
for key, df in data.items():
    if 'Mixpanel_user_events' in key:
        mixpanel_user_events = df
        break

if mixpanel_user_events is not None:
    # Mostrar tabla de usuarios vs eventos (solo Mixpanel)
    st.markdown("### 📊 Tabla de Usuarios y Eventos (Mixpanel)")
    
    # Obtener columnas de eventos (excluir columnas de identificación)
    event_columns = [col for col in mixpanel_user_events.columns 
                    if col not in ['user', 'email', 'applicant_id', 'data_source']]
    
    if event_columns:
        # Crear tabla con usuarios como filas y eventos como columnas
        user_event_table = mixpanel_user_events[['user', 'email', 'data_source'] + event_columns].copy()
        
        # Mostrar la tabla
        st.markdown("#### Conteo de Eventos por Usuario")
        st.dataframe(user_event_table, use_container_width=True)
        
        # Mostrar estadísticas de eventos
        st.markdown("#### Estadísticas de Eventos")
        event_stats = user_event_table[event_columns].describe().round(2)
        st.dataframe(event_stats, use_container_width=True)
        
        # Gráfico de eventos más frecuentes
        st.markdown("#### Eventos Más Frecuentes")
        event_totals = user_event_table[event_columns].sum().sort_values(ascending=False)
        fig_top_events = px.bar(
            x=event_totals.values,
            y=event_totals.index,
            orientation='h',
            title='Total de Eventos por Tipo (Mixpanel)',
            labels={'x': 'Total de Eventos', 'y': 'Tipo de Evento'}
        )
        fig_top_events.update_layout(
            plot_bgcolor='#eaefff',
            paper_bgcolor='#eaefff',
            font=dict(family="Inter", size=14, color="#333"),
            title=dict(
                font=dict(size=20, family="DM Sans", color="#0C1461"),
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_top_events, use_container_width=True)
    
    # Encontrar el evento más frecuente por usuario (solo Mixpanel)
    top_events_df = get_top_event_per_user(mixpanel_user_events)
    
    if not top_events_df.empty:
        st.markdown("### 📈 Evento Más Frecuente por Usuario (Mixpanel)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Usuarios por Evento Más Frecuente")
            top_events_sorted = top_events_df.nlargest(10, 'event_count')
            st.dataframe(top_events_sorted, use_container_width=True)
        
        with col2:
            # Gráfico de eventos más frecuentes
            event_counts = top_events_df['top_event'].value_counts().head(10)
            fig_top_events = px.bar(
                x=event_counts.values,
                y=event_counts.index,
                orientation='h',
                title='Top 10 Eventos Más Frecuentes (Mixpanel)',
                labels={'x': 'Número de Usuarios', 'y': 'Evento'}
            )
            fig_top_events.update_layout(
                plot_bgcolor='#eaefff',
                paper_bgcolor='#eaefff',
                font=dict(family="Inter", size=14, color="#333"),
                title=dict(
                    font=dict(size=20, family="DM Sans", color="#0C1461"),
                    x=0.5,
                    xanchor='center'
                )
            )
            st.plotly_chart(fig_top_events, use_container_width=True)
        
        # Análisis por fuente de datos (solo Mixpanel)
        st.markdown("### 🔄 Análisis de Mixpanel")
        
        source_analysis = top_events_df.groupby('data_source').agg({
            'event_count': ['mean', 'max', 'sum'],
            'total_events': ['mean', 'max', 'sum'],
            'user': 'count'
        }).round(2)
        
        source_analysis.columns = ['Promedio Evento Top', 'Máx Evento Top', 'Total Eventos Top', 
                                 'Promedio Total Eventos', 'Máx Total Eventos', 'Total Eventos', 'Usuarios']
        source_analysis = source_analysis.reset_index()
        
        st.dataframe(source_analysis, use_container_width=True)

# 2. COMPARACIÓN ENTRE FUENTES DE DATOS
st.markdown("## 🔄 Comparación entre Fuentes de Datos")

# Solo usar datos de PostgreSQL para la segunda tabla
postgres_user_events = None
for key, df in data.items():
    if 'PostgreSQL_user_events' in key:
        postgres_user_events = df
        break

if postgres_user_events is not None:
    # Mostrar tabla de usuarios vs eventos (solo PostgreSQL)
    st.markdown("### 📊 Tabla de Usuarios y Eventos (PostgreSQL)")
    
    # Obtener columnas de eventos (excluir columnas de identificación)
    event_columns = [col for col in postgres_user_events.columns 
                    if col not in ['user', 'email', 'applicant_id', 'data_source']]
    
    if event_columns:
        # Crear tabla con usuarios como filas y eventos como columnas
        user_event_table = postgres_user_events[['user', 'email', 'data_source'] + event_columns].copy()
        
        # Mostrar la tabla
        st.markdown("#### Conteo de Eventos por Usuario")
        st.dataframe(user_event_table, use_container_width=True)
        
        # Mostrar estadísticas de eventos
        st.markdown("#### Estadísticas de Eventos")
        event_stats = user_event_table[event_columns].describe().round(2)
        st.dataframe(event_stats, use_container_width=True)
        
        # Gráfico de eventos más frecuentes
        st.markdown("#### Eventos Más Frecuentes")
        event_totals = user_event_table[event_columns].sum().sort_values(ascending=False)
        fig_top_events = px.bar(
            x=event_totals.values,
            y=event_totals.index,
            orientation='h',
            title='Total de Eventos por Tipo (PostgreSQL)',
            labels={'x': 'Total de Eventos', 'y': 'Tipo de Evento'}
        )
        fig_top_events.update_layout(
            plot_bgcolor='#eaefff',
            paper_bgcolor='#eaefff',
            font=dict(family="Inter", size=14, color="#333"),
            title=dict(
                font=dict(size=20, family="DM Sans", color="#0C1461"),
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_top_events, use_container_width=True)
    
    # Encontrar el evento más frecuente por usuario (solo PostgreSQL)
    top_events_df = get_top_event_per_user(postgres_user_events)
    
    if not top_events_df.empty:
        st.markdown("### 📈 Evento Más Frecuente por Usuario (PostgreSQL)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Usuarios por Evento Más Frecuente")
            top_events_sorted = top_events_df.nlargest(10, 'event_count')
            st.dataframe(top_events_sorted, use_container_width=True)
        
        with col2:
            # Gráfico de eventos más frecuentes
            event_counts = top_events_df['top_event'].value_counts().head(10)
            fig_top_events = px.bar(
                x=event_counts.values,
                y=event_counts.index,
                orientation='h',
                title='Top 10 Eventos Más Frecuentes (PostgreSQL)',
                labels={'x': 'Número de Usuarios', 'y': 'Evento'}
            )
            fig_top_events.update_layout(
                plot_bgcolor='#eaefff',
                paper_bgcolor='#eaefff',
                font=dict(family="Inter", size=14, color="#333"),
                title=dict(
                    font=dict(size=20, family="DM Sans", color="#0C1461"),
                    x=0.5,
                    xanchor='center'
                )
            )
            st.plotly_chart(fig_top_events, use_container_width=True)
        
        # Análisis por fuente de datos (solo PostgreSQL)
        st.markdown("### 🔄 Análisis de PostgreSQL")
        
        source_analysis = top_events_df.groupby('data_source').agg({
            'event_count': ['mean', 'max', 'sum'],
            'total_events': ['mean', 'max', 'sum'],
            'user': 'count'
        }).round(2)
        
        source_analysis.columns = ['Promedio Evento Top', 'Máx Evento Top', 'Total Eventos Top', 
                                 'Promedio Total Eventos', 'Máx Total Eventos', 'Total Eventos', 'Usuarios']
        source_analysis = source_analysis.reset_index()
        
        st.dataframe(source_analysis, use_container_width=True)

# 3. ANÁLISIS TEMPORAL
st.markdown("## ⏰ Análisis Temporal")

# Solo usar datos de MongoDB para la tercera tabla
mongo_user_events = None
for key, df in data.items():
    if 'MongoDB_user_events' in key:
        mongo_user_events = df
        break

if mongo_user_events is not None:
    # Mostrar tabla de usuarios vs eventos (solo MongoDB)
    st.markdown("### 📊 Tabla de Usuarios y Eventos (MongoDB)")
    
    # Obtener columnas de eventos (excluir columnas de identificación)
    event_columns = [col for col in mongo_user_events.columns 
                    if col not in ['user', 'email', 'applicant_id', 'data_source']]
    
    if event_columns:
        # Crear tabla con usuarios como filas y eventos como columnas
        user_event_table = mongo_user_events[['user', 'email', 'data_source'] + event_columns].copy()
        
        # Mostrar la tabla
        st.markdown("#### Conteo de Eventos por Usuario")
        st.dataframe(user_event_table, use_container_width=True)
        
        # Mostrar estadísticas de eventos
        st.markdown("#### Estadísticas de Eventos")
        event_stats = user_event_table[event_columns].describe().round(2)
        st.dataframe(event_stats, use_container_width=True)
        
        # Gráfico de eventos más frecuentes
        st.markdown("#### Eventos Más Frecuentes")
        event_totals = user_event_table[event_columns].sum().sort_values(ascending=False)
        fig_top_events = px.bar(
            x=event_totals.values,
            y=event_totals.index,
            orientation='h',
            title='Total de Eventos por Tipo (MongoDB)',
            labels={'x': 'Total de Eventos', 'y': 'Tipo de Evento'}
        )
        fig_top_events.update_layout(
            plot_bgcolor='#eaefff',
            paper_bgcolor='#eaefff',
            font=dict(family="Inter", size=14, color="#333"),
            title=dict(
                font=dict(size=20, family="DM Sans", color="#0C1461"),
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_top_events, use_container_width=True)
    
    # Encontrar el evento más frecuente por usuario (solo MongoDB)
    top_events_df = get_top_event_per_user(mongo_user_events)
    
    if not top_events_df.empty:
        st.markdown("### 📈 Evento Más Frecuente por Usuario (MongoDB)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Usuarios por Evento Más Frecuente")
            top_events_sorted = top_events_df.nlargest(10, 'event_count')
            st.dataframe(top_events_sorted, use_container_width=True)
        
        with col2:
            # Gráfico de eventos más frecuentes
            event_counts = top_events_df['top_event'].value_counts().head(10)
            fig_top_events = px.bar(
                x=event_counts.values,
                y=event_counts.index,
                orientation='h',
                title='Top 10 Eventos Más Frecuentes (MongoDB)',
                labels={'x': 'Número de Usuarios', 'y': 'Evento'}
            )
            fig_top_events.update_layout(
                plot_bgcolor='#eaefff',
                paper_bgcolor='#eaefff',
                font=dict(family="Inter", size=14, color="#333"),
                title=dict(
                    font=dict(size=20, family="DM Sans", color="#0C1461"),
                    x=0.5,
                    xanchor='center'
                )
            )
            st.plotly_chart(fig_top_events, use_container_width=True)
        
        # Análisis por fuente de datos (solo MongoDB)
        st.markdown("### 🔄 Análisis de MongoDB")
        
        source_analysis = top_events_df.groupby('data_source').agg({
            'event_count': ['mean', 'max', 'sum'],
            'total_events': ['mean', 'max', 'sum'],
            'user': 'count'
        }).round(2)
        
        source_analysis.columns = ['Promedio Evento Top', 'Máx Evento Top', 'Total Eventos Top', 
                                 'Promedio Total Eventos', 'Máx Total Eventos', 'Total Eventos', 'Usuarios']
        source_analysis = source_analysis.reset_index()
        
        st.dataframe(source_analysis, use_container_width=True)

# 4. ANÁLISIS DE EVENTOS
st.markdown("## 📊 Análisis de Eventos")

# Combinar todos los resúmenes de eventos
all_event_summaries = []
for key, df in data.items():
    if 'events' in key and 'user_events' not in key:
        all_event_summaries.append(df)

if all_event_summaries:
    combined_events = pd.concat(all_event_summaries, ignore_index=True)
    
    st.markdown("#### Resumen de Eventos por Fuente")
    st.dataframe(combined_events, use_container_width=True)

# 5. ANÁLISIS DE APLICANTES
st.markdown("## 👥 Análisis de Aplicantes")

# Combinar todos los archivos de aplicantes
all_applicants = []
for key, df in data.items():
    if 'applicants' in key:
        all_applicants.append(df)

if all_applicants:
    combined_applicants = pd.concat(all_applicants, ignore_index=True)
    
    st.markdown("#### Datos de Aplicantes por Fuente")
    
    # Estadísticas básicas de aplicantes
    applicant_stats = combined_applicants.groupby('data_source').agg({
        'user': 'count'
    }).reset_index()
    applicant_stats.columns = ['Fuente de Datos', 'Total de Aplicantes']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(applicant_stats, use_container_width=True)
    
    with col2:
        # Gráfico de aplicantes por fuente
        fig_applicants = px.pie(
            applicant_stats,
            values='Total de Aplicantes',
            names='Fuente de Datos',
            title='Distribución de Aplicantes por Fuente'
        )
        fig_applicants.update_layout(
            plot_bgcolor='#eaefff',
            paper_bgcolor='#eaefff',
            font=dict(family="Inter", size=14, color="#333"),
            title=dict(
                font=dict(size=20, family="DM Sans", color="#0C1461"),
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_applicants, use_container_width=True)

# 6. RESUMEN GENERAL
st.markdown("## 📋 Resumen General")

# Calcular estadísticas generales
total_users = sum(len(df) for key, df in data.items() if 'user_summary' in key)
total_events = sum(len(df) for key, df in data.items() if 'events' in key and 'user_events' not in key)
total_applicants = sum(len(df) for key, df in data.items() if 'applicants' in key)

# Mostrar KPIs generales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_users:,}</h2>
        <p>Total de Usuarios</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_events:,}</h2>
        <p>Total de Eventos</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_applicants:,}</h2>
        <p>Total de Aplicantes</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi">
        <h2>{len(data):,}</h2>
        <p>Archivos Cargados</p>
    </div>
    """, unsafe_allow_html=True)

# Mostrar información detallada
st.markdown("### 📊 Información Detallada")
st.markdown(f"""
- **Archivos de usuarios cargados**: {len([k for k in data.keys() if 'user_summary' in k])}
- **Archivos de eventos cargados**: {len([k for k in data.keys() if 'events' in k and 'user_events' not in k])}
- **Archivos de actividad diaria cargados**: {len([k for k in data.keys() if 'daily' in k])}
- **Archivos de aplicantes cargados**: {len([k for k in data.keys() if 'applicants' in k])}
- **Fuentes de datos disponibles**: {', '.join(set([k.split('_')[0] for k in data.keys()]))}
""")

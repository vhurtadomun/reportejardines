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
        "Mixpanel": "inputs/mixpanel_applicants_collapsed.csv"
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
    
    # Archivo de aplicantes fusionados de MongoDB
    mongo_applicants_merged_file = "inputs/mongo_applicants_merged.csv"
    
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
    
    # Cargar archivo de aplicantes fusionados de MongoDB
    try:
        df = pd.read_csv(mongo_applicants_merged_file)
        data["mongo_applicants_merged"] = df
    except Exception as e:
        st.error(f"❌ Error cargando mongo_applicants_merged: {str(e)}")
    
    return data

# Función para encontrar el evento más frecuente por usuario
# def get_top_event_per_user(df, user_col='user', email_col='email'):
#     """Encuentra el evento más frecuente para cada usuario"""
#     event_columns = [col for col in df.columns if col not in [user_col, email_col, 'applicant_id', 'data_source']]
    
#     if not event_columns:
#         return pd.DataFrame()
    
#     results = []
#     for _, row in df.iterrows():
#         user = row[user_col]
#         email = row[email_col]
#         data_source = row.get('data_source', 'Unknown')
        
#         # Encontrar el evento con mayor valor
#         event_counts = {col: row[col] for col in event_columns if pd.notna(row[col]) and row[col] > 0}
        
#         if event_counts:
#             top_event = max(event_counts.items(), key=lambda x: x[1])
#             results.append({
#                 'user': user,
#                 'email': email,
#                 'data_source': data_source,
#                 'top_event': top_event[0],
#                 'event_count': top_event[1],
#                 'total_events': sum(event_counts.values())
#             })
    
#     return pd.DataFrame(results)

# Cargar datos
data = load_data()

if not data:
    st.error("❌ No se pudieron cargar los archivos")
    st.stop()

# 6. RESUMEN GENERAL
st.markdown("Resumen General")

# Calcular estadísticas específicas por fuente
total_users_postgres = 0
total_events_mixpanel = 0
total_notes_mongo = 0
total_favorites = 0

# Total usuarios de PostgreSQL
# for key, df in data.items():
#     if 'PostgreSQL_user_summary' in key:
#         total_users_postgres = len(df)
#         break

# Por ahora, establecer valores por defecto
total_users_postgres = 0

# Total eventos de Mixpanel
# for key, df in data.items():
#     if 'Mixpanel_user_events' in key:
#         # Sumar todos los eventos de Mixpanel
#         event_columns = [col for col in df.columns 
#                         if col not in ['user', 'email', 'applicant_id', 'data_source']]
#         if event_columns:
#             total_events_mixpanel = df[event_columns].sum().sum()
#         break

# Por ahora, establecer un valor por defecto
total_events_mixpanel = 0

# Total notas de MongoDB (desde mongo_applicants_merged.csv)
total_notes_mongo = 0
for key, df in data.items():
    if 'mongo_applicants_merged' in key:
        # Contar registros donde type es 'campus_note'
        if 'type' in df.columns:
            total_notes_mongo = len(df[df['type'] == 'campus_note'])
        break

# Total favoritos (buscar en PostgreSQL)
# for key, df in data.items():
#     if 'PostgreSQL_user_events' in key:
#         favorite_columns = [col for col in df.columns if 'favorite' in col.lower()]
#         if favorite_columns:
#             total_favorites = df[favorite_columns].sum().sum()
#         break

# Por ahora, establecer un valor por defecto
total_favorites = 0

# Mostrar KPIs generales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_users_postgres:,}</h2>
        <p>Total de Usuarios (PostgreSQL)</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_events_mixpanel:,}</h2>
        <p>Total de Eventos (Mixpanel)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_notes_mongo:,}</h2>
        <p>Notas Guardadas (MongoDB)</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_favorites:,}</h2>
        <p>Favoritos Guardados (PostgreSQL)</p>
    </div>
    """, unsafe_allow_html=True)

# Mostrar información detallada
st.markdown("### 📊 Información Detallada")
st.markdown(f"""
- **Usuarios de PostgreSQL**: {total_users_postgres:,}
- **Eventos de Mixpanel**: {total_events_mixpanel:,}
- **Notas guardadas en MongoDB**: {total_notes_mongo:,}
- **Favoritos guardados en PostgreSQL**: {total_favorites:,}
- **Archivos cargados**: {len(data):,}
- **Fuentes de datos disponibles**: {', '.join(set([k.split('_')[0] for k in data.keys()]))}
""")

# Tabla de notas guardadas
st.markdown("### 📝 Notas Guardadas")
for key, df in data.items():
    if 'mongo_applicants_merged' in key:
        # Filtrar solo registros de tipo campus_note
        notes_df = df[df['type'] == 'campus_note'].copy()
        
        if not notes_df.empty:
            # Función para extraer el contenido del JSON
            def extract_note_content(data_str):
                try:
                    import json
                    if isinstance(data_str, str):
                        data_dict = json.loads(data_str)
                        return data_dict.get('content', '')
                    return ''
                except:
                    return ''
            
            # Extraer el contenido de las notas
            notes_df['nota'] = notes_df['data'].apply(extract_note_content)
            
            # Seleccionar columnas para mostrar
            display_columns = ['userId', 'email', 'nota']
            available_columns = [col for col in display_columns if col in notes_df.columns]
            
            if available_columns:
                # Renombrar userId a user para la visualización
                if 'userId' in available_columns:
                    notes_df = notes_df.rename(columns={'userId': 'user'})
                    available_columns = ['user' if col == 'userId' else col for col in available_columns]
                
                # Mostrar la tabla
                st.dataframe(notes_df[available_columns], use_container_width=True)
            else:
                st.info("No se encontraron columnas necesarias para mostrar las notas")
        else:
            st.info("No se encontraron notas guardadas")
        break

# 1. ANÁLISIS DE EVENTOS POR USUARIO
# st.markdown("## 🎯 Análisis de Eventos por Usuario")

# # Solo usar datos de Mixpanel para la tabla principal
# mixpanel_user_events = None
# for key, df in data.items():
#     if 'Mixpanel_user_events' in key:
#         mixpanel_user_events = df
#         break

# if mixpanel_user_events is not None:
#     # Mostrar tabla de usuarios vs eventos (solo Mixpanel)
#     st.markdown("### 📊 Tabla de Usuarios y Eventos (Mixpanel)")
    
#     # Obtener columnas de eventos (excluir columnas de identificación)
#     event_columns = [col for col in mixpanel_user_events.columns 
#                     if col not in ['user', 'email', 'applicant_id', 'data_source']]
    
#     if event_columns:
#         # Crear tabla con usuarios como filas y eventos como columnas
#         user_event_table = mixpanel_user_events[['user', 'email', 'data_source'] + event_columns].copy()
        
#         # Mostrar la tabla
#         st.markdown("#### Conteo de Eventos por Usuario")
#         st.dataframe(user_event_table, use_container_width=True)

# 2. COMPARACIÓN ENTRE FUENTES DE DATOS
# st.markdown("## 🔄 Comparación entre Fuentes de Datos")

# # Solo usar datos de PostgreSQL para la segunda tabla
# postgres_user_events = None
# for key, df in data.items():
#     if 'PostgreSQL_user_events' in key:
#         postgres_user_events = df
#         break

# if postgres_user_events is not None:
#     # Mostrar tabla de usuarios vs eventos (solo PostgreSQL)
#     st.markdown("### 📊 Tabla de Usuarios y Eventos (PostgreSQL)")
    
#     # Obtener columnas de eventos (excluir columnas de identificación)
#     event_columns = [col for col in postgres_user_events.columns 
#                     if col not in ['user', 'email', 'applicant_id', 'data_source']]
    
#     if event_columns:
#         # Crear tabla con usuarios como filas y eventos como columnas
#         user_event_table = postgres_user_events[['user', 'email', 'data_source'] + event_columns].copy()
        
#         # Mostrar la tabla
#         st.markdown("#### Conteo de Eventos por Usuario")
#         st.dataframe(user_event_table, use_container_width=True)

# 3. ANÁLISIS TEMPORAL
# st.markdown("## ⏰ Análisis Temporal")

# # Solo usar datos de MongoDB para la tercera tabla
# mongo_user_events = None
# for key, df in data.items():
#     if 'MongoDB_user_events' in key:
#         mongo_user_events = df
#         break

# if mongo_user_events is not None:
#     # Mostrar tabla de usuarios vs eventos (solo MongoDB)
#     st.markdown("### 📊 Tabla de Usuarios y Eventos (MongoDB)")
    
#     # Obtener columnas de eventos (excluir columnas de identificación)
#     event_columns = [col for col in mongo_user_events.columns 
#                     if col not in ['user', 'email', 'applicant_id', 'data_source']]
    
#     if event_columns:
#         # Crear tabla con usuarios como filas y eventos como columnas
#         user_event_table = mongo_user_events[['user', 'email', 'data_source'] + event_columns].copy()
        
#         # Mostrar la tabla
#         st.markdown("#### Conteo de Eventos por Usuario")
#         st.dataframe(user_event_table, use_container_width=True)

# 4. ANÁLISIS DE EVENTOS
# st.markdown("## 📊 Análisis de Eventos")

# # Combinar todos los resúmenes de eventos
# all_event_summaries = []
# for key, df in data.items():
#     if 'events' in key and 'user_events' not in key:
#         all_event_summaries.append(df)

# if all_event_summaries:
#     combined_events = pd.concat(all_event_summaries, ignore_index=True)
    
#     st.markdown("#### Resumen de Eventos por Fuente")
#     st.dataframe(combined_events, use_container_width=True)

# 5. ANÁLISIS DE APLICANTES
# st.markdown("## 👥 Análisis de Aplicantes")

# # Combinar todos los archivos de aplicantes
# all_applicants = []
# for key, df in data.items():
#     if 'applicants' in key:
#         all_applicants.append(df)

# if all_applicants:
#     combined_applicants = pd.concat(all_applicants, ignore_index=True)
    
#     st.markdown("#### Datos de Aplicantes por Fuente")
    
#     # Estadísticas básicas de aplicantes
#     applicant_stats = combined_applicants.groupby('data_source').agg({
#         'user': 'count'
#     }).reset_index()
#     applicant_stats.columns = ['Fuente de Datos', 'Total de Aplicantes']
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.dataframe(applicant_stats, use_container_width=True)
    
#     with col2:
#         # Gráfico de aplicantes por fuente
#         fig_applicants = px.pie(
#             applicant_stats,
#             values='Total de Aplicantes',
#             names='Fuente de Datos',
#             title='Distribución de Aplicantes por Fuente'
#         )
#         fig_applicants.update_layout(
#             plot_bgcolor='#eaefff',
#             paper_bgcolor='#eaefff',
#             font=dict(family="Inter", size=14, color="#333"),
#             title=dict(
#                 font=dict(size=20, family="DM Sans", color="#0C1461"),
#                 x=0.5,
#                 xanchor='center'
#             )
#         )
#         st.plotly_chart(fig_applicants, use_container_width=True)

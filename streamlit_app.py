import streamlit as st
import pandas as pd
import plotly.express as px

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
encabezado_con_logo("Reporte Web - Jardines")

# Intentar diferentes nombres de archivo
csv_files = [
    "inputs/data_compilation.csv"
]

df = None
csv_path = None

for file_path in csv_files:
    try:
        # Primero leer el archivo completo para ver qué columnas están disponibles
        df_temp = pd.read_csv(file_path, nrows=1)
        available_columns = df_temp.columns.tolist()
        
        # Definir columnas que queremos leer
        desired_columns = ["event", "user", "date", "$browser", "$os", "$device", "$current_url", "distinct_id", "data_source"]
        
        # Solo leer las columnas que existen
        cols_to_read = [col for col in desired_columns if col in available_columns]
        
        # Leer el archivo con las columnas disponibles
        df = pd.read_csv(file_path, usecols=cols_to_read, low_memory=False)
        csv_path = file_path
        
        # Mostrar información sobre las columnas disponibles
        st.info(f"Columnas disponibles: {', '.join(available_columns)}")
        st.info(f"Columnas utilizadas: {', '.join(cols_to_read)}")
        
        break
    except Exception as e:
        st.error(f"Error al leer {file_path}: {str(e)}")
        continue

if df is None:
    st.error("❌ No se pudo cargar el archivo data_compilation.csv. Verifica que el archivo esté en la carpeta 'inputs'")
    st.stop()

# 🧮 ESTADÍSTICAS BÁSICAS
st.markdown("## 🧮 Estadísticas Básicas")

# 1. Número total de clics
total_clics = len(df)

# Verificar qué columnas de usuario están disponibles
user_column = None
if 'user' in df.columns:
    user_column = 'user'
elif 'userUuid' in df.columns:
    user_column = 'userUuid'
elif 'distinct_id' in df.columns:
    user_column = 'distinct_id'

if user_column:
    usuarios_unicos = df[user_column].nunique()
else:
    usuarios_unicos = 0
    st.warning("⚠️ No se encontró columna de usuario. Usando 0 como valor por defecto.")

# 2. Clics únicos vs. clics totales
clics_unicos_vs_totales = {
    "Clics Totales": total_clics,
    "Usuarios Únicos": usuarios_unicos,
    "Promedio Clics por Usuario": round(total_clics / usuarios_unicos, 2) if usuarios_unicos > 0 else 0
}

# Mostrar KPIs básicos
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi">
        <h2>{total_clics:,}</h2>
        <p>Total de Clics</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi">
        <h2>{usuarios_unicos:,}</h2>
        <p>Usuarios Únicos</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi">
        <h2>{clics_unicos_vs_totales['Promedio Clics por Usuario']}</h2>
        <p>Promedio Clics/Usuario</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Estadísticas por fuente de datos
st.markdown("### 📊 Distribución por Fuente de Datos")

if 'data_source' in df.columns:
    data_source_stats = df['data_source'].value_counts().reset_index()
    data_source_stats.columns = ['Fuente de Datos', 'Total de Registros']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Conteo por Fuente de Datos")
        st.dataframe(data_source_stats, use_container_width=True)
    
    with col2:
        # Gráfico de fuentes de datos
        fig_data_source = px.pie(
            data_source_stats, 
            values='Total de Registros', 
            names='Fuente de Datos',
            title='Distribución de Registros por Fuente de Datos'
        )
        fig_data_source.update_layout(
            plot_bgcolor='#eaefff',
            paper_bgcolor='#eaefff',
            font=dict(family="Inter", size=14, color="#333"),
            title=dict(
                font=dict(size=20, family="DM Sans", color="#0C1461"),
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_data_source, use_container_width=True)
else:
    st.info("No hay información de fuente de datos disponible")

# 4. Clics por sección o elemento (event)
st.markdown("### 📊 Clics por Sección/Elemento")

if 'event' in df.columns and user_column:
    eventos_stats = df.groupby('event').agg({
        user_column: ['count', 'nunique']
    }).round(2)

    eventos_stats.columns = ['Total Clics', 'Usuarios Únicos']
    eventos_stats = eventos_stats.reset_index()
    eventos_stats['Promedio Clics por Usuario'] = (eventos_stats['Total Clics'] / eventos_stats['Usuarios Únicos']).round(2)
    eventos_stats = eventos_stats.sort_values('Total Clics', ascending=False)

    # Mostrar top 10 eventos
    st.markdown("#### Top 10 Eventos por Total de Clics")
    st.dataframe(eventos_stats.head(10), use_container_width=True)
else:
    st.info("No hay información de eventos o usuarios disponible")

# 4. Clics por tipo de dispositivo
st.markdown("### 📱 Clics por Tipo de Dispositivo")

if '$device' in df.columns:
    device_stats = df['$device'].value_counts().reset_index()
    device_stats.columns = ['Dispositivo', 'Total Clics']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribución por Dispositivo")
        st.dataframe(device_stats, use_container_width=True)
    
    with col2:
        # Gráfico de dispositivos
        fig_device = px.pie(
            device_stats, 
            values='Total Clics', 
            names='Dispositivo',
            title='Distribución de Clics por Dispositivo'
        )
        fig_device.update_layout(
            plot_bgcolor='#eaefff',
            paper_bgcolor='#eaefff',
            font=dict(family="Inter", size=14, color="#333"),
            title=dict(
                font=dict(size=20, family="DM Sans", color="#0C1461"),
                x=0.5,
                xanchor='center'
            )
        )
        st.plotly_chart(fig_device, use_container_width=True)
else:
    st.info("No hay información de dispositivo disponible en los datos")

# 5. Clics por navegador / sistema operativo
st.markdown("### 🌐 Clics por Navegador y Sistema Operativo")

col1, col2 = st.columns(2)

with col1:
    if '$browser' in df.columns:
        browser_stats = df['$browser'].value_counts().reset_index()
        browser_stats.columns = ['Navegador', 'Total Clics']
        st.markdown("#### Distribución por Navegador")
        st.dataframe(browser_stats, use_container_width=True)
    else:
        st.info("No hay información de navegador disponible")

with col2:
    if '$os' in df.columns:
        os_stats = df['$os'].value_counts().reset_index()
        os_stats.columns = ['Sistema Operativo', 'Total Clics']
        st.markdown("#### Distribución por Sistema Operativo")
        st.dataframe(os_stats, use_container_width=True)
    else:
        st.info("No hay información de sistema operativo disponible")

# 6. Clics por URL (sección/elemento)
st.markdown("### 🔗 Clics por URL")

if '$current_url' in df.columns:
    url_stats = df['$current_url'].value_counts().reset_index()
    url_stats.columns = ['URL', 'Total Clics']
    
    st.markdown("#### Top 10 URLs por Clics")
    st.dataframe(url_stats.head(10), use_container_width=True)
    
    # Gráfico de URLs
    fig_url = px.bar(
        url_stats.head(10),
        x='URL',
        y='Total Clics',
        title='Top 10 URLs por Total de Clics'
    )
    fig_url.update_layout(
        xaxis_title="URL",
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
    fig_url.update_xaxes(tickangle=45)
    st.plotly_chart(fig_url, use_container_width=True)
else:
    st.info("No hay información de URL disponible")

# Nota sobre CTR
st.markdown("### 📈 Nota sobre Tasa de Clics (CTR)")
st.info("""
Para calcular la Tasa de Clics (CTR) necesitaríamos información sobre las impresiones (pageviews, views, etc.). 
En los datos actuales solo tenemos información de clics, por lo que no podemos calcular el CTR directamente.
""")

# Mostrar tabla de eventos recientes
st.subheader("📋 Primeros 100 eventos")
df_sample = df.head(100)
st.dataframe(df_sample)

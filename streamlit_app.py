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

st.title('Notas MongoDB')

# Leer el archivo
file_path = 'inputs/mongo_applicants_merged.csv'
df = pd.read_csv(file_path)

# Mostrar información de diagnóstico
st.write("**Información del dataset:**")
st.write(f"Columnas disponibles: {list(df.columns)}")
st.write(f"Total de filas: {len(df)}")

# Mostrar primeras filas para ver qué datos hay
st.write("**Primeras 3 filas del dataset:**")
st.dataframe(df.head(3))

# Mostrar solo las columnas user, email y data
st.write("**Tabla de notas:**")
st.dataframe(df[['user', 'email', 'data']])

import streamlit as st
import pandas as pd

st.title("Reporte de Clics - Mixpanel")

csv_path = "inputs/mixpanel_applicants_merged_20250708_100107.csv"

# Leer solo las columnas necesarias
cols = ["event", "distinct_id", "date"]
try:
    df = pd.read_csv(csv_path, usecols=lambda c: c in cols, low_memory=False)
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
    st.stop()

# Estadísticas
usuarios_unicos = df["distinct_id"].nunique()
total_clics = len(df)
promedio_clics = total_clics / usuarios_unicos if usuarios_unicos > 0 else 0

st.metric("Usuarios únicos", usuarios_unicos)
st.metric("Total de clics (eventos)", total_clics)
st.metric("Promedio de clics por usuario", f"{promedio_clics:.2f}")

# (Opcional) Mostrar tabla de eventos recientes
df_sample = df.head(100)
st.subheader("Primeros 100 eventos")
st.dataframe(df_sample)

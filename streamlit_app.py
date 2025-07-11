import pandas as pd
import streamlit as st
import ast

st.title('Notas MongoDB')

# Leer el archivo
file_path = 'reportejardines/inputs/mongo_applicants_merged.csv'
df = pd.read_csv(file_path)

# Función para extraer el texto de la nota desde la columna 'data'
def extraer_nota(data_str):
    try:
        # Convertir el string a dict
        data_dict = ast.literal_eval(data_str)
        return data_dict.get('content', '')
    except Exception:
        return ''

# Crear columna 'nota' con el texto extraído
df['nota'] = df['data'].apply(extraer_nota)

# Seleccionar usuario (user o userId)
def obtener_usuario(row):
    if pd.notnull(row['user']):
        return row['user']
    return row['userId']

df['usuario'] = df.apply(obtener_usuario, axis=1)

# Seleccionar email (si existe)
def obtener_email(row):
    if pd.notnull(row['email']):
        return row['email']
    return ''

df['correo'] = df.apply(obtener_email, axis=1)

# Mostrar la tabla final
st.dataframe(df[['usuario', 'correo', 'nota']])

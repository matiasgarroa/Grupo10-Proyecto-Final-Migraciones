import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import pandas_gbq

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

sql_indicadores = """
SELECT * FROM `pi-soy-henry.migrations.indicadores`
"""
indicadores = pandas_gbq.read_gbq(sql_indicadores, project_id='pi-soy-henry')

sql_hechos = """
SELECT * FROM `pi-soy-henry.migrations.hechos`
"""
hechos = pandas_gbq.read_gbq(sql_hechos, project_id='pi-soy-henry')

# Define los widgets de la sección izquierda
st.sidebar.title("Sección izquierda")
name = st.sidebar.text_input("Ingresa tu nombre")
age = st.sidebar.number_input("Ingresa tu edad")

# Define los widgets de la sección derecha
st.title("Sección derecha")
color = st.selectbox("¿Cuál es tu color favorito?", ["Rojo", "Azul", "Verde"])
animal = st.selectbox("¿Cuál es tu animal favorito?", ["Perro", "Gato", "Pájaro"])

# Muestra los resultados
st.write("Hola, " + name + "!")
st.write("Tienes " + str(age) + " años.")
st.write("Tu color favorito es " + color + " y tu animal favorito es el " + animal + ".")
import streamlit as st
from google.cloud import bigquery

# Carga tus credenciales desde el archivo JSON descargado
credentials_path = 'pi-soy-henry-67f5715648a9.json'
client = bigquery.Client.from_service_account_json(credentials_path)

# Ejemplo de consulta SQL
query = '''
SELECT *
FROM `hechos`
LIMIT 10
'''

# Ejecuta la consulta y almacena los resultados en un dataframe de Pandas
df = client.query(query).to_dataframe()

# Muestra los resultados en Streamlit
st.write(df)
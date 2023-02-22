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

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10")

# Print results.
st.write("Some wise words from Shakespeare:")
for row in rows:
    st.write("✍️ " + row['word'])

# Ejemplo de consulta SQL
rows = run_query("SELECT * FROM `pi-soy-henry.migrations.indicadores` LIMIT 10")

for row in rows:
    st.write(row['indicator_name'])

sql_indicadores = """
SELECT * FROM `pi-soy-henry.migrations.indicadores`
"""
indicadores = pandas_gbq.read_gbq(sql_indicadores, project_id='pi-soy-henry')

st.write(indicadores)

sql_hechos = """
SELECT * FROM `pi-soy-henry.migrations.hechos`
"""
hechos = pandas_gbq.read_gbq(sql_hechos, project_id='pi-soy-henry')
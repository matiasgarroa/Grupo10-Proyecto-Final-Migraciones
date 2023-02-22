import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

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

dataf = pd.read_gbq("SELECT * FROM `pi-soy-henry.migrations.indicadores`", credentials=credentials)

print(dataf)

QUERY = "SELECT * FROM `your-project-id.your-dataset-id.your-table-id`"

# Ejecutar la consulta y obtener los resultados como DataFrame de Pandas
df = client.query(QUERY).to_dataframe()

# Mostrar los resultados en Streamlit
st.write(df)
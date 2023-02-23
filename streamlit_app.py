import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import numpy as np

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

#Importamos datos
indicadores = run_query("SELECT * FROM `pi-soy-henry.migrations.indicadores`")
indicadores = pd.DataFrame(indicadores)

hechos = run_query("SELECT * FROM `pi-soy-henry.migrations.hechos`")
hechos = pd.DataFrame(hechos)


### Helper Methods ###
def get_unique_dates(df_data):
    #returns unique dates list in the form "YEAR" for labels
    unique_date = np.unique(df_data.anio).tolist()
    return unique_date



####################
### INTRODUCCIÓN ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Grupo10 - Analizador de Migraciones')
with row0_2:
    st.text("")
    st.subheader('Streamlit App')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("La migración es un fenómeno global que afecta a muchas personas en todo el mundo. Hay muchas razones por las que la gente decide emigrar, incluyendo motivos económicos, políticos, sociales y de seguridad. Algunos de los desafíos más comunes que enfrentan los migrantes incluyen la discriminación, la falta de recursos, apoyo, y la separación de sus seres queridos. ")
    st.markdown("Queremos proporcionarte una herramienta útil y accesible, para ayudarte tomar decisiones informadas sobre tu destino de emigración.")
    st.markdown("Podrás encontrar el codigo fuente en [PF Henry GitHub Repository](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones)")

#################
### SELECTION ###
#################

st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

### YEAR RANGE ###
st.sidebar.markdown("**First select the data range you want to analyze:** 👇")
unique_dates = get_unique_dates(hechos)
start_season, end_season = st.sidebar.select_slider('Select the year range you want to include', unique_dates, value= [1960,2019])
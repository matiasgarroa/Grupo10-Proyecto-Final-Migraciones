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
    st.markdown("Hola! La migración es un fenómeno global que afecta a muchas personas en todo el mundo. Hay muchas razones por las que la gente decide emigrar, incluyendo motivos económicos, políticos, sociales y de seguridad. Algunos de los desafíos más comunes que enfrentan los migrantes incluyen la discriminación, la falta de recursos, apoyo, y la separación de sus seres queridos. ")
    st.markdown("Queremos proporcionarte una herramienta útil y accesible, para ayudarte tomar decisiones informadas sobre tu destino de emigración.")
    st.markdown("Podrás encontrar el codigo fuente en [PF Henry GitHub Repository](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones)")
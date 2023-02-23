import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

st.set_page_config(layout="wide")

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
hechos = hechos.sort_values('anio' ,ascending=True)

### Helper Methods ###
def get_unique_anios(df_data):
    #devuelve los valores unicos de hechos['anio'] en forma de lista
    unique_anios = df_data['anio'].unique().tolist()
    return unique_anios

def get_unique_pais(df_data):
    #devuelve los valores unicos de hechos['pais'] en forma de lista
    unique_pais = df_data['pais'].unique().tolist()
    return unique_pais

def get_unique_nationality(df_data):
    #devuelve los valores unicos de hechos['nationality'] en forma de lista
    unique_nationality = df_data['nationality'].tolist()
    unique_nationality = unique_nationality.unique()
    return unique_nationality

def get_unique_cod_indicador(df_data):
    #devuelve los valores unicos de hechos['cod_indicador'] en forma de lista
    unique_cod_indicador = df_data['cod_indicador'].tolist()
    unique_cod_indicador = unique_cod_indicador.unique()
    return unique_cod_indicador

def filter_anio(df_data):
    df_filtered_anios = pd.DataFrame()
    anios = df_data['anio'].unique().tolist() #season list "13-14"
    start_raw = start_anio
    end_raw = end_anio
    start_index = anios.index(start_raw)
    end_index = anios.index(end_raw)+1
    anios_selected = anios[start_index:end_index]
    df_filtered_anios = df_data[df_data['anio'].isin(anios_selected)]
    return df_filtered_anios

def filter_pais(df_data):
    df_filtered_pais = pd.DataFrame()
    if all_paises_selected == 'Seleccione paises manualmente':
        df_filtered_pais = df_data[df_data['pais'].isin(selected_paises)]
        return df_filtered_pais
    return df_data

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

st.write(hechos.head(1))

#################
### SELECTION ###
#################

st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

### YEAR RANGE ###
st.sidebar.markdown("**Aquí puedes filtrar datos** 👇")
unique_dates = get_unique_anios(hechos)
start_anio, end_anio = st.sidebar.select_slider('Seleccione el periodo de años que desea incluir: ', unique_dates, value= [ 1960 , 2021 ])
df_data_filtered_anio = filter_anio(hechos)  

### COUNTRY SELECTION ###
unique_paises = get_unique_pais(df_data_filtered_anio)
all_paises_selected = st.sidebar.selectbox('¿Quieres incluir paises o regiones en específico? Si tu respuesta es sí, cliquea en la caja debajo y selecciona los paises en el nuevo campo.', ['Incluir todos los paises y regiones','Seleccionar paises y regiones manualmente'])
if all_paises_selected == 'Seleccionar paises y regiones manualmente':
    selected_paises = st.sidebar.multiselect("Selecciona los paises y regiones que deseas incluir en el analysis. Puedes borrar la actual selección clickeando el boton X a la derecha", unique_paises, default = unique_paises)
df_data_filtered = filter_pais(df_data_filtered_anio)   